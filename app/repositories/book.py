from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm import selectinload

from app.models import Book, User
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    @staticmethod
    async def create(
            session: AsyncSession,
            book_data: BookCreate,
            user_id: UUID
    )-> Book:
        db_book = Book(**book_data.model_dump(), user_id=user_id)
        session.add(db_book)
        await session.commit()
        return db_book

    @staticmethod
    async def find_all(
            session: AsyncSession,
            author: str | None = None,
            owner: str | None = None,
            genre: str | None = None
    ) -> Sequence[Book]:
        stmt = select(Book).options(selectinload(Book.user))

        if author is not None:
            """ Поиск по автору книг. """
            stmt = stmt.where(Book.author.ilike(f"%{author}%"))

        if owner is not None:
            """ Поиск по владельцу книг. """
            stmt = stmt.join(Book.user).where(User.username == owner)

        if genre is not None:
            """ Поиск по жанру книги. """
            stmt = stmt.where(Book.genre.ilike(genre))

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def find_by_id(
            session: AsyncSession,
            book_id: UUID
    ) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update(
            session: AsyncSession,
            db_book: Book,
            book_data: BookUpdate,
    ) -> Book:
        update_data = book_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_book, field, value)

        await session.commit()
        await session.refresh(db_book)
        return db_book

    @staticmethod
    async def delete(
            session: AsyncSession,
            db_book: Book
    ) -> Book:

        await session.delete(db_book)
        await session.commit()

        return db_book