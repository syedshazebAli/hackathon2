"""
Simple test to verify the backend models work
"""
from backend.models import User, Task, TaskCreate, TaskUpdate
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
    task_dict = task.model_dump()
    print(f"Serialized task: {task_dict['title']}")
    
    # Test TaskCreate model
    task_create = TaskCreate(
        title="New Task",
        description="Description for new task",
        status="pending",
        priority="high",
        category="work",
        user_id=user.id
    )
    
    print(f"Created TaskCreate model: {task_create.title}")
    
    # Test TaskUpdate model
    task_update = TaskUpdate(status="completed")
    print(f"Created TaskUpdate model with status: {task_update.status}")
    
    print("All models working correctly!")


if __name__ == "__main__":
    test_models()