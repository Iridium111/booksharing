import uuid

from starlette.middleware.base import BaseHTTPMiddleware    # FastAPI обертка над starlette, на уровень ниже
from starlette.requests import Request
from starlette.responses import Response
from time import time

from app.core.exceptions import BookShareBaseException
def create_request_id() -> str:
    """генерация уникального индификатора"""
    return f"req-{uuid.uuid4().hex[:8]}"


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        request_id = create_request_id()
        request.state.request_id = request_id

        start_time = time()
        try:
            response = await call_next(request)
        except Exception as exc:
            # Обработка ошибки
            raise

        end_time = time()
        # time
        response.headers["X-Request-Id"] = request_id
        response.headers["X-Process-Time"] = str(end_time - start_time)
        response.headers["X-Request-Data"] = f"{method},{path},{client_ip},{user_agent}"
        return response


