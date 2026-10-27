import asyncio
from pathlib import Path
from typing import List, Optional
import uuid
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from backend.app.config import settings
from backend.app.schemas import DebateDocument, SessionSummary
from backend.app.services.store import (
    delete_session,
    get_debate,
    get_notebook_path,
    list_sessions,
)
from backend.app.services.jobs import job_runner

router = APIRouter(tags=["sessions"])


@router.get("/sessions", response_model=List[SessionSummary])
async def get_sessions_list():
    return list_sessions()


@router.get("/sessions/{session_id}/debate", response_model=DebateDocument)
async def get_session_debate(session_id: str):
    doc = get_debate(session_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"Sesi '{session_id}' tidak ditemukan.")
    return doc


@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    success = delete_session(session_id)
    if not success and session_id == "demo_titanic":
        raise HTTPException(status_code=400, detail="Sesi demo tidak dapat dihapus.")
    if not success:
        raise HTTPException(status_code=404, detail=f"Sesi '{session_id}' tidak ditemukan.")
    return {"ok": True, "message": f"Sesi '{session_id}' berhasil dihapus."}


@router.post("/sessions")
async def create_new_session(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target: Optional[str] = Form(None)
):
    # Validasi tipe file
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Hanya file berformat .csv yang didukung. Silakan unggah file CSV yang valid."
        )

    # Baca byte file
    content = await file.read()
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Ukuran file ({len(content) / (1024*1024):.1f} MB) melebihi batas {settings.max_file_size_mb} MB."
        )

    if len(content.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="File CSV yang diunggah kosong."
        )

    session_id = str(uuid.uuid4())
    job_id = job_runner.create_job()

    # Jalankan background task via BackgroundTasks
    background_tasks.add_task(
        job_runner.run_pipeline_task,
        job_id=job_id,
        session_id=session_id,
        raw_bytes=content,
        filename=file.filename,
        requested_target=target
    )

    return {"job_id": job_id, "session_id": session_id}


@router.get("/sessions/{session_id}/notebook")
async def download_session_notebook(session_id: str):
    nb_path = get_notebook_path(session_id)
    if nb_path is None or not nb_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Notebook untuk sesi '{session_id}' belum siap atau tidak ditemukan."
        )

    return FileResponse(
        nb_path,
        media_type="application/x-ipynb+json",
        filename=f"shadow_arena_{session_id}.ipynb",
        headers={"Content-Disposition": f"attachment; filename=shadow_arena_{session_id}.ipynb"}
    )
