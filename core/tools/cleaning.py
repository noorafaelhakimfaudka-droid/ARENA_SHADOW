# ml-agents/core/tools/cleaning.py
"""
Tool Data Cleaning & Preprocessing Scikit-Learn Murni.
- Menyusun ColumnTransformer Scikit-Learn yang aman (zero data leakage).
- Fit HANYA pada data train (fit-in-fold).
- Mendukung imputasi median/mean/most_frequent, OneHotEncoder, dan StandardScaler.
- Menjalankan rekayasa fitur turunan sederhana (rasio 2 kolom numerik).
- Dilarang memanggil LLM (Murni komputasi Scikit-Learn).
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler, StandardScaler


def build_preprocessor_pipeline(
    numeric_columns: List[str],
    categorical_columns: List[str],
    num_impute: str = "median",
    cat_impute: str = "most_frequent",
    scaler: str = "standard"
) -> ColumnTransformer:
    """
    Membangun Scikit-Learn ColumnTransformer terpadu.
    Menjamin preprocessing fit-in-fold secara deterministik.
    """
    transformers = []

    # 1. Pipeline Numerik: Imputasi + Penskalaan
    if numeric_columns:
        num_steps = [("imputer", SimpleImputer(strategy=num_impute))]
        if scaler == "standard":
            num_steps.append(("scaler", StandardScaler()))
        elif scaler == "robust":
            num_steps.append(("scaler", RobustScaler()))
        
        num_pipe = Pipeline(steps=num_steps)
        transformers.append(("num", num_pipe, numeric_columns))

    # 2. Pipeline Kategorikal: Imputasi + OneHotEncoder (max_categories=25 mencegah ledakan dimensi)
    if categorical_columns:
        cat_steps = [
            ("imputer", SimpleImputer(strategy=cat_impute)),
            ("onehot", OneHotEncoder(max_categories=25, handle_unknown="ignore", sparse_output=False))
        ]
        cat_pipe = Pipeline(steps=cat_steps)
        transformers.append(("cat", cat_pipe, categorical_columns))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )
    return preprocessor


def apply_simple_feature_engineering(
    df: pd.DataFrame,
    plans: Optional[List[Dict[str, str]]] = None
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Menerapkan maksimal 1-2 fitur turunan sederhana jika diusulkan oleh Feature Strategist.
    Contoh: Rasio dua kolom numerik atau ekstraksi tanggal.
    """
    df_out = df.copy()
    created_features: List[str] = []
    
    if not plans:
        return df_out, created_features

    for item in plans[:2]:  # Batasi maksimal 2 fitur sesuai Scope PRD
        name = item.get("name", "").strip()
        formula = item.get("formula", "").strip()
        if not name or not formula:
            continue
        
        try:
            # Contoh pola: "rasio colA terhadap colB" atau "colA / colB"
            if "/" in formula:
                parts = [p.strip() for p in formula.split("/")]
                if len(parts) == 2 and parts[0] in df_out.columns and parts[1] in df_out.columns:
                    col_a, col_b = parts[0], parts[1]
                    s_a = pd.to_numeric(df_out[col_a], errors="coerce").fillna(0.0).astype(float)
                    s_b = pd.to_numeric(df_out[col_b], errors="coerce").fillna(0.0).astype(float)
                    denom = s_b.replace(0.0, np.nan)
                    df_out[name] = (s_a / denom).fillna(0.0)
                    created_features.append(name)
            elif "*" in formula:
                parts = [p.strip() for p in formula.split("*")]
                if len(parts) == 2 and parts[0] in df_out.columns and parts[1] in df_out.columns:
                    col_a, col_b = parts[0], parts[1]
                    s_a = pd.to_numeric(df_out[col_a], errors="coerce").fillna(0.0).astype(float)
                    s_b = pd.to_numeric(df_out[col_b], errors="coerce").fillna(0.0).astype(float)
                    df_out[name] = s_a * s_b
                    created_features.append(name)
            elif "+" in formula:
                parts = [p.strip() for p in formula.split("+")]
                if len(parts) == 2 and parts[0] in df_out.columns and parts[1] in df_out.columns:
                    col_a, col_b = parts[0], parts[1]
                    s_a = pd.to_numeric(df_out[col_a], errors="coerce").fillna(0.0).astype(float)
                    s_b = pd.to_numeric(df_out[col_b], errors="coerce").fillna(0.0).astype(float)
                    df_out[name] = s_a + s_b
                    created_features.append(name)
        except Exception:
            pass

    return df_out, created_features


def prepare_features_and_target(
    df: pd.DataFrame,
    target_col: str,
    drop_columns: Optional[List[str]] = None,
    fe_plans: Optional[List[Dict[str, str]]] = None
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str], List[str]]:
    """
    Mengeksekusi pembersihan awal data tabular:
    1. Membuang kolom yang ditentukan Auditor/Skeptic (ID, konstan, leakage).
    2. Memisahkan X (fitur) dan y (target).
    3. Menerapkan rekayasa fitur turunan sederhana jika ada.
    4. Mengklasifikasikan kolom numerik dan kategorikal yang tersisa.
    """
    if target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ditemukan di dataset!")

    df_clean = df.copy()
    drops_to_apply = [c for c in (drop_columns or []) if c in df_clean.columns and c != target_col]
    
    if drops_to_apply:
        df_clean = df_clean.drop(columns=drops_to_apply)

    # Ekstraksi target
    y = df_clean[target_col].copy()
    X = df_clean.drop(columns=[target_col]).copy()

    # Rekayasa fitur jika ada usulan
    X, new_feats = apply_simple_feature_engineering(X, fe_plans)

    # Identifikasi tipe fitur akhir
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

    return X, y, num_cols, cat_cols, drops_to_apply
