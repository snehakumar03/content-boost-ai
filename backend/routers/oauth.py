"""
OAuth router for Google and GitHub social login.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.oauth_account import OAuthAccount
from services.jwt_service import JWTService
import requests
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

router = APIRouter(prefix="/api/auth/oauth", tags=["oauth"])
jwt_service = JWTService()

# OAuth configuration
OAUTH_CONFIG = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        "scope": "openid email profile"
    },
    "github": {
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
        "scope": "user:email"
    }
}


@router.get("/{provider}")
async def oauth_login(provider: str):
    """
    Initiate OAuth login flow.

    Redirects the user to the OAuth provider's authorization page.
    Supported providers: google, github
    """
    if provider not in OAUTH_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider: {provider}"
        )

    config = OAUTH_CONFIG[provider]

    # Check if credentials are configured
    if not config["client_id"] or not config["client_secret"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{provider.capitalize()} OAuth is not configured. Please set {provider.upper()}_CLIENT_ID and {provider.upper()}_CLIENT_SECRET environment variables."
        )

    redirect_uri = f"http://localhost:8000/api/auth/oauth/callback/{provider}"

    # Generate state parameter for CSRF protection
    import secrets
    state = secrets.token_urlsafe(16)

    auth_url = (
        f"{config['auth_url']}?"
        f"client_id={config['client_id']}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={config['scope']}&"
        f"state={state}"
    )

    return RedirectResponse(auth_url)


@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    """
    Handle OAuth callback from provider.

    Exchanges the authorization code for tokens,
    retrieves user information, and creates/links user account.
    """
    if provider not in OAUTH_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider: {provider}"
        )

    config = OAUTH_CONFIG[provider]
    redirect_uri = f"http://localhost:8000/api/auth/oauth/callback/{provider}"

    try:
        # Exchange code for access token
        token_response = requests.post(
            config["token_url"],
            data={
                "code": code,
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            },
            headers={"Accept": "application/json"}
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange authorization code"
            )

        token_data = token_response.json()
        access_token = token_data["access_token"]

        # Get user info
        headers = {"Authorization": f"Bearer {access_token}"}
        if provider == "github":
            headers["Accept"] = "application/json"

        user_response = requests.get(config["userinfo_url"], headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve user information"
            )

        user_data = user_response.json()

        # Extract user information based on provider
        if provider == "google":
            email = user_data.get("email")
            name = user_data.get("name", user_data.get("given_name", ""))
            provider_user_id = user_data.get("id")
        elif provider == "github":
            email = user_data.get("email")
            if not email:
                # Get primary email from GitHub
                email_response = requests.get(
                    "https://api.github.com/user/emails",
                    headers=headers
                )
                if email_response.status_code == 200:
                    emails = email_response.json()
                    primary_email = next((e["email"] for e in emails if e.get("primary")), None)
                    email = primary_email
            name = user_data.get("name") or user_data.get("login", "")
            provider_user_id = str(user_data.get("id"))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported provider"
            )

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required from OAuth provider"
            )

        # Create or get user using auth service
        from services.auth_service import AuthService
        auth_service = AuthService()

        user = auth_service.create_oauth_user(
            email=email,
            name=name,
            provider=provider,
            provider_user_id=provider_user_id
        )

        # Generate JWT tokens
        access_token = jwt_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = jwt_service.create_refresh_token(data={"sub": str(user.id)})

        # Redirect to frontend with tokens
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        return RedirectResponse(
            f"{frontend_url}/oauth/callback?"
            f"access_token={access_token}&"
            f"refresh_token={refresh_token}&"
            f"user_id={user.id}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth error: {str(e)}"
        )
