"""NLLB translation service, loaded once at API startup."""

from __future__ import annotations

import logging

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from app.config import NLLB_MODEL_ID
from app.models.language_map import LANGUAGES, SOURCE_NLLB_CODE
from app.services.chunker import split_into_chunks


logger = logging.getLogger(__name__)


class NLLBTranslator:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None

    def load(self) -> None:
        """Download/load NLLB exactly once for the process."""
        if self.model is not None and self.tokenizer is not None:
            return
        logger.info("Loading NLLB model on %s", self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_ID, src_lang=SOURCE_NLLB_CODE)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL_ID).to(self.device)
        self.model.eval()

    def translate(self, text: str, target_language: str) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Translation model is not loaded yet.")
        language = LANGUAGES[target_language]
        translated_chunks: list[str] = []
        for chunk in split_into_chunks(text):
            inputs = self.tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(language.nllb_code)
            with torch.inference_mode():
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=forced_bos_token_id,
                    max_new_tokens=512,
                )
            translated_chunks.append(self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0])
        return "\n\n".join(translated_chunks)


translator = NLLBTranslator()
