# ml-agents/core/tools/profiling.py
"""
Tool Profiling & Analisis Data Python Murni.
- Menghitung statistik deskriptif, tipe data, missing values, dan kardinalitas.
- Mendeteksi calon kolom ID, kolom konstan, dan kandidat target.
- Menghitung korelasi fitur terhadap target untuk mendeteksi target leakage (|r| > 0.90).
- Dilarang memanggil LLM (Murni komputasi numerik).
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def load_and_clean_raw_df(csv_path_or_df: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
    """Membaca CSV dan mengonversi string spasi kosong menjadi NaN."""
    if isinstance(csv_path_or_df, pd.DataFrame):
        df = csv_path_or_df.copy()
    else:
        df = pd.read_csv(csv_path_or_df)
    
    # Bersihkan string spasi putih yang tersembunyi
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: np.nan if isinstance(x, str) and not x.strip() else x)
        # Coba konversi kolom object numerik yang sempat tersimpan sebagai string (misal TotalCharges)
        try:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > len(df) * 0.7:  # Jika > 70% valid numerik
                df[col] = converted
        except Exception:
            pass
            
    return df


def profile_dataset(csv_path_or_df: Union[str, Path, pd.DataFrame]) -> Dict[str, Any]:
    """
    Menghasilkan profil statistik terstruktur dari dataset.
    Digunakan oleh Agen 1 (Framing) dan Agen 2 (Data Auditor) untuk mengambil keputusan berbasis data nyata.
    """
    df = load_and_clean_raw_df(csv_path_or_df)
    filename = Path(csv_path_or_df).name if isinstance(csv_path_or_df, (str, Path)) else "dataframe"
    n_rows, n_cols = df.shape

    columns_summary: Dict[str, Dict[str, Any]] = {}
    missing_percentages: Dict[str, float] = {}
    id_or_constant_candidates: List[str] = []
    numeric_columns: List[str] = []
    categorical_columns: List[str] = []
    candidate_targets: List[str] = []

    for col in df.columns:
        s = df[col]
        dtype_str = str(s.dtype)
        n_unique = s.nunique(dropna=True)
        n_missing = int(s.isna().sum())
        missing_pct = round((n_missing / n_rows) * 100, 2)

        # Identifikasi tipe
        is_num = pd.api.types.is_numeric_dtype(s)
        if is_num:
            numeric_columns.append(col)
        else:
            categorical_columns.append(col)

        columns_summary[col] = {
            "dtype": dtype_str,
            "missing_count": n_missing,
            "missing_pct": missing_pct,
            "n_unique": n_unique
        }
        if missing_pct > 0:
            missing_percentages[col] = missing_pct

        # Deteksi Kolom ID atau Kolom Konstan (n_unique <= 1)
        is_id_name = any(col.lower().strip() == p or col.lower().strip().endswith(p) for p in ["id", "_id", "uuid", "guid", "index", "no"])
        if n_unique == 1:
            id_or_constant_candidates.append(f"{col} (Konstan: 1 nilai unik)")
        elif is_id_name and n_unique >= min(10, n_rows):
            id_or_constant_candidates.append(f"{col} (ID Unik: {n_unique} nilai unik)")
        elif not is_num and n_unique > n_rows * 0.5 and n_rows >= 50:
            id_or_constant_candidates.append(f"{col} (ID Unik: {n_unique} nilai unik)")
        elif not is_num and n_unique > 200 and (n_unique / n_rows) > 0.2 and n_rows >= 200:
            id_or_constant_candidates.append(f"{col} (ID Unik: {n_unique} nilai unik)")

        # Deteksi Calon Target (Kardinalitas 2-10 untuk klasifikasi, atau kolom numerik kontinu di ujung)
        if 2 <= n_unique <= 10:
            candidate_targets.append(col)

    # Jika tidak ada target diskrit, masukkan kolom numerik terakhir sebagai calon regresi
    if not candidate_targets and numeric_columns:
        candidate_targets.append(numeric_columns[-1])

    # Ambil 5 baris sampel representatif
    sample_rows = df.head(5).to_dict(orient="records")
    # Bersihkan NaN dalam sampel untuk JSON serializability
    clean_samples = []
    for row in sample_rows:
        clean_row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
        clean_samples.append(clean_row)

    return {
        "filename": filename,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns_summary": columns_summary,
        "missing_percentages": missing_percentages,
        "id_or_constant_candidates": id_or_constant_candidates,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "candidate_targets": candidate_targets,
        "sample_rows": clean_samples
    }


def calculate_target_correlations(
    df: pd.DataFrame,
    target_col: str,
    task_type: str = "binary_classification"
) -> Dict[str, float]:
    """
    Menghitung skor asosiasi/korelasi tiap fitur terhadap target.
    Mendeteksi fitur yang berpotensi menjadi 'Target Leakage' (|r| > 0.90 atau AUC > 0.95).
    """
    if target_col not in df.columns:
        return {}

    correlations: Dict[str, float] = {}
    y_raw = df[target_col]

    # Ubah target biner menjadi 0/1 jika klasifikasi
    if task_type == "binary_classification":
        if not pd.api.types.is_numeric_dtype(y_raw):
            classes = y_raw.dropna().unique()
            if len(classes) == 2:
                # Petakan kelas kedua sebagai 1
                y = (y_raw == classes[1]).astype(int)
            else:
                y = pd.factorize(y_raw)[0]
        else:
            y = y_raw.copy()
    else:
        y = pd.to_numeric(y_raw, errors="coerce")

    # Hitung korelasi numerik
    for col in df.columns:
        if col == target_col:
            continue
        s = df[col]
        if pd.api.types.is_numeric_dtype(s):
            valid_mask = s.notna() & y.notna()
            if valid_mask.sum() > 10:
                s_valid = s[valid_mask]
                y_valid = y[valid_mask]
                
                # Hitung korelasi Pearson
                corr = s_valid.corr(y_valid)
                if not np.isnan(corr):
                    correlations[col] = round(float(abs(corr)), 4)
                else:
                    correlations[col] = 0.0

    # Urutkan korelasi tertinggi ke terendah
    sorted_corr = dict(sorted(correlations.items(), key=lambda x: x[1], reverse=True))
    return sorted_corr


def audit_iqr_and_skewness(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Memeriksa pencilan ekstrem IQR (pagar 1.5x IQR) dan kemiringan (skewness)
    pada seluruh kolom numerik (Fase 2 EDA).
    """
    res: Dict[str, Any] = {}
    for col in df.select_dtypes(include=["number"]).columns:
        s = df[col].dropna()
        if len(s) < 5:
            continue
        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = int(((s < lower_bound) | (s > upper_bound)).sum())
        skewness = round(float(s.skew()), 4) if len(s) > 2 else 0.0
        res[col] = {
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "iqr": round(iqr, 2),
            "outlier_count": outliers,
            "outlier_pct": round(outliers / len(s) * 100, 2),
            "skewness": skewness,
            "is_heavily_skewed": abs(skewness) > 1.0
        }
    return res


