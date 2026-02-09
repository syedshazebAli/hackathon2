from jose import jwt, JWTError
from fastapi import HTTPException, status
from ..config import BETTER_AUTH_SECRET
from datetime import datetime
from typing import Optional

# Get the secret from config
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

ALGORITHM = "HS256"


def verify_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token and return user information if valid.
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("userId")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            return None
        
        # Return user information
        return {
            "user_id": user_id,
            "email": email
        }
    except JWTError:
        return None