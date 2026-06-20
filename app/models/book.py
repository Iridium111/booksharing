from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import TimeStampMixin

class Book(Base, TimeStampMixin):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)


