from uuid import UUID

from pydantic import BaseModel, ConfigDict

class OwnerResponse(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str


class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    genre: str
    user: OwnerResponse

    model_config = ConfigDict(from_attributes=True)  # Дословно - можешь брать из атрибутов значения


class BookUpdate(BaseModel):
    title: str | None
    author: str | None

