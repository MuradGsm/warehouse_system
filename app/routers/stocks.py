from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_session
from app.core.rbac import require_roles
from app.models.current_stock import CurrentStock
from app.schemas.stock import StockOut

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get('/', response_model=List[StockOut])
async def list_stocks(
    warehouse_id: int | None = Query(default=None),
    material_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager", "storekeeper")),
):
    stmt = select(CurrentStock)
    if warehouse_id is not None:
        stmt = stmt.where(CurrentStock.warehouse_id == warehouse_id)
    if material_id is not None:
        stmt = stmt.where(CurrentStock.material_id == material_id)

    res = await session.execute(stmt.order_by(CurrentStock.warehouse_id, CurrentStock.material_id))
    return res.scalars().all()