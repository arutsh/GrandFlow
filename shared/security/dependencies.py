from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .jwt_utils import decode_access_token
from uuid import UUID
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Only valid in users service


def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        role = payload.get("role")

        if not user_id:
            raise ValueError("Missing user_id in token payload")

        # Safely convert to UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise ValueError("Invalid UUID format for user_id")

        return {"user_id": user_uuid, "role": role, "token": token}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token is invalid or expired: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
