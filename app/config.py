
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import cached_property

load_dotenv()


class AppModule():
    def __init__(self, name: str, module: str, db_models: str):
        self.name = name
        self.module = module
        self.db_models = db_models

class Settings(BaseSettings):
    VERSION: str = "0.0.1"
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
    DATABASE_URL: str = "sqlite://db.sqlite3"
    
    APP_MODULES: list[AppModule] = [
       AppModule(name="video", module="app.video", db_models="app.video.models")
    ]
    
    @cached_property    
    def TORTOISE_ORM_CONFIG(self): 
        return {
            "connections": {
                "default": self.DATABASE_URL
                # PostgreSQL example: "postgres://user:password@localhost:5432/dbname"
                # MySQL example: "mysql://user:password@localhost:3306/dbname"
            },
            "apps": {
                "models": {
                    "models": [app.db_models for app in self.APP_MODULES],
                    "default_connection": "default",
                }
            },
        }
    
    class Config:
        env_file = ".env"
        case_sensitive= True
    
    
settings = Settings()