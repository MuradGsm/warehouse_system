from pydantic import BaseModel
from datetime import datetime


class TransferEventOut(BaseModel):
    id: int
    transfer_id: int
    event_type: str
    actor_user_id: int
    event_time: datetime
    payload_json: str | None
    idempotency_key: str | None

    class Config:
        from_attributes = True

