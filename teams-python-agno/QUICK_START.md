# 🚀 Guia Rápido - 5 Minutos

## Setup Inicial (2 minutos)

### 1. Configure as credenciais

Edite o arquivo `.env`:

```env
# OpenAI (obtenha em: https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-seu-key-aqui

# AgentOps (obtenha em: https://agentops.ai)
AGENTOPS_API_KEY=seu-key-aqui
```

### 2. Execute o setup

```powershell
.\setup.ps1
```

### 3. Inicie a aplicação

```powershell
# Opção 1: Tudo junto
.\start-all.ps1

# Opção 2: Separado (2 terminais)
.\start-backend.ps1   # Terminal 1
.\start-frontend.ps1  # Terminal 2
```

---

## Usando a Aplicação (3 minutos)

### 1. Acesse o Frontend

Abra: **http://localhost:8501**

### 2. Crie seu primeiro bot

1. Clique em **"➕ Criar Bot"**
2. Preencha:
   - **Nome:** Assistente Python
   - **Descrição:** Expert em Python
   - **Instruções:** Você é um especialista em Python e FastAPI
   - **RAG:** ✅ Habilitado
3. Clique **"Criar Bot"**

### 3. Faça upload de um documento

1. Clique em **"📄 Documentos"**
2. Selecione o bot
3. Faça upload de um PDF, DOCX ou TXT
4. Aguarde o processamento (status: ✅ completed)

### 4. Converse com o bot

1. Clique em **"💬 Chat"**
2. Selecione o bot
3. Digite uma pergunta relacionada ao documento
4. Veja a resposta com as fontes!

---

## Testando a API (Opcional)

Acesse: **http://localhost:8000/docs**

### Exemplo: Criar Bot via cURL

```bash
curl -X POST http://localhost:8000/api/bots \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bot Teste",
    "description": "Bot de teste",
    "instructions": "Você é um assistente útil",
    "enable_rag": true
  }'
```

---

## Monitorando com AgentOps

1. Acesse: **https://app.agentops.ai**
2. Faça login
3. Veja as sessões de chat em tempo real!

**AgentOps rastreia automaticamente:**
- 🔍 Todas as chamadas LLM
- 💰 Custos e tokens
- ⏱️ Latência
- ❌ Erros
- 📊 Performance

---

## Estrutura Rápida

```
teams-python-agno/
├── backend/           # FastAPI + AgentOps
│   └── app/
│       ├── main.py   # Servidor
│       ├── agents/   # Agentes IA
│       ├── services/ # RAG, ChromaDB
│       └── routers/  # API routes
│
├── frontend/          # Streamlit
│   └── app.py        # Interface web
│
└── shared/           # Config compartilhada
    └── config.py
```

---

## Próximos Passos

✅ **Básico funcionando!** Agora você pode:

1. **Adicionar mais documentos** para treinar melhor
2. **Criar bots especializados** (Python, Marketing, etc)
3. **Explorar o AgentOps** dashboard
4. **Customizar prompts** para resultados melhores
5. **Integrar com Teams** (próxima etapa)

---

## Troubleshooting Rápido

### ❌ "MongoDB não conecta"

```powershell
# Inicie o MongoDB
net start MongoDB

# Ou via Docker
docker run -d -p 27017:27017 mongo
```

### ❌ "Import error no Python"

```powershell
# Reinstale dependências
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ "AgentOps não rastreia"

Verifique se a API key está correta no `.env`:
```env
AGENTOPS_API_KEY=sua-key-aqui
```

---

## 🎉 Pronto!

Você agora tem um sistema completo de:
- ✅ Bots de IA com RAG
- ✅ Upload e processamento de documentos
- ✅ Chat inteligente
- ✅ Monitoramento com AgentOps

**Tempo total:** ~5 minutos ⚡

---

## Ajuda Adicional

- 📚 **README completo:** `README.md`
- 🔧 **API Docs:** http://localhost:8000/docs
- 🤖 **AgentOps Docs:** https://docs.agentops.ai
- 💬 **Suporte:** Crie uma issue no GitHub
