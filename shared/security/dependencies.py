from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwt_utils import decode_access_token
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Only valid in users service


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return {"user_id": UUID(payload.get("user_id")), "role": payload.get("role")}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
