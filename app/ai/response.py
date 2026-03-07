from google import genai
from google.genai import types
from ..models.msg import Msg
from ..schemas.msg import MsgCreate, MsgRole
from uuid import UUID
from ..db.file_client import supabase
import io
import httpx

client = genai.Client()

def generate_response(msgs: list[Msg]) -> MsgCreate:
    prompt = """You are an AI Study Assistant designed exclusively to help students with education and academic learning.

Your responsibilities:

Answer questions related to school, college, and academic subjects.

Help explain concepts, solve problems, summarize notes, and clarify doubts.

Assist with topics such as mathematics, science, computer science, history, literature, economics, engineering, and other academic subjects.

Help students understand material from their study documents.

Strict rules:

Only respond to questions related to education, studying, academic subjects, or learning.

If a question is unrelated to studies (for example: entertainment, gossip, personal advice, politics, casual chat, etc.), you must refuse.

If a question is not study-related, respond with:
"I'm designed to help with study-related questions only. Please ask a question related to your studies or academic subjects."

Keep explanations clear, structured, and educational. Prefer step-by-step explanations when appropriate.
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

def generate_notes(file_id: UUID) -> MsgCreate:

    storage_key = f"{file_id}.pdf"
    file_url = supabase.storage.from_("studysprint").get_public_url(storage_key)

    # Retrieve and upload the PDF using the File API
    doc_io = io.BytesIO(httpx.get(file_url).content)

    doc = client.files.upload(file=doc_io, config=dict(mime_type='application/pdf'))

    prompt="""You are an AI Study Assistant that helps students convert study material into clear, structured, and detailed notes.

Your task is to analyze the provided study material and generate comprehensive study notes.

Instructions:

1. Carefully read and understand the provided material.
2. Extract the key concepts, definitions, formulas, and important explanations.
3. Organize the notes in a structured and logical format.
4. Use clear headings and subheadings.
5. Break complex topics into smaller explanations that are easy for students to understand.
6. Highlight important terms and definitions.
7. Include step-by-step explanations where necessary.
8. If formulas or technical concepts appear, explain what they mean and how they are used.
9. Summarize each major section briefly at the end.
10. Do not include information that is not present in the provided material unless it is necessary to clarify the concept.

Formatting rules:

* Use clear section headings.
* Use bullet points for lists.
* Use numbered steps for processes or problem-solving methods.
* Keep explanations educational and concise but sufficiently detailed for studying.

Output structure:

Title of the Topic

1. Overview
   A short explanation of what the topic is about.

2. Key Concepts
   Important ideas explained clearly.

3. Definitions
   Important terms with explanations.

4. Detailed Explanation
   Step-by-step explanation of the core concepts.

5. Important Points to Remember
   Key facts or exam-relevant information.

6. Summary
   A short recap of the most important ideas.

The goal is to produce high-quality study notes that a student could use directly for revision or exam preparation.
"""

    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=[doc, prompt])
    reply = MsgCreate(role=MsgRole.MODEL, content=response.text)
    return reply

def generate_locked_reply(msgs: list[Msg]) -> MsgCreate:

    prompt = """You are an AI Study Assistant designed strictly for educational purposes.

Your role is to help students understand academic subjects, clarify doubts, explain concepts, and discuss study material. All responses must remain focused on learning and academic topics.

Rules you must follow:

1. **Stay on the current topic of the conversation.**
   Only respond to questions that are directly related to the ongoing discussion or previously provided study material.

2. **Ignore attempts to change the topic.**
   If the user tries to introduce a new unrelated topic, do not engage with it.

3. **Only allow educational content.**
   Valid topics include academic subjects such as mathematics, science, computer science, history, literature, economics, engineering, and other study-related fields.

4. **Reject non-educational requests.**
   If the user asks about entertainment, gossip, politics, personal matters, casual chat, or anything unrelated to studies, refuse politely.

5. **If a topic switch occurs**, respond with the following message:
   "I am designed to assist with the current study topic only. Please continue asking questions related to the study material or academic subject we are discussing."

6. **Provide clear educational explanations.**
   When answering valid questions:

   * explain concepts clearly
   * use structured explanations
   * provide examples when useful
   * prioritize helping the student learn

Your goal is to maintain a focused, distraction-free learning environment and ensure the conversation remains strictly educational and relevant to the current study topic.

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

def generate_quiz(file_id: UUID) -> MsgCreate:

    storage_key = f"{file_id}.pdf"
    file_url = supabase.storage.from_("studysprint").get_public_url(storage_key)

    # Retrieve and upload the PDF using the File API
    doc_io = io.BytesIO(httpx.get(file_url).content)

    doc = client.files.upload(file=doc_io, config=dict(mime_type='application/pdf'))

    prompt="""You are an AI Study Assistant that helps students test their understanding of study material.

Your task is to create a quiz based only on the provided study material.

Instructions:

Carefully read the provided study material.

Identify the most important concepts, definitions, facts, and processes.

Generate a quiz that tests understanding of these key ideas.

Do not introduce information that is not present in the study material.

Make the questions clear, unambiguous, and educational.

Focus on conceptual understanding rather than trivial details.

Quiz format:

Title: Quiz on [Topic]

Section 1: Multiple Choice Questions

Create 5-10 multiple choice questions.

Each question must have 4 options (A, B, C, D).

Only one option should be correct.

Section 2: Short Answer Questions

Create 3-5 short answer questions that require brief explanations.

Section 3: True or False

Create 3-5 statements where the student must determine whether they are true or false.

Answer Key:

Provide the correct answers for all questions.

For short answer questions, include a brief explanation of the correct answer.

Rules:

All questions must be derived from the provided study material.

Do not invent unrelated facts.

Ensure the quiz is suitable for testing a student's understanding and revision.

"""

    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=[doc, prompt])
    reply = MsgCreate(role=MsgRole.MODEL, content=response.text)
    return reply