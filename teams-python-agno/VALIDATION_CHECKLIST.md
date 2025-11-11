# ✅ Checklist de Validação - Teams Bot Automation v2.0

Use este checklist para validar a refatoração e garantir que tudo está funcionando corretamente.

---

## 📋 Setup e Configuração

### Arquivos de Configuração

- [ ] `.env` criado com base em `.env.example`
- [ ] `AZURE_OPENAI_ENDPOINT` configurado
- [ ] `AZURE_OPENAI_API_KEY` configurado
- [ ] `AZURE_CHAT_DEPLOYMENT` configurado
- [ ] `AZURE_EMBEDDING_DEPLOYMENT` configurado
- [ ] `DATABASE_TYPE` definido (sqlite/postgresql/mongodb)
- [ ] `VECTOR_STORE` definido (chromadb/faiss/qdrant)

### Diretórios

- [ ] `data/` existe
- [ ] `data/chromadb/` existe (se usar ChromaDB)
- [ ] `data/uploads/` existe
- [ ] `logs/` existe

### Ambientes Virtuais

- [ ] `backend/venv/` criado
- [ ] `frontend/venv/` criado
- [ ] Dependências backend instaladas (`pip list`)
- [ ] Dependências frontend instaladas (`pip list`)

---

## 🔧 Backend

### Inicialização

- [ ] Backend inicia sem erros
- [ ] Mensagem "✅ SQLite conectado" aparece
- [ ] Mensagem "✅ Azure OpenAI Adapter inicializado" aparece
- [ ] Mensagem "✅ RAG Service inicializado" aparece
- [ ] Servidor roda em `http://localhost:8000`

### Endpoints Básicos

- [ ] `GET /` retorna JSON com info da API
- [ ] `GET /health` retorna status "healthy"
- [ ] `GET /system/info` retorna config do sistema
- [ ] `GET /docs` abre Swagger UI
- [ ] `GET /redoc` abre ReDoc

### Database

- [ ] Arquivo `data/teams_bots.db` criado (SQLite)
- [ ] Tabelas criadas (bots, documents, conversations, messages)
- [ ] Conexão database OK (teste via `/system/info`)

### Adapters

- [ ] LLM Adapter inicializado (Azure OU OpenAI)
- [ ] Vector Store Adapter inicializado
- [ ] Sem erros de import nos adapters

---

## 🎨 Frontend

### Inicialização

- [ ] Frontend inicia sem erros
- [ ] Streamlit abre em `http://localhost:8501`
- [ ] Interface carrega corretamente

### Páginas

- [ ] Página Home funciona
- [ ] Página Galeria de Bots funciona
- [ ] Página Criar Bot funciona
- [ ] Página Chat funciona
- [ ] Página Upload Documentos funciona

### Conectividade

- [ ] Frontend se conecta ao backend
- [ ] Requisições API funcionam
- [ ] Erros de API são exibidos corretamente

---

## 🤖 Funcionalidades Core

### Bots

- [ ] **Criar bot via API**
  ```powershell
  curl -X POST http://localhost:8000/api/bots `
    -H "Content-Type: application/json" `
    -d '{"name":"Teste","description":"Bot teste","instructions":"Você é um assistente","enable_rag":true}'
  ```
- [ ] **Listar bots** (`GET /api/bots`)
- [ ] **Obter bot por ID** (`GET /api/bots/{id}`)
- [ ] **Atualizar bot** (`PUT /api/bots/{id}`)
- [ ] **Deletar bot** (`DELETE /api/bots/{id}`)

### Documentos

- [ ] **Upload documento via API**
  ```powershell
  curl -X POST http://localhost:8000/api/documents `
    -F "file=@test.pdf" `
    -F "bot_id=BOT_ID"
  ```
- [ ] Documento processado com sucesso
- [ ] Chunks criados corretamente
- [ ] Embeddings gerados (Azure OpenAI)
- [ ] Armazenados no vector store
- [ ] **Listar documentos** (`GET /api/documents`)
- [ ] **Deletar documento** (`DELETE /api/documents/{id}`)

### Chat

- [ ] **Chat simples (sem RAG)**
  ```powershell
  curl -X POST http://localhost:8000/api/chat `
    -H "Content-Type: application/json" `
    -d '{"bot_id":"BOT_ID","message":"Olá!","enable_rag":false}'
  ```
- [ ] Resposta recebida do Azure OpenAI
- [ ] Tokens contabilizados
- [ ] **Chat com RAG (com documentos)**
  - [ ] Documentos relevantes encontrados
  - [ ] Contexto injetado no prompt
  - [ ] Resposta baseada nos documentos
  - [ ] Fontes retornadas corretamente
- [ ] **Chat com RAG (sem documentos relevantes)**
  - [ ] Funciona sem erros
  - [ ] Informa que não há contexto

---

## 🧪 Testes Específicos

### Azure OpenAI

