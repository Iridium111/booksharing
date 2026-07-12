from sqlalchemy import MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID


NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class BaseModel(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(BaseModel):
    __abstract__ = True # Эта таблица не для создания, а для наследовния
    __mapper_args__ = {
        "eager_defaults": True,
    }

    id: Mapped[UUID] = mapped_column(   # UUID - почитать
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

