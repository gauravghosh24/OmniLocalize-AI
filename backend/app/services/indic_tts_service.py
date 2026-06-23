"""Indic Parler-TTS voice generation for Hindi and Tamil."""

from __future__ import annotations

import logging
from pathlib import Path

import soundfile as sf
import torch
from transformers import AutoModel, AutoTokenizer

from app.config import HF_TOKEN, INDIC_PARLER_MODEL_ID, VOICE_STYLES
from app.services.tts_errors import HF_TOKEN_MISSING, MODEL_ACCESS_NOT_ACCEPTED, TTSAccessError


logger = logging.getLogger(__name__)


class IndicParlerService:
    """Lazy wrapper for AI4Bharat's Indic Parler-TTS checkpoint."""
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

    def load(self) -> None:
        if self.model is not None and self.tokenizer is not None:
            return
        if not HF_TOKEN:
            raise TTSAccessError(HF_TOKEN_MISSING)
        logger.info("Loading Indic Parler-TTS on %s", self.device)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                INDIC_PARLER_MODEL_ID,
                token=HF_TOKEN,
                trust_remote_code=True,
            )
            self.model = AutoModel.from_pretrained(
                INDIC_PARLER_MODEL_ID,
                token=HF_TOKEN,
                trust_remote_code=True,
            ).to(self.device)
        except OSError as error:
            error_text = str(error).lower()
            if any(marker in error_text for marker in ("gated repo", "401", "403", "unauthorized", "access to model")):
                raise TTSAccessError(MODEL_ACCESS_NOT_ACCEPTED) from error
            raise
        self.model.eval()

    def generate(self, text: str, language_name: str, voice_style: str, output_path: Path) -> None:
        self.load()
        description = f"{VOICE_STYLES[voice_style]} The speaker is speaking {language_name}."
        description_ids = self.tokenizer(description, return_tensors="pt").input_ids.to(self.device)
        prompt_ids = self.tokenizer(text, return_tensors="pt").input_ids.to(self.device)
        with torch.inference_mode():
            audio = self.model.generate(input_ids=description_ids, prompt_input_ids=prompt_ids)
        audio_array = audio.detach().cpu().numpy().squeeze()
        sampling_rate = getattr(self.model.config, "sampling_rate", 44_100)
        sf.write(output_path, audio_array, sampling_rate)


indic_tts_service = IndicParlerService()
