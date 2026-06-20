from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence

from app.models import Book
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    @staticmethod
    async def create(
            session: AsyncSession,
            book_data: BookCreate
    )-> Book:
        db_book = Book(**book_data.model_dump())
        session.add(db_book)
        await session.commit()
        return db_book

    @staticmethod
    async def find_all(
            session: AsyncSession,
    ) -> Sequence[Book]:            # Sequence - последовательность, что это?
        stmt = select(Book)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def find_by_id(
            session: AsyncSession,
            book_id: UUID
    ) -> Book | None:
        stmt = select(Book).where (Book.id == book_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update(
            session: AsyncSession,
            book_id: UUID,
            book_data: BookUpdate
    ) -> Book | None:
        db_book = await BookRepository.find_by_id(session, book_id)
        if db_book is None:
            return None

        update_data = book_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_book, field, value)

        await session.commit()
        await session.refresh(db_book)
        return db_book

    @staticmethod
    async def delete(
            session: AsyncSession,
            book_id: UUID
    ) -> Book | None:
        db_book = await BookRepository.find_by_id(session, book_id)
        if db_book is None:
            return None
        await session.delete(db_book)
        await session.commit()

        return db_book