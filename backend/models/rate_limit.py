"""
Rate limit model for tracking API usage.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RateLimit(Base):
    """
    Rate limit model for tracking API usage by IP address or user.

    Attributes:
        id: Primary key
        user_id: Foreign key to user (null for anonymous users)
        ip_address: Client IP address for tracking anonymous users
        request_count: Number of requests made in the time window
        date: Date of the requests (for daily reset)
        created_at: Record creation timestamp
    """
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # NULL for anonymous
    ip_address = Column(String(45), nullable=False)  # IPv6 compatible
    request_count = Column(Integer, default=0)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="rate_limits")

    # Unique constraint to prevent duplicate records
    __table_args__ = (
        UniqueConstraint('ip_address', 'date', 'user_id', name='unique_ip_date_user'),
    )

    def __repr__(self):
        return f"<RateLimit(id={self.id}, ip={self.ip_address}, count={self.request_count}, date={self.date})>"
