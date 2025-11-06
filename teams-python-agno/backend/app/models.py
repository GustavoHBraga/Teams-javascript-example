"""
Pydantic models for MongoDB documents
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BotModel(BaseModel):
    """Modelo de Bot"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    instructions: str
    enable_rag: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


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


class DocumentModel(BaseModel):
    """Modelo de Documento"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    bot_id: str
    filename: str
    content_type: str
    file_size: int
    status: str = "processing"  # processing, completed, failed
    chunk_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


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
