from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_session
from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialOut
from app.core.rbac import require_roles


router = APIRouter(prefix='/materials', tags=['materials'])

@router.post('', response_model=MaterialOut)
async def create_material(
    data: MaterialCreate,
    session: AsyncSession = Depends(get_session),
    user = Depends(require_roles('admin', 'operator'))
):
    m = Material(name=data.name, category=data.category, unit=data.unit)
    session.add(m)
    await session.commit()
    await session.refresh(m)

    return m

@router.get('', response_model=List[MaterialOut])
async def list_materials(
    q: str | None = Query(default=None, description="search by name"),
    session: AsyncSession = Depends(get_session),
    user = Depends(require_roles('admin', 'operator', 'manager'))
):
    stmt = select(Material)
    if q: 
        stmt = stmt.where(Material.name.ilike(f'%{q}%'))
    stmt = stmt.order_by(Material.id)

    res = await session.execute(stmt)

    return res.scalars().all()

@router.get("/{material_id}", response_model=MaterialOut)
async def get_material(
    material_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager")),
):
    m = (await session.execute(select(Material).where(Material.id == material_id))).scalar_one_or_none()
    if not m:
        raise HTTPException(404, "Material not found")
    return m