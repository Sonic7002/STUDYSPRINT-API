from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo
from enum import Enum

class MsgRole(str, Enum):
    MODEL = "model"
    USER = "user"

class MsgCreate(BaseModel):
    role: MsgRole
    content: str

    @field_validator("content")
    @classmethod
    def not_empty(cls, text: str, info: ValidationInfo):
        if not text.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return text
    
class MsgDelete(BaseModel):
    msg_id: UUID
    convo_id: UUID

class MsgRead(BaseModel):
    id: UUID
    user_id: UUID
    convo_id: UUID
    role: MsgRole
    content: str
    created_at: datetime
