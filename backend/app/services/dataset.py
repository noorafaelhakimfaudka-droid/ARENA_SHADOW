import io
from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
import pandas as pd


class DatasetValidationError(ValueError):
    """Raised when CSV validation fails with user-friendly Indonesian message."""
    pass


def load_csv_safely(
    file_source: Union[str, Path, bytes, io.BytesIO],
    max_rows: int = 50000,
    max_size_mb: int = 20
) -> Tuple[pd.DataFrame, str]:
    """
    Memuat file CSV secara aman:
    - Memeriksa batas ukuran file (maks 20 MB).
    - Mendeteksi encoding (utf-8, latin1, cp1252) dan delimiter.
    - Menolak file kosong atau < 30 baris.
    - Melakukan subsampling acak berulang (random_state=42) jika baris > max_rows.
    """
    raw_bytes: bytes
    dataset_name: str = "dataset.csv"

    if isinstance(file_source, (str, Path)):
        path = Path(file_source)
        dataset_name = path.name
        if not path.exists():
            raise DatasetValidationError(f"File '{dataset_name}' tidak ditemukan di server.")
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            raise DatasetValidationError(
                f"Ukuran file ({size_mb:.1f} MB) melebihi batas maksimum {max_size_mb} MB."
            )
        raw_bytes = path.read_bytes()
    elif isinstance(file_source, bytes):
        size_mb = len(file_source) / (1024 * 1024)
        if size_mb > max_size_mb:
            raise DatasetValidationError(
                f"Ukuran file ({size_mb:.1f} MB) melebihi batas maksimum {max_size_mb} MB."
            )
        raw_bytes = file_source
    elif isinstance(file_source, io.BytesIO):
        raw_bytes = file_source.getvalue()
        size_mb = len(raw_bytes) / (1024 * 1024)
        if size_mb > max_size_mb:
            raise DatasetValidationError(
                f"Ukuran file ({size_mb:.1f} MB) melebihi batas maksimum {max_size_mb} MB."
            )
    else:
        raise DatasetValidationError("Format sumber file tidak didukung.")

    if not raw_bytes or len(raw_bytes.strip()) == 0:
        raise DatasetValidationError("File CSV kosong. Silakan unggah file yang berisi data tabular.")

    # Deteksi encoding
    decoded_text: Optional[str] = None
    for enc in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            decoded_text = raw_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue

    if decoded_text is None:
        raise DatasetValidationError("Gagal membaca encoding file. Pastikan file berformat UTF-8 atau teks standar.")

    # Deteksi delimiter sederhana
    first_lines = [line for line in decoded_text.splitlines()[:5] if line.strip()]
    if not first_lines:
        raise DatasetValidationError("File CSV tidak memiliki baris data yang valid.")

    delimiter = ","
    candidate_delims = [",", ";", "\t", "|"]
    first_line = first_lines[0]
    delim_counts = {d: first_line.count(d) for d in candidate_delims}
    best_delim = max(delim_counts, key=delim_counts.get)
    if delim_counts[best_delim] > 0:
        delimiter = best_delim

    try:
        df = pd.read_csv(io.StringIO(decoded_text), sep=delimiter)
    except Exception as e:
        raise DatasetValidationError(f"Format CSV tidak dapat di-parse: {str(e)}")

    if df.empty or len(df) < 30:
        raise DatasetValidationError(
            f"Dataset terlalu kecil ({len(df)} baris). Minimal 30 baris dibutuhkan untuk train/test split dan cross-validation yang valid."
        )

    # Bersihkan nama kolom dari whitespace
    df.columns = [str(c).strip() for c in df.columns]

    # Subsampling jika melebihi batas maksimum
    if len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=42).reset_index(drop=True)

    return df, dataset_name
