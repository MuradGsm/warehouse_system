from pydantic import BaseModel

class BranchCreate(BaseModel):
    name: str

class BranchOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
