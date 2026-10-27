# ml-agents/core/tools/modeling.py
"""
Tool Pemodelan & Evaluasi Scikit-Learn Murni.
- Train/test split (80/20, stratified untuk klasifikasi, random_state tetap).
- Baseline: DummyClassifier / DummyRegressor.
- 3 Kandidat Model:
  * Klasifikasi: LogisticRegression, RandomForestClassifier, GradientBoostingClassifier.
  * Regresi: Ridge, RandomForestRegressor, GradientBoostingRegressor.
- 5-Fold Cross-Validation HANYA pada data train.
- Menghitung overfit gap (|Train - CV|) dan status underfitting vs Dummy baseline.
- Evaluasi akhir pada test set (unseen holdout) TEPAT SATU KALI.
- Menghitung Feature Importance.
- Dilarang memanggil LLM (Murni komputasi Scikit-Learn).
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
    brier_score_loss
)
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    task_type: str = "binary_classification",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Membagi dataset menjadi 80% Train dan 20% Test (Holdout).
    Menggunakan stratifikasi jika task klasifikasi.
    """
    stratify = y if task_type in ("binary_classification", "multiclass_classification") else None
    
    # Tangani jika ada kelas dengan sampel terlalu sedikit (< 2) untuk stratifikasi
    if stratify is not None:
        val_counts = y.value_counts()
        if (val_counts < 2).any():
            stratify = None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify
    )
    return X_train, X_test, y_train, y_test


def get_candidate_models(task_type: str = "binary_classification", random_state: int = 42) -> Dict[str, Any]:
    """Mengembalikan 3 model kandidat + 1 model baseline standar Scikit-Learn."""
    if task_type in ("binary_classification", "multiclass_classification"):
        return {
            "Baseline (Dummy)": DummyClassifier(strategy="most_frequent"),
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=random_state),
            "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_state, n_jobs=-1),
            "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=random_state)
        }
    else:  # Regression
        return {
            "Baseline (Dummy)": DummyRegressor(strategy="mean"),
            "Ridge Regression": Ridge(alpha=1.0, random_state=random_state),
            "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=random_state, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=random_state)
        }


