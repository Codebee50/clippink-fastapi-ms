from asyncio import Semaphore
import asyncio
from io import BytesIO
import uuid
import requests
from app.langgraph_workflows.schemas import SceneSchema
import replicate
from app.common.utils import get_url_from_s3_key

from app.config import settings
import logging
import time
logger = logging.getLogger(__name__)

class ImageService:
    _semaphore = Semaphore(6)
    _rate_limit_delay = 3
    _last_request_time = 0
    _rate_lock = asyncio.Lock()
    
    def __init__(self, scenes: list[SceneSchema]=None, video_id: str=None):
        self.scenes = scenes
        self.video_id = video_id
    
    def generate_images(self, aspect_ratio="9:16") -> list[str]:
        image_urls = []
        
        for scene in self.scenes:
            image_key = self._generate_image_seedream(scene, aspect_ratio)
            image_url = get_url_from_s3_key(image_key)  
            image_urls.append(image_url)
            scene.image_url = image_url
            scene.image_file_key = image_key
            time.sleep(10)
        return image_urls
    
    
    def _upload_image_to_s3(self, image_url: str, image_format: str="png") -> str:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            s3_key = f"images/{self.video_id}/{uuid.uuid4()}.{image_format}"
            s3_client= settings.get_s3_client()
            s3_client.upload_fileobj(
                BytesIO(response.content),
                settings.AWS_BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": f"image/{image_format}"
                }
            )
            return s3_key  
        except Exception as e:
            logger.error(f"Error uploading image to s3: {e}")
            return image_url
        

    def _generate_image_seedream(self, scene: SceneSchema, aspect_ratio="9:16")-> str:
        logger.info(f"Generating image for scene: {scene.order_number}")
        output = replicate.run(
            "bytedance/seedream-4",
            input={
                "size": "2K",
                "width": 2048,
                "height": 2048,
                "prompt": scene.visual_prompt,
                "max_images": 1,
                "image_input": [],
                "aspect_ratio": aspect_ratio,
                "enhance_prompt": True,
                "sequential_image_generation": "disabled",
            }
        )
        
        
        logger.info(f"Image generated for scene: {scene.order_number} successfully: {output[0].url}")
            
        return self._upload_image_to_s3(output[0].url, "jpeg")