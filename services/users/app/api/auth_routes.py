from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from ..models import UserModel, SessionModel
from ..db.session import SessionLocal
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_token,
    verify_token_hash,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserModel(
        id=str(uuid4()),
        email=req.email,
        first_name=req.first_name,
        last_name=req.last_name,
        role=req.role,
        customer_id=req.customer_id,
        hashed_password=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    refresh_token = create_refresh_token()
    issue_at = datetime.now(ZoneInfo("UTC"))
    session = SessionModel(
        id=str(uuid4()),
        user_id=user.id,
        issued_at=issue_at,
        expires_at=issue_at + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        refresh_token_hash=hash_token(refresh_token),
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    token = create_access_token({"sub": user.id, "session_id": session.id})

    return TokenResponse(access_token=token, refresh_token=refresh_token)


@router.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token = create_refresh_token()
    issue_at = datetime.now(ZoneInfo("UTC"))
    session = SessionModel(
        id=str(uuid4()),
        user_id=user.id,
        issued_at=issue_at,
        expires_at=issue_at + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        refresh_token_hash=hash_token(refresh_token),
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    token = create_access_token({"sub": user.id, "session_id": session.id})

    return TokenResponse(access_token=token, refresh_token=refresh_token)


@router.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    session = db.query(SessionModel).filter(SessionModel.revoked == False).all()

    for s in session:
        # Session model always has naive datetime, assume UTC
        if s.expires_at.replace(tzinfo=ZoneInfo("UTC")) < datetime.now(ZoneInfo("UTC")):
            continue
        if verify_token_hash(refresh_token, s.refresh_token_hash):
            # Rotate new refresh token
            new_refresh = create_refresh_token()
            s.refresh_token_hash = hash_token(new_refresh)
            db.commit()

            access_token = create_access_token({"sub": s.user_id, "session_id": s.id})

            return TokenResponse(access_token=access_token, refresh_token=new_refresh)

    raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
