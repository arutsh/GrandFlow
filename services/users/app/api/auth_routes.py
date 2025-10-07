from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime
from zoneinfo import ZoneInfo

from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse

from app.db.session import SessionLocal
from app.utils.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_token,
    verify_token_hash,
)
from app.crud.sessions_curd import create_session, get_non_revoked_sessions
from app.crud.user_crud import get_user_by_email, create_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register_endpoint(req: RegisterRequest, db: Session = Depends(get_db)):

    try:
        user = create_user(
            session=db,
            email=req.email,
            password=req.password,
            first_name=req.first_name,
            last_name=req.last_name,
            role=req.role,
            customer_id=req.customer_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    refresh_token = create_refresh_token()
    session = create_session(
        session=db,
        user_id=user.id,
        refresh_token_hash=refresh_token,
    )

    token = create_access_token({"user_id": user.id, "session_id": session.id})

    return TokenResponse(access_token=token, refresh_token=refresh_token, status=user.status)


@router.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, req.email)
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token = create_refresh_token()

    session = create_session(
        session=db,
        user_id=user.id,
        refresh_token_hash=refresh_token,
    )

    token = create_access_token({"user_id": user.id, "session_id": session.id})

    return TokenResponse(access_token=token, refresh_token=refresh_token, status=user.status)


@router.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    sessions = get_non_revoked_sessions(db)

    for s in sessions:
        # Session model always has naive datetime, assume UTC
        if s.expires_at.replace(tzinfo=ZoneInfo("UTC")) < datetime.now(ZoneInfo("UTC")):
            continue
        if verify_token_hash(refresh_token, s.refresh_token_hash):
            # Rotate new refresh token
            new_refresh = create_refresh_token()
            s.refresh_token_hash = hash_token(new_refresh)
            db.commit()

            access_token = create_access_token({"user_id": s.user_id, "session_id": s.id})

            return TokenResponse(
                access_token=access_token, refresh_token=new_refresh, status=s.user.status
            )

    raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
