from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
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
    voice_id: str = "ClAtsC1ukzT6U0XgCO4c"  # Default (Moe Moe)

@app.get("/")
def home():
    return {"status": "ElevenLabs Burmese TTS API is running!"}

@app.post("/generate-audio")
async def generate_audio(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Vercel Environment Variable မှ API Key ကို ဆွဲထုတ်သည်
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ElevenLabs API Key not configured")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{request.voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    # မြန်မာလို အကောင်းဆုံးထွက်ရန် multilingual v2 မော်ဒယ်ကို အသုံးပြုသည်
    data = {
        "text": request.text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"ElevenLabs API Error: {response.text}")
    
    output_file = "/tmp/output.mp3"
    with open(output_file, "wb") as f:
        f.write(response.content)
        
    return FileResponse(
        output_file, 
        media_type="audio/mpeg", 
        filename="speech.mp3"
    )
