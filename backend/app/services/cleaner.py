"""Small, predictable input cleanup helpers."""

from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """Trim text, collapse spare spaces, and retain intentional paragraphs."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    return text.strip()
