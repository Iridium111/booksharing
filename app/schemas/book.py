from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str

class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str

    model_config = ConfigDict(from_attributes=True)  # Дословно - можешь брать из атрибутов значения

class BookUpdate(BaseModel):
    title: str | None
    author: str | None
