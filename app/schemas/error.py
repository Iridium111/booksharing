from datetime import datetime

from typing import Any
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Детали конкретной ошибки """
    field: str |  None = None
    message: str
    message: Any
    code: str | None = None


class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""
    status: str = "error"
    status_code: int
    message: str
    details: list[ErrorDetail] = []
    timestamp: str
    path: str | None = None
    request_id: str | None = None




