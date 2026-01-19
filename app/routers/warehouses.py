from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.warehouse import Warehouse
from app.models.branch import Branch
from app.schemas.warehouse import WarehouseCreate, WarehouseOut
from app.core.rbac import require_roles

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])

@router.post("", response_model=WarehouseOut)
async def create_warehouse(
    data: WarehouseCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator")),
):
    branch = (await session.execute(select(Branch).where(Branch.id == data.branch_id))).scalar_one_or_none()
    if not branch:
        raise HTTPException(400, "Branch does not exist")

    w = Warehouse(branch_id=data.branch_id, name=data.name, address=data.address)
    session.add(w)
    await session.commit()
    await session.refresh(w)
    return w

@router.get("", response_model=list[WarehouseOut])
async def list_warehouses(
    branch_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager")),
):
    stmt = select(Warehouse)
    if branch_id is not None:
        stmt = stmt.where(Warehouse.branch_id == branch_id)
    stmt = stmt.order_by(Warehouse.id)

    res = await session.execute(stmt)
    return res.scalars().all()

@router.get("/{warehouse_id}", response_model=WarehouseOut)
async def get_warehouse(
    warehouse_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager")),
):
    w = (await session.execute(select(Warehouse).where(Warehouse.id == warehouse_id))).scalar_one_or_none()
    if not w:
        raise HTTPException(404, "Warehouse not found")
    return w
