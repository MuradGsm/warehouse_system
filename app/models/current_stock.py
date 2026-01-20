from datetime import datetime
from sqlalchemy import Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CurrentStock(Base):
    __tablename__ = 'current_stock'

    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), primary_key=True)

    on_hand_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)

    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 