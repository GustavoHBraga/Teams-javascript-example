# 🤖 Teams Bot Automation - Azure OpenAI Edition

**Plataforma corporativa de automação com bots IA treinados via RAG**

Sistema modular, dinâmico e assertivo construído para ambientes corporativos, usando Azure OpenAI, SQLite e FastAPI.

---

## 🎯 Features Principais

- ✅ **Azure OpenAI Corporativo** - Integração nativa com instância Azure
- ✅ **Database Dinâmico** - SQLite (padrão), PostgreSQL ou MongoDB
- ✅ **Vector Store Flexível** - ChromaDB, FAISS ou Qdrant
- ✅ **RAG Avançado** - Retrieval Augmented Generation otimizado
- ✅ **API REST Completa** - FastAPI com documentação automática
- ✅ **Interface Web** - Streamlit moderna e responsiva
- ✅ **AgentOps** - Monitoramento opcional de agentes IA
- ✅ **Upload Documentos** - PDF, DOCX, TXT, MD
- ✅ **Embeddings Azure** - text-embedding-ada-002 ou custom
- ✅ **Chat Inteligente** - GPT-4 com contexto documental

---

## 🏗️ Arquitetura

```
teams-python-agno/
├── backend/                    # FastAPI + Azure OpenAI
│   ├── app/
│   │   ├── main.py            # Servidor FastAPI
│   │   ├── database.py        # Database dinâmico
│   │   ├── models.py          # SQLAlchemy Models
│   │   ├── adapters/          # 🆕 Adaptadores genéricos
│   │   │   ├── llm_adapter.py         # Azure OpenAI / OpenAI
│   │   │   └── vector_store_adapter.py # ChromaDB / FAISS / Qdrant
│   │   ├── agents/            # Agentes IA
│   │   │   └── chat_agent.py  # Chat com RAG
│   │   ├── services/          # Serviços de negócio
│   │   │   └── rag_service_v2.py  # RAG otimizado
│   │   └── routers/           # API Endpoints
│   │       ├── bots.py
│   │       ├── chat.py
│   │       └── documents.py
│   └── requirements.txt
│
├── frontend/                   # Streamlit
│   ├── app.py                 # App principal
│   ├── pages/                 # Páginas da interface
│   └── requirements.txt
│
├── shared/                     # Código compartilhado
│   └── config.py              # 🆕 Configuração dinâmica
│
├── data/                       # Dados persistentes
│   ├── teams_bots.db          # SQLite database
│   ├── chromadb/              # Vector store
│   └── uploads/               # Arquivos enviados
│
├── .env.example               # Template de variáveis
└── README.md                  # Esta documentação
```

---

## 🚀 Quick Start

### Pré-requisitos

- **Python 3.11+**
- **Azure OpenAI** - Recurso criado no Azure Portal
- **Git** - Para clonar o repositório

### 1️⃣ Clone e Configure

```powershell
# Clone o repositório
cd C:\projetos
git clone <seu-repositorio>
cd teams-python-agno

# Crie arquivo .env com suas credenciais
Copy-Item .env.example .env
notepad .env
```

### 2️⃣ Configure o .env

Edite o arquivo `.env` com suas credenciais Azure:

```env
# ==================== Azure OpenAI (Corporativo) ====================
USE_AZURE_OPENAI=true

# Suas credenciais Azure (obtenha no Azure Portal)
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_KEY=sua-chave-api-aqui
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Seus deployment names (crie no Azure Portal)
AZURE_CHAT_DEPLOYMENT=gpt-4
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# ==================== Database ====================
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite+aiosqlite:///./data/teams_bots.db

# ==================== Vector Store ====================
VECTOR_STORE=chromadb
CHROMADB_PERSIST_DIR=./data/chromadb

# ==================== AgentOps (Opcional) ====================
AGENTOPS_ENABLED=false
# AGENTOPS_API_KEY=sua-chave-agentops
```

### 3️⃣ Backend

```powershell
# Entre na pasta backend
cd backend

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt

# Rode o servidor
python -m app.main
```

