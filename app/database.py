"""Database models and session management."""
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import config

Base = declarative_base()

class Intelligence(Base):
    """Table for storing extracted intelligence."""
    __tablename__ = "intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    type = Column(String)  # bank_account, upi_id, phone, url, ifsc
    value = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    """Table for storing conversation history."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, unique=True, index=True)
    persona = Column(String)
    messages = Column(Text)  # JSON string of messages
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create engine and session
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
