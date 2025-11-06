"""
Bots Router
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from app.database import get_database
from app.models import BotCreate, BotResponse, BotModel
from app.services import chroma_service


router = APIRouter()


@router.post("/", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(bot: BotCreate):
    """Cria um novo bot"""
    db = get_database()
    
    # Prepara documento
    bot_dict = bot.model_dump()
    
    # Insere no MongoDB
    result = await db.bots.insert_one(bot_dict)
    
    # Busca bot criado
    created_bot = await db.bots.find_one({"_id": result.inserted_id})
    
    # Converte para response
    return BotResponse(
        id=str(created_bot["_id"]),
        name=created_bot["name"],
        description=created_bot["description"],
        instructions=created_bot["instructions"],
        enable_rag=created_bot["enable_rag"],
        created_at=created_bot["created_at"],
        updated_at=created_bot["updated_at"]
    )


@router.get("/", response_model=List[BotResponse])
async def list_bots():
    """Lista todos os bots"""
    db = get_database()
    
    bots = []
    cursor = db.bots.find()
    
    async for bot in cursor:
        bots.append(BotResponse(
            id=str(bot["_id"]),
            name=bot["name"],
            description=bot["description"],
            instructions=bot["instructions"],
            enable_rag=bot["enable_rag"],
            created_at=bot["created_at"],
            updated_at=bot["updated_at"]
        ))
    
    return bots


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: str):
    """Busca bot por ID"""
    db = get_database()
    
    # Valida ObjectId
    if not ObjectId.is_valid(bot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de bot inválido"
        )
    
    # Busca bot
    bot = await db.bots.find_one({"_id": ObjectId(bot_id)})
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot não encontrado"
        )
    
    return BotResponse(
        id=str(bot["_id"]),
        name=bot["name"],
        description=bot["description"],
        instructions=bot["instructions"],
        enable_rag=bot["enable_rag"],
        created_at=bot["created_at"],
        updated_at=bot["updated_at"]
    )


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(bot_id: str):
    """Deleta um bot e seus documentos"""
    db = get_database()
    
    # Valida ObjectId
    if not ObjectId.is_valid(bot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de bot inválido"
        )
    
    # Deleta bot
    result = await db.bots.delete_one({"_id": ObjectId(bot_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot não encontrado"
        )
    
    # Deleta documentos do bot
    await db.documents.delete_many({"bot_id": bot_id})
    
    # Deleta collection no ChromaDB
    await chroma_service.delete_bot_documents(bot_id)
    
    return None
