from app.common.utils import download_file_remote_to_local
from app.config import settings
from app.langgraph_workflows.schemas import SceneSchema
from app.langgraph_workflows.services.image_service import ImageService
import asyncio
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

async def main():
    prompts = [
        # --- OBJECTS: Airplanes, Rockets, Buildings (40% - 12 Prompts) ---
        "Cinematic shot of a sleek private jet flying above a sea of golden clouds at sunset, 8k, photorealistic",
        "A massive SpaceX-style rocket lifting off from a launchpad, fire and smoke billows, night sky, ultra-detailed",
        "Futuristic cyberpunk skyscraper with glowing neon signs and rain-slicked glass, low angle shot, 8k",
        "Vintage silver propeller plane parked on a grassy runway, soft morning mist, nostalgic 35mm film look",
        "Brutalist concrete architecture building with sharp geometric shadows against a bright blue sky, minimalist",
        "Modern glass mansion perched on a cliffside overlooking the ocean, twilight lighting, luxury aesthetic",
        "Close-up of a space shuttle orbiting Earth, sunlight reflecting off the hull, stars in the background, 8k",
        "Intricate steampunk airship floating through a cloudy sky, copper and brass textures, Victorian aesthetic",
        "A lone minimalist white lighthouse on a jagged rock, crashing waves, moody gray sky, high contrast",
        "Extreme macro shot of a high-end cinema camera lens, glass reflections, tech-luxury aesthetic, 8k",
        "High-speed bullet train blurred in motion at a modern station, streaks of light, industrial design",
        "A high-tech drone hovering over a tropical coastline, turquoise water below, sharp focus, cinematic",

        # --- CARTOON / STYLIZED (30% - 9 Prompts) ---
        "3D Pixar-style cute astronaut sitting on a small moon, holding a fishing rod catching a star, vibrant colors",
        "Lo-fi anime style, a cozy attic bedroom with a telescope, starry night visible through the window, warm lighting",
        "Whimsical 3D claymation treehouse in a magical forest, glowing lanterns, soft textures, toy-like feel",
        "Flat vector illustration of a glowing brain connected to digital circuits, vibrant purple and gold, modern tech",
        "Playful 3D render of a stylized rocket ship with a 'smile' design, bright orange fire, soft studio lighting",
        "Studio Ghibli style landscape of a rolling green hill with a single red door standing in the middle, blue sky",
        "Minimalist 2D character silhouette walking through a world of giant geometric shapes, pastel color palette",
        "3D isometric illustration of a tiny cozy library with floating books, warm glow, high-quality rendering",
        "Colorful pop-art illustration of a hand holding a lightning bolt, bold outlines, Ben-Day dots, comic style",

        # --- CREATIVE / MISC (30% - 9 Prompts) ---
        "Abstract liquid marble texture in shades of deep blue and gold, flowing movement, elegant and high-end",
        "A cybernetic robotic hand gently touching a real green leaf, nature meets tech, soft bokeh, 8k",
        "Breathtaking macro shot of a glowing jellyfish in deep dark water, neon pink and blue bioluminescence",
        "Geometric 3D glass pyramids floating in a void, light refracting into rainbows, minimalist aesthetic",
        "A vintage celestial map of the stars with gold leaf detailing, aged paper texture, academic aesthetic",
        "Ethereal rays of light shining through thick colorful smoke, abstract movement, cinematic atmosphere",
        "Close-up of a vintage vinyl record spinning, needle in the groove, dust particles in the light, warm tones",
        "A lone tree with glowing purple leaves in the middle of a white salt flat desert, surreal dreamscape",
        "High-speed photography of a splash of milk forming a perfect crown shape, clean white background, macro"
    ]
    scenes = []
    for i, prompt in enumerate(prompts):
        scene = SceneSchema(
            order_number=i+1,
            visual_prompt=prompt,
            mood="dramatic",
            visual_type="image",
            narration=prompt
        )
        scenes.append(scene)
        
    image_service = ImageService(scenes=scenes, video_id="landing-page-images")
    image_urls = await image_service.generate_images(aspect_ratio="2:3")
    print(f"Image urls: {image_urls}")
    
    for image in image_urls:
        if image is None:
            continue
        
        local_path = settings.OUTPUT_DIR / f"landing/image_{uuid.uuid4()}.jpeg"
        print(f"Downloading image to {local_path}")
        await download_file_remote_to_local(image, local_path)
        
        
if __name__ == "__main__":
    asyncio.run(main())