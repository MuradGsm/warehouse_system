from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.core.rbac import require_roles
from app.schemas.transfer import (TransferCreate, TransferOut, DispatchRequest, ReceiveRequest)
from app.models.transfer import Transfer

from app.services.transfers import create_transfer, dispatch_transfer, receive_transfer


router = APIRouter(prefix="/transfers", tags=["Transfers"])

@router.post("", response_model=TransferOut)
async def create(
    data: TransferCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator")),
):
    t = await create_transfer(session, operator_id=user.id, data=data)
    await session.commit()
    await session.refresh(t)
    return t

@router.get("", response_model=list[TransferOut])
async def list_transfers(
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager")),
):
    res = await session.execute(select(Transfer).order_by(Transfer.id.desc()))
    return res.scalars().all()

@router.get("/{transfer_id}", response_model=TransferOut)
async def get_one(
    transfer_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator", "manager")),
):
    t = (await session.execute(select(Transfer).where(Transfer.id == transfer_id))).scalar_one()
    return t

@router.post("/{transfer_id}/dispatch", response_model=TransferOut)
async def dispatch(
    transfer_id: int,
    data: DispatchRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "storekeeper")),
):
    t = await dispatch_transfer(session, transfer_id, actor_id=user.id, shipped_qty=data.shipped_qty, seal_number=data.seal_number, idempotency_key=data.idempotency_key)
    await session.commit()
    await session.refresh(t)
    return t

@router.post("/{transfer_id}/receive", response_model=TransferOut)
async def receive(
    transfer_id: int,
    data: ReceiveRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "storekeeper")),
):
    t = await receive_transfer(session, transfer_id, actor_id=user.id, received_qty=data.received_qty, damaged_qty=data.damaged_qty, idempotency_key=data.idempotency_key)
    await session.commit()
    await session.refresh(t)
    return t