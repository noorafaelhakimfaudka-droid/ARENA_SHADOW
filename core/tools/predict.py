# ml-agents/core/tools/predict.py
"""
Tool Serialisasi & Mode Prediksi Data Baru (M5).
- Menyimpan seluruh Pipeline Scikit-Learn ke model.joblib.
- Menyimpan schema.json (kolom wajib, tipe data, rentang min/max, kategori yang dikenal).
- Memvalidasi input data baru secara ketat:
  * Kolom wajib tidak boleh hilang.
  * Tipe data divalidasi.
  * Memberi peringatan jika numerik di luar rentang latih atau kategori belum pernah dilihat.
- Menghasilkan prediksi:
  * Klasifikasi: Label prediksi dan probabilitas tiap kelas.
  * Regresi: Nilai prediksi dan rentang error berdasarkan MAE test set.
  * Penjelasan pengaruh fitur utama (Feature Importance) murni berbasis komputasi Python.
- Dilarang memanggil LLM (Murni komputasi Scikit-Learn).
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def save_artifacts_for_prediction(
    pipeline: Pipeline,
    df_raw: pd.DataFrame,
    target_col: str,
    task_type: str,
    champion_name: str,
    test_metrics: Dict[str, Any],
    top_features: List[Dict[str, Any]],
    output_dir: Path | str,
    fe_plans: Optional[List[Dict[str, str]]] = None
) -> Tuple[Path, Path]:
    """
    Menyimpan model.joblib dan schema.json ke dalam folder outputs/<run_id>/.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Simpan model.joblib (Pipeline Lengkap)
    model_path = out_dir / "model.joblib"
    joblib.dump(pipeline, model_path)

    # 2. Susun schema.json berbasis kolom fitur yang benar-benar dipakai model
    model_input_cols = []
    if hasattr(pipeline, "named_steps") and "preprocessor" in pipeline.named_steps:
        preprocessor = pipeline.named_steps["preprocessor"]
        if hasattr(preprocessor, "transformers"):
            for name, trans, cols in preprocessor.transformers:
                if name != "remainder" and hasattr(cols, "__iter__"):
                    for c in cols:
                        if c in df_raw.columns and c not in model_input_cols:
                            model_input_cols.append(c)

    # Tambahkan kolom sumber formula jika ada fitur turunan
    if fe_plans:
        for plan in fe_plans:
            formula = plan.get("formula", "")
            for c in df_raw.columns:
                if c in formula and c not in model_input_cols and c != target_col:
                    model_input_cols.append(c)

    if model_input_cols:
        feature_cols = model_input_cols
        drop_cols_detected = [c for c in df_raw.columns if c != target_col and c not in model_input_cols]
    else:
        feature_cols = [c for c in df_raw.columns if c != target_col]
        drop_cols_detected = []

    column_schemas: Dict[str, Dict[str, Any]] = {}

    for col in feature_cols:
        s = df_raw[col]
        if pd.api.types.is_numeric_dtype(s):
            column_schemas[col] = {
                "type": "numeric",
                "min": float(s.min()) if s.notna().any() else 0.0,
                "max": float(s.max()) if s.notna().any() else 0.0,
                "median": float(s.median()) if s.notna().any() else 0.0
            }
        else:
            column_schemas[col] = {
                "type": "categorical",
                "known_values": [str(v) for v in s.dropna().unique().tolist()[:50]]
            }

    schema_data = {
        "target_column": target_col,
        "task_type": task_type,
        "champion_model_name": champion_name,
        "test_metrics": test_metrics,
        "columns": column_schemas,
        "drop_columns": drop_cols_detected,
        "top_features": top_features,
        "feature_engineering": fe_plans or []
    }

    schema_path = out_dir / "schema.json"
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2, ensure_ascii=False)

    return model_path, schema_path


def load_model_and_schema(run_dir: Path | str) -> Tuple[Pipeline, Dict[str, Any]]:
    """Membaca model.joblib dan schema.json dari folder run."""
    r_dir = Path(run_dir)
    model_path = r_dir / "model.joblib"
    schema_path = r_dir / "schema.json"

    if not model_path.exists():
        raise FileNotFoundError(f"Berkas model tidak ditemukan di {model_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Berkas schema tidak ditemukan di {schema_path}")

    pipeline = joblib.load(model_path)
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    return pipeline, schema


