import uuid
from langgraph.graph import END, START, StateGraph
from langgraph.managed.base import V
from app.common.utils import get_url_from_s3_key
from app.database import get_db_session
from app.langgraph_workflows.services.image_service import ImageService
from app.langgraph_workflows.services.voice_service import VoiceService
from app.langgraph_workflows.states import ScriptToVideoState
from app.langgraph_workflows.schemas import GeneratedSceneListSchema, SceneListSchema, SceneSchema
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import logging

from app.video.models import Scene, Video, VideoStatus

logger = logging.getLogger(__name__)

class ScriptToVideo:
    def __init__(self):
        self.graph= None

    def _generate_scenes_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
        logger.info(f"Generating scenes for video: {state.video_id}")
        SYSTEM_PROMPT = """
            You are a professional short-form video director and storyboard artist.

            Your task is to convert a narrated script into a sequence of visually engaging scenes for a faceless video.

            The output will be used to generate AI images or short video clips that match the narration and pacing.

            RULES:
            - Break the script into clear, sequential scenes.
            - Each scene must represent a single visual idea.
            - Scenes must flow naturally and follow the order of the script.
            - Do NOT include on-screen humans unless explicitly implied by the narration.
            - Optimize pacing for short-form content (TikTok, Reels, Shorts).

            FOR EACH SCENE, GENERATE:
            - narration: The exact line or sentence spoken in that scene (do not rewrite unless necessary for clarity).
            - visual_prompt: A concise but vivid description of what should be shown visually.
            - duration_seconds: Estimated duration (between 2 and 6 seconds).
            - visual_type: One of ["image", "video"].
            - mood: One of ["dramatic", "mysterious", "inspiring", "educational", "energetic"].

            CONSTRAINTS:
            - Avoid repeating the same visual concept across scenes.
            - Prefer abstract, symbolic, historical, animated, or environment-focused visuals.
            - Assume visuals will be generated without showing a narrator or presenter.
            - Keep prompts suitable for a general audience.

            OUTPUT FORMAT:
            Return valid JSON only, with the following structure:

            {
                "scenes": [
                    {
                    "order_number": 1,
                    "narration": "",
                    "visual_prompt": "",
                    "duration_seconds": 0,
                    "visual_type": "",
                    "mood": ""
                    }
                ]
            }
        """
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        structured_llm = llm.with_structured_output(GeneratedSceneListSchema)
        response = structured_llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=state.script)])
        
        scenes = [SceneSchema(**scene.model_dump()) for scene in response.scenes]
        
        with get_db_session() as db:
            video = db.query(Video).filter(Video.id == state.video_id).first()
            if video and video.status == VideoStatus.pending:
                video.status= VideoStatus.processing
                db.commit()
                
        logger.info(f"Scenes generated for video: {state.video_id} successfully")
        return ScriptToVideoState(script=state.script, scenes=scenes, video_id=state.video_id)
    
    def _generate_audio_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
        logger.info(f"Generating audio for video: {state.video_id}")
        voice_service= VoiceService(scenes=state.scenes, video_id=state.video_id)
        final_audio_key = voice_service.generate_scenes_audio()
          
        logger.info(f"Audio generated for video: {state.video_id} successfully")
        return ScriptToVideoState(script=state.script, scenes=voice_service.scenes, video_id=state.video_id, final_audio_key=final_audio_key)
    
    def _generate_images_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
        logger.info(f"Generating images for video: {state.video_id}")
        image_service = ImageService(scenes=state.scenes)
        image_service.generate_images()
        
        logger.info(f"Images generated for video: {state.video_id} successfully")
        return ScriptToVideoState(script=state.script, scenes=image_service.scenes, video_id=state.video_id, final_audio_key=state.final_audio_key)
    
    def _persist_results_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
        logger.info(f"Persisting results for video: {state.video_id} to database")
        with get_db_session() as db:
            video = db.query(Video).filter(Video.id == state.video_id).first()
            if video and video.status == VideoStatus.processing:
                video.status = VideoStatus.completed
                video.final_audio_key = state.final_audio_key
                video.final_audio_url = get_url_from_s3_key(state.final_audio_key)
                db.commit()
                
                for scene in state.scenes:
                    scene_model = Scene(
                        order_number = scene.order_number,
                        video_id = state.video_id,
                        media_type = scene.visual_type,
                        narration = scene.narration,
                        duration_seconds = scene.duration_seconds,
                        visual_prompt = scene.visual_prompt,
                        mood = scene.mood,
                        audio_url = scene.audio_url,
                        audio_file_key = scene.audio_file_key,
                        image_url = scene.image_url,
                        image_file_key = scene.image_file_key,
                        video_url = scene.video_url,
                        video_file_key = scene.video_file_key,
                    )
                    db.add(scene_model)
                db.commit()
                
        logger.info(f"Results persisted for video: {state.video_id} successfully")
        return ScriptToVideoState(script=state.script, scenes=state.scenes, video_id=state.video_id, final_audio_key=state.final_audio_key)

    def build_graph(self):
        graph_builder = StateGraph(ScriptToVideoState)
        graph_builder.add_node("generate_scenes", self._generate_scenes_node)
        
        graph_builder.add_edge(START, "generate_scenes")
        graph_builder.add_node("generate_audio", self._generate_audio_node)
        
        graph_builder.add_edge("generate_scenes", "generate_audio")
        
        graph_builder.add_node("generate_images", self._generate_images_node)
        
        graph_builder.add_edge("generate_audio", "generate_images")
        
        graph_builder.add_node("persist_results", self._persist_results_node)
        
        graph_builder.add_edge("generate_images", "persist_results")
        
        graph_builder.add_edge("persist_results", END)
                
        self.graph = graph_builder.compile()
        return self.graph