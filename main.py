from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import edge_tts
import os
import tempfile

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API Edge-TTS Aktif!"}

@app.post("/generate")
async def generate_tts(text: str, background_tasks: BackgroundTasks, voice: str = "id-ID-ArdiNeural"):
    # Membuat file MP3 sementara
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    
    # Proses konversi teks ke suara
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)
    
    # Menghapus file MP3 dari server Render setelah berhasil dikirim ke n8n
    background_tasks.add_task(os.remove, path)
    
    # Mengirimkan file MP3 kembali ke n8n
    return FileResponse(path, media_type="audio/mpeg", filename="voiceover.mp3")
