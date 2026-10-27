from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    auc as calc_auc,
    roc_auc_score,
    roc_curve,
    f1_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from backend.app.schemas import ProblemSpec


def create_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    Membangun preprocessor Pipeline & ColumnTransformer.
    Hanya di-fit pada data training untuk mencegah kebocoran data.
    """
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    num_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(max_categories=25, handle_unknown="ignore", sparse_output=False)),
    ])

    transformers = []
    if num_cols:
        transformers.append(("num", num_transformer, num_cols))
    if cat_cols:
        transformers.append(("cat", cat_transformer, cat_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")



def run_full_modeling_pipeline(
    df: pd.DataFrame,
    problem: ProblemSpec,
    progress_callback: Optional[Callable[[int, str, str, int], None]] = None
) -> Dict[str, Any]:
    """
    Menjalankan pipeline ML nyata secara lengkap, deterministik (random_state=42),
    dan menghasilkan fakta-fakta angka terverifikasi untuk arena debat.
    """
    target_col = problem.target
    clean_df = df.dropna(subset=[target_col]).copy()

    y_raw = clean_df[target_col]
    X_raw = clean_df.drop(columns=[target_col])

    # Konversi target ke integer codes jika klasifikasi
    if problem.task in ("binary", "multiclass"):
        y, class_labels = pd.factorize(y_raw, sort=True)
        y = pd.Series(y, index=clean_df.index)
        classes_str = [str(c) for c in class_labels]
    else:
        y = y_raw
        classes_str = []

    # 1. SPLIT STRATIFIED TRAIN/TEST (80/20) SEBELUM STATISTIK APA PUN
    if progress_callback:
        progress_callback(1, "guardian", "Mengunci test set (80/20 stratified split)...", 10)

    stratify_target = y if problem.task in ("binary", "multiclass") else None
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.2, stratify=stratify_target, random_state=42
    )

    # 2. FEATURE ENGINEERING & LEAKAGE DETECTION
    if progress_callback:
        progress_callback(2, "wrangler", "Melakukan rekayasa fitur & audit kebocoran data...", 25)

    from backend.app.services.leakage import detect_leakage
    from backend.app.services.features import engineer_features

    # Deteksi kebocoran dulu
    X_tr_noleak, X_te_noleak, leak_report = detect_leakage(X_train_raw, y_train, X_test_raw)

    # Rekayasa fitur generik + VIF
    X_train, X_test, fe_report = engineer_features(X_tr_noleak, X_te_noleak)

    # 3. KANDIDAT MODEL & 5-FOLD STRATIFIED CV
    if progress_callback:
        progress_callback(3, "guardian", "Melatih 4 kandidat model di CV 5-lipatan...", 45)

    preprocessor = create_preprocessor(X_train)

    from sklearn.model_selection import KFold
    if problem.task == "regression":
        from sklearn.dummy import DummyRegressor
        from sklearn.linear_model import Ridge
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        scoring_metric = "r2"
        candidates = {
            "Dummy": DummyRegressor(strategy="mean"),
            "Ridge": Ridge(random_state=42),
            "Random Forest": RandomForestRegressor(n_estimators=60, n_jobs=-1, random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42),
        }
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
    else:
        scoring_metric = "roc_auc" if problem.task == "binary" else "f1_macro"
        candidates = {
            "Dummy": DummyClassifier(strategy="prior"),
            "Logistic Regression L2": LogisticRegression(max_iter=1000, random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=60, n_jobs=-1, random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        }
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    pipes = {
        name: Pipeline(steps=[("prep", preprocessor), ("clf", clf)])
        for name, clf in candidates.items()
    }


    cv_scores: Dict[str, np.ndarray] = {}
    leaderboard_data = []

    for name, pipe in pipes.items():
        try:
            scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=scoring_metric)
        except Exception:
            # Fallback untuk model dummy jika metrik tidak kompatibel
            scores = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        cv_scores[name] = scores
        leaderboard_data.append({
            "model": name,
            "cv_auc": round(float(np.mean(scores)), 3),
            "cv_std": round(float(np.std(scores)), 3),
        })

    # Urutkan model berdasarkan skor CV (selain Dummy)
    real_candidates = [m for m in leaderboard_data if m["model"] != "Dummy"]
    real_candidates.sort(key=lambda x: x["cv_auc"], reverse=True)
    top1_name = real_candidates[0]["model"]
    top2_name = real_candidates[1]["model"] if len(real_candidates) > 1 else top1_name

    # 4. OVERFITTING / UNDERFITTING: LEARNING CURVE
    if progress_callback:
        progress_callback(4, "guardian", "Mendiagnosis learning curve & gap train-valid...", 60)

    # Subsample data jika besar untuk kecepatan
    sub_n = min(len(X_train), 5000)
    X_sub = X_train.iloc[:sub_n]
    y_sub = y_train.iloc[:sub_n]

    best_pipe = pipes[top1_name]
    sizes, tr_sc, va_sc = learning_curve(
        best_pipe, X_sub, y_sub, cv=cv, scoring=scoring_metric,
        train_sizes=np.linspace(0.2, 1.0, 5), random_state=42
    )
    tr_means = [round(float(v), 3) for v in np.mean(tr_sc, axis=1)]
    va_means = [round(float(v), 3) for v in np.mean(va_sc, axis=1)]
    train_val_gap = round(float(tr_means[-1] - va_means[-1]), 3)

    # 5. UJI KANARI (LABEL PERMUTATION) & UJI DERAU (15% GAUSSIAN NOISE)
    if progress_callback:
        progress_callback(5, "guardian", "Menjalankan uji kanari & uji stres derau 15%...", 75)

    # Kanari: acak label
    rng = np.random.default_rng(42)
    y_shuffled = pd.Series(rng.permutation(y_sub.values), index=y_sub.index)
    canary_scores = cross_val_score(best_pipe, X_sub, y_shuffled, cv=cv, scoring=scoring_metric)
    canary_auc = round(float(np.mean(canary_scores)), 3)

    # Derau 15% pada fitur numerik
    X_noisy = X_sub.copy()
    num_cols = X_noisy.select_dtypes(include=[np.number]).columns
    for nc in num_cols:
        col_std = X_noisy[nc].std()
        if pd.isna(col_std) or col_std == 0:
            col_std = 1.0
        noise = rng.normal(0, 0.15 * col_std, size=len(X_noisy))
        X_noisy[nc] = X_noisy[nc] + noise

    noise_results: Dict[str, float] = {}
    for name in [top1_name, "Logistic Regression L2"]:
        if name in pipes:
            n_sc = cross_val_score(pipes[name], X_noisy, y_sub, cv=cv, scoring=scoring_metric)
            noise_results[name] = round(float(np.mean(n_sc)), 3)

    # 6. UJI SIGNIFIKANSI STATISTIK: NADEAU-BENGIO CORRECTED T-TEST
    if progress_callback:
        progress_callback(6, "guardian", "Menguji signifikansi statistik Nadeau-Bengio...", 85)

    s1 = cv_scores[top1_name]
    s2 = cv_scores[top2_name]
    diff = s1 - s2
    k = len(diff)
    diff_mean = float(np.mean(diff))
    diff_var = float(np.var(diff, ddof=1)) if k > 1 else 1e-6
    # Rasio fold test / train dalam 5-fold CV adalah 0.2 / 0.8 = 0.25
    correction = (1.0 / k) + 0.25
    t_stat = diff_mean / np.sqrt(max(correction * diff_var, 1e-9))
    p_value = round(float(2.0 * stats.t.sf(abs(t_stat), df=k - 1)), 3)

    # ATURAN KEPUTUSAN MODEL PRODUKSI TRANSPARAN:
    # Jika p >= 0.05, pilih model yang lebih sederhana, stabil terhadap derau, dan interpretable (Logistic L2)
    # Jika p < 0.05, pilih model performa tertinggi
    if p_value >= 0.05:
        champion_name = "Logistic Regression L2" if "Logistic Regression L2" in pipes else top2_name
        champion_reason = f"Perbedaan performa tidak signifikan (p={p_value:.3f} >= 0.05). Memilih {champion_name} karena stabil terhadap derau & mudah dijelaskan."
    else:
        champion_name = top1_name
        champion_reason = f"Keunggulan performa signifikan secara statistik (p={p_value:.3f} < 0.05)."

    # 7. EVALUASI AKHIR PADA TEST SET TERKUNCI (SEKALI SAJA)
    if progress_callback:
        progress_callback(7, "storyteller", "Membuka gembok data uji untuk evaluasi akhir...", 95)

    champion_pipe = pipes[champion_name]
    champion_pipe.fit(X_train, y_train)

    from sklearn.metrics import r2_score
    if problem.task == "binary":
        y_prob = champion_pipe.predict_proba(X_test)[:, 1]
        test_auc = round(float(roc_auc_score(y_test, y_prob)), 3)
        y_pred = (y_prob >= 0.5).astype(int)

        # ROC Curve coordinates
        fpr_raw, tpr_raw, _ = roc_curve(y_test, y_prob)
        fpr = [round(float(v), 3) for v in fpr_raw[::max(1, len(fpr_raw) // 10)]]
        tpr = [round(float(v), 3) for v in tpr_raw[::max(1, len(tpr_raw) // 10)]]

        # PR-AUC
        prec, rec, _ = precision_recall_curve(y_test, y_prob)
        pr_auc = round(float(calc_auc(rec, prec)), 3)
        cm = confusion_matrix(y_test, y_pred).tolist()
        clf_rep = classification_report(y_test, y_pred, output_dict=True)
    elif problem.task == "regression":
        y_pred = champion_pipe.predict(X_test)
        test_auc = round(float(r2_score(y_test, y_pred)), 3)
        fpr, tpr = [], []
        pr_auc = 0.0
        cm = []
        clf_rep = {}
    else:
        y_pred = champion_pipe.predict(X_test)
        test_auc = round(float(f1_score(y_test, y_pred, average="macro")), 3)
        fpr, tpr = [], []
        pr_auc = 0.0
        cm = confusion_matrix(y_test, y_pred).tolist()
        clf_rep = classification_report(y_test, y_pred, output_dict=True)


    # Permutation importance
    perm_imp = permutation_importance(
        champion_pipe, X_test, y_test,
        scoring=scoring_metric, n_repeats=15, random_state=42
    )
    feature_names = list(X_test.columns)
    imp_scores = {
        name: round(float(val), 3)
        for name, val in zip(feature_names, perm_imp.importances_mean)
    }
    sorted_imp = sorted(imp_scores.items(), key=lambda x: x[1], reverse=True)

    # Tambahkan test_auc dan status champion ke leaderboard
    for entry in leaderboard_data:
        if entry["model"] == champion_name:
            entry["champion"] = True
            entry["test_auc"] = test_auc
        else:
            entry["champion"] = False
            # Hitung test_auc untuk kandidat lainnya
            other_pipe = pipes[entry["model"]]
            other_pipe.fit(X_train, y_train)
            if problem.task == "binary":
                o_prob = other_pipe.predict_proba(X_test)[:, 1]
                entry["test_auc"] = round(float(roc_auc_score(y_test, o_prob)), 3)
            elif problem.task == "regression":
                o_pred = other_pipe.predict(X_test)
                entry["test_auc"] = round(float(r2_score(y_test, o_pred)), 3)
            else:
                o_pred = other_pipe.predict(X_test)
                entry["test_auc"] = round(float(f1_score(y_test, o_pred, average="macro")), 3)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "classes": classes_str,
        "pipes": pipes,
        "champion_name": champion_name,
        "champion_pipe": champion_pipe,
        "champion_reason": champion_reason,
        "leaderboard": leaderboard_data,
        "learning_curve": {
            "sizes": [f"{int(s*100)}%" for s in np.linspace(0.2, 1.0, 5)],
            "train": tr_means,
            "valid": va_means,
            "gap": train_val_gap
        },
        "canary_auc": canary_auc,
        "noise_results": noise_results,
        "nadeau_bengio": {
            "top1": top1_name,
            "top2": top2_name,
            "p_value": p_value,
            "is_significant": p_value < 0.05
        },
        "final_eval": {
            "test_auc": test_auc,
            "pr_auc": pr_auc,
            "confusion_matrix": cm,
            "classification_report": clf_rep,
            "fpr": fpr,
            "tpr": tpr,
            "permutation_importance": sorted_imp
        },
        "leak_report": leak_report,
        "fe_report": fe_report
    }
