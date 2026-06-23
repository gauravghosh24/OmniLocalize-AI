"""Coqui XTTS-v2 voice generation for French and German."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import torch

from app.config import XTTS_MODEL_ID, XTTS_SPEAKER, XTTS_SPEAKER_WAV


logger = logging.getLogger(__name__)


class XTTSService:
    """Lazy singleton wrapper around Coqui TTS."""
    def __init__(self) -> None:
        self.use_gpu = torch.cuda.is_available()
        self.tts = None

    def load(self) -> None:
        if self.tts is not None:
            return
        if os.getenv("COQUI_TOS_AGREED") != "1":
            raise RuntimeError(
                "French and German audio use Coqui XTTS-v2, which requires accepting the "
                "CPML terms. Review https://coqui.ai/cpml, then set COQUI_TOS_AGREED=1 in "
                "backend/.env and restart the backend."
            )
        try:
            from TTS.api import TTS
        except ImportError as error:
            missing_package = error.name or "a Coqui TTS dependency"
            raise RuntimeError(
                "Coqui TTS could not start because "
                f"'{missing_package}' is missing. Install matching PyTorch and TorchAudio builds, "
                "then restart the backend."
            ) from error
        logger.info("Loading XTTS-v2 on %s", "CUDA" if self.use_gpu else "CPU")
        self.tts = TTS(model_name=XTTS_MODEL_ID, gpu=self.use_gpu)

    def _speaker_kwargs(self) -> dict[str, str]:
        if XTTS_SPEAKER_WAV:
            return {"speaker_wav": XTTS_SPEAKER_WAV}
        if XTTS_SPEAKER:
            return {"speaker": XTTS_SPEAKER}
        speakers = getattr(self.tts, "speakers", None) or []
        if speakers:
            return {"speaker": speakers[0]}
        raise RuntimeError(
            "This XTTS checkpoint requires a speaker. Set XTTS_SPEAKER to a bundled speaker "
            "or XTTS_SPEAKER_WAV to a licensed local reference recording in backend/.env."
        )

    def generate(self, text: str, language: str, output_path: Path) -> None:
        self.load()
        self.tts.tts_to_file(text=text, language=language, file_path=str(output_path), **self._speaker_kwargs())


xtts_service = XTTSService()
