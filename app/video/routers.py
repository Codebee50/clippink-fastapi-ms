from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.database import get_db
from app.video.models import Video, VideoStatus
from app.video.schemas import ScriptToVideoRequestSchema
from app.video.tasks import compile_video_task, script_to_video_task
from pydub import AudioSegment
from fastapi import HTTPException
router = APIRouter()

@router.post("/compile-video/{video_id}/")
async def compile_video(video_id:str, db: Session=Depends(get_db)):
    video= db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.status != VideoStatus.completed:
        raise HTTPException(status_code=400, detail="Video is not completed")
    
    compile_video_task.delay(video_id)
    
    return {"message": "Video compiled successfully"}

    

@router.get("/{video_id}/")
async def get_video_by_id(video_id: str, db: Session=Depends(get_db)):
    video = db.query(Video).options(selectinload(Video.scenes)).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video

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
async def script_to_video(req_body: ScriptToVideoRequestSchema, db: Session=Depends(get_db)):
    
    video = Video(script=req_body.script)
    db.add(video)
    db.commit()
    db.refresh(video)
    
    script_to_video_task.delay(video.id)
    

    return {"message": "Video created successfully", "video": video}