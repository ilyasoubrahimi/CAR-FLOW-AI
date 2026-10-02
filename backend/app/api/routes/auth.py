from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core import security
from app.repositories.user import UserRepository
from app.schemas.auth import Token, UserLogin, UserRead

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_username(form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserRead)
async def get_current_user(
    token: str = Depends(security.oauth2_scheme), # I'll define this in security.py
    db: AsyncSession = Depends(get_db)
):
    payload = security.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    repo = UserRepository(db)
    user = await repo.get_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
