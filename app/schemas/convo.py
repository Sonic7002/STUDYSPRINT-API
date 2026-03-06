from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ValidationInfo, field_validator
from typing import Optional

class ConvoCreate(BaseModel):
    data : str

    @field_validator("data")
    @classmethod
    def not_empty(cls, text: str, info: ValidationInfo):
        if not text.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return text
    
class ConvoRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime

class ConvoPatch(BaseModel):
    name: Optional[str] = None