from fastapi import FastAPI

from app.api.v1.router import api_v1_router

app = FastAPI(
    title="BookShare API",
    description="Ассинхронная платформа для шеринга книг.",
    version="1.0.",
)

app.include_router(api_v1_router, prefix="/api/v1")