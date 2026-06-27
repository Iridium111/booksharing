import uuid
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.core.exceptions import BookShareBaseException
from app.schemas.error import ErrorDetail, ErrorResponse


def create_request_id() -> str:
    """генерация уникального индификатора"""
    return f"req-{uuid.uuid4().hex[:8]}"

async def bookshare_exception_handler(request: Request, exc: BookShareBaseException) -> JSONResponse:
    request_id = create_request_id()

    details = []
    if exc.detail:
        for field, msg in exc.detail.items():
            details.append(ErrorDetail(field=str(field), message=msg))

    # Это используется чаще.
    error_response = ErrorResponse(
        status='error',
        status_code=exc.status_code,
        message=exc.message,
        details=details,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=str(request.url.path),
        request_id=request_id,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


