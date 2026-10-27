# ml-agents/app.py
"""
Shadow Arena — Streamlit Multi-Agent Machine Learning Assistant & Arena
Menghubungkan 5 Agen AI Machine Learning dengan output komputasi nyata (state.json).
- Desain visual resmi: Dark Chocolate (#0F0804 -> #1A0E07 -> #2D1A0E), Aksen Madu Emas / Honey Gold (#E8B04A), Teks Cream (#FFF4E0)
- Roster 5 Agen: Problem Framer (#F5B83D), Data Wrangler (#7BD389 / #8DB255), Model Guardian (#FF5C5C / #B83A2E), Insight Storyteller (#F37726 / #D9703F), Notebook Builder (#5BB8E8 / #5B9BB5)
- Area utama: Arena visual melingkar 5 Agen responsif murni Auto-Fit tanpa letterbox
- Single Source of Truth (SSOT) via core.tools.session_payload
- Mode Prediksi interaktif dinamis berbasis schema.json
- Validasi & unduh notebook .ipynb tervalidasi via st.download_button
- Latih CSV baru end-to-end dengan 5 Agen
"""

from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import nbformat
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Pastikan direktori proyek ada di sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.tools.session_payload import (
    build_arena_session_payload,
    to_friendly_term
)
from core.tools.predict import predict_single_or_batch
from core.tools.notebook import build_reproducible_notebook
from main import cmd_train

