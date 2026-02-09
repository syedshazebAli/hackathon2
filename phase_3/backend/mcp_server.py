from typing import List, Optional
from fastapi import Depends
from sqlmodel import Session, select
from .models import Task, TaskUpdate, Conversation, Message
from .database import get_session


async def add_task(title: str, description: Optional[str] = None, user_id: str = "") -> dict:
    """
    Creates a new task for the user
    """
    with next(get_session()) as session:
        task = Task(title=title, description=description, user_id=user_id)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "success": True,
            "message": f"Task '{title}' added successfully!",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        }


async def list_tasks(user_id: str = "", completed: Optional[bool] = None) -> List[dict]:
    """
    Lists all tasks for the user, optionally filtered by completion status
    """
    with next(get_session()) as session:
        query = select(Task).where(Task.user_id == user_id)
        
        if completed is not None:
            query = query.where(Task.completed == completed)
            
        tasks = session.exec(query).all()
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ]


async def complete_task(task_id: str, user_id: str = "") -> dict:
    """
    Marks a task as completed
    """
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        
        if not task:
            return {"success": False, "message": f"Task with ID {task_id} not found"}
        
        if task.user_id != user_id:
            return {"success": False, "message": "Unauthorized to modify this task"}
        
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "success": True,
            "message": f"Task '{task.title}' marked as completed!",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        }


async def delete_task(task_id: str, user_id: str = "") -> dict:
    """
    Deletes a task
    """
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        
        if not task:
            return {"success": False, "message": f"Task with ID {task_id} not found"}
        
        if task.user_id != user_id:
            return {"success": False, "message": "Unauthorized to delete this task"}
        
        session.delete(task)
        session.commit()
        
        return {
            "success": True,
            "message": f"Task '{task.title}' deleted successfully!"
        }


async def update_task(
    task_id: str, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    completed: Optional[bool] = None,
    user_id: str = ""
) -> dict:
    """
    Updates task properties
    """
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        
        if not task:
            return {"success": False, "message": f"Task with ID {task_id} not found"}
        
        if task.user_id != user_id:
            return {"success": False, "message": "Unauthorized to modify this task"}
        
        update_data = {}
        if title is not None:
            task.title = title
            update_data["title"] = title
        if description is not None:
            task.description = description
            update_data["description"] = description
        if completed is not None:
            task.completed = completed
            update_data["completed"] = completed
            
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "success": True,
            "message": f"Task '{task.title}' updated successfully!",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
        }