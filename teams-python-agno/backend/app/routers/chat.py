"""
Chat Router
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from fastapi import APIRouter, HTTPException, status
import agentops
from bson import ObjectId
from app.database import get_database
from app.models import ChatMessage, ChatResponse
from app.agents import chat_agent
import uuid


router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Endpoint de chat com RAG
    AgentOps rastreia automaticamente esta sessão
    """
    db = get_database()
    
    # Valida bot_id
    if not ObjectId.is_valid(message.bot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de bot inválido"
        )
    
    # Busca bot
    bot = await db.bots.find_one({"_id": ObjectId(message.bot_id)})
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot não encontrado"
        )
    
    # Inicia sessão AgentOps (se não existe)
    session_id = message.session_id or str(uuid.uuid4())
    
    try:
        # Usa agente de chat
        result = await chat_agent.chat_with_rag(
            bot_id=message.bot_id,
            bot_instructions=bot["instructions"],
            user_message=message.message,
            enable_rag=bot.get("enable_rag", True)
        )
        
        # Salva no histórico
        history_entry = {
            "bot_id": message.bot_id,
            "session_id": session_id,
            "message": message.message,
            "response": result["response"],
            "sources": result["sources"],
            "model": result.get("model"),
            "tokens_used": result.get("tokens_used", 0)
        }
        
        await db.chat_history.insert_one(history_entry)
        
        # Retorna resposta
        return ChatResponse(
            bot_id=message.bot_id,
            message=message.message,
            response=result["response"],
            sources=result["sources"],
            session_id=session_id
        )
        
    except Exception as e:
        # AgentOps rastreia o erro automaticamente
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar chat: {str(e)}"
        )


@router.get("/history")
async def get_chat_history(bot_id: str = None, session_id: str = None, limit: int = 50):
    """Busca histórico de chat"""
    db = get_database()
    
    query = {}
    if bot_id:
        query["bot_id"] = bot_id
    if session_id:
        query["session_id"] = session_id
    
    history = []
    cursor = db.chat_history.find(query).sort("timestamp", -1).limit(limit)
    
    async for entry in cursor:
        history.append({
            "id": str(entry["_id"]),
            "bot_id": entry["bot_id"],
            "session_id": entry.get("session_id"),
            "message": entry["message"],
            "response": entry["response"],
            "sources": entry.get("sources", []),
            "timestamp": entry.get("timestamp")
        })
    
    return history
