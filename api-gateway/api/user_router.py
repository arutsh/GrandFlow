from fastapi import APIRouter
from shared.schemas.auth_schema import LoginRequest, TokenResponse, RegisterRequest
from services.users_client import login_via_gateway, register_via_gateway


router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_via_gateway_endpoint(payload: LoginRequest):
    """Login user via users service through the API gateway."""
    return await login_via_gateway(payload.model_dump())


@router.post("/register", response_model=TokenResponse)
async def register_via_gateway_endpoint(payload: RegisterRequest):
    """Register user via users service through the API gateway."""
    return await register_via_gateway(payload)
