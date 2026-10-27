import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from backend.app.config import settings
from backend.app.services.validators import validate_dialogue

logger = logging.getLogger("shadow_arena.llm")

# Circuit breaker flag jika kuota habis atau API key invalid
_quota_exhausted: bool = False
_exhaustion_reason: str = ""


class LLMDialogueOutput(BaseModel):
    title: str = Field(description="Judul babak singkat maksimal 28 karakter")
    mood: str = Field(description="Emosi agen: calm, angry, shock, atau happy")
    dialog: str = Field(description="Teks dialog agen maksimal 190 karakter dalam bahasa Indonesia")


def is_llm_available() -> bool:
    if settings.is_offline or _quota_exhausted:
        return False
    return True


def get_llm_status() -> Tuple[bool, Optional[str]]:
    if settings.is_offline:
        return False, "GEMINI_API_KEY tidak disetel di .env; beralih ke mode offline"
    if _quota_exhausted:
        return False, _exhaustion_reason or "Kuota Gemini API habis (429 Resource Exhausted); beralih ke mode offline"
    return True, None


def generate_agent_turn(
    agent_name: str,
    agent_role: str,
    round_title_default: str,
    round_stage: str,
    facts: Dict[str, Any],
    recent_turns: List[Dict[str, str]],
    offline_fallback_fn: Any
) -> Tuple[str, str, str, str]:
    global _quota_exhausted, _exhaustion_reason

    # 1. Cek mode offline atau circuit breaker
    if not is_llm_available():
        title, mood, dialog = offline_fallback_fn()
        return title, mood, dialog, "offline"

    # 2. Coba inisialisasi client Gemini
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.gemini_api_key)
    except Exception as e:
        logger.warning(f"Gagal menginisialisasi Google GenAI client: {str(e)[:100]}. Menggunakan mode offline.")
        title, mood, dialog = offline_fallback_fn()
        return title, mood, dialog, "offline"

    # Ringkasan 2 babak terakhir untuk konteks balas-membalas
    context_str = ""
    if recent_turns:
        context_str = "Konteks 2 babak sebelumnya:\n" + "\n".join([
            f"- {t.get('agent', 'AGEN')}: \"{t.get('dialog', '')}\""
            for t in recent_turns[-2:]
        ])

    facts_summary = "\n".join([f"- {k}: {v}" for k, v in facts.items()])

    prompt = (
        f"Kamu berperan sebagai {agent_name} ({agent_role}) dalam arena debat anime x data science 'Shadow Arena'.\n"
        f"Topik babak: {round_title_default} (Tahap: {round_stage}).\n"
        f"{context_str}\n\n"
        f"FAKTA KOMPUTASI NYATA (HANYA GUNAKAN ANGKA-ANGKA INI JIKA MENYEBUT ANGKA):\n"
        f"{facts_summary}\n\n"
        f"ATURAN KERAS:\n"
        f"1. Dialog maksimal 190 karakter, 1-2 kalimat bernas, bahasa Indonesia bergaya anime ekspresif.\n"
        f"2. Judul (title) maksimal 28 karakter.\n"
        f"3. Mood harus salah satu dari: calm, angry, shock, happy.\n"
        f"4. DILARANG MENGARANG ANGKA! Setiap angka di dialog harus ada persis di FAKTA.\n"
        f"5. Balas atau sambung emosi dari babak sebelumnya."
    )

    max_retries = 2
    current_prompt = prompt

    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=current_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LLMDialogueOutput,
                    temperature=0.7,
                )
            )

            res_text = response.text.strip()
            parsed = json.loads(res_text)
            title = parsed.get("title", round_title_default)[:28]
            mood = parsed.get("mood", "calm")
            if mood not in ("calm", "angry", "shock", "happy"):
                mood = "calm"
            dialog = parsed.get("dialog", "").strip()

            # Validasi panjang dan konsistensi angka
            is_valid, errors = validate_dialogue(title, dialog, facts)
            if is_valid:
                return title, mood, dialog, "llm"

            # Jika gagal validasi, siapkan instruksi retry
            logger.info(f"Percobaan {attempt + 1} validasi gagal: {errors}. Melakukan retry.")
            current_prompt = (
                f"{prompt}\n\n"
                f"PERINGATAN: Percobaan sebelumnya gagal karena: {', '.join(errors)}.\n"
                f"Perbaiki sekarang: panjang dialog WAJIB <= 190 karakter dan HANYA gunakan angka dari fakta di atas!"
            )

        except Exception as e:
            err_msg = str(e)
            logger.warning(f"Gemini API error pada percobaan {attempt + 1}: {err_msg[:120]}")
            if any(k in err_msg for k in ["RESOURCE_EXHAUSTED", "429", "API_KEY_INVALID", "quota", "Quota"]):
                _quota_exhausted = True
                _exhaustion_reason = f"Gemini API: {err_msg[:80]}"
            break

    # Fallback jika semua percobaan gagal
    logger.info("Beralih ke template offline deterministik.")
    title, mood, dialog = offline_fallback_fn()
    return title, mood, dialog, "offline"
