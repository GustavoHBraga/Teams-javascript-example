"""
Documents Router
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, BackgroundTasks
from typing import List
import aiofiles
from bson import ObjectId
import uuid
from app.database import get_database
from app.models import DocumentResponse
from app.services import rag_service
from shared.config import UPLOADS_DIR


router = APIRouter()


# Tipos de arquivo permitidos
ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
    "text/markdown": ".md"
}


async def process_document_background(
    doc_id: str,
    bot_id: str,
    file_path: str,
    filename: str,
    content_type: str
):
    """Processa documento em background"""
    db = get_database()
    
    try:
        # Processa com RAG
        chunk_count = await rag_service.process_document(
            bot_id=bot_id,
            file_path=file_path,
            filename=filename,
            content_type=content_type
        )
        
        # Atualiza status
        await db.documents.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": {"status": "completed", "chunk_count": chunk_count}}
        )
        
        print(f"✅ Documento processado: {filename} ({chunk_count} chunks)")
        
    except Exception as e:
        # Marca como falha
        await db.documents.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": {"status": "failed"}}
        )
        print(f"❌ Erro ao processar documento: {e}")


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    bot_id: str = Form(...)
):
    """Upload de documento para treinamento"""
    db = get_database()
    
    # Valida bot_id
    if not ObjectId.is_valid(bot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de bot inválido"
        )
    
    # Verifica se bot existe
    bot = await db.bots.find_one({"_id": ObjectId(bot_id)})
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot não encontrado"
        )
    
    # Valida tipo de arquivo
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não suportado. Tipos permitidos: {', '.join(ALLOWED_TYPES.keys())}"
        )
    
    # Salva arquivo
    file_ext = ALLOWED_TYPES[file.content_type]
    file_id = str(uuid.uuid4())
    file_path = UPLOADS_DIR / f"{file_id}{file_ext}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Cria documento no MongoDB
    document = {
        "bot_id": bot_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "status": "processing",
        "chunk_count": 0
    }
    
    result = await db.documents.insert_one(document)
    doc_id = str(result.inserted_id)
    
    # Processa em background
    background_tasks.add_task(
        process_document_background,
        doc_id,
        bot_id,
        str(file_path),
        file.filename,
        file.content_type
    )
    
    # Retorna documento
    created_doc = await db.documents.find_one({"_id": result.inserted_id})
    
    return DocumentResponse(
        id=str(created_doc["_id"]),
        bot_id=created_doc["bot_id"],
        filename=created_doc["filename"],
        content_type=created_doc["content_type"],
        file_size=created_doc["file_size"],
        status=created_doc["status"],
        chunk_count=created_doc["chunk_count"],
        created_at=created_doc["created_at"]
    )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(bot_id: str = None):
    """Lista documentos (opcionalmente filtrado por bot)"""
    db = get_database()
    
    query = {}
    if bot_id:
        query["bot_id"] = bot_id
    
    documents = []
    cursor = db.documents.find(query)
    
    async for doc in cursor:
        documents.append(DocumentResponse(
            id=str(doc["_id"]),
            bot_id=doc["bot_id"],
            filename=doc["filename"],
            content_type=doc["content_type"],
            file_size=doc["file_size"],
            status=doc["status"],
            chunk_count=doc["chunk_count"],
            created_at=doc["created_at"]
        ))
    
    return documents


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(doc_id: str):
    """Deleta um documento"""
    db = get_database()
    
    # Valida ObjectId
    if not ObjectId.is_valid(doc_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de documento inválido"
        )
    
    # Deleta documento
    result = await db.documents.delete_one({"_id": ObjectId(doc_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return None
