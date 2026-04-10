"""
JWT token service for creating and validating tokens.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
import secrets

load_dotenv()


class JWTService:
    """
    Service for creating and validating JWT tokens.

    Uses HS256 algorithm with configurable expiration times.
    """

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    def create_access_token(self, data: Dict) -> str:
        """
        Create an access token with short expiration.

        Args:
            data: Payload data to encode (should include 'sub' for user ID)

        Returns:
            Encoded JWT access token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: Dict) -> str:
        """
        Create a refresh token with longer expiration.

        Args:
            data: Payload data to encode (should include 'sub' for user ID)

        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decode and validate a JWT token.

        Args:
            token: JWT token to decode

        Returns:
            Decoded payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    def verify_access_token(self, token: str) -> Optional[str]:
        """
        Verify an access token and extract user ID.

        Args:
            token: Access token to verify

        Returns:
            User ID if valid, None if invalid
        """
        payload = self.decode_token(token)
        if payload and payload.get("type") == "access":
            return payload.get("sub")
        return None

    def verify_refresh_token(self, token: str) -> Optional[str]:
        """
        Verify a refresh token and extract user ID.

        Args:
            token: Refresh token to verify

        Returns:
            User ID if valid, None if invalid
        """
        payload = self.decode_token(token)
        if payload and payload.get("type") == "refresh":
            return payload.get("sub")
        return None
