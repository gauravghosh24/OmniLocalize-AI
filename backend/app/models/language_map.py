"""One source of truth for supported languages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageConfig:
    code: str
    name: str
    nllb_code: str
    tts_engine: str
    xtts_language: str | None = None


LANGUAGES: dict[str, LanguageConfig] = {
    "hi": LanguageConfig("hi", "Hindi", "hin_Deva", "indic"),
    "ta": LanguageConfig("ta", "Tamil", "tam_Taml", "indic"),
    "fr": LanguageConfig("fr", "French", "fra_Latn", "xtts", "fr"),
    "de": LanguageConfig("de", "German", "deu_Latn", "xtts", "de"),
}

SUPPORTED_LANGUAGE_CODES = set(LANGUAGES)
SOURCE_NLLB_CODE = "eng_Latn"
