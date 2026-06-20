from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.core.database import get_async_session
from app.repositories.book import BookRepository
from app.schemas.book import BookResponse, BookCreate, BookUpdate

# APIRouter - ?
# prefix - "/" по сути /books, проще написать так если нужен атрибут /{book_id}
# tags - то, как выглядит в сваггере
router = APIRouter(prefix='/books', tags=['Books'])

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(get_async_session)):
    return await BookRepository.create(session, book_data)

@router.get("/", response_model=list[BookResponse], status_code=200)
async def get_books(session: AsyncSession = Depends(get_async_session)):
    return await BookRepository.find_all(session)       # Нужен ли тут id?

@router.patch("/{book_id}", response_model=BookResponse, status_code=200)
async def update_book(
        book_id: UUID,
        book_data: BookUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    db_book = await BookRepository.update(
        session,
        book_id,
        book_data
    )
    if db_book is None:
        raise HTTPException(status_code=404,
                            detail="Book not found")
    return db_book

@router.delete("/{book_id}", response_model=BookResponse, status_code=200)
async def delete_book(
        book_id: UUID,
        session: AsyncSession = Depends(get_async_session)
):
    return await BookRepository.delete(session, book_id)