from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)  # 201 - ресурс создан
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserRepository.create(session, user_data)

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK) # 200 - положительный ответ
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return await UserRepository.find_all(session)

"""
типы HTTP-запросов
GET - получить данные с сервера (просмотр)
POST - отправить данные на сервер 
PATCH - частично изменить объект на сервере 
PUT - полностью обновить или заменить объект на сервере 
DELETE - удалить объект на сервере 
"""

"domen.ru/api/v1/users"

