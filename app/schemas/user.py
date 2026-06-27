from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):   # Ответ
    id: UUID

    model_config = ConfigDict(from_attributes=True)     # Подтянет каждый атрибут на место своих значений

class LoginRequest(BaseModel):
    """Запрос на логин."""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Ответ с токенами при логине или рефреше."""
    access_token: str
    refresh_token: str

class RefreshResponse(BaseModel):
    """Запрос на обновление access token."""
    refresh_token: str