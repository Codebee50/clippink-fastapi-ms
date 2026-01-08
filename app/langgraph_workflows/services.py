from elevenlabs import ElevenLabs, VoiceSettings

from app.langgraph_workflows.schemas import SceneSchema
from app.config import settings


elevenlabs_client = ElevenLabs(api_key=settings.ELEVEN_LABS_API_KEY)
VOICE_ID = "j9jfwdrw7BRfcR43Qohk"
# VOICE_ID = "EXAVITQu4vr4xnSDxMaL"


def mood_to_eleven_labs_voice_settings(mood: str) -> VoiceSettings:
    presets = {
        "mysterious": VoiceSettings(
            stability=45,
            similarity_boost=75,
            style=65,
            use_speaker_boost=True,
        ),
        "dramatic": VoiceSettings(
            stability=40,
            similarity_boost=80,
            style=70,
            use_speaker_boost=True,
        ),
        "inspiring": VoiceSettings(
            stability=50,
            similarity_boost=75,
            style=60,
            use_speaker_boost=True,
        ),
        "educational": VoiceSettings(
            stability=60,
            similarity_boost=70,
            style=45,
            use_speaker_boost=True,
        ),
        "energetic": VoiceSettings(
            stability=35,
            similarity_boost=80,
            style=75,
            use_speaker_boost=True,
        ),
    }

    return presets.get(
        mood,
        VoiceSettings(
            stability=55,
            similarity_boost=75,
            style=50,
            use_speaker_boost=True,
        ),
    )


def generate_scene_audio(scene: SceneSchema, session_id: str):
    print(f"Generating audio for scene: {scene.narration}")
    narration = scene.narration
     
    voice_settings = mood_to_eleven_labs_voice_settings(scene.mood)
    
    audio = elevenlabs_client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=narration,
        output_format="mp3_44100_128",
        model_id="eleven_multilingual_v2"
    )
    
    session_dir = settings.OUTPUT_DIR / f"{session_id}"
    session_dir.mkdir(exist_ok=True, parents=True)
    
    audio_path = session_dir / f"{scene.order_number}.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
            
    return audio_path