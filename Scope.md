# Scope Proyek: Multi-Agent Machine Learning Assistant

Dokumen ini adalah batasan resmi proyek. Semua fitur di luar dokumen ini **tidak dikerjakan** sampai seluruh "Definisi Selesai" (Bagian 9) terpenuhi dan disetujui instruktur.

---

## 1. Tujuan Proyek

Membangun sistem multi-agent yang menerima **satu file CSV tabular**, lalu secara otomatis:

1. memahami data dan menentukan problem statement,
2. membersihkan dan menyiapkan data,
3. memilih, melatih, dan mengevaluasi model machine learning dengan benar,
4. menghasilkan insight, visualisasi, dan cerita data (data storytelling),
5. menghasilkan notebook `.ipynb` yang bisa dijalankan ulang dari awal sampai akhir,
6. menyimpan model final supaya pengguna bisa **memasukkan data baru dan langsung mendapat hasil prediksi**.

Fokus proyek ini adalah **membangun machine learning dari nol dengan benar**, bukan tampilan atau animasi.

---

## 2. Prinsip Utama (Wajib)

1. **LLM memutuskan, Python mengerjakan.**
   - Agen (LLM) membuat *rencana* dan *keputusan* dalam format JSON.
   - Eksekusi (pandas, scikit-learn, matplotlib) dilakukan oleh kode Python.
2. **Semua angka berasal dari eksekusi kode.**
   - LLM tidak boleh menulis angka metrik, jumlah baris, atau korelasi dari "kepalanya sendiri".
   - Angka dimasukkan ke narasi dari hasil komputasi.
3. **Tidak ada data hardcode.**
   - Dataset berbeda harus menghasilkan problem statement, cleaning, model, dan insight yang berbeda.
4. **Gagal harus terlihat.**
   - Jika LLM mati atau error, tampilkan pesan error yang jelas.
   - Jangan diam-diam memakai teks cadangan yang seolah-olah hasil agen.
5. **Klaim harus bisa dibuktikan.**
   - README hanya boleh mengklaim hal yang bisa dijalankan dan dicek instruktur.

---

## 3. Batasan Data

| Termasuk | Tidak termasuk |
|---|---|
| Satu file CSV tabular | Gabungan beberapa tabel / database |
| Maksimal ±50.000 baris, ±50 kolom | Big data |
| Klasifikasi biner, klasifikasi multikelas, regresi | Time series forecasting, clustering, rekomendasi |
| Kolom numerik, kategorikal, tanggal sederhana | Teks bebas/NLP, gambar, audio |

Dataset uji wajib (minimal 3, berbeda jenis):
- 1 klasifikasi biner (contoh: Titanic, Telco Churn),
- 1 regresi (contoh: House Prices, Insurance Charges),
- 1 dataset pilihan sendiri yang **belum pernah dipakai saat development**.

---

## 4. Arsitektur

### 4.1 Alur Agen (berurutan, tanpa debat)

    CSV
     │
     ▼
    [Agen 1: Problem Framing] ──► problem statement, target, jenis tugas, metrik
     │
     ▼
    [Agen 2: Data] ──► profil data, rencana cleaning, feature engineering → data bersih
     │
     ▼
    [Agen 3: Modeling] ──► split, baseline + kandidat model, CV, cek leakage/overfit, evaluasi test
     │
     ▼
    [Agen 4: Insight & Storytelling] ──► grafik + narasi berdasarkan angka hasil eksekusi
     │
     ▼
    [Agen 5: Notebook Generator] ──► notebook.ipynb yang dijalankan ulang dan diverifikasi
     │
     ▼
    model.joblib + schema.json disimpan
     │
     ▼
    [Mode Prediksi] input data baru ──► validasi ──► model ──► hasil prediksi + penjelasan

- Agen saling berbagi **satu objek state** (dict, disimpan sebagai `state.json`).
- Setiap agen membaca state, menambah bagiannya, lalu meneruskan state.
- **Tidak ada** debat, voting, koalisi, skor reputasi, atau "putaran kritik".

