from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import User

from app.core.database import get_async_session
from app.repositories.book import BookRepository
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.core.exceptions import ResourceNotFound
from app.core.deps import get_current_user

router = APIRouter(prefix='/books', tags=['Books'])

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)):    # Как работает get_current_user?
    return await BookRepository.create(
        session,
        book_data,
        current_user.id)

@router.get("/", response_model=list[BookResponse], status_code=200)
async def get_books(session: AsyncSession = Depends(get_async_session),
                    author: str | None = None,
                    owner: str | None = None,
                    genre: str |None = None):
    return await BookRepository.find_all(session=session,
                                         author=author,
                                         owner=owner,
                                         genre=genre)
    # raise ResourceNotFound(resource="Book", detail={"book_id": 1})

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