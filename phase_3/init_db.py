import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import engine
from backend.models import Task, Conversation, Message
from sqlmodel import SQLModel

def create_tables():
    print("Initializing database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    print("- Task table")
    print("- Conversation table") 
    print("- Message table")

if __name__ == "__main__":
    create_tables()