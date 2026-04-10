"""
Authentication service for user management.
"""
from passlib.context import CryptContext
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User, UserRole
from database import SessionLocal
from services.jwt_service import JWTService


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_service = JWTService()


class AuthService:
    """
    Service for handling authentication operations.

    Provides user registration, login, password management,
    and token generation.
    """

    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        """Ensure database session is closed."""
        if hasattr(self, 'db'):
            self.db.close()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            plain_password: Plain text password
            hashed_password: Bcrypt hashed password

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    def create_user(self, email: str, password: str, name: str = None) -> User:
        """
        Create a new user with email/password.

        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            name: Optional display name

        Returns:
            Created User object

        Raises:
            ValueError: If email already exists
        """
        # Check if user exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError(f"Email {email} is already registered")

        # Hash password and create user
        hashed_password = self.get_password_hash(password)
        db_user = User(
            email=email,
            name=name or email.split("@")[0],
            hashed_password=hashed_password,
            is_verified=False  # Requires email verification
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def create_oauth_user(self, email: str, name: str, provider: str, provider_user_id: str) -> User:
        """
        Create or find a user from OAuth login.

        Args:
            email: User's email from OAuth provider
            name: User's name from OAuth provider
            provider: OAuth provider name (google, github)
            provider_user_id: User ID from provider

        Returns:
            User object
        """
        from models.oauth_account import OAuthAccount

        # Check if OAuth account exists
        oauth_account = self.db.query(OAuthAccount).filter(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id
        ).first()

        if oauth_account:
            return self.db.query(User).filter(User.id == oauth_account.user_id).first()

        # Check if user with email exists
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            # Create new user
            user = User(
                email=email,
                name=name,
                hashed_password=None,  # OAuth users don't have passwords
                is_verified=True  # OAuth users are pre-verified
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        # Link OAuth account
        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id
        )
        self.db.add(oauth_account)
        self.db.commit()

        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email
            password: Plain text password

        Returns:
            User object if authenticated, None otherwise
        """
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return None

        # OAuth users without passwords can't login with password
        if not user.hashed_password:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    def login(self, email: str, password: str) -> dict:
        """
        Login a user and generate tokens.

        Args:
            email: User's email
            password: Plain text password

        Returns:
            Dictionary with access_token, refresh_token, and user data

        Raises:
            ValueError: If credentials are invalid
        """
        user = self.authenticate_user(email, password)

        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is disabled")

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        # Generate tokens
        access_token = jwt_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = jwt_service.create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "is_verified": user.is_verified
            }
        }

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: User's ID

        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.

        Args:
            email: User's email

        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
