"""
RAG Service with LangChain and OpenAI
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from typing import List, Dict
import aiofiles
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from docx import Document
from shared.config import settings, UPLOADS_DIR
from .chromadb_service import chroma_service


class RAGService:
    """Serviço de RAG (Retrieval Augmented Generation)"""
    
    def __init__(self):
        # OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key,
            model=settings.embedding_model
        )
        
        # Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        print("✅ RAG Service inicializado")
    
    async def extract_text(self, file_path: str, content_type: str) -> str:
        """Extrai texto de diferentes tipos de arquivo"""
        
        if content_type == "application/pdf":
            return await self._extract_from_pdf(file_path)
        
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await self._extract_from_docx(file_path)
        
        elif content_type in ["text/plain", "text/markdown"]:
            return await self._extract_from_text(file_path)
        
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {content_type}")
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        """Extrai texto de PDF"""
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        return "\n\n".join([page.page_content for page in pages])
    
    async def _extract_from_docx(self, file_path: str) -> str:
        """Extrai texto de DOCX"""
        doc = Document(file_path)
        return "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    async def _extract_from_text(self, file_path: str) -> str:
        """Extrai texto de arquivo texto"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    
    async def process_document(
        self,
        bot_id: str,
        file_path: str,
        filename: str,
        content_type: str
    ) -> int:
        """Processa documento completo: extrai texto, divide em chunks, gera embeddings"""
        
        # 1. Extrai texto
        text = await self.extract_text(file_path, content_type)
        
        if not text.strip():
            raise ValueError("Documento vazio ou não foi possível extrair texto")
        
        # 2. Divide em chunks
        chunks = self.text_splitter.split_text(text)
        
        # 3. Gera embeddings (batch)
        embeddings = await self._generate_embeddings_batch(chunks)
        
        # 4. Prepara metadatas
        metadatas = [
            {
                "bot_id": bot_id,
                "filename": filename,
                "chunk_index": i,
                "source": filename
            }
            for i in range(len(chunks))
        ]
        
        # 5. Adiciona ao ChromaDB
        count = await chroma_service.add_documents(
            bot_id=bot_id,
            chunks=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return count
    
    async def _generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings em batch para melhor performance"""
        # OpenAI permite até 2048 textos por request
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embeddings.embed_documents(batch)
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    async def search_relevant_documents(
        self,
        bot_id: str,
        query: str,
        max_results: int = None
    ) -> List[Dict]:
        """Busca documentos relevantes para uma query"""
        
        if max_results is None:
            max_results = settings.max_chunks_per_query
        
        # 1. Gera embedding da query
        query_embedding = self.embeddings.embed_query(query)
        
        # 2. Busca no ChromaDB
        results = await chroma_service.search_similar(
            bot_id=bot_id,
            query_embedding=query_embedding,
            n_results=max_results
        )
        
        # 3. Formata resultados
        documents = []
        if results and "documents" in results and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                distance = results["distances"][0][i] if "distances" in results else 0
                
                documents.append({
                    "content": doc,
                    "metadata": metadata,
                    "similarity": 1 - distance,  # Converte distância em similaridade
                    "source": metadata.get("filename", "Unknown")
                })
        
        return documents


# Instância global
rag_service = RAGService()
