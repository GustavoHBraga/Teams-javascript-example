# 🔄 Guia de Migração - v1.0 → v2.0

## O que Mudou?

### ✅ Melhorias Principais

1. **Azure OpenAI Corporativo**
   - Antes: OpenAI padrão (openai.com)
   - Agora: Azure OpenAI (instância corporativa)
   - Benefício: Dados ficam dentro do Azure, conformidade LGPD

2. **Database Dinâmico**
   - Antes: MongoDB fixo
   - Agora: SQLite (padrão), PostgreSQL ou MongoDB
   - Benefício: Começa simples, escala quando precisar

3. **Vector Store Flexível**
   - Antes: ChromaDB fixo
   - Agora: ChromaDB (padrão), FAISS ou Qdrant
   - Benefício: Escolha a melhor opção para seu caso

4. **Arquitetura Modular**
   - Antes: Código acoplado
   - Agora: Adapters pattern (LLM e Vector Store)
   - Benefício: Troca de provider sem reescrever código

5. **Menos Dependências**
   - Antes: LangChain pesado
   - Agora: Implementação própria, leve
   - Benefício: Mais rápido, menos bugs

## 📋 Checklist de Migração

### 1. Backup dos Dados Atuais

```powershell
# Backup MongoDB (se estiver usando)
mongodump --db teams_bots_python --out ./backup_mongodb

# Backup ChromaDB
Copy-Item -Recurse ./data/chromadb ./backup_chromadb
```

### 2. Configure Azure OpenAI

**No Azure Portal:**

1. Crie recurso "Azure OpenAI"
2. Crie deployments:
   - Chat: `gpt-4` ou `gpt-35-turbo`
   - Embedding: `text-embedding-ada-002`
3. Copie endpoint e API key

**No projeto:**

```env
USE_AZURE_OPENAI=true
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_KEY=sua-chave
AZURE_CHAT_DEPLOYMENT=gpt-4
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

### 3. Escolha o Database

**Opção A: SQLite (Recomendado para começar)**

```env
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite+aiosqlite:///./data/teams_bots.db
```

**Opção B: Continuar com MongoDB**

```env
DATABASE_TYPE=mongodb
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=teams_bots
```

**Opção C: PostgreSQL (Produção)**

```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/teams_bots
```

### 4. Escolha o Vector Store

**Opção A: ChromaDB (Padrão, continua igual)**

```env
VECTOR_STORE=chromadb
CHROMADB_PERSIST_DIR=./data/chromadb
```

**Opção B: FAISS (Mais rápido)**

```env
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./data/faiss
```

**Opção C: Qdrant (Cloud)**

```env
VECTOR_STORE=qdrant
QDRANT_URL=https://sua-instancia.qdrant.io
QDRANT_API_KEY=sua-chave
```

### 5. Execute o Setup

```powershell
# Rode o novo setup
.\setup_v2.ps1

# Inicie os serviços
.\start-all-v2.ps1
```

## 🔄 Migração de Dados

### MongoDB → SQLite

Se você tem dados no MongoDB e quer migrar para SQLite:

```python
# Script: migrate_mongodb_to_sqlite.py

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models import Bot, Base

async def migrate():
    # Conecta MongoDB antigo
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    mongo_db = mongo_client.teams_bots_python
    
    # Conecta SQLite novo
    engine = create_async_engine("sqlite+aiosqlite:///./data/teams_bots.db")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session_maker = async_sessionmaker(engine, class_=AsyncSession)
    
    # Migra bots
    async with session_maker() as session:
        async for mongo_bot in mongo_db.bots.find():
            bot = Bot(
                id=str(mongo_bot["_id"]),
                name=mongo_bot["name"],
                description=mongo_bot.get("description", ""),
                instructions=mongo_bot["instructions"],
                enable_rag=mongo_bot.get("enable_rag", True),
                created_by=mongo_bot.get("created_by", "user@example.com"),
                created_at=mongo_bot.get("created_at"),
                is_active=mongo_bot.get("is_active", True)
            )
            session.add(bot)
        
        await session.commit()
    
    print("✅ Migração concluída!")

asyncio.run(migrate())
```

Execute:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python migrate_mongodb_to_sqlite.py
```

### ChromaDB → FAISS

O vector store pode ser recriado. Basta fazer upload dos documentos novamente na v2.

## 🆕 Novos Arquivos

Arquivos criados na v2.0:

- `shared/config.py` - ✏️ Atualizado com Azure OpenAI
- `backend/app/adapters/` - 🆕 Novos adaptadores
  - `llm_adapter.py` - Azure OpenAI / OpenAI
  - `vector_store_adapter.py` - ChromaDB / FAISS / Qdrant
- `backend/app/services/rag_service_v2.py` - 🆕 RAG otimizado
- `backend/app/database.py` - ✏️ Database dinâmico
- `backend/app/main.py` - ✏️ Atualizado
- `backend/requirements.txt` - ✏️ Novas dependências
- `README_NEW.md` - 🆕 Documentação consolidada
- `setup_v2.ps1` - 🆕 Setup automatizado
- `start-backend-v2.ps1` - 🆕 Script backend
- `start-frontend-v2.ps1` - 🆕 Script frontend
- `start-all-v2.ps1` - 🆕 Script completo

## ⚠️ Breaking Changes

### Mudanças que Quebram Compatibilidade

1. **Importações**
   - Antes: `from app.services.rag_service import rag_service`
   - Agora: `from app.services.rag_service_v2 import rag_service`

2. **Configurações**
   - Antes: `settings.openai_api_key`
   - Agora: `settings.azure_openai_api_key` (se usar Azure)

3. **Models OpenAI**
   - Antes: `settings.chat_model` (retorna "gpt-4")
   - Agora: `settings.get_chat_model()` (retorna deployment name)

4. **Database Session**
   - Antes: Síncrono
   - Agora: Async (use `await`)

## 🎯 Recomendações

### Para Desenvolvimento

```env
USE_AZURE_OPENAI=false  # Use OpenAI padrão se não tem Azure
DATABASE_TYPE=sqlite
VECTOR_STORE=chromadb
AGENTOPS_ENABLED=false
```

### Para Produção Corporativa

```env
USE_AZURE_OPENAI=true  # Azure OpenAI obrigatório
DATABASE_TYPE=postgresql
VECTOR_STORE=qdrant  # Ou chromadb
AGENTOPS_ENABLED=true
```

## 📞 Suporte

Problemas na migração? Abra uma issue no GitHub com:

- Versão Python
- Sistema operacional
- Configuração (.env sanitizado)
- Mensagem de erro completa

## ✅ Validação Pós-Migração

Após migrar, valide:

```powershell
# 1. Backend iniciou
curl http://localhost:8000/health

# 2. Sistema info
curl http://localhost:8000/system/info

# 3. Crie um bot de teste
curl -X POST http://localhost:8000/api/bots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bot Teste",
    "description": "Teste migração",
    "instructions": "Você é um assistente",
    "enable_rag": true
  }'

# 4. Liste bots
curl http://localhost:8000/api/bots
```

Se todos funcionarem, migração OK! ✅

---

**Dúvidas?** Consulte `README_NEW.md` completo.
