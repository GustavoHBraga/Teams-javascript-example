"""
RAG Service Refatorado - Dinâmico e Modular
Suporta múltiplos vector stores e Azure OpenAI
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from typing import List, Dict, Optional
import aiofiles
from shared.config import settings
from app.adapters.llm_adapter import get_llm_adapter
from app.adapters.vector_store_adapter import get_vector_store_adapter


class RAGService:
    """Serviço RAG genérico e assertivo"""
    
    def __init__(self):
        # Adaptadores dinâmicos
        self.llm_adapter = get_llm_adapter(settings)
        self.vector_store = get_vector_store_adapter(settings)
        
        # Text Splitter (sem LangChain para menos dependências)
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        
        print("✅ RAG Service inicializado")
        print(f"   Vector Store: {settings.vector_store}")
        print(f"   LLM Provider: {'Azure OpenAI' if settings.use_azure else 'OpenAI'}")
    
    async def extract_text_from_file(
        self,
        file_path: str,
        content_type: str
    ) -> str:
        """Extrai texto de diferentes tipos de arquivos"""
        
        if content_type == "application/pdf":
            return await self._extract_from_pdf(file_path)
        
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await self._extract_from_docx(file_path)
        
        elif content_type in ["text/plain", "text/markdown", "text/md"]:
            return await self._extract_from_text(file_path)
        
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {content_type}")
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        """Extrai texto de PDF"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text.strip():
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Erro ao extrair PDF: {e}")
    
    async def _extract_from_docx(self, file_path: str) -> str:
        """Extrai texto de DOCX"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise ValueError(f"Erro ao extrair DOCX: {e}")
    
    async def _extract_from_text(self, file_path: str) -> str:
        """Extrai texto de arquivo texto"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo: {e}")
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """
        Divide texto em chunks com overlap
        Implementação simples sem dependências pesadas
        """
        if not text.strip():
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Define fim do chunk
            end = start + self.chunk_size
            
            # Se não é o último chunk, tenta quebrar em uma quebra de linha
            if end < text_length:
                # Procura por quebra de linha próxima
                newline_pos = text.rfind('\n', start, end)
                if newline_pos > start:
                    end = newline_pos
                # Senão, procura por espaço
                else:
                    space_pos = text.rfind(' ', start, end)
                    if space_pos > start:
                        end = space_pos
            
            # Extrai chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start considerando overlap
            start = end - self.chunk_overlap if end < text_length else text_length
        
        return chunks
    
    async def process_document(
        self,
        bot_id: str,
        file_path: str,
        filename: str,
        content_type: str
    ) -> int:
        """
        Processa documento completo:
        1. Extrai texto
        2. Divide em chunks
        3. Gera embeddings
        4. Armazena no vector store
        """
        
        # 1. Extrai texto
        text = await self.extract_text_from_file(file_path, content_type)
        
        if not text.strip():
            raise ValueError("Documento vazio ou texto não extraído")
        
        # 2. Divide em chunks
        chunks = self.split_text_into_chunks(text)
        
        if not chunks:
            raise ValueError("Nenhum chunk gerado do documento")
        
        print(f"📄 {len(chunks)} chunks criados de '{filename}'")
        
        # 3. Gera embeddings (batch)
        embeddings = await self.llm_adapter.generate_embeddings_batch(chunks)
        
        print(f"🔢 {len(embeddings)} embeddings gerados")
        
        # 4. Prepara metadatas
        metadatas = [
            {
                "bot_id": bot_id,
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "source": filename
            }
            for i in range(len(chunks))
        ]
        
        # 5. Armazena no vector store
        count = await self.vector_store.add_documents(
            collection_name=f"bot_{bot_id}",
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        print(f"✅ {count} documentos adicionados ao vector store")
        
        return count
    
    async def search_relevant_documents(
        self,
        bot_id: str,
        query: str,
        max_results: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca documentos relevantes para uma query
        """
        
        if max_results is None:
            max_results = settings.max_chunks_per_query
        
        # 1. Gera embedding da query
        query_embedding = await self.llm_adapter.generate_embedding(query)
        
        # 2. Busca no vector store
        results = await self.vector_store.search_similar(
            collection_name=f"bot_{bot_id}",
            query_embedding=query_embedding,
            n_results=max_results,
            filter_metadata={"bot_id": bot_id}
        )
        
        # 3. Formata resultados
        documents = []
        
        if results and "documents" in results and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                if not doc:
                    continue
                
                metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                distance = results["distances"][0][i] if "distances" in results else 1.0
                
                # Converte distância em similaridade (1 = idêntico, 0 = diferente)
                similarity = 1 - min(distance, 1.0)
                
                # Filtra por threshold
                if similarity >= settings.similarity_threshold:
                    documents.append({
                        "content": doc,
                        "metadata": metadata,
                        "similarity": similarity,
                        "source": metadata.get("filename", "Unknown"),
                        "chunk_index": metadata.get("chunk_index", 0)
                    })
        
        # Ordena por similaridade
        documents.sort(key=lambda x: x["similarity"], reverse=True)
        
        print(f"🔍 {len(documents)} documentos relevantes encontrados (threshold: {settings.similarity_threshold})")
        
        return documents
    
    async def delete_bot_documents(self, bot_id: str) -> bool:
        """Deleta todos documentos de um bot"""
        try:
            result = await self.vector_store.delete_collection(f"bot_{bot_id}")
            if result:
                print(f"🗑️ Documentos do bot {bot_id} deletados")
            return result
        except Exception as e:
            print(f"❌ Erro ao deletar documentos: {e}")
            return False
    
    async def get_bot_document_count(self, bot_id: str) -> int:
        """Retorna número de documentos de um bot"""
        try:
            count = await self.vector_store.get_collection_count(f"bot_{bot_id}")
            return count
        except Exception as e:
            print(f"❌ Erro ao contar documentos: {e}")
            return 0


# Instância global
rag_service = RAGService()
