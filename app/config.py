
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import cached_property
import boto3

load_dotenv()


class AppModule():
    def __init__(self, name: str, module: str, db_models: str):
        self.name = name
        self.module = module
        self.db_models = db_models

class Settings(BaseSettings):
    VERSION: str = "0.0.1"
    ELEVEN_LABS_API_KEY: str = "YOUR_ELEVENLABS_API_KEY"
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
    DATABASE_URL: str = "sqlite://db.sqlite3"
    OUTPUT_DIR: Path = Path("elevenlabs_audio")
    AWS_ACCESS_KEY_ID: str = "YOUR_AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: str = "YOUR_AWS_SECRET_ACCESS_KEY"
    AWS_REGION: str = "YOUR_AWS_REGION"
    AWS_BUCKET_NAME: str = "YOUR_AWS_BUCKET_NAME"
    REPLICATE_API_TOKEN: str = "YOUR_REPLICATE_API_TOKEN"
    
    
    APP_MODULES: list[AppModule] = [
       AppModule(name="video", module="app.video", db_models="app.video.models")
    ]
    
    def get_s3_client(self) -> boto3.client:
        return boto3.client(
            "s3",
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION
        )
    
    class Config:
        env_file = ".env"
        case_sensitive= True
    
    def model_post_init(self, __context) -> None:
        try:
            self.OUTPUT_DIR.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Error creating output directory: {e}")
            
    
settings = Settings()

