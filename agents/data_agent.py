# ml-agents/agents/data_agent.py
"""
Agen 2 — Data Understanding & Cleaning Plan (Ronde 2 Debat).
Kolaborasi & Debat:
- FEATURE STRATEGIST: Merancang strategi imputasi, encoding, scaling, dan rekayasa fitur turunan.
- DATA AUDITOR: Mengaudit integritas kolom, memburu kolom ID/konstan, dan mendeteksi Target Leakage (|r| > 0.90).
- SKEPTIC: Memvalidasi rencana pembersihan dan memveto fitur bocor.
Eksekusi Python: Membangun ColumnTransformer Scikit-Learn dan menyiapkan X & y.
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from agents.base_agent import BaseAgent
from agents.personas import DATA_AUDITOR, FEATURE_STRATEGIST, SKEPTIC, build_data_cleaning_prompt
from core.llm import GeminiClient
from core.state import SharedState
from core.tools.cleaning import build_preprocessor_pipeline, prepare_features_and_target
from core.tools.profiling import (
    calculate_target_correlations,
    profile_dataset,
    audit_iqr_and_skewness,
    audit_multicollinearity
)


def run_data_cleaning_debate(
    df: pd.DataFrame,
    target_col: str,
    task_type: str,
    state: SharedState,
    client: GeminiClient
) -> Tuple[pd.DataFrame, pd.Series, ColumnTransformer, List[str], List[str]]:
    """
    Menjalankan debat Ronde 2 (Data Cleaning & Anti-Leakage) secara dinamis menggunakan Gemini.
    Mengeksekusi ColumnTransformer yang aman (zero leakage).
    """
    # 1. Analisis fakta korelasi & profiling oleh Python
    profile = profile_dataset(df)
    correlations = calculate_target_correlations(df, target_col=target_col, task_type=task_type)
    iqr_data = audit_iqr_and_skewness(df)
    vif_warnings = audit_multicollinearity(df)

    agent_aud = BaseAgent(DATA_AUDITOR, client=client)
    agent_feat = BaseAgent(FEATURE_STRATEGIST, client=client)
    agent_skep = BaseAgent(SKEPTIC, client=client)

    # Langkah 1: Data Auditor mengidentifikasi kolom berbahaya & leakage
    prompt_aud = build_data_cleaning_prompt(
        profiling_data=profile,
        target_col=target_col,
        target_correlations=correlations
    )
    aud_res = agent_aud.think_and_decide(
        prompt=prompt_aud,
        round_name="Ronde 2: Data & Leakage Audit",
        state=state,
        stance="AUDIT_LEAKAGE"
    )

    drop_candidates = [item.get("column") for item in aud_res.get("drop_columns", []) if item.get("column")]
    # Tambahkan kolom ID otomatis dari profiling Python jika ada yang belum terdeteksi
    for id_info in profile.get("id_or_constant_candidates", []):
        col_name = id_info.split()[0]
        if col_name in df.columns and col_name not in drop_candidates:
            drop_candidates.append(col_name)

    # Langkah 2: Feature Strategist merancang preprocessing
    prompt_feat = f"""
Data Auditor merekomendasikan membuang kolom: {drop_candidates}
Daftar korelasi fitur tersisa: {correlations}
Kolom numerik: {profile.get('numeric_columns')}
Kolom kategorikal: {profile.get('categorical_columns')}

Sebagai FEATURE STRATEGIST:
1. Tentukan strategi imputasi numerik ('median' atau 'mean') dan kategorikal ('most_frequent').
2. Tentukan penskalaan numerik ('standard' atau 'robust').
3. Usulkan maksimal 1 rekayasa fitur turunan rasio sederhana (contoh: 'colA / colB') jika relevan, atau kosongkan.
Keluarkan HANYA JSON:
{{
  "num_impute": "median",
  "cat_impute": "most_frequent",
  "scaler": "standard",
  "feature_engineering": [
    {{"name": "nama_fitur", "formula": "colA / colB"}}
  ],
  "feature_notes": "string penjelasan strategi preprocessing"
}}
"""
    feat_res = agent_feat.think_and_decide(
        prompt=prompt_feat,
        round_name="Ronde 2: Data & Leakage Audit",
        state=state,
        stance="STRATEGI_PREPROCESSING"
    )

    # Langkah 3: Skeptic memberikan persetujuan
    prompt_skep = f"""
Rencana Pembersihan Data:
- Kolom yang Dibuang: {drop_candidates}
- Imputasi: Numerik={feat_res.get('num_impute')}, Kategori={feat_res.get('cat_impute')}
- Scaling: {feat_res.get('scaler')}
- Rekayasa Fitur: {feat_res.get('feature_engineering')}

Sebagai SKEPTIC, pastikan tidak ada data leakage yang lolos ke training.
Keluarkan HANYA JSON: {{"decision": "APPROVE atau VETO", "skeptic_audit": "string evaluasi integritas"}}
"""
    skep_res = agent_skep.think_and_decide(
        prompt=prompt_skep,
        round_name="Ronde 2: Data & Leakage Audit",
        state=state,
        stance="VERIFIKASI_PREPROCESSING"
    )

    # 2. Eksekusi Scikit-Learn oleh Python murni
    fe_plans = feat_res.get("feature_engineering", [])
    X, y, num_cols, cat_cols, final_drops = prepare_features_and_target(
        df=df,
        target_col=target_col,
        drop_columns=drop_candidates,
        fe_plans=fe_plans
    )

    preprocessor = build_preprocessor_pipeline(
        numeric_columns=num_cols,
        categorical_columns=cat_cols,
        num_impute=feat_res.get("num_impute", "median"),
        cat_impute=feat_res.get("cat_impute", "most_frequent"),
        scaler=feat_res.get("scaler", "standard")
    )

    state.data_plan = {
        "drop_columns": final_drops,
        "imputation": {"num": feat_res.get("num_impute", "median"), "cat": feat_res.get("cat_impute", "most_frequent")},
        "scaler": feat_res.get("scaler", "standard"),
        "engineered_features": [f["name"] for f in fe_plans if "name" in f],
        "feature_engineering_plans": fe_plans,
        "skeptic_verdict": skep_res.get("skeptic_audit", "Approved"),
        "iqr_outliers": iqr_data,
        "multicollinearity_warnings": vif_warnings
    }

    state.data_execution = {
        "final_feature_count": X.shape[1],
        "numeric_features": num_cols,
        "categorical_features": cat_cols
    }

    return X, y, preprocessor, num_cols, cat_cols
