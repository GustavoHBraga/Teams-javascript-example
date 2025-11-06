"""
Database models with SQLAlchemy (SQLite/PostgreSQL)
Also includes MongoDB models for future migration
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from database import Base
import uuid


def generate_uuid():
    """Generate unique ID"""
    return str(uuid.uuid4())


# ==================== SQLAlchemy Models (SQLite/PostgreSQL) ====================

class Bot(Base):
    """Bot model - AI agents created by users"""
    __tablename__ = "bots"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    
    # RAG Configuration
    enable_rag = Column(Boolean, default=False)
    
    # Metadata
    created_by = Column(String(100), nullable=False, default="user@example.com")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    documents = relationship("Document", back_populates="bot", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="bot", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "enable_rag": self.enable_rag,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active
        }


class Document(Base):
    """Document model - Files uploaded for RAG"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    bot_id = Column(String, ForeignKey("bots.id"), nullable=False)
    
    # File information
    filename = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Processing
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    chunk_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bot = relationship("Bot", back_populates="documents")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "bot_id": self.bot_id,
            "filename": self.filename,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "status": self.status,
            "chunk_count": self.chunk_count,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Conversation(Base):
    """Conversation model - Chat sessions"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    bot_id = Column(String, ForeignKey("bots.id"), nullable=False)
    
    # Metadata
    user_id = Column(String(100), nullable=False, default="user@example.com")
    started_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    bot = relationship("Bot", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "bot_id": self.bot_id,
            "user_id": self.user_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
            "is_active": self.is_active
        }


class Message(Base):
    """Message model - Individual chat messages"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ==================== Pydantic Schemas (API) ====================

class BotCreate(BaseModel):
    """Schema para criação de bot"""
    name: str
    description: str
    instructions: str
    enable_rag: bool = True


class BotResponse(BaseModel):
    """Schema de resposta de bot"""
    id: str
    name: str
    description: str
    instructions: str
    enable_rag: bool
    created_at: datetime
    updated_at: datetime


class DocumentResponse(BaseModel):
    """Schema de resposta de documento"""
    id: str
    bot_id: str
    filename: str
    content_type: str
    file_size: int
    status: str
    chunk_count: int
    created_at: datetime


class ChatMessage(BaseModel):
    """Mensagem de chat"""
    bot_id: str
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Resposta de chat"""
    bot_id: str
    message: str
    response: str
    sources: List[str] = []
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

