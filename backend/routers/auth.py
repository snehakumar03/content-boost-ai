"""
Authentication router for login, register, logout, and user info endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import get_db
from models.user import User
from services.auth_service import AuthService
from services.rate_limit_service import RateLimitService
from dependencies.auth import get_current_user, get_current_user_optional

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()
rate_limit_service = RateLimitService()


# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str
    is_verified: bool


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.

    Returns the created user information.
    """
    try:
        user = auth_service.create_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "is_verified": user.is_verified,
            "message": "User registered successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Login with email and password.

    Returns JWT tokens and user information.
    """
    try:
        result = auth_service.login(credentials.email, credentials.password)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout the current user.

    In a stateless JWT system, the client simply removes the token.
    This endpoint can be used for server-side logout logging.
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's information.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        is_verified=current_user.is_verified
    )


@router.get("/rate-limit")
async def get_rate_limit_status(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get current rate limit status for the user or IP.

    Shows how many requests remain for today.
    """
    ip_address = request.client.host
    user_id = current_user.id if current_user else None

    return rate_limit_service.get_rate_limit_status(user_id, ip_address)


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Verify if the current token is valid.

    Returns user information if token is valid.
    """
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role
        }
    }
