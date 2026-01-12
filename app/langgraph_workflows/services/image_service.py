from asyncio import Semaphore
import asyncio
from io import BytesIO
import uuid
import requests
from app.langgraph_workflows.schemas import SceneSchema
import replicate
from app.common.utils import get_url_from_s3_key
import aiohttp
from app.config import settings
import logging
from aiolimiter import AsyncLimiter
import time
logger = logging.getLogger(__name__)




class ImageService:
    _concurrency_limit = asyncio.Semaphore(5) #ensure you dont exceed n concurrent api calls i.e you dont call the api more than n times at the same time
    _rate_limit = AsyncLimiter(max_rate=3, time_period=60) #ensure you dont exceed max_rate api calls per time_period seconds
    
    
    def __init__(self, scenes: list[SceneSchema]=None, video_id: str=None):
        self.scenes = scenes
        self.video_id = video_id
    
    async def generate_images(self, aspect_ratio="9:16") -> list[str]:
        image_urls = []
        
        tasks = [
            self._generate_single_image(scene, aspect_ratio) for scene in self.scenes
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error generating image for scene: {self.scenes[i].order_number}: {result}")
                image_urls.append(None)
            else:
                image_urls.append(result)
        return image_urls
    
    async def _generate_single_image(self, scene, aspect_ratio="9:16") -> str:
        async with self._concurrency_limit:
            async with self._rate_limit:
                return await self._generate_image_stability(scene, aspect_ratio)
            
            
    async def _generate_image_stability(self, scene: SceneSchema, aspect_ratio="9:16")-> str:
        logger.info(f"Generating image for scene: {scene.order_number} using stability")
        
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(
            None,
            lambda: replicate.run(
                "stability-ai/stable-diffusion-3.5-large",
                input={
                    "cfg": 4.5,
                    'prompt': scene.visual_prompt
                }
            )
        )

        s3_key = await self._upload_image_to_s3(output.url, "jpeg")
        scene.image_url = get_url_from_s3_key(s3_key)
        scene.image_file_key = s3_key
        
        return self._upload_image_to_s3(output.url, "jpeg")
        
    
    async def _generate_image_seedream(self, scene: SceneSchema, aspect_ratio="9:16")-> str:
        logger.info(f"Generating image for scene: {scene.order_number} using seeddream")
        
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(
            None,
            lambda: replicate.run(
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
        )
                
        logger.info(f"Image generated for scene: {scene.order_number} successfully: {output[0].url}")
        
        s3_key = await self._upload_image_to_s3(output[0].url, "jpeg")
        scene.image_url = get_url_from_s3_key(s3_key)
        scene.image_file_key = s3_key
            
        return self._upload_image_to_s3(output[0].url, "jpeg")

    async def _upload_image_to_s3(self, image_url: str, image_format: str="png") -> str:
        try:
            async with aiohttp.ClientSession() as session: #i am using aiohttp because it is more efficient than requests because it is asynchronous and can handle multiple requests at the same time
                async with session.get(image_url) as response:
                    response.raise_for_status()
                    image_data = await response.read()
                    
            
            
            s3_key = f"images/{self.video_id}/{uuid.uuid4()}.{image_format}"
            
            loop = asyncio.get_running_loop()
            
            await loop.run_in_executor(
                None,
                lambda: settings.get_s3_client().upload_fileobj(
                    BytesIO(image_data),
                    settings.AWS_BUCKET_NAME,
                    s3_key,
                    ExtraArgs={
                        "ContentType": f"image/{image_format}"
                    }
                )
            )
            
            return s3_key  
        except Exception as e:
            logger.error(f"Error uploading image to s3: {e}")
            return image_url