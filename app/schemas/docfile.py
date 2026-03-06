from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
    
class FileRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime
