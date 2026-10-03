from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core import security
from app.repositories.user import UserRepository
from app.models.vehicle import User, UserRole

async def get_current_user(
    token: str = Depends(security.oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    repo = UserRepository(db)
    user = await repo.get_by_id(payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    return user

async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required"
        )
    return current_user
