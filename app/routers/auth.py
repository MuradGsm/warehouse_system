from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token, verify_password
from app.core.config import settings

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=TokenResponse)
async def login(data:LoginRequest, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.email == data.email, User.is_active == True)
    user = (await session.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token(subject=str(user.id), expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return TokenResponse(access_token=token)

