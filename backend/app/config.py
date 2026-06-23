"""Central configuration for the local backend."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


APP_DIR = Path(__file__).resolve().parent
# The backend root is the only dotenv source. Secrets stay out of source code.
load_dotenv(APP_DIR.parent / ".env")
OUTPUT_DIR = APP_DIR / "outputs"
TEXT_OUTPUT_DIR = OUTPUT_DIR / "text"
AUDIO_OUTPUT_DIR = OUTPUT_DIR / "audio"

NLLB_MODEL_ID = "facebook/nllb-200-distilled-600M"
XTTS_MODEL_ID = "tts_models/multilingual/multi-dataset/xtts_v2"
INDIC_PARLER_MODEL_ID = "ai4bharat/indic-parler-tts"
MAX_CHUNK_WORDS = 350
MAX_INPUT_CHARACTERS = 50_000

XTTS_SPEAKER = os.getenv("XTTS_SPEAKER")
XTTS_SPEAKER_WAV = os.getenv("XTTS_SPEAKER_WAV")
HF_TOKEN = os.getenv("HF_TOKEN")

VOICE_STYLES = {
    "professional": "A clear professional speaker with calm tone, moderate speed, and high-quality studio recording.",
    "friendly": "A friendly speaker with warm tone, natural pace, and expressive delivery.",
    "storytelling": "A storytelling voice with expressive tone, smooth pacing, and engaging delivery.",
    "calm": "A calm speaker with soft tone, slow pace, and clear pronunciation.",
    "energetic": "An energetic speaker with lively tone, confident delivery, and clear pronunciation.",
}


def ensure_output_directories() -> None:
    """Create generated-file directories before the first request."""
    TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
