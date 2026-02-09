from fastapi import Request, HTTPException, status, Depends
from typing import Optional, Dict, Any
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import BETTER_AUTH_SECRET
from models import User, UserRead
from sqlmodel import Session, select
from database import get_session
import uuid

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthHandler:
    """Better Auth compatible handler for session verification"""
    
    def __init__(self):
        if not BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET environment variable is not set")
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create an access token similar to Better Auth"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def verify_token(self, token: str, session: Session) -> Optional[Dict[str, Any]]:
        """Verify the token and return user information"""
        try:
            payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            
            if user_id is None:
                return None
                
            # Find user in database
            user = session.get(User, uuid.UUID(user_id))
            if not user:
                return None
                
            return {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "name": user.name,
                    "image": user.avatar_url,
                    "emailVerified": user.email_verified
                },
                "accessToken": token
            }
        except JWTError:
            return None

# Create a global instance of the auth handler
auth_handler = AuthHandler()


def get_current_user(
    request: Request, 
    session: Session = Depends(get_session)
) -> User:
    """Dependency to get current user from token"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header.split(" ")[1]
    user_info = auth_handler.verify_token(token, session)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the user object from the database
    user_id = user_info["user"]["id"]
    user = session.get(User, uuid.UUID(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user