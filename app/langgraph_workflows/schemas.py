from typing import Literal
from pydantic import BaseModel, Field


class SceneSchema(BaseModel):
    order_number: int = Field(..., description="The order number of the scene")
    narration: str = Field(..., description="The excerpt of the script that the scene is based on")
    visual_prompt: str = Field(..., description="A concise but vivid description of what should be shown visually")
    duration_seconds: int = Field(..., description="The duration of the scene in seconds")
    mood: Literal["dramatic", "mysterious", "inspiring", "educational", "energetic"] = Field(..., description="The mood of the scene")
    visual_type: str = Field(..., description="The type of visual media to be generated")

class SceneListSchema(BaseModel):
    scenes: list[SceneSchema] = Field(..., description="The list of scenes")