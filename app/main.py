from fastapi import FastAPI
from app.video.routers import router as video_router
from app.config import settings
from tortoise.contrib.fastapi import register_tortoise

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Clippink microservice",
    description="Video processing microservice for Clippink",
    version=settings.VERSION,
    contact={
        "name": "Clippink",
        "url": "https://clipp.ink",
        "email": "onuhudoudo@gmail.com",
    },
)


app.include_router(video_router, prefix="/video", tags=["Video"])

register_tortoise(
    app,
    config = settings.TORTOISE_ORM_CONFIG,
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": settings.VERSION,
    }
    
