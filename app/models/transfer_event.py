from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TransferEvent(Base):
    __tablename__ = 'transfer_events'

    id: Mapped[int] = mapped_column(primary_key=True)

    transfer_id: Mapped[int] = mapped_column(ForeignKey('transfers.id'), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    event_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(200), unique=True, nullable=True)
    