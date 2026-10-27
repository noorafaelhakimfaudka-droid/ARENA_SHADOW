from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def compute_vif_for_features(df_numeric: pd.DataFrame) -> Dict[str, float]:
    """
    Menghitung Variance Inflation Factor (VIF) untuk setiap fitur numerik.
    VIF = 1 / (1 - R^2)
    """
    vifs: Dict[str, float] = {}
    cols = list(df_numeric.columns)
    if len(cols) <= 1:
        return {cols[0]: 1.0} if cols else {}

    # Imputasi sederhana untuk menghitung VIF
    clean_df = df_numeric.fillna(df_numeric.median()).copy()

    for col in cols:
        y = clean_df[col].values
        X = clean_df.drop(columns=[col]).values

        # Hindari varians nol
        if np.std(y) < 1e-6 or np.std(X) < 1e-6:
            vifs[col] = 1.0
            continue

        try:
            model = LinearRegression().fit(X, y)
            r2 = model.score(X, y)
            if r2 >= 0.9999:
                vif = 999.0
            else:
                vif = 1.0 / (1.0 - r2)
            vifs[col] = round(float(vif), 2)
        except Exception:
            vifs[col] = 1.0

    return vifs


def engineer_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    vif_threshold: float = 5.0
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Melakukan rekayasa fitur generik dan domain pada data train dan test,
    serta menyaring fitur dengan Variance Inflation Factor (VIF) < threshold.
    """
    Xtr = X_train.copy()
    Xte = X_test.copy()

    engineered_candidates: Dict[str, Tuple[pd.Series, pd.Series]] = {}

    # 1. Aturan domain Titanic / hubungan keluarga
    col_map = {c.lower(): c for c in Xtr.columns}
    if "sibsp" in col_map and "parch" in col_map:
        s_col = col_map["sibsp"]
        p_col = col_map["parch"]
        if pd.api.types.is_numeric_dtype(Xtr[s_col]) and pd.api.types.is_numeric_dtype(Xtr[p_col]):
            fam_tr = Xtr[s_col].fillna(0) + Xtr[p_col].fillna(0) + 1
            fam_te = Xte[s_col].fillna(0) + Xte[p_col].fillna(0) + 1
            engineered_candidates["family_size"] = (fam_tr, fam_te)

            alone_tr = (fam_tr == 1).astype(int)
            alone_te = (fam_te == 1).astype(int)
            engineered_candidates["is_alone"] = (alone_tr, alone_te)

    # 2. Rasio / interaksi numerik generik
    num_cols = Xtr.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 2 and len(engineered_candidates) < 3:
        c1, c2 = num_cols[0], num_cols[1]
        denom_tr = Xtr[c2].astype(float).abs() + 1e-4
        denom_te = Xte[c2].astype(float).abs() + 1e-4
        ratio_tr = Xtr[c1].astype(float) / denom_tr
        ratio_te = Xte[c1].astype(float) / denom_te
        engineered_candidates[f"{c1}_div_{c2}"] = (ratio_tr, ratio_te)

    # Uji VIF satu per satu
    accepted_features: List[str] = []
    rejected_features: List[str] = []
    vif_scores: Dict[str, float] = {}

    current_num = Xtr.select_dtypes(include=[np.number]).copy()

    for feat_name, (tr_series, te_series) in engineered_candidates.items():
        trial_num = current_num.copy()
        trial_num[feat_name] = tr_series

        trial_vifs = compute_vif_for_features(trial_num)
        feat_vif = trial_vifs.get(feat_name, 1.0)

        if feat_vif < vif_threshold:
            # Fitur lolos skrining multikolinearitas
            Xtr[feat_name] = tr_series
            Xte[feat_name] = te_series
            current_num[feat_name] = tr_series
            accepted_features.append(feat_name)
            vif_scores[feat_name] = feat_vif
        else:
            rejected_features.append(feat_name)
            vif_scores[feat_name] = feat_vif

    # Hitung VIF akhir untuk semua fitur numerik
    final_vifs = compute_vif_for_features(Xtr.select_dtypes(include=[np.number]))
    max_vif = max(final_vifs.values()) if final_vifs else 1.0

    if accepted_features:
        evidence = f"{', '.join(accepted_features[:2])} | VIF max={max_vif:.1f} < {vif_threshold}"
    else:
        evidence = f"Fitur eksisting optimal | VIF max={max_vif:.1f} < {vif_threshold}"

    report = {
        "accepted_features": accepted_features,
        "rejected_features": rejected_features,
        "vif_scores": final_vifs,
        "max_vif": max_vif,
        "evidence": evidence
    }

    return Xtr, Xte, report
