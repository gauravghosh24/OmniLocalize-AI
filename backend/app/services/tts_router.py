"""Route localized text to the right local text-to-speech engine."""

from __future__ import annotations

from app.models.language_map import LANGUAGES
from app.services.file_manager import audio_path
from app.services.indic_tts_service import indic_tts_service
from app.services.xtts_service import xtts_service


def generate_audio(text: str, language_code: str, voice_style: str) -> str:
    language = LANGUAGES[language_code]
    filename, output_path = audio_path(language_code)
    if language.tts_engine == "indic":
        indic_tts_service.generate(text, language.name, voice_style, output_path)
    elif language.tts_engine == "xtts":
        xtts_service.generate(text, language.xtts_language or language_code, output_path)
    else:
        raise ValueError(f"No TTS engine configured for {language_code}.")
    return filename
