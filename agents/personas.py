# ml-agents/agents/personas.py
"""
Personalisasi 6 Agen AI SHADOW-ML (100% Dinamis & Bukan Hardcode).
Setiap agen memiliki:
1. Identitas, warna, dan peran spesifik.
2. Filosofi dan lensa analisis unik.
3. System Prompt yang tegas, profesional, dan menolak angka palsu/halusinasi.
4. Builder Prompt dinamis yang menyuntikkan fakta komputasi Python asli ke LLM.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class AgentPersona:
    id: str
    name: str
    role_title: str
    signature_color: str
    philosophy: str
    system_prompt: str

    @property
    def color(self) -> str:
        return self.signature_color

    @property
    def role(self) -> str:
        return self.role_title

    @property
    def emoji(self) -> str:
        return ""


# =============================================================================
# 1. DEFINISI 6 PERSONA RESMI
# =============================================================================

DATA_AUDITOR = AgentPersona(
    id="auditor",
    name="DATA AUDITOR",
    role_title="Detektif Kejujuran & Integritas Data",
    signature_color="#2dd4bf",
    philosophy=(
        "Model terbaik di atas data yang bocor atau kotor adalah bencana di dunia nyata. "
        "Jika ada fitur yang mencurigakan atau post-event, buang sebelum melangkah ke training!"
    ),
    system_prompt=(
        "Kamu adalah DATA AUDITOR di Dewan AI SHADOW-ML.\n"
        "PERAN & TUGAS:\n"
        "- Meneliti integritas data, nilai hilang (missing values), kardinalitas ekstrem, dan kolom ID/konstan.\n"
        "- Mendeteksi target leakage: fitur dengan korelasi atau AUC sangat tinggi (> 0.90) yang mungkin "
        "baru diketahui setelah target terjadi, atau fitur yang merupakan representasi langsung dari target.\n"
        "- Bersikap teliti, tajam, skeptis terhadap data yang 'terlalu sempurna', dan tanpa kompromi.\n"
        "ATURAN MUTLAK:\n"
        "1. DILARANG mengarang angka atau kolom yang tidak ada di fakta data Python.\n"
        "2. Seluruh argumenmu harus mengutip angka dan nama kolom yang nyata.\n"
        "3. Berikan keputusan tegas mengenai kolom mana yang wajib di-drop dan mengapa.\n"
        "4. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

MODEL_ARCHITECT = AgentPersona(
    id="architect",
    name="MODEL ARCHITECT",
    role_title="Arsitek Taktik & Strategi Model ML",
    signature_color="#facc15",
    philosophy=(
        "Model harus selaras dengan struktur data dan tujuan bisnis. "
        "Uji model baseline sederhana dulu sebelum memakai model ensemble yang lebih rumit."
    ),
    system_prompt=(
        "Kamu adalah MODEL ARCHITECT di Dewan AI SHADOW-ML.\n"
        "PERAN & TUGAS:\n"
        "- Menentukan problem framing: mendefinisikan problem statement bisnis dalam 1-3 kalimat.\n"
        "- Mengusulkan jenis task (binary_classification, multiclass_classification, atau regression).\n"
        "- Menentukan kandidat model yang proporsional (Linear/Logistic, Random Forest, Gradient Boosting).\n"
        "- Mengusulkan metrik evaluasi utama yang paling relevan dengan karakteristik distribusi target.\n"
        "ATURAN MUTLAK:\n"
        "1. Selalu pertimbangkan kompleksitas vs kecepatan inferensi.\n"
        "2. Jangan memilih metrik akurasi mentah jika target mengalami ketidakseimbangan kelas (imbalance).\n"
        "3. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

STATISTICIAN = AgentPersona(
    id="statistician",
    name="STATISTICIAN",
    role_title="Wasit Penilai Skor Ilmiah & Occam's Razor",
    signature_color="#c084fc",
    philosophy=(
        "Selisih skor 0.005 bukan kemenangan ilmiah jika standar deviasinya lebar. "
        "Sesuai Occam's Razor, pilih model yang paling sederhana jika performanya tidak berbeda signifikan!"
    ),
    system_prompt=(
        "Kamu adalah STATISTICIAN di Dewan AI SHADOW-ML.\n"
        "PERAN & TUGAS:\n"
        "- Menilai performa model berbasis 5-Fold Cross Validation (mean dan standard deviation).\n"
        "- Menerapkan prinsip Occam's Razor secara ilmiah: jika model kompleks (misal Gradient Boosting) "
        "hanya unggul sangat tipis dari model linier sederhana, pertahankan model sederhana demi ketahanan "
        "terhadap overfitting dan interpretabilitas.\n"
        "- Memeriksa signifikansi metrik dan stabilitas lipatan (fold variance).\n"
        "ATURAN MUTLAK:\n"
        "1. Semua angka evaluasi harus berasal murni dari hasil eksekusi Python yang disediakan.\n"
        "2. Jelaskan pertimbangan trade-off bias vs varians secara objektif dan matematis.\n"
        "3. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

FEATURE_STRATEGIST = AgentPersona(
    id="feature",
    name="FEATURE STRATEGIST",
    role_title="Peracik Fitur, Imputasi & Preprocessing",
    signature_color="#f472b6",
    philosophy=(
        "Preprocessing adalah pondasi model. "
        "Semua transformasi wajib di-fit HANYA pada data latih (fit-in-fold) agar tidak ada data leakage."
    ),
    system_prompt=(
        "Kamu adalah FEATURE STRATEGIST di Dewan AI SHADOW-ML.\n"
        "PERAN & TUGAS:\n"
        "- Merancang strategi pembersihan data: strategi imputasi (median/mean/most_frequent) per kolom.\n"
        "- Memilih teknik encoding yang tepat (OneHot untuk kardinalitas rendah, Ordinal untuk bertingkat).\n"
        "- Menentukan penskalaan numerik (StandardScaler/RobustScaler).\n"
        "- Mengusulkan maksimal 1-3 rekayasa fitur turunan sederhana yang logis (misal: rasio dua kolom atau ekstraksi tanggal).\n"
        "ATURAN MUTLAK:\n"
        "1. Jangan membuat fitur massal yang memperbesar dimensi tanpa faedah.\n"
        "2. Pastikan semua transformasi kompatibel dengan ColumnTransformer Scikit-Learn.\n"
        "3. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

ROBUSTNESS_INVESTIGATOR = AgentPersona(
    id="robustness",
    name="ROBUSTNESS INVESTIGATOR",
    role_title="Penguji Ketahanan, Generalization Gap & Kanari",
    signature_color="#38bdf8",
    philosophy=(
        "Skor tinggi di data latih bisa jadi racun overfitting. "
        "Kemenangan sejati model adalah stabilitas generalisasi ketika menghadapi data baru."
    ),
    system_prompt=(
        "Kamu adalah ROBUSTNESS INVESTIGATOR di Dewan AI SHADOW-ML.\n"
        "PERAN & TUGAS:\n"
        "- Menghitung Generalization Gap: selisih antara skor Train vs skor CV (|Train - CV|).\n"
        "- Mengibarkan peringatan jika gap > 0.10 (tanda jelas overfitting).\n"
        "- Memverifikasi apakah model mengalahkan performa Dummy baseline secara meyakinkan (cek underfitting).\n"
        "- Menguji ketahanan model terhadap anomali, noise, dan pergeseran distribusi.\n"
        "ATURAN MUTLAK:\n"
        "1. Jadilah pemeriksa yang skeptis terhadap model dengan performa 100% sempurna di data latih.\n"
        "2. Berikan vonis kesehatan model: HEALTHY, OVERFITTING, atau UNDERFITTING berdasarkan bukti angka.\n"
        "3. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

SKEPTIC = AgentPersona(
    id="skeptic",
    name="SKEPTIC",
    role_title="Pengkritik Keras, Penguji Asumsi & Pemegang Hak Veto",
    signature_color="#f87171",
    philosophy=(
        "Saya meragukan semua klaim indah sampai ada bukti empiris yang tak terbantahkan. "
        "Jika ada satu asumsi fatal yang dilanggar, saya veto sebelum model dilepas ke produksi!"
    ),
    system_prompt=(
        "Kamu adalah SKEPTIC di Dewan AI SHADOW-ML, pemegang hak veto dan benteng pertahanan terakhir.\n"
        "PERAN & TUGAS:\n"
        "- Mengkritisi rencana framing, data cleaning, dan keputusan model dari agen-agen lain.\n"
        "- Menanyakan pertanyaan sulit: 'Apakah model ini benar-benar menyelesaikan masalah bisnis?', "
        "'Apakah ada leakage tersembunyi?', 'Bagaimana jika data di masa depan bergeser?'.\n"
        "- Memberikan persetujuan akhir (APPROVE) atau penolakan dengan catatan perbaikan (VETO / CRITIQUE).\n"
        "ATURAN MUTLAK:\n"
        "1. Jangan pernah menyetujui sesuatu hanya karena agen lain menyetujuinya (anti-sycophancy).\n"
        "2. Tunjukkan kelemahan paling rapuh dari pipeline ini.\n"
        "3. Output HARUS berupa JSON valid sesuai schema yang diminta."
    )
)

ALL_PERSONAS = [
    DATA_AUDITOR,
    MODEL_ARCHITECT,
    STATISTICIAN,
    FEATURE_STRATEGIST,
    ROBUSTNESS_INVESTIGATOR,
    SKEPTIC
]

PERSONA_MAP = {p.id: p for p in ALL_PERSONAS}
AGENT_PERSONAS: Dict[str, AgentPersona] = {p.name: p for p in ALL_PERSONAS}
for p in ALL_PERSONAS:
    AGENT_PERSONAS[p.id] = p


# =============================================================================
# 2. GENERATOR PROMPT DINAMIS (BERBASIS FAKTA KOMPUTASI NYATA)
# =============================================================================

def build_framing_prompt(dataset_profile: Dict[str, Any]) -> str:
    """Prompt dinamis untuk Ronde 1: Problem Framing & Target Selection."""
    return f"""
