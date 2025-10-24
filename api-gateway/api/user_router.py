from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from shared.schemas.auth_schema import LoginRequest, TokenResponse, RegisterRequest
from services.users_client import (
    get_user_by_id,
    login_via_gateway,
    refresh_token_via_gateway,
    register_via_gateway,
    update_user_via_gateway,
)
from shared.schemas.user_schema import User, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_via_gateway_endpoint(payload: LoginRequest):
    """Login user via users service through the API gateway."""
    return await login_via_gateway(payload.model_dump())


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token_via_gateway_endpoint(refresh_token: str):
    """Refresh token via users service through the API gateway."""
    return await refresh_token_via_gateway(refresh_token)


@router.post("/register", response_model=TokenResponse)
async def register_via_gateway_endpoint(payload: RegisterRequest):
    """Register user via users service through the API gateway."""
    return await register_via_gateway(payload)


@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id_endpoint(user_id: str, token: str = Depends(oauth2_scheme)):
    """Get user by ID via users service through the API gateway."""
    return await get_user_by_id(user_id, token=token)


@router.patch("/users/{user_id}", response_model=User)
async def update_user_via_gateway_endpoint(
    user_id: str, payload: UserUpdate, token: str = Depends(oauth2_scheme)
):
    """Update user by ID via users service through the API gateway."""
    return await update_user_via_gateway(user_id, payload, token=token)
