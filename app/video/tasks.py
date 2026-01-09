from celery import shared_task

from app.langgraph_workflows.graphs.script_to_video_processor import ScriptToVideo
from app.langgraph_workflows.states import ScriptToVideoState
import asyncio

async def process_script_to_video(video_id: str):
    pass
    


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