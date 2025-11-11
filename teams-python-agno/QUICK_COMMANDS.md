# ⚡ Quick Commands - Teams Bot Automation v2.0

## 🚀 Setup Inicial (Primeira Vez)

```powershell
# 1. Configure credenciais
notepad .env

# 2. Execute setup
.\setup_v2.ps1

# 3. Inicie tudo
.\start-all-v2.ps1
```

---

## 🔄 Comandos Diários

### Iniciar Aplicação

```powershell
# Inicia backend + frontend
.\start-all-v2.ps1

# OU manualmente:
# Terminal 1 - Backend
cd backend; .\venv\Scripts\Activate.ps1; python -m app.main

# Terminal 2 - Frontend
cd frontend; .\venv\Scripts\Activate.ps1; streamlit run app.py
```

### Acessar URLs

```
📚 API Docs:    http://localhost:8000/docs
💬 API Chat:    http://localhost:8000
🎨 Interface:   http://localhost:8501
📊 Health:      http://localhost:8000/health
ℹ️  System Info: http://localhost:8000/system/info
```

---

## 🧪 Testes Rápidos

### Health Check

```powershell
curl http://localhost:8000/health
```

### System Info

```powershell
curl http://localhost:8000/system/info
```

### Criar Bot (API)

```powershell
curl -X POST http://localhost:8000/api/bots `
  -H "Content-Type: application/json" `
  -d '{
    "name": "Bot Teste",
    "description": "Assistente de testes",
    "instructions": "Você é um assistente prestativo",
    "enable_rag": true
  }'
```

### Listar Bots

```powershell
curl http://localhost:8000/api/bots
```

### Chat Simples

```powershell
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{
    "bot_id": "SEU_BOT_ID",
    "message": "Olá, como você pode me ajudar?",
    "enable_rag": true
  }'
```

---

## 🔧 Manutenção

### Atualizar Dependências

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Limpar Cache

```powershell
# Limpar __pycache__
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Limpar vector store
Remove-Item -Recurse -Force .\data\chromadb
New-Item -ItemType Directory -Path .\data\chromadb
```

### Recriar Database

```powershell
# SQLite
Remove-Item .\data\teams_bots.db
# Reinicie o backend - será recriado automaticamente
```

### Ver Logs

```powershell
# Backend logs (console)
cd backend
.\venv\Scripts\Activate.ps1
python -m app.main

# Logs em arquivo (se configurado)
Get-Content .\logs\app.log -Tail 50 -Wait
```

---

## 📦 Instalação de Dependências Opcionais

### PostgreSQL Driver

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install asyncpg
```

### FAISS (Vector Store)

```powershell
pip install faiss-cpu  # CPU only
# OU
pip install faiss-gpu  # Com GPU
```

### Qdrant (Vector Store)

```powershell
pip install qdrant-client
```

### AgentOps

```powershell
pip install agentops
```

---

## 🔍 Debugging

### Teste Azure OpenAI

```powershell
cd backend
.\venv\Scripts\Activate.ps1

python -c "
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key='SUA_CHAVE',
    api_version='2024-02-15-preview',
    azure_endpoint='SEU_ENDPOINT'
)
response = client.chat.completions.create(
    model='SEU_DEPLOYMENT',
    messages=[{'role': 'user', 'content': 'Teste'}]
)
print(response.choices[0].message.content)
"
```

### Teste Database

```powershell
python -c "
from app.database import connect_db, test_connection, get_database_info
import asyncio

async def test():
    await connect_db()
    print('Database conectado')
    ok = await test_connection()
    print(f'Teste: {\"OK\" if ok else \"FALHA\"}')
    info = get_database_info()
    print(f'Tipo: {info[\"type\"]}')

asyncio.run(test())
"
```

### Teste Vector Store

```powershell
python -c "
from app.adapters.vector_store_adapter import get_vector_store_adapter
from shared.config import settings

adapter = get_vector_store_adapter(settings)
print(f'Vector Store: {settings.vector_store}')
print('Adapter criado com sucesso!')
"
```

---

## 🐳 Docker (Opcional)

### Build

```powershell
docker build -t teams-bot-api -f backend/Dockerfile .
```

### Run

```powershell
docker run -d `
  -p 8000:8000 `
  --env-file .env `
  --name teams-bot-api `
  teams-bot-api
```

### Logs

```powershell
docker logs -f teams-bot-api
```

### Stop

```powershell
docker stop teams-bot-api
docker rm teams-bot-api
```

---

## 📊 Monitoramento

### AgentOps Dashboard

```
https://app.agentops.ai
```

### Métricas do Sistema

```powershell
curl http://localhost:8000/system/info | jq
```

### Database Stats

```powershell
# SQLite
sqlite3 .\data\teams_bots.db "SELECT COUNT(*) FROM bots;"
sqlite3 .\data\teams_bots.db "SELECT COUNT(*) FROM documents;"
```

---

## 🔐 Segurança

### Regenerar .env

```powershell
# Backup atual
Copy-Item .env .env.backup

# Criar novo
Copy-Item .env.example .env
notepad .env
```

### Variáveis Críticas

```env
AZURE_OPENAI_API_KEY=***  # NUNCA commitar!
AGENTOPS_API_KEY=***      # NUNCA commitar!
```

### .gitignore Essencial

```gitignore
.env
*.db
*.log
__pycache__/
venv/
data/
```

---

## 📱 Atalhos Úteis

### PowerShell Aliases (Opcional)

Adicione ao seu `$PROFILE`:

```powershell
# Abrir profile
notepad $PROFILE

# Adicionar aliases
function Start-TeamsBot { .\start-all-v2.ps1 }
function Start-TeamsBackend { .\start-backend-v2.ps1 }
function Start-TeamsFrontend { .\start-frontend-v2.ps1 }
function Setup-TeamsBot { .\setup_v2.ps1 }

Set-Alias tbot Start-TeamsBot
Set-Alias tback Start-TeamsBackend
Set-Alias tfront Start-TeamsFrontend
Set-Alias tsetup Setup-TeamsBot
```

Uso após reiniciar terminal:

```powershell
tbot    # Inicia tudo
tback   # Inicia backend
tfront  # Inicia frontend
tsetup  # Executa setup
```

---

## 🆘 Problemas Comuns

### Erro: "Cannot activate virtual environment"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Module not found"

```powershell
cd backend  # ou frontend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Erro: "Port 8000 already in use"

```powershell
# Encontrar processo
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Matar processo
Stop-Process -Id PROCESS_ID -Force
```

### Erro: "Azure OpenAI authentication failed"

```powershell
# Verifique variáveis
Get-Content .env | Select-String "AZURE"

# Teste manualmente
python -c "import os; print(os.getenv('AZURE_OPENAI_API_KEY'))"
```

---

## 📚 Documentação

```
📖 README_NEW.md         - Guia completo
🔄 MIGRATION_GUIDE.md    - Migração v1→v2
📋 REFACTORING_SUMMARY.md - Sumário executivo
⚡ QUICK_COMMANDS.md      - Este arquivo
```

---

**💡 Dica:** Mantenha este arquivo aberto enquanto desenvolve!

**Versão:** 2.0.0  
**Atualizado:** 2025
