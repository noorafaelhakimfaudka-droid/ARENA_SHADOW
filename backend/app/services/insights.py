from typing import Any, Dict, List
import pandas as pd


def generate_insights(
    df: pd.DataFrame,
    target_col: str,
    modeling_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Mengekstrak temuan substantif dari data dan evaluasi model,
    termasuk rate per grup/segmen dan permutation importance fitur.
    """
    clean_df = df.dropna(subset=[target_col]).copy()
    y_series = clean_df[target_col]

    # Cek rata-rata target per kategori untuk fitur berkardinalitas rendah (<= 6)
    group_rates: Dict[str, Dict[str, float]] = {}

    cat_cols = clean_df.select_dtypes(exclude=["number"]).columns.tolist()
    # Tambahkan pclass jika ada
    col_map = {c.lower(): c for c in clean_df.columns}
    if "pclass" in col_map and col_map["pclass"] not in cat_cols:
        cat_cols.append(col_map["pclass"])

    for col in cat_cols:
        if clean_df[col].nunique() <= 6:
            try:
                # Jika target biner/numerik, hitung mean target per grup
                if pd.api.types.is_numeric_dtype(y_series):
                    rates = clean_df.groupby(col, observed=True)[target_col].mean()
                    group_rates[col] = {
                        str(k): round(float(v) * 100, 1)
                        for k, v in rates.items()
                    }
            except Exception:
                continue

    # Ambil top fitur dari permutation importance
    perm_imp = modeling_results.get("final_eval", {}).get("permutation_importance", [])
    top_features = perm_imp[:5]

    return {
        "group_rates": group_rates,
        "top_features": top_features,
    }
