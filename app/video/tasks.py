from pathlib import Path
import tempfile
from celery import shared_task
from sqlalchemy.orm import Session

from app.common.utils import get_url_from_s3_key
from app.database import get_db_session, provide_db_session
from app.langgraph_workflows.graphs.script_to_video_processor import ScriptToVideo
from app.langgraph_workflows.states import ScriptToVideoState
import asyncio
import logging

logger = logging.getLogger(__name__)

from app.video.models import Video, VideoStatus



@shared_task
@provide_db_session
def compile_video_task(db: Session, video_id: str):
    logger.info(f"Video compilation started for {video_id}")
    
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise ValueError(f"Video with ID {video_id} not found")
    
    if video.status != VideoStatus.completed:
        raise ValueError(f"Asset generation for video with ID {video_id} is not completed")
    
    
    try:
        temp_dir = Path(tempfile.mkdtemp())
        
        sorted_scenes = sorted(video.scenes, key=lambda x: x.order_number)
        
        for i, scene in enumerate(sorted_scenes):
            scene_data = {
                "image": None, 
                "audio": None,
                "duration": scene.duration_seconds,
                "order_number": scene.order_number
            }
            
            if scene.image_file_key:
                image_url = get_url_from_s3_key(scene.image_file_key)
                image_path = temp_dir / f"scene_image_{scene.order_number}.jpg"
                
                
    except Exception as e:
        logger.error(f"Error compiling video: {e}")
        return False
    return True

@shared_task 
@provide_db_session
def script_to_video_task(db: Session, video_id: str):
    logger.info(f"Video generation started for {video_id}")
    
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise ValueError(f"Video with ID {video_id} not found")
    
    
    script_to_video = ScriptToVideo()
    graph = script_to_video.build_graph()
    
    state = ScriptToVideoState(script=video.script, video_id=str(video_id))
    result = graph.invoke(state)
    
        
    logger.info(f"Scenes generated successfully for video:: {video_id} ")    
    logger.info("--------------------------------")
    logger.info("Result: ", result)
    return True