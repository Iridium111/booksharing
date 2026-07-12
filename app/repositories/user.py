from uuid import UUID

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    @staticmethod
    async def create(
            session: AsyncSession,
            user_data: UserCreate
    )-> User:
        user_dict = user_data.model_dump(exclude={"password"})
        data_user = User(**user_dict,
                         hashed_password=hash_password(user_data.password))
        session.add(data_user)
        await session.commit()
        return data_user

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
    async def find_by_email(session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def find_all(session: AsyncSession) -> Sequence[User]:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_refresh_token(session: AsyncSession,
                                   user_id: UUID,
                                   refresh_token: str | None)-> None:
        user = await session.get(User, user_id)
        if user:
            user.refresh_token = refresh_token
            await session.commit()


