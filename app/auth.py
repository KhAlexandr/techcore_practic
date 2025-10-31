import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload["token"] = token
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействиетльные данные для аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_role(required_role: str, user: dict = Depends(verify_token)):
    if user.get("role") != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Должнабыть быть роль: {required_role} ",
        )
    return user


async def verify_admin(user: dict = Depends(verify_token)):
    return await require_role("admin", user)


async def verify_user(user: dict = Depends(verify_token)):
    return await require_role("user", user)
