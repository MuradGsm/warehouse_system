from pydantic import BaseModel

class TransferAssignRequest(BaseModel):
    driver_id: int | None = None
    storekeeper_from_id: int | None = None
    storekeeper_to_id: int | None = None

    