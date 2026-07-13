from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.admin.admin import admin
from app.api.router import api_v1_router
from app.core.errror_handlers import bookshare_exception_handler
from app.core.exceptions import BookShareBaseException
from app.core.middleware import ErrorHandlingMiddleware

app = FastAPI(
    title="BookShare API",
    description="Ассинхронная платформа для шеринга книг.",
    version="1.0.",
)

app.add_exception_handler(BookShareBaseException, bookshare_exception_handler)

app.add_middleware(ErrorHandlingMiddleware)

app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-secret-key",
)

app.include_router(api_v1_router, prefix="/api/v1")

admin.mount_to(app)