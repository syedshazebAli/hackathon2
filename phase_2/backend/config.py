import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication configuration
BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")
BETTER_AUTH_URL: Optional[str] = os.getenv("BETTER_AUTH_URL", "http://localhost:8888")

# Application configuration
APP_NAME: str = "Task Management API"
API_V1_STR: str = "/api/v1"

# Validate required environment variables
def validate_config():
    if not BETTER_AUTH_SECRET:
        raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

validate_config()