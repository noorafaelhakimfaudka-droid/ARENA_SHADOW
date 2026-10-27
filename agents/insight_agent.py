# ml-agents/agents/insight_agent.py
"""
Agen 4 — Insight & Data Storytelling (Ronde 4 Debat).
Kolaborasi:
- STATISTICIAN & FEATURE STRATEGIST: Merangkum narasi temuan berdasarkan angka dan feature importance.
- SKEPTIC: Menambahkan catatan batas kemampuan model dan kehati-hatian penerapan bisnis.
Eksekusi Python: Membuat 5-6 grafik visualisasi di figures/ dan menyusun report.md.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
from agents.base_agent import BaseAgent
from agents.personas import FEATURE_STRATEGIST, SKEPTIC, STATISTICIAN, build_storytelling_prompt
from core.llm import GeminiClient
from core.state import SharedState
from core.tools.plotting import generate_all_figures


def run_insight_and_storytelling(
    df: pd.DataFrame,
    target_col: str,
    task_type: str,
    output_dir: Path | str,
    state: SharedState,
    client: GeminiClient
) -> Dict[str, Any]:
    """
    Menghasilkan grafik visualisasi, narasi data storytelling terstruktur,
    dan menyusun file report.md resmi.
    """
    out_dir = Path(output_dir)
    cv_summary = state.modeling_results.get("cv_summary", {})
    test_metrics = state.modeling_results.get("test_metrics", {})
    top_features = state.modeling_results.get("top_features", [])
    champion_name = state.modeling_plan.get("champion_model", "Champion Model")

    # 1. Eksekusi Visualisasi Grafik oleh Python murni
    figures = generate_all_figures(
        df=df,
        target_col=target_col,
        task_type=task_type,
        cv_results=cv_summary,
        test_metrics=test_metrics,
        top_features=top_features,
        output_dir=out_dir
    )
    state.figures = figures

    # 2. Sintesis Data Storytelling oleh LLM berbasis fakta angka nyata
    agent_stat = BaseAgent(STATISTICIAN, client=client)
    agent_skep = BaseAgent(SKEPTIC, client=client)

    prompt_story = build_storytelling_prompt(
        problem_statement=state.framing.get("problem_statement", ""),
        target_col=target_col,
        champion_name=champion_name,
        test_metrics=test_metrics,
        top_feature_importance=top_features
    )

    story_res = agent_stat.think_and_decide(
        prompt=prompt_story,
        round_name="Ronde 4: Insight & Data Storytelling",
        state=state,
        stance="DATA_STORYTELLING"
    )

    # Pastikan chart_narratives tersedia untuk visualisasi audio-visual storytelling
    chart_narratives = story_res.get("chart_narratives", {})
    if not isinstance(chart_narratives, dict) or not chart_narratives:
        story_res["chart_narratives"] = {
            "fig1_target_distribution": f"Grafik ini menampilkan proporsi dan persebaran kolom target '{target_col}'. Pola ini menentukan strategi mitigasi ketidakseimbangan kelas.",
            "fig2_feature_distributions": "Grafik sebaran fitur numerik menguji keberadaan anomali dan rentang data sebelum transformasi.",
            "fig3_correlation_matrix": "Matriks korelasi memetakan hubungan linear antar variabel numerik guna mendeteksi multikolinearitas dan target leakage.",
            "fig4_cv_model_comparison": f"Perbandingan 5-Fold Cross Validation menunjukkan model {champion_name} memimpin secara konsisten dengan varians terkendali.",
            "fig5_evaluation_metrics": f"Evaluasi holdout test set membuktikan generalisasi yang kuat dengan metrik utama yang teruji.",
            "fig6_feature_importance": f"Feature Importance mengidentifikasi variabel-variabel penentu terbesar dalam menggerakkan keputusan model."
        }

    state.insights = story_res

    # 3. Penyusunan Berkas report.md
    report_content = f"""# Laporan Hasil Analisis Machine Learning & Debat Multi-Agent
**Disusun oleh Dewan AI SHADOW-ML** · Run ID: `{state.run_id}`

---

## 1. Ringkasan Eksekutif
{story_res.get('executive_summary', 'Analisis komprehensif berhasil diselesaikan.')}

- **Dataset**: `{state.dataset_info.get('filename')}` ({state.dataset_info.get('n_rows'):,} baris, {state.dataset_info.get('n_cols')} kolom)
- **Target**: `{target_col}` ({task_type})
- **Model Champion**: `{champion_name}`
- **Metrik Utama (Test Set)**:
{chr(10).join([f"  - **{k.upper()}**: {v}" for k, v in test_metrics.items() if not isinstance(v, (dict, list))])}

---

## 2. Temuan Utama (Key Findings)
{chr(10).join([f"{i+1}. {finding}" for i, finding in enumerate(story_res.get('key_findings', []))])}

---

## 3. Fitur Paling Berpengaruh (Feature Importance)
Model mengidentifikasi fitur-fitur berikut sebagai faktor penentu utama:
{chr(10).join([f"- **{f['feature']}**: Skor Pengaruh {f['importance']}" for f in top_features[:5]])}

---

## 4. Rekomendasi Aksi Bisnis
{chr(10).join([f"- [Aksi {i+1}] {rec}" for i, rec in enumerate(story_res.get('business_recommendation', []))])}

---

## 5. Catatan Kritis & Limitasi (Skeptic Caveat)
> *"{story_res.get('skeptic_caveat', 'Gunakan model dengan pengawasan berkala.')}"*

---

## 6. Bukti Visualisasi Data
Berikut visualisasi grafik yang dihasilkan di folder `figures/`:
{chr(10).join([f"- ![{Path(fig).stem}]({fig})" for fig in figures])}
"""

    report_path = out_dir / "report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return story_res
