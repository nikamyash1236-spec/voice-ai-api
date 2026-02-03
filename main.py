from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import random

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Voice AI API is live!"}

API_KEY = "test123"

class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str

@app.post("/detect-voice")
def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(None)
):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Audio format validation
    if data.audio_format not in ["mp3", "wav"]:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Base64 decoding
    try:
        audio_bytes = base64.b64decode(data.audio_base64, validate=True)
        audio_size = len(audio_bytes)
        if audio_size < 1000:
            raise ValueError("Audio too short")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid audio input")

    # ---- SIMPLE AI LOGIC ----
    is_ai = (audio_size % 2 == 0)

    if is_ai:
        confidence = round(random.uniform(0.75, 0.95), 2)
        message = "AI-generated voice detected"
    else:
        confidence = round(random.uniform(0.55, 0.75), 2)
        message = "Human voice detected"

    return {
        "status": "success",
        "is_ai_generated": is_ai,
        "confidence": confidence,
        "language": data.language,
        "message": message
    }

