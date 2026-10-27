"""
Layanan Text-to-Speech Studio Neural Manusiawi untuk 5 Agen AI Antigravity.
Menghasilkan suara alami, hangat, artikulatif dengan intonasi manusia nyata:
1. Membersihkan istilah teknis, nama berkas, ekstensi, dan desimal menjadi frasa percakapan alami.
2. Tidak menyisipkan tag XML mentah sehingga suara tidak akan pernah membacakan kode/tag.
3. Modulasi nada (pitch), kecepatan (rate), dan volume disesuaikan dengan peran & emosi agen.
4. Smart caching berbasis hash teks agar selalu sinkron dengan narasi terbaru.
"""

import asyncio
import hashlib
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
from core.llm import load_env_file
load_env_file()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_AUDIO_DIR = BASE_DIR / "static" / "audio"
STATIC_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Parameter Vokal Murni 5 Agen Resmi Antigravity (Intonasi Manusiawi Hangat)
AGENT_VOICE_CONFIG = {
    0: {"voice": "id-ID-ArdiNeural", "rate": "-2%", "pitch": "+0Hz", "volume": "+6%"},   # Data Wrangler (Santai, taktis, jernih)
    1: {"voice": "id-ID-ArdiNeural", "rate": "-3%", "pitch": "-1Hz", "volume": "+8%"},  # Problem Framer (Wibawa arsitektural)
    2: {"voice": "id-ID-ArdiNeural", "rate": "-4%", "pitch": "-2Hz", "volume": "+12%"}, # Model Guardian (Tegas, berwibawa, berat)
    3: {"voice": "id-ID-GadisNeural", "rate": "-3%", "pitch": "+0Hz", "volume": "+8%"}, # Insight Storyteller (Hangat, naratif, empati)
    4: {"voice": "id-ID-GadisNeural", "rate": "-1%", "pitch": "+1Hz", "volume": "+6%"},  # Notebook Builder (Cerdas, tangkas, antusias)
}


