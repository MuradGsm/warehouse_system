import asyncio
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASS = "admin123"
ADMIN_NAME = "Admin"


async def main():
    async with AsyncSessionLocal() as session:
        exists = (await session.execute(select(User).where(User.email == ADMIN_EMAIL))).scalar_one_or_none()
        if exists:
            print("Admin already exists")
            return

        user = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASS),
            role="admin",
            is_active=True,
        )
        session.add(user)
        await session.commit()
        print("Admin created:", ADMIN_EMAIL, ADMIN_PASS)


if __name__ == "__main__":
    asyncio.run(main())
