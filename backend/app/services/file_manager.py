"""Safe persistence and lookup for locally generated files."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from app.config import AUDIO_OUTPUT_DIR, TEXT_OUTPUT_DIR, ensure_output_directories


SAFE_FILENAME = re.compile(r"^[a-z]{2}_\d{8}_\d{6}_\d{3}\.(?:txt|wav)$")


def build_filename(language_code: str, extension: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return f"{language_code}_{timestamp}.{extension}"


def save_text(language_code: str, text: str) -> str:
    ensure_output_directories()
    filename = build_filename(language_code, "txt")
    (TEXT_OUTPUT_DIR / filename).write_text(text, encoding="utf-8")
    return filename


def audio_path(language_code: str) -> tuple[str, Path]:
    ensure_output_directories()
    filename = build_filename(language_code, "wav")
    return filename, AUDIO_OUTPUT_DIR / filename


def get_generated_file(directory: Path, filename: str, extension: str) -> Path:
    """Allow only this application's own generated output names."""
    if not SAFE_FILENAME.fullmatch(filename) or not filename.endswith(f".{extension}"):
        raise ValueError("Invalid generated filename.")
    path = directory / filename
    if not path.is_file():
        raise FileNotFoundError(filename)
    return path
