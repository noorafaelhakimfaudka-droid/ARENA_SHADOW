# ml-agents/agents/framing_agent.py
"""
Agen 1 — Problem Framing (Ronde 1 Debat).
Kolaborasi & Debat:
- MODEL ARCHITECT: Mengusulkan problem statement, target, task_type, dan primary_metric.
- DATA AUDITOR: Mengaudit calon target, sebaran nilai, dan potensi bias.
- SKEPTIC: Menguji apakah metrik yang dipilih realistis dan menyetujui framing akhir.
Validasi Python: Memastikan target ada di dataset dan task_type sesuai dengan kardinalitas target.
"""

from __future__ import annotations
from typing import Any, Dict
import pandas as pd
from agents.base_agent import BaseAgent
from agents.personas import DATA_AUDITOR, MODEL_ARCHITECT, SKEPTIC, build_framing_prompt
from core.llm import GeminiClient
from core.state import SharedState
from core.tools.profiling import profile_dataset


def run_framing_debate(
    df: pd.DataFrame,
    state: SharedState,
    client: GeminiClient,
    force_target: str = ""
) -> Dict[str, Any]:
    """
    Menjalankan debat Ronde 1 (Framing) secara dinamis menggunakan Gemini.
    Menghasilkan framing akhir yang divalidasi oleh Python.
    """
    # 1. Profiling awal oleh Python murni
    profile = profile_dataset(df)
    state.dataset_info = {
        "filename": profile["filename"],
        "n_rows": profile["n_rows"],
        "n_cols": profile["n_cols"],
        "numeric_cols": profile["numeric_columns"],
        "categorical_cols": profile["categorical_columns"]
    }

    # Jika pengguna memaksakan target tertentu via CLI
    if force_target and force_target in df.columns:
        profile["candidate_targets"] = [force_target]

    # Inisialisasi Agen
    agent_arch = BaseAgent(MODEL_ARCHITECT, client=client)
    agent_aud = BaseAgent(DATA_AUDITOR, client=client)
    agent_skep = BaseAgent(SKEPTIC, client=client)

    # Langkah 1: Model Architect mengusulkan framing
    prompt_arch = build_framing_prompt(profile)
    arch_proposal = agent_arch.think_and_decide(
        prompt=prompt_arch,
        round_name="Ronde 1: Problem Framing",
        state=state,
        stance="USULAN_FRAMING"
    )

    chosen_target = arch_proposal.get("target_column") or profile["candidate_targets"][0]
    # Validasi Python: Target harus ada di DataFrame
    if chosen_target not in df.columns:
        chosen_target = profile["candidate_targets"][0]

    # Langkah 2: Data Auditor mengaudit target
    target_series = df[chosen_target].dropna()
    n_unique_target = target_series.nunique()
    is_num = pd.api.types.is_numeric_dtype(target_series)
    
    # Python menentukan task_type nyata
    is_float = pd.api.types.is_float_dtype(target_series)
    if is_float and n_unique_target > 2:
        validated_task = "regression"
    elif n_unique_target == 2:
        validated_task = "binary_classification"
    elif 3 <= n_unique_target <= 15 and not is_float:
        validated_task = "multiclass_classification"
    else:
        validated_task = "regression" if is_num else "multiclass_classification"

    prompt_aud = f"""
Model Architect mengusulkan target '{chosen_target}' dengan tipe task '{arch_proposal.get('task_type')}'.
Fakta Python:
- Jumlah nilai unik target: {n_unique_target}
- Sebaran nilai target: {target_series.value_counts(normalize=True).head(5).to_dict()}
- Tipe data target: {target_series.dtype}

Sebagai DATA AUDITOR, berikan audit kejujuranmu terhadap target ini. Apakah ada ketidakseimbangan kelas (imbalance)?
Keluarkan HANYA JSON: {{"audit_verdict": "string penjelasan audit target", "is_target_valid": true}}
"""
    aud_res = agent_aud.think_and_decide(
        prompt=prompt_aud,
        round_name="Ronde 1: Problem Framing",
        state=state,
        stance="AUDIT_TARGET"
    )

    # Langkah 3: Skeptic menguji dan menetapkan konsensus
    prompt_skep = f"""
Usulan Model Architect:
- Problem: {arch_proposal.get('problem_statement')}
- Target: {chosen_target}
- Metrik Usulan: {arch_proposal.get('primary_metric')}

Audit Data Auditor:
- {aud_res.get('audit_verdict')}

Sebagai SKEPTIC, evaluasi apakah metrik '{arch_proposal.get('primary_metric')}' sudah tepat untuk kasus ini.
Tetapkan metrik akhir dan berikan catatan kritis.
Keluarkan HANYA JSON: {{"decision": "APPROVE atau CRITIQUE", "final_metric": "nama_metrik", "skeptic_note": "string"}}
"""
    skep_res = agent_skep.think_and_decide(
        prompt=prompt_skep,
        round_name="Ronde 1: Problem Framing",
        state=state,
        stance="EVALUASI_KRITIS_FRAMING"
    )

    final_metric = skep_res.get("final_metric") or arch_proposal.get("primary_metric") or "roc_auc"
    if validated_task == "regression" and final_metric.lower() in ("roc_auc", "f1", "accuracy"):
        final_metric = "r2"

    framing_result = {
        "problem_statement": arch_proposal.get("problem_statement", f"Prediksi {chosen_target} berbasis machine learning"),
        "target_column": chosen_target,
        "task_type": validated_task,
        "primary_metric": final_metric,
        "reasoning": arch_proposal.get("reasoning", ""),
        "skeptic_note": skep_res.get("skeptic_note", "")
    }

    state.framing = framing_result
    return framing_result
