from pathlib import Path
import tempfile
from celery import shared_task
from sqlalchemy.orm import Session

from app.common.utils import get_url_from_s3_key
from app.database import get_db_session, provide_db_session
from app.langgraph_workflows.graphs.script_to_video_processor import AssetGenerator
from app.langgraph_workflows.states import AssetGeneratorState
import asyncio
import logging
from app.config import settings

from app.video.utils import compile_video
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
    
    
    asyncio.run(compile_video(video, settings.OUTPUT_DIR))

    return True

@shared_task 
@provide_db_session
def script_to_video_task(db: Session, video_id: str):
    logger.info(f"Video generation started for {video_id}")
    
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise ValueError(f"Video with ID {video_id} not found")
    
    
    asset_generator = AssetGenerator()
    graph = asset_generator.build_graph()
    
    state = AssetGeneratorState(script=video.script, video_id=str(video_id))
    result = graph.invoke(state)
    
        
    logger.info(f"Scenes generated successfully for video:: {video_id} ")    
    logger.info("--------------------------------")
    logger.info("Result: ", result)
    return True