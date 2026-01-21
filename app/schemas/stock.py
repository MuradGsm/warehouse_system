from pydantic import BaseModel
from datetime import datetime


class StockOut(BaseModel):
    warehouse_id: int
    material_id: int
    on_hand_qty: float
    updated_at: datetime

    class Config:
        from_attributes = True
        