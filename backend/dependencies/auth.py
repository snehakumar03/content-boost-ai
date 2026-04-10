"""
Authentication dependencies for FastAPI routes.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.jwt_service import JWTService

# Initialize JWT service and security scheme
jwt_service = JWTService()
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.

    Raises:
        HTTPException 401: If no valid token is provided

    Returns:
        User object
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    user_id = jwt_service.verify_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )

    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication dependency.
    Returns the user if authenticated, None otherwise.

    Useful for endpoints that work for both authenticated
    and unauthenticated users.
    """
    if not credentials:
        return None

    token = credentials.credentials
    user_id = jwt_service.verify_access_token(token)

    if not user_id:
        return None

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or not user.is_active:
        return None

    return user
