from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    safe_decode,
    verify_password,
)
from app.models.user import User
from app.schemas.token import Message
from app.schemas.user import UserLogin, UserRead, UserRegister
from app.services.cookies import clear_auth_cookies, set_auth_cookies

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, session: SessionDep, response: Response):
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=payload.email.lower().strip(),
        phone=payload.phone,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    set_auth_cookies(response, access, refresh)
    return user


@router.post("/login", response_model=UserRead)
def login(payload: UserLogin, session: SessionDep, response: Response):
    user = session.exec(
        select(User).where(User.email == payload.email.lower().strip())
    ).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    set_auth_cookies(response, access, refresh)
    return user


@router.post("/logout", response_model=Message)
def logout(response: Response):
    clear_auth_cookies(response)
    return Message(message="Logged out")


@router.post("/refresh", response_model=Message)
def refresh(request: Request, response: Response, session: SessionDep):
    settings = get_settings()
    token = request.cookies.get(settings.cookie_refresh_name)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
        )

    payload = safe_decode(token)
    if not payload or payload.get("type") != "refresh":
        clear_auth_cookies(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    try:
        user_id = UUID(payload["sub"])
    except (KeyError, ValueError):
        clear_auth_cookies(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        )

    user = session.get(User, user_id)
    if not user or not user.is_active:
        clear_auth_cookies(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    access = create_access_token(str(user.id))
    refresh_tok = create_refresh_token(str(user.id))
    set_auth_cookies(response, access, refresh_tok)
    return Message(message="Tokens refreshed")


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser):
    return current_user
