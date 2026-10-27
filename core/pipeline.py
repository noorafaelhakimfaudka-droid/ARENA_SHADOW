# ml-agents/core/pipeline.py
"""
Orkestrator Utama Pipeline SHADOW Multi-Agent Machine Learning.
Menyediakan antarmuka terpadu `run_pipeline` untuk eksekusi 5 tahap sekuensial agen:
1. Problem Framer
2. Data Wrangler
3. Model Guardian
4. Insight Storyteller
5. Notebook Builder
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from main import cmd_train
from core.state import SharedState


def run_pipeline(
    csv_file: str | Path,
    target: Optional[str] = None,
    out: Optional[str | Path] = None,
    progress_cb: Optional[Callable[[str, str, Optional[Dict[str, Any]]], None]] = None,
    **kwargs
) -> SharedState:
    """
    Menjalankan pipeline 5 agen secara terprogram.
    
    Args:
        csv_file: Path ke dataset tabular (.csv).
        target: Nama kolom target (opsional, jika kosong agen Problem Framer akan menentukan).
        out: Folder output artefak (opsional, default: outputs/run_<timestamp>).
        progress_cb: Callback untuk Streamlit atau visualisasi live progress.
        
    Returns:
        SharedState: Objek state bersama yang berisi seluruh hasil kalkulasi, metrik, dan artefak.
    """
    args = argparse.Namespace(
        csv_file=str(csv_file),
        target=target or "",
        out=str(out) if out else ""
    )
    return cmd_train(args, progress_cb=progress_cb, **kwargs)
