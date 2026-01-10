from pydantic import BaseModel, Field

from app.langgraph_workflows.schemas import SceneSchema

class ScriptToVideoState(BaseModel):
    script: str = Field(..., description="The script to be converted to a video")
    video_id: str = Field(default=None, description="The ID of the video to be created")
    scenes: list[SceneSchema] = Field(default=[], description="The scenes of the video")
    final_audio_key: str= Field(default=None, description="The key of the final audio file")
    
    
   