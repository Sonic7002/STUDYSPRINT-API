from google import genai
from google.genai import types
from ..models.msg import Msg
from ..schemas.msg import MsgCreate, MsgRole

def generate_response(msgs: list[Msg]) -> MsgCreate:
    client = genai.Client()

    prompt = """You are a mental health support assistant.

    Rules:
    - You are NOT a therapist or medical professional.
    - You do NOT prescribe.
    - You provide emotional support, grounding, and coping suggestions.
    - If user expresses self-harm or suicidal intent:
    - Respond with empathy
    - Encourage seeking professional help
    - Suggest contacting local helplines
    - Do NOT provide instructions or validation for self-harm

    Tone:
    - Calm
    - Supportive
    - Non-judgmental
    - Clear and grounded

    Always prioritize user safety.
    """

    data = [
        types.Content(
            role="user",
            parts=[types.Part(text=f"INSTRUCTIONS:\n{prompt}")]
        )
    ]

    for msg in msgs:
        data.append(
            types.Content(
                role=msg.role,
                parts=[types.Part(text=msg.content)]
            )
        )

    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=data)
    reply = MsgCreate(role=MsgRole.MODEL, content=response.text)
    return reply

def generate_convo(data: str) -> str:
    client = genai.Client()
    prompt = f"""You are generating a title for a chat conversation.

Given the first message of the conversation, generate a short, clear, descriptive title.

Rules:
- Maximum 4 words
- No punctuation at the end
- No quotes
- No emojis
- No extra commentary
- Output ONLY the title

First message:
{data}"""
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    return(response.text)
