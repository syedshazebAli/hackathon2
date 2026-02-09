from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import Session, SQLModel, create_engine
from api.routes import tasks
from api.routes.ai import router as ai_router
from config import APP_NAME, validate_config
from auth import get_current_user

# Import the hardcoded database engine
from database import engine
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate configuration on startup
    logger.info("Validating configuration...")
    validate_config()
    logger.info("Configuration validated successfully")

    # Create database tables on startup
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    yield
    # Cleanup on shutdown if needed
    logger.info("Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="Secure task management API with Better Auth integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware - Configure for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default port
        "http://localhost:3001",  # Alternative Next.js port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://localhost:3000",
        "https://localhost:3001"
    ],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(ai_router, prefix="/api", tags=["ai"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/user")
def get_user():
    """Endpoint to get current user info - for auth verification"""
    # For testing, return a mock user
    # In a real implementation, you would use the authenticated user
    return {
        "id": "mock-user-id",
        "email": "test@example.com",
        "name": "Test User",
        "avatar_url": "",
        "email_verified": True
    }

# Temporarily disable authentication for testing
# Global dependency to ensure all endpoints require authentication
# @app.middleware("http")
# async def auth_middleware(request, call_next):
#     # Skip auth for root, health check, and user endpoints
#     if request.url.path in ["/", "/health", "/user"]:
#         response = await call_next(request)
#         return response
#
#     # For API routes, verify the token
#     if request.url.path.startswith("/api") and request.url.path != "/api/auth/login":
#         # Extract and verify token
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Missing or invalid Authorization header",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#
#         # Token will be verified in the route handlers via dependency injection
#         # Store user info in request state for use in route handlers if needed
#         # The actual verification happens in the get_current_user dependency
#
#     response = await call_next(request)
#     return response