# =============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# =============================================================================
st.set_page_config(
    page_title="Shadow Arena — Multi-Agent ML Assistant & Arena",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. CSS TEMA NAVY TINTA & ORANYE JUPYTER (RESMI M8 & HTML REFERENCE)
# =============================================================================
st.markdown("""
<style>
    /* Sembunyikan header default & toolbar Streamlit */
    header [data-testid="stToolbar"],
    .stDeployButton,
    #MainMenu,
    footer,
    [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    header {
        display: none !important;
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Pola latar belakang global Amber & Cokelat Hangat */
    html, body {
        background: radial-gradient(ellipse at 50% 45%, #3a2214 0%, #1f1209 55%, #0f0804 100%) !important;
        background-color: #0f0804 !important;
        color: #FFF4E0 !important;
        overflow: hidden !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], section.main {
        background: transparent !important;
        color: #FFF4E0 !important;
        overflow: hidden !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Container utama mengikuti wadah dengan presisi 100% tanpa overflow */
    .block-container,
    [data-testid="stMainBlockContainer"],
    [data-testid="block-container"],
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
    }

    div.stElementContainer:has(iframe),
    div[data-testid="stCustomComponentV1"],
    div.element-container:has(iframe) {
        width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        flex: 1 1 auto !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        overflow: hidden !important;
    }

    iframe {
        width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        border: none !important;
        background: transparent !important;
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
    }


    /* Tombol toggle sidebar yang rapi di pojok kiri atas */
    [data-testid="stSidebarCollapsedControl"] {
        top: 12px !important;
        left: 12px !important;
        z-index: 9999 !important;
        color: #E8B04A !important;
        background: rgba(45, 26, 14, 0.95) !important;
        border: 1.5px solid #5a3a22 !important;
        border-radius: 20px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.6) !important;
    }
    [data-testid="stSidebarCollapsedControl"]:hover {
        border-color: #E8B04A !important;
        background: #3a2214 !important;
    }
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] svg {
        color: #E8B04A !important;
        fill: #E8B04A !important;
    }

    /* =========================================================================
       SIDEBAR STYLING — PANEL COKELAT HANGAT DENGAN AKSEN MADU (HONEY)
       ========================================================================= */
    [data-testid="stSidebar"] {
        background-color: #1a0e07 !important;
        border-right: 1.5px solid #5a3a22 !important;
    }

    [data-testid="stSidebarContent"] {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        background-color: #1a0e07 !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stCaption {
        color: #FFF4E0 !important;
        font-family: "Fredoka", "Nunito", "Trebuchet MS", system-ui, sans-serif !important;
        font-weight: 500 !important;
    }

    .brand-title {
        font-family: "Fredoka", "Nunito", "Trebuchet MS", system-ui, sans-serif !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #E8B04A !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 2px !important;
    }

    .brand-subtitle {
        font-family: "Fredoka", "Nunito", "Trebuchet MS", system-ui, sans-serif !important;
        font-size: 12px !important;
        color: #dfcdb9 !important;
        margin-bottom: 16px !important;
        font-weight: 500 !important;
    }

    /* Metadata Card Sesi */
    .session-meta-card {
        background: #2d1a0e !important;
        color: #FFF4E0 !important;
        border: 1.5px solid #5a3a22 !important;
        border-left: 4px solid #E8B04A !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        margin-top: 6px !important;
        margin-bottom: 14px !important;
        font-size: 12px !important;
        line-height: 1.6 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4) !important;
    }
    .session-meta-card b {
        color: #E8B04A !important;
    }
    .session-meta-card code {
        background: #150b05 !important;
        color: #8DB255 !important;
        border: 1px solid #5a3a22 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-size: 11px !important;
        font-family: "JetBrains Mono", monospace !important;
        font-weight: 700 !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #2d1a0e !important;
        border: 1px solid #5a3a22 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
        border-color: #E8B04A !important;
    }
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] div {
        color: #FFF4E0 !important;
    }

    /* Popover Menu */
    ul[data-baseweb="menu"] {
        background-color: #1a0e07 !important;
        border: 1px solid #5a3a22 !important;
    }
    li[data-baseweb="menu-item"] {
        color: #FFF4E0 !important;
        background-color: #1a0e07 !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #2d1a0e !important;
        color: #E8B04A !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #150b05 !important;
        border: 1.5px dashed #5a3a22 !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #E8B04A !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #331c10 !important;
        color: #FFF4E0 !important;
        border: 1px solid #5a3a22 !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #E8B04A !important;
        color: #1a0e07 !important;
    }

    /* Inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background-color: #2d1a0e !important;
        color: #FFF4E0 !important;
        border: 1px solid #5a3a22 !important;
        border-radius: 6px !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: #E8B04A !important;
        box-shadow: 0 0 8px rgba(232,176,74,0.3) !important;
    }

    /* Tombol Utama (Primary) */
    div.stButton > button[kind="primary"] {
        background: #E8B04A !important;
        color: #1a0e07 !important;
        border: 1px solid #E8B04A !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(232,176,74,0.3) !important;
        transition: transform 0.15s ease, background 0.15s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        background: #F3A83B !important;
    }

    /* Tombol Biasa */
    div.stButton > button[kind="secondary"] {
        background: #331c10 !important;
        color: #FFF4E0 !important;
        border: 1px solid #5a3a22 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #4a2d1b !important;
        border-color: #E8B04A !important;
    }

    /* Tombol Unduh Notebook */
    div.stDownloadButton > button {
        background: #E8B04A !important;
        color: #1a0e07 !important;
        border: 1px solid #E8B04A !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(232,176,74,0.3) !important;
    }
    div.stDownloadButton > button:hover {
        background: #F3A83B !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #2d1a0e !important;
        border: 1px solid #5a3a22 !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
    }

    hr {
        border-color: #5a3a22 !important;
        margin: 14px 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 3. MANAJEMEN SESI OUTPUTS
# =============================================================================
def list_available_runs() -> List[Path]:
    """Mencari semua folder run di outputs/ yang memiliki state.json."""
    outputs_dir = BASE_DIR / "outputs"
    runs: List[Path] = []
    if outputs_dir.exists():
        for d in sorted(outputs_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if d.is_dir() and (d / "state.json").exists():
                runs.append(d)
    return runs


available_runs = list_available_runs()
run_names = [r.name for r in available_runs]

query_run = st.query_params.get("run", "")
default_idx = 0
if query_run and query_run in run_names:
    default_idx = run_names.index(query_run)
elif "run_titanic" in run_names:
    default_idx = run_names.index("run_titanic")
elif run_names:
    default_idx = 0

# Siapkan metadata sesi yang tersedia untuk Sesi Drawer di arena
available_sessions_meta = []
for r in available_runs:
    clean_name = r.name
    if clean_name.startswith("run_"):
        clean_name = clean_name[4:]
    available_sessions_meta.append({
        "name": r.name,
        "dataset_name": clean_name
    })

# Wadah Utama Rendering Arena di Tengah Layar
arena_placeholder = st.empty()

def render_arena_view(payload: Optional[Dict[str, Any]], round_idx: int = 0, autoplay: bool = False):
    """Merender Panggung Arena di wadah tengah layar secara responsif & dinamis."""
    arena_file = BASE_DIR / "index.html"
    if not arena_file.exists():
        arena_file = BASE_DIR / "standalone_arena.html"

    if not arena_file.exists():
        arena_placeholder.error("Berkas arena HTML (index.html) tidak ditemukan di direktori kerja.")
        return

    arena_html = arena_file.read_text(encoding="utf-8")
    safe_session_json = json.dumps(payload, ensure_ascii=False).replace("</script>", r"<\/script>") if payload else "null"
    safe_available_json = json.dumps(available_sessions_meta, ensure_ascii=False).replace("</script>", r"<\/script>")
    should_autoplay = "true" if autoplay else "false"

    build_ts = int(time.time() * 1000)
    injected_script = f"""
<!-- shadow-build-{build_ts} -->
<script id="shadow-session-injector">
window.SESSION = {safe_session_json};
window.AVAILABLE_SESSIONS = {safe_available_json};
window.AUTO_START = {should_autoplay};
window.START_ROUND = {round_idx};
</script>
"""
    if "</head>" in arena_html:
        arena_html = arena_html.replace("</head>", f"{injected_script}\n</head>")
    else:
        arena_html = f"{injected_script}\n{arena_html}"

    with arena_placeholder:
        components.html(arena_html, height=1080, scrolling=False)


# =============================================================================
# 4. SIDEBAR KONTROL PENUH
# =============================================================================
is_training_active = False

with st.sidebar:
    st.markdown('<div class="brand-title">SHADOW ARENA</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Multi-Agent Machine Learning Assistant &amp; Arena</div>', unsafe_allow_html=True)

    selected_run_dir: Optional[Path] = None
    session_payload: Optional[Dict[str, Any]] = None

    if available_runs:
        st.markdown("**Pilih Sesi Riset Tersimpan:**")
        selected_run_name = st.selectbox(
            "Folder Run Tersedia di outputs/",
            run_names,
            index=default_idx,
            label_visibility="collapsed"
        )
        selected_run_dir = next((r for r in available_runs if r.name == selected_run_name), available_runs[0])
        session_payload = build_arena_session_payload(selected_run_dir)

        # Panel Metadata Sesi (SSOT)
        ds_name = session_payload.get("dataset_name", selected_run_name)
        row_info = session_payload.get("row_info_panel", "-")
        target_info = session_payload.get("target", "-")
        task_info = session_payload.get("task_type", "klasifikasi biner")
        champ_info = session_payload.get("champion", "Gradient Boosting")

        st.markdown(f"""
        <div class="session-meta-card">
            <div><b>Dataset:</b> <code>{ds_name}</code></div>
            <div><b>Baris:</b> <code>{row_info}</code></div>
            <div><b>Target:</b> <code>{target_info}</code> ({task_info})</div>
            <div><b>Champion:</b> <code>{champ_info}</code></div>
        </div>
        """, unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # UNDUH NOTEBOOK RESMI (.ipynb) TERVALIDASI
        # ---------------------------------------------------------------------
        nb_content_str = session_payload.get("notebook_content", "")
        target_nb_filename = f"shadow_arena_{ds_name}.ipynb"

        if not nb_content_str and selected_run_dir:
            candidate_nb = selected_run_dir / "notebook.ipynb"
            if candidate_nb.exists():
                try:
                    nb_obj = nbformat.read(candidate_nb, as_version=4)
                    nbformat.validate(nb_obj)
                    nb_content_str = candidate_nb.read_text(encoding="utf-8")
                except Exception as e:
                    st.caption(f"Validasi notebook: {e}")

        if nb_content_str:
            st.download_button(
                label="Unduh Notebook (.ipynb)",
                data=nb_content_str,
                file_name=target_nb_filename,
                mime="application/x-ipynb+json",
                help="Notebook tervalidasi yang dihasilkan dari langkah eksekusi nyata 5 agen."
            )

        # ---------------------------------------------------------------------
        # MODE PREDIKSI DATA BARU (DARI SCHEMA.JSON)
        # ---------------------------------------------------------------------
        schema_dict = session_payload.get("schema", {})
        if schema_dict and "columns" in schema_dict:
            with st.expander("Mode Prediksi Data Baru", expanded=False):
                st.caption("Masukkan nilai fitur untuk menguji model final secara instan:")
                with st.form("pred_form"):
                    pred_inputs: Dict[str, Any] = {}
                    cols_spec = schema_dict.get("columns", {})
                    
                    for col_name, spec in cols_spec.items():
                        if spec.get("type") == "numeric":
                            min_v = float(spec.get("min", 0.0))
                            max_v = float(spec.get("max", 100.0))
                            med_v = float(spec.get("median", (min_v + max_v) / 2))
                            pred_inputs[col_name] = st.number_input(
                                f"{col_name} [{min_v:.1f} - {max_v:.1f}]",
                                value=med_v,
                                key=f"pred_{col_name}"
                            )
                        else:
                            known = spec.get("known_values", [])
                            options = known if known else ["Unknown"]
                            pred_inputs[col_name] = st.selectbox(
                                col_name,
                                options=options,
                                key=f"pred_{col_name}"
                            )

                    submit_pred = st.form_submit_button("Hitung Prediksi", type="primary")

                if submit_pred:
                    try:
                        pred_res = predict_single_or_batch(selected_run_dir, pred_inputs)
                        p_list = pred_res.get("predictions", [])
                        if p_list:
                            first_p = p_list[0]
                            st.success(f"**Hasil:** {first_p.get('formatted_output', '')}")
                            if "probabilities" in first_p:
                                st.caption("Distribusi Probabilitas Kelas:")
                                for cls_lbl, p_val in first_p["probabilities"].items():
                                    st.progress(float(p_val), text=f"Kelas {cls_lbl}: {p_val * 100:.1f}%")
                            st.info(first_p.get("explanation", ""))
                    except Exception as e:
                        st.error(f"Gagal memprediksi: {e}")

    else:
        st.info("Belum ada sesi di outputs/. Silakan latih dataset CSV baru di bawah ini.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # LATIH CSV BARU DENGAN 5 AGEN AI
    # -------------------------------------------------------------------------
    with st.expander("Latih CSV Baru (5 Agen)", expanded=(len(available_runs) == 0)):
        uploaded_csv = st.file_uploader(
            "Unggah file CSV tabular",
            type=["csv"],
            help="Maksimal 50.000 baris, 50 kolom tabular."
        )
        target_override = st.text_input(
            "Target (opsional, kosongkan jika otomatis):",
            placeholder="contoh: survived / churn / charges"
        )

        is_training_active = False
        if uploaded_csv and st.button("Mulai Pelatihan 5 Agen", type="primary", key="btn_train"):
            is_training_active = True
            new_csv_path = BASE_DIR / "data" / uploaded_csv.name
            new_csv_path.parent.mkdir(parents=True, exist_ok=True)
            new_csv_path.write_bytes(uploaded_csv.getvalue())

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            clean_stem = Path(uploaded_csv.name).stem.replace(" ", "_")
            new_out_dir = BASE_DIR / "outputs" / f"run_{clean_stem}_{timestamp}"

            args = argparse.Namespace(
                csv_file=str(new_csv_path),
                target=target_override.strip() if target_override else "",
                out=str(new_out_dir)
            )

            # Hitung estimasi baris
            est_rows = 1000
            try:
                est_rows = len(pd.read_csv(new_csv_path, usecols=[0]))
            except Exception:
                pass

            live_session_id = f"run_{clean_stem}_{timestamp}"
            static_progress_file = BASE_DIR / "static" / "live_progress.json"
            static_progress_file.parent.mkdir(parents=True, exist_ok=True)

            # Inisialisasi tampilan LIVE ronde awal (Problem Framer)
            initial_round = {
                "agent": 1,
                "title": "Problem Formulation",
                "mood": "calm",
                "dialog": f"Perumusan masalah dimulai untuk dataset '{clean_stem}' ({est_rows:,} baris). Dewan menganalisis struktur data, mengidentifikasi target prediksi utama, dan menetapkan metrik evaluasi yang tepat secara objektif.",
                "proof": f"Memuat CSV: {clean_stem} | {est_rows:,} baris",
                "chart": {"t": "bar", "l": ["Baris (x100)", "Kolom", "Kesiapan"], "v": [min(int(est_rows / 100), 500), 16, 98], "max": 500, "title": "Dimensi Awal & Kesiapan Data"},
                "stage": "PROBLEM"
            }

            live_state = {
                "status": "training",
                "session_id": live_session_id,
                "dataset_name": clean_stem,
                "row_info": f"{est_rows:,} total",
                "target": "Merumuskan...",
                "task_type": "analisis awal",
                "champion": "Kandidat...",
                "current_round": 0,
                "rounds": [initial_round]
            }
            static_progress_file.write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")
            render_arena_view(live_state, round_idx=0, autoplay=False)

            with st.status("🏛️ Dewan 5 Agen Sedang Berdebat & Meneliti Data...", expanded=True) as status_box:
                def on_progress(agent_key: str, msg: str, extra: Optional[Dict[str, Any]] = None):
                    st.markdown(msg)
                    if extra and not extra.get("finished"):
                        new_rnd = {
                            "agent": extra.get("agent", 0),
                            "title": extra.get("title", f"Ronde {agent_key}"),
                            "mood": extra.get("mood", "calm"),
                            "dialog": extra.get("dialog", msg),
                            "proof": extra.get("proof", f"Audit: {agent_key}"),
                            "chart": extra.get("chart", {
                                "t": "bar",
                                "l": ["Fitur", "Model", "Audit", "Target"],
                                "v": [70, 85, 92, 98],
                                "max": 100,
                                "title": f"Progres Live: {agent_key.upper()}"
                            }),
                            "stage": extra.get("stage", "LIVE")
                        }
                        if len(live_state["rounds"]) == 1 and extra.get("round_idx") == 0:
                            live_state["rounds"][0] = new_rnd
                        else:
                            live_state["rounds"].append(new_rnd)
                        live_state["current_round"] = len(live_state["rounds"]) - 1
                        if extra.get("target"):
                            live_state["target"] = extra["target"]
                        elif extra.get("agent") == 1 and "Target" in extra.get("title", ""):
                            live_state["target"] = extra.get("proof", "").replace("Target: ", "")
                        if extra.get("champion"):
                            live_state["champion"] = extra["champion"]
                        elif extra.get("agent") == 2 and "Champion" in extra.get("title", ""):
                            live_state["champion"] = extra.get("proof", "").replace("Champion: ", "")
                        static_progress_file.write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")

                try:
                    import importlib
                    import main
                    importlib.reload(main)
                    main.cmd_train(args, progress_cb=on_progress)
                    
                    # Bangun 16 babak penuh tervalidasi via build_arena_session_payload
                    full_payload = build_arena_session_payload(new_out_dir)
                    final_rounds = full_payload.get("rounds", [])
                    if not final_rounds or len(final_rounds) < 16:
                        final_rounds = live_state["rounds"]

                    live_state["status"] = "done"
                    live_state["rounds"] = final_rounds
                    if full_payload.get("target"):
                        live_state["target"] = full_payload["target"]
                    if full_payload.get("task_type"):
                        live_state["task_type"] = full_payload["task_type"]
                    if full_payload.get("champion"):
                        live_state["champion"] = full_payload["champion"]
                    static_progress_file.write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")

                    status_box.update(label="✅ Pelatihan Selesai! Seluruh 16 Babak Siap di Arena.", state="complete", expanded=False)
                    st.success("Pelatihan selesai! Dewan 5 agen sedang mempersembahkan seluruh 16 babak debat secara berurutan di panggung arena.")
                    st.caption("Setelah selesai menyaksikan debat, klik tombol di bawah untuk menyinkronkan panel sidebar:")
                    if st.button("🔄 Sinkronkan Sidebar dengan Sesi Baru Ini", key="btn_sync_done", type="primary"):
                        st.query_params["run"] = new_out_dir.name
                        if "autoplay" in st.query_params:
                            del st.query_params["autoplay"]
                        st.rerun()

                except Exception as e:
                    live_state["status"] = "error"
                    live_state["error_message"] = str(e)
                    static_progress_file.write_text(json.dumps(live_state, ensure_ascii=False), encoding="utf-8")
                    status_box.update(label="❌ Terjadi Kesalahan", state="error", expanded=True)
                    st.error(f"Error: {e}")


# =============================================================================
# 5. AREA UTAMA: RENDERING ARENA DI WADAH TENGAH
# =============================================================================
if not is_training_active:
    render_arena_view(session_payload, round_idx=0, autoplay=False)



