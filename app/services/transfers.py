import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import timezone

from app.models.transfer import Transfer
from app.models.transfer_event import TransferEvent
from app.models.current_stock import CurrentStock


async def _get_or_create_stock(session: AsyncSession, warehouse_id: int, material_id: int) -> CurrentStock:
    stock = (
        await session.execute(
            select(CurrentStock).where(
                CurrentStock.warehouse_id == warehouse_id,
                CurrentStock.material_id == material_id
            )
        )
    ).scalar_one_or_none()

    if stock:
        return stock
    stock = CurrentStock(warehouse_id=warehouse_id, material_id=material_id, on_hand_qty=0)
    session.add(stock)
    await session.flush()

    return stock

async def _ensure_idempotent(session: AsyncSession, idempotency_key: str) -> None:
    exists = (
        await session.execute(
            select(TransferEvent.id).where(TransferEvent.idempotency_key == idempotency_key)
        )
    ).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate request (idempotency key already used)")

def _to_naive_utc(dt):
    """Accepts datetime or None. Returns naive datetime in UTC."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

async def create_transfer(session: AsyncSession, operator_id: int, data) -> Transfer:
    deadline = _to_naive_utc(data.deadline_at)

    t = Transfer(
        from_warehouse_id=data.from_warehouse_id,
        to_warehouse_id=data.to_warehouse_id,
        material_id=data.material_id,
        planned_qty=data.planned_qty,
        deadline_at=deadline,  # <-- ТОЛЬКО ТАК
        operator_id=operator_id,
        status="draft",
    )
    session.add(t)
    await session.flush()

    session.add(
        TransferEvent(
            transfer_id=t.id,
            event_type="created",
            actor_user_id=operator_id,
            payload_json=json.dumps({"planned_qty": float(data.planned_qty)}),
        )
    )
    return t

async def dispatch_transfer(session: AsyncSession, transfer_id: int, actor_id: int, shipped_qty: float, seal_number: str | None, idempotency_key: str):
    await _ensure_idempotent(session, idempotency_key)

    t =  (await session.execute(select(Transfer).where(Transfer.id == transfer_id))).scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found")
    if t.status not in ('draft', 'status'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot dispatch from status={t.status}")
    
    stock_from = await _get_or_create_stock(session, t.from_warehouse_id, t.material_id)
    if float(stock_from.on_hand_qty) < float(shipped_qty):
        raise HTTPException(400, "Not enough stock to dispatch")
    
    stock_from.on_hand_qty = float(stock_from.on_hand_qty) - float(shipped_qty)

    t.status = 'in_transit'

    if seal_number:
        t.seal_number = seal_number
    t.storekeeper_from_id = actor_id

    session.add(
        TransferEvent(
            transfer_id=t.id,
            event_type="pickup_confirmed",
            actor_user_id=actor_id,
            idempotency_key=idempotency_key,
            payload_json=json.dumps({"shipped_qty": float(shipped_qty), "seal_number": seal_number}),
        )
    )

    return t

async def receive_transfer(session: AsyncSession, transfer_id: int, actor_id: int, received_qty: float, damaged_qty: float, idempotency_key: str):
    await _ensure_idempotent(session, idempotency_key)

    t = (await session.execute(select(Transfer).where(Transfer.id == transfer_id))).scalar_one_or_none()
    if not t:
        raise HTTPException(404, "Transfer not found")
    if t.status != "in_transit":
        raise HTTPException(400, f"Cannot receive from status={t.status}")

    stock_to = await _get_or_create_stock(session, t.to_warehouse_id, t.material_id)
    stock_to.on_hand_qty = float(stock_to.on_hand_qty) + float(received_qty)

    t.storekeeper_to_id = actor_id

    if float(received_qty) == float(t.planned_qty) and float(damaged_qty) == 0:
        t.status = "received"
        event_type = "delivery_confirmed"
    else:
        t.status = "discrepancy"
        event_type = "delivery_with_discrepancy"

    session.add(
        TransferEvent(
            transfer_id=t.id,
            event_type=event_type,
            actor_user_id=actor_id,
            idempotency_key=idempotency_key,
            payload_json=json.dumps({"received_qty": float(received_qty), "damaged_qty": float(damaged_qty)}),
        )
    )

    return t