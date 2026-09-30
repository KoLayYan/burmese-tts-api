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
    rate: str = "+0%"  # ဥပမာ - "-20%" (နှေးစေရန်) သို့မဟုတ် "+20%" (မြန်စေရန်)

@app.get("/")
def home():
    return {"status": "Burmese TTS API with speech rate control is running!"}

@app.post("/generate-audio")
async def generate_audio(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    output_file = "/tmp/output.mp3"
    voice = request.voice if request.voice else "my-MM-NilarNeural"
    rate = request.rate if request.rate else "+0%"
    
    try:
        # edge-tts တွင် rate ထည့်သွင်းခြင်း
        communicate = edge_tts.Communicate(request.text, voice, rate=rate)
        await communicate.save(output_file)
        
        return FileResponse(
            output_file, 
            media_type="audio/mpeg", 
            filename="speech.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
