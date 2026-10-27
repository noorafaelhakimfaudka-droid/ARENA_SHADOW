import re
from typing import Any, Dict, List, Set, Tuple


def extract_numbers_from_text(text: str) -> List[float]:
    """
    Mengekstrak semua angka dari teks, termasuk persentase dan desimal.
    Contoh: '74%', '0.85', '891', '19.9%' -> [74.0, 0.85, 891.0, 19.9]
    """
    # Regex untuk mencocokkan angka integer atau float, opsional diikuti %
    matches = re.findall(r"(?<![a-zA-Z_])(\d+(?:\.\d+)?)(%?)", text)
    numbers = []
    for num_str, pct_flag in matches:
        val = float(num_str)
        numbers.append(val)
        # Jika diikuti %, simpan juga bentuk fraksi desimalnya (e.g. 74% -> 0.74)
        if pct_flag == "%":
            numbers.append(round(val / 100.0, 4))
    return numbers


def extract_numbers_from_facts(facts: Dict[str, Any]) -> Set[float]:
    """
    Mengekstrak semua angka yang sah dari dictionary facts,
    termasuk versi persentase atau pembulatan.
    """
    valid_numbers: Set[float] = set()

    def _collect(val: Any):
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            v = float(val)
            valid_numbers.add(round(v, 3))
            valid_numbers.add(round(v, 2))
            valid_numbers.add(round(v, 1))
            valid_numbers.add(round(v, 0))
            # Jika desimal 0..1, tambahkan bentuk persentasenya
            if 0.0 <= v <= 1.0:
                pct = v * 100.0
                valid_numbers.add(round(pct, 1))
                valid_numbers.add(round(pct, 0))
        elif isinstance(val, dict):
            for v in val.values():
                _collect(v)
        elif isinstance(val, (list, tuple)):
            for v in val:
                _collect(v)
        elif isinstance(val, str):
            # Jika ada angka di dalam string facts (e.g. '891 baris')
            for n in extract_numbers_from_text(val):
                valid_numbers.add(round(n, 2))
                valid_numbers.add(round(n, 1))
                valid_numbers.add(round(n, 0))

    _collect(facts)
    return valid_numbers


def validate_dialogue(
    title: str,
    dialog: str,
    facts: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Memvalidasi hasil dialog LLM:
    1. Batas panjang: title <= 28 karakter, dialog <= 190 karakter.
    2. Konsistensi angka: semua angka di dialog harus ada di facts (toleransi pembulatan).
    """
    errors: List[str] = []

    if len(title) > 28:
        errors.append(f"Title melebihi batas 28 karakter ({len(title)} karakter).")

    if len(dialog) > 190:
        errors.append(f"Dialog melebihi batas 190 karakter ({len(dialog)} karakter).")

    dialog_numbers = extract_numbers_from_text(dialog)
    facts_numbers = extract_numbers_from_facts(facts)

    for num in dialog_numbers:
        # Cek apakah angka ada di facts_numbers dengan toleransi pembulatan
        matched = False
        rounded_1 = round(num, 1)
        rounded_2 = round(num, 2)
        rounded_0 = round(num, 0)
        
        # Angka kecil standar seperti 1, 2, 3 (e.g. '1-2 kalimat', '3 kelas') diizinkan jika relevan
        if num in (1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 100.0):
            matched = True
        else:
            for valid_num in facts_numbers:
                if (
                    abs(num - valid_num) < 0.02
                    or abs(rounded_1 - valid_num) < 0.02
                    or abs(rounded_2 - valid_num) < 0.02
                    or abs(rounded_0 - valid_num) < 0.5
                ):
                    matched = True
                    break

        if not matched:
            errors.append(f"Angka {num} di dialog tidak ditemukan di facts.")

    return len(errors) == 0, errors
