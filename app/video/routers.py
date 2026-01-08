from fastapi import APIRouter

from app.video.models import Video
from app.video.schemas import ScriptToVideoRequestSchema
from app.video.tasks import script_to_video_task

router = APIRouter()

@router.post("/script-to-video/")
async def script_to_video(req_body: ScriptToVideoRequestSchema):
    
    # video = await Video.create(script=req_body.script)
    
    script_to_video_task.delay(req_body.script)
    

    return {"message": "Video created successfully"}