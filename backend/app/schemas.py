"""Pydantic request and response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.models.language_map import SUPPORTED_LANGUAGE_CODES


VoiceStyle = Literal["professional", "friendly", "storytelling", "calm", "energetic"]


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=50_000)
    target_languages: list[str] = Field(min_length=1)

    @field_validator("target_languages")
    @classmethod
    def validate_languages(cls, values: list[str]) -> list[str]:
        values = list(dict.fromkeys(values))
        unsupported = set(values) - SUPPORTED_LANGUAGE_CODES
        if unsupported:
            raise ValueError(f"Unsupported language code(s): {', '.join(sorted(unsupported))}")
        return values


class AudioRequest(BaseModel):
    text: str = Field(min_length=1, max_length=50_000)
    language_code: str
    voice_style: VoiceStyle = "professional"

    @field_validator("language_code")
    @classmethod
    def validate_language(cls, value: str) -> str:
        if value not in SUPPORTED_LANGUAGE_CODES:
            raise ValueError(f"Unsupported language code: {value}")
        return value


class LocalizeRequest(TranslationRequest):
    voice_style: VoiceStyle = "professional"


class TranslationResult(BaseModel):
    language: str
    language_code: str
    translated_text: str


class AudioResult(BaseModel):
    language: str
    language_code: str
    audio_file: str | None = None
    audio_error: str


class LocalizeResult(TranslationResult):
    text_file: str
    audio_file: str | None = None
    audio_error: str


class LocalizeResponse(BaseModel):
    status: Literal["success"]
    results: list[LocalizeResult]