### 4.2 LLM
- Pakai **satu penyedia saja**: Gemini **atau** Ollama lokal. Pilih satu, jangan dua-duanya.
- API key disimpan di `.env` (sediakan `.env.example`), jangan di dalam kode.
- Setiap panggilan LLM dicatat ke `llm_log.jsonl`: waktu, agen, prompt, respons.
- Output LLM wajib JSON dan divalidasi. Jika tidak valid, coba ulang maksimal 2x, lalu tampilkan error.

---

## 5. Spesifikasi Agen

### Agen 1 — Problem Framing
- **Input:** nama kolom, tipe data, 5–10 baris sampel, statistik ringkas.
- **Tugas:**
  - menentukan problem statement dalam 1–3 kalimat,
  - menentukan kolom target,
  - menentukan jenis tugas (klasifikasi/regresi),
  - menentukan metrik utama beserta alasannya.
- **Output (contoh):**

      {
        "problem_statement": "Memprediksi apakah pelanggan akan berhenti berlangganan ...",
        "target": "churn",
        "task_type": "binary_classification",
        "primary_metric": "f1",
        "reason": "Kelas tidak seimbang sehingga akurasi menyesatkan ..."
      }

- **Validasi Python:** target harus ada di dataset, dan jenis tugas harus cocok dengan isi kolom target.

### Agen 2 — Data (Understanding, Processing, Cleaning, Feature Engineering)
- **Input:** hasil profiling dari Python (missing, duplikat, tipe, outlier, kardinalitas).
- **Tugas:** membuat rencana dalam JSON, lalu Python mengeksekusinya.
  - Kolom yang dibuang, beserta alasannya (ID, konstan, terlalu banyak missing).
  - Strategi imputasi per kolom.
  - Encoding kategorikal dan scaling.
  - Maksimal 3 fitur turunan sederhana, misalnya ekstraksi tanggal atau rasio dua kolom.
- **Batasan:** semua langkah transformasi dimasukkan ke `sklearn.Pipeline` / `ColumnTransformer` supaya hanya di-fit pada data train.
- **Di luar scope:** pembuatan fitur otomatis massal, deteksi anomali dengan model.

### Agen 3 — Modeling & Evaluasi
- **Wajib:**
  - Train/test split (80/20, stratified untuk klasifikasi, `random_state` tetap).
  - Baseline `DummyClassifier` / `DummyRegressor`.
  - 3 kandidat model: Linear/Logistic Regression, Random Forest, Gradient Boosting.
  - 5-fold cross-validation **hanya pada data train**.
  - Agen memilih model terbaik dan menjelaskan alasannya, berdasarkan skor CV hasil eksekusi.
- **Cek kualitas (dihitung Python, dijelaskan agen):**
  - **Leakage:**
    - fitur dengan korelasi/AUC sangat tinggi terhadap target (> 0.95),
    - kolom ID,
    - kolom yang jelas baru diketahui setelah kejadian.
  - **Overfitting:** selisih skor train vs CV besar (contoh: > 0.10).
  - **Underfitting:** model tidak jauh lebih baik dari baseline Dummy.
- **Tuning:** opsional, hanya grid kecil (maksimal ±20 kombinasi) untuk model terpilih.
- **Evaluasi akhir:**
  - Test set dipakai **satu kali** untuk model final.
  - Klasifikasi: classification report dan confusion matrix.
  - Regresi: MAE, RMSE, R², dan plot residual.
- **Di luar scope:** deep learning, AutoML, XGBoost/LightGBM (boleh hanya jika semua sudah selesai), uji statistik lanjutan.

### Agen 4 — Insight & Data Storytelling
- **Grafik wajib (5–8 grafik, dibuat oleh matplotlib/seaborn):**
  - distribusi target,
  - distribusi 2–3 fitur penting,
  - heatmap korelasi,
  - hubungan target vs fitur penting,
  - confusion matrix atau plot residual,
  - feature importance.
- **Tugas agen:**
  - menulis narasi data storytelling dengan alur **konteks → temuan → bukti (grafik/angka) → rekomendasi**,
  - menulis 3–5 insight utama.
- **Aturan:** setiap angka dalam narasi harus berasal dari hasil komputasi yang dikirim ke agen.
- **Output:** `report.md` dan folder `figures/`.

