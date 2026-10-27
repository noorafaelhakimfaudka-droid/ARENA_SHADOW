import json
import shutil
from pathlib import Path
from typing import Any, List, Optional
import joblib

from backend.app.config import settings
from backend.app.schemas import DebateDocument, SessionSummary


def get_session_dir(session_id: str) -> Path:
    return settings.sessions_dir / session_id


def create_session(session_id: str, raw_bytes: bytes, filename: str) -> Path:
    s_dir = get_session_dir(session_id)
    s_dir.mkdir(parents=True, exist_ok=True)
    raw_path = s_dir / "raw.csv"
    raw_path.write_bytes(raw_bytes)

    meta_info = {
        "session_id": session_id,
        "dataset_name": filename,
    }
    (s_dir / "meta.json").write_text(json.dumps(meta_info), encoding="utf-8")
    return s_dir


def save_debate(session_id: str, doc: DebateDocument):
    s_dir = get_session_dir(session_id)
    s_dir.mkdir(parents=True, exist_ok=True)
    debate_path = s_dir / "debate.json"
    with open(debate_path, "w", encoding="utf-8") as f:
        json.dump(doc.model_dump(), f, indent=2, ensure_ascii=False)


def get_debate(session_id: str) -> Optional[DebateDocument]:
    # Jika meminta demo_titanic
    if session_id == "demo_titanic":
        demo_path = settings.data_dir / "demo_titanic.debate.json"
        if demo_path.exists():
            with open(demo_path, "r", encoding="utf-8") as f:
                return DebateDocument.model_validate(json.load(f))

    s_dir = get_session_dir(session_id)
    debate_path = s_dir / "debate.json"
    if not debate_path.exists():
        return None
    with open(debate_path, "r", encoding="utf-8") as f:
        return DebateDocument.model_validate(json.load(f))


def save_model(session_id: str, model_obj: Any):
    s_dir = get_session_dir(session_id)
    model_path = s_dir / "model.joblib"
    joblib.dump(model_obj, model_path)


def list_sessions() -> List[SessionSummary]:
    summaries: List[SessionSummary] = []

    # Sertakan demo jika ada
    demo_path = settings.data_dir / "demo_titanic.debate.json"
    if demo_path.exists():
        try:
            with open(demo_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                meta = d.get("meta", {})
                champ = None
                for lb in d.get("leaderboard", []):
                    if lb.get("champion"):
                        champ = lb.get("model")
                summaries.append(SessionSummary(
                    session_id="demo_titanic",
                    dataset_name=meta.get("dataset_name", "titanic.csv"),
                    target=meta.get("problem", {}).get("target", "survived"),
                    champion=champ,
                    created_at=meta.get("created_at", ""),
                    n_rows=meta.get("n_rows", 891),
                    n_cols=meta.get("n_cols", 12),
                    mode="demo"
                ))
        except Exception:
            pass

    if not settings.sessions_dir.exists():
        return summaries

    for p in sorted(settings.sessions_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if not p.is_dir():
            continue
        debate_file = p / "debate.json"
        if debate_file.exists():
            try:
                with open(debate_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    meta = d.get("meta", {})
                    champ = None
                    for lb in d.get("leaderboard", []):
                        if lb.get("champion"):
                            champ = lb.get("model")
                    summaries.append(SessionSummary(
                        session_id=p.name,
                        dataset_name=meta.get("dataset_name", "dataset.csv"),
                        target=meta.get("problem", {}).get("target", "-"),
                        champion=champ,
                        created_at=meta.get("created_at", ""),
                        n_rows=meta.get("n_rows", 0),
                        n_cols=meta.get("n_cols", 0),
                        mode=meta.get("mode", "offline")
                    ))
            except Exception:
                continue

    return summaries


def delete_session(session_id: str) -> bool:
    if session_id == "demo_titanic":
        return False
    s_dir = get_session_dir(session_id)
    if s_dir.exists():
        shutil.rmtree(s_dir, ignore_errors=True)
        return True
    return False


def get_notebook_path(session_id: str) -> Optional[Path]:
    if session_id == "demo_titanic":
        nb = settings.sessions_dir / "demo_titanic" / "shadow_arena.ipynb"
        if nb.exists():
            return nb
    s_dir = get_session_dir(session_id)
    nb_path = s_dir / "shadow_arena.ipynb"
    if nb_path.exists():
        return nb_path
    return None
