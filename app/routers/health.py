from fastapi import APIRouter, Depends
from app.core.rbac import require_roles

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health():
    return {"status": "alive"}

@router.get("/admin-only")
async def admin_only(user=Depends(require_roles("admin"))):
    return {"ok": True, "user": user.email}