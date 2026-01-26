from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transfer(Base):
    __tablename__ = 'transfers'

    __table_args__=(
        CheckConstraint('planned_qty>0', name='ck_transfers_planned_qty_positive'),
        CheckConstraint('from_warehouse_id<>to_warehouse_id', name='ck_transfers_from_to_diff')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    from_warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouses.id'), nullable=False)
    to_warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouses.id'), nullable=False)

    material_id: Mapped[int] = mapped_column(ForeignKey('materials.id'), nullable=False)

    planned_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    shipped_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    received_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    damaged_qty: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False, default=0)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default='draft')

    operator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    storekeeper_from_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    storekeeper_to_id: Mapped[int] =  mapped_column(ForeignKey('users.id'), nullable=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    seal_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)