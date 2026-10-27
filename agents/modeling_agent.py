# ml-agents/agents/modeling_agent.py
"""
Agen 3 — Modeling, Evaluasi & Occam's Razor (Ronde 3 Debat).
Kolaborasi & Debat:
- MODEL ARCHITECT: Mengusulkan model kandidat dan strategi evaluasi.
- STATISTICIAN: Menilai signifikansi skor 5-Fold CV dan menegakkan prinsip Occam's Razor.
- ROBUSTNESS INVESTIGATOR: Mendiagnosis Generalization Gap (|Train - CV| > 0.10) dan memverifikasi ketahanan model.
- SKEPTIC: Memvalidasi kemenangan model dan memberikan izin final training.
Eksekusi Python: 5-Fold CV pada train, fit champion pada train, evaluasi holdout test set TEPAT SATU KALI.
"""

from __future__ import annotations
from typing import Any, Dict, List, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from agents.base_agent import BaseAgent
from agents.personas import MODEL_ARCHITECT, ROBUSTNESS_INVESTIGATOR, SKEPTIC, STATISTICIAN, build_modeling_prompt
from core.llm import GeminiClient
from core.state import SharedState
from core.tools.modeling import (
    evaluate_cross_validation,
    fit_and_evaluate_final_model,
    split_train_test,
    calculate_nadeau_bengio_ttest,
    run_permutation_canary_test
)
from core.tools.profiling import calculate_adversarial_validation


def run_modeling_debate(
    X: pd.DataFrame,
    y: pd.Series,
    preprocessor: ColumnTransformer,
    task_type: str,
    primary_metric: str,
    state: SharedState,
    client: GeminiClient
) -> Tuple[Pipeline, Dict[str, Any], List[Dict[str, Any]], pd.DataFrame, pd.Series]:
    """
    Menjalankan debat Ronde 3 (Modeling & Occam's Razor) secara dinamis menggunakan Gemini.
    Menghasilkan model champion terlatih, metrik test set, dan feature importances.
    """
    # 1. Split Train/Test 80/20 & Eksekusi 5-Fold CV oleh Python murni
    X_train, X_test, y_train, y_test = split_train_test(X, y, task_type=task_type)
    cv_data = evaluate_cross_validation(
        X_train=X_train,
        y_train=y_train,
        preprocessor=preprocessor,
        task_type=task_type,
        primary_metric=primary_metric
    )

    agent_arch = BaseAgent(MODEL_ARCHITECT, client=client)
    agent_stat = BaseAgent(STATISTICIAN, client=client)
    agent_rob = BaseAgent(ROBUSTNESS_INVESTIGATOR, client=client)
    agent_skep = BaseAgent(SKEPTIC, client=client)

    # Langkah 1: Statistician mengevaluasi CV & menerapkan Occam's Razor
    prompt_stat = build_modeling_prompt(
        task_type=task_type,
        primary_metric=primary_metric,
        baseline_score=cv_data["baseline_score"],
        cv_results=cv_data["cv_results"],
        train_scores=cv_data["train_scores"]
    )
    stat_res = agent_stat.think_and_decide(
        prompt=prompt_stat,
        round_name="Ronde 3: Modeling & Occam's Razor",
        state=state,
        stance="PENILAIAN_OCCAM_RAZOR"
    )

    chosen_champion = stat_res.get("champion_model") or "Random Forest"

    # Langkah 2: Robustness Investigator menganalisis Overfit Gap & Ketahanan
    prompt_rob = f"""
Statistician memilih model '{chosen_champion}' dengan rasionalisasi:
{stat_res.get('statistician_rationale')}

Hasil Skor Train vs CV Komputasi Python:
{cv_data['cv_results']}

Sebagai ROBUSTNESS INVESTIGATOR:
1. Hitung dan verifikasi selisih skor Train vs CV (|Train - CV|) untuk '{chosen_champion}'.
2. Apakah gap > 0.10 (overfitting)?
3. Apakah model mengalahkan baseline dummy ({cv_data['baseline_score']:.4f}) secara meyakinkan?
4. Berikan vonis kesehatan: HEALTHY, OVERFITTING, atau UNDERFITTING.
Keluarkan HANYA JSON:
{{
  "robustness_verdict": "HEALTHY / OVERFITTING / UNDERFITTING",
  "overfit_gap_analysis": "string analisis gap",
  "underfit_check": "string evaluasi vs baseline"
}}
"""
    rob_res = agent_rob.think_and_decide(
        prompt=prompt_rob,
        round_name="Ronde 3: Modeling & Occam's Razor",
        state=state,
        stance="UJI_KETAHANAN_OVERFIT"
    )

    # Langkah 3: Skeptic memberikan persetujuan final
    prompt_skep = f"""
Konsensus Modeling:
- Model Champion: {chosen_champion}
- Alasan Statistician: {stat_res.get('statistician_rationale')}
- Vonis Robustness: {rob_res.get('robustness_verdict')} ({rob_res.get('overfit_gap_analysis')})

Sebagai SKEPTIC, apakah kamu menyetujui model champion ini untuk dilatih dan dievaluasi pada unseen test set?
Keluarkan HANYA JSON: {{"decision": "APPROVE atau VETO", "skeptic_final_remarks": "string catatan akhir"}}
"""
    skep_res = agent_skep.think_and_decide(
        prompt=prompt_skep,
        round_name="Ronde 3: Modeling & Occam's Razor",
        state=state,
        stance="KONSENSUS_MODELING"
    )

    # 2. Pelatihan Final & Evaluasi Test Set (Tepat 1 Kali) oleh Python murni
    final_pipe, test_metrics, top_features = fit_and_evaluate_final_model(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        preprocessor=preprocessor,
        champion_model_name=chosen_champion,
        task_type=task_type
    )

    # 3. Uji Validitas Lanjutan: Nadeau-Bengio, Kanari Permutasi, dan Adversarial Validation
    champ_cv_scores = cv_data["cv_results"].get(chosen_champion, {}).get("cv_scores", [])
    base_cv_scores = cv_data["cv_results"].get("Baseline (Dummy)", {}).get("cv_scores", [])
    nadeau_bengio = calculate_nadeau_bengio_ttest(champ_cv_scores, base_cv_scores, n_splits=5)
    canary = run_permutation_canary_test(X_train, y_train, preprocessor, chosen_champion, task_type=task_type)
    adversarial = calculate_adversarial_validation(X_train, X_test)

    state.modeling_plan = {
        "candidate_models": list(cv_data["cv_results"].keys()),
        "champion_model": chosen_champion,
        "statistician_rationale": stat_res.get("statistician_rationale", ""),
        "robustness_verdict": rob_res.get("robustness_verdict", "HEALTHY"),
        "skeptic_approval": skep_res.get("decision", "APPROVE"),
        "nadeau_bengio": nadeau_bengio
    }

    state.modeling_results = {
        "cv_summary": cv_data["cv_results"],
        "baseline_score": cv_data["baseline_score"],
        "test_metrics": test_metrics,
        "top_features": top_features,
        "canary_test": canary,
        "adversarial_validation": adversarial,
        "nadeau_bengio": nadeau_bengio
    }

    return final_pipe, test_metrics, top_features, X_train, y_train
