from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def detect_leakage(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    threshold: float = 0.85
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Mendeteksi dan membuang kolom kebocoran data (target leakage & ID columns):
    1. Kolom ID-like (kardinalitas >= 95% dari jumlah baris).
    2. Kolom duplikat / salinan persis label.
    3. Kolom dengan |r| > threshold (0.85) terhadap target.
    
    Fitur bocor dibuang dari train DAN test set.
    """
    n_train = len(X_train)
    leaky_info: Dict[str, Dict[str, Any]] = {}

    # Siapkan y numerik untuk korelasi
    if pd.api.types.is_numeric_dtype(y_train):
        y_num = y_train.fillna(y_train.median()).values
    else:
        y_num = pd.factorize(y_train)[0]

    for col in X_train.columns:
        series = X_train[col]
        nunique = series.nunique(dropna=True)
        reason = None
        corr_val = 0.0

        # 1. Cek ID-like columns (hanya untuk object/string atau integer berurutan)
        if n_train >= 30 and (nunique / n_train >= 0.95):
            is_id_type = False
            col_lower = str(col).lower()
            if not pd.api.types.is_numeric_dtype(series):
                is_id_type = True
            elif pd.api.types.is_integer_dtype(series) or (series.dropna() % 1 == 0).all():
                # Integer: cek apakah rentang berurutan atau nama kolom mengindikasikan ID
                vals = series.dropna().sort_values()
                if (vals.diff().dropna() == 1).mean() > 0.8 or any(k in col_lower for k in ["id", "uuid", "index", "code", "key"]):
                    is_id_type = True
            elif any(k in col_lower for k in ["id", "uuid", "index", "code", "key"]):
                is_id_type = True

            if is_id_type:
                reason = f"ID-like (kardinalitas {nunique}/{n_train} = {nunique/n_train:.1%})"
                leaky_info[col] = {"reason": reason, "corr": 0.0, "type": "id"}
                continue

        # 2. Cek salinan label langsung / korelasi tinggi
        if pd.api.types.is_numeric_dtype(series):
            clean_s = series.fillna(series.median()).values
            if np.std(clean_s) > 1e-8 and np.std(y_num) > 1e-8:
                r = np.corrcoef(clean_s, y_num)[0, 1]
                if np.isnan(r):
                    r = 0.0
                corr_val = abs(float(r))
        else:
            # Categorical: factorize atau Cramér's V
            fact_s = pd.factorize(series)[0]
            if len(np.unique(fact_s)) > 1 and np.std(y_num) > 1e-8:
                r = np.corrcoef(fact_s, y_num)[0, 1]
                if np.isnan(r):
                    r = 0.0
                corr_val = abs(float(r))

        if corr_val >= 0.999:
            reason = f"Salinan persis target (|r| = {corr_val:.2f})"
            leaky_info[col] = {"reason": reason, "corr": round(corr_val, 3), "type": "duplicate"}
        elif corr_val > threshold:
            reason = f"Korelasi ekstrem dengan target (|r| = {corr_val:.2f} > {threshold})"
            leaky_info[col] = {"reason": reason, "corr": round(corr_val, 3), "type": "high_corr"}

    leaky_cols = list(leaky_info.keys())

    # Buang dari train dan test
    X_train_clean = X_train.drop(columns=leaky_cols)
    X_test_clean = X_test.drop(columns=leaky_cols)

    # Susun teks bukti audit
    if leaky_cols:
        first_col = leaky_cols[0]
        first_corr = leaky_info[first_col]["corr"]
        evidence = f"{first_col}: |r|={first_corr:.2f} > {threshold} → DIBUANG"
        passed = False
    else:
        evidence = f"Audit kebocoran bersih: 0 kolom bocor (|r| < {threshold})"
        passed = True

    report = {
        "leaky_columns": leaky_cols,
        "details": leaky_info,
        "passed": passed,
        "evidence": evidence,
        "dropped_count": len(leaky_cols)
    }

    return X_train_clean, X_test_clean, report
