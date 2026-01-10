from celery import shared_task
from sqlalchemy.orm import Session

from app.database import get_db_session, provide_db_session
from app.langgraph_workflows.graphs.script_to_video_processor import ScriptToVideo
from app.langgraph_workflows.states import ScriptToVideoState
import asyncio
import logging

logger = logging.getLogger(__name__)

from app.video.models import Video

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