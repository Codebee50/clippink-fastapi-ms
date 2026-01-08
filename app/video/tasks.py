from celery import shared_task

from app.langgraph_workflows.graphs.script_to_video_processor import ScriptToVideo
from app.langgraph_workflows.states import ScriptToVideoState
from app.video.models import Video
import asyncio

async def process_script_to_video(video_id: str):
    video = await Video.get(id=video_id)
    if not video:
        raise ValueError(f"Video with ID {video_id} not found")
    


@shared_task 
def script_to_video_task(script: str):
    print(f"Video generation started for {script}")
        
    script_to_video = ScriptToVideo()
    graph = script_to_video.build_graph()
    
    state = ScriptToVideoState(script=script)
    result = graph.invoke(state)
    
        
    print(f"Scenes generated successfully for video:: ", result.get("scenes"))    
    print("--------------------------------")
    print("Result: ", result)
    return True