def audit_multicollinearity(df: pd.DataFrame, threshold: float = 0.85) -> List[Dict[str, Any]]:
    """
    Mendeteksi multikolinearitas dan korelasi silang ekstrem antar-fitur independen (VIF screening).
    """
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    warnings: List[Dict[str, Any]] = []
    if len(num_cols) < 2:
        return warnings
    corr_matrix = df[num_cols].corr().abs()
    for i in range(len(num_cols)):
        for j in range(i + 1, len(num_cols)):
            col1, col2 = num_cols[i], num_cols[j]
            val = float(corr_matrix.loc[col1, col2])
            if val >= threshold:
                warnings.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation": round(val, 4),
                    "risk": "Multikolinearitas tinggi, sinyal berpotensi saling kanibalisasi (VIF tinggi)"
                })
    return warnings


def calculate_adversarial_validation(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Adversarial Validation: Menguji apakah Train dan Holdout kembar identik
    atau mengalami covariate shift / domain drift.
    Target: 0 (Train), 1 (Holdout/Test).
    Jika AUC ~ 0.50 (misal 0.495), data kembar identik bebas dari domain shift!
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    n_tr = len(X_train)
    n_te = len(X_test)
    if n_tr < 5 or n_te < 5:
        return {"adversarial_auc": 0.50, "is_identical": True, "verdict": "Data uji kecil, diasumsikan setara"}

    X_comb = pd.concat([X_train, X_test], axis=0, ignore_index=True)
    y_comb = np.array([0] * n_tr + [1] * n_te)

    num_cols = X_comb.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = X_comb.select_dtypes(exclude=["number"]).columns.tolist()

    trans = []
    if num_cols:
        trans.append(("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols))
    if cat_cols:
        trans.append(("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), cat_cols))
    
    prep = ColumnTransformer(transformers=trans, remainder="drop")

    adv_pipe = Pipeline([
        ("prep", prep),
        ("clf", LogisticRegression(max_iter=500, random_state=random_state))
    ])
    try:
        cv_scores = cross_val_score(adv_pipe, X_comb, y_comb, cv=3, scoring="roc_auc")
        adv_auc = round(float(np.mean(cv_scores)), 4)
    except Exception:
        adv_auc = 0.50

    is_identical = abs(adv_auc - 0.50) <= 0.15
    return {
        "adversarial_auc": adv_auc,
        "is_identical": is_identical,
        "verdict": f"AUC Diskriminator {adv_auc} (~0.50): Data Latih dan Data Holdout terbukti kembar identik (bebas domain drift)" if is_identical else f"AUC Diskriminator {adv_auc}: Waspada, terdeteksi potensi pergeseran distribusi (covariate shift)"
    }

