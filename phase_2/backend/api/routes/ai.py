"""
AI API Routes for Chatbot functionality
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from uuid import UUID

from database import get_session
# from auth import get_current_user
# from models import User
from task_processor import AIRequest, AIResponse, ai_processor

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=AIResponse)
async def process_ai_request(
    ai_request: AIRequest,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user),
):
    """
    Process natural language requests for task management
    """
    # For testing, use a mock user ID if not provided
    # In a real implementation, you would use the authenticated user's ID
    if not ai_request.user_id:
        from uuid import uuid4
        ai_request.user_id = str(uuid4())

    # Process the request with the AI processor
    response = await ai_processor.process_request(ai_request)

    return response