def verbalize_number_indonesian(match: re.Match) -> str:
    """Mengubah desimal menjadi pembacaan bahasa Indonesia yang luwes dan alami."""
    val_str = match.group(0)
    try:
        val = float(val_str)
        if 0 < val < 0.01:
            ten_thous = int(round(val * 10000))
            return f"nol koma nol nol {ten_thous}"
        elif 0.01 <= val < 0.05:
            thous = int(round(val * 1000))
            return f"nol koma nol {thous}"
        elif 0.05 <= val < 1.0:
            cents = int(round(val * 100))
            puluhan = ['', 'sepuluh', 'dua puluh', 'tiga puluh', 'empat puluh', 'lima puluh', 'enam puluh', 'tujuh puluh', 'delapan puluh', 'sembilan puluh']
            satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan']
            p = cents // 10
            s = cents % 10
            if cents < 10:
                kata = f"nol {satuan[s]}"
            elif 11 <= cents <= 19:
                belasan = ['', 'sebelas', 'dua belas', 'tiga belas', 'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'delapan belas', 'sembilan belas']
                kata = belasan[cents - 10]
            elif s == 0:
                kata = puluhan[p]
            else:
                kata = f"{puluhan[p]} {satuan[s]}"
            return f"nol koma {kata}"
        elif 1.0 <= val < 10.0:
            cents = int(round((val - int(val)) * 100))
            return f"{int(val)} koma {cents}"
        return val_str
    except Exception:
        return val_str


def humanize_text_for_speech(text: str) -> str:
    """
    Mengubah teks teknis & angka mentah menjadi frasa percakapan manusiawi yang mengalir indah.
    Mencegah mesin membacakan tag XML, underscore, timestamp, nama file, atau desimal rumit.
    """
    if not text:
        return ""

    t = text
    # Hapus bukti audit dan format markdown
    t = re.sub(r"\[BUKTI AUDIT:.*?\]", "", t)
    t = re.sub(r"\[.*?\]\(.*?\)", "", t)
    t = re.sub(r"[*#`~\[\]<>{}]", " ", t)

    # Ganti tanda kurung berisi teks atau angka dengan jeda koma lembut
    t = re.sub(r"\(([\w\s\.,%]+)\)", r", \1, ", t)
    t = t.replace("'", " ").replace('"', " ")

    # Bersihkan nama file panjang, timestamp & ekstensi
    t = re.sub(r"shadow_arena_[\w\-]+_\d{8}_\d{6}\.ipynb", "notebook riset shadow arena", t)
    t = re.sub(r"[\w\-]+_\d{8}_\d{6}\.ipynb", "notebook riset", t)
    t = re.sub(r"[\w\-]+\.ipynb", "notebook riset", t)
    t = re.sub(r"[\w\-]+\.joblib", "model final", t)
    t = re.sub(r"_\d{8}_\d{6}", "", t)

    # Normalisasi simbol matematika & notasi data science
    t = re.sub(r"\|r\|\s*<\s*0\.85", "korelasi di bawah nol koma delapan lima", t)
    t = re.sub(r"\|r\|\s*>\s*0\.85", "korelasi di atas nol koma delapan lima", t)
    t = re.sub(r"\|r\|\s*<\s*0\.95", "korelasi di bawah nol koma sembilan lima", t)
    t = re.sub(r"\|r\|\s*>\s*0\.95", "korelasi di atas nol koma sembilan lima", t)
    t = re.sub(r"\|Train\s*-\s*CV\|", "selisih skor latih dan validasi", t)
    t = re.sub(r"80/20", "delapan puluh berbanding dua puluh", t)
    t = re.sub(r"5-Fold Stratified CV", "lima lipatan stratified cross validation", t, flags=re.IGNORECASE)
    t = re.sub(r"5-Fold", "lima lipatan", t, flags=re.IGNORECASE)
    t = re.sub(r"5-fold", "lima lipatan", t, flags=re.IGNORECASE)
    t = re.sub(r"Stratified CV", "stratified cross validation", t, flags=re.IGNORECASE)
    t = re.sub(r"Cross Validation", "cross validation", t, flags=re.IGNORECASE)
    t = re.sub(r"\bCV\b", "cross validation", t)
    t = re.sub(r"VIF\s*<\s*5\.0", "skor V-I-F di bawah lima", t)
    t = re.sub(r"VIF\s*<\s*2\.8", "skor V-I-F di bawah dua koma delapan", t)
    t = re.sub(r"\bVIF\b", "V I F", t)
    t = re.sub(r"\bROC-AUC\b", "skor A U C", t, flags=re.IGNORECASE)
    t = re.sub(r"\bPR-AUC\b", "skor Precision-Recall", t, flags=re.IGNORECASE)
    t = re.sub(r"\bF1-score\b", "skor F satu", t, flags=re.IGNORECASE)
    t = re.sub(r"\bF1 score\b", "skor F satu", t, flags=re.IGNORECASE)
    t = re.sub(r"\bF1\b", "skor F satu", t)
    t = re.sub(r"\bLogReg\b", "Logistic Regression", t)
    t = re.sub(r"\bRandomForest\b", "Random Forest", t)
    t = re.sub(r"\bHistGradBoost\b", "Histogram Gradient Boosting", t)

    # Normalisasi persentase
    t = re.sub(r"(\d+)%", r"\1 persen", t)

    # Normalisasi nama variabel tabular umum agar tidak dibaca kode mentah
    var_replacements = [
        (r"\bPclass\b", "kelas tiket"),
        (r"\bpclass\b", "kelas tiket"),
        (r"\bSibSp\b", "kerabat keluarga"),
        (r"\bsibsp\b", "kerabat keluarga"),
        (r"\bParch\b", "orang tua dan anak"),
        (r"\bparch\b", "orang tua dan anak"),
        (r"\bEmbarked\b", "pelabuhan keberangkatan"),
        (r"\bembarked\b", "pelabuhan keberangkatan"),
        (r"\bFare\b", "tarif tiket"),
        (r"\bfare\b", "tarif tiket"),
        (r"\bPassengerId\b", "nomor identitas penumpang"),
        (r"\bpassengerid\b", "nomor identitas penumpang"),
    ]
    for pattern, rep in var_replacements:
        t = re.sub(pattern, rep, t)

    # Normalisasi istilah teknis variabel ke bahasa manusia lisan
    direct_replacements = [
        ("n_train", "data latih"),
        ("n_test", "data uji"),
        ("vif_max", "skor VIF"),
        ("leakage_corr_max", "korelasi kebocoran"),
        ("P-value", "nilai P"),
        ("p-value", "nilai P"),
        ("Brier score", "skor Brier"),
        ("overfit gap", "selisih overfit"),
        ("nbclient", "pemeriksaan notebook"),
        ("random seed", "seed acak"),
        ("zip_code", "kode pos"),
        ("drop_columns", "kolom yang dibuang"),
        ("11 cell", "sebelas sel kode"),
    ]
    for k, v in direct_replacements:
        t = t.replace(k, v)

    # Verbalisasi desimal angka nyata
    t = re.sub(r"\b\d+\.\d+\b", verbalize_number_indonesian, t)

    # Ganti underscore dengan spasi
    t = t.replace("_", " ")

    # Hapus spasi ganda
    t = re.sub(r"\s+", " ", t).strip()
    return t


def get_agent_voice_params(agent_id: int, mood: str = "calm") -> Dict[str, str]:
    """Menentukan parameter vokal murni (pitch, rate, volume) berdasarkan peran dan emosi."""
    cfg = AGENT_VOICE_CONFIG.get(agent_id, AGENT_VOICE_CONFIG[0])
    voice = cfg["voice"]
    rate = cfg["rate"]
    pitch = cfg["pitch"]
    volume = cfg["volume"]

    # Modulasi halus berdasarkan emosi babak
    if mood == "angry":
        pitch = "-2Hz"
        volume = "+16%"
    elif mood == "shock":
        pitch = "+2Hz"
        rate = "+1%"
        volume = "+12%"
    elif mood == "happy":
        pitch = "+2Hz"
        volume = "+10%"

    return {"voice": voice, "rate": rate, "pitch": pitch, "volume": volume}


async def synthesize_round_audio(session_id: str, round_idx: int, round_data: Dict[str, Any]) -> Optional[str]:
    """Menghasilkan berkas audio MP3 murni tanpa tag XML atau kode mentah."""
    clean_session = re.sub(r"[^\w\-]", "_", session_id)

    raw_dialog = round_data.get("dialog", "")
    spoken_text = humanize_text_for_speech(raw_dialog)
    if not spoken_text:
        return None

    # Cache cerdas berbasis hash teks
    text_hash = hashlib.md5(spoken_text.encode("utf-8")).hexdigest()[:8]
    out_file = STATIC_AUDIO_DIR / f"{clean_session}_r{round_idx}_{text_hash}.mp3"

    # Jika file dengan hash teks ini sudah ada dan valid (>5KB), langsung gunakan
    if out_file.exists() and out_file.stat().st_size > 5120:
        return f"/app/static/audio/{out_file.name}"

    agent_id = round_data.get("agent", 0)
    if isinstance(agent_id, str):
        map_agents = {"wrangler": 0, "framer": 1, "guardian": 2, "storyteller": 3, "builder": 4}
        agent_id = map_agents.get(agent_id.lower(), 0)

    mood = round_data.get("mood", "calm")
    params = get_agent_voice_params(agent_id, mood=mood)

    try:
        import edge_tts
        comm = edge_tts.Communicate(
            text=spoken_text,
            voice=params["voice"],
            rate=params["rate"],
            pitch=params["pitch"],
            volume=params["volume"]
        )
        await comm.save(str(out_file))
        return f"/app/static/audio/{out_file.name}"
    except Exception as e:
        print(f"[EDGE TTS ERROR]: Babak {round_idx} gagal: {e}")
        return None


def synthesize_round_audio_sync(session_id: str, round_idx: int, round_data: Dict[str, Any]) -> Optional[str]:
    """Pembungkus sinkron untuk menghasilkan audio 1 babak."""
    try:
        loop = asyncio.new_event_loop()
        url = loop.run_until_complete(synthesize_round_audio(session_id, round_idx, round_data))
        loop.close()
        return url
    except Exception as e:
        print(f"[TTS SYNC ERROR]: {e}")
        return None


def sync_session_audio(session_id: str, rounds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Memproses seluruh babak secara paralel cepat dan menyematkan audio_url."""
    if not rounds:
        return rounds

    def process_one(item):
        i, r = item
        url = synthesize_round_audio_sync(session_id, i, r)
        r["audio_url"] = url
        return r

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(process_one, list(enumerate(rounds))))

    return rounds
