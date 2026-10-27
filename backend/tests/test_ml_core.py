import io
import numpy as np
import pandas as pd
import pytest

from backend.app.services.dataset import load_csv_safely, DatasetValidationError
from backend.app.services.profiling import profile_dataset
from backend.app.services.problem import infer_problem
from backend.app.services.leakage import detect_leakage
from backend.app.services.features import engineer_features
from backend.app.services.modeling import create_preprocessor, run_full_modeling_pipeline
from backend.app.schemas import ProblemSpec


def test_dataset_validation_rejects_empty_and_small():
    # Empty CSV
    with pytest.raises(DatasetValidationError, match="kosong"):
        load_csv_safely(b"")

    # Less than 30 rows
    small_csv = "col1,col2\n" + "\n".join([f"{i},{i*2}" for i in range(15)])
    with pytest.raises(DatasetValidationError, match="terlalu kecil"):
        load_csv_safely(small_csv.encode("utf-8"))


def test_leakage_detection_catches_synthetic_leaks():
    # Buat dataset sintetis dengan 3 jenis kebocoran:
    # 1. ID column (kardinalitas 100%)
    # 2. Perfect copy dari label
    # 3. High correlation numeric (> 0.85)
    np.random.seed(42)
    n = 100
    y_train = pd.Series(np.random.choice([0, 1], size=n))
    
    X_train = pd.DataFrame({
        "user_id": [f"ID_{i}" for i in range(n)],
        "target_copy": y_train.copy(),
        "leaky_numeric": y_train + np.random.normal(0, 0.1, size=n),  # r > 0.95
        "clean_feature_1": np.random.normal(0, 1, size=n),
        "clean_feature_2": np.random.choice(["A", "B", "C"], size=n)
    })
    
    X_test = X_train.copy()
    
    X_tr_clean, X_te_clean, report = detect_leakage(X_train, y_train, X_test, threshold=0.85)
    
    assert "user_id" in report["leaky_columns"]
    assert "target_copy" in report["leaky_columns"]
    assert "leaky_numeric" in report["leaky_columns"]
    assert "clean_feature_1" not in report["leaky_columns"]
    assert "clean_feature_2" not in report["leaky_columns"]
    assert report["passed"] is False
    assert "user_id" not in X_tr_clean.columns
    assert "user_id" not in X_te_clean.columns


def test_pipeline_anti_contamination():
    # Tes bahwa preprocessor hanya fit di train set dan tidak terpengaruh data test
    X_train = pd.DataFrame({
        "num": [10.0, 20.0, 30.0, 40.0],
        "cat": ["a", "b", "a", "b"]
    })
    prep = create_preprocessor(X_train)
    prep.fit(X_train)
    
    num_imputer = prep.named_transformers_["num"].named_steps["imputer"]
    num_scaler = prep.named_transformers_["num"].named_steps["scaler"]
    
    initial_mean = float(num_scaler.mean_[0])
    assert initial_mean == 25.0
    
    # Mengubah data test tidak boleh mengubah statistik train yang sudah di-fit
    X_test_wild = pd.DataFrame({
        "num": [9999.0, 8888.0],
        "cat": ["c", "d"]
    })
    transformed_test = prep.transform(X_test_wild)
    assert float(num_scaler.mean_[0]) == 25.0


def test_profiling_and_problem_inference():
    df = pd.DataFrame({
        "age": [22, 38, 26, np.nan, 35] * 10,
        "sex": ["male", "female", "female", "male", "female"] * 10,
        "survived": [0, 1, 1, 0, 0] * 10
    })
    
    prob = infer_problem(df)
    assert prob.target == "survived"
    assert prob.task == "binary"
    assert prob.metric == "ROC-AUC"
    
    profile = profile_dataset(df, target_col="survived")
    assert profile.n_numeric >= 1
    assert profile.n_categorical >= 1
    assert len(profile.class_balance) == 2


def test_full_modeling_pipeline_on_titanic():
    # Muat data titanic nyata
    df, _ = load_csv_safely("data/titanic.csv")
    prob = infer_problem(df, requested_target="survived")
    
    results = run_full_modeling_pipeline(df, prob)
    
    # Validasi output ML nyata
    assert "champion_name" in results
    assert "leaderboard" in results
    assert len(results["leaderboard"]) >= 4
    assert results["learning_curve"]["gap"] is not None
    assert results["canary_auc"] <= 0.65  # label shuffled should be near ~0.50
    assert "p_value" in results["nadeau_bengio"]
    assert results["final_eval"]["test_auc"] > 0.65
    assert len(results["final_eval"]["permutation_importance"]) > 0
