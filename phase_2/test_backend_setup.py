"""
Test script to verify the backend setup
"""
import asyncio
from sqlmodel import Session, select
from backend.database import engine
from backend.models import User, Task
from datetime import datetime
import uuid


def test_models():
    print("Testing model creation...")
    
    # Create a user
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        name="Test User",
        email_verified=True
    )
    
    print(f"Created user: {user.email} with ID: {user.id}")
    
    # Create a task
    task = Task(
        id=uuid.uuid4(),
        title="Test Task",
        description="This is a test task",
        status="pending",
        priority="medium",
        user_id=user.id
    )
    
    print(f"Created task: {task.title} for user ID: {task.user_id}")
    
    # Test serialization
    task_read = task.model_dump()
    print(f"Serialized task: {task_read['title']}")
    
    print("Models working correctly!")


def test_database_connection():
    print("\nTesting database connection...")
    
    try:
        with Session(engine) as session:
            # Try to count users (should be 0 initially)
            user_count = session.exec(select(User)).all()
            print(f"Connected to database. Found {len(user_count)} users.")
            
            # Try to count tasks (should be 0 initially)
            task_count = session.exec(select(Task)).all()
            print(f"Found {len(task_count)} tasks.")
            
        print("Database connection working correctly!")
    except Exception as e:
        print(f"Database connection failed: {e}")


if __name__ == "__main__":
    test_models()
    test_database_connection()