"""FastAPI application for local translation and voice generation."""

from __future__ import annotations

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.config import MAX_INPUT_CHARACTERS, TEXT_OUTPUT_DIR, ensure_output_directories
from app.models.language_map import LANGUAGES
from app.schemas import AudioRequest, AudioResult, LocalizeRequest, LocalizeResponse, LocalizeResult, TranslationRequest, TranslationResult
from app.services.cleaner import clean_text
from app.services.file_manager import get_generated_file, save_text
from app.services.translator import translator


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)
VOICE_DISABLED_MESSAGE = "Voice generation is disabled in Version 1. It will be added later."


@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_output_directories()
    # Translation powers every core flow. TTS models are lazy-loaded when their
    # first matching language is requested and stay in memory afterwards.
    translator.load()
    yield


app = FastAPI(
    title="OmniLocalize AI API",
    description="Local NLLB multilingual text translation.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def normalized_text(text: str) -> str:
    cleaned = clean_text(text)
    if not cleaned:
        raise HTTPException(status_code=422, detail="Please provide English text to localize.")
    if len(cleaned) > MAX_INPUT_CHARACTERS:
        raise HTTPException(status_code=422, detail=f"Text must be at most {MAX_INPUT_CHARACTERS:,} characters.")
    return cleaned


def translate_text(text: str, language_code: str) -> str:
    try:
        return translator.translate(text, language_code)
    except Exception as error:
        logger.exception("Translation failed for %s", language_code)
        raise HTTPException(status_code=500, detail=f"Translation failed for {LANGUAGES[language_code].name}: {error}") from error


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "translation_device": str(translator.device),
        "translation_model": "ready" if translator.model is not None else "loading",
    }


@app.post("/api/translate", response_model=list[TranslationResult])
def translate(request: TranslationRequest) -> list[TranslationResult]:
    text = normalized_text(request.text)
    return [
        TranslationResult(
            language=LANGUAGES[code].name,
            language_code=code,
            translated_text=translate_text(text, code),
        )
        for code in request.target_languages
    ]


@app.get("/api/translate", response_model=list[TranslationResult])
def translate_preview(
    text: str = Query(..., min_length=1, max_length=MAX_INPUT_CHARACTERS),
    target_languages: list[str] = Query(..., min_length=1),
) -> list[TranslationResult]:
    """Translate text supplied as query parameters, without creating audio files."""
    language_codes = list(dict.fromkeys(target_languages))
    unsupported = set(language_codes) - set(LANGUAGES)
    if unsupported:
        raise HTTPException(status_code=422, detail=f"Unsupported language code(s): {', '.join(sorted(unsupported))}")
    cleaned = normalized_text(text)
    return [
        TranslationResult(
            language=LANGUAGES[code].name,
            language_code=code,
            translated_text=translate_text(cleaned, code),
        )
        for code in language_codes
    ]


@app.post("/api/generate-audio", response_model=AudioResult)
def generate_audio_endpoint(request: AudioRequest) -> AudioResult:
    """Preserve the endpoint while keeping all Version 1 TTS models inactive."""
    normalized_text(request.text)
    return AudioResult(
        language=LANGUAGES[request.language_code].name,
        language_code=request.language_code,
        audio_error=VOICE_DISABLED_MESSAGE,
    )


@app.post("/api/localize", response_model=LocalizeResponse)
def localize(request: LocalizeRequest) -> LocalizeResponse:
    text = normalized_text(request.text)
    results: list[LocalizeResult] = []
    for language_code in request.target_languages:
        translated_text = translate_text(text, language_code)
        results.append(
            LocalizeResult(
                language=LANGUAGES[language_code].name,
                language_code=language_code,
                translated_text=translated_text,
                text_file=save_text(language_code, translated_text),
                audio_error=VOICE_DISABLED_MESSAGE,
            )
        )
    return LocalizeResponse(status="success", results=results)


@app.get("/api/download/text/{filename}")
def download_text(filename: str) -> FileResponse:
    try:
        path = get_generated_file(TEXT_OUTPUT_DIR, filename, "txt")
    except (ValueError, FileNotFoundError) as error:
        raise HTTPException(status_code=404, detail="Text file not found.") from error
    return FileResponse(path, media_type="text/plain; charset=utf-8", filename=filename)


@app.get("/api/download/audio/{filename}")
def download_audio(filename: str) -> JSONResponse:
    return JSONResponse(status_code=410, content={"audio_error": VOICE_DISABLED_MESSAGE})


@app.get("/api/preview/audio/{filename}")
def preview_audio(filename: str) -> JSONResponse:
    return JSONResponse(status_code=410, content={"audio_error": VOICE_DISABLED_MESSAGE})
