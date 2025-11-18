"""Database connection management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.database import Base

# Get database path
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src', 'database')
DB_PATH = os.path.join(DB_DIR, 'predictions.db')

# Ensure directory exists
os.makedirs(DB_DIR, exist_ok=True)

# Create engine
DATABASE_URL = f'sqlite:///{DB_PATH}'
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def get_engine():
    """Get database engine."""
    return engine


def get_session():
    """Get database session."""
    return Session()


def init_db():
    """Initialize database - create all tables."""
    Base.metadata.create_all(engine)
    print(f"Database initialized at: {DB_PATH}")


def close_session():
    """Close current session."""
    Session.remove()



