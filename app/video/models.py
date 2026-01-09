from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, UUID, Integer, ForeignKey
import uuid
from app.database import Base

class Video(Base):
    __tablename__ = "video"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    script = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class Scene(Base):
    __tablename__ = "scene"
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = Column(Integer, nullable=False, default=0)
    video_id = Column(UUID, ForeignKey("video.id"), nullable=False)
    media_type = Column(String(20), nullable=False, default="image")
    narration = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=False, default=0)
    visual_prompt = Column(Text, nullable=True)
    mood = Column(String(20), nullable=True)