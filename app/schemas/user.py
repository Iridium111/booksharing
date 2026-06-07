from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):   # Ответ
    id: UUID

    model_config = ConfigDict(from_attributes=True)     # Подтянет каждый атрибут на место своих значений


