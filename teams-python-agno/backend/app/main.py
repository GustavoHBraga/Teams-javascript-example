"""
FastAPI Application with AgentOps Integration
"""
import sys
from pathlib import Path

# Adiciona pasta raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import agentops
from shared.config import settings
from app.routers import bots, documents, chat
from app.database import connect_db, close_db


# Inicializa AgentOps
agentops.init(
    api_key=settings.agentops_api_key,
    default_tags=["teams-bot", "production"]
)

# Cria aplicação FastAPI
app = FastAPI(
    title="Teams Bot Automation API",
    description="API para gerenciamento de bots com RAG e AgentOps",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Events
@app.on_event("startup")
async def startup_event():
    """Executa na inicialização"""
    await connect_db()
    print("🚀 API iniciada com sucesso!")
    print(f"📊 AgentOps ativo: {agentops.is_initialized()}")
    print(f"📝 Docs: http://{settings.api_host}:{settings.api_port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Executa no desligamento"""
    await close_db()
    agentops.end_all_sessions()
    print("👋 API encerrada")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agentops": agentops.is_initialized(),
        "version": "1.0.0"
    }


# Rotas
app.include_router(bots.router, prefix="/api/bots", tags=["Bots"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


# Root
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Teams Bot Automation API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
