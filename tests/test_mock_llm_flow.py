# ml-agents/tests/test_mock_llm_flow.py
"""
Test Alur Penuh Multi-Agent dengan Mock LLM (Sesuai Kriteria Penilaian Bagian 9 Poin 7).
Memastikan seluruh rangkaian ronde debat 1 s/d 5 berjalan lancar dan terintegrasi
tanpa bergantung pada kuota internet atau jaringan cloud.
"""

from pathlib import Path
from typing import Any, Dict
import pandas as pd
import pytest

from core.llm import GeminiClient
from core.state import SharedState
from agents.framing_agent import run_framing_debate
from agents.data_agent import run_data_cleaning_debate
from agents.modeling_agent import run_modeling_debate
from agents.insight_agent import run_insight_and_storytelling
from agents.notebook_agent import run_notebook_and_export_artifacts
from core.tools.predict import predict_single_or_batch


class MockGeminiClient(GeminiClient):
    """Klien LLM Tiruan (Mock) untuk pengujian deterministik CI/CD."""

    def __init__(self, log_file: Path | str):
        super().__init__(api_key="mock_key", log_file=log_file)

    def generate_json(
        self,
        agent_name: str,
        prompt: str,
        system_prompt: str = "",
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """Mengembalikan respons JSON sintetis yang realistis berdasarkan peran agen."""
        if agent_name == "MODEL ARCHITECT":
            return {
                "problem_statement": "Memprediksi target berbasis data demografis untuk optimasi keputusan.",
                "target_column": "charges",
                "task_type": "regression",
                "primary_metric": "r2",
                "reasoning": "Target bertipe numerik kontinu, maka task adalah regresi dengan metrik R2."
            }
        elif agent_name == "DATA AUDITOR":
            return {
                "drop_columns": [],
                "audit_verdict": "Data bersih tanpa indikasi target leakage ekstrem.",
                "is_target_valid": True
            }
        elif agent_name == "FEATURE STRATEGIST":
            return {
                "num_impute": "median",
                "cat_impute": "most_frequent",
                "scaler": "standard",
                "feature_engineering": [],
                "feature_notes": "Imputasi standar fit-in-fold diterapkan."
            }
        elif agent_name == "STATISTICIAN":
            if "storytelling" in prompt.lower() or "narasi" in prompt.lower():
                return {
                    "executive_summary": "Model berhasil dilatih dengan generalisasi yang stabil.",
                    "key_findings": ["Fitur age dan bmi memiliki korelasi positif terhadap charges."],
                    "business_recommendation": ["Gunakan model untuk estimasi biaya awal."],
                    "skeptic_caveat": "Periksa deviasi residual secara berkala."
                }
            return {
                "champion_model": "Ridge Regression",
                "champion_cv_score": 0.75,
                "statistician_rationale": "Sesuai Occam's Razor, model linier dipilih karena stabil dan terhindar dari overfitting.",
                "overfit_gap": 0.02,
                "robustness_status": "HEALTHY",
                "rejection_notes": []
            }
        elif agent_name == "ROBUSTNESS INVESTIGATOR":
            return {
                "robustness_verdict": "HEALTHY",
                "overfit_gap_analysis": "Gap 0.02 berada jauh di bawah ambang batas bahaya 0.10.",
                "underfit_check": "Model mengungguli baseline dummy secara signifikan."
            }
        elif agent_name == "SKEPTIC":
            return {
                "decision": "APPROVE",
                "final_metric": "r2",
                "skeptic_note": "Asumsi validasi silang terpenuhi.",
                "skeptic_audit": "Pembersihan disetujui.",
                "skeptic_final_remarks": "Model disetujui untuk dievaluasi pada test set."
            }
        return {"status": "ok"}


def test_full_pipeline_with_mock_llm(tmp_path: Path):
    """Pengujian alur penuh 5 ronde multi-agent menggunakan Mock LLM."""
    csv_file = tmp_path / "mock_test.csv"
    df = pd.DataFrame({
        "age": [20, 30, 40, 50, 60, 25, 35, 45, 55, 65],
        "bmi": [22.0, 25.5, 30.1, 28.4, 32.0, 21.0, 26.0, 29.0, 31.0, 33.0],
        "sex": ["male", "female", "male", "female", "male", "female", "male", "female", "male", "female"],
        "charges": [1500.0, 2800.0, 4500.0, 6200.0, 8900.0, 1900.0, 3400.0, 5100.0, 7500.0, 9900.0]
    })
    df.to_csv(csv_file, index=False)

    run_dir = tmp_path / "run_mock"
    run_dir.mkdir(parents=True, exist_ok=True)
    mock_client = MockGeminiClient(log_file=run_dir / "llm_log.jsonl")
    state = SharedState(run_id="mock_run", csv_path=str(csv_file))

    # Ronde 1: Framing
    framing = run_framing_debate(df, state, mock_client)
    assert framing["task_type"] == "regression"
    assert framing["target_column"] == "charges"

    # Ronde 2: Data Cleaning
    X, y, prep, num_cols, cat_cols = run_data_cleaning_debate(df, framing["target_column"], framing["task_type"], state, mock_client)
    assert len(num_cols) == 2
    assert len(cat_cols) == 1

    # Ronde 3: Modeling
    pipe, test_metrics, top_feats, X_tr, y_tr = run_modeling_debate(
        X, y, prep, framing["task_type"], framing["primary_metric"], state, mock_client
    )
    assert "mae" in test_metrics

    # Ronde 4: Insight
    story = run_insight_and_storytelling(df, framing["target_column"], framing["task_type"], run_dir, state, mock_client)
    assert (run_dir / "report.md").exists()
    assert len(state.figures) >= 4

    # Ronde 5: Notebook & Export
    nb_p, m_p, s_p, is_repro = run_notebook_and_export_artifacts(str(csv_file), df, pipe, run_dir, state)
    assert nb_p.exists()
    assert m_p.exists()
    assert s_p.exists()
    assert is_repro is True

    # Verifikasi Prediksi
    pred_res = predict_single_or_batch(run_dir, {"age": 28, "bmi": 24.5, "sex": "female"})
    assert len(pred_res["predictions"]) == 1
    assert "charges" in pred_res["predictions"][0]["formatted_output"]


def test_cmd_train_progress_callback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Memastikan cmd_train dengan progress_cb berjalan mulus tanpa NameError time."""
    import argparse
    import main

    csv_file = tmp_path / "mock_cb.csv"
    df = pd.DataFrame({
        "age": [20, 30, 40, 50, 60, 25, 35, 45, 55, 65],
        "bmi": [22.0, 25.5, 30.1, 28.4, 32.0, 21.0, 26.0, 29.0, 31.0, 33.0],
        "sex": ["male", "female", "male", "female", "male", "female", "male", "female", "male", "female"],
        "charges": [1500.0, 2800.0, 4500.0, 6200.0, 8900.0, 1900.0, 3400.0, 5100.0, 7500.0, 9900.0]
    })
    df.to_csv(csv_file, index=False)

    out_dir = tmp_path / "out_cb"
    args = argparse.Namespace(
        csv_file=str(csv_file),
        target="charges",
        out=str(out_dir)
    )

    # Percepat sleep
    monkeypatch.setattr(main.time, "sleep", lambda x: None)

    callbacks_received = []
    def dummy_cb(agent_key: str, msg: str, extra: Any = None):
        callbacks_received.append((agent_key, msg))

    state = main.cmd_train(args, progress_cb=dummy_cb)
    assert state is not None
    assert len(callbacks_received) >= 5
    assert any("PROBLEM FRAMER" in msg for _, msg in callbacks_received)