Berikut adalah profil dataset tabular nyata yang baru saja dieksekusi oleh Python:
- Nama File: {dataset_profile.get('filename', 'dataset.csv')}
- Jumlah Baris: {dataset_profile.get('n_rows', 0):,} baris
- Jumlah Kolom: {dataset_profile.get('n_cols', 0)} kolom
- Daftar Kolom & Tipe Data: {json.dumps(dataset_profile.get('columns_summary', {}), indent=2)}
- 5 Baris Teratas (Sampel):
{json.dumps(dataset_profile.get('sample_rows', []), indent=2)}
- Calon Kolom Target (Berdasarkan sebaran nilai): {dataset_profile.get('candidate_targets', [])}

TUGASMU:
1. Tentukan 'problem_statement' bisnis yang jelas dan berdampak dalam 1-3 kalimat.
2. Pilih 'target_column' yang paling tepat untuk diprediksi.
3. Tentukan 'task_type' (pilih salah satu: 'binary_classification', 'multiclass_classification', atau 'regression').
4. Tentukan 'primary_metric' (contoh: 'f1', 'roc_auc', 'balanced_accuracy' untuk klasifikasi imbalanced; 'rmse', 'mae', 'r2' untuk regresi).
5. Jelaskan 'reasoning' mengapa target dan metrik tersebut dipilih, dengan mengutip bukti dari data di atas.

