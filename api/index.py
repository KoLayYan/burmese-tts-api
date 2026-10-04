from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice: str = "my-MM-NilarNeural"
    rate: str = "+0%"

@app.get("/")
def home():
    return {"status": "Burmese TTS API running!"}

@app.post("/generate-audio")
async def generate_audio(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    output_file = "/tmp/output.mp3"
    voice = request.voice or "my-MM-NilarNeural"
    rate = request.rate or "+0%"
    try:
        communicate = edge_tts.Communicate(request.text, voice, rate=rate)
        await communicate.save(output_file)
        return FileResponse(output_file, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
