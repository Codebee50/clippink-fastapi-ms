import logging
from elevenlabs import ElevenLabs, VoiceSettings
from pydub import AudioSegment
from app.common.utils import get_url_from_s3_key
from app.langgraph_workflows.schemas import SceneSchema
import uuid
from app.config import settings
from typing import Tuple
import io
import json
elevenlabs_client = ElevenLabs(api_key=settings.ELEVEN_LABS_API_KEY)
VOICE_ID = "j9jfwdrw7BRfcR43Qohk"

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self, scenes: list[SceneSchema]=None, video_id: str=None):
        self.scenes = scenes
        self.video_id = video_id
    
    def _upload_audio_chunk_to_s3(self, audio_bytes: bytes, mark_final: bool=False)-> Tuple[str, str]:
        try:
            s3_client = settings.get_s3_client()
        except Exception as e:
            pass
        
        key = f"audios/{self.video_id}/{'final_' if mark_final else ''}{uuid.uuid4()}.mp3"
        s3_client.put_object(
            Bucket = settings.AWS_BUCKET_NAME,
            Key = key,
            Body = audio_bytes,
            ContentType = "audio/mpeg"
        )
        
        return key, get_url_from_s3_key(key)
        
    
    def generate_scenes_audio(self) -> str:
        if not self.scenes:
            raise ValueError("Expected scenes, got None")
        if not self.video_id:
            raise ValueError("Expected video_id, got None")
        
        return self._generate_scenes_audio_eleven_labs()
    
    def _generate_scenes_audio_eleven_labs(self) -> str:
        final_audio = AudioSegment.empty()
        
        for scene in sorted(self.scenes, key=lambda x: x.order_number):
            print(f"Generating audio for scene: {scene.narration}")
            narration = scene.narration
            
            #note: eleven labs yields audio data as an iterable of chunks
            response = elevenlabs_client.text_to_speech.convert_with_timestamps(
                voice_id=VOICE_ID,
                text=narration,
                output_format="mp3_44100_128",
                model_id="eleven_multilingual_v2",
                # voice_settings=voice_settings
            )
            
            import base64
            
            audio_bytes = base64.b64decode(response.audio_base_64)
            # audio_bytes = b"".join(chunk for chunk in response.audio_base_64)
            alignment = response.alignment
            
            word_timings = self._process_alignment_to_word_timings(alignment, narration)
            print(f"Word timings for scene: {scene.narration} are: {json.dumps(word_timings, indent=4)}")

            audio_file_key, audio_url = self._upload_audio_chunk_to_s3(audio_bytes, scene.order_number)
            
            print(f"Uploaded audio chunk for scene: {scene.narration} to s3 at url: {audio_url}")

            
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
            final_audio += audio_segment
            
            scene.audio_file_key = audio_file_key
            scene.audio_url = audio_url
            
            scene.duration_seconds = len(audio_segment) / 1000.0
            scene.captions = word_timings
    
        final_audio_buffer =  io.BytesIO()
        final_audio.export(final_audio_buffer, format="mp3", bitrate="128k")
        final_audio_buffer.seek(0)
            
        final_audio_key, _ = self._upload_audio_chunk_to_s3(final_audio_buffer.read(), mark_final=True)
        
        print(f"Final audio for video: {self.video_id} successfully uploaded to s3 at url: {get_url_from_s3_key(final_audio_key)}")
        return final_audio_key
    
    def _process_alignment_to_word_timings(self, alignment, text: str) -> list:
        if not alignment:
            return []
        
        words = text.split()
        word_timings = []
        char_index = 0
        
        for word in words:
            word_start_char = char_index
            word_end_char = char_index + len(word)
            
            if word_start_char < len(alignment.character_start_times_seconds):
                start_time = alignment.character_start_times_seconds[word_start_char]
                end_time = alignment.character_end_times_seconds[min(word_end_char -1, len(alignment.character_end_times_seconds) - 1)]
                
                word_timings.append({
                    "text": word,
                    "start": start_time,
                    "end": end_time
                })
                
                #move past the word and any whitespace 
                char_index = word_end_char
                while char_index < len(text) and text[char_index].isspace():
                    char_index += 1
            
        phrase_timings = []
        phrase_size = 3
        for i in range(0, len(word_timings), phrase_size):
            phrase_words = word_timings[i:i + phrase_size]
            phrase_timings.append({
                "text": " ".join(word["text"] for word in phrase_words),
                "start": phrase_words[0]["start"],
                "end": phrase_words[-1]["end"],
                "words": phrase_words
            })
        return phrase_timings
            