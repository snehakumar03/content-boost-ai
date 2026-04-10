"""
OAuth account model for social login integration.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class OAuthAccount(Base):
    """
    OAuth account model for linking social providers to user accounts.

    Attributes:
        id: Primary key
        user_id: Foreign key to user
        provider: OAuth provider (google, github)
        provider_user_id: User ID from the OAuth provider
        access_token: OAuth access token
        refresh_token: OAuth refresh token
        expires_at: Token expiration timestamp
        created_at: Account link timestamp
    """
    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(50), nullable=False)  # 'google' or 'github'
    provider_user_id = Column(String(255), nullable=False)
    access_token = Column(String(500))  # Consider encrypting in production
    refresh_token = Column(String(500))  # Consider encrypting in production
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="oauth_accounts")

    def __repr__(self):
        return f"<OAuthAccount(id={self.id}, provider={self.provider}, user_id={self.user_id})>"
