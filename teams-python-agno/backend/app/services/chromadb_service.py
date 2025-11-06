"""
ChromaDB Service - Vector Database
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from shared.config import settings
import uuid


class ChromaDBService:
    """Serviço para gerenciar ChromaDB"""
    
    def __init__(self):
        # Inicializa cliente ChromaDB
        self.client = chromadb.PersistentClient(
            path=settings.chromadb_path,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        print(f"✅ ChromaDB inicializado: {settings.chromadb_path}")
    
    def get_or_create_collection(self, bot_id: str):
        """Obtém ou cria collection para um bot"""
        collection_name = f"bot_{bot_id}"
        
        collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"bot_id": bot_id}
        )
        
        return collection
    
    async def add_documents(
        self,
        bot_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict]
    ) -> int:
        """Adiciona documentos ao ChromaDB"""
        collection = self.get_or_create_collection(bot_id)
        
        # Gera IDs únicos para cada chunk
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        # Adiciona ao ChromaDB
        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return len(chunks)
    
    async def search_similar(
        self,
        bot_id: str,
        query_embedding: List[float],
        n_results: int = 5
    ) -> Dict:
        """Busca documentos similares"""
        collection = self.get_or_create_collection(bot_id)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    
    async def delete_bot_documents(self, bot_id: str):
        """Deleta todos documentos de um bot"""
        try:
            collection_name = f"bot_{bot_id}"
            self.client.delete_collection(name=collection_name)
            print(f"🗑️ Collection deletada: {collection_name}")
        except Exception as e:
            print(f"⚠️ Erro ao deletar collection: {e}")
    
    async def get_collection_count(self, bot_id: str) -> int:
        """Retorna número de documentos na collection"""
        try:
            collection = self.get_or_create_collection(bot_id)
            return collection.count()
        except:
            return 0


# Instância global
chroma_service = ChromaDBService()
