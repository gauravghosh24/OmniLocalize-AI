"""Sentence-aware chunking suitable for translation models."""

from __future__ import annotations

import re

from app.config import MAX_CHUNK_WORDS


SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[\"'“”A-Z0-9])")


def split_into_chunks(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    """Split text near sentence boundaries without exceeding ``max_words``."""
    sentences = [sentence.strip() for sentence in SENTENCE_BOUNDARY.split(text) if sentence.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    current_words: list[str] = []
    for sentence in sentences:
        sentence_words = sentence.split()
        if len(sentence_words) > max_words:
            if current_words:
                chunks.append(" ".join(current_words))
                current_words = []
            chunks.extend(
                " ".join(sentence_words[index : index + max_words])
                for index in range(0, len(sentence_words), max_words)
            )
            continue
        if current_words and len(current_words) + len(sentence_words) > max_words:
            chunks.append(" ".join(current_words))
            current_words = []
        current_words.extend(sentence_words)

    if current_words:
        chunks.append(" ".join(current_words))
    return chunks
