from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Msg(Base):
    __tablename__ = "msgs"

    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable= False)
    convo_id: Mapped[str] = mapped_column(ForeignKey("convos.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = datetime.utcnow, nullable = False)