✅ **Backend rodando em:** http://localhost:8000  
📚 **Documentação API:** http://localhost:8000/docs

### 4️⃣ Frontend

```powershell
# Abra outro terminal e entre na pasta frontend
cd frontend

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt

# Rode o Streamlit
streamlit run app.py
```

✅ **Frontend rodando em:** http://localhost:8501

---

## 🔧 Configuração Azure OpenAI

### Como Obter Credenciais Azure

1. **Acesse o Azure Portal**: https://portal.azure.com
2. **Crie um recurso Azure OpenAI**:
   - Busque por "Azure OpenAI"
   - Clique em "Create"
   - Selecione sua subscription e resource group
   - Escolha uma região (East US, West Europe, etc.)
3. **Obtenha o Endpoint e API Key**:
   - Vá em "Keys and Endpoint"
   - Copie "KEY 1" ou "KEY 2"
   - Copie o "Endpoint"
4. **Crie Deployments**:
   - Vá em "Model deployments" → "Manage Deployments"
   - No Azure OpenAI Studio, crie:
     - **Chat**: GPT-4 ou GPT-3.5-turbo
     - **Embeddings**: text-embedding-ada-002
   - Anote os nomes dos deployments

### Exemplo de Configuração

```env
AZURE_OPENAI_ENDPOINT=https://minhaempresa-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=1a2b3c4d5e6f7g8h9i0j...
AZURE_CHAT_DEPLOYMENT=gpt-4-deployment
AZURE_EMBEDDING_DEPLOYMENT=embedding-deployment
```

---

## 📦 Stack Tecnológica

### Backend
- **FastAPI** 0.109.0 - Framework web moderno e rápido
- **SQLAlchemy** 2.0.25 - ORM para SQL databases
- **Azure OpenAI SDK** - Cliente oficial Microsoft
- **AgentOps** 0.2.6 - Observabilidade (opcional)

### Database (Dinâmico)
- **SQLite** (padrão) - Leve, sem instalação
- **PostgreSQL** (opcional) - Robusto e escalável
- **MongoDB** (opcional) - NoSQL flexível

### Vector Store (Dinâmico)
- **ChromaDB** 0.4.22 (padrão) - Fácil e eficiente
- **FAISS** 1.7.4 (opcional) - Rápido, local
- **Qdrant** 1.7.3 (opcional) - Cloud, escalável

### Document Processing
- **pypdf** - Extração de PDFs
- **python-docx** - Documentos Word
- **tiktoken** - Tokenização OpenAI

### Frontend
- **Streamlit** - Interface web em Python
- **Plotly** - Visualizações interativas

---

## 🎨 Interface Streamlit

### Páginas Disponíveis

- **🏠 Home** - Dashboard com estatísticas
- **🤖 Galeria de Bots** - Visualiza e gerencia bots
- **🎨 Criar Bot** - Formulário de criação
- **💬 Chat** - Interface de conversa com RAG
- **📄 Upload Documentos** - Gestão de arquivos

### Features da UI

- ✅ Upload com drag & drop
- ✅ Chat em tempo real
- ✅ Visualização de fontes (RAG)
- ✅ Estatísticas e métricas
- ✅ Tema customizável

---

## 🔍 Como Funciona o RAG

### Fluxo Completo

1. **Upload de Documento**
   - Usuário faz upload (PDF, DOCX, TXT, MD)
   - Sistema extrai texto
   - Divide em chunks (default: 1000 caracteres, overlap: 200)

2. **Geração de Embeddings**
   - Cada chunk vira um vetor (Azure OpenAI)
   - Armazenado no vector store (ChromaDB/FAISS/Qdrant)
   - Indexado por bot_id

3. **Chat com RAG**
   - Usuário faz pergunta
   - Sistema busca chunks similares (top 5)
   - Filtra por threshold de similaridade (0.7)
   - Injeta contexto no prompt
   - Azure OpenAI responde baseado nos documentos

### Diagrama

```
Documento → Chunks → Embeddings → Vector Store
                                       ↓
Pergunta → Embedding → Busca → Contexto → LLM → Resposta
```

