from uuid import UUID

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import session
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    @staticmethod
    async def create(session: AsyncSession, user_data: UserCreate) -> User:
        db_user = User(**user_data.model_dump()) # User(username="Alex", email="alex@mail.ru")
        session.add(db_user)
        await session.commit()
        return db_user

    @staticmethod
    async def find_by_username(session: AsyncSession, username: str)-> User | None:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()  # либо найдем, либо None


    @staticmethod
    async def find_by_uuid(session: AsyncSession, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() # либо найдем, либо None


    @staticmethod
    async def find_all(session: AsyncSession) -> Sequence[User]:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()