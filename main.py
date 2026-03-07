from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import docfile, user, msg, convo, auth, health
from app.db.base import Base
from app.db.session import engine
import os

Base.metadata.create_all(bind=engine)
app = FastAPI(title="STUDY SPRINT API")

origins = os.getenv("ALLOWED_ORIGINS", "*")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(user.router, prefix="/api/v1")
app.include_router(msg.router, prefix="/api/v1")
app.include_router(convo.router, prefix="/api/v1")
app.include_router(docfile.router, prefix="/api/v1")
app.include_router(auth.router)
app.include_router(health.router)