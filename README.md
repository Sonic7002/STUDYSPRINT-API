# StudySprint API – Focused Study Chatbot

StudySprint AI is an AI-powered chatbot API designed to help students **stay focused on studying**.
The system answers only **study-related** questions and prevents topic diversion.

Students can also **generate notes or quizzes from uploaded study material**. When a conversation is based on an uploaded document, the chatbot **locks the discussion to that material** to prevent off-topic questions.

This project was built as a **hackathon prototype** to demonstrate how AI can support **distraction-free learning**.

## Deployed link

- deployed: <https://studysprint-api-f9jd.onrender.com>
- open api docs: <https://studysprint-api-f9jd.onrender.com/docs/>

## 🚀 Core Idea

Most AI chatbots allow conversations to drift into unrelated topics.
StudyGuard AI solves this by enforcing strict **educational boundaries**.

Two interaction modes exist:

### 1️⃣ General Study Mode

Students can ask questions about academic subjects.

Examples:

- Mathematics

- Physics

- Computer Science

- History

- Literature

- Economics

The AI rejects **non-educational questions**.

### 2️⃣ Document Study Mode

Students can upload a **PDF study material** and:

- Generate **detailed notes**

- Generate **practice quizzes**

Once a document-based study session starts, the chatbot **restricts the conversation to the uploaded material**, preventing topic switching.

Example:
```
Upload: Thermodynamics.pdf
↓
Generate notes
↓
Ask questions about the document
```
If a user asks unrelated questions, the system rejects them.

## ✨ Features
### 📄 Upload Study Material

Upload **PDF study materials** for AI-assisted learning.

### 🧠 AI Generated Notes

Automatically create **structured study notes** from uploaded documents.

### 📝 Quiz Generation

Generate quizzes including:

- Multiple choice questions

- Short answer questions

- True/False questions

### 💬 Study Chatbot

Ask questions related to academic topics.

### 🎯 Topic Guard

The system prevents:

- casual chat

- entertainment questions

- unrelated topic switching

This keeps the conversation **focused on learning**.

## 🏗️ Tech Stack

**Backend**

- FastAPI

- Python

**Database**

- SQLAlchemy

- PostgreSQL (Neon)

**AI Integration**

- LLM API (Gemini)

**File Handling**

- PDF upload

- Supabase cloud storage

## ⚙️ Installation
### Clone the repository
```bash
git clone https://github.com/yourusername/studyguard-ai.git
cd STUDYSPRINT-API
```
### Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### ▶️ Running the Server
```bash
uvicorn app.main:app --reload
```
### API docs:
```
http://127.0.0.1:8000/docs
```

## 🔒 AI Guardrails

The AI is instructed to:

- Answer **only educational questions**

- Ignore **topic switching**

- Stay **focused on study material when provided**


### 📄 File Storage

Uploaded files are stored in the **cloud** via **Supabase**.

Only **PDF files are accepted**.

### 💡 Future Improvements

Possible improvements include:

- Vector search for better document question answering

- Flashcard generation

- OCR support for scanned PDFs

- Multi-document study sessions

### 👨‍💻 Author

Built as a hackathon project exploring AI-powered study assistants.

**Srijan Kargupta (c) 2026**