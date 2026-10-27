# ml-agents/tests/test_m1_pipeline.py
"""
Unit & Integration Test untuk Tahap M1 (Pipeline ML Python Murni Tanpa LLM).
- Menguji profiling data & deteksi korelasi leakage.
- Menguji ColumnTransformer (fit-in-fold).
- Menguji Baseline Dummy vs 3 kandidat model pada 5-Fold CV.
- Menguji evaluasi test set dan feature importance.
- Menguji penyimpanan model.joblib + schema.json dan prediksi data baru.
- Menguji perakitan & re-eksekusi notebook dengan nbclient.
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from core.tools.profiling import profile_dataset, calculate_target_correlations
from core.tools.cleaning import prepare_features_and_target, build_preprocessor_pipeline
from core.tools.modeling import split_train_test, evaluate_cross_validation, fit_and_evaluate_final_model
from core.tools.plotting import generate_all_figures
from core.tools.predict import save_artifacts_for_prediction, predict_single_or_batch
from core.tools.notebook import build_reproducible_notebook, verify_and_replay_notebook


@pytest.fixture
def sample_classification_data(tmp_path: Path) -> Path:
    """Fixture dataset klasifikasi biner."""
    csv_file = tmp_path / "telco_sample.csv"
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "customerID": [f"ID_{i}" for i in range(n)],
        "tenure": np.random.randint(1, 72, n),
        "MonthlyCharges": np.round(np.random.uniform(20, 110, n), 2),
        "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n),
        "churn": np.random.choice(["No", "Yes"], n, p=[0.7, 0.3])
    })
    df.to_csv(csv_file, index=False)
    return csv_file


@pytest.fixture
def sample_regression_data(tmp_path: Path) -> Path:
    """Fixture dataset regresi."""
    csv_file = tmp_path / "insurance_sample.csv"
    np.random.seed(42)
    n = 200
    age = np.random.randint(18, 65, n)
    bmi = np.round(np.random.normal(30, 5, n), 2)
    smoker = np.random.choice(["yes", "no"], n, p=[0.2, 0.8])
    charges = 250 * age + 300 * bmi + (smoker == "yes") * 15000 + np.random.normal(0, 500, n)
    df = pd.DataFrame({
        "age": age,
        "bmi": bmi,
        "smoker": smoker,
        "charges": np.round(charges, 2)
    })
    df.to_csv(csv_file, index=False)
    return csv_file


def test_profiling_and_leakage_detection(sample_classification_data: Path):
    """Menguji fungsi profiling dan deteksi korelasi kebocoran data."""
    df = pd.read_csv(sample_classification_data)
    profile = profile_dataset(df)
    
    assert profile["n_rows"] == 200
    assert profile["n_cols"] == 5
    assert "churn" in profile["candidate_targets"]
    assert any("customerID" in item for item in profile["id_or_constant_candidates"])
    
    correlations = calculate_target_correlations(df, target_col="churn", task_type="binary_classification")
    assert isinstance(correlations, dict)


def test_planted_leakage_is_detected(tmp_path: Path):
    """Menguji bahwa fitur bocor yang sengaja ditanam (korelasi > 0.95) berhasil terdeteksi."""
    leak_file = tmp_path / "leak_data.csv"
    np.random.seed(42)
    n = 100
    y = np.random.choice([0, 1], n)
    # Fitur bocor identik dengan target + sedikit noise
    leaky_feature = y * 100 + np.random.normal(0, 0.01, n)
    normal_feature = np.random.normal(0, 1, n)
    df = pd.DataFrame({
        "normal_feat": normal_feature,
        "leaky_feat": leaky_feature,
        "target": y
    })
    df.to_csv(leak_file, index=False)
    
    corrs = calculate_target_correlations(df, target_col="target", task_type="binary_classification")
    assert "leaky_feat" in corrs
    assert corrs["leaky_feat"] > 0.95, f"Korelasi leaky_feat harus > 0.95, didapat: {corrs['leaky_feat']}"


def test_full_pipeline_classification(sample_classification_data: Path, tmp_path: Path):
    """Menguji alur penuh klasifikasi: cleaning -> CV -> test evaluation -> plot -> predict -> notebook."""
    df = pd.read_csv(sample_classification_data)
    run_dir = tmp_path / "run_clf"
    
    # 1. Cleaning & ColumnTransformer
    X, y, num_cols, cat_cols, drops = prepare_features_and_target(
        df, target_col="churn", drop_columns=["customerID"]
    )
    assert "customerID" not in X.columns
    assert "churn" not in X.columns
    preprocessor = build_preprocessor_pipeline(num_cols, cat_cols)
    
    # 2. Split & Cross Validation
    X_train, X_test, y_train, y_test = split_train_test(X, y, task_type="binary_classification")
    cv_res = evaluate_cross_validation(X_train, y_train, preprocessor, task_type="binary_classification")
    
    assert "Baseline (Dummy)" in cv_res["cv_results"]
    assert "Random Forest" in cv_res["cv_results"]
    assert cv_res["cv_results"]["Random Forest"]["cv_mean"] > 0.0
    
    # 3. Fit Model Final & Evaluasi Test Set
    pipe, test_metrics, top_feats = fit_and_evaluate_final_model(
        X_train, y_train, X_test, y_test, preprocessor,
        champion_model_name="Random Forest",
        task_type="binary_classification"
    )
    assert "accuracy" in test_metrics
    assert "f1_score" in test_metrics
    assert len(top_feats) > 0
    
    # 4. Plotting
    figs = generate_all_figures(df, "churn", "binary_classification", cv_res["cv_results"], test_metrics, top_feats, run_dir)
    assert len(figs) >= 4
    for fig_path in figs:
        assert (run_dir / fig_path).exists()
        
    # 5. Serialisasi & Mode Prediksi
    m_path, s_path = save_artifacts_for_prediction(
        pipe, df, "churn", "binary_classification", "Random Forest", test_metrics, top_feats, run_dir
    )
    assert m_path.exists()
    assert s_path.exists()
    
    # Uji prediksi data baru
    new_data = {"tenure": 12, "MonthlyCharges": 65.0, "Contract": "Month-to-month"}
    pred_res = predict_single_or_batch(run_dir, new_data)
    assert len(pred_res["predictions"]) == 1
    assert "churn" in pred_res["predictions"][0]["formatted_output"]
    assert "probabilities" in pred_res["predictions"][0]
    
    # 6. Perakitan & Re-eksekusi Notebook
    nb_path = build_reproducible_notebook(
        str(sample_classification_data), "churn", "binary_classification", ["customerID"],
        "Random Forest", {"problem_statement": "Uji klasifikasi"}, test_metrics,
        run_dir / "notebook.ipynb"
    )
    assert nb_path.exists()
    
    ok, msg = verify_and_replay_notebook(nb_path)
    assert ok is True, f"Re-eksekusi notebook gagal: {msg}"


def test_full_pipeline_regression(sample_regression_data: Path, tmp_path: Path):
    """Menguji alur penuh regresi: cleaning -> CV -> test evaluation -> predict."""
    df = pd.read_csv(sample_regression_data)
    run_dir = tmp_path / "run_reg"
    
    X, y, num_cols, cat_cols, drops = prepare_features_and_target(df, target_col="charges")
    preprocessor = build_preprocessor_pipeline(num_cols, cat_cols)
    
    X_train, X_test, y_train, y_test = split_train_test(X, y, task_type="regression")
    cv_res = evaluate_cross_validation(X_train, y_train, preprocessor, task_type="regression", primary_metric="r2")
    
    assert "Ridge Regression" in cv_res["cv_results"]
    assert "Random Forest" in cv_res["cv_results"]
    
    pipe, test_metrics, top_feats = fit_and_evaluate_final_model(
        X_train, y_train, X_test, y_test, preprocessor,
        champion_model_name="Random Forest",
        task_type="regression"
    )
    assert "mae" in test_metrics
    assert "rmse" in test_metrics
    assert "r2" in test_metrics
    
    save_artifacts_for_prediction(pipe, df, "charges", "regression", "Random Forest", test_metrics, top_feats, run_dir)
    
    # Uji prediksi regresi
    new_patient = {"age": 45, "bmi": 28.5, "smoker": "no"}
    pred_res = predict_single_or_batch(run_dir, new_patient)
    assert "charges" in pred_res["predictions"][0]["formatted_output"]
    assert "error_margin" in pred_res["predictions"][0]


def test_missing_column_is_rejected(sample_regression_data: Path, tmp_path: Path):
    """DoD Poin 8: Input data baru dengan kolom hilang wajib ditolak secara transparan."""
    df = pd.read_csv(sample_regression_data)
    run_dir = tmp_path / "run_reject"
    X, y, num_cols, cat_cols, drops = prepare_features_and_target(df, target_col="charges")
    preprocessor = build_preprocessor_pipeline(num_cols, cat_cols)
    X_train, X_test, y_train, y_test = split_train_test(X, y, task_type="regression")
    pipe, test_metrics, top_feats = fit_and_evaluate_final_model(
        X_train, y_train, X_test, y_test, preprocessor,
        champion_model_name="Random Forest", task_type="regression"
    )
    save_artifacts_for_prediction(pipe, df, "charges", "regression", "Random Forest", test_metrics, top_feats, run_dir)
    
    # Input yang kehilangan kolom wajib 'age'
    invalid_input = {"bmi": 28.5, "smoker": "no"}
    with pytest.raises(ValueError, match="Input ditolak: Kolom wajib 'age' tidak ditemukan"):
        predict_single_or_batch(run_dir, invalid_input)
