# 🎨 Frontend - Guia de Atualização

## 📋 Checklist de Validação do Frontend

O backend foi completamente refatorado. Este guia lista o que precisa ser verificado/atualizado no frontend.

---

## ✅ O que NÃO Muda

### Endpoints da API (Mesmos)

Os endpoints continuam os mesmos:

```python
BASE_URL = "http://localhost:8000"

# Bots
GET    /api/bots
POST   /api/bots
GET    /api/bots/{id}
PUT    /api/bots/{id}
DELETE /api/bots/{id}

# Documents
GET    /api/documents
POST   /api/documents
DELETE /api/documents/{id}

# Chat
POST   /api/chat
GET    /api/chat/history
```

**Ação:** ✅ Nenhuma mudança necessária se já está usando estes endpoints

---

## 🔍 O que Precisa Validar

### 1. Schemas de Request/Response

#### Criar Bot

**Request (mesmo):**
```json
{
  "name": "Bot Teste",
  "description": "Descrição",
  "instructions": "Instruções",
  "enable_rag": true
}
```

**Response (pode ter campos novos):**
```json
{
  "id": "abc-123",
  "name": "Bot Teste",
  "description": "Descrição",
  "instructions": "Instruções",
  "enable_rag": true,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "is_active": true,
  "created_by": "user@example.com"  // 🆕 Novo campo
}
```

**Ação:** ⚠️ Verificar se frontend lida com campos extras

#### Chat

**Request (mesmo):**
```json
{
  "bot_id": "abc-123",
  "message": "Olá",
  "enable_rag": true
}
```

**Response (campos extras):**
```json
{
  "response": "Olá! Como posso ajudar?",
  "sources": ["doc1.pdf", "doc2.docx"],
  "context_used": true,
  "model": "gpt-4",
  "tokens_used": 150,
  "usage": {                    // 🆕 Novo objeto
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

**Ação:** ⚠️ Verificar se exibe novos campos (opcional)

#### Upload Documento

**Request (mesmo):**
```
multipart/form-data
- file: <arquivo>
- bot_id: "abc-123"
```

**Response (campos extras):**
```json
{
  "id": "doc-123",
  "bot_id": "abc-123",
  "filename": "documento.pdf",
  "content_type": "application/pdf",
  "file_size": 102400,
  "status": "completed",        // pending, processing, completed, failed
  "chunk_count": 45,            // 🆕 Número de chunks criados
  "created_at": "2025-01-01T00:00:00"
}
```

**Ação:** ⚠️ Verificar se exibe `chunk_count` e `status`

---

## 🆕 Novos Endpoints (Opcional)

### Health Check

```python
GET /health

Response:
{
  "status": "healthy",
  "version": "2.0.0",
  "database": {
    "type": "sqlite",
    "status": "connected"
  },
  "vector_store": "chromadb",
  "llm_provider": "Azure OpenAI",
  "agentops": false
}
```

**Uso sugerido:** Exibir status do sistema no dashboard

### System Info

```python
GET /system/info

Response:
{
  "version": "2.0.0",
  "database": {...},
  "vector_store": {...},
  "llm": {
    "provider": "Azure OpenAI",
    "chat_model": "gpt-4",
    "embedding_model": "text-embedding-ada-002"
  },
  "rag": {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "max_chunks": 5,
    "similarity_threshold": 0.7
  }
}
```

**Uso sugerido:** Página de configurações/admin

---

## 📝 Código Frontend Sugerido

### Verificar Conexão Backend

```python
# pages/0_🏠_Home.py ou app.py

import streamlit as st
import requests

