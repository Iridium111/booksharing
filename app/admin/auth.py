from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed
from uuid import UUID

from app.core.database import async_session_maker
from app.core.security import verify_password
from app.repositories.user import UserRepository


class AdminAuthProvider(AuthProvider):
    async def login(self,
                    username: str,
                    password: str,
                    remember_me:bool,
                    request: Request,
                    response: Response,
                    ) -> Response:
        async with async_session_maker() as session:
            user = await UserRepository.find_by_username(
                session,
                username=username
            )

            if user is None:
                raise LoginFailed('Invalid username or password.')
            if not verify_password(password, user.hashed_password):
                raise LoginFailed("Invalid username or password.")
            if not user.is_admin:
                raise LoginFailed("User is not admin.")

            request.session["admin_user_id"] = str(user.id)
            return response

    async def is_authenticated(self, request: Request) -> bool:
        admin_user_id = request.session.get("admin_user_id")
        if admin_user_id is None:
            return False

        try:
            user_id = UUID(admin_user_id)
        except (ValueError, TypeError):
            request.session.pop("admin_user_id", None)
            return False

        async with async_session_maker() as session:
            admin = await UserRepository.find_by_uuid(session,
                                                      user_id=user_id)

        return admin is not None and admin.is_admin


    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
