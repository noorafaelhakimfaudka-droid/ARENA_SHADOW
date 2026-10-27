from typing import Optional, List
import numpy as np
import pandas as pd
from backend.app.schemas import ProblemSpec
from backend.app.services.dataset import DatasetValidationError


CANDIDATE_TARGET_NAMES = [
    "survived", "churn", "target", "label", "default", "y", "class", "outcome", "status"
]


def infer_problem(df: pd.DataFrame, requested_target: Optional[str] = None) -> ProblemSpec:
    """
    Menentukan kolom target dan jenis masalah machine learning secara cerdas dan deterministik.
    """
    target_col: Optional[str] = None

    if requested_target:
        clean_target = requested_target.strip()
        matched = [c for c in df.columns if c.lower() == clean_target.lower()]
        if not matched:
            raise DatasetValidationError(
                f"Kolom target '{requested_target}' tidak ditemukan di dalam dataset. "
                f"Kolom yang tersedia: {', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''}"
            )
        target_col = matched[0]
    else:
        # Coba cocokkan dari nama-nama umum
        col_lower_map = {c.lower(): c for c in df.columns}
        for cand in CANDIDATE_TARGET_NAMES:
            if cand in col_lower_map:
                target_col = col_lower_map[cand]
                break

        # Jika belum ada, gunakan kolom terakhir
        if target_col is None:
            target_col = df.columns[-1]

    # Cek nilai unik target
    target_series = df[target_col].dropna()
    if target_series.empty:
        raise DatasetValidationError(f"Kolom target '{target_col}' tidak memiliki nilai valid (semua bernilai kosong/NaN).")

    unique_vals = target_series.unique()
    n_unique = len(unique_vals)

    if n_unique < 2:
        raise DatasetValidationError(
            f"Kolom target '{target_col}' hanya memiliki 1 nilai unik ({unique_vals[0]}). "
            "Model ML membutuhkan minimal 2 kelas/nilai untuk dipelajari."
        )

    classes: List[str] = []
    task = "binary"
    metric = "ROC-AUC"
    metric_label = "Area under ROC Curve"

    if n_unique == 2:
        task = "binary"
        classes = [str(x) for x in sorted(unique_vals, key=lambda v: str(v))]
        metric = "ROC-AUC"
        metric_label = "Area under ROC Curve"
    elif n_unique <= 20 or not pd.api.types.is_numeric_dtype(target_series):
        task = "multiclass"
        classes = [str(x) for x in sorted(unique_vals, key=lambda v: str(v))]
        metric = "Macro-F1"
        metric_label = "Macro Averaged F1-Score"
    else:
        task = "regression"
        classes = []
        metric = "R2"
        metric_label = "R-squared"

    return ProblemSpec(
        task=task,
        target=target_col,
        classes=classes,
        metric=metric,
        metric_label=metric_label
    )
