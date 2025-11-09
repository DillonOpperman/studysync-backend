# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_mysql_password_here')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'studysync')

# Create database URL
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # Set to True for SQL query logging
)

# Create session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Initialize the database"""
    # Import all models here
    from models import User, StudyGroup, GroupMember, Message, MessageReaction, StudySession, SessionAttendee
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_db():
    """Get database session"""
    return db_session

def close_db():
    """Close database session"""
    db_session.remove()