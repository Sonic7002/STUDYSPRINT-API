from uuid import uuid4, UUID as PyUUID
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base
from ..core.security import hash_password

class User(Base):
    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(UUID, primary_key = True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(225), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    def set_password(self, password: str):
        self.hashed_password = hash_password(password)
