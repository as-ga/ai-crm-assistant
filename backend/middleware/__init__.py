from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, APIKeyCookie
import services.jwt as jwt


bearer_scheme = HTTPBearer(auto_error=False)
cookie_scheme = APIKeyCookie(name="token", auto_error=False)


async def auth_middleware(
    request: Request,
    bearer_token: Optional[object] = Depends(bearer_scheme),
    cookie_token: Optional[str] = Depends(cookie_scheme)
):

    token = None

    if bearer_token:
        token = bearer_token.credentials
    elif cookie_token:
        token = cookie_token
    else:
        token = request.headers.get(
            "Authorization") or request.cookies.get("token")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token missing (Header or Cookie required)."
        )

    try:
        decoded_token = jwt.decode_jwt_token(token)

        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token."
            )

        return decoded_token

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials."
        )
