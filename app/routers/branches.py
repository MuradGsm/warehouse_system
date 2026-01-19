from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.core.rbac import require_roles
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchOut
from typing import List

router = APIRouter(prefix='/branch', tags=['branch'])

@router.post('', response_model=BranchOut)
async def create_branch(
    data: BranchCreate,
    session: AsyncSession = Depends(get_session),
    user = Depends(require_roles('admin', "operator"))
):
    branch = Branch(name = data.name)
    session.add(branch)
    await session.commit()
    await session.refresh(branch)
    return branch


@router.get('', response_model=List[BranchOut])
async def list_branches(
    session: AsyncSession = Depends(get_session),
    user = Depends(require_roles('admin', 'operator', 'manager')),
):
    res = await session.execute(select(Branch).where())
    return res.scalars().all()

@router.get('\{branch_id}', response_model=BranchOut)
async def get_branch(
    branch_id: int, 
    session: AsyncSession = Depends(get_session),
    user = Depends(require_roles('admin', 'operator', 'manager')),
):
    branch = (await session.execute(select(Branch).where(Branch.id == branch_id))).scalar_one_or_none()
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch