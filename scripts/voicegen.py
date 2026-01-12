from app.langgraph_workflows.schemas import SceneSchema
from app.langgraph_workflows.services.voice_service import VoiceService


def main():
    scenes = [
        SceneSchema(
            order_number=1,
            narration="We’ve made life faster, easier, and smoother than ever before.",
            visual_prompt="A test visual prompt",
            mood="dramatic",
            visual_type="image"
        ),
        SceneSchema(
            order_number=2,
            narration="This is the real cost of convenience.",
            visual_prompt="A test visual prompt",
            mood="dramatic",
            visual_type="image"
        )
    ]
    
    voice_service = VoiceService(scenes=scenes, video_id="6964540cf02d5d235b84027a")
    voice_service.generate_scenes_audio()

if __name__ == "__main__":
    main()