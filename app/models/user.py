from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base import Base

class User(Base):
    __tablename__='users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(String(50), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    
