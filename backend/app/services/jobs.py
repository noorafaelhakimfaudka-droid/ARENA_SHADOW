import asyncio
import logging
from typing import AsyncGenerator, Dict, List, Optional
import uuid

from backend.app.schemas import JobProgressEvent
from backend.app.services.dataset import load_csv_safely, DatasetValidationError
from backend.app.services.problem import infer_problem
from backend.app.services.modeling import run_full_modeling_pipeline
from backend.app.services.insights import generate_insights
from backend.app.services.orchestrator import build_debate_document
from backend.app.services.notebook_builder import build_and_execute_notebook
from backend.app.services.store import (
    create_session,
    save_debate,
    save_model,
)

logger = logging.getLogger("shadow_arena.jobs")


class JobRunner:
    def __init__(self):
        self.job_events: Dict[str, List[JobProgressEvent]] = {}
        self.listeners: Dict[str, List[asyncio.Queue]] = {}

    def create_job(self) -> str:
        job_id = str(uuid.uuid4())
        self.job_events[job_id] = []
        self.listeners[job_id] = []
        return job_id

    def emit_progress(
        self,
        job_id: str,
        step: int,
        agent: str,
        message: str,
        pct: int,
        done: bool = False,
        error: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        evt = JobProgressEvent(
            step=step,
            agent=agent,
            message=message,
            pct=pct,
            done=done,
            error=error,
            session_id=session_id
        )
        if job_id in self.job_events:
            self.job_events[job_id].append(evt)

        # Broadcast ke semua listener aktif
        for q in self.listeners.get(job_id, []):
            try:
                q.put_nowait(evt)
            except Exception:
                pass

    async def run_pipeline_task(
        self,
        job_id: str,
        session_id: str,
        raw_bytes: bytes,
        filename: str,
        requested_target: Optional[str] = None
    ):
        try:
            # 1. Simpan CSV awal
            session_dir = create_session(session_id, raw_bytes, filename)
            self.emit_progress(
                job_id, 1, "wrangler", "Memvalidasi dan memuat file CSV...", 5
            )

            # 2. Muat dan validasi dataset
            df, ds_name = load_csv_safely(raw_bytes)

            # 3. Inferensi masalah
            self.emit_progress(
                job_id, 2, "framer", "Menganalisis problem statement dan target...", 15
            )
            prob = infer_problem(df, requested_target=requested_target)

            # 4. Pipeline ML nyata dengan progress callback
            def ml_progress_cb(step_idx: int, agent_name: str, msg: str, percent: int):
                self.emit_progress(job_id, step_idx + 2, agent_name, msg, percent)

            ml_results = await asyncio.to_thread(
                run_full_modeling_pipeline, df, prob, ml_progress_cb
            )

            # 5. Ekstraksi Insight
            self.emit_progress(
                job_id, 6, "storyteller", "Mengekstrak pola segmentasi dan storytelling...", 85
            )
            insights = await asyncio.to_thread(
                generate_insights, df, prob.target, ml_results
            )

            # 6. Rakit & eksekusi Notebook
            self.emit_progress(
                job_id, 7, "notebook", "Merakit dan memvalidasi notebook .ipynb...", 92
            )
            nb_info = {"filename": "shadow_arena.ipynb", "valid": True, "cells_count": 28}

            # 7. Rakit Dokumen Debat
            doc = await asyncio.to_thread(
                build_debate_document,
                session_id=session_id,
                dataset_name=filename,
                df=df,
                problem=prob,
                ml_results=ml_results,
                insights_data=insights,
                notebook_info=nb_info
            )

            # Bangun notebook sesungguhnya dari rounds debat
            nb_path, nb_valid, nb_cells = await asyncio.to_thread(
                build_and_execute_notebook,
                session_dir=session_dir,
                csv_filename=filename,
                problem=prob,
                rounds=doc.rounds,
                ml_results=ml_results
            )
            doc.notebook.valid = nb_valid
            doc.notebook.cells_count = nb_cells

            # Simpan debate.json dan model.joblib
            save_debate(session_id, doc)
            if "champion_pipe" in ml_results:
                save_model(session_id, ml_results["champion_pipe"])

            # Selesai
            self.emit_progress(
                job_id, 8, "notebook", "Debat dan perakitan model berhasil selesai!", 100,
                done=True, session_id=session_id
            )

        except DatasetValidationError as dve:
            logger.warning(f"Validasi dataset gagal: {str(dve)}")
            self.emit_progress(
                job_id, 0, "framer", f"Gagal: {str(dve)}", 0,
                done=False, error=str(dve)
            )
        except Exception as e:
            logger.error(f"Job {job_id} gagal tidak terduga: {str(e)}", exc_info=True)
            err_msg = f"Terjadi kesalahan saat memproses data: {str(e)[:150]}"
            self.emit_progress(
                job_id, 0, "guardian", err_msg, 0,
                done=False, error=err_msg
            )

    async def event_generator(self, job_id: str) -> AsyncGenerator[str, None]:
        if job_id not in self.job_events:
            err_evt = JobProgressEvent(
                step=0, agent="system", message="Job tidak ditemukan", pct=0, error="Job ID tidak valid"
            )
            yield f"data: {err_evt.model_dump_json()}\n\n"
            return

        # Buat queue lokal pada event loop request saat ini
        q: asyncio.Queue = asyncio.Queue()
        if job_id not in self.listeners:
            self.listeners[job_id] = []
        self.listeners[job_id].append(q)

        # Kirim semua event yang sudah terjadi sebelumnya
        already_done = False
        sent_count = 0
        existing_events = list(self.job_events[job_id])
        for evt in existing_events:
            yield f"data: {evt.model_dump_json()}\n\n"
            sent_count += 1
            if evt.done or evt.error:
                already_done = True
                break

        if already_done:
            if q in self.listeners.get(job_id, []):
                self.listeners[job_id].remove(q)
            return

        try:
            while True:
                try:
                    evt: JobProgressEvent = await asyncio.wait_for(q.get(), timeout=30.0)
                    yield f"data: {evt.model_dump_json()}\n\n"
                    if evt.done or evt.error:
                        break
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            if job_id in self.listeners and q in self.listeners[job_id]:
                self.listeners[job_id].remove(q)


job_runner = JobRunner()
