from typing import Literal
from pydantic import BaseModel, Field

#created this to be used for llm generation so it doesn't hallucinate files metadata
class GeneratedSceneSchema(BaseModel):
    order_number: int = Field(..., description="The order number of the scene")
    narration: str = Field(..., description="The excerpt of the script that the scene is based on")
    visual_prompt: str = Field(..., description="A concise but vivid description of what should be shown visually")
    duration_seconds: int = Field(..., description="The duration of the scene in seconds")
    mood: Literal["dramatic", "mysterious", "inspiring", "educational", "energetic"] = Field(..., description="The mood of the scene")
    # visual_type: str = Field(..., description="The type of visual media to be generated")


class GeneratedSceneListSchema(BaseModel):
    scenes: list[GeneratedSceneSchema] = Field(..., description="The list of scenes")


class SceneSchema(BaseModel):
    order_number: int = Field(..., description="The order number of the scene")
    narration: str = Field(..., description="The excerpt of the script that the scene is based on")
    visual_prompt: str = Field(..., description="A concise but vivid description of what should be shown visually")
    duration_seconds: int = Field(..., description="The duration of the scene in seconds")
    mood: Literal["dramatic", "mysterious", "inspiring", "educational", "energetic"] = Field(..., description="The mood of the scene")
    visual_type: str = Field(..., description="The type of visual media to be generated")
    
    audio_url: str = Field(default=None, description="The URL of the audio file for this scene")
    audio_file_key: str = Field(default=None, description="The key of the audio file")
    image_url: str = Field(default=None, description="The URL of the image file for this scene if it applies")
    image_file_key: str = Field(default=None, description="The key of the image file")
    video_url: str = Field(default=None, description="The URL of the video file for this scene if it applies")
    video_file_key: str = Field(default=None, description="The key of the video file")

class SceneListSchema(BaseModel):
    scenes: list[SceneSchema] = Field(..., description="The list of scenes")