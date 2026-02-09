from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_NWatng38HLGQ@ep-bitter-salad-ai18jb4i-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session