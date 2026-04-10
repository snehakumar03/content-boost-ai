"""
Rate limiting service for API usage tracking.
"""
import os
from datetime import date, datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from models.rate_limit import RateLimit
from models.user import User
from database import SessionLocal


class RateLimitService:
    """
    Service for enforcing and tracking rate limits.

    Unauthenticated users: 5 requests per day
    Authenticated users: Unlimited requests
    """

    def __init__(self):
        self.db = SessionLocal()
        self.daily_limit_free = int(os.getenv("RATE_LIMIT_FREE_TIER", "5"))
        self.daily_limit_auth = int(os.getenv("RATE_LIMIT_AUTH_TIER", "999999"))

    def __del__(self):
        """Ensure database session is closed."""
        if hasattr(self, 'db'):
            self.db.close()

    def check_rate_limit(self, user_id: Optional[int] = None, ip_address: str = "127.0.0.1") -> Tuple[bool, int, int]:
        """
        Check if user/IP is within rate limits.

        Args:
            user_id: User ID (None for anonymous)
            ip_address: Client IP address

        Returns:
            Tuple of (can_proceed, current_count, daily_limit)
        """
        today = date.today()

        # Authenticated users have unlimited access
        if user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user and user.is_active:
                return True, 0, self.daily_limit_auth

        # Unauthenticated users - check IP-based rate limit
        rate_limit = self.db.query(RateLimit).filter(
            RateLimit.ip_address == ip_address,
            RateLimit.date == today,
            RateLimit.user_id.is_(None)
        ).first()

        current_count = rate_limit.request_count if rate_limit else 0
        can_proceed = current_count < self.daily_limit_free

        return can_proceed, current_count, self.daily_limit_free

    def increment_rate_limit(self, user_id: Optional[int] = None, ip_address: str = "127.0.0.1"):
        """
        Increment the rate limit counter for today.

        Args:
            user_id: User ID (None for anonymous)
            ip_address: Client IP address
        """
        today = date.today()

        # Don't track authenticated users
        if user_id:
            return

        # Find or create rate limit record
        rate_limit = self.db.query(RateLimit).filter(
            RateLimit.ip_address == ip_address,
            RateLimit.date == today,
            RateLimit.user_id.is_(None)
        ).first()

        if rate_limit:
            rate_limit.request_count += 1
        else:
            rate_limit = RateLimit(
                ip_address=ip_address,
                date=today,
                request_count=1
            )
            self.db.add(rate_limit)

        self.db.commit()

    def get_rate_limit_status(self, user_id: Optional[int] = None, ip_address: str = "127.0.0.1") -> dict:
        """
        Get current rate limit status.

        Args:
            user_id: User ID (None for anonymous)
            ip_address: Client IP address

        Returns:
            Dictionary with rate limit information
        """
        can_proceed, current_count, daily_limit = self.check_rate_limit(user_id, ip_address)

        return {
            "can_proceed": can_proceed,
            "current_count": current_count,
            "daily_limit": daily_limit,
            "remaining": max(0, daily_limit - current_count),
            "is_authenticated": bool(user_id)
        }
