import os.path
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, HTTPException, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.core.config import settings

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)  # 201 - ресурс создан
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await UserRepository.create(session, user_data)

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK) # 200 - положительный ответ
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return await UserRepository.find_all(session)

@router.post("/avatar/upload")
async def upload(files: Annotated[list[UploadFile], File()], file: UploadFile):
    allowed_content_types = {"image/png", "image/jpeg", "image/webp"}
    max_file_size = 5 * 1024 * 1024 # % Mb

    if file.content_type not in allowed_content_types:
        print(file.content_type)
        raise HTTPException(400, "Invalid content type.")

    if file.size > max_file_size:
        raise HTTPException(400, "File too large.")

    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

    content = await file.read()
    file_ext = file.filename.split(".")[-1]

    file_path = os.path.join(settings.UPLOAD_DIR, str(f"{uuid.uuid4()}.{file_ext}"))
    with open(file_path, "wb") as f:
        f.write(content)

        # Импорт списка файлов
    for f in files:
        print(f.filename)

    return {"filename": file.filename, "content_type": file.content_type,
            "file_size": file.size}

"""
типы HTTP-запросов
GET - получить данные с сервера (просмотр)
POST - отправить данные на сервер 
PATCH - частично изменить объект на сервере 
PUT - полностью обновить или заменить объект на сервере 
DELETE - удалить объект на сервере 
"""

"domen.ru/api/v1/users"

