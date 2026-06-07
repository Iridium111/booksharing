from sqlalchemy.orm import Mapped

from app.models.base import Base
from app.models.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = 'users'

    username: Mapped[str]
    email: Mapped[str]