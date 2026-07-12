import os.path
import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import User

from app.core.database import get_async_session
from app.repositories.book import BookRepository
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.core.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix='/books', tags=['Books'])

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)):
    return await BookRepository.create(
        session,
        book_data,
        current_user.id)

@router.get("/", response_model=list[BookResponse], status_code=200)
async def get_books(session: AsyncSession = Depends(get_async_session),
                    author: str | None = None,
                    owner: str | None = None,
                    genre: str |None = None,
                    limit: int = 10,
                    offset: int = 0):
    return await BookRepository.find_all(session=session,
                                         author=author,
                                         owner=owner,
                                         genre=genre,
                                         limit=limit,
                                         offset=offset)

@router.patch("/{book_id}", response_model=BookResponse, status_code=200)
async def update_book(
        book_id: UUID,
        book_data: BookUpdate,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):

    db_book = await BookRepository.find_by_id(session, book_id)
    if db_book is None:
        raise HTTPException(status_code=404,
                            detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="User not allowed")

    return await BookRepository.update(session=session, db_book=db_book, book_data=book_data)

@router.delete("/{book_id}", response_model=BookResponse, status_code=200)
async def delete_book(
        book_id: UUID,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_user)
):
    db_book = await BookRepository.find_by_id(session, book_id)
    if db_book is None:
        raise HTTPException(status_code=404,
                            detail="Book not found")

    if current_user.id != db_book.user_id:
        raise HTTPException(status_code=403,
                            detail="User not allowed")

    return await BookRepository.delete(session=session, db_book=db_book)

@router.post("/{book_id}/cover/upload", response_model=BookResponse)
async def upload(file: UploadFile,
                 book_id: UUID,
                 session: AsyncSession = Depends(get_async_session),
                 current_user: User = Depends(get_current_user)):
    allowed_content_types = {"image/png", "image/jpeg", "image/webp"}
    max_file_size = 5 * 1024 * 1024

    current_book = await BookRepository.find_by_id(session, book_id)
    if current_book is None:
        raise HTTPException(status_code=404,
                            detail="Book not found.")

    if current_user.id != current_book.user_id:
        raise HTTPException(status_code=403,
                            detail="User not allowed")

    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400,
                            detail="Invalid file type.")

    if file.size > max_file_size:
        raise HTTPException(status_code=400,
                            detail="File too large.")

    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

    content = await file.read()
    file_ext = file.filename.split(".")[-1]

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        f"{uuid.uuid4()}.{file_ext}"
    )
    with open(file_path, "wb") as f:
        f.write(content)

    updated_book = await BookRepository.set_cover_url(
        session=session,
        db_book=current_book,
        cover_url=file_path
    )

    return updated_book
