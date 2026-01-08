from fastapi import APIRouter

from app.config import settings
from app.video.models import Video
from app.video.schemas import ScriptToVideoRequestSchema
from app.video.tasks import script_to_video_task
from pydub import AudioSegment

router = APIRouter()

@router.get("/merge-audio-files/{session_id}")
async def merge_audio_files(session_id: str):
    final_audio = AudioSegment.empty()
    session_dir = settings.OUTPUT_DIR / f"{session_id}"
    
    print(f"Merging audio files for session: {session_dir}")
    
    for audio_file in sorted(session_dir.glob("*.mp3")):
        final_audio += AudioSegment.from_mp3(audio_file)
        
    final_audio.export(session_dir / "final_audio.mp3", format="mp3")
    return {"message": "Audio files merged successfully"}

@router.post("/script-to-video/")
async def script_to_video(req_body: ScriptToVideoRequestSchema):
    
    # video = await Video.create(script=req_body.script)
    
    script_to_video_task.delay(req_body.script)
    

    return {"message": "Video created successfully"}