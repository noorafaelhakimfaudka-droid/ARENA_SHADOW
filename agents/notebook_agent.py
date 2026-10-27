# ml-agents/agents/notebook_agent.py
"""
Agen 5 — Notebook Generator & Artefak Deployment (Ronde 5).
- Merakit notebook.ipynb yang mandiri dan reproducible menggunakan nbformat.
- Menjalankan ulang notebook secara otomatis dengan nbclient untuk verifikasi bebas error.
- Menyimpan model.joblib (Pipeline lengkap) dan schema.json untuk mode prediksi data baru.
- Menyimpan final state.json.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Tuple
import pandas as pd
from sklearn.pipeline import Pipeline
from core.state import SharedState
from core.tools.notebook import build_reproducible_notebook, verify_and_replay_notebook
from core.tools.predict import save_artifacts_for_prediction


def run_notebook_and_export_artifacts(
    csv_path: str,
    df_raw: pd.DataFrame,
    final_pipeline: Pipeline,
    output_dir: Path | str,
    state: SharedState
) -> Tuple[Path, Path, Path, bool]:
    """
    Menyusun notebook.ipynb, memverifikasi re-eksekusi bersih,
    serta mengekspor model.joblib dan schema.json.
    """
    out_dir = Path(output_dir)
    target_col = state.framing.get("target_column", "target")
    task_type = state.framing.get("task_type", "binary_classification")
    champion_name = state.modeling_plan.get("champion_model", "Champion Model")
    drop_cols = state.data_plan.get("drop_columns", [])
    test_metrics = state.modeling_results.get("test_metrics", {})
    top_features = state.modeling_results.get("top_features", [])

    # 1. Rakit notebook.ipynb
    nb_path = out_dir / "notebook.ipynb"
    build_reproducible_notebook(
        csv_path=csv_path,
        target_col=target_col,
        task_type=task_type,
        drop_columns=drop_cols,
        champion_model_name=champion_name,
        framing_data=state.framing,
        test_metrics=test_metrics,
        output_path=nb_path
    )

    # 2. Verifikasi Re-eksekusi Bersih via nbclient
    is_reproducible, repro_msg = verify_and_replay_notebook(nb_path)

    state.notebook_info = {
        "notebook_path": str(nb_path),
        "is_verified": is_reproducible,
        "verification_message": repro_msg
    }

    # 3. Ekspor Artefak Prediksi (M5)
    fe_plans = state.data_plan.get("feature_engineering_plans", [])
    model_p, schema_p = save_artifacts_for_prediction(
        pipeline=final_pipeline,
        df_raw=df_raw,
        target_col=target_col,
        task_type=task_type,
        champion_name=champion_name,
        test_metrics=test_metrics,
        top_features=top_features,
        output_dir=out_dir,
        fe_plans=fe_plans
    )

    state.model_path = str(model_p)
    state.schema_path = str(schema_p)

    # 4. Simpan Final state.json
    state_file = state.save_to_file(out_dir)

    return nb_path, model_p, schema_p, is_reproducible
