from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(nullable=True, default=None)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    books = relationship("Book", back_populates="user")


