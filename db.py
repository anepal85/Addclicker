# db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configure your database URL here (e.g., SQLite, MySQL, PostgreSQL)
DATABASE_URL = 'sqlite:///clicks.db'  # Change this to your desired database

# Create the engine
engine = create_engine(DATABASE_URL)

# Bind the engine to the Base's metadata
Base.metadata.bind = engine

# Create all tables (if they don't exist)
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def get_session():
    """Create and return a new database session."""
    return Session()