---

## 📖 Documentação da API

### URL Base
```
http://localhost:8000
```

### Principais Endpoints

#### 🤖 Bots

```http
# Criar bot
POST /api/bots
Content-Type: application/json

{
  "name": "Assistente RH",
  "description": "Bot especializado em RH",
  "instructions": "Você é um assistente especializado em Recursos Humanos...",
  "enable_rag": true
}

# Listar bots
GET /api/bots

# Detalhes do bot
GET /api/bots/{bot_id}

# Atualizar bot
PUT /api/bots/{bot_id}

# Deletar bot
DELETE /api/bots/{bot_id}
```

#### 📄 Documentos

```http
# Upload documento
POST /api/documents
Content-Type: multipart/form-data

file: <arquivo>
bot_id: <id_do_bot>

# Listar documentos
GET /api/documents?bot_id={bot_id}

# Deletar documento
DELETE /api/documents/{document_id}
```

#### 💬 Chat

```http
# Enviar mensagem
POST /api/chat
Content-Type: application/json

{
  "bot_id": "abc-123",
  "message": "Quais são os benefícios?",
  "enable_rag": true
}

# Resposta
{
  "response": "Os benefícios incluem...",
  "sources": ["manual-rh.pdf", "politica-beneficios.docx"],
  "context_used": true,
  "model": "gpt-4",
  "tokens_used": 450
}
```

---

## 🧪 Exemplos de Uso

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Criar bot
response = requests.post(f"{BASE_URL}/api/bots", json={
    "name": "Assistente Técnico",
    "description": "Expert em Python e Azure",
    "instructions": "Você é um especialista técnico em Python e Azure OpenAI...",
    "enable_rag": True
})
bot = response.json()
print(f"Bot criado: {bot['id']}")

# 2. Upload documento
files = {'file': open('manual_tecnico.pdf', 'rb')}
data = {'bot_id': bot['id']}

response = requests.post(
    f"{BASE_URL}/api/documents",
    files=files,
    data=data
)
doc = response.json()
print(f"Documento enviado: {doc['id']}")

# 3. Chat com RAG
response = requests.post(f"{BASE_URL}/api/chat", json={
    "bot_id": bot['id'],
    "message": "Como fazer deploy no Azure?",
    "enable_rag": True
})

result = response.json()
print(f"Resposta: {result['response']}")
print(f"Fontes: {result['sources']}")
print(f"Tokens: {result['tokens_used']}")
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Criar bot
curl -X POST http://localhost:8000/api/bots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bot Teste",
    "description": "Bot de testes",
    "instructions": "Você é um assistente útil",
    "enable_rag": true
  }'

# Upload documento
curl -X POST http://localhost:8000/api/documents \
  -F "file=@documento.pdf" \
  -F "bot_id=abc-123"

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "abc-123",
    "message": "Olá, como você pode me ajudar?",
    "enable_rag": true
  }'
