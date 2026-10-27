# ml-agents/core/llm.py
"""
Klien LLM Google Gemini Cloud Terpadu & Teruji.
- Menggunakan model utama: gemini-3.1-flash-lite dengan fallback ke gemini-3.5-flash-lite dan gemini-3.8-flash.
- Mewajibkan output berformat JSON valid via response_mime_type='application/json'.
- Pencatatan otomatis setiap panggilan ke llm_log.jsonl (waktu, agen, prompt, respons).
- Mekanisme retry maksimal 2x bila output JSON tidak valid.
- Gagal Terlihat: Menampilkan pesan error eksplisit jika API Key tidak ada atau koneksi gagal.
"""

from __future__ import annotations
import datetime
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request


def load_env_file(env_path: Optional[Path | str] = None) -> None:
    """Membaca file .env sederhana tanpa ketergantungan library eksternal."""
    if env_path is None:
        # Cari file .env di folder proyek atau direktori induk
        candidates = [
            Path.cwd() / ".env",
            Path(__file__).resolve().parent.parent / ".env",
            Path(__file__).resolve().parent / ".env"
        ]
        for c in candidates:
            if c.exists():
                env_path = c
                break

    if env_path and Path(env_path).exists():
        for line in Path(env_path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v


# Muat environment saat modul diimpor
load_env_file()


class GeminiClient:
    """Klien resmi Google AI Studio (Gemini Flash) dengan jaminan validitas JSON & logging."""

    DEFAULT_MODELS = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        log_file: Optional[Path | str] = None,
        timeout_seconds: int = 25
    ):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
        preferred_model = model_name or os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite").strip()
        
        # Susun urutan model prioritas
        self.models = [preferred_model] + [m for m in self.DEFAULT_MODELS if m != preferred_model]
        self.timeout = timeout_seconds
        self.log_file = Path(log_file) if log_file else Path("outputs") / "llm_log.jsonl"
        self._genai_client = None
        if self.api_key:
            try:
                from google import genai
                self._genai_client = genai.Client(api_key=self.api_key)
            except Exception:
                self._genai_client = None


    def log_interaction(
        self,
        agent_name: str,
        prompt: str,
        response_text: str,
        model_used: str,
        duration_ms: float,
        is_error: bool = False,
        error_msg: str = ""
    ) -> None:
        """Mencatat setiap interaksi agen LLM ke llm_log.jsonl secara terstruktur."""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "agent": agent_name,
                "model": model_used,
                "duration_ms": round(duration_ms, 2),
                "prompt": prompt,
                "response": response_text,
                "is_error": is_error,
                "error_message": error_msg
            }
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            # Jangan sampai logging menggagalkan proses komputasi utama
            print(f"[Peringatan Log] Gagal menulis ke {self.log_file}: {e}")

    def call_gemini_raw(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = "gemini-3.1-flash-lite",
        enforce_json: bool = True,
        max_output_tokens: int = 8192
    ) -> str:
        """Mengirim HTTP request langsung ke Google AI Studio API."""
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY tidak ditemukan! "
                "Silakan isi file .env dengan: GEMINI_API_KEY=AIzaSy... "
                "Dapatkan kunci gratis di https://aistudio.google.com/"
            )

        if self._genai_client:
            from google.genai import types
            cfg = types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=max_output_tokens,
                response_mime_type="application/json" if enforce_json else "text/plain",
                system_instruction=system_prompt if system_prompt else None
            )
            response = self._genai_client.models.generate_content(
                model=model,
                contents=prompt,
                config=cfg
            )
            return response.text.strip()

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            f"?key={self.api_key}"
        )

        gen_config: Dict[str, Any] = {
            "temperature": 0.2,
            "maxOutputTokens": max_output_tokens,
        }
        if enforce_json:
            gen_config["responseMimeType"] = "application/json"

        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": gen_config
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        body_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=body_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if not candidates:
                raise RuntimeError(f"Gemini API tidak mengembalikan kandidat respons: {data}")
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                raise RuntimeError("Format bagian respons Gemini kosong.")
            return parts[0].get("text", "").strip()

    def generate_json(
        self,
        agent_name: str,
        prompt: str,
        system_prompt: str = "",
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Memanggil Gemini dengan validasi JSON ketat dan mekanisme retry otomatis.
        - Memastikan keluaran berupa dictionary/JSON valid.
        - Jika JSON rusak, meminta ulang dengan menyertakan pesan kesalahan parsing.
        """
        last_error = None
        current_prompt = prompt

        for attempt in range(max_retries + 1):
            t0 = time.time()
            model_used = self.models[0]
            
            # Coba model-model dalam rantai fallback jika terjadi error koneksi
            response_text = ""
            for m in self.models:
                for sub_retry in range(3):
                    try:
                        model_used = m
                        response_text = self.call_gemini_raw(
                            prompt=current_prompt,
                            system_prompt=system_prompt,
                            model=m,
                            enforce_json=True
                        )
                        break
                    except urllib.error.HTTPError as he:
                        last_error = he
                        # Jika server sedang sibuk (503) atau terkena rate limit (429), tunggu dan coba lagi
                        if he.code in (429, 503):
                            time.sleep(2.0 * (sub_retry + 1))
                            continue
                        elif he.code == 404:
                            break  # Model tidak tersedia di akun ini, coba model berikutnya
                        else:
                            raise
                    except Exception as e:
                        last_error = e
                        time.sleep(1.0)
                        continue
                if response_text:
                    break

            duration_ms = (time.time() - t0) * 1000

            if not response_text:
                err_msg = f"Seluruh model Gemini gagal dihubungi. Error terakhir: {last_error}"
                self.log_interaction(
                    agent_name=agent_name,
                    prompt=current_prompt,
                    response_text="",
                    model_used=model_used,
                    duration_ms=duration_ms,
                    is_error=True,
                    error_msg=err_msg
                )
                raise RuntimeError(err_msg)

            # Validasi parsing JSON
            try:
                # Bersihkan markdown formatting ```json ... ``` jika masih ada
                cleaned = response_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()

                parsed_json = json.loads(cleaned)

                # Catat sukses ke log
                self.log_interaction(
                    agent_name=agent_name,
                    prompt=current_prompt,
                    response_text=response_text,
                    model_used=model_used,
                    duration_ms=duration_ms,
                    is_error=False
                )
                return parsed_json

            except json.JSONDecodeError as je:
                last_error = je
                self.log_interaction(
                    agent_name=agent_name,
                    prompt=current_prompt,
                    response_text=response_text,
                    model_used=model_used,
                    duration_ms=duration_ms,
                    is_error=True,
                    error_msg=f"Gagal decode JSON (Percobaan {attempt + 1}): {je}"
                )
                # Tambahkan instruksi koreksi untuk percobaan berikutnya
                current_prompt = (
                    f"{prompt}\n\n"
                    f"[PERINGATAN SISTEM]: Respons sebelumnya tidak dapat di-parse sebagai JSON yang valid: {je}.\n"
                    f"Keluarkan HANYA objek JSON murni tanpa pembuka/penutup markdown atau teks pengantar."
                )

        raise ValueError(
            f"Agen [{agent_name}] gagal menghasilkan JSON yang valid setelah {max_retries + 1} percobaan. "
            f"Error: {last_error}"
        )
