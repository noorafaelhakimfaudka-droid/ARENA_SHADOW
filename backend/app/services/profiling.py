from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from backend.app.schemas import DatasetProfile, ClassBalanceItem, TopMissingItem, PreviewData


def profile_dataset(df: pd.DataFrame, target_col: Optional[str] = None) -> DatasetProfile:
    """
    Menghitung profil dataset secara menyeluruh dan deterministik.
    """
    n_rows, n_cols = df.shape
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    total_cells = n_rows * n_cols
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells * 100), 1) if total_cells > 0 else 0.0

    # Top missing columns
    col_missing = df.isna().mean() * 100
    top_missing_items: List[TopMissingItem] = []
    for col, pct in col_missing.sort_values(ascending=False).items():
        if pct > 0:
            top_missing_items.append(TopMissingItem(col=str(col), pct=round(float(pct), 1)))
        if len(top_missing_items) >= 5:
            break

    # Class balance jika target terdefinisi
    class_balance: List[ClassBalanceItem] = []
    if target_col and target_col in df.columns:
        counts = df[target_col].value_counts(normalize=True, dropna=False)
        for label, share in counts.items():
            label_str = "Kosong" if pd.isna(label) else str(label)
            class_balance.append(ClassBalanceItem(label=label_str, share=round(float(share), 3)))

    # Preview data: <= 6 kolom, 3 baris
    preview_cols = list(df.columns[:6])
    preview_df = df[preview_cols].head(3)
    preview_rows: List[List[Any]] = []
    for _, row in preview_df.iterrows():
        row_vals = []
        for val in row:
            if pd.isna(val):
                row_vals.append("-")
            elif isinstance(val, (float, np.floating)):
                row_vals.append(f"{val:.2f}" if abs(val) < 1000 else f"{val:.0f}")
            else:
                row_vals.append(str(val)[:12])
        preview_rows.append(row_vals)

    return DatasetProfile(
        n_numeric=len(num_cols),
        n_categorical=len(cat_cols),
        missing_pct=missing_pct,
        class_balance=class_balance,
        top_missing=top_missing_items,
        preview=PreviewData(cols=preview_cols, rows=preview_rows)
    )
