from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    branch_id: int
    name: str
    address: str | None = None


class WarehouseOut(BaseModel):
    id: int
    branch_id: int
    name: str
    address: str | None = None
    is_active: bool

    class Config:
        from_attributes = True
