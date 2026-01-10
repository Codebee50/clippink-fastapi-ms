from app.langgraph_workflows.schemas import SceneSchema
import replicate

from app.config import settings
import logging
import time
logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, scenes: list[SceneSchema]=None, video_id: str=None):
        self.scenes = scenes
        self.video_id = video_id
    
    def generate_images(self) -> list[str]:
        image_urls = []
        for scene in self.scenes:
            image_url = self._generate_image_seedream(scene)
            image_urls.append(image_url)
            scene.image_url = image_url
            time.sleep(10)
        return image_urls
    
    def _generate_image_stable_diffusion(self) -> str:
        pass
    
    def _generate_image_dalle_3(self) -> str:
        pass
    
    def _generate_image_seedream(self, scene: SceneSchema)-> str:
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
                "aspect_ratio": "9:16",
                "enhance_prompt": True,
                "sequential_image_generation": "disabled"
            }
        )
        
        
        logger.info(f"Image generated for scene: {scene.order_number} successfully: {output[0].url}")
        # with open(f"images/{self.video_id}/{scene.order_number}.png", "wb") as f:
        #     f.write(output[0].read())
            
        return output[0].url