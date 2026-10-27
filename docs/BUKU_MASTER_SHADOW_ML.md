# BUKU MASTER SHADOW-ML: ENSIKLOPEDIA SUPER LENGKAP
## Edisi Definitif: Buku Pegangan Tunggal, Naskah 34 Slide, Landasan Matematika, Bedah Kode Baris Demi Baris, Glosarium 110+ Istilah, dan Simulasi 40 Pertanyaan Sidang

> **Klasifikasi Berkas**: Satu-Satunya Sumber Kebenaran Tunggal (*Single Source of Truth / SSOT*), Buku Pegangan Presenter, dan Panduan Sidang Dewan Penguji.
> **Nama Sistem**: SHADOW (*Scientific Holistic Auditable Data Orchestration Workflow*).
> **Prinsip Utama**: *"LLM Memutuskan (Merumuskan Rencana JSON), Python Mengerjakan (Menghitung Angka Pasti dengan Scikit-Learn/Pandas)"*.
> **Model Bahasa (LLM)**: `gemini-3.1-flash-lite` (Gateway Tunggal Forensik via `core/llm.py` dengan Fallback Deterministik).
> **Gaya Bahasa**: Sangat mudah dimengerti, ramah, menggunakan analogi konkret dunia nyata, tetapi tetap memiliki kedalaman akademis dan pembuktian matematika formal.
> **Total Halaman Setara**: ~80 halaman A4 (saat dicetak).

---

# DAFTAR ISI UTAMA

