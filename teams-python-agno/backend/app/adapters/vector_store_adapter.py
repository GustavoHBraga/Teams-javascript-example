"""
Vector Store Adapter - Suporta ChromaDB, FAISS, Qdrant
Adaptador genérico para diferentes bancos vetoriais
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import numpy as np
from shared.config import Settings


class BaseVectorStoreAdapter(ABC):
    """Interface base para adaptadores de vector store"""
    
    @abstractmethod
    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> int:
        """Adiciona documentos ao store"""
        pass
    
    @abstractmethod
    async def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """Busca documentos similares"""
        pass
    
    @abstractmethod
    async def delete_collection(self, collection_name: str) -> bool:
        """Deleta uma collection"""
        pass
    
    @abstractmethod
    async def get_collection_count(self, collection_name: str) -> int:
        """Retorna número de documentos na collection"""
        pass


class ChromaDBAdapter(BaseVectorStoreAdapter):
    """Adaptador para ChromaDB"""
    
    def __init__(self, settings: Settings):
        import chromadb
        from chromadb.config import Settings as ChromaSettings
        
        self.settings = settings
        
        # Cliente persistente
        self.client = chromadb.PersistentClient(
            path=settings.chromadb_persist_dir,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        print(f"✅ ChromaDB Adapter inicializado: {settings.chromadb_persist_dir}")
    
    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> int:
        """Adiciona documentos ao ChromaDB"""
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": f"Documents for bot {collection_name}"}
            )
            
            # Gera IDs se não fornecidos
            if ids is None:
                import uuid
                ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            
            # Adiciona em batch
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            return len(documents)
        except Exception as e:
            print(f"❌ Erro ao adicionar documentos ao ChromaDB: {e}")
            raise
    
    async def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """Busca documentos similares no ChromaDB"""
        try:
            collection = self.client.get_collection(name=collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            return results
        except Exception as e:
            print(f"❌ Erro ao buscar no ChromaDB: {e}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    async def delete_collection(self, collection_name: str) -> bool:
        """Deleta collection do ChromaDB"""
        try:
            self.client.delete_collection(name=collection_name)
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar collection: {e}")
            return False
    
    async def get_collection_count(self, collection_name: str) -> int:
        """Retorna contagem de documentos"""
        try:
            collection = self.client.get_collection(name=collection_name)
            return collection.count()
        except:
            return 0


class FAISSAdapter(BaseVectorStoreAdapter):
    """Adaptador para FAISS (local, rápido)"""
    
    def __init__(self, settings: Settings):
        import faiss
        import pickle
        from pathlib import Path
        
        self.settings = settings
        self.faiss_path = Path(settings.faiss_index_path)
        self.faiss_path.mkdir(parents=True, exist_ok=True)
        
        # Dicionário de índices em memória
        self.indexes: Dict[str, Any] = {}
        self.metadata_store: Dict[str, List[Dict]] = {}
        
        print(f"✅ FAISS Adapter inicializado: {settings.faiss_index_path}")
    
    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> int:
        """Adiciona documentos ao FAISS"""
        import faiss
        import pickle
        
        try:
            embeddings_array = np.array(embeddings).astype('float32')
            dimension = embeddings_array.shape[1]
            
            # Cria ou carrega índice
            if collection_name not in self.indexes:
                index = faiss.IndexFlatL2(dimension)
                self.indexes[collection_name] = index
                self.metadata_store[collection_name] = []
            
            index = self.indexes[collection_name]
            
            # Adiciona vetores
            index.add(embeddings_array)
            
            # Armazena metadados
            for i, doc in enumerate(documents):
                meta = metadatas[i].copy()
                meta['document'] = doc
                self.metadata_store[collection_name].append(meta)
            
            # Persiste
            self._save_index(collection_name)
            
            return len(documents)
        except Exception as e:
            print(f"❌ Erro ao adicionar ao FAISS: {e}")
            raise
    
    async def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """Busca documentos similares no FAISS"""
        import faiss
        
        try:
            if collection_name not in self.indexes:
                self._load_index(collection_name)
            
            if collection_name not in self.indexes:
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
            query_array = np.array([query_embedding]).astype('float32')
            
            distances, indices = self.indexes[collection_name].search(query_array, n_results)
            
            # Formata resultados
            documents = []
            metadatas = []
            
            for idx in indices[0]:
                if idx < len(self.metadata_store[collection_name]):
                    meta = self.metadata_store[collection_name][idx]
                    documents.append(meta.pop('document', ''))
                    metadatas.append(meta)
            
            return {
                "documents": [documents],
                "metadatas": [metadatas],
                "distances": distances.tolist()
            }
        except Exception as e:
            print(f"❌ Erro ao buscar no FAISS: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    async def delete_collection(self, collection_name: str) -> bool:
        """Deleta collection do FAISS"""
        try:
            if collection_name in self.indexes:
                del self.indexes[collection_name]
                del self.metadata_store[collection_name]
            
            index_file = self.faiss_path / f"{collection_name}.index"
            meta_file = self.faiss_path / f"{collection_name}.meta"
            
            if index_file.exists():
                index_file.unlink()
            if meta_file.exists():
                meta_file.unlink()
            
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar FAISS collection: {e}")
            return False
    
    async def get_collection_count(self, collection_name: str) -> int:
        """Retorna contagem"""
        try:
            if collection_name in self.metadata_store:
                return len(self.metadata_store[collection_name])
            return 0
        except:
            return 0
    
    def _save_index(self, collection_name: str):
        """Salva índice em disco"""
        import faiss
        import pickle
        
        index_file = self.faiss_path / f"{collection_name}.index"
        meta_file = self.faiss_path / f"{collection_name}.meta"
        
        faiss.write_index(self.indexes[collection_name], str(index_file))
        
        with open(meta_file, 'wb') as f:
            pickle.dump(self.metadata_store[collection_name], f)
    
    def _load_index(self, collection_name: str):
        """Carrega índice do disco"""
        import faiss
        import pickle
        
        index_file = self.faiss_path / f"{collection_name}.index"
        meta_file = self.faiss_path / f"{collection_name}.meta"
        
        if index_file.exists() and meta_file.exists():
            self.indexes[collection_name] = faiss.read_index(str(index_file))
            
            with open(meta_file, 'rb') as f:
                self.metadata_store[collection_name] = pickle.load(f)


class QdrantAdapter(BaseVectorStoreAdapter):
    """Adaptador para Qdrant (cloud/self-hosted)"""
    
    def __init__(self, settings: Settings):
        from qdrant_client import AsyncQdrantClient
        from qdrant_client.models import Distance, VectorParams
        
        self.settings = settings
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        print(f"✅ Qdrant Adapter inicializado: {settings.qdrant_url}")
    
    async def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> int:
        """Adiciona documentos ao Qdrant"""
        from qdrant_client.models import PointStruct, Distance, VectorParams
        import uuid
        
        try:
            # Cria collection se não existir
            try:
                await self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=len(embeddings[0]),
                        distance=Distance.COSINE
                    )
                )
            except:
                pass  # Collection já existe
            
            # Prepara pontos
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            
            points = [
                PointStruct(
                    id=ids[i],
                    vector=embeddings[i],
                    payload={**metadatas[i], "document": documents[i]}
                )
                for i in range(len(documents))
            ]
            
            # Adiciona pontos
            await self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            
            return len(documents)
        except Exception as e:
            print(f"❌ Erro ao adicionar ao Qdrant: {e}")
            raise
    
    async def search_similar(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """Busca documentos similares no Qdrant"""
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        try:
            # Prepara filtro se necessário
            query_filter = None
            if filter_metadata:
                conditions = [
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_metadata.items()
                ]
                query_filter = Filter(must=conditions)
            
            # Busca
            results = await self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=n_results,
                query_filter=query_filter
            )
            
            # Formata resultados
            documents = [r.payload.get('document', '') for r in results]
            metadatas = [{k: v for k, v in r.payload.items() if k != 'document'} for r in results]
            distances = [r.score for r in results]
            
            return {
                "documents": [documents],
                "metadatas": [metadatas],
                "distances": [distances]
            }
        except Exception as e:
            print(f"❌ Erro ao buscar no Qdrant: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    async def delete_collection(self, collection_name: str) -> bool:
        """Deleta collection do Qdrant"""
        try:
            await self.client.delete_collection(collection_name=collection_name)
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar Qdrant collection: {e}")
            return False
    
    async def get_collection_count(self, collection_name: str) -> int:
        """Retorna contagem"""
        try:
            info = await self.client.get_collection(collection_name=collection_name)
            return info.points_count
        except:
            return 0


class VectorStoreAdapterFactory:
    """Factory para criar o adaptador correto"""
    
    @staticmethod
    def create_adapter(settings: Settings) -> BaseVectorStoreAdapter:
        """Cria adaptador baseado na configuração"""
        if settings.vector_store == "chromadb":
            return ChromaDBAdapter(settings)
        elif settings.vector_store == "faiss":
            return FAISSAdapter(settings)
        elif settings.vector_store == "qdrant":
            return QdrantAdapter(settings)
        else:
            raise ValueError(f"Vector store não suportado: {settings.vector_store}")


# Instância global
_vector_store_adapter: Optional[BaseVectorStoreAdapter] = None


def get_vector_store_adapter(settings: Settings = None) -> BaseVectorStoreAdapter:
    """Obtém instância do adaptador de vector store"""
    global _vector_store_adapter
    
    if _vector_store_adapter is None:
        if settings is None:
            from shared.config import settings as default_settings
            settings = default_settings
        _vector_store_adapter = VectorStoreAdapterFactory.create_adapter(settings)
    
    return _vector_store_adapter