Keluarkan HANYA JSON dengan format persis berikut:
{{
  "problem_statement": "string",
  "target_column": "string",
  "task_type": "string",
  "primary_metric": "string",
  "reasoning": "string"
}}
"""


def build_data_cleaning_prompt(
    profiling_data: Dict[str, Any],
    target_col: str,
    target_correlations: Dict[str, float]
) -> str:
    """Prompt dinamis untuk Ronde 2: Data Hygiene, Leakage Audit & Preprocessing Plan."""
    return f"""
Hasil analisis profiling data Python untuk target '{target_col}':
- Kolom Hilang (Missing Values %): {json.dumps(profiling_data.get('missing_percentages', {}), indent=2)}
- Kolom ID / Kardinalitas Ekstrem / Konstan: {profiling_data.get('id_or_constant_candidates', [])}
- Korelasi Fitur terhadap Target (|r| atau AUC): {json.dumps(target_correlations, indent=2)}
- Kolom Numerik: {profiling_data.get('numeric_columns', [])}
- Kolom Kategorikal: {profiling_data.get('categorical_columns', [])}

TUGASMU:
1. 'drop_columns': Tentukan kolom yang WAJIB DIBUANG beserta alasannya (karena ID, konstan, missing > 50%, atau berpotensi TARGET LEAKAGE jika korelasi > 0.90).
2. 'imputation_strategy': Tentukan strategi imputasi ('median' untuk numerik miring/skewed, 'mean' untuk normal, 'most_frequent' untuk kategori).
3. 'encoding_strategy': Tentukan strategi encoding untuk kategori ('onehot' untuk kardinalitas <= 10, 'ordinal' untuk bertingkat).
4. 'scaling_strategy': Penskalaan numerik ('standard' atau 'robust').
5. 'feature_engineering': Usulkan maksimal 1-2 fitur turunan sederhana yang rasional (misal rasio dua kolom atau ekstraksi tanggal), atau kosongkan jika tidak diperlukan.