### Agen 5 — Notebook Generator
- **Tugas:**
  - Merakit `notebook.ipynb` dengan `nbformat` dari langkah-langkah yang **benar-benar dijalankan**: load → framing → cleaning → modeling → evaluasi → insight.
  - Sel markdown berisi penjelasan dari agen.
  - Sel kode berasal dari template/kode yang sudah dieksekusi, tidak ditulis bebas oleh LLM tanpa dijalankan.
- **Verifikasi wajib:**
  - Notebook dijalankan ulang dengan `nbclient`.
  - Harus selesai tanpa error.
  - Metrik di notebook harus sama dengan hasil pipeline (toleransi 0.001).

### Fitur Interaksi — Prediksi Data Baru
Setelah pipeline selesai, model final bisa dipakai untuk memprediksi data baru.

- **Yang disimpan saat training** (di `outputs/<run_id>/`):
  - `model.joblib`: **seluruh** Pipeline (preprocessing + model), supaya data baru diproses dengan cara yang persis sama.
  - `schema.json`: daftar kolom input, tipe data, rentang nilai (min/max) untuk numerik, dan nilai yang dikenal untuk kategorikal.
- **Cara input (pilih minimal 2):**
  1. **Interaktif di CLI:** `python main.py predict --run outputs/<run_id>`. Program menanyakan nilai tiap kolom satu per satu.
  2. **Satu baris JSON:** `python main.py predict --run outputs/<run_id> --json '{"age": 30, "contract": "Month-to-month", ...}'`
  3. **Batch CSV:** `python main.py predict --run outputs/<run_id> --input data_baru.csv`. Hasilnya ditulis ke `predictions.csv`.
- **Validasi input (dikerjakan Python):**
  - kolom wajib tidak boleh hilang,
  - tipe data harus benar,
  - beri peringatan jika nilai numerik di luar rentang data latih atau kategori belum pernah dilihat,
  - kolom yang dibuang saat training (misal ID) boleh diabaikan.
- **Output yang ditampilkan:**
  - **Klasifikasi:** label prediksi dan probabilitas tiap kelas (contoh: `Churn = Ya (probabilitas 0.82)`).
  - **Regresi:** nilai prediksi dan perkiraan rentang error berdasarkan MAE test set (contoh: `Harga = 350.000 ± 25.000`).
  - **Penjelasan singkat** (opsional, oleh Agen 4): 2–3 kalimat yang menyebut fitur paling berpengaruh. Penjelasan ini dibuat dari feature importance atau kontribusi yang dihitung Python, tidak dikarang LLM.
- **Batasan:**
  - Hanya memakai model hasil run yang sudah ada. Tidak ada training ulang saat prediksi.
  - Tidak ada API/server. Cukup CLI, atau form Streamlit sederhana setelah M6.

---

## 6. Di Luar Scope (Jangan Dikerjakan)

- Arena/animasi/UI bergaya game, avatar agen, efek suara.
- Debat antar agen, voting, koalisi, "political war", agen placebo.
- Vault enkripsi, sandbox keamanan, deteksi prompt injection.
- Benchmark puluhan run, gate milestone formal, dokumen PRD panjang.
- Lebih dari satu penyedia LLM, fine-tuning LLM.
- Deployment (API, Docker, cloud), login pengguna.
- Badge atau angka "VERIFIED"/"LOLOS" yang ditulis manual di UI atau README.

UI boleh dibuat **hanya setelah M6 selesai**, cukup CLI atau satu halaman Streamlit sederhana (upload CSV → jalankan → tampilkan laporan → unduh notebook → form input prediksi).

---

## 7. Struktur Folder yang Disarankan

    ml-agents/
    ├── main.py                 # python main.py train data/titanic.csv
    │                           # python main.py predict --run outputs/<run_id>
    ├── Scope.md
    ├── README.md
    ├── requirements.txt
    ├── .env.example
    ├── core/
    │   ├── llm.py              # satu klien LLM + logging + validasi JSON
    │   ├── state.py            # struktur state bersama
    │   └── tools/              # fungsi Python murni (tanpa LLM)
    │       ├── profiling.py
    │       ├── cleaning.py
    │       ├── modeling.py
    │       ├── plotting.py
    │       ├── notebook.py
    │       └── predict.py      # load model.joblib + schema.json, validasi input, prediksi
    ├── agents/
    │   ├── framing_agent.py
    │   ├── data_agent.py
    │   ├── modeling_agent.py
    │   ├── insight_agent.py
    │   └── notebook_agent.py
    ├── data/                   # dataset uji
    ├── outputs/<run_id>/       # state.json, llm_log.jsonl, figures/, report.md, notebook.ipynb,
    │                           # model.joblib, schema.json, predictions.csv
    └── tests/

