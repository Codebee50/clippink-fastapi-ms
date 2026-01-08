from app.langgraph_workflows.schemas import SceneSchema, SceneListSchema
from app.langgraph_workflows.states import ScriptToVideoState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def generate_scenes_node(state: ScriptToVideoState) -> ScriptToVideoState:
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