from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_session
from app.core.rbac import require_roles
from app.schemas.transfer import (TransferCreate, TransferOut, DispatchRequest, ReceiveRequest)
from app.schemas.transfer_event import TransferEventOut
from app.schemas.transfer_assign import TransferAssignRequest
from app.models.transfer import Transfer
from app.models.transfer_event import TransferEvent

from app.services.transfers import create_transfer, dispatch_transfer, receive_transfer, assign_transfer


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

@router.get('/{transfer_id}/events', response_model=List[TransferEventOut])
async def list_events(
    transfer_id: int,
    session: AsyncSession = Depends(get_session),
    user= Depends(require_roles("admin", "operator", "manager", "storekeeper", "driver"))
):
    res = await session.execute(select(TransferEvent).where(TransferEvent.transfer_id == transfer_id).order_by(TransferEvent.id.asc()))
    return res.scalars().all()

@router.post("/{transfer_id}/assign", response_model=TransferOut)
async def assign(
    transfer_id: int,
    data: TransferAssignRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("admin", "operator")),
):
    t = await assign_transfer(session, transfer_id=transfer_id, actor_id=user.id, data=data)
    await session.commit()
    await session.refresh(t)
    return t