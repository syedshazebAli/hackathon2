from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from models import Task, TaskRead, TaskCreate, TaskUpdate, User
from database import engine, get_session
# from auth import get_current_user

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # For testing, return all tasks (without user filtering)
    # In a real implementation, you would still filter by user
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/tasks", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # For testing without auth, create or get a default user
    # In a real implementation, you would use the authenticated user's ID
    
    # Check if the user exists, if not create a default user
    user = session.get(User, task.user_id)
    if not user:
        # Create a default user with the provided ID
        user = User(
            id=task.user_id,
            email="default@test.com",
            name="Default User"
        )
        session.add(user)
        session.commit()
    
    # Create the task with the validated data
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(
    task_id: UUID,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # Find the task (without user filtering for testing)
    # In a real implementation, you would still filter by user
    statement = select(Task).where(Task.id == task_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    task: TaskUpdate,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # Find the task (without user filtering for testing)
    # In a real implementation, you would still filter by user
    statement = select(Task).where(Task.id == task_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided values
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # Find the task (without user filtering for testing)
    # In a real implementation, you would still filter by user
    statement = select(Task).where(Task.id == task_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete")
def complete_task(
    task_id: UUID,
    session: Session = Depends(get_session)
    # current_user: User = Depends(get_current_user)
):
    # Find the task (without user filtering for testing)
    # In a real implementation, you would still filter by user
    statement = select(Task).where(Task.id == task_id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task status to completed and set completed_at timestamp
    db_task.status = "completed"
    from datetime import datetime
    db_task.completed_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return {"message": "Task marked as completed", "task": db_task}