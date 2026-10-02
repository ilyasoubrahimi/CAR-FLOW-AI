from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.models.vehicle import User
from app.schemas.auth import UserLogin

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def create_admin(self, user_in: UserLogin, password_hash: str) -> User:
        user = User(
            username=user_in.username,
            hashed_password=password_hash,
            email=f"{user_in.username}@admin.marrakechdrive.com",
            full_name="Admin User",
            role="ADMIN"
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
