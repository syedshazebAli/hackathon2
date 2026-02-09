from sqlmodel import create_engine, Session
from sqlalchemy import Engine
import os

# Hardcode SQLite database engine
engine: Engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False}, echo=True)


def get_session():
    with Session(engine) as session:
        yield session