0. [BAGIAN 0: KATA PENGANTAR DAN CARA MEMBACA BUKU INI](#bagian-0-kata-pengantar-dan-cara-membaca-buku-ini)
   - [0.1 Untuk Siapa Buku Ini?](#01-untuk-siapa-buku-ini)
   - [0.2 Peta Navigasi: Cara Membaca Sesuai Kebutuhan](#02-peta-navigasi-cara-membaca-sesuai-kebutuhan)
   - [0.3 Konvensi Penulisan dan Simbol](#03-konvensi-penulisan-dan-simbol)
1. [BAGIAN 1: MENGENAL SHADOW SECARA SEDERHANA (HAKIKAT DAN FILOSOFI)](#bagian-1-mengenal-shadow-secara-sederhana-hakikat-dan-filosofi)
   - [1.1 Analogi Sederhana: Apa Itu SHADOW?](#11-analogi-sederhana-apa-itu-shadow)
   - [1.2 Mengapa Dunia Butuh SHADOW? (5 Krisis AI Saat Ini)](#12-mengapa-dunia-butuh-shadow-5-krisis-ai-saat-ini)
   - [1.3 Doktrin Emas: LLM Memutuskan, Python Mengerjakan](#13-doktrin-emas-llm-memutuskan-python-mengerjakan)
   - [1.4 Tiga Prinsip Filosofi Sains: Hume, Popper, dan Pisau Bedah Occam](#14-tiga-prinsip-filosofi-sains-hume-popper-dan-pisau-bedah-occam)
   - [1.5 Kartu Identitas Proyek (Ringkasan Satu Halaman)](#15-kartu-identitas-proyek-ringkasan-satu-halaman)
2. [BAGIAN 2: TIM 5 AGEN AHLI DAN CARA MEREKA BEKERJA](#bagian-2-tim-5-agen-ahli-dan-cara-mereka-bekerja)
   - [2.1 Pola Kolaborasi Papan Tulis (Blackboard Pattern)](#21-pola-kolaborasi-papan-tulis-blackboard-pattern)
   - [2.2 Agen 1: Problem Framer](#22-agen-1-problem-framer)
   - [2.3 Agen 2: Data Wrangler](#23-agen-2-data-wrangler)
   - [2.4 Agen 3: Model Guardian](#24-agen-3-model-guardian)
   - [2.5 Agen 4: Insight Storyteller](#25-agen-4-insight-storyteller)
   - [2.6 Agen 5: Notebook Builder](#26-agen-5-notebook-builder)
   - [2.7 Tabel Ringkasan 5 Agen (Cheatsheet Cepat)](#27-tabel-ringkasan-5-agen-cheatsheet-cepat)
3. [BAGIAN 3: BENTENG HIGIENITAS DATA DAN PROTOKOL ANTI-LEAKAGE](#bagian-3-benteng-higienitas-data-dan-protokol-anti-leakage)
   - [3.1 Apa Itu Target Leakage?](#31-apa-itu-target-leakage)
   - [3.2 Algoritma Scan Otomatis Korelasi dan Rasio Kolom ID](#32-algoritma-scan-otomatis-korelasi-dan-rasio-kolom-id)
   - [3.3 Protokol Brankas Data Uji (Sealed Holdout 80/20)](#33-protokol-brankas-data-uji-sealed-holdout-8020)
   - [3.4 Aturan Emas Fit-in-Fold](#34-aturan-emas-fit-in-fold)
   - [3.5 Uji Kanari Permutasi](#35-uji-kanari-permutasi)
4. [BAGIAN 4: MATEMATIKA SPEKTRAL DAN ALJABAR LINIER YANG MUDAH DIPAHAMI](#bagian-4-matematika-spektral-dan-aljabar-linier-yang-mudah-dipahami)
   - [4.1 Analogi Meja Bergoyang: Matriks Gram](#41-analogi-meja-bergoyang-matriks-gram)
   - [4.2 Nilai Eigen dan Angka Kondisi](#42-nilai-eigen-dan-angka-kondisi)
   - [4.3 Penalti Ridge L2: Ganjal Kayu Penyelamat](#43-penalti-ridge-l2-ganjal-kayu-penyelamat)
   - [4.4 Uji Brier Score Murphy (1973)](#44-uji-brier-score-murphy-1973)
   - [4.5 ROC-AUC pada Data Timpang dan Uji Nadeau-Bengio](#45-roc-auc-pada-data-timpang-dan-uji-nadeau-bengio)
   - [4.6 Ringkasan Rumus Matematika (Formula Sheet)](#46-ringkasan-rumus-matematika-formula-sheet)
5. [BAGIAN 5: PANDUAN LENGKAP DAN NASKAH KATA-DEMI-KATA 34 SLIDE](#bagian-5-panduan-lengkap-dan-naskah-kata-demi-kata-34-slide)
6. [BAGIAN 6: BUKTI EMPIRIS RIIL DARI 3 DATASET BENCHMARK](#bagian-6-bukti-empiris-riil-dari-3-dataset-benchmark)
   - [6.1 Benchmark 1: Titanic (Klasifikasi Biner)](#61-benchmark-1-titanic-klasifikasi-biner)
   - [6.2 Benchmark 2: Medical Insurance (Regresi Kontinu)](#62-benchmark-2-medical-insurance-regresi-kontinu)
   - [6.3 Benchmark 3: Telco Customer Churn (Data Timpang)](#63-benchmark-3-telco-customer-churn-data-timpang)
   - [6.4 Tabel Rekapitulasi Komparatif](#64-tabel-rekapitulasi-komparatif)
7. [BAGIAN 7: BEDAH KODE REKAYASA SISTEM DAN ANATOMI BERKAS](#bagian-7-bedah-kode-rekayasa-sistem-dan-anatomi-berkas)
   - [7.1 Peta Repositori Lengkap](#71-peta-repositori-lengkap)
   - [7.2 Bedah Berkas Pengendali](#72-bedah-berkas-pengendali)
   - [7.3 Bedah Berkas Alat Deterministik](#73-bedah-berkas-alat-deterministik)
   - [7.4 Bedah Berkas Produksi dan Antarmuka](#74-bedah-berkas-produksi-dan-antarmuka)
8. [BAGIAN 8: AUDIT 9 KRITERIA KELAYAKAN SISTEM DAN HASIL PYTEST](#bagian-8-audit-9-kriteria-kelayakan-sistem-dan-hasil-pytest)
   - [8.1 Matriks Pembuktian 9 Kriteria Kelayakan](#81-matriks-pembuktian-9-kriteria-kelayakan)
   - [8.2 Laporan Hasil Pengujian Otomatis Pytest (24/24 Lulus 100 Persen)](#82-laporan-hasil-pengujian-otomatis-pytest)
9. [BAGIAN 9: DEFENSE WAR ROOM 40 PERTANYAAN KRITIS DAN JAWABAN TELAK](#bagian-9-defense-war-room-40-pertanyaan-kritis-dan-jawaban-telak)
10. [BAGIAN 10: CHEATSHEET EKSEKUSI TERMINAL](#bagian-10-cheatsheet-eksekusi-terminal)
11. [BAGIAN 11: GLOSARIUM LENGKAP 110 ISTILAH](#bagian-11-glosarium-lengkap-110-istilah)
12. [BAGIAN 12: PANDUAN INSTALASI DAN SETUP DARI NOL](#bagian-12-panduan-instalasi-dan-setup-dari-nol)
13. [BAGIAN 13: BEDAH KODE BARIS DEMI BARIS (DEEP DIVE)](#bagian-13-bedah-kode-baris-demi-baris-deep-dive)
14. [BAGIAN 14: ALUR DATA END-TO-END (STEP-BY-STEP TRACE)](#bagian-14-alur-data-end-to-end-step-by-step-trace)
15. [BAGIAN 15: PERBANDINGAN SHADOW VS SISTEM LAIN](#bagian-15-perbandingan-shadow-vs-sistem-lain)
16. [BAGIAN 16: PANDUAN PRESENTER PROFESIONAL](#bagian-16-panduan-presenter-profesional)

---

# BAGIAN 0: KATA PENGANTAR DAN CARA MEMBACA BUKU INI

## 0.1 Untuk Siapa Buku Ini?

Buku ini ditulis untuk **tiga jenis pembaca** sekaligus:

1. **Presenter / Mahasiswa yang Akan Sidang**: Anda akan menemukan naskah lisan kata-demi-kata untuk 34 slide, jawaban untuk 40 pertanyaan kritis penguji, dan panduan bahasa tubuh saat presentasi. Baca Bagian 5, 9, 10, dan 16.

2. **Pengembang / Programmer yang Ingin Memahami Kode**: Anda akan menemukan bedah kode baris demi baris, arsitektur modul, dan alur data end-to-end. Baca Bagian 7, 12, 13, dan 14.

3. **Akademisi / Dosen yang Ingin Menilai**: Anda akan menemukan landasan matematika, pembuktian spektral, dan audit 9 kriteria kelayakan. Baca Bagian 3, 4, 6, dan 8.

---

## 0.2 Peta Navigasi: Cara Membaca Sesuai Kebutuhan

```
  +--------------------------------------------------------------+
  |                    PETA NAVIGASI BUKU                        |
  +--------------------------------------------------------------+
  |                                                              |
  |   "Saya mau presentasi besok!"                               |
  |    --> Bagian 0 -> Bagian 1 -> Bagian 5 -> Bagian 10 ->      |
  |        Bagian 16 -> Bagian 9                                 |
  |                                                              |
  |   "Saya mau paham konsepnya dari nol"                        |
  |    --> Bagian 0 -> Bagian 1 -> Bagian 2 -> Bagian 3 ->       |
  |        Bagian 4 -> Bagian 6 -> Bagian 11                     |
  |                                                              |
  |   "Saya mau ngoding / setup / modifikasi"                    |
  |    --> Bagian 12 -> Bagian 7 -> Bagian 13 -> Bagian 14       |
  |                                                              |
  |   "Saya dosen penguji / reviewer"                            |
  |    --> Bagian 1 -> Bagian 3 -> Bagian 4 -> Bagian 6 ->       |
  |        Bagian 8 -> Bagian 15                                 |
  |                                                              |
  |   "Saya mau baca semua dari A sampai Z"                      |
  |    --> Baca urut dari Bagian 0 sampai Bagian 16              |
  |                                                              |
  +--------------------------------------------------------------+
```

---

## 0.3 Konvensi Penulisan dan Simbol

| Simbol / Format | Arti |
| :--- | :--- |
| **Teks Tebal** | Istilah penting atau konsep kunci |
| *Teks Miring* | Istilah asing / bahasa Inggris |
| `kode_seperti_ini` | Nama file, variabel, fungsi, atau perintah terminal |
| > Blok kutipan | Naskah lisan yang harus diucapkan saat presentasi |
| Tanda [KUNCI] | Konsep fundamental yang sangat penting untuk dipahami |
| Tanda [JEBAKAN] | Pertanyaan berbahaya dari penguji yang perlu diwaspadai |
| Tanda [ANALOGI] | Penjelasan menggunakan perumpamaan kehidupan nyata |

**Catatan Bahasa**: Buku ini ditulis dalam Bahasa Indonesia dengan istilah teknis Bahasa Inggris yang dipertahankan karena merupakan standar industri global. Setiap istilah asing dijelaskan dalam Glosarium (Bagian 11).

---

# BAGIAN 1: MENGENAL SHADOW SECARA SEDERHANA (HAKIKAT DAN FILOSOFI)

## 1.1 Analogi Sederhana: Apa Itu SHADOW?

[ANALOGI] Bayangkan Anda memimpin sebuah **laboratorium sains data kelas dunia**. Di laboratorium tersebut, Anda memiliki:
1. **Seorang Konsultan Ahli (LLM / Model Bahasa)**: Memiliki wawasan luas tentang bisnis, mengerti arti kolom dalam bahasa manusia (misalnya tahu bahwa kolom `Age` artinya umur, dan `Charges` artinya tagihan biaya), serta pandai menulis laporan untuk direksi.
2. **Sekelompok Ilmuwan Hitung yang Super Teliti (Python Scikit-Learn, Pandas, NumPy)**: Tidak pernah tidur, tidak bisa disuap, dan menghitung setiap rumus matematika dengan kalkulator presisi tinggi tanpa pernah meleset satu desimal pun.

Jika Anda menyuruh konsultan ahli untuk menghitung akar kuadrat atau membalik matriks matematika 100x100 secara manual di kepalanya, dia kemungkinan besar akan **mengarang angka** (halusinasi) karena otaknya dirancang untuk merangkai kata, bukan kalkulator. Sebaliknya, jika Anda hanya menyuruh ilmuwan hitung bekerja sendiri tanpa arahan, mereka tidak mengerti apa tujuan bisnis dari data tersebut.

**SHADOW adalah sistem orkestrasi yang menggabungkan keduanya secara harmonis!**

* **Nama Resmi**: *Scientific Holistic Auditable Data Orchestration Workflow*.
  - *Scientific*: Berdasarkan metode ilmiah yang ketat.
  - *Holistic*: Menangani seluruh proses dari awal sampai akhir.
  - *Auditable*: Setiap langkah bisa diperiksa ulang dan dibuktikan.
  - *Data Orchestration*: Mengatur aliran data secara terkoordinasi.
  - *Workflow*: Alur kerja yang terstruktur dan berulang.
* **Tugas Utama**: Mengambil file data CSV apa pun yang Anda berikan, menganalisisnya secara otomatis, membuang data yang curang atau bocor, menguji berbagai model matematika secara adil, memilih model terbaik yang paling jujur, membuatkan grafik publikasi yang tajam, menuliskan laporan bisnis, dan membungkus seluruh pekerjaannya ke dalam sebuah buku catatan kode (*Jupyter Notebook*) yang siap Anda jalankan ulang kapan saja.
* **Sifat Sistem**: Mandiri (otonom), berjalan 100% di komputer/laptop lokal tanpa perlu mengunggah data rahasia ke internet, dan dapat diaudit setiap langkahnya.

### [ANALOGI] Restoran Bintang Lima

Bayangkan SHADOW seperti **restoran bintang lima** yang terstruktur rapi:

| Peran di Restoran | Peran di SHADOW | Penjelasan |
| :--- | :--- | :--- |
| **Kepala Koki (Chef de Cuisine)** | **LLM (Gemini Flash Lite)** | Merancang menu dan menentukan resep, tapi TIDAK memasak sendiri |
| **Juru Masak Eksekutif** | **Python Scikit-Learn** | Memasak sesuai resep, mengukur bumbu tepat per gram |
| **Buku Resep** | **state.json** | Catatan resmi seluruh keputusan dan hasil |
| **Pengawas Kebersihan Dapur** | **Modul Anti-Leakage** | Memastikan bahan tidak terkontaminasi |
| **Pelayan yang Menyajikan** | **Notebook Builder** | Menyajikan hasil akhir dalam piring cantik |
| **Penguji Rasa Independen** | **Pytest dan Nbclient** | Memastikan masakan sesuai standar |

---

## 1.2 Mengapa Dunia Butuh SHADOW? (5 Krisis AI Saat Ini)

Saat ini, banyak perusahaan dan pengembang tergoda menggunakan platform AutoML instan atau pembungkus (*wrapper*) chatbot AI biasa. Namun di dunia nyata, sistem-sistem tersebut sering mengalami **5 kegagalan fatal**:

### Krisis 1: Target Leakage (Kebocoran Kunci Jawaban)

*Contoh Kasus*: Pada data pelanggan yang ingin berhenti berlangganan (*churn*), terdapat kolom `Alasan_Berhenti`. Model AI yang bodoh akan menggunakan kolom ini untuk memprediksi apakah pelanggan akan berhenti. Hasilnya di laboratorium? Akurasi 99.9%! Tetapi saat dipakai di kantor operasional esok harinya, sistem gagal total karena calon pelanggan yang belum berhenti tentu belum memiliki catatan alasan berhenti!

*Mengapa ini berbahaya?*: Karena di dunia nyata, Anda akan membuat keputusan bisnis senilai miliaran rupiah berdasarkan model yang pada dasarnya curang. [ANALOGI] Bayangkan seperti siswa yang mendapat nilai 100 di ujian karena membawa contekan, lalu dikirim ke kompetisi olimpiade matematika internasional -- hasilnya akan memalukan!

*Solusi SHADOW*: Memiliki radar penapis kebocoran yang otomatis mendeteksi dan menghapus kolom yang berbau masa depan sebelum model sempat melihatnya.

### Krisis 2: Halusinasi Angka Metrik (Angka Gaib)

Banyak chatbot AI menulis laporan: *"Akurasi model adalah 94.5% dan F1-Score 0.91"*, padahal kode di latar belakang tidak pernah dijalankan! AI hanya merangkai angka yang terdengar meyakinkan.

*Mengapa ini berbahaya?*: [ANALOGI] Seperti dokter yang menuliskan hasil lab tanpa benar-benar memeriksa darah pasien. Keputusan medis yang diambil berdasarkan angka palsu bisa membunuh!

*Solusi SHADOW*: Angka akurasi, p-value, dan koefisien dihitung langsung oleh Python Scikit-Learn dan dikunci di brankas digital `state.json`. AI hanya diperbolehkan membaca angka tersebut, dilarang keras mengubahnya walau satu digit.

### Krisis 3: Notebook Hasil Ekspor yang Rusak (*Broken Reproducibility*)

Banyak sistem mengklaim bisa membuat Jupyter Notebook. Namun saat dibuka oleh dosen penguji atau rekan kerja, notebook tersebut melempar pesan error merah panjang (`ModuleNotFoundError`, `NameError`, atau urutan kode terbalik).

*Mengapa ini berbahaya?*: Reproduktibilitas adalah jantung dari sains! Jika eksperimen tidak bisa diulang, hasilnya tidak bisa dipercaya. [ANALOGI] Ini seperti resep kue yang tidak bisa dimasak ulang -- mungkin kuenya enak karena kebetulan, bukan karena resepnya benar.

*Solusi SHADOW*: Agen ke-5 SHADOW menguji ulang notebook tersebut secara otomatis di latar belakang (*headless execution*) menggunakan mesin `nbclient`. Jika ada satu sel saja yang error, sistem menolak memberi label selesai.

### Krisis 4: Debat Melingkar Tanpa Ujung (*Critique Loops dan Token Waste*)

Banyak kerangka kerja multi-agen (seperti AutoGen atau CrewAI) membiarkan agen berdebat: Agen A menulis kode, Agen B mengkritik, Agen A merevisi, Agen B mengkritik lagi. Akibatnya? Token API habis, kuota jebol, memori laptop penuh, dan proses tidak pernah selesai.

*Mengapa ini berbahaya?*: [ANALOGI] Bayangkan rapat kantor yang berlangsung 8 jam tanpa keputusan. Semua orang bicara, tidak ada yang bekerja. Biaya token API yang terbuang bisa ratusan ribu rupiah per percobaan!

*Solusi SHADOW*: Menggunakan jalur sekuensial linier berbasis papan tulis (*Blackboard Pattern*). Lima agen bekerja bergantian seperti estafet lari; tidak ada debat tak berujung.

### Krisis 5: Keputusan Kotak Hitam (*Black-Box Mystery*)

Banyak AutoML langsung memilih model Deep Learning rumit dengan jutaan parameter. Tidak ada yang tahu mengapa model memprediksi demikian.

*Mengapa ini berbahaya?*: Di bidang keuangan, kesehatan, atau hukum, Anda wajib menjelaskan **mengapa** keputusan diambil. "Karena AI bilang begitu" bukan jawaban yang bisa diterima di pengadilan!

*Solusi SHADOW*: Mengutamakan prinsip *Occam's Razor*. Jika model linier yang sederhana dan mudah dijelaskan sudah memberikan akurasi yang baik dan stabil, model linier itulah yang dipilih sebagai juara (*Champion*).

---

## 1.3 Doktrin Emas: LLM Memutuskan, Python Mengerjakan

[KUNCI] Ini adalah aturan nomor satu dalam seluruh arsitektur SHADOW.

```
+--------------------------------------------------------+
|             Large Language Model (AI Otak)              |
|                 (gemini-3.1-flash-lite)                 |
|                                                        |
|  BOLEH:                                                |
|  - Membaca ringkasan profil data                       |
|  - Merumuskan tujuan bisnis dan target                 |
|  - Mengambil keputusan strategi dalam bentuk JSON rapi |
|  - Menulis narasi laporan berdasarkan angka Python     |
|                                                        |
|  DILARANG KERAS:                                       |
|  - Menghitung rata-rata, median, atau korelasi         |
|  - Menulis angka akurasi, F1-Score, atau p-value       |
|  - Melatih model machine learning                      |
|  - Mengubah angka yang sudah dihitung Python           |
+----------------------------+---------------------------+
                             | Mengirim Rencana Strategis (JSON)
                             v
+--------------------------------------------------------+
|           Python Deterministic Core (Tangan Kerja)     |
|                (Scikit-Learn, Pandas, NumPy)            |
|                                                        |
|  BOLEH:                                                |
|  - Membagi data 80% Latih dan 20% Uji                 |
|  - Membersihkan nilai kosong dan menapis kebocoran     |
|  - Melatih model matematika secara adil (5-Fold CV)    |
|  - Menghitung akurasi, kurva ROC-AUC, dan Brier score  |
|  - Menguji notebook secara mandiri tanpa campur tangan |
|                                                        |
|  DILARANG KERAS:                                       |
|  - Memutuskan strategi bisnis tanpa arahan LLM         |
|  - Menulis narasi bahasa manusia                       |
+--------------------------------------------------------+
```

### Mengapa Pemisahan Ini Sangat Penting?

[ANALOGI] Bayangkan sebuah rumah sakit:
- **Dokter konsultan** menentukan diagnosis dan rencana perawatan (peran LLM)
- **Peralatan laboratorium** mengukur kadar gula darah, tekanan darah, dan kolesterol (peran Python)
- **Tidak pernah** dokter disuruh menghitung kadar gula darah secara manual di kepalanya!
- **Tidak pernah** mesin lab yang menentukan diagnosis pasien!

Hasilnya: Sistem yang cerdas memahami konteks manusiawi, tetapi memiliki kepatuhan matematis 100% yang tidak bisa disangkal.

### Bukti Nyata Pemisahan di Kode

Perhatikan arsitektur folder proyek:

| Folder | Isi | Memanggil LLM? |
| :--- | :--- | :--- |
| `core/tools/*.py` | Profiling, cleaning, modeling, plotting, predict | **TIDAK!** Murni Python |
| `agents/*.py` | Framing, data, modeling, insight, notebook agent | **YA**, tapi hanya untuk membuat rencana JSON |
| `core/llm.py` | Gateway Gemini + log forensik | YA, ini jembatan ke LLM |
| `core/state.py` | Papan tulis bersama | TIDAK, hanya menyimpan data |

Tidak ada satu pun baris `import llm` di dalam folder `core/tools/`. Ini menjamin angka dari Python tidak bisa terkontaminasi halusinasi.

---

## 1.4 Tiga Prinsip Filosofi Sains: Hume, Popper, dan Pisau Bedah Occam

SHADOW tidak hanya dibangun dari kode pemrograman, melainkan berdiri tegak di atas tiga pilar filsafat sains modern:

### Pilar 1: Masalah Induksi David Hume (Jangan Terlalu Percaya Diri dengan Masa Lalu)

Filosof David Hume (1711-1776) mengingatkan kita: Hanya karena kita melihat 1.000 angsa berwarna putih di masa lalu, bukan berarti semua angsa di dunia pasti berwarna putih. (Ternyata ada angsa hitam di Australia!)

Dalam Machine Learning, data latih adalah masa lalu. Jika kita melatih model dan langsung memujinya hebat hanya karena nilainya bagus di data latih, kita sedang melakukan kesalahan fatal (*Overfitting*).

*Penerapan SHADOW*: Kami mengunci 20% data ke dalam **Brankas Tertutup (*Sealed Holdout*)**. Data ini disembunyikan sejak detik pertama dan tidak boleh disentuh selama pelatihan. Model baru diuji pada brankas ini di akhir untuk melihat kemampuannya menghadapi masa depan yang sesungguhnya.

[ANALOGI] Bayangkan seorang petinju yang hanya sparring dengan saudara kembarnya (data latih). Dia merasa hebat karena selalu menang. Tapi saat dimasukkan ke ring melawan lawan asing (data uji), dia baru tahu kemampuan aslinya.

### Pilar 2: Falsifikasi Karl Popper (Uji Lawan Terlemah Terlebih Dahulu)

Filosof Karl Popper (1902-1994) menyatakan bahwa sebuah teori ilmiah tidak bisa dianggap hebat sebelum diuji kemampuannya untuk disangkal (*falsifiable*). Teori yang tidak bisa dibantah bukanlah sains -- itu adalah dogma!

*Penerapan SHADOW*: Sebelum mengadu model-model canggih, SHADOW selalu melatih **Dummy Baseline** (model tebakan acak / tebakan mayoritas paling bodoh). Jika sebuah model canggih tidak mampu mengalahkan tebakan bodoh ini secara signifikan, model canggih tersebut dinyatakan gagal secara ilmiah.

[ANALOGI] Bayangkan seorang pengusaha yang mengklaim obat baru ajaibnya bisa menyembuhkan flu. Sebelum dipuji, kita harus membandingkan: Apakah obatnya lebih baik daripada hanya minum air putih dan istirahat (baseline)? Jika tidak lebih baik, obat tersebut tidak berguna!

### Pilar 3: Pisau Bedah Occam / Occam's Razor (Sederhana Itu Mulia)

Prinsip kuno *Lex Parsimoniae* oleh William of Ockham (1287-1347): *"Jangan menambah kerumitan jika hal yang sederhana sudah cukup."*

*Penerapan SHADOW*: Jika Model A (Regresi Linier) menghasilkan akurasi 80.0% dengan penjelasan pengaruh fitur yang sangat terang benderang, sedangkan Model B (Random Forest 500 pohon) menghasilkan akurasi 80.5% namun rumit dan berat di memori, maka SHADOW memilih **Model A** sebagai juaranya. Kompleksitas hanya boleh diambil jika peningkatannya terbukti nyata secara statistik (diuji dengan Nadeau-Bengio Corrected t-Test).

[ANALOGI] Jika Anda bisa pergi ke kantor dengan sepeda motor (cepat, murah, mudah parkir) dan kereta cepat (mahal, perlu booking, tapi hanya 2 menit lebih cepat), pilihlah sepeda motor! Kecuali jarak temputnya jauh sekali sehingga kereta benar-benar unggul signifikan.

---

## 1.5 Kartu Identitas Proyek (Ringkasan Satu Halaman)

| Atribut | Detail |
| :--- | :--- |
| **Nama Lengkap** | SHADOW: Scientific Holistic Auditable Data Orchestration Workflow |
| **Versi** | 1.0 (Edisi Sidang Akhir) |
| **Bahasa Pemrograman** | Python 3.11+ |
| **Model AI** | Google Gemini 3.1 Flash Lite (dengan fallback ke 3.5 dan 3.8) |
| **Pustaka ML Inti** | Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn |
| **Pustaka Pendukung** | nbformat, nbclient, joblib |
| **Pola Arsitektur** | Blackboard Pattern (Papan Tulis Bersama) |
| **Jumlah Agen** | 5 Agen Sekuensial |
| **Format Input** | File CSV tabular (hingga ~50.000 baris, ~50 kolom) |
| **Jenis Tugas ML** | Klasifikasi Biner, Klasifikasi Multikelas, Regresi Kontinu |
| **Format Output** | state.json, report.md, notebook.ipynb, model.joblib, schema.json, figures/*.png |
| **Antarmuka** | CLI (main.py) + Streamlit Arena (app.py) + Slide Web (slides.html) |
| **Kebutuhan RAM** | Minimal 8 GB (dioptimalkan satu model aktif sekaligus) |
| **Kebutuhan Jaringan** | Hanya untuk memanggil API Gemini; komputasi ML 100% lokal |
| **Total Tes Otomatis** | 24 tes (6 pipeline + 18 backend), 100% lulus |
| **Dataset Benchmark** | Titanic (700 baris), Insurance (1.338 baris), Telco Churn (600 baris) |

---

# BAGIAN 2: TIM 5 AGEN AHLI DAN CARA MEREKA BEKERJA

## 2.1 Pola Kolaborasi Papan Tulis (Blackboard Pattern)

[ANALOGI] Bayangkan sebuah ruang operasi di rumah sakit terbaik. Di dinding ruang operasi tersebut terdapat sebuah **Papan Tulis Besar (Blackboard)**.
Di papan tulis itulah semua data pasien ditulis: tekanan darah, hasil rontgen, golongan darah, hingga riwayat alergi.

Lima dokter spesialis masuk bergantian secara teratur:
* Dokter ke-1 datang, membaca papan tulis, menuliskan rencana tindakan, lalu keluar.
* Dokter ke-2 datang, melihat catatan dokter ke-1, membersihkan peralatan bedah yang kotor, menuliskan kondisi steril di papan tulis, lalu keluar.
* Dokter ke-3 datang, melakukan operasi, mengukur tanda vital, mencatat hasil operasi di papan tulis, lalu keluar.
* Dokter ke-4 datang, membaca hasil operasi, menuliskan resume medis untuk keluarga pasien, lalu keluar.
* Dokter ke-5 datang, menyusun seluruh berkas rekam medis menjadi buku laporan resmi yang rapi dan terverifikasi.

**Tidak ada dokter yang berteriak-teriak mendebat dokter lain tanpa henti!**
Dalam SHADOW, papan tulis digital ini bernama `state.json` (atau objek kelas `SharedState`). Kelima agen bekerja secara berurutan dan disiplin.

```
[ CSV Mentah ]
      |
      v
+--------------+      +--------------+      +--------------+      +--------------+      +--------------+
|   Tahap 1    |      |   Tahap 2    |      |   Tahap 3    |      |   Tahap 4    |      |   Tahap 5    |
|Problem Framer| -->  | Data Wrangler| -->  |Model Guardian| -->  | Storyteller  | -->  |Notebook Build|
+--------------+      +--------------+      +--------------+      +--------------+      +--------------+
      |                      |                     |                     |                     |
      +----------------------+---------------+-----+---------------------+---------------------+
                                             v
                             +-------------------------------+
                             |       PAPAN TULIS UTAMA       |
                             |         (state.json)          |
                             |  - Profil data mentah         |
                             |  - Kolom target terpilih      |
                             |  - Fitur bocor yang dibuang   |
                             |  - Metrik evaluasi Scikit-Learn|
                             |  - Bobot koefisien resmi      |
                             |  - Transkrip debat agen       |
                             +-------------------------------+
```

### Mengapa Blackboard, Bukan Debat?

| Aspek | Blackboard (SHADOW) | Critique Loop (AutoGen/CrewAI) |
| :--- | :--- | :--- |
| **Alur** | Sekuensial, satu arah, pasti selesai | Melingkar, bisa tak berujung |
| **Token API** | Hemat (5 pemanggilan LLM) | Boros (puluhan pemanggilan) |
| **Waktu** | ~20-30 detik total | Bisa 5-15 menit |
| **Memori** | Ringan (satu model aktif) | Berat (multiple agen di memori) |
| **Determinisme** | Input sama = output sama | Bisa berbeda tiap kali jalan |

---

## 2.2 Agen 1: Problem Framer

* **Ibarat Peran**: Direktur Perencanaan Proyek.
* **File Kode**: `agents/framing_agent.py`
* **Tugas Utama**: Membaca susunan awal file CSV yang diunggah pengguna. Menjawab pertanyaan mendasar: *"Masalah apa yang sebenarnya ingin kita selesaikan dengan data ini?"*
* **Cara Kerja (Langkah demi Langkah)**:
  1. Menerima ringkasan profil data dari Python (jumlah baris, kolom, tipe data, missing values).
  2. Menganalisis sebaran nilai pada setiap kolom menggunakan statistik deskriptif.
  3. Memeriksa daftar kolom kandidat target (kolom biner, kolom numerik kontinu, dll).
  4. Memilih kolom target yang paling masuk akal (misalnya kolom `Survived` pada data Titanic).
  5. Menentukan jenis tugas pembelajaran mesin:
     - **Klasifikasi Biner**: Jika target bernilai 2 kategori (Selamat vs Tidak Selamat)
     - **Klasifikasi Multikelas**: Jika target bernilai 3+ kategori (Rendah, Sedang, Tinggi)
     - **Regresi Kontinu**: Jika target bernilai angka desimal kontinu (nominal uang, suhu)
  6. Memilih metrik penilaian yang paling adil:
     - `ROC-AUC` untuk data seimbang
     - `F1-Score` untuk data timpang
     - `R2` / `MAE` untuk regresi
* **Keluaran**: Rencana strategis dalam format JSON yang ditulis ke papan tulis `state.json`.
* **Contoh Output JSON**:
  ```json
  {
    "problem_statement": "Memprediksi apakah penumpang kapal selamat atau tidak",
    "target_column": "Survived",
    "task_type": "binary_classification",
    "primary_metric": "roc_auc",
    "reasoning": "Target biner dengan distribusi cukup seimbang"
  }
  ```
* **Validasi Python**: Setelah LLM mengembalikan JSON, Python MEMVALIDASI bahwa `target_column` benar-benar ada di kolom dataset! Jika tidak ada, sistem melempar error.

---

## 2.3 Agen 2: Data Wrangler

* **Ibarat Peran**: Inspektur Kebersihan dan Petugas Forensik Data.
* **File Kode**: `agents/data_agent.py` + `core/tools/cleaning.py` + `core/tools/profiling.py`
* **Tugas Utama**: Menjamin data yang masuk ke mesin pemodelan 100% higienis, bersih dari kotoran, dan bebas dari unsur kecurangan.
* **Cara Kerja (Langkah demi Langkah)**:
  1. **Audit Nilai Kosong (Missing Values)**: Memetakan kolom mana yang bolong dan merencanakan teknik penambalannya:
     - Kolom numerik: diisi dengan angka **median** (tengah) karena tahan terhadap outlier
     - Kolom kategorikal: diisi dengan kategori **modus** (yang paling sering muncul)
  2. **Pemusnahan Kolom Identitas Palsu**: Menghitung rasio keunikan kolom. Jika ada kolom yang unik di atas 95% (seperti `PassengerId` atau `customerID`), kolom langsung dibuang karena hanya akan membuat model menghafal nomor acak.
  3. **Penyisiran Kebocoran Target (Anti-Leakage Scan)**: Menghitung korelasi Pearson terhadap target. Jika ada fitur dengan |r| >= 0.85, fitur langsung disita dan dibuang.
  4. **Konversi Kolom Tersembunyi**: Kolom yang tampak sebagai teks tapi sebenarnya numerik (seperti `TotalCharges` yang berisi string angka) dideteksi dan dikonversi secara otomatis.
  5. **Pembuatan Pipa Transformasi**: Merakit Scikit-Learn `ColumnTransformer` yang membungkus semua resep pembersihan dalam satu wadah rapi.
* **Keluaran**: Daftar kolom bersih, pipa transformasi data Scikit-Learn (`ColumnTransformer`), dan data yang sudah dibagi menjadi 80% latih dan 20% uji.

---

## 2.4 Agen 3: Model Guardian

* **Ibarat Peran**: Wasit Pertandingan yang Adil dan Auditor Kualitas Independen.
* **File Kode**: `agents/modeling_agent.py` + `core/tools/modeling.py`
* **Tugas Utama**: Melatih berbagai model kandidat dan memilih satu model terbaik tanpa memihak.
* **Cara Kerja (Langkah demi Langkah)**:
  1. **Menyiapkan Patokan Dasar (Dummy Baseline)**: Melatih model tebakan paling bodoh:
     - Untuk klasifikasi: `DummyClassifier(strategy="most_frequent")` -- selalu menebak kelas mayoritas
     - Untuk regresi: `DummyRegressor(strategy="mean")` -- selalu menebak angka rata-rata
  2. **Melatih 3 Model Kandidat**:
     - **Model Linier**: `LogisticRegression(max_iter=1000)` atau `Ridge(alpha=1.0)` -- sederhana, stabil, bisa dijelaskan
     - **Random Forest**: `RandomForestClassifier(n_estimators=100, max_depth=10)` -- kumpulan pohon keputusan
     - **Gradient Boosting**: `GradientBoostingClassifier(n_estimators=100, max_depth=4)` -- pohon bertahap
  3. **Uji Validasi Silang 5 Lipatan (5-Fold Stratified Cross Validation)**: Membagi data latih menjadi 5 bagian yang seimbang, melatih pada 4 bagian, menguji pada 1 bagian secara bergantian. Total: 5 percobaan per model! Ini menghasilkan 5 skor per model, sehingga kita bisa menghitung rata-rata dan simpangan baku.
  4. **Mengukur Celah Overfitting (Overfit Gap)**: Menghitung |skor latih - skor validasi|. Jika nilainya di atas 0.10, model sakit (*severe overfit*) dan tidak layak menjadi champion.
  5. **Menjalankan Uji Kanari Permutasi**: Mengacak label target 100% untuk membuktikan model belajar dari sinyal, bukan noise.
  6. **Menjalankan Uji Nadeau-Bengio**: Membandingkan champion vs baseline secara statistik dengan koreksi tumpang tindih CV.
  7. **Menerapkan Pisau Bedah Occam**: Jika Logistic Regression mendapat skor 79.6% dan Random Forest mendapat 80.5% tetapi overfit gap-nya 20x lebih lebar, Logistic Regression yang dipilih!
  8. **Evaluasi Final pada Holdout**: Setelah champion terpilih, fit ulang pada SELURUH data latih (80%), lalu evaluasi pada data uji (20%) TEPAT SATU KALI.
* **Keluaran**: Satu model juara (*Champion Model*), pipeline lengkap, metrik akhir pada holdout, confusion matrix, dan daftar fitur terpenting.

---

## 2.5 Agen 4: Insight Storyteller

* **Ibarat Peran**: Juru Bicara dan Penulis Laporan Manajemen.
* **File Kode**: `agents/insight_agent.py` + `core/tools/plotting.py`
* **Tugas Utama**: Mengubah angka-angka rumit, bobot matriks, dan kurva statistik menjadi narasi bahasa manusia yang mudah dipahami direksi perusahaan.
* **Cara Kerja**:
  1. **Mengambil Fakta Nyata**: Mengambil koefisien asli dari model juara yang sudah dilatih Python. Jika model linier, mengambil `coef_`. Jika model ensemble (Random Forest), mengambil `feature_importances_`.
  2. **Membuat 4 Grafik Resolusi Tinggi (150 DPI)**:
     - **Target Distribution**: Grafik sebaran data target (berapa orang selamat vs meninggal, atau distribusi biaya).
     - **Correlation Heatmap**: Peta panas korelasi antar-fitur numerik.
     - **Confusion Matrix / Residual Plot**: Grafik tebakan benar vs salah (klasifikasi) atau kurva residu (regresi).
     - **Feature Importance**: Diagram batang 10 faktor terpenting yang mempengaruhi prediksi.
  3. **Menyusun Dokumen Laporan (`report.md`)**: Berisi ringkasan eksekutif, faktor pendorong utama bisnis, serta catatan peringatan (*caveats*) agar pengguna tidak salah menginterpretasikan hasil.
* **Keluaran**: File laporan `report.md` dan 4 gambar visual tajam di folder `figures/`.
* **Aturan Penting**: Setiap angka dalam narasi HARUS berasal dari `state.json`. LLM hanya menyusun narasi kualitatif di sekitar angka yang sudah dikunci.

---

## 2.6 Agen 5: Notebook Builder

* **Ibarat Peran**: Pabrik Perakitan Produk Akhir dan Quality Assurance.
* **File Kode**: `agents/notebook_agent.py` + `core/tools/notebook.py`
* **Tugas Utama**: Mengemas seluruh alur riset ke dalam satu file Jupyter Notebook mandiri (`notebook.ipynb`) dan memastikan file tersebut dapat dijalankan orang lain tanpa hambatan.
* **Cara Kerja**:
  1. **Menyusun 11 Sel Kode Bersih**: Menulis kode Python murni mulai dari impor pustaka, pemuatan data CSV, pembuangan fitur bocor, split 80/20, pelatihan model, hingga kalkulasi skor akhir. Setiap sel bisa berdiri sendiri secara logis.
  2. **Eksekusi Ulang Tanpa Layar (Headless Replay via `nbclient`)**: Menjalankan notebook tersebut dari sel pertama hingga sel terakhir pada kernel Python terisolasi. Timeout: 300 detik.
  3. **Verifikasi Kecocokan Nilai**: Membandingkan angka yang keluar dari eksekusi notebook dengan angka di papan tulis `state.json`. Keduanya harus cocok persis hingga toleransi 0.001. Jika tidak cocok, ada yang salah!
  4. **Penyimpanan Berkas Siap Pakai**: Menyimpan artefak model lengkap (`model.joblib`) dan kontrak data (`schema.json`) untuk keperluan produksi.
* **Keluaran**: File `notebook.ipynb` yang dijamin 100% bebas error saat dijalankan ulang oleh dewan penguji.

---

## 2.7 Tabel Ringkasan 5 Agen (Cheatsheet Cepat)

| No | Nama Agen | Ibarat | File Utama | Input | Output | Waktu |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Problem Framer | Direktur | `framing_agent.py` | Profil data | Target, task_type, metric | ~2 dtk |
| 2 | Data Wrangler | Inspektur | `data_agent.py` | Data mentah | Data bersih, ColumnTransformer | ~3 dtk |
| 3 | Model Guardian | Wasit | `modeling_agent.py` | Data bersih | Champion model, metrik | ~10 dtk |
| 4 | Insight Storyteller | Juru Bicara | `insight_agent.py` | Metrik dan model | report.md, 4 grafik PNG | ~3 dtk |
| 5 | Notebook Builder | Pabrik QA | `notebook_agent.py` | Seluruh state | notebook.ipynb tervalidasi | ~5 dtk |

**Total Waktu Pipeline**: ~20-30 detik pada laptop 8 GB RAM untuk dataset ~1.000 baris.

---

# BAGIAN 3: BENTENG HIGIENITAS DATA DAN PROTOKOL ANTI-LEAKAGE

## 3.1 Apa Itu Target Leakage?

[ANALOGI] Bayangkan Anda seorang guru yang sedang menyelenggarakan ujian akhir matematika. Saat membuat lembar soal, Anda lupa dan tidak sengaja mencetak **kunci jawaban** di pojok kanan bawah setiap lembar kertas ujian murid.

Seorang murid melihat kunci jawaban tersebut, menyalinnya ke lembar jawaban, dan mengumpulkan hasilnya dalam waktu 5 menit. Nilainya? **100 Sempurna!** Apakah murid tersebut jenius? Tentu tidak. Murid tersebut tampak pintar hanya karena ada **informasi masa depan yang bocor** ke dalam ruang ujian. Begitu murid tersebut dibawa ke dunia kerja nyata di mana kunci jawaban tidak tersedia, dia tidak bisa menyelesaikan masalah apa pun.

**Inilah yang disebut Target Leakage dalam Machine Learning!** Fitur yang berkorelasi sangat tinggi dengan label masa depan menyusup ke dalam data latih. Model machine learning yang tidak diawasi akan menghafal fitur tersebut dan menghasilkan akurasi palsu 99% yang akan runtuh seketika saat diterapkan di dunia nyata.

### 3 Jenis Target Leakage yang Paling Berbahaya

| Jenis | Contoh | Mengapa Berbahaya |
| :--- | :--- | :--- |
| **Leakage Langsung** | Kolom `Alasan_Berhenti` pada data prediksi churn | Kolom ini HANYA ADA setelah pelanggan sudah berhenti! |
| **Leakage Tidak Langsung** | Kolom `BiayaPembatalan` berkorelasi r=0.95 dengan churn | Biaya ini dihitung SETELAH pelanggan memutuskan pergi |
| **Leakage Prosedural** | Menghitung median dari SELURUH data termasuk data uji | Statistik data uji bocor ke pipeline latih |

---

## 3.2 Algoritma Scan Otomatis Korelasi dan Rasio Kolom ID

Modul pertahanan SHADOW (`core/tools/profiling.py` dan `cleaning.py`) menerapkan dua lapis sensor otomatis:

### Sensor Lapis 1: Pembasmi Kolom Identitas Palsu (Keunikan >= 95%)

```
Algoritma (Bahasa Sederhana):
  UNTUK SETIAP kolom di dataset:
    hitung rasio_keunikan = jumlah_nilai_unik / jumlah_baris_total
    JIKA rasio_keunikan >= 0.95:
      TANDAI kolom sebagai "ID / Identifier"
      BUANG dari matriks fitur
      CATAT di log audit
```

* Kolom seperti `Nomor_KTP`, `ID_Pelanggan`, atau `Nomor_Tiket` memiliki sifat unik untuk setiap individu.
* Jika kolom ini dibiarkan masuk, model akan mencoba menghubungkan: *"Jika ID = 4821, maka orang ini selamat"*. Ini adalah kesimpulan bodoh yang tidak ada gunanya untuk orang baru yang memiliki ID berbeda.
* **Tindakan SHADOW**: Sistem otomatis mendeteksi kolom yang memiliki rasio nilai unik di atas 95% dari total baris data dan langsung mendepaknya keluar dari matriks latih.

### Sensor Lapis 2: Penapis Korelasi Ekstrem (|r| >= 0.85)

```
Algoritma (Bahasa Sederhana):
  UNTUK SETIAP fitur numerik:
    hitung r = korelasi_pearson(fitur, target)
    JIKA |r| >= 0.85:
      TANDAI fitur sebagai "Proksi Target Bocor"
      BUANG dari matriks fitur
      CATAT di log audit forensik
```

Nilai korelasi berkisar antara -1.0 hingga +1.0:
- r = +1.0 artinya hubungan positif sempurna (naik bersama)
- r = -1.0 artinya hubungan negatif sempurna (satu naik, satu turun)
- r = 0.0 artinya tidak ada hubungan linier sama sekali

Jika |r| >= 0.85, artinya fitur tersebut hampir identik dengan target -- sangat mencurigakan dan kemungkinan besar adalah informasi masa depan yang bocor!

---

## 3.3 Protokol Brankas Data Uji (Sealed Holdout 80/20)

Dalam sains data yang jujur, Anda tidak boleh menguji model Anda pada data yang sudah pernah dilihatnya saat belajar.

```
Seluruh Dataset Mentah (100% Baris)
  |
  +---> 80% DATA LATIH (Training Arena)
  |     - Tempat menghitung rata-rata dan median
  |     - Tempat melatih model kandidat
  |     - Tempat validasi silang (5-Fold CV)
  |     - SATU-SATUNYA arena yang boleh dilihat model!
  |
  +---> 20% BRANKAS DATA UJI (Sealed Holdout Vault)
        - Disimpan di brankas terisolasi sejak awal!
        - Tidak boleh dilihat model saat belajar
        - Tidak boleh dipakai untuk menghitung median
        - HANYA DIBUKA 1 KALI di akhir untuk evaluasi final!
```

[ANALOGI] Bayangkan 20% data ini adalah amplop soal ujian nasional yang disegel di brankas Bank Indonesia. Amplop HANYA dibuka pada hari ujian, setelah semua siswa selesai belajar. Tidak ada yang boleh mengintip sebelumnya!

Mengapa 20% data ini harus disegel rapat? Karena inilah satu-satunya cara objektif untuk membuktikan kepada dewan penguji bahwa model kita benar-benar mampu mengenali pola umum, bukan sekadar menghafal isi lembar latihan.

---

## 3.4 Aturan Emas Fit-in-Fold

[KUNCI] **Ini adalah kesalahan paling umum yang dilakukan 80% praktisi pemula!**

Banyak praktisi sains data pemula melakukan kesalahan fatal berikut pada kode Python mereka:

```python
# CONTOH KODE SALAH (MEMICU KEBOCORAN DATA):
imputer = SimpleImputer(strategy='median')
X_semua = imputer.fit_transform(X_semua)   # <-- SALAH BESAR!
X_train, X_test = train_test_split(X_semua)
# Median sudah menyerap info dari X_test! Kebocoran terjadi!
```

Mengapa kode di atas salah besar? Karena saat Anda memanggil `.fit_transform()` pada seluruh dataset, nilai median yang dihitung sudah menyerap informasi dari baris-baris data uji `X_test`! Informasi dari masa depan sudah merembes ke masa lalu.

```python
# CONTOH KODE BENAR (CARA SHADOW):
X_train, X_test = train_test_split(X_semua)   # Pisahkan DULU!
imputer = SimpleImputer(strategy='median')
imputer.fit(X_train)                   # Hitung median HANYA dari data latih
X_train = imputer.transform(X_train)   # Terapkan ke data latih
X_test = imputer.transform(X_test)     # Data uji hanya menerima transformasi
```

**Aturan Emas SHADOW (Fit-in-Fold Strictness)**:
1. Data uji dipisahkan terlebih dahulu.
2. Parameter statistik (seperti rata-rata, median, standar deviasi, dan kamus kategori) dihitung **HANYA dari data latih** menggunakan perintah `.fit()`.
3. Data uji hanya boleh menerima transformasi pasif menggunakan perintah `.transform()`.
4. Dalam validasi silang 5 lipatan, proses ini diulang di dalam setiap lipatan (*inside each fold*) secara ketat melalui Scikit-Learn `Pipeline`.

[ANALOGI] Bayangkan Anda seorang guru yang membuat ujian. Jika Anda menghitung rata-rata nilai seluruh siswa (termasuk siswa yang belum ujian) untuk menentukan batas kelulusan, maka batas kelulusan Anda sudah "tercemar" oleh informasi masa depan.

---

## 3.5 Uji Kanari Permutasi

[ANALOGI] Di tambang batu bara zaman dulu, para penambang membawa burung kenari (*canary*) ke dalam terowongan. Jika ada gas beracun, kenari akan mati lebih dulu -- memberi peringatan dini kepada manusia.

**Uji Kanari SHADOW** bekerja serupa:
1. Ambil data latih yang sudah bersih.
2. **Acak 100% label target** menggunakan permutasi acak -- hubungan fitur-target hancur total!
3. Latih model champion pada data acak ini.
4. Ukur skornya.

**Jika model belajar dari sinyal yang benar**, skor pada data acak harus ANJLOK ke tingkat tebakan acak:
- Klasifikasi: ROC-AUC mendekati 0.50 (setara lempar koin)
- Regresi: R2 mendekati 0.0 atau negatif

**Jika skor tetap tinggi pada data acak**, itu artinya ada kebocoran prosedural yang tersembunyi!

Implementasi kode: fungsi `run_permutation_canary_test()` di `core/tools/modeling.py`.

---

# BAGIAN 4: MATEMATIKA SPEKTRAL DAN ALJABAR LINIER YANG MUDAH DIPAHAMI

## 4.1 Analogi Meja Bergoyang: Matriks Gram

[ANALOGI] Mari kita tinggalkan sejenak rumus-rumus rumit dan bayangkan sebuah **meja berkaki empat**.

* Setiap kolom fitur dalam data Anda adalah sebuah kaki penyangga meja.
* Jika semua kaki berdiri di sudut yang berbeda dan kokoh (fitur-fitur berdiri independen), meja tersebut akan sangat stabil. Anda bisa menaruh beban apa pun di atas meja tersebut tanpa takut goyang.
* Namun, apa yang terjadi jika Anda memasang dua kaki meja di tempat yang sama persis atau sangat berdekatan (artinya: dua fitur memiliki informasi yang sama persis / berkorelasi sangat tinggi)? Meja tersebut sekarang kehilangan keseimbangan. Meja akan **bergoyang luar biasa** bahkan hanya karena embusan angin kecil!

Dalam aljabar linier, meja tersebut diwakili oleh **Matriks Gram G = X^T * X** (berukuran p x p, di mana p adalah jumlah fitur). Untuk menemukan bobot atau koefisien regresi terbaik (beta), komputer harus membalikkan matriks ini melalui rumus:

```
beta = (X^T * X)^(-1) * X^T * y
```

Membalikkan matriks sama seperti membagi angka dengan penyebutnya. Jika matriks Anda sehat, pembagian berjalan mulus. Namun jika ada dua fitur yang kembar (multikolinearitas), komputer serasa disuruh **membagi dengan angka nol**! Komputer akan panik, sistem menjadi tidak stabil, dan angka koefisien yang dihasilkan akan melonjak jutaan kali lipat tanpa kendali.

---

## 4.2 Nilai Eigen dan Angka Kondisi

Bagaimana cara seorang dokter sains data mengetahui apakah matriks datanya sedang sakit parah? Jawabannya adalah dengan memeriksa **Nilai Eigen (Eigenvalues)** melalui Teorema Dekomposisi Spektral:

```
X^T * X = Q * Lambda * Q^T

Lambda = [lambda_max, lambda_2, ..., lambda_min]
         (dari besar ke kecil, semua >= 0)
```

Nilai eigen terkecil (lambda_min) mencerminkan seberapa kokoh kaki meja Anda yang paling lemah:
* Jika ada dua fitur yang saling meniru, maka **lambda_min akan mendekati angka 0**.
* Ketika matriks dibalik, komponen inversinya adalah **1 / lambda_min**.
* Coba Anda bayangkan: 1 dibagi 0.000001 hasilnya adalah **1.000.000**! Variansi bobot meledak menuju tak terhingga.

### Alat Pengukur Derajat Sakit: Angka Kondisi (Condition Number / kappa)

```
kappa = lambda_max / lambda_min
```

| kappa | Status | Analogi |
| :--- | :--- | :--- |
| Kurang dari 10 | Sehat Bugar (*Well-conditioned*) | Meja kokoh, empat kaki kuat |
| 10 sampai 30 | Sakit Ringan (Multikolinearitas Sedang) | Meja agak goyang, hati-hati |
| Di atas 30 | **Sakit Parah (*Severely Ill-conditioned*)** | Meja hampir ambruk! |
| Di atas 1.000.000 | Kritis | Komputer mengalami error floating point |

---

## 4.3 Penalti Ridge L2: Ganjal Kayu Penyelamat

[ANALOGI] Bagaimana cara SHADOW menyembuhkan meja yang bergoyang dan sakit parah ini? Jawabannya sangat elegan: Kita memasang **ganjal kayu tambahan** di bawah setiap kaki meja!

Dalam matematika regresi, teknik ganjal kayu ini disebut **Regularisasi Ridge (L2)** atau Regularisasi Tikhonov. Kita menambahkan sedikit penalti sebesar `lambda_penalti` dikalikan dengan Matriks Identitas `I`:

```
beta_ridge = (X^T * X + lambda_penalti * I)^(-1) * X^T * y
```

### Keajaiban Matematis Penyelamatan Ridge

Ketika kita menambahkan `lambda_penalti * I`, seluruh nilai eigen matriks bergeser ke atas secara merata:

```
lambda_baru = lambda_lama + lambda_penalti
```

Perhatikan apa yang terjadi pada kaki meja terlemah:
1. Nilai eigen terkecil yang tadinya nyaris nol (0.00001) kini **pasti bernilai positif**: lambda_min_baru = 0.00001 + 1.0 = 1.00001!
2. Matriks kini **dijamin mustahil bernilai nol atau singular**.
3. Angka kondisi yang tadinya bernilai puluhan juta langsung turun drastis:
   - Sebelum Ridge: kappa = 400 / 0.00001 = **40.000.000** (Sakit Parah!)
   - Setelah Ridge: kappa = (400 + 1) / (0.00001 + 1) = 401 / 1.00001 = **400.99** (Sembuh Total!)
4. Bobot koefisien kembali tenang, stabil, dan memiliki daya tahan tinggi terhadap data baru di masa depan.

Inilah alasan ilmiah mengapa SHADOW secara otomatis memilih model linier teregularisasi Ridge L2 saat mendeteksi adanya korelasi antar-fitur pada data tabular!

---

## 4.4 Uji Brier Score Murphy (1973)

Banyak model klasifikasi hanya dinilai dari akurasi tebakan akhirnya (benar atau salah). Padahal di dunia nyata, **derajat keyakinan (probabilitas)** dari tebakan tersebut jauh lebih penting!

[ANALOGI] Bayangkan dua peramal cuaca di televisi:
* Peramal A berkata: *"Besok 100% pasti cerah!"* Ternyata besok hujan deras. **SOMBONG!**
* Peramal B berkata: *"Besok ada kemungkinan hujan 60% dan cerah 40%."* Besok hujan turun. **BIJAKSANA!**

Peramal B jauh lebih bijaksana dan terkalibrasi daripada Peramal A yang sombong (*overconfident*).

**Brier Score** mengukur seberapa akurat dan jujur probabilitas ramalan:

```
Brier Score = (1 / N) * SUM_{i=1}^N (p_i - y_i)^2
(Skor 0 berarti ramalan sempurna dan terkalibrasi total)
```

### Tiga Komponen Pembedah Allan H. Murphy (1973)

Brier Score dapat dibedah menjadi tiga bagian:

```
Brier Score = Reliability - Resolution + Uncertainty
```

| Komponen | Arti | Target |
| :--- | :--- | :--- |
| **Reliability** (Kejujuran Kalibrasi) | Jika model berkata 80% selamat, apakah benar ~80 dari 100 orang selamat? | Ingin mendekati 0 |
| **Resolution** (Daya Pisah Model) | Seberapa hebat model membedakan kelompok yang selamat dari yang tidak | Ingin setinggi mungkin |
| **Uncertainty** (Kesulitan Alami Masalah) | Tingkat ketidakpastian dasar yang tidak bisa dihilangkan model apa pun | Tidak bisa diubah |

---

## 4.5 ROC-AUC pada Data Timpang dan Uji Nadeau-Bengio

Pada data yang sangat tidak seimbang (*imbalanced data*, misalnya kasus penipuan kartu kredit di mana hanya 1 dari 1.000 transaksi yang merupakan penipuan):
* Kurva **ROC-AUC** bisa terlihat sangat tinggi (misalnya 0.95), padahal kenyataannya model gagal mendeteksi penipuan! Mengapa? Karena rumus ROC-AUC membagi dengan jumlah transaksi normal yang sangat besar, sehingga kesalahan model tertutupi oleh lautan data normal.
* Oleh karena itu, SHADOW secara otomatis beralih memantau **PR-AUC (Precision-Recall AUC)** dan **Weighted F1-Score** saat mendeteksi data yang timpang.

### Uji Signifikansi Statistik Terkoreksi Nadeau-Bengio (2003)

Saat membandingkan dua model pada validasi silang (Cross Validation), kita tidak boleh menggunakan uji-t biasa (Student's t-test). Mengapa? Karena lipatan data latih saling tumpang tindih (*overlapping training sets*), sehingga observasi tidak saling bebas (*independent*).

SHADOW mengadopsi rumus koreksi variansi **Nadeau-Bengio**:

```
Var_terkoreksi = Var_sampel * ( (1 / K) + (n_test / n_train) )

K = jumlah fold (5)
n_test / n_train = 1 / (K - 1) = 0.25
```

Dengan koreksi ini, dewan penguji dapat yakin 100% bahwa keunggulan model champion kita memang nyata secara statistik, bukan kebetulan semata.

---

## 4.6 Ringkasan Rumus Matematika (Formula Sheet)

| No | Rumus | Kegunaan di SHADOW |
| :---: | :--- | :--- |
| 1 | `beta = (X^T*X)^(-1) * X^T*y` | Solusi analitis OLS (Ordinary Least Squares) |
| 2 | `beta_ridge = (X^T*X + lambda*I)^(-1) * X^T*y` | Solusi Ridge teregularisasi L2 |
| 3 | `kappa = lambda_max / lambda_min` | Angka kondisi matriks (ukuran kestabilan) |
| 4 | `Brier = (1/N) * SUM(p_i - y_i)^2` | Kejujuran probabilitas ramalan |
| 5 | `Var_NB = s^2 * (1/K + n_test/n_train)` | Koreksi Nadeau-Bengio untuk CV |
| 6 | `r = cov(X,Y) / (std(X) * std(Y))` | Korelasi Pearson (deteksi leakage) |
| 7 | `Accuracy = (TP+TN) / (TP+TN+FP+FN)` | Ketepatan prediksi keseluruhan |
| 8 | `F1 = 2*P*R / (P+R)` | Keseimbangan presisi dan recall |
| 9 | `R2 = 1 - SS_res / SS_tot` | Varians terjelaskan oleh model (regresi) |
| 10 | `MAE = (1/N) * SUM abs(y_i - y_hat_i)` | Rata-rata kesalahan absolut (regresi) |

---

# BAGIAN 5: PANDUAN LENGKAP DAN NASKAH KATA-DEMI-KATA 34 SLIDE

> **Petunjuk Presenter Sidang**:
> Bagian ini memuat urutan 34 slide yang **100% PERSIS DAN IDENTIK** dengan berkas presentasi web `slides.html`.
> Untuk setiap slide, pelajari: **Pesan Utama**, **Penjelasan Bahasa Mudah**, **Naskah Lisan Kata-demi-Kata**, **Panduan Aksi Panggung**, dan **Strategi Menjawab Jebakan Penguji**.
> Waktu ideal presentasi: **15 hingga 20 menit** (rata-rata 30-40 detik per slide).

---

### SLIDE 1: JUDUL DAN HERO SPLASH
* **Judul**: **SHADOW: Multi-Agent ML Assistant**
* **Konsep Bahasa Mudah**: Pembukaan megah yang menegaskan proyek ini adalah asisten sains data profesional yang jujur dan patuh pada kaidah rekayasa perangkat lunak modern.
* **Panduan Aksi Panggung**: Berdiri tegak di sisi layar proyektor. Tatap seluruh dewan penguji dengan ramah dan percaya diri. Buka kedua tangan Anda.
* **Naskah Lisan Kata-demi-Kata**:
  > "Selamat pagi Bapak dan Ibu Dewan Penguji yang kami hormati.
  >
  > Hari ini kami mempersembahkan **SHADOW: Multi-Agent Machine Learning Assistant**. Sistem ini adalah platform pembelajaran mesin multi-agen otonom yang dibangun dengan integritas sains data tertinggi dan kepatuhan penuh terhadap standar rekayasa perangkat lunak modern.
  >
  > Proyek ini bukan sekadar skrip pemanggil model biasa, melainkan platform agnostik yang dirancang untuk memproses file CSV tabular apa pun secara deterministik, bebas dari kebocoran target, dan dapat diaudit secara forensik dari hulu ke hilir. Seluruh angka evaluasi yang akan kami tunjukkan hari ini bersumber 100% dari komputasi Scikit-Learn lokal, bukan dari halusinasi model bahasa."
* **[JEBAKAN]**: Jangan pernah menyebut proyek ini sebagai 'Aplikasi Titanic'! Tegaskan bahwa sistem ini bekerja pada file CSV apa pun. Titanic hanyalah salah satu bahan uji coba.

---

### SLIDE 2: RINGKASAN EKSEKUTIF
* **Judul**: **Integritas Sains Data Berbasis Bukti**
* **Naskah Lisan**:
  > "Fondasi SHADOW bertumpu pada empat pilar integritas:
  >
  > Pertama, *Local Execution* -- seluruh data diproses secara lokal pada laptop pengguna tanpa mengunggah data rahasia ke cloud.
  > Kedua, *Zero Metric Hallucination* -- kami memisahkan penalaran LLM dari komputasi numerik.
  > Ketiga, *Forensic Audit Trail* -- setiap pemanggilan API LLM dicatat lengkap dengan timestamp milidetik dan prompt mentah di file log forensik.
  > Keempat, *Full Reproducibility* -- setiap eksperimen menghasilkan notebook Jupyter yang terbukti dapat dijalankan ulang secara mandiri dengan hasil yang identik."

### SLIDE 3: LANDASAN MASALAH
* **Judul**: **Krisis Integritas pada AutoML dan Wrapper LLM Tradisional**
* **Naskah Lisan**:
  > "Di industri saat ini, banyak sistem AutoML mengalami lima kegagalan fatal: target leakage tersembunyi, halusinasi angka metrik, notebook yang rusak, perdebatan agen tanpa henti, dan keputusan kotak hitam. SHADOW dibangun secara spesifik dari prinsip *first-principles* untuk menuntaskan kelima krisis integritas ini."

### SLIDE 4: PONDASI METODOLOGI
* **Judul**: **Pondasi Ilmiah dan Metodologi Ketat**
* **Naskah Lisan**:
  > "Lima prinsip metodologi ketat: Pertama, doktrin LLM Memutuskan Python Mengerjakan. Kedua, Protokol Brankas Data Uji 80/20. Ketiga, prinsip Occam's Razor. Keempat, stabilisasi multikolinearitas via aljabar spektral Ridge L2. Dan kelima, penolakan mutlak terhadap manipulasi atau rekayasa angka."

### SLIDE 5: RUANG LINGKUP
* **Judul**: **Ruang Lingkup dan Batasan Masalah**
* **Naskah Lisan**:
  > "Secara ruang lingkup, SHADOW dirancang khusus untuk data tabular terstruktur berformat CSV -- mencakup kasus klasifikasi biner, klasifikasi multikelas, dan regresi kontinu. Sistem ini dioptimalkan untuk berjalan secara efisien pada laptop standar dengan RAM 8 GB, menerapkan prinsip satu model aktif pada satu waktu, dan menggunakan Python 3.11+ bersama pustaka Scikit-Learn dan Gemini Flash Lite."

### SLIDE 6: ARSITEKTUR 5 TAHAP
* **Judul**: **Diagram Alur: 5 Tahap Sekuensial Linier**
* **Naskah Lisan**:
  > "Mari kita telaah arsitektur multi-agen SHADOW. Kami menolak perdebatan melingkar yang tidak menentu. Alur kerja berjalan maju secara terstruktur melalui **5 Tahap Sekuensial Agen**:
  >
  > Tahap 1: Problem Framer merumuskan masalah dan target.
  > Tahap 2: Data Wrangler membersihkan data dan memusnahkan leakage.
  > Tahap 3: Model Guardian melatih baseline dan model kandidat dengan 5-fold CV.
  > Tahap 4: Insight Storyteller mengekstrak koefisien dan narasi bisnis.
  > Tahap 5: Notebook Builder merakit notebook mandiri dan memvalidasinya secara headless via nbclient.
  > Seluruh agen membaca dan memperkaya satu Blackboard repositori terpusat: `state.json`."

### SLIDE 7-13: DETAIL TAHAP 1-2 (FRAMING, DATA, LEAKAGE, PREPROCESSING, FIT-IN-FOLD, SEALED HOLDOUT)

Setiap slide menjelaskan secara mendalam satu aspek dari Tahap 1 dan 2. Naskah lisan mengikuti pola yang sama: menyebutkan judul konsep, menjelaskan dengan bahasa mudah, lalu memberi bukti teknis.

### SLIDE 14-15: MATEMATIKA SPEKTRAL DAN RIDGE L2

* **Naskah Lisan Slide 14**:
  > "Mari kita tinjau keindahan matematika di balik sistem kami. Solusi analitis OLS bergantung pada inversi Matriks Gram: beta = (X^T * X)^(-1) * X^T * y. Melalui dekomposisi spektral, inversi memuat suku 1 per lambda_j. Jika terjadi multikolinearitas, lambda_min mendekati nol dan variansi bobot meledak tak terkendali."

* **Naskah Lisan Slide 15**:
  > "Bagaimana SHADOW menyelamatkan matriks yang sakit ini? Kami menerapkan regularisasi penalti Ridge L2. Nilai eigen baru terkoreksi menjadi lambda_j ditambah lambda_penalti. Angka kondisi yang tadinya puluhan juta langsung turun drastis ke kisaran 400."

### SLIDE 16-21: TAHAP 3-5 (MODELING, BASELINE, CV, STORYTELLING, NOTEBOOK)

Setiap slide membedah satu aspek dari evaluasi model, Insight Storyteller, dan Notebook Builder.

### SLIDE 22: BUKTI EMPIRIS TITANIC
* **Naskah Lisan**:
  > "Ini adalah bukti empiris pertama kami pada dataset Titanic: Model Champion Logistic Regression (L2) mencapai Akurasi Holdout 80.00%, Weighted F1 0.7750, dan ROC-AUC 0.7564. Perhatikan Overfit Gap yang sangat tipis: hanya 0.0036! Menunjukkan generalisasi yang sangat prima."

### SLIDE 23: BUKTI EMPIRIS INSURANCE
* **Naskah Lisan**:
  > "Bukti empiris kedua pada dataset Medical Insurance untuk kasus regresi kontinu: R-Squared sebesar 0.9882, dengan Mean Absolute Error hanya 789.89. Fitur status merokok dan BMI terbukti menjadi pendorong biaya terbesar."

### SLIDE 24: BUKTI EMPIRIS TELCO CHURN
* **Naskah Lisan**:
  > "Bukti empiris ketiga pada dataset Telco Churn untuk klasifikasi data tidak seimbang: ROC-AUC 0.7813 dan berhasil menangkap 19 pelanggan churn sejati. Ketiga dataset membuktikan pipeline kami adaptif tanpa mengubah satu baris pun kode inti."

### SLIDE 25-31: PRODUKSI, PYTEST, ANATOMI KODE

Slide ini membahas inferensi mandiri, penegakan schema, test suite pytest, dan bedah repositori.

### SLIDE 32: MATRIKS 9 KRITERIA
* **Naskah Lisan**:
  > "Tabel ini merangkum pembuktian kepatuhan terhadap seluruh sembilan kriteria kelayakan resmi. Kami tidak meminta kelulusan atas dasar janji, melainkan atas dasar bukti eksekusi nyata."

### SLIDE 33: STREAMLIT SHADOW ARENA
* **Naskah Lisan**:
  > "Aplikasi Streamlit Shadow Arena mengusung tema Dark Chocolate dan Madu Emas. Arena ini menghubungkan output state.json ke panggung visual 5 agen dan menyediakan formulir input dinamis."

### SLIDE 34: KESIMPULAN DAN TANYA JAWAB
* **Panduan Aksi Panggung**: Buka kedua telapak tangan ke arah dewan penguji. Senyum hangat, tatap mata dewan penguji, dan persilakan sesi tanya jawab dimulai.
* **Naskah Lisan**:
  > "Sebagai kesimpulan, SHADOW membuktikan bahwa otomasi machine learning tidak harus mengorbankan integritas sains data.
  >
  > Dengan memisahkan penalaran strategis AI dari eksekusi komputasi deterministik Python, kami menghadirkan sistem yang jujur, bebas halusinasi, tangguh terhadap kebocoran data, dan dapat diaudit secara forensik.
  >
  > Sistem ini siap diuji secara langsung pada file CSV baru apa pun dari Bapak dan Ibu Dewan Penguji hari ini. Terima kasih atas perhatiannya, sesi tanya jawab dan demonstrasi langsung resmi kami buka."

---

# BAGIAN 6: BUKTI EMPIRIS RIIL DARI 3 DATASET BENCHMARK

Seluruh angka di bawah ini diekstrak langsung dari berkas artefak eksekusi nyata di folder `outputs/`:

## 6.1 Benchmark 1: Titanic (Klasifikasi Biner)

* **Lokasi Artefak**: `outputs/run_titanic/state.json`
* **Dimensi**: 700 baris x 9 kolom.
* **Tantangan Data**: Nilai hilang pada kolom `Age` sebesar 19.3%, kolom identitas unik `PassengerId` (keunikan 100%).
* **Keputusan Tahap 1 (Problem Framer)**: Target = `Survived`, Task = `binary_classification`, Metrik Primer = `ROC-AUC / Weighted F1`.
* **Keputusan Tahap 2 (Data Wrangler)**: Kolom `PassengerId` didrop. Imputasi median + RobustScaler untuk numerik, Imputasi modus + OneHotEncoder untuk kategori.
* **Hasil Evaluasi Tahap 3 (Model Guardian)**:
  * Baseline Dummy: Akurasi 61.60%, ROC-AUC 0.5000.
  * Logistic Regression (L2): CV Akurasi 79.64%, Holdout Test Akurasi **80.00%**, Weighted F1 **0.7750**, ROC-AUC **0.7564**, Brier Score **0.1523**, Overfit Gap **0.0036**.
  * Random Forest: CV Akurasi 80.50%, Holdout Test Akurasi 79.28%, Overfit Gap 0.0820.
  * **Model Champion Terpilih**: **Logistic Regression (L2)** (Menerapkan Pisau Bedah Occam: Akurasi stabil dengan overfit gap 20x lebih tipis dibanding Random Forest).
* **Matriks Kebingungan (Confusion Matrix pada 140 Baris Data Uji Unseen)**:
  * True Negative (Diprediksi Meninggal dan Benar Meninggal): **101 orang**
  * False Positive (Diprediksi Selamat padahal Meninggal): **6 orang**
  * False Negative (Diprediksi Meninggal padahal Selamat): **22 orang**
  * True Positive (Diprediksi Selamat dan Benar Selamat): **11 orang**
* **Faktor Pendorong Terbesar**: Jenis kelamin wanita (`Sex_female` koefisien +1.28) dan kelas kabin mewah (`Pclass` kelas 1).
* **Verifikasi Tahap 5**: Berkas `notebook.ipynb` lolos eksekusi ulang via `nbclient` tanpa runtime error.

---

## 6.2 Benchmark 2: Medical Insurance (Regresi Kontinu)

* **Lokasi Artefak**: `outputs/run_insurance/state.json`
* **Dimensi**: 1.338 baris x 7 kolom.
* **Tantangan Data**: Target bernilai uang kontinu (`charges`) dengan rentang ribuan, fitur demografi campuran.
* **Keputusan Tahap 1**: Target = `charges`, Task = `regression`, Metrik Primer = `R-Squared (R2) / MAE`.
* **Hasil Evaluasi**:
  * Baseline Dummy: R2 -0.0012, MAE 9.150.
  * Ridge Regression (L2): CV R2 0.9870, Holdout Test R2 **0.9882** (98.82% varians terjelaskan!), MAE **789.89**, RMSE **987.84**.
  * **Model Champion**: **Ridge Regression (L2)** (Stabilisasi L2 menyerap multikolinearitas usia dan BMI).
* **Faktor Pendorong Terbesar**: Status tidak merokok (`smoker_no` menurunkan tagihan -8.968), BMI (menaikkan +3.378), Usia (menaikkan +2.540).

---

## 6.3 Benchmark 3: Telco Customer Churn (Data Timpang)

* **Lokasi Artefak**: `outputs/run_telco_churn/state.json`
* **Dimensi**: 600 baris x 6 kolom. Ketimpangan: 73% bertahan vs 27% churn.
* **Keputusan Tahap 1**: Target = `churn`, Metrik Primer = `F1-Score / PR-AUC`.
* **Keputusan Tahap 2**: Kolom `customerID` didrop otomatis.
* **Hasil Evaluasi**:
  * Baseline Dummy: F1 0.0000 (Menebak semua pelanggan tidak churn).
  * Logistic Regression (L2): Holdout Test Akurasi **70.00%**, ROC-AUC **0.7813**, Weighted F1 **0.6865**.
* **Matriks Kebingungan (120 Baris Data Uji Unseen)**: TN=65, FP=12, FN=24, TP=19.

---

## 6.4 Tabel Rekapitulasi Komparatif

| Parameter | Dataset 1: Titanic | Dataset 2: Insurance | Dataset 3: Telco Churn |
| :--- | :--- | :--- | :--- |
| **Jenis Tugas ML** | Klasifikasi Biner | Regresi Kontinu | Klasifikasi Timpang |
| **Jumlah Baris** | 700 | 1.338 | 600 |
| **Kolom Target** | `Survived` | `charges` | `churn` |
| **Metrik Primer** | ROC-AUC / F1 | R-Squared / MAE | F1-Score / PR-AUC |
| **Kolom ID Didrop** | `PassengerId` | - | `customerID` |
| **Model Champion** | Logistic Regression (L2) | Ridge Regression (L2) | Logistic Regression (L2) |
| **Skor Utama Holdout** | **Akurasi 80.00%** | **R2 = 0.9882** | **ROC-AUC = 0.7813** |
| **Overfit Gap** | **0.0036 (Sangat Tipis)** | 0.0012 | 0.0150 |
| **Replay Notebook** | **LULUS 100% (nbclient)** | **LULUS 100%** | **LULUS 100%** |

---

# BAGIAN 7: BEDAH KODE REKAYASA SISTEM DAN ANATOMI BERKAS

## 7.1 Peta Repositori Lengkap

```
ml-agents/
+-- main.py                     # Entry point CLI terpadu: train dan predict
+-- app.py                      # Dashboard Streamlit Studio Arena
+-- slides.html                 # Slide Presentasi Web Interaktif 34 Slide
+-- Makefile                    # Target: make slides, streamlit, test, gram, clean
+-- README.md                   # Dokumentasi publik portofolio
+-- Scope.md                    # Kontrak acuan resmi dan Definition of Done
+-- pyproject.toml              # Konfigurasi proyek dan pytest
+-- requirements.txt            # Pustaka Python terkurasi
+-- docs/
|   +-- BUKU_MASTER_SHADOW_ML.md # BUKU INI!
+-- core/
|   +-- pipeline.py             # Orkestrator run_pipeline 5 agen
|   +-- state.py                # Blackboard: dataclass SharedState (SSOT)
|   +-- llm.py                  # Gateway Gemini + log forensik + retry + fallback
|   +-- tools/                  # SEMUA KOMPUTASI DETERMINISTIK (TANPA LLM!)
|       +-- profiling.py        # Statistik deskriptif, missing, kardinalitas, kandidat target
|       +-- cleaning.py         # ColumnTransformer (fit-in-fold, median, robust, onehot)
|       +-- modeling.py         # 5-Fold CV, Dummy, Overfit Gap, Occam, Nadeau-Bengio, Canary
|       +-- plotting.py         # Ekstraksi bobot dan 4 visualisasi Matplotlib 150 DPI
|       +-- notebook.py         # Perakitan .ipynb dan eksekusi headless nbclient
|       +-- predict.py          # Validasi schema ketat dan inferensi mandiri
|       +-- session_payload.py  # Builder payload arena visual Streamlit
+-- agents/                     # SEMUA AGEN (PEMBUAT RENCANA JSON VIA LLM)
|   +-- personas.py             # Definisi persona 5 agen dan template prompt dinamis
|   +-- base_agent.py           # Runner penghubung LLM, fakta data, dan fallback
|   +-- framing_agent.py        # Tahap 1: Problem Framing
|   +-- data_agent.py           # Tahap 2: Data Wrangler dan Anti-Leakage
|   +-- modeling_agent.py       # Tahap 3: Model Guardian dan Occam's Razor
|   +-- insight_agent.py        # Tahap 4: Insight Storyteller dan Pelaporan
|   +-- notebook_agent.py       # Tahap 5: Notebook Builder dan Ekspor
+-- data/                       # Dataset benchmark (titanic.csv, insurance.csv, telco_churn.csv)
+-- outputs/                    # Folder artefak nyata per sesi run
+-- tests/                      # Suite unit dan integration test (6/6 passed)
    +-- test_m1_pipeline.py     # 5 tes pipeline inti
    +-- test_mock_llm_flow.py   # 1 tes alur penuh dengan mock LLM offline
```

### Aturan Emas Arsitektur

* `core/tools/` **TIDAK BOLEH** mengimpor atau memanggil LLM. Murni Python deterministik.
* `agents/` **TIDAK BOLEH** melatih model secara langsung. Agen memanggil fungsi di `core/tools/`.
* Pemisahan ini menjamin bahwa semua angka bersumber dari komputasi, bukan halusinasi.

---

## 7.2 Bedah Berkas Pengendali

### 1. `main.py` -- Pintu Masuk Terminal CLI (467 baris)
* Menggunakan modul bawaan `argparse` untuk mendukung dua subperintah:
  - `python main.py train <data.csv>`: Menjalankan pipeline pelatihan 5 agen dari hulu ke hilir.
  - `python main.py predict --run <folder> --input '<json>'`: Menjalankan inferensi data baru.
* Mengorkestrasi seluruh 5 tahap secara berurutan dengan callback notifikasi ke Streamlit.
* Menyimpan `state.json` di akhir proses.

### 2. `core/state.py` -- Papan Tulis Bersama / Blackboard SSOT (90 baris)
* Mengimplementasikan Python `@dataclass` bernama `SharedState` dengan 14 atribut terstruktur.
* Menyediakan fungsi `save_to_file()` untuk serialisasi ke JSON via `json.dump(asdict(self))`.
* Menyediakan fungsi `load_from_file()` untuk memuat kembali via `cls(**data)`.
* Menyediakan fungsi `add_debate_turn()` untuk mencatat setiap giliran bicara agen ke transkrip.

### 3. `core/llm.py` -- Gerbang Komunikasi LLM Aman (298 baris)
* Membungkus pemanggilan Google Gemini (`gemini-3.1-flash-lite`) melalui kelas `GeminiClient`.
* Mendukung dua metode koneksi: (a) pustaka `google-genai` resmi, (b) HTTP `urllib` langsung.
* **Rantai Fallback 3 Model**: Jika model utama gagal (error 404), coba model berikutnya.
* **Retry pada Error Sementara**: Jika error 429 (rate limit) atau 503 (server sibuk), tunggu progresif.
* **Validasi JSON Ketat**: Jika respons bukan JSON valid, tambahkan instruksi koreksi dan minta ulang.
* Mencatat setiap transaksi ke `llm_log.jsonl` dengan format: timestamp, agen, model, latensi, prompt, response.
* Membersihkan markdown formatting (```json ... ```) secara otomatis.

---

## 7.3 Bedah Berkas Alat Deterministik

1. **`core/tools/profiling.py`** (277 baris):
   Menghitung jumlah baris, tipe data kolom, jumlah nilai kosong, statistik deskriptif (mean, median, std, skewness), mendeteksi kolom ID unik (> 95%), dan menghitung korelasi Pearson terhadap target.

2. **`core/tools/cleaning.py`** (148 baris):
   Merakit Scikit-Learn `ColumnTransformer` melalui fungsi `build_preprocessor_pipeline()`:
   - Numerik: `SimpleImputer(strategy='median')` + `RobustScaler()`
   - Kategorikal: `SimpleImputer(strategy='most_frequent')` + `OneHotEncoder(max_categories=25, handle_unknown='ignore')`
   Juga mendukung pembuatan fitur turunan sederhana (maksimal 2 fitur).

3. **`core/tools/modeling.py`** (391 baris) -- **FILE TERPENTING!**:
   - `split_train_test()`: Membagi 80/20 dengan stratifikasi untuk klasifikasi.
   - `get_candidate_models()`: Mengembalikan 4 model (Dummy + 3 kandidat).
   - `evaluate_cross_validation()`: 5-Fold CV, overfit gap, Pipeline yang menjamin fit-in-fold.
   - `fit_and_evaluate_final_model()`: Evaluasi holdout SATU KALI.
   - `extract_feature_importance()`: Mengekstrak `coef_` atau `feature_importances_`.
   - `calculate_nadeau_bengio_ttest()`: Uji statistik terkoreksi.
   - `run_permutation_canary_test()`: Uji kanari anti-kebocoran prosedural.

4. **`core/tools/plotting.py`** (277 baris):
   Mengekstrak bobot koefisien nyata dari pipeline Scikit-Learn dan menggambar 4 grafik PNG resolusi tinggi (150 DPI) menggunakan Matplotlib/Seaborn tanpa campur tangan LLM.

---

## 7.4 Bedah Berkas Produksi dan Antarmuka

1. **`core/tools/predict.py`** (240 baris):
   - `save_artifacts_for_prediction()`: Menyimpan `model.joblib` dan `schema.json`.
   - `predict_single_or_batch()`: Memuat pipeline, validasi input, menolak kolom hilang via `ValueError`.
   - Schema.json mencatat kolom wajib, tipe data, rentang min/max, dan kategori yang dikenal.

2. **`core/tools/notebook.py`** (277 baris):
   Menyusun 11 sel kode menggunakan `nbformat` dan menjalankan ulang secara headless via `nbclient.NotebookClient(timeout=300, kernel_name='python3')`.

3. **`app.py`** (698 baris):
   Aplikasi Streamlit dengan tema Dark Chocolate (#0F0804) dan Honey Gold (#E8B04A). Fitur: panggung visual 5 agen, penjelajah sesi riset, unduh notebook, form prediksi dari schema.

---

# BAGIAN 8: AUDIT 9 KRITERIA KELAYAKAN SISTEM DAN HASIL PYTEST

## 8.1 Matriks Pembuktian 9 Kriteria Kelayakan

| No | Kriteria Kelayakan Resmi | Bukti Implementasi | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Pelatihan CLI Berjalan Penuh** | 3 dataset berhasil dari hulu ke hilir | **LULUS** |
| **2** | **Bebas Data Hardcoded** | Dataset berbeda = hasil berbeda secara dinamis | **LULUS** |
| **3** | **Notebook Tervalidasi Nbclient** | nbclient replay sukses, toleransi 0.001 | **LULUS** |
| **4** | **Bukti Pemanggilan API LLM** | llm_log.jsonl terisi lengkap per sesi | **LULUS** |
| **5** | **Gagal Harus Terlihat Transparan** | Error eksplisit, tidak ada silent failure | **LULUS** |
| **6** | **Metrik Murni dari Python** | Semua angka dari Scikit-Learn, dikunci di state.json | **LULUS** |
| **7** | **Test Suite Pytest Lulus Penuh** | 24/24 PASSED (6 pipeline + 18 backend) | **LULUS** |
| **8** | **Inferensi Mandiri dan Penolakan Input** | predict.py menolak input cacat via ValueError | **LULUS** |
| **9** | **Penguasaan Materi Repositori** | Presenter siap bedah kode dan rumus | **SIAP UJI** |

---

## 8.2 Laporan Hasil Pengujian Otomatis Pytest

### A. Test Suite Pipeline Inti (`pytest -v tests`): 6/6 PASSED (14.80s)
1. `test_profiling_and_leakage_detection`: Profiling dan pembuangan kolom ID -- **PASSED**
2. `test_planted_leakage_is_detected`: Leakage buatan r=0.99 terdeteksi -- **PASSED**
3. `test_full_pipeline_classification`: Alur penuh klasifikasi + nbclient -- **PASSED**
4. `test_full_pipeline_regression`: Alur penuh regresi + nbclient -- **PASSED**
5. `test_missing_column_is_rejected`: Penolakan input cacat (DoD 8) -- **PASSED**
6. `test_full_pipeline_with_mock_llm`: Orkestrator offline dengan Mock LLM -- **PASSED**

### B. Test Suite Backend (`pytest -v backend/tests`): 18/18 PASSED
* Validasi numerik, batas karakter, endpoint REST, siklus sesi, pencegahan kontaminasi.

**Total**: **24 Pengujian Berhasil Lulus Sempurna (100%)**

---

# BAGIAN 9: DEFENSE WAR ROOM 40 PERTANYAAN KRITIS DAN JAWABAN TELAK

Gunakan bagian ini sebagai senjata rahasia untuk melibas pertanyaan tersulit dewan penguji:

### Q1: "Apakah sistem ini hanya dibuat khusus untuk dataset Titanic?"
> "Sama sekali tidak, Bapak/Ibu. Titanic hanyalah salah satu dari tiga dataset benchmark pengujian kami. SHADOW adalah platform agnostik yang dapat memproses file CSV tabular apa pun. Di benchmark kedua, kami menguji data asuransi untuk regresi kontinu dengan R2 = 0.9882, dan di benchmark ketiga kami menguji data Telco Churn untuk klasifikasi timpang. Kami siap mendemonstrasikannya langsung pada file CSV baru apa pun dari dewan penguji hari ini."

### Q2: "Bagaimana Anda membuktikan bahwa angka akurasi 80% tidak dikarang oleh LLM?"
> "Kami menerapkan doktrin pemisahan mutlak: LLM Memutuskan, Python Mengerjakan. LLM hanya bertugas merumuskan rencana dan narasi kualitatif. Seluruh perhitungan evaluasi dihitung oleh pustaka Scikit-Learn di modul `core/tools/modeling.py` dan dikunci ke dalam file `state.json`. Jika LLM mencoba mengubah angka, respons tersebut otomatis digugurkan."

### Q3: "Mengapa Logistic Regression, bukan XGBoost atau Deep Learning?"
> "Kami menerapkan prinsip Occam's Razor secara ilmiah. Pada data tabular berukuran ratusan hingga ribuan baris, model linier teregularisasi L2 menawarkan generalisasi yang sangat stabil dengan interpretabilitas bobot fitur yang transparan. Pada dataset Titanic, Random Forest hanya unggul 0.5% pada data latih namun memiliki overfit gap 20x lebih lebar. Kami mengutamakan ketahanan generalisasi di dunia nyata."

### Q4: "Bagaimana sistem mencegah Data Leakage saat imputasi?"
> "Kami menerapkan protokol Fit-in-Fold secara ketat menggunakan Scikit-Learn ColumnTransformer. Nilai median dan modus dihitung HANYA dari data latih aktif pada setiap fold. Data uji 20% disegel sejak awal dalam Sealed Holdout Vault dan sama sekali tidak pernah disentuh oleh proses imputasi."

### Q5: "Apa yang terjadi jika multikolinearitas parah?"
> "Ketika multikolinearitas terjadi, nilai eigen terkecil lambda_min dari Matriks Gram X^T * X mendekati nol, menyebabkan angka kondisi melonjak di atas 30 dan variansi bobot OLS meledak. SHADOW menyelamatkannya dengan penalti Ridge L2 (lambda * I). Nilai eigen baru terkoreksi menjadi lambda_min + lambda, menjamin matriks strictly definit positif."

### Q6: "Mengapa tidak menggunakan pola critique loop seperti AutoGen?"
> "Pola critique loop sering terjebak dalam perdebatan semantik tak berujung yang memboroskan ribuan token API dan tidak menjamin konvergensi. SHADOW mengadopsi Pola 5 Tahap Sekuensial Linier di atas arsitektur Blackboard: Setiap agen memiliki wewenang tegas dan meneruskan estafet secara deterministik."

### Q7: "Bagaimana membuktikan notebook benar-benar reproducible?"
> "Modul `notebook.py` menggunakan mesin `nbclient.NotebookClient` untuk mengeksekusi ulang seluruh 11 sel kode secara headless di kernel terisolasi sebelum menandai eksperimen selesai. Jika ada sel error atau metrik tidak identik dengan toleransi 0.001, sistem langsung membatalkan status kelulusan."

### Q8: "Bagaimana menangani input yang kehilangan kolom saat inferensi?"
> "Modul `predict.py` mencocokkan input terhadap `schema.json`. Jika ada kolom wajib yang hilang, sistem melempar `ValueError` transparan dan menolak prediksi, mencegah silent failure di lingkungan produksi."

### Q9: "Mengapa ROC-AUC menyesatkan pada data tidak seimbang?"
> "Karena False Positive Rate pada kurva ROC membagi FP dengan seluruh True Negative. Pada data timpang di mana TN berjumlah masif, lonjakan FP hanya mengubah FPR sedikit sekali. SHADOW secara otomatis beralih memantau PR-AUC atau Weighted F1-Score."

### Q10: "Apa fungsi Uji Nadeau-Bengio?"
> "Uji-t standar pada Cross Validation tidak valid karena lipatan data latih tumpang tindih. Koreksi variansi Nadeau-Bengio (2003) memperhitungkan rasio n_test / n_train, menjadikan pengujian signifikansi antar-model valid secara matematis."

### Q11: "Apa itu Brier Score dan mengapa dekomposisinya penting?"
> "Brier Score mengukur akurasi kuadratik probabilitas prediksi. Dekomposisi Murphy (1973) membedahnya menjadi Reliability, Resolution, dan Uncertainty -- membuktikan apakah model terkalibrasi atau hanya beruntung."

### Q12: "Bagaimana membedakan peran LLM vs Python di kode?"
> "Semua file di `core/tools/` murni berisi fungsi Python tanpa import LLM. Sementara file di `agents/` dan `core/llm.py` bertugas memformat prompt dan memvalidasi JSON. Pemisahan ini terlihat jelas di arsitektur direktori kami."

### Q13: "Bagaimana jika internet mati saat presentasi?"
> "Sistem dilengkapi Deterministic Offline Fallback. Di `core/llm.py`, jika koneksi putus, agen beralih ke logika deterministik bawaan. Test `test_mock_llm_flow.py` membuktikan pipeline berjalan 100% offline."

### Q14: "Mengapa gemini-3.1-flash-lite?"
> "Latensi rendah (rata-rata di bawah 1 detik), kuota hemat, kepatuhan JSON tinggi, dan efisien untuk laptop pengembang."

### Q15: "Apa itu Single Source of Truth (SSOT)?"
> "SSOT kami adalah `state.json`. Semua agen membaca dan menulis ke sini. Streamlit, grafik, dan notebook semuanya merujuk ke satu file ini sehingga tidak akan pernah terjadi inkonsistensi."

### Q16: "Bagaimana menentukan Klasifikasi vs Regresi?"
> "Problem Framer memeriksa tipe data dan jumlah nilai unik target. Kategori atau diskrit kurang dari 10 unik = klasifikasi. Float kontinu dengan ratusan nilai = regresi."

### Q17: "Bagaimana menangani outlier?"
> "RobustScaler menggunakan median dan IQR (Q3-Q1), sangat kebal outlier. Berbeda dengan StandardScaler yang membagi dengan deviasi standar yang rentan terhadap nilai ekstrem."

### Q18: "Berapa lama waktu eksekusi pipeline?"
> "Sekitar 20-30 detik pada laptop 8 GB RAM untuk dataset ~1.000 baris, termasuk validasi nbclient."

### Q19: "Mengapa 5-Fold, bukan 10-Fold?"
> "Keseimbangan bias-variansi optimal dan efisien pada laptop 8 GB. Setiap fold: 80% latih, 20% validasi."

### Q20: "Bagaimana menangani kolom tanggal?"
> "Data Wrangler mengekstrak fitur turunan (hari, bulan, tahun). String mentahnya dibuang untuk mencegah ledakan kardinalitas."

### Q21: "Bagaimana jika kategori baru muncul di data uji?"
> "`OneHotEncoder(handle_unknown='ignore')`. Kategori asing diisi nol pada semua kolom dummy tanpa crash."

### Q22: "Bukti tidak ada silent failure?"
> "Penanganan eksepsi eksplisit di setiap modul. Data rusak = `ValueError` atau `SystemExit` transparan. Kriteria 5 dan 8 mewajibkan ini."

### Q23: "Bagaimana memverifikasi tidak overfit?"
> "Model Guardian menghitung Overfit Gap = |skor latih - skor validasi|. Gap di atas 0.10 = peringatan. Titanic champion: gap hanya 0.0036."

### Q24: "Apa itu Permutation Canary Test?"
> "Mengacak label target 100%. Jika skor anjlok ke ~0.50, model belajar dari sinyal. Jika tetap tinggi, ada kebocoran."

### Q25: "Kontribusi terbesar proyek ini?"
> "Membuktikan bahwa otomasi ML dengan AI generatif tidak harus mengorbankan integritas metodologi sains data."

### Q26: "Bagaimana state.json menjamin konsistensi?"
> "SharedState adalah Python dataclass. Serialisasi via `json.dump(asdict(self))`. Setiap agen menulis ke atribut spesifiknya."

### Q27: "Perbedaan SHADOW dengan H2O AutoML?"
> "H2O adalah kotak hitam yang memilih model tanpa penjelasan. SHADOW menerapkan Occam's Razor, audit trail, dan notebook reproducible."

### Q28: "Bagaimana jika API key salah?"
> "`ValueError` eksplisit: 'GEMINI_API_KEY tidak ditemukan!' dengan instruksi jelas untuk mendapatkan kunci."

### Q29: "Bisa dipakai untuk data sensitif?"
> "Ya, data diproses 100% lokal. API LLM hanya menerima ringkasan metadata, bukan data mentah."

### Q30: "Bagaimana menjamin seed reproducibility?"
> "`random_state=42` diterapkan konsisten di `train_test_split`, `StratifiedKFold`, dan semua model kandidat."

### Q31: "Mengapa max_categories=25 pada OneHotEncoder?"
> "Mencegah ledakan dimensi kolom dummy pada fitur kategorikal dengan kardinalitas sangat tinggi."

### Q32: "Bedanya RobustScaler dan StandardScaler?"
> "StandardScaler: mean dan std, rentan outlier. RobustScaler: median dan IQR, kebal outlier."

### Q33: "Bagaimana menangani dataset besar di atas 50.000 baris?"
> "Scope proyek membatasi hingga ~50.000 baris. Untuk data lebih besar, disarankan subsampling representatif."

### Q34: "Mengapa model.joblib, bukan pickle?"
> "Joblib lebih efisien untuk objek NumPy/Scikit-Learn besar, mendukung kompresi, dan lebih aman."

### Q35: "Bagaimana menangani multiclass?"
> "StratifiedKFold menjaga proporsi setiap kelas. Logistic Regression otomatis menggunakan one-vs-rest."

### Q36: "Apa itu ColumnTransformer?"
> "Wadah Scikit-Learn yang menerapkan transformasi berbeda untuk kolom berbeda (numerik vs kategorikal) dalam satu objek. Menjamin fit-in-fold konsisten."

### Q37: "Limitasi yang Anda akui?"
> "Belum mendukung time series, NLP, gambar, clustering. Korelasi hanya linier (Pearson). Belum ada hyperparameter tuning otomatis massal."

### Q38: "Bagaimana jika LLM mengarang angka dalam narasi?"
> "Agen 4 mengekstrak angka dari `state.json` dan memasukkannya ke template. LLM mengisi narasi kualitatif di sekitar angka yang sudah dikunci."

### Q39: "Mengapa log forensik penting?"
> "Untuk audit trail: kapan LLM dipanggil, berapa lama, apa promptnya, apa responsnya. Penguji bisa memverifikasi bahwa agen benar-benar bekerja."

### Q40: "Jika diminta demo langsung, apa langkahnya?"
> "1. Buka terminal. 2. Jalankan `python main.py train data/titanic.csv`. 3. Tunggu ~25 detik. 4. Buka `outputs/run_*/notebook.ipynb`. 5. Tunjukkan grafik dan metrik."

---

# BAGIAN 10: CHEATSHEET EKSEKUSI TERMINAL

## 10.1 Tombol Pintas Presentasi (`slides.html`)

Buka berkas `slides.html` langsung di peramban web (Chrome / Edge / Firefox):

| Tombol | Fungsi |
| :--- | :--- |
| `F` | Masuk / Keluar Layar Penuh (*Fullscreen*) |
| `Panah Kanan` / `Spasi` | Maju ke Slide Berikutnya |
| `Panah Kiri` | Mundur ke Slide Sebelumnya |
| `N` atau `P` | Membuka Laci Catatan Pembicara (*Speaker Notes*) |
| `L` | Mengaktifkan / Mematikan Virtual Laser Pointer Merah |
| `S` | Menjeda / Melanjutkan Stopwatch Presentasi |
| `T` | Membuka Daftar Isi 34 Slide untuk lompatan cepat |
| `Klik Angka Slide di Footer` | Membuka jendela masukan nomor slide |
| `Ctrl + P` | Mencetak seluruh 34 slide menjadi PDF |

---

## 10.2 Perintah Terminal Cepat

### 1. Dashboard Streamlit Arena
```powershell
streamlit run app.py
```
Buka peramban di: `http://localhost:8501`

### 2. Demo Aljabar Spektral
```powershell
python scripts/demo_gram_matrix_vif.py
```
Membuktikan bagaimana korelasi memicu angka kondisi 23 juta dan Ridge L2 menekannya kembali ke 421.

### 3. Pelatihan Pipeline 5 Agen
```powershell
python main.py train data/titanic.csv
python main.py train data/insurance.csv
python main.py train data/telco_churn.csv
```

### 4. Prediksi Data Baru (DoD 8)
```powershell
python main.py predict --run outputs/run_titanic --input '{"Pclass": 3, "Sex": "male", "Age": 22, "SibSp": 1, "Parch": 0, "Fare": 7.25, "Embarked": "S"}'

python main.py predict --run outputs/run_insurance --input '{"age": 35, "sex": "female", "bmi": 26.5, "children": 2, "smoker": "no", "region": "southwest"}'
```

### 5. Verifikasi Pytest
```powershell
pytest -v tests
pytest -v tests backend/tests
```

---

# BAGIAN 11: GLOSARIUM LENGKAP 110 ISTILAH

| No | Istilah | Definisi Sederhana |
| :---: | :--- | :--- |
| 1 | **Accuracy (Akurasi)** | Persentase tebakan yang benar dari seluruh tebakan. Rumus: (TP+TN)/(TP+TN+FP+FN) |
| 2 | **Agent (Agen)** | Entitas AI yang memiliki peran khusus dalam sistem multi-agen |
| 3 | **API** | Jembatan komunikasi antar-program komputer |
| 4 | **API Key** | Kunci akses rahasia untuk menggunakan layanan AI (seperti password) |
| 5 | **Argparse** | Modul Python bawaan untuk membaca perintah dari terminal |
| 6 | **Artefak** | File hasil keluaran sistem (model, notebook, grafik, laporan) |
| 7 | **AUC** | Area Under Curve. Luas area di bawah kurva. Semakin besar semakin bagus |
| 8 | **Backoff** | Menunggu lebih lama setiap kali gagal, lalu mencoba lagi |
| 9 | **Baseline** | Patokan dasar yang harus dikalahkan model yang lebih canggih |
| 10 | **Binary Classification** | Tugas menebak antara dua kemungkinan (Ya/Tidak, Selamat/Tidak) |
| 11 | **Blackboard Pattern** | Pola arsitektur di mana agen berbagi satu papan tulis bersama |
| 12 | **Brier Score** | Skor mengukur seberapa jujur probabilitas ramalan model (0=sempurna) |
| 13 | **CLI** | Command Line Interface. Antarmuka berbasis teks / terminal |
| 14 | **ColumnTransformer** | Wadah Scikit-Learn untuk transformasi berbeda per jenis kolom |
| 15 | **Condition Number** | Rasio nilai eigen terbesar/terkecil. Mengukur kestabilan matriks |
| 16 | **Confusion Matrix** | Tabel 2x2 yang menunjukkan tebakan benar vs salah |
| 17 | **Correlation (Korelasi)** | Ukuran seberapa erat hubungan dua variabel (-1 sampai +1) |
| 18 | **Cross-Validation (CV)** | Teknik menguji model berulang pada lipatan data yang berbeda |
| 19 | **CSV** | Comma-Separated Values. Format file tabel sederhana |
| 20 | **Dataclass** | Fitur Python untuk membuat kelas data terstruktur secara ringkas |
| 21 | **Deterministic** | Selalu menghasilkan output sama untuk input yang sama |
| 22 | **Dummy** | Model paling bodoh: selalu menebak mayoritas/rata-rata |
| 23 | **Eigenvalue (Nilai Eigen)** | Angka yang menunjukkan kekuatan sebuah arah dalam ruang vektor |
| 24 | **F1-Score** | Rata-rata harmonis Presisi dan Recall. Adil untuk data timpang |
| 25 | **Fallback** | Rencana cadangan jika rencana utama gagal |
| 26 | **False Negative (FN)** | Diprediksi negatif padahal sebenarnya positif (luput) |
| 27 | **False Positive (FP)** | Diprediksi positif padahal sebenarnya negatif (alarm palsu) |
| 28 | **Feature (Fitur)** | Kolom input yang digunakan model untuk membuat prediksi |
| 29 | **Feature Engineering** | Membuat kolom fitur baru dari kolom yang sudah ada |
| 30 | **Feature Importance** | Peringkat seberapa berpengaruh setiap fitur terhadap prediksi |
| 31 | **Fit** | Proses menghitung parameter dari data (belajar) |
| 32 | **Fit-in-Fold** | Menghitung parameter HANYA dari data latih di setiap lipatan |
| 33 | **Float** | Angka desimal (misalnya 3.14, 0.001) |
| 34 | **Fold (Lipatan)** | Satu bagian dari data dalam validasi silang |
| 35 | **Forensik** | Pencatatan bukti yang sangat detail untuk audit |
| 36 | **Gemini** | Model bahasa besar buatan Google |
| 37 | **Gradient Boosting** | Model yang membangun pohon keputusan secara bertahap |
| 38 | **Halusinasi** | Ketika AI mengarang informasi yang tidak benar |
| 39 | **Headless Execution** | Menjalankan program tanpa tampilan layar (di latar belakang) |
| 40 | **Holdout** | Bagian data yang disimpan terpisah untuk evaluasi akhir |
| 41 | **Hyperparameter** | Pengaturan model yang ditentukan sebelum pelatihan |
| 42 | **Imputation (Imputasi)** | Mengisi nilai kosong dengan perkiraan (median, modus) |
| 43 | **IQR** | Interquartile Range. Rentang antara kuartil 25% dan 75% |
| 44 | **Joblib** | Pustaka Python untuk menyimpan objek Scikit-Learn ke file |
| 45 | **JSON** | Format data terstruktur yang mudah dibaca manusia dan mesin |
| 46 | **JSONL** | JSON Lines: satu objek JSON per baris untuk log |
| 47 | **Jupyter Notebook** | Buku catatan kode interaktif populer di sains data |
| 48 | **Kernel** | Mesin penerjemah kode di balik layar Jupyter Notebook |
| 49 | **L2 Regularization** | Menambahkan penalti pada besarnya bobot untuk stabilisasi model |
| 50 | **Label** | Jawaban yang benar (target) yang ingin diprediksi model |
| 51 | **Latency (Latensi)** | Waktu tunggu dari kirim permintaan hingga terima jawaban |
| 52 | **Leakage** | Kebocoran informasi masa depan ke data latih (curang!) |
| 53 | **LLM** | Large Language Model. Model AI besar yang bisa memahami teks |
| 54 | **MAE** | Mean Absolute Error. Rata-rata selisih absolut prediksi vs kenyataan |
| 55 | **Matriks Gram** | X^T * X yang harus dibalik untuk menemukan bobot OLS |
| 56 | **Median** | Nilai tengah jika data diurutkan. Kebal terhadap outlier |
| 57 | **Missing Values** | Data yang kosong / tidak terisi pada beberapa baris |
| 58 | **Mock** | Tiruan/palsu yang digunakan untuk pengujian tanpa koneksi asli |
| 59 | **Modus** | Nilai yang paling sering muncul dalam data |
| 60 | **Multiclass** | Menebak antara 3+ kemungkinan (Rendah/Sedang/Tinggi) |
| 61 | **Multikolinearitas** | Dua fitur sangat mirip sehingga mengganggu kestabilan model |
| 62 | **Nbclient** | Pustaka Python untuk menjalankan notebook secara headless |
| 63 | **Nbformat** | Pustaka Python untuk membuat/membaca file notebook (.ipynb) |
| 64 | **Notebook (.ipynb)** | File Jupyter Notebook berisi sel kode dan penjelasan |
| 65 | **NumPy** | Pustaka Python untuk komputasi array numerik cepat |
| 66 | **Occam's Razor** | Prinsip: pilih solusi paling sederhana yang cukup baik |
| 67 | **OLS** | Ordinary Least Squares. Metode regresi klasik |
| 68 | **OneHotEncoder** | Mengubah kategori teks menjadi kolom biner 0/1 |
| 69 | **Outlier** | Nilai ekstrem yang jauh dari rata-rata data |
| 70 | **Overfitting** | Model terlalu menghafal data latih, gagal di data baru |
| 71 | **Overfit Gap** | Selisih skor latih vs skor validasi. Gap besar = overfit |
| 72 | **P-value** | Probabilitas hasil terjadi secara kebetulan. Di bawah 0.05 = signifikan |
| 73 | **Pandas** | Pustaka Python untuk manipulasi data tabular (DataFrame) |
| 74 | **Pearson Correlation** | Ukuran hubungan linier antara dua variabel numerik |
| 75 | **Pipeline** | Rangkaian langkah berurutan dalam satu wadah Scikit-Learn |
| 76 | **PR-AUC** | Precision-Recall AUC. Lebih adil dari ROC-AUC pada data timpang |
| 77 | **Precision (Presisi)** | Dari yang diprediksi positif, berapa banyak yang benar? |
| 78 | **Predict** | Menggunakan model terlatih untuk menebak data baru |
| 79 | **Preprocessing** | Tahap membersihkan dan menyiapkan data sebelum pemodelan |
| 80 | **Pytest** | Kerangka kerja pengujian otomatis untuk Python |
| 81 | **R2 (R-Squared)** | Persentase variasi data yang berhasil dijelaskan model (0 sampai 1) |
| 82 | **Random Forest** | Kumpulan ratusan pohon keputusan yang saling melengkapi |
| 83 | **Random State** | Angka benih acak untuk memastikan hasil bisa diulang |
| 84 | **Recall** | Dari yang benar-benar positif, berapa banyak yang tertangkap? |
| 85 | **Regression (Regresi)** | Tugas memprediksi angka kontinu (harga, suhu, biaya) |
| 86 | **Reproducibility** | Kemampuan untuk mengulang eksperimen dengan hasil yang sama |
| 87 | **Retry** | Mencoba ulang jika percobaan pertama gagal |
| 88 | **Ridge Regression** | Regresi linier dengan penalti L2 untuk stabilisasi |
| 89 | **RMSE** | Root Mean Squared Error. Rata-rata kuadratik kesalahan |
| 90 | **ROC-AUC** | Luas area di bawah kurva ROC. Mengukur daya pisah model |
| 91 | **RobustScaler** | Penskalaan berdasarkan median dan IQR, kebal outlier |
| 92 | **Scikit-Learn** | Pustaka Python utama untuk machine learning klasik |
| 93 | **Schema** | Kontrak format data: kolom wajib, tipe data, rentang nilai |
| 94 | **Sealed Holdout** | Data uji yang disegel dan tidak boleh disentuh saat latihan |
| 95 | **Serialization** | Menyimpan objek program ke dalam file (joblib, JSON) |
| 96 | **SharedState** | Objek memori bersama di SHADOW (papan tulis digital) |
| 97 | **SSOT** | Single Source of Truth. Satu sumber kebenaran tunggal |
| 98 | **StandardScaler** | Penskalaan berdasarkan mean dan std. Rentan outlier |
| 99 | **Stratified Split** | Membagi data dengan mempertahankan proporsi kelas |
| 100 | **Streamlit** | Framework Python untuk membuat dashboard web interaktif |
| 101 | **Target** | Kolom yang ingin diprediksi oleh model (variabel dependen) |
| 102 | **Token** | Unit teks terkecil yang diproses LLM (~0.75 kata) |
| 103 | **Transform** | Menerapkan transformasi yang sudah dipelajari ke data baru |
| 104 | **True Negative (TN)** | Diprediksi negatif, dan memang benar negatif |
| 105 | **True Positive (TP)** | Diprediksi positif, dan memang benar positif |
| 106 | **Underfitting** | Model terlalu sederhana, tidak mampu menangkap pola data |
| 107 | **Unseen Data** | Data yang belum pernah dilihat model saat pelatihan |
| 108 | **Validation** | Menguji model pada sebagian data latih untuk memilih yang terbaik |
| 109 | **Variance (Variansi)** | Ukuran sebaran data dari rata-ratanya |
| 110 | **VIF** | Variance Inflation Factor. Mengukur multikolinearitas suatu fitur |

---

# BAGIAN 12: PANDUAN INSTALASI DAN SETUP DARI NOL

## 12.1 Prasyarat Sistem

| Komponen | Minimum | Rekomendasi |
| :--- | :--- | :--- |
| Sistem Operasi | Windows 10 / macOS 12 / Ubuntu 20.04 | Windows 11 / macOS 14 |
| RAM | 8 GB | 16 GB |
| Python | 3.11 | 3.12+ |
| Penyimpanan | 500 MB kosong | 2 GB kosong |
| Internet | Diperlukan untuk API Gemini | Koneksi stabil |

## 12.2 Langkah Instalasi (Step-by-Step)

### Langkah 1: Siapkan Python Virtual Environment

```powershell
# Masuk ke folder proyek
cd path\ke\ml-agents

# Buat virtual environment
python -m venv .venv

# Aktifkan (Windows PowerShell)
.venv\Scripts\activate

# Aktifkan (macOS / Linux)
source .venv/bin/activate
```

### Langkah 2: Instal Dependensi

```powershell
pip install -r requirements.txt
```

### Langkah 3: Konfigurasi API Key Gemini

1. Buka https://aistudio.google.com/ dan login dengan akun Google.
2. Klik "Get API Key" dan salin kunci yang muncul.
3. Buat file `.env` di folder proyek:

```
GEMINI_API_KEY=AIzaSy-kunci-anda-di-sini
GEMINI_MODEL=gemini-3.1-flash-lite
```

### Langkah 4: Uji Instalasi

```powershell
# Jalankan test suite
pytest -v tests

# Jika semua PASSED, instalasi berhasil!

# Coba training pertama
python main.py train data/titanic.csv
```

### Langkah 5: Buka Dashboard (Opsional)

```powershell
streamlit run app.py
# Buka browser: http://localhost:8501
```

---

# BAGIAN 13: BEDAH KODE BARIS DEMI BARIS (DEEP DIVE)

## 13.1 Bedah `core/state.py` -- Papan Tulis Digital (90 baris)

```python
@dataclass
class SharedState:
    run_id: str           # ID unik sesi, contoh: "run_20261022_072700"
    csv_path: str         # Path absolut ke file CSV input

    # Profil statistik dari profiling.py:
    dataset_info: Dict = {}

    # Keputusan Agen 1 (target, task_type, metric):
    framing: Dict = {}

    # Rencana dan eksekusi pembersihan dari Agen 2:
    data_plan: Dict = {}
    data_execution: Dict = {}

    # Strategi dan hasil evaluasi dari Agen 3:
    modeling_plan: Dict = {}
    modeling_results: Dict = {}

    # Narasi dan grafik dari Agen 4:
    insights: Dict = {}
    figures: List[str] = []

    # Status notebook dari Agen 5:
    notebook_info: Dict = {}

    # Log setiap giliran bicara agen:
    debate_transcripts: List = []

    # Path ke artefak produksi:
    model_path: str = ""
    schema_path: str = ""
```

**Mengapa dataclass?** Karena Python dataclass secara otomatis membuat `__init__`, `__repr__`, dan mendukung `asdict()` untuk serialisasi JSON. Tidak perlu menulis kode boilerplate!

## 13.2 Bedah `core/llm.py` -- Gateway Gemini Aman (298 baris)

**Mekanisme Pertahanan Berlapis:**

```
Pemanggilan LLM
    |
    v
1. Coba model utama (gemini-3.1-flash-lite)
   |-- Sukses? --> Lanjut validasi JSON
   |-- Error 429/503? --> Tunggu 2*retry detik, coba lagi (max 3x)
   |-- Error 404? --> Coba model cadangan berikutnya
   |
2. Coba model cadangan 1 (gemini-3.5-flash-lite)
   |-- (proses yang sama)
   |
3. Coba model cadangan 2 (gemini-3.8-flash)
   |-- (proses yang sama)
   |
4. Semua gagal? --> RuntimeError transparan!

Validasi JSON:
    |
    v
1. Bersihkan markdown (```json ... ```)
2. Coba json.loads()
   |-- Sukses? --> Return dict
   |-- Gagal? --> Tambah instruksi koreksi ke prompt
   |          --> Ulangi pemanggilan (max 2x)
   |
3. Tetap gagal? --> ValueError transparan!
```

## 13.3 Bedah `core/tools/modeling.py` -- Jantung Evaluasi (391 baris)

Fungsi terpenting: `evaluate_cross_validation()`

```python
for name, model_instance in models.items():
    # Bungkus preprocessor + model dalam Pipeline Scikit-Learn
    pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),  # ColumnTransformer
        ("model", model_instance)        # Kandidat model
    ])
    # Pipeline MENJAMIN fit-in-fold:
    # Saat cross_val_score(), Pipeline otomatis memanggil
    # preprocessor.fit_transform() HANYA pada data latih per fold,
    # dan preprocessor.transform() pada data validasi per fold.
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=scoring)
```

**Mengapa Pipeline penting?** Tanpa Pipeline, `fit_transform` pada preprocessor bisa bocor! Pipeline memastikan `fit` dan `transform` selalu terpisah di setiap lipatan CV secara otomatis.

---

# BAGIAN 14: ALUR DATA END-TO-END (STEP-BY-STEP TRACE)

Berikut adalah perjalanan lengkap data dari CSV mentah hingga prediksi siap pakai:

```
LANGKAH 1: PENGGUNA
  +-- Mengetik: python main.py train data/titanic.csv
       |
LANGKAH 2: main.py (Pengendali Utama)
  +-- Membaca CSV via profiling.load_and_clean_raw_df()
  +-- Membuat SharedState kosong
  +-- Membuat GeminiClient (membaca .env, siapkan log)
  |
LANGKAH 3: TAHAP 1 -- FRAMING (Agen 1)
  +-- profiling.profile_dataset() --> ringkasan statistik
  +-- framing_agent memanggil LLM dengan ringkasan
  +-- LLM mengembalikan JSON: {target, task_type, metric}
  +-- Python MEMVALIDASI: target benar-benar ada di kolom!
  +-- Tulis ke state.framing
  |
LANGKAH 4: TAHAP 2 -- DATA CLEANING (Agen 2)
  +-- profiling mendeteksi kolom ID (keunikan > 95%)
  +-- profiling menghitung korelasi --> deteksi leakage (|r| >= 0.85)
  +-- Kolom bocor dan ID di-drop
  +-- cleaning.build_preprocessor_pipeline() --> ColumnTransformer
  +-- modeling.split_train_test() --> 80% train, 20% test DISEGEL
  +-- Tulis ke state.data_plan, state.data_execution
  |
LANGKAH 5: TAHAP 3 -- MODELING (Agen 3)
  +-- Latih 4 model pada data train (via 5-Fold CV)
  +-- Hitung overfit gap per model
  +-- Jalankan Permutation Canary Test
  +-- Jalankan Nadeau-Bengio t-test
  +-- LLM memilih champion (berdasarkan Occam's Razor)
  +-- Python MEMVALIDASI pilihan LLM
  +-- Fit champion pada FULL train, evaluasi holdout SATU KALI
  +-- Hitung: accuracy, F1, ROC-AUC, Brier, confusion matrix
  +-- Tulis ke state.modeling_results
  |
LANGKAH 6: TAHAP 4 -- STORYTELLING (Agen 4)
  +-- Ekstrak bobot fitur dari pipeline Scikit-Learn
  +-- Gambar 4 grafik PNG (150 DPI) via matplotlib
  +-- LLM menulis narasi berdasarkan angka Python
  +-- Simpan report.md dan figures/*.png
  +-- Tulis ke state.insights, state.figures
  |
LANGKAH 7: TAHAP 5 -- NOTEBOOK DAN EKSPOR (Agen 5)
  +-- Susun 11 sel kode via nbformat
  +-- Eksekusi headless via nbclient (timeout 300s)
  +-- Verifikasi: metrik notebook == metrik state.json (toleransi 0.001)
  +-- Simpan model.joblib dan schema.json
  +-- Simpan notebook.ipynb
  +-- Tulis ke state.notebook_info, state.model_path
  |
LANGKAH 8: SELESAI!
  +-- state.save_to_file() --> outputs/run_*/state.json
  +-- Cetak ringkasan ke terminal
```

---

# BAGIAN 15: PERBANDINGAN SHADOW VS SISTEM LAIN

| Aspek | **SHADOW** | **AutoGen** | **CrewAI** | **H2O AutoML** | **ChatGPT Code** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pola Agen** | Sekuensial Blackboard | Critique Loop | Role-Play Loop | Non-agen | Single agen |
| **Kontrol Halusinasi** | Pemisahan mutlak LLM/Python | Tidak dijamin | Tidak dijamin | N/A | Minimal |
| **Anti-Leakage** | Scan otomatis |r| >= 0.85 | Manual | Manual | Terbatas | Manual |
| **Reproduktibilitas** | Notebook + nbclient replay | Tidak dijamin | Tidak dijamin | Log terbatas | Tidak bisa replay |
| **Audit Trail** | llm_log.jsonl forensik | Log informal | Log informal | Log berbayar | Tidak ada |
| **Privasi Data** | 100% lokal | Kirim ke cloud | Kirim ke cloud | Kirim ke cloud | Kirim ke cloud |
| **Biaya Token** | ~5 pemanggilan | Puluhan/ratusan | Puluhan | 0 (non-LLM) | Tak terbatas |
| **Occam's Razor** | Otomatis | Tidak | Tidak | Model voting | Tidak |
| **Fit-in-Fold** | Dijamin via Pipeline | Tergantung kode | Tergantung kode | Ya | Tidak dijamin |
| **Keluaran** | model + notebook + report | Kode mentah | Kode mentah | Model saja | Kode mentah |

**Kesimpulan**: SHADOW unggul dalam **integritas sains data** dan **auditabilitas** dibanding framework multi-agen lain yang lebih fokus pada fleksibilitas agen.

---

# BAGIAN 16: PANDUAN PRESENTER PROFESIONAL

## 16.1 Persiapan Malam Sebelumnya

1. **Pasang Charger Laptop** -- Jangan sampai mati di tengah demo!
2. **Buka `slides.html` di browser** -- Tekan `F` untuk fullscreen.
3. **Jalankan semua 3 benchmark** -- Pastikan folder `outputs/` terisi:
   ```powershell
   python main.py train data/titanic.csv
   python main.py train data/insurance.csv
   python main.py train data/telco_churn.csv
   ```
4. **Jalankan pytest** -- Pastikan 24/24 PASSED.
5. **Baca Bagian 9** -- Hafalkan jawaban 10 pertanyaan pertama.
6. **Siapkan terminal terbuka** -- Untuk demo langsung jika diminta.
7. **Pastikan `.env` berisi API key yang valid** -- Test dengan perintah cepat.

## 16.2 Timeline Presentasi (20 Menit)

| Menit | Slide | Aktivitas |
| :---: | :---: | :--- |
| 0:00 - 1:00 | 1-2 | Pembukaan dan Ringkasan Eksekutif |
| 1:00 - 3:00 | 3-5 | Masalah, Metodologi, Ruang Lingkup |
| 3:00 - 6:00 | 6-13 | Arsitektur 5 Agen dan Proteksi Data |
| 6:00 - 8:00 | 14-15 | Matematika Spektral (puncak akademis) |
| 8:00 - 11:00 | 16-21 | Modeling, Storytelling, Notebook |
| 11:00 - 14:00 | 22-27 | Bukti Empiris 3 Dataset dan Produksi |
| 14:00 - 16:00 | 28-33 | Bedah Kode, Pytest, Streamlit |
| 16:00 - 18:00 | 34 | Kesimpulan dan Undangan Demo Langsung |
| 18:00 - 20:00+ | - | Tanya Jawab (gunakan Bagian 9!) |

## 16.3 Tips Bahasa Tubuh

| Situasi | Tips |
| :--- | :--- |
| **Pembukaan** | Berdiri tegak, tangan terbuka, tatap seluruh penguji. Senyum hangat. |
| **Menjelaskan rumus** | Tempo PELAN, artikulasi JELAS, tunjuk rumus di layar satu per satu |
| **Menunjukkan hasil** | Tunjuk angka hijau dengan laser pointer (tombol L), senyum bangga |
| **Menjawab pertanyaan sulit** | Anggukkan kepala, ulangi pertanyaan, jawab terstruktur (3 poin) |
| **Tidak tahu jawaban** | Jangan panik! Gunakan kalimat penyelamat (lihat 16.4) |
| **Penutupan** | Buka kedua telapak tangan ke arah penguji, ucapkan terima kasih |

## 16.4 Kalimat Penyelamat Saat Tidak Tahu Jawaban

> "Pertanyaan yang sangat baik, Bapak/Ibu. Dalam batasan scope proyek ini, kami belum mengeksplorasi aspek tersebut secara mendalam. Namun secara konseptual, pendekatan yang bisa diambil adalah [berikan hipotesis umum]. Kami dengan senang hati akan mendalami topik ini sebagai pengembangan lanjutan."

## 16.5 Checklist Terakhir Sebelum Naik Panggung

- [ ] Laptop terisi penuh / charger terpasang
- [ ] `slides.html` sudah dibuka di browser, mode fullscreen
- [ ] Terminal terbuka siap demo
- [ ] Folder `outputs/` berisi 3 artefak benchmark
- [ ] Pytest 24/24 PASSED
- [ ] File `.env` berisi API key yang valid
- [ ] Air minum tersedia di podium
- [ ] Buku Master ini sudah dibaca minimal Bagian 5, 9, dan 16
- [ ] Tarik napas dalam-dalam, tersenyum, dan percaya diri!

---

> **Pernyataan Penutup**: Dokumen Buku Master ini adalah satu-satunya sumber kebenaran tunggal (*Single Source of Truth*) yang mengintegrasikan seluruh naskah lisan, monograf matematika, rekayasa software, glosarium istilah, panduan instalasi, perbandingan sistem, dan bukti pengujian sistem SHADOW-ML.
>
> Totalnya mencakup **16 Bagian**, **40 Pertanyaan Sidang**, **110 Istilah Glosarium**, dan **panduan presenter profesional**.
>
> **Selamat maju sidang dan raih hasil terbaik!**
>
> *"Build what the PRD specifies. Test what is built. Verify what is claimed. Report what the evidence supports."*
