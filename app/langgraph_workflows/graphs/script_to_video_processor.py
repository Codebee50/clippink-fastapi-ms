import uuid
from langgraph.graph import END, START, StateGraph
from app.langgraph_workflows.services import generate_scene_audio
from app.langgraph_workflows.states import ScriptToVideoState
from app.langgraph_workflows.schemas import SceneListSchema
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class ScriptToVideo:
    def __init__(self):
        self.graph= None

    def _generate_scenes_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
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
        structured_llm = llm.with_structured_output(SceneListSchema)
        response = structured_llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=state.script)])
        return ScriptToVideoState(script=state.script, scenes=response.scenes)
    
    
    def _generate_eleven_labs_audio_node(self, state: ScriptToVideoState) -> ScriptToVideoState:
        print("Generating audio for the scenes...")
        session_id = str(uuid.uuid4())
        for scene in state.scenes:
            audio_path = generate_scene_audio(scene, session_id)
            print("Generated audio for scene: ", scene.order_number, "at: ", audio_path)
            
        return ScriptToVideoState(script=state.script, scenes=state.scenes)

    def build_graph(self):
        graph_builder = StateGraph(ScriptToVideoState)
        graph_builder.add_node("generate_scenes", self._generate_scenes_node)
        
        graph_builder.add_edge(START, "generate_scenes")
        graph_builder.add_node("generate_eleven_labs_audio", self._generate_eleven_labs_audio_node)
        
        graph_builder.add_edge("generate_scenes", "generate_eleven_labs_audio")
        
        graph_builder.add_edge("generate_eleven_labs_audio", END)
        
        self.graph = graph_builder.compile()
        return self.graph