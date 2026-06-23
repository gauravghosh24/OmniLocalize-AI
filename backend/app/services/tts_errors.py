"""Safe, user-actionable errors for optional text-to-speech providers."""

from __future__ import annotations


class TTSAccessError(RuntimeError):
    """Raised when an optional TTS model cannot be accessed safely."""


HF_TOKEN_MISSING = "Hugging Face token missing. Please add HF_TOKEN to backend/.env after accepting model access."
MODEL_ACCESS_NOT_ACCEPTED = "Model access not accepted. Please accept the model terms on Hugging Face and restart the backend."
