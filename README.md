# OmniLocalize AI

OmniLocalize AI is a local multilingual text translation engine for Indian and European languages.

## Version 1: text translation only

Version 1 translates English text into Hindi, Tamil, French, and German with `facebook/nllb-200-distilled-600M`. It saves each translation as a text file and provides copy and download controls in the dashboard.

Voice generation and text-to-speech are planned for Version 2. TTS services remain in the codebase but are disabled in Version 1: no voice model is loaded, downloaded, or invoked.
## Features

- Local NLLB-200 translation from English to Hindi, Tamil, French, and German
- Sentence-aware chunking for long input
- Text result cards with copy and text-download actions
- FastAPI backend and Next.js dashboard
- CPU fallback, with CUDA used automatically when a compatible PyTorch installation is present

## System requirements

- Windows, Linux, or macOS
- Python 3.10+
- Node.js 20.9+ and npm
- 16 GB RAM recommended

## Project layout

```text
omnilocalize-ai/
├── backend/                  # FastAPI translation service
│   └── app/outputs/text/     # generated text files (gitignored)
├── frontend/                 # Next.js dashboard
└── README.md
```

## Run the backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
python run_backend.py
```

For CPU-only use, install PyTorch from its [official selector](https://pytorch.org/get-started/locally/) instead of the CUDA command. The first start downloads the NLLB model. Browse `http://localhost:8000/docs` for the API.

## Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend calls `http://localhost:8000` by default. To use another local backend address, copy `frontend/.env.example` to `frontend/.env.local` and set `NEXT_PUBLIC_BACKEND_URL`.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Backend and translation-model status |
| GET | `/api/translate?text=Hello&target_languages=fr&target_languages=de` | Preview translations without saving files |
| POST | `/api/translate` | Translate text without saving files |
| POST | `/api/localize` | Translate selected languages and save text files |
| GET | `/api/download/text/{filename}` | Download a generated text file |

`/api/generate-audio` and the audio download/preview routes are intentionally disabled in Version 1. They return an `audio_error` explaining that voice generation will be added later.

Example localization request:

```json
{
  "text": "A long English article goes here.",
  "target_languages": ["hi", "ta", "fr", "de"]
}
```

The response includes `translated_text`, `text_file`, `audio_file: null`, and an `audio_error` explaining that voice generation is disabled in Version 1.

## Future scope

- Voice generation and regional TTS (Version 2)
- More source and target languages
- Optional subtitle export formats
- Batch document import