Aturan: `core/tools/` **tidak boleh** memanggil LLM. `agents/` **tidak boleh** melatih model langsung; agen memanggil fungsi di `core/tools/`.

---

## 8. Tahapan Pengerjaan

Setiap tahap diakhiri **demo ke instruktur** sebelum lanjut ke tahap berikutnya.

| Tahap | Isi | Bukti selesai |
|---|---|---|
| **M1** | Pipeline ML biasa **tanpa LLM**: load → cleaning → split → 3 model + baseline → evaluasi → grafik | Berjalan di 2 dataset, hasil masuk akal |
| **M2** | `core/llm.py` + Agen 1 (Framing) + Agen 2 (Data) | `llm_log.jsonl` terisi; framing berbeda untuk dataset berbeda |
| **M3** | Agen 3 (Modeling & Evaluasi) + cek leakage/overfit/underfit | Dataset dengan leakage yang sengaja ditanam berhasil terdeteksi |
| **M4** | Agen 4 (Insight) + Agen 5 (Notebook) | Notebook berjalan ulang tanpa error dan metriknya cocok |
| **M5** | Mode prediksi: simpan `model.joblib` + `schema.json`, perintah `predict` (interaktif, JSON, batch CSV) | Input data baru → hasil prediksi keluar; input salah → pesan error yang jelas |
| **M6** | Uji di 3 dataset (termasuk 1 dataset baru), README jujur, presentasi | Semua poin Bagian 9 terpenuhi |

---

## 9. Definisi Selesai (Kriteria Penilaian)

Proyek dianggap selesai jika **semua** poin berikut terpenuhi:

1. `python main.py train <file.csv>` berjalan dari awal sampai akhir pada **3 dataset**, termasuk 1 dataset yang dipilih instruktur saat demo.
2. Hasil tiap dataset **berbeda dan sesuai datanya**: problem statement, kolom yang dibersihkan, model terpilih, dan insight.
3. `notebook.ipynb` hasil generate **bisa dijalankan ulang** tanpa error, dan metriknya sama dengan laporan.
4. `llm_log.jsonl` membuktikan setiap agen benar-benar memanggil LLM.
5. Jika LLM dimatikan, program berhenti dengan **pesan error yang jelas**.
6. Tidak ada angka di laporan/narasi yang tidak berasal dari hasil komputasi.
7. Ada test (`pytest`):
   - minimal 1 test per fungsi di `core/tools/`,
   - 1 test alur penuh dengan LLM palsu (mock),
   - 1 test bahwa leakage yang ditanam terdeteksi.
8. Mode prediksi berjalan:
   - instruktur mengetik data baru dan mendapat label/nilai prediksi beserta probabilitas atau rentang error,
   - prediksi untuk baris yang diambil dari test set sama dengan hasil di notebook,
   - input dengan kolom hilang atau tipe salah ditolak dengan pesan yang jelas.
9. Murid bisa menjelaskan setiap file dan setiap keputusan agen dengan kata-katanya sendiri.

---

## 10. Catatan tentang Proyek SHADOW Sebelumnya

- Mulai **repo baru yang kecil**. Jangan menambal SHADOW.
- Bagian yang boleh dijadikan **referensi** (dibaca, ditulis ulang dengan versi sederhana):
  - `shadow_core/pipeline.py`: pipeline sklearn fit-in-fold,
  - `shadow_core/leakage/l1_target.py` dan `l8_index.py`: ide deteksi leakage,
  - `shadow_core/modeling.py`: baseline + kandidat pada fold yang sama.
- Pelajaran dari SHADOW:
  - arena dan dialog agen yang ditulis manual **tidak dihitung** sebagai multi-agent,
  - klaim di README harus sesuai dengan kode.
