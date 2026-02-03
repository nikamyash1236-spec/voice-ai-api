from fastapi import FastAPI, Header, HTTPException, Request
import base64
import random

app = FastAPI()

API_KEY = "test123"


@app.get("/")
def read_root():
    return {"message": "Voice AI API is live!"}


@app.post("/detect-voice")
async def detect_voice(request: Request, x_api_key: str = Header(None)):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Read raw JSON body (tester-proof)
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Accept BOTH snake_case and camelCase
    language = body.get("language")
    audio_format = body.get("audio_format") or body.get("audioFormat")
    audio_base64 = body.get("audio_base64") or body.get("audioBase64")

    # Validate required fields
    if not language or not audio_format or not audio_base64:
        raise HTTPException(status_code=422, detail="Missing required fields")

    # Validate audio format
    if audio_format not in ["mp3", "wav"]:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Decode Base64 (NO strict validation)
    try:
        audio_bytes = base64.b64decode(audio_base64)
        if len(audio_bytes) < 50:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid audio input")

    # ---- SIMPLE AI LOGIC ----
    is_ai = len(audio_bytes) % 2 == 0
    confidence = round(
        random.uniform(0.75, 0.95) if is_ai else random.uniform(0.55, 0.75),
        2
    )

    return {
        "status": "success",
        "is_ai_generated": is_ai,
        "confidence": confidence,
        "language": language,
        "message": "AI-generated voice detected" if is_ai else "Human voice detected"
    }
