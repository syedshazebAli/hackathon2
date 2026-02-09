from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(nullable=False)


class Task(TaskBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ConversationBase(SQLModel):
    user_id: str = Field(nullable=False)
    title: Optional[str] = Field(default=None)


class Conversation(ConversationBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageBase(SQLModel):
    conversation_id: str = Field(nullable=False)
    role: str = Field(nullable=False)  # user, assistant, system
    content: str = Field(nullable=False)


class Message(MessageBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)