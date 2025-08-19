from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, func
from datetime import datetime
from app.db.session import Base
from app.models.user import User

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False) # Clave Foranea hacia users.id
    user: Mapped["User"] = relationship("User", back_populates="token")

    token_hash: Mapped[str] = mapped_column(String(255), unique=True , nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    ip_address: Mapped[str] = mapped_column(String(45), nullable=True) # IPv4 or IPv6
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