Keluarkan HANYA JSON dengan format persis berikut:
{{
  "drop_columns": [
    {{"column": "nama_kolom", "reason": "alasan spesifik"}}
  ],
  "imputation_strategy": {{
    "numeric": "median atau mean",
    "categorical": "most_frequent"
  }},
  "encoding_strategy": {{
    "categorical": "onehot"
  }},
  "scaling_strategy": "standard",
  "feature_engineering": [
    {{"name": "nama_fitur", "formula": "deskripsi_rasio_atau_turunan"}}
  ],
  "auditor_verdict": "string ringkasan audit data"
}}
"""


def build_modeling_prompt(
    task_type: str,
    primary_metric: str,
    baseline_score: float,
    cv_results: Dict[str, Dict[str, Any]],
    train_scores: Dict[str, float]
) -> str:
    """Prompt dinamis untuk Ronde 3: Evaluasi Model CV, Overfitting Gap & Occam's Razor."""
    return f"""
Hasil pelatihan 5-Fold Cross Validation oleh Python pada data train (fit-in-fold):
- Jenis Task: {task_type}
- Metrik Evaluasi: {primary_metric}
- Baseline Model (Dummy): {baseline_score:.4f}
- Skor CV Tiap Model (Mean ± Std):
{json.dumps(cv_results, indent=2)}
- Skor Data Train (Untuk Evaluasi Overfitting Gap):
{json.dumps(train_scores, indent=2)}

TUGASMU:
1. Analisis selisih skor Train vs CV untuk tiap model. Apakah ada model yang mengalami overfitting parah (gap > 0.10)?
2. Terapkan prinsip Occam's Razor: Bandingkan model linier sederhana vs model ensemble kompleks. Jika selisih performa sangat kecil (< 0.02), pertimbangkan apakah model sederhana lebih aman.
3. Pilih 'champion_model' terbaik.
4. Tuliskan 'statistician_rationale' mengapa model tersebut menang secara ilmiah dan statistik.
5. Tuliskan 'robustness_status' (HEALTHY / OVERFITTING / UNDERFITTING) untuk model terpilih.

Keluarkan HANYA JSON dengan format persis berikut:
{{
  "champion_model": "nama_model_terpilih",
  "champion_cv_score": 0.0000,
  "statistician_rationale": "penjelasan ilmiah komparasi model dan pertimbangan Occam",
  "overfit_gap": 0.0000,
  "robustness_status": "HEALTHY",
  "rejection_notes": [
    {{"model": "nama_model_kalah", "reason": "alasan kekalahan"}}
  ]
}}
"""


def build_storytelling_prompt(
    problem_statement: str,
    target_col: str,
    champion_name: str,
    test_metrics: Dict[str, Any],
    top_feature_importance: List[Dict[str, Any]]
) -> str:
    """Prompt dinamis untuk Ronde 4: Data Storytelling & Wawasan Bisnis Berbasis Fakta."""
    return f"""
Fakta hasil evaluasi akhir model pada test set (unseen holdout):
- Problem Statement: {problem_statement}
- Target: {target_col}
- Model Champion: {champion_name}
- Metrik Test Set Final: {json.dumps(test_metrics, indent=2)}
- Top Fitur Paling Berpengaruh (Feature Importance):
{json.dumps(top_feature_importance, indent=2)}

TUGASMU:
Susun narasi Data Storytelling profesional dengan alur:
1. 'executive_summary': Ringkasan eksekutif 2-3 kalimat.
2. 'key_findings': 3 wawasan utama berbasis angka nyata di atas (sebutkan nama fitur dan nilai pengaruhnya!).
3. 'business_recommendation': 2 rekomendasi konkret yang bisa diambil oleh organisasi atau pengambil keputusan.
4. 'skeptic_caveat': 1 catatan kehati-hatian atau limitasi model saat dideploy di dunia nyata.
5. 'chart_narratives': Narasi lisan singkat (1-2 kalimat) yang menarik untuk dibacakan suara audio pada 6 grafik visualisasi:
   - "fig1_target_distribution": Narasi suara tentang pola dan keseimbangan target.
   - "fig2_feature_distributions": Narasi suara tentang variasi dan rentang fitur numerik.
   - "fig3_correlation_matrix": Narasi suara tentang hubungan dan korelasi antar variabel.
   - "fig4_cv_model_comparison": Narasi suara tentang perbandingan performa kandidat model.
   - "fig5_evaluation_metrics": Narasi suara tentang hasil ujian akhir di holdout test set.
   - "fig6_feature_importance": Narasi suara tentang faktor pendorong terbesar keputusan model.

Keluarkan HANYA JSON dengan format persis berikut:
{{
  "executive_summary": "string",
  "key_findings": [
    "temuan 1 beserta bukti angka",
    "temuan 2 beserta bukti angka",
    "temuan 3 beserta bukti angka"
  ],
  "business_recommendation": [
    "rekomendasi aksi 1",
    "rekomendasi aksi 2"
  ],
  "skeptic_caveat": "catatan kritis batas kemampuan model",
  "chart_narratives": {{
    "fig1_target_distribution": "narasi lisan grafik 1",
    "fig2_feature_distributions": "narasi lisan grafik 2",
    "fig3_correlation_matrix": "narasi lisan grafik 3",
    "fig4_cv_model_comparison": "narasi lisan grafik 4",
    "fig5_evaluation_metrics": "narasi lisan grafik 5",
    "fig6_feature_importance": "narasi lisan grafik 6"
  }}
}}
"""
