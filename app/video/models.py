from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, UUID, Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SQlEnum
from sqlalchemy.orm import relationship

class VideoStatus(Enum):
    pending= 'pending'
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'

class Video(Base):
    __tablename__ = "video"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    script = Column(Text, nullable=False)
    status = Column(SQlEnum(VideoStatus), nullable=False, default=VideoStatus.pending)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    final_audio_key = Column(String(255), nullable=True)
    final_audio_url = Column(String(255), nullable=True)
    scenes = relationship("Scene", back_populates="video")

class Scene(Base):
    __tablename__ = "scene"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    order_number = Column(Integer, nullable=False, default=0)
    video_id = Column(UUID, ForeignKey("video.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String(20), nullable=False, default="image")
    narration = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=False, default=0)
    visual_prompt = Column(Text, nullable=True)
    mood = Column(String(20), nullable=True)
    audio_url = Column(String(255), nullable=True)
    audio_file_key = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    image_file_key = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    video_file_key = Column(String(255), nullable=True)
    audio_duration_seconds = Column(Float, default=1)
    video = relationship("Video", back_populates="scenes")
    captions = Column(JSONB, nullable=True)