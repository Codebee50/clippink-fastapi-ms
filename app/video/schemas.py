from pydantic import BaseModel


class ScriptToVideoRequestSchema(BaseModel):
    script:str