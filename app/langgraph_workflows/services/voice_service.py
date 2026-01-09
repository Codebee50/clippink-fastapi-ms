from elevenlabs import ElevenLabs, VoiceSettings
from app.langgraph_workflows.schemas import SceneSchema
import uuid
from app.config import settings

elevenlabs_client = ElevenLabs(api_key=settings.ELEVEN_LABS_API_KEY)
VOICE_ID = "j9jfwdrw7BRfcR43Qohk"

class VoiceService:
    def __init__(self, scenes: list[SceneSchema]=None):
        self.scenes = scenes
    
    def generate_scenes_audio(self) -> list[str]:
        if not self.scenes:
            raise ValueError("Expected scenes, got None")
        return self._generate_scenes_audio_eleven_labs()
    
    def _generate_scenes_audio_eleven_labs(self) -> list[str]:
        session_id = str(uuid.uuid4())
        audio_paths = []
        for scene in self.scenes:
            print(f"Generating audio for scene: {scene.narration}")
            narration = scene.narration
            
            audio = elevenlabs_client.text_to_speech.convert(
                voice_id=VOICE_ID,
                text=narration,
                output_format="mp3_44100_128",
                model_id="eleven_multilingual_v2",
                # voice_settings=voice_settings
            )
            
            session_dir = settings.OUTPUT_DIR / f"{session_id}"
            session_dir.mkdir(exist_ok=True, parents=True)
            
            audio_path = session_dir / f"{scene.order_number}.mp3"
            with open(audio_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)
                    
            audio_paths.append(audio_path)
        return audio_paths