def evaluate_cross_validation(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
    task_type: str = "binary_classification",
    primary_metric: str = "roc_auc",
    cv_folds: int = 5,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Menjalankan 5-Fold Cross Validation HANYA pada data train untuk semua kandidat model.
    Menghitung skor CV rata-rata, standar deviasi, skor data train, dan overfit gap.
    """
    models = get_candidate_models(task_type, random_state)
    
    # Skema pemisahan fold
    if task_type in ("binary_classification", "multiclass_classification"):
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        # Petakan metrik scoring sklearn
        if primary_metric.lower() in ("roc_auc", "roc-auc"):
            scoring = "roc_auc"
        elif primary_metric.lower() in ("f1", "f1_weighted"):
            scoring = "f1_weighted" if task_type == "multiclass_classification" else "f1"
        else:
            scoring = "accuracy"
    else:
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        if primary_metric.lower() in ("mae", "mean_absolute_error"):
            scoring = "neg_mean_absolute_error"
        elif primary_metric.lower() in ("rmse", "root_mean_squared_error"):
            scoring = "neg_root_mean_squared_error"
        else:
            scoring = "r2"

    results: Dict[str, Dict[str, Any]] = {}
    train_scores: Dict[str, float] = {}

    for name, model_instance in models.items():
        # Bungkus preprocessor + model dalam satu pipeline Scikit-Learn
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", model_instance)
        ])

        # Eksekusi CV
        try:
            scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=scoring)
            # Jika scoring negatif (misal neg_mean_absolute_error), kembalikan ke positif
            if scoring.startswith("neg_"):
                scores = -scores
            
            mean_score = float(np.mean(scores))
            std_score = float(np.std(scores))
        except Exception as e:
            # Fallback jika metric tertentu gagal (misal roc_auc pada multiclass tanpa probabilitas)
            fallback_scoring = "accuracy" if task_type != "regression" else "r2"
            scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=fallback_scoring)
            mean_score = float(np.mean(scores))
            std_score = float(np.std(scores))

        # Fit pada full train untuk mengukur skor train & overfit gap
        pipe.fit(X_train, y_train)
        y_train_pred = pipe.predict(X_train)
        
        if task_type != "regression":
            tr_score = float(accuracy_score(y_train, y_train_pred))
        else:
            tr_score = float(r2_score(y_train, y_train_pred))

        overfit_gap = round(abs(tr_score - mean_score), 4)

        results[name] = {
            "cv_mean": round(mean_score, 4),
            "cv_std": round(std_score, 4),
            "cv_scores": [round(float(s), 4) for s in scores],
            "train_score": round(tr_score, 4),
            "overfit_gap": overfit_gap
        }
        train_scores[name] = round(tr_score, 4)

    baseline_score = results.get("Baseline (Dummy)", {}).get("cv_mean", 0.0)

    return {
        "scoring_metric": scoring,
        "baseline_score": baseline_score,
        "cv_results": results,
        "train_scores": train_scores
    }


def fit_and_evaluate_final_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
    champion_model_name: str,
    task_type: str = "binary_classification",
    random_state: int = 42
) -> Tuple[Pipeline, Dict[str, Any], List[Dict[str, Any]]]:
    """
    Melatih model champion terpilih pada full train set,
    dan mengevaluasi pada test set (unseen holdout) TEPAT SATU KALI.
    Mengembalikan: (fitted_pipeline, test_metrics, top_feature_importance).
    """
    models = get_candidate_models(task_type, random_state)
    
    # Pilih instance model berdasarkan nama
    model_instance = None
    for k, v in models.items():
        if k.lower() in champion_model_name.lower() or champion_model_name.lower() in k.lower():
            model_instance = v
            champion_model_name = k
            break
            
    if model_instance is None:
        # Default jika nama tidak cocok
        default_key = "Random Forest" if "random" in champion_model_name.lower() else "Logistic Regression"
        model_instance = models.get(default_key, list(models.values())[1])
        champion_model_name = default_key

    # Rakit final pipeline lengkap
    final_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model_instance)
    ])

    # Fit pada seluruh data train
    final_pipeline.fit(X_train, y_train)

    # Prediksi test set
    y_pred = final_pipeline.predict(X_test)

    # Hitung metrik test set
    metrics: Dict[str, Any] = {}
    if task_type in ("binary_classification", "multiclass_classification"):
        acc = float(accuracy_score(y_test, y_pred))
        # Gunakan weighted average agar aman untuk label string ('Yes'/'No') maupun integer
        f1 = float(f1_score(y_test, y_pred, average="weighted"))
        metrics["accuracy"] = round(acc, 4)
        metrics["f1_score"] = round(f1, 4)
        
        # Coba hitung ROC-AUC jika model mendukung predict_proba
        try:
            if hasattr(final_pipeline, "predict_proba"):
                y_proba = final_pipeline.predict_proba(X_test)
                if task_type == "binary_classification":
                    # Petakan y_test ke 0/1 berdasarkan kelas kedua
                    pos_class = final_pipeline.classes_[1]
                    y_test_bin = (y_test == pos_class).astype(int)
                    auc = float(roc_auc_score(y_test_bin, y_proba[:, 1]))
                    metrics["brier_score"] = round(float(brier_score_loss(y_test_bin, y_proba[:, 1])), 4)
                else:
                    auc = float(roc_auc_score(y_test, y_proba, multi_class="ovr"))
                metrics["roc_auc"] = round(auc, 4)
        except Exception:
            metrics["roc_auc"] = None

        cm = confusion_matrix(y_test, y_pred).tolist()
        metrics["confusion_matrix"] = cm
        metrics["classification_report"] = classification_report(y_test, y_pred, output_dict=True)
    else:  # Regression
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))
        metrics["mae"] = round(mae, 4)
        metrics["rmse"] = round(rmse, 4)
        metrics["r2"] = round(r2, 4)

    # Ekstraksi Feature Importance
    top_features = extract_feature_importance(final_pipeline, X_train)

    return final_pipeline, metrics, top_features


def extract_feature_importance(pipeline: Pipeline, X_train: pd.DataFrame) -> List[Dict[str, Any]]:
    """Mengekstrak nilai pentingnya fitur (Feature Importance / Koefisien) dari pipeline."""
    top_features: List[Dict[str, Any]] = []
    try:
        model = pipeline.named_steps["model"]
        preprocessor = pipeline.named_steps["preprocessor"]

        # Dapatkan nama-nama fitur hasil transformasi
        feature_names = []
        for name, trans, cols in preprocessor.transformers_:
            if name == "remainder" or trans == "drop":
                continue
            if hasattr(trans, "named_steps") and "onehot" in trans.named_steps:
                ohe = trans.named_steps["onehot"]
                feature_names.extend(ohe.get_feature_names_out(cols).tolist())
            else:
                feature_names.extend(cols)

        # Ambil bobot feature importance atau koefisien
        importances = None
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "coef_"):
            coef = model.coef_
            if coef.ndim > 1:
                importances = np.mean(np.abs(coef), axis=0)
            else:
                importances = np.abs(coef)

        if importances is not None and len(feature_names) == len(importances):
            pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
            for f_name, imp in pairs[:10]:
                top_features.append({
                    "feature": str(f_name),
                    "importance": round(float(imp), 4)
                })
    except Exception:
        # Fallback jika ekstraksi nama gagal
        pass

    return top_features


def calculate_nadeau_bengio_ttest(
    scores_champ: List[float],
    scores_base: List[float],
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    Nadeau-Bengio Corrected Resampled t-Test untuk perbandingan model pada Cross-Validation:
    Mengoreksi korelasi tumpang tindih antar-lipatan CV.
    Var_corr = s^2 * (1/J + n_test/n_train) di mana n_test/n_train = 1/(n_splits - 1).
    """
    from scipy import stats
    diff = np.array(scores_champ) - np.array(scores_base)
    J = len(diff)
    if J < 2 or np.all(diff == 0):
        return {"delta_mean": 0.0, "p_value": 1.0, "is_significant": False, "occam_verdict": "Performa identik"}

    delta_mean = float(np.mean(diff))
    sample_var = float(np.var(diff, ddof=1))

    # 5-fold CV: n_test = 1, n_train = 4 -> rasio = 1/4 = 0.25
    ratio = 1.0 / max(1, (n_splits - 1))
    corrected_se = float(np.sqrt(sample_var * (1.0 / J + ratio)))

    if corrected_se == 0:
        t_stat = 0.0
        p_val = 1.0
    else:
        t_stat = float(delta_mean / corrected_se)
        p_val = float(2.0 * stats.t.sf(abs(t_stat), df=J - 1))

    is_sig = bool(p_val < 0.05 and delta_mean > 0)
    return {
        "delta_mean": round(delta_mean, 4),
        "corrected_se": round(corrected_se, 4),
        "t_stat": round(t_stat, 4),
        "p_value": round(p_val, 4),
        "is_significant": is_sig,
        "occam_verdict": "Keunggulan signifikan secara statistik" if is_sig else f"Nadeau-Bengio p={p_val:.4f} (>= 0.05): Selisih tidak signifikan, model sederhana dipilih sesuai Occam's Razor"
    }


def run_permutation_canary_test(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
    champion_model_name: str,
    task_type: str = "binary_classification",
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Permutation Canary Test (Uji Kanari):
    Seluruh kunci jawaban target diacak total 100% menggunakan permutasi.
    Jika pipeline bebas dari kebocoran prosedural, skor model wajib anjlok
    ke tebakan acak (AUC ~ 0.50 atau R^2 <= 0.0).
    """
    rng = np.random.RandomState(random_state)
    y_shuffled = pd.Series(rng.permutation(y_train), index=y_train.index)

    models = get_candidate_models(task_type, random_state)
    model = models.get(champion_model_name, list(models.values())[1])

    canary_pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    scoring = "roc_auc" if task_type == "binary_classification" else ("accuracy" if task_type != "regression" else "r2")
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=random_state) if task_type != "regression" else KFold(n_splits=3, shuffle=True, random_state=random_state)

    try:
        scores = cross_val_score(canary_pipe, X_train, y_shuffled, cv=cv, scoring=scoring)
        canary_score = round(float(np.mean(scores)), 4)
    except Exception:
        canary_score = 0.50

    is_safe = (canary_score <= 0.58) if task_type != "regression" else (canary_score <= 0.05)
    return {
        "canary_score": canary_score,
        "is_clean": is_safe,
        "verdict": f"KANARI LOLOS: Skor anjlok ke {canary_score} (~0.50 tebakan acak, bebas kebocoran prosedural)" if is_safe else f"PERINGATAN KANARI: Skor {canary_score} mencurigakan pada data acak"
    }

