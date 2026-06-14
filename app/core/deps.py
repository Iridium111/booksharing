import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import decode_token
from app.models import User

oauth2_scheme = HTTPBearer() # "Authorization: Bearer <token> "

async def get_current_user(
        bearer = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        payload = decode_token(bearer.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await session.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user