from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
import os
import re
from dotenv import load_dotenv
from .models import Message, Conversation
from .database import get_session
from .mcp_server import add_task, list_tasks, complete_task, delete_task, update_task

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo AI Chatbot", version="1.0.0")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


def extract_task_info(text: str) -> tuple:
    """
    Extract task title and description from user input
    """
    # Look for patterns like "Add task: title - description" or "Add task: title"
    add_task_pattern = r"(?:add|create|make)\s+(?:a\s+)?(?:task|todo)[:\s]+([^-\n]+)(?:[-:]\s*(.+))?\.?$"
    match = re.search(add_task_pattern, text.lower().strip())
    
    if match:
        title = match.group(1).strip()
        description = match.group(2).strip() if match.group(2) else ""
        return title, description
    
    return None, None


def extract_task_id(text: str) -> str:
    """
    Extract task ID from user input
    """
    # Look for patterns like "complete task 123" or "delete task abc"
    id_pattern = r'(?:task|id)[\s:]*(\w+)'
    match = re.search(id_pattern, text.lower())
    
    if match:
        return match.group(1)
    
    return None


def mock_agent_response(user_message: str, user_id: str) -> str:
    """
    Mock AI agent that simulates the real agent's behavior using pattern matching
    """
    lower_msg = user_message.lower()
    
    # Pattern matching for different commands
    if any(word in lower_msg for word in ['add', 'create', 'make']) and any(word in lower_msg for word in ['task', 'todo']):
        title, description = extract_task_info(user_message)
        if title:
            # Call the add_task MCP tool
            import asyncio
            result = asyncio.run(add_task(title=title, description=description, user_id=user_id))
            return result.get("message", "Task added successfully!")
        else:
            return "I didn't understand the task you wanted to add. Please say something like 'Add task: Buy groceries'"
    
    elif 'list' in lower_msg and any(word in lower_msg for word in ['task', 'tasks', 'todo']):
        # Call the list_tasks MCP tool
        import asyncio
        completed_filter = 'completed' in lower_msg
        result = asyncio.run(list_tasks(user_id=user_id, completed=completed_filter))
        if result:
            response = "Here are your tasks:\n"
            for task in result:
                status = "✓" if task["completed"] else "○"
                response += f"- [{status}] {task['title']} (ID: {task['id']})\n"
            return response
        else:
            return "You have no tasks."
    
    elif any(word in lower_msg for word in ['complete', 'done', 'finish']) and any(word in lower_msg for word in ['task', 'tasks']):
        task_id = extract_task_id(user_message)
        if task_id:
            # Call the complete_task MCP tool
            import asyncio
            result = asyncio.run(complete_task(task_id=task_id, user_id=user_id))
            return result.get("message", "Task completed!")
        else:
            return "I need the task ID to complete. Please specify which task you want to mark as completed."
    
    elif any(word in lower_msg for word in ['delete', 'remove']) and any(word in lower_msg for word in ['task', 'tasks']):
        task_id = extract_task_id(user_message)
        if task_id:
            # Call the delete_task MCP tool
            import asyncio
            result = asyncio.run(delete_task(task_id=task_id, user_id=user_id))
            return result.get("message", "Task deleted!")
        else:
            return "I need the task ID to delete. Please specify which task you want to remove."
    
    elif any(word in lower_msg for word in ['update', 'change', 'modify']) and any(word in lower_msg for word in ['task', 'tasks']):
        task_id = extract_task_id(user_message)
        if task_id:
            # For simplicity, we'll just acknowledge the request
            return f"I received your request to update task {task_id}. In a real implementation, this would call the update_task MCP tool."
        else:
            return "I need the task ID to update. Please specify which task you want to modify."
    
    else:
        # Default response for unrecognized commands
        return "I'm your AI assistant for managing tasks. You can ask me to add, list, complete, delete, or update tasks. For example, say 'Add task: Buy groceries'."


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest):
    """
    Main chat endpoint that integrates Mock AI Agent and MCP Tools
    """
    # Get database session
    session = next(get_session())
    
    try:
        # 1. Fetch conversation history from DB
        conversation_stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).limit(1)
        conversation = session.exec(conversation_stmt).first()
        
        # Create a new conversation if none exists
        if not conversation:
            conversation = Conversation(user_id=user_id, title=request.message[:50])
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        
        # 2. Store user message in DB
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()
        
        # 3. Fetch all messages in the conversation for context
        messages_stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.timestamp)
        all_messages = session.exec(messages_stmt).all()
        
        # Format messages for the mock agent
        formatted_messages = []
        for msg in all_messages[:-1]:  # Exclude the current user message
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add system message to guide the mock agent
        formatted_messages.insert(0, {
            "role": "system",
            "content": """You are a helpful AI assistant that helps users manage their tasks. You have access to the following tools:
- add_task: Add a new task
- list_tasks: List all tasks
- complete_task: Mark a task as completed
- delete_task: Delete a task
- update_task: Update task details

Always respond conversationally and confirm actions taken."""
        })
        
        # 4. Run Mock Agent with MCP tools (pattern matching approach)
        ai_response = mock_agent_response(request.message, user_id)
        
        # 5. Store AI response in DB
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        session.add(ai_message)
        session.commit()
        
        # 6. Return AI response to user
        return ChatResponse(response=ai_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        session.close()


@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    from .database import engine
    # Create tables
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)