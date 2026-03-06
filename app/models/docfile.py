from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = datetime.utcnow, nullable = False)
