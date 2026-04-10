"""
User model for authentication and authorization.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    User model for authentication.

    Attributes:
        id: Primary key
        email: Unique email address
        name: User's display name
        hashed_password: Bcrypt hashed password (nullable for OAuth users)
        role: User role (user or admin)
        is_active: Account status
        is_verified: Email verification status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last successful login timestamp
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    oauth_accounts = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    rate_limits = relationship("RateLimit", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
