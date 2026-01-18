from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

from app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    