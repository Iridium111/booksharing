from fastapi import APIRouter
from app.api.v1.user import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.book import router as books_router

api_v1_router = APIRouter()

api_v1_router.include_router(users_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(books_router)