```

---

## ⚙️ Configurações Avançadas

### Trocar para PostgreSQL

```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/teams_bots
```

Instale o driver:
```powershell
pip install asyncpg
```

### Trocar para FAISS (mais rápido)

```env
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./data/faiss
```

Instale FAISS:
```powershell
pip install faiss-cpu  # Ou faiss-gpu para GPU
```

### Usar Qdrant (cloud)

```env
VECTOR_STORE=qdrant
QDRANT_URL=https://sua-instancia.qdrant.io
QDRANT_API_KEY=sua-chave-api
```

Instale Qdrant:
```powershell
pip install qdrant-client
```

### Ajustar Parâmetros RAG

```env
CHUNK_SIZE=1500               # Tamanho dos chunks
CHUNK_OVERLAP=300             # Overlap entre chunks
MAX_CHUNKS_PER_QUERY=7        # Máximo de chunks retornados
SIMILARITY_THRESHOLD=0.75     # Threshold de similaridade (0-1)
```

### Ativar AgentOps

```env
AGENTOPS_ENABLED=true
AGENTOPS_API_KEY=sua-chave-agentops
```

Obtenha chave em: https://agentops.ai

---

## 🐛 Troubleshooting

### Erro: "Import errors" ao rodar

**Solução**: Certifique-se de ativar o ambiente virtual

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Se erro de execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Azure OpenAI authentication failed"

**Solução**: Verifique suas credenciais

```powershell
# Teste suas credenciais
python -c "
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key='SUA_CHAVE',
    api_version='2024-02-15-preview',
    azure_endpoint='SEU_ENDPOINT'
)
print('Conexão OK!')
"
```

### Erro: "Database locked" (SQLite)

**Solução**: Feche outras conexões ou use PostgreSQL

```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql+asyncpg://localhost/teams_bots
```

### ChromaDB não inicia

**Solução**: Delete e recrie o diretório

```powershell
Remove-Item -Recurse -Force .\data\chromadb
New-Item -ItemType Directory -Path .\data\chromadb
```

---

## 📊 Monitoramento com AgentOps

### Ativar AgentOps

1. Crie conta em: https://agentops.ai
2. Obtenha API key no dashboard
3. Configure no `.env`:

```env
AGENTOPS_ENABLED=true
AGENTOPS_API_KEY=sua-chave-agentops
```

### O que é Rastreado

- ✅ **Chamadas LLM** - Todas interações com Azure OpenAI
- ✅ **Tokens** - Uso e custos estimados
- ✅ **Latência** - Tempo de resposta
- ✅ **Erros** - Exceções e falhas
- ✅ **Sessões** - Conversas completas
- ✅ **RAG** - Buscas no vector store

### Dashboard

Acesse: https://app.agentops.ai

---

## 🚀 Deploy em Produção

### Azure App Service

```bash
# Login Azure
az login

# Deploy backend
az webapp up \
  --name teams-bot-api \
  --resource-group seu-rg \
  --runtime "PYTHON:3.11" \
  --sku B1

# Configure variáveis de ambiente
az webapp config appsettings set \
  --name teams-bot-api \
  --resource-group seu-rg \
  --settings \
    USE_AZURE_OPENAI=true \
    AZURE_OPENAI_ENDPOINT="..." \
    AZURE_OPENAI_API_KEY="..."
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY shared/ ../shared/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```powershell
# Build
docker build -t teams-bot-api .

# Run
docker run -d -p 8000:8000 --env-file .env teams-bot-api
```

---

## 📈 Performance

### Benchmarks (Média)

- **RAG Query**: ~500ms (com 10k chunks)
- **Upload PDF**: ~2s (documento de 10 páginas)
- **Chat sem RAG**: ~1s
- **Chat com RAG**: ~1.5s
- **Embeddings**: ~100ms (batch de 10)

### Otimizações Implementadas

- ✅ Batch embeddings (até 16 por vez no Azure)
- ✅ Async I/O completo (FastAPI + aiosqlite)
- ✅ Connection pooling
- ✅ Lazy loading de adaptadores
- ✅ Caching de configurações

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

MIT License - Use livremente em projetos corporativos

---

## 🙋 Suporte

- **Issues**: Abra uma issue no GitHub
- **Docs Azure**: https://learn.microsoft.com/azure/ai-services/openai/
- **Docs FastAPI**: https://fastapi.tiangolo.com/
- **Docs AgentOps**: https://docs.agentops.ai

---

## 📝 Changelog

### v2.0.0 (Refatoração Azure)
- ✅ Integração nativa com Azure OpenAI
- ✅ Arquitetura modular com adapters
- ✅ Database dinâmico (SQLite/PostgreSQL/MongoDB)
- ✅ Vector store flexível (ChromaDB/FAISS/Qdrant)
- ✅ RAG otimizado sem dependências pesadas
- ✅ AgentOps opcional
- ✅ Documentação consolidada

### v1.0.0 (Versão Original)
- OpenAI padrão
- MongoDB fixo
- ChromaDB fixo
- LangChain dependencies

---

**Desenvolvido com ❤️ para ambientes corporativos**

*Versão 2.0.0 - Azure OpenAI Edition*