def validate_input_dataframe(df_input: pd.DataFrame, schema: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
    """
    Memvalidasi data input baru terhadap schema.json.
    Mengembalikan: (df_validated, daftar_peringatan).
    """
    warnings: List[str] = []
    columns_spec = schema.get("columns", {})
    df_clean = df_input.copy()

    drop_cols = set(schema.get("drop_columns", []))
    for col, spec in columns_spec.items():
        if col in drop_cols:
            continue  # Kolom yang dibuang saat training diabaikan sesuai Scope Bagian 5
        if col not in df_clean.columns:
            # DoD Poin 8: Input salah atau kolom hilang wajib ditolak secara transparan
            raise ValueError(f"Input ditolak: Kolom wajib '{col}' tidak ditemukan dalam data input (DoD Poin 8).")
        else:
            # Validasi rentang numerik
            if spec["type"] == "numeric":
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
                min_val, max_val = spec.get("min", -np.inf), spec.get("max", np.inf)
                out_of_bounds = df_clean[(df_clean[col] < min_val) | (df_clean[col] > max_val)]
                if len(out_of_bounds) > 0:
                    warnings.append(f"Kolom '{col}' memiliki nilai di luar rentang latih [{min_val:.2f}, {max_val:.2f}].")
            else:
                # Validasi kategori
                known_cats = set(spec.get("known_values", []))
                unseen = set(df_clean[col].dropna().astype(str).unique()) - known_cats
                if unseen:
                    warnings.append(f"Kolom '{col}' memiliki kategori baru yang belum pernah dilihat: {list(unseen)[:3]}.")

    return df_clean, warnings


def predict_single_or_batch(
    run_dir: Path | str,
    input_data: Union[Dict[str, Any], pd.DataFrame]
) -> Dict[str, Any]:
    """
    Menjalankan prediksi pada data baru (satu baris dict atau DataFrame batch):
    - Mengembalikan label prediksi, probabilitas/margin error, peringatan, dan penjelasan fitur.
    """
    pipeline, schema = load_model_and_schema(run_dir)
    task_type = schema.get("task_type", "binary_classification")
    target_col = schema.get("target_column", "target")
    top_features = schema.get("top_features", [])

    if isinstance(input_data, dict):
        df_in = pd.DataFrame([input_data])
    else:
        df_in = input_data.copy()

    # Terapkan rekayasa fitur turunan dari schema jika ada
    from core.tools.cleaning import apply_simple_feature_engineering
    fe_plans = schema.get("feature_engineering", [])
    if fe_plans:
        df_in, _ = apply_simple_feature_engineering(df_in, fe_plans)

    df_validated, warnings = validate_input_dataframe(df_in, schema)

    # Eksekusi prediksi via Pipeline
    preds = pipeline.predict(df_validated)

    results: List[Dict[str, Any]] = []
    
    # Ambil probabilitas jika klasifikasi
    probas = None
    if hasattr(pipeline, "predict_proba"):
        try:
            probas = pipeline.predict_proba(df_validated)
        except Exception:
            pass

    test_mae = schema.get("test_metrics", {}).get("mae", 0.0)

    for i in range(len(df_validated)):
        row_res: Dict[str, Any] = {}
        pred_val = preds[i]

        if task_type in ("binary_classification", "multiclass_classification"):
            row_res["prediction"] = str(pred_val)
            if probas is not None:
                classes = pipeline.classes_
                prob_dict = {str(c): round(float(p), 4) for c, p in zip(classes, probas[i])}
                row_res["probabilities"] = prob_dict
                max_prob = max(prob_dict.values())
                row_res["formatted_output"] = f"{target_col} = {pred_val} (Probabilitas: {max_prob * 100:.1f}%)"
            else:
                row_res["formatted_output"] = f"{target_col} = {pred_val}"
        else:  # Regression
            val = float(pred_val)
            row_res["prediction"] = round(val, 2)
            row_res["error_margin"] = round(float(test_mae), 2)
            row_res["formatted_output"] = f"{target_col} = {val:,.2f} ± {test_mae:,.2f} (Estimasi MAE)"

        # Susun penjelasan pengaruh fitur berbasis data Python murni
        feat_expl = []
        if top_features:
            for tf in top_features[:3]:
                feat_expl.append(f"Fitur '{tf['feature']}' (Tingkat pengaruh: {tf['importance']})")
        row_res["explanation"] = (
            f"Keputusan prediksi sangat dipengaruhi oleh: {', '.join(feat_expl)}."
            if feat_expl else "Prediksi dihitung dari kombinasi seluruh fitur pada model."
        )
        results.append(row_res)

    return {
        "target_column": target_col,
        "task_type": task_type,
        "champion_model": schema.get("champion_model_name", "Champion"),
        "warnings": warnings,
        "predictions": results
    }
