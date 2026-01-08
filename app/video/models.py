from tortoise.models import Model
from tortoise import fields
import uuid

class Video(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    script = fields.TextField()
    status = fields.CharField(max_length=20, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Scene(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    order_number = fields.IntField(default=0)
    video = fields.ForeignKeyField("models.Video", related_name="scenes")
    media_type = fields.CharField(max_length=20, default="image")
    narration = fields.TextField(null=True) # The excerpt of the script that the scene is based on
    duration_seconds = fields.IntField(default=0)
    visual_prompt = fields.TextField(null=True)
    mood = fields.CharField(max_length=20, null=True)