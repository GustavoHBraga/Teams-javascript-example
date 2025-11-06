"""
Configuração compartilhada entre backend e frontend
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # MongoDB
    mongodb_url: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URL")
    mongodb_db_name: str = Field(default="teams_bots_python", alias="MONGODB_DB_NAME")
    
    # OpenAI
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    chat_model: str = Field(default="gpt-4-turbo-preview", alias="CHAT_MODEL")
    
    # AgentOps
    agentops_api_key: str = Field(alias="AGENTOPS_API_KEY")
    
    # ChromaDB
    chromadb_host: str = Field(default="localhost", alias="CHROMADB_HOST")
    chromadb_port: int = Field(default=8000, alias="CHROMADB_PORT")
    chromadb_path: str = Field(default="./data/chromadb", alias="CHROMADB_PATH")
    
    # API
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_reload: bool = Field(default=True, alias="API_RELOAD")
    
    # RAG
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")
    max_chunks_per_query: int = Field(default=5, alias="MAX_CHUNKS_PER_QUERY")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", alias="LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global de configurações
settings = Settings()


# Diretórios importantes
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
UPLOADS_DIR = DATA_DIR / "uploads"

# Criar diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR, UPLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
