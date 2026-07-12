

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.deps import get_current_user
from app.models import User
from app.repositories.user import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

from starlette import status

from app.core.database import get_async_session
from app.schemas.user import UserResponse, UserCreate, TokenResponse, LoginRequest, RefreshResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)

async def register_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    existing_user = await UserRepository.find_by_email(session, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    existing_user = await UserRepository.find_by_username(session, username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(
        credentials: LoginRequest,
        session: AsyncSession = Depends(get_async_session)
):
    user = await UserRepository.find_by_username(session, username=credentials.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    await UserRepository.update_refresh_token(session, user.id, refresh_token)


    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/logout")
async def logout(
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)):
    await UserRepository.update_refresh_token(session, current_user.id, refresh_token=None)
    return {"message": "Successfully logged out."}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
        request: RefreshResponse,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        payload = decode_token(request.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    existing_user = await UserRepository.find_by_uuid(session, user_id=user_uuid)
    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if request.refresh_token != existing_user.refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token({"sub": str(existing_user.id)})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=request.refresh_token
    )