- [ ] **Teste de chat**
  ```python
  from app.adapters.llm_adapter import get_llm_adapter
  from shared.config import settings
  import asyncio
  
  async def test():
      llm = get_llm_adapter(settings)
      result = await llm.chat_completion(
          messages=[{"role": "user", "content": "Olá!"}]
      )
      print(result["content"])
  
  asyncio.run(test())
  ```
- [ ] **Teste de embedding**
  ```python
  async def test():
      llm = get_llm_adapter(settings)
      embedding = await llm.generate_embedding("teste")
      print(f"Embedding size: {len(embedding)}")
  
  asyncio.run(test())
  ```

### Vector Store

- [ ] **Adicionar documento teste**
  ```python
  from app.adapters.vector_store_adapter import get_vector_store_adapter
  from shared.config import settings
  import asyncio
  
  async def test():
      vs = get_vector_store_adapter(settings)
      count = await vs.add_documents(
          collection_name="test_collection",
          documents=["Documento teste"],
          embeddings=[[0.1]*1536],  # Mock embedding
          metadatas=[{"source": "test"}]
      )
      print(f"Adicionados: {count}")
  
  asyncio.run(test())
  ```
- [ ] **Buscar documento teste**
  ```python
  async def test():
      vs = get_vector_store_adapter(settings)
      results = await vs.search_similar(
          collection_name="test_collection",
          query_embedding=[0.1]*1536,
          n_results=1
      )
      print(results)
  
  asyncio.run(test())
  ```

### RAG End-to-End

- [ ] Upload PDF real
- [ ] Processamento completo
- [ ] Busca por query relevante
- [ ] Chat com contexto do PDF
- [ ] Resposta coerente com documento

---

## 🔍 Validação de Qualidade

### Código

- [ ] Sem erros de lint críticos
- [ ] Imports funcionando
- [ ] Type hints corretos (maioria)
- [ ] Docstrings presentes

### Performance

- [ ] Upload de PDF (10 páginas) < 5s
- [ ] Chat simples < 2s
- [ ] Chat com RAG < 3s
- [ ] Embeddings batch (10 chunks) < 1s

### Logs

- [ ] Logs informativos no console
- [ ] Sem warnings críticos
- [ ] Erros tratados graciosamente

---

## 📚 Documentação

### Arquivos Criados

- [ ] `README_NEW.md` existe e está completo
- [ ] `MIGRATION_GUIDE.md` existe
- [ ] `REFACTORING_SUMMARY.md` existe
- [ ] `QUICK_COMMANDS.md` existe
- [ ] Este arquivo (`VALIDATION_CHECKLIST.md`) existe

### Scripts PowerShell

- [ ] `setup_v2.ps1` funciona
- [ ] `start-backend-v2.ps1` funciona
- [ ] `start-frontend-v2.ps1` funciona
- [ ] `start-all-v2.ps1` funciona

---

## 🚀 Pronto para Produção?

### Segurança

- [ ] `.env` não está no git
- [ ] Credenciais não expostas no código
- [ ] CORS configurado adequadamente
- [ ] Validação de inputs implementada

### Escalabilidade

- [ ] Database pode ser trocado facilmente
- [ ] Vector store pode ser trocado facilmente
- [ ] LLM provider pode ser trocado facilmente

### Monitoramento

- [ ] Logs estruturados
- [ ] Health check endpoint
- [ ] System info endpoint
- [ ] AgentOps opcional configurado

### Backup

- [ ] Estratégia de backup definida
- [ ] Dados críticos identificados
- [ ] Procedimento de restore documentado

---

## ✅ Validação Final

### Checklist Mínimo (MVP)

- [ ] Backend inicia sem erros
- [ ] Frontend inicia sem erros
- [ ] Azure OpenAI conectado
- [ ] Criar bot funciona
- [ ] Upload documento funciona
- [ ] Chat com RAG funciona
- [ ] Documentação acessível

### Checklist Completo (Produção)

- [ ] Todos os itens do checklist mínimo ✅
- [ ] Testes específicos passam ✅
- [ ] Performance aceitável ✅
- [ ] Logs claros e úteis ✅
- [ ] Documentação completa ✅
- [ ] Scripts de deploy prontos ✅

---

## 📊 Resultado

**Status Geral:**

- Total de itens: ~100+
- Concluídos: _____ / _____
- Taxa de sucesso: _____%

**Aprovado para:**

- [ ] ✅ Desenvolvimento
- [ ] ✅ Testes
- [ ] ✅ Homologação
- [ ] ✅ Produção

---

## 📝 Notas

Use este espaço para anotar observações durante a validação:

```
Data da validação: _____________________
Validado por: _________________________

Observações:
- 
- 
- 

Problemas encontrados:
- 
- 
- 

Ações necessárias:
- 
- 
- 
```

---

**Versão do Checklist:** 1.0  
**Compatível com:** Teams Bot Automation v2.0 Azure Edition
