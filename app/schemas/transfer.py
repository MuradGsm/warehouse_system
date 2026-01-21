from pydantic import BaseModel
from datetime import datetime


class TransferCreate(BaseModel):
    from_warehouse_id: int
    to_warehouse_id: int
    material_id: int
    planned_qty: float
    deadline_at: datetime | None = None


class TransferOut(BaseModel):
    id: int
    from_warehouse_id: int
    to_warehouse_id: int
    material_id: int
    planned_qty: float
    status: str
    operator_id: int

    driver_id: int | None = None
    storekeeper_from_id: int | None = None
    storekeeper_to_id: int | None = None
    seal_number: str | None = None
    deadline_at: datetime | None = None

    class Config:
        from_attributes = True


class DispatchRequest(BaseModel):
    shipped_qty: float
    seal_number: str | None = None
    idempotency_key: str

class ReceiveRequest(BaseModel):
    received_qty: float
    damaged_qty: float = 0
    idempotency_key: str