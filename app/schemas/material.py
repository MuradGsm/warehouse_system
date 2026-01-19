from pydantic import BaseModel


class MaterialCreate(BaseModel):
    name: str
    category: str
    unit: str



class MaterialOut(BaseModel):
    id: int
    name: str
    category: str
    unit: str
    is_active: bool

    class Config:
        from_attributes = True