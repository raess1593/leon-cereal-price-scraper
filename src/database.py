"""Database bootstrap layer for SQLAlchemy engine, sessions, and metadata."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Local SQLite database stored inside the project data directory.
db_url = "sqlite:///data/lonja.db"
engine = create_engine(url=db_url, connect_args={"check_same_thread": False})
# Session factory used by scripts to open short-lived units of work.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Declarative base shared by all ORM models in this project.
Base = declarative_base()