def check_backend_status():
    """Verifica se backend está online"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
        return False, None
    except:
        return False, None

# No início da página
st.set_page_config(page_title="Teams Bot", page_icon="🤖")

# Check backend
backend_ok, health_data = check_backend_status()

if not backend_ok:
    st.error("⚠️ Backend não está respondendo!")
    st.info("Certifique-se que o backend está rodando: `python -m app.main`")
    st.stop()
else:
    st.success(f"✅ Backend online (v{health_data.get('version', '?')})")
```

### Exibir Info do Sistema

```python
# pages/X_⚙️_Configurações.py

import streamlit as st
import requests

st.title("⚙️ Configurações do Sistema")

# Busca info
response = requests.get("http://localhost:8000/system/info")
if response.status_code == 200:
    info = response.json()
    
    # Database
    st.subheader("💾 Database")
    st.write(f"Tipo: {info['database']['type']}")
    st.write(f"Status: {info['database']['status']}")
    
    # Vector Store
    st.subheader("🔍 Vector Store")
    st.write(f"Tipo: {info['vector_store']['type']}")
    
    # LLM
    st.subheader("🤖 LLM Provider")
    st.write(f"Provider: {info['llm']['provider']}")
    st.write(f"Chat Model: {info['llm']['chat_model']}")
    st.write(f"Embedding Model: {info['llm']['embedding_model']}")
    
    # RAG
    st.subheader("📚 RAG Config")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Chunk Size", info['rag']['chunk_size'])
        st.metric("Max Chunks", info['rag']['max_chunks'])
    with col2:
        st.metric("Chunk Overlap", info['rag']['chunk_overlap'])
        st.metric("Similarity Threshold", f"{info['rag']['similarity_threshold']:.1%}")
```

### Melhorar Exibição de Chat

```python
# pages/3_💬_Chat.py

# Ao exibir resposta, mostrar tokens
if response:
    data = response.json()
    
    st.markdown(f"**🤖 Assistente:** {data['response']}")
    
    # Exibir fontes (se RAG)
    if data.get('context_used') and data.get('sources'):
        with st.expander("📚 Fontes consultadas"):
            for source in data['sources']:
                st.write(f"- {source}")
    
    # Exibir métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modelo", data.get('model', 'N/A'))
    with col2:
        st.metric("Tokens", data.get('tokens_used', 0))
    with col3:
        similarity = "✅" if data.get('context_used') else "❌"
        st.metric("RAG", similarity)
```

### Melhorar Upload de Documentos

```python
# pages/4_📄_Upload_Documentos.py

# Após upload
if uploaded_file:
    files = {'file': uploaded_file}
    data = {'bot_id': selected_bot_id}
    
    with st.spinner("⏳ Processando documento..."):
        response = requests.post(
            "http://localhost:8000/api/documents",
            files=files,
            data=data
        )
    
    if response.status_code == 200:
        doc_data = response.json()
        
        st.success("✅ Documento enviado com sucesso!")
        
        # Exibir detalhes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", doc_data['status'])
        with col2:
            st.metric("Chunks", doc_data.get('chunk_count', 0))
        with col3:
            size_mb = doc_data['file_size'] / (1024 * 1024)
            st.metric("Tamanho", f"{size_mb:.2f} MB")
        
        # Se ainda processando
        if doc_data['status'] == 'processing':
            st.info("⏳ Documento sendo processado em background...")
            st.button("🔄 Atualizar Status")
```

---

## 🧪 Testes Frontend

### Checklist de Validação

Execute estes testes na interface:

#### Home / Dashboard

- [ ] Página carrega sem erros
- [ ] Backend status exibido
- [ ] Estatísticas carregam (se houver)

#### Galeria de Bots

- [ ] Lista de bots carrega
- [ ] Detalhes do bot exibidos corretamente
- [ ] Deletar bot funciona
- [ ] Editar bot funciona (se implementado)

#### Criar Bot

- [ ] Formulário funciona
- [ ] Validação de campos
- [ ] Bot criado com sucesso
- [ ] Redirecionamento pós-criação

#### Chat

- [ ] Selecionar bot funciona
- [ ] Enviar mensagem funciona
- [ ] Resposta exibida corretamente
- [ ] Fontes exibidas (se RAG)
- [ ] Histórico mantido na sessão
- [ ] Métricas exibidas (tokens, modelo)

#### Upload Documentos

- [ ] Upload drag & drop funciona
- [ ] Validação de tipo de arquivo
- [ ] Progress bar (se implementado)
- [ ] Status de processamento
- [ ] Chunk count exibido
- [ ] Listar documentos funciona
- [ ] Deletar documento funciona

---

## 🐛 Possíveis Problemas

### 1. CORS

Se frontend não conecta ao backend:

```python
# Backend já configurado com CORS
# Mas se der erro, ajuste em backend/app/main.py:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Timeout

Se uploads grandes demoram:

```python
# Aumentar timeout no frontend
response = requests.post(
    url,
    files=files,
    timeout=300  # 5 minutos
)
```

### 3. Campos Faltando

Se API retorna erro de campos:

```python
# Verificar schema no backend
# Em backend/app/models.py → Pydantic schemas
# Ajustar frontend para enviar todos campos obrigatórios
```

---

## 📊 Melhorias Sugeridas

### Dashboard Completo

```python
# pages/0_🏠_Home.py

import plotly.express as px

# Buscar estatísticas
bots = requests.get("http://localhost:8000/api/bots").json()
docs = requests.get("http://localhost:8000/api/documents").json()

# Métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🤖 Bots", len(bots))
with col2:
    st.metric("📄 Documentos", len(docs))
with col3:
    active_bots = sum(1 for b in bots if b.get('is_active'))
    st.metric("✅ Ativos", active_bots)
with col4:
    total_chunks = sum(d.get('chunk_count', 0) for d in docs)
    st.metric("📚 Chunks", total_chunks)

# Gráfico de documentos por bot
if docs:
    df = pd.DataFrame(docs)
    fig = px.bar(df.groupby('bot_id').size().reset_index(), 
                 x='bot_id', y=0, title="Documentos por Bot")
    st.plotly_chart(fig)
```

### Página de Configurações

Crie `pages/9_⚙️_Configurações.py` com o código sugerido acima.

### Logs de Atividades

```python
# Se implementar logging no backend
GET /api/logs

# Frontend:
st.subheader("📋 Logs Recentes")
logs = requests.get("http://localhost:8000/api/logs").json()
for log in logs[-10:]:  # Últimos 10
    st.text(f"{log['timestamp']} - {log['message']}")
```

---

## ✅ Conclusão Frontend

### O que fazer agora:

1. **Testar todas as páginas** com novo backend
2. **Verificar schemas** de request/response
3. **Adicionar novos campos** na UI (opcional)
4. **Implementar melhorias sugeridas** (opcional)
5. **Criar página de configurações** (recomendado)

### Prioridade:

- 🔴 **Alta**: Testar funcionalidades existentes
- 🟡 **Média**: Exibir novos campos (chunk_count, usage, etc)
- 🟢 **Baixa**: Melhorias visuais e dashboard

### Status:

- ✅ Backend 100% pronto
- ⚠️ Frontend precisa validação
- 📝 Melhorias opcionais documentadas

---

**💡 Próximo passo:** Execute `start-all-v2.ps1` e teste cada página do frontend!

**Versão:** 1.0  
**Compatível com:** Backend v2.0 Azure Edition
