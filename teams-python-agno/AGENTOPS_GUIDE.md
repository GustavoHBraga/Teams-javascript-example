# 📊 AgentOps - Observabilidade Completa

## O que é AgentOps?

**AgentOps** é uma plataforma de observabilidade para agentes de IA que rastreia automaticamente:

- 🔍 **LLM Calls** - Todas chamadas à OpenAI/Anthropic/etc
- 💰 **Custos** - Tokens e gastos em tempo real
- ⏱️ **Performance** - Latência e throughput
- ❌ **Errors** - Falhas e exceções
- 🔗 **Traces** - Fluxo completo de execução
- 📊 **Analytics** - Insights e tendências

---

## Por que usar AgentOps?

### Sem AgentOps ❌
```python
# Você não sabe:
# - Quantos tokens usou
# - Quanto custou
# - Onde deu erro
# - Performance real
```

### Com AgentOps ✅
```python
import agentops

agentops.init(api_key="your-key")

# AgentOps rastreia TUDO automaticamente!
# - Tokens: 1,234
# - Custo: $0.05
# - Latência: 1.2s
# - Status: Success
```

---

## Como Funciona

### 1. Inicialização

```python
# app/main.py
import agentops

agentops.init(
    api_key=settings.agentops_api_key,
    default_tags=["production", "teams-bot"]
)
```

### 2. Decoradores (Opcional)

```python
from agentops import record_action

class ChatAgent:
    @record_action("chat_with_rag")
    async def chat_with_rag(self, bot_id, message):
        # AgentOps rastreia esta função
        response = await openai.chat.completions.create(...)
        return response
```

### 3. Rastreamento Automático

AgentOps detecta automaticamente:

```python
# ✅ OpenAI
client = AsyncOpenAI(api_key=...)
response = await client.chat.completions.create(...)
# → AgentOps rastreia: modelo, tokens, custo, latência

# ✅ LangChain
chain = LLMChain(llm=ChatOpenAI())
result = chain.run("pergunta")
# → AgentOps rastreia: toda a chain

# ✅ Embeddings
embeddings = OpenAIEmbeddings()
vectors = embeddings.embed_documents(texts)
# → AgentOps rastreia: quantidade, custo
```

---

## Dashboard AgentOps

Acesse: **https://app.agentops.ai**

### O que você vê:

#### 1. **Sessions** (Sessões de Chat)
```
📊 Session: abc123
   ├─ Mensagem 1: "Como fazer deploy?"
   │  ├─ RAG Search: 3 docs (120ms)
   │  ├─ LLM Call: GPT-4 (1,234 tokens, $0.05, 1.2s)
   │  └─ Response: "Para fazer deploy..."
   │
   └─ Mensagem 2: "E no Azure?"
      ├─ RAG Search: 2 docs (98ms)
      ├─ LLM Call: GPT-4 (890 tokens, $0.03, 0.9s)
      └─ Response: "No Azure você deve..."
```

#### 2. **Metrics** (Métricas Agregadas)
```
📈 Hoje:
   - Total Sessions: 45
   - Total Tokens: 123,456
   - Total Cost: $6.78
   - Avg Latency: 1.3s
   - Success Rate: 98.2%
```

#### 3. **Traces** (Traces Detalhados)
```
🔍 Trace: chat_with_rag
   ├─ 00:00.000 → Início
   ├─ 00:00.120 → RAG Search (ChromaDB)
   ├─ 00:00.250 → Generate Embeddings (OpenAI)
   ├─ 00:00.450 → Build Prompt
   ├─ 00:01.650 → LLM Call (GPT-4)
   └─ 00:01.800 → Fim (Total: 1.8s)
```

#### 4. **Errors** (Erros e Exceções)
```
❌ Errors (últimas 24h):
   - Rate Limit: 2x
   - Timeout: 1x
   - Invalid API Key: 0x
```

---

## Integração no Projeto

### Backend (FastAPI)

```python
# app/main.py
import agentops

# Inicializa na startup
agentops.init(api_key=settings.agentops_api_key)

app = FastAPI()

# AgentOps rastreia automaticamente todos os endpoints!
```

### Agentes (Chat)

```python
# app/agents/chat_agent.py
import agentops

class ChatAgent:
    @agentops.record_action("chat_with_rag")
    async def chat_with_rag(self, bot_id, message):
        # 1. RAG Search (rastreado)
        docs = await rag_service.search(message)
        
        # 2. LLM Call (rastreado)
        response = await openai.chat.completions.create(...)
        
        # 3. Response (rastreado)
        return response
```

### Sessões de Chat

```python
# app/routers/chat.py
import agentops

@router.post("/chat")
async def chat(message: ChatMessage):
    # AgentOps cria sessão automaticamente
    session_id = agentops.start_session(
        tags=["chat", f"bot_{message.bot_id}"]
    )
    
    try:
        response = await chat_agent.chat_with_rag(...)
        agentops.end_session(session_id, "Success")
        return response
    except Exception as e:
        agentops.end_session(session_id, "Error")
        raise
```

---

## Exemplos de Uso

### 1. Rastrear Custo por Bot

```python
# No dashboard, filtre por tag: bot_abc123
# Veja: tokens, custo, sessões

# Resultado:
# Bot "Assistente Python":
#   - 234 sessões
#   - 45,678 tokens
#   - $2.34 total
#   - $0.01 por sessão
```

### 2. Identificar Gargalos

```python
# No trace, veja onde demora mais:

Trace: chat_with_rag (3.5s total)
  ├─ RAG Search: 0.1s (3%)
  ├─ Embeddings: 0.2s (6%)
  ├─ LLM Call: 3.0s (86%) ← GARGALO!
  └─ Parse: 0.2s (6%)

# Solução: Cache LLM responses
```

### 3. Monitorar Qualidade

```python
# Analytics > Quality Metrics

Últimos 7 dias:
  - Avg Response Time: 1.5s
  - Success Rate: 98%
  - User Satisfaction: 4.5/5
  
Trends:
  📈 Response time: -15% (melhorou!)
  📉 Cost per query: -20% (otimizado!)
```

---

## APIs AgentOps

### Session API

```python
import agentops

# Criar sessão
session = agentops.start_session(
    tags=["production", "bot_123"],
    metadata={"user_id": "abc", "bot_name": "Assistente"}
)

# Adicionar evento
agentops.record_event(
    session_id=session.id,
    event_type="rag_search",
    properties={"docs_found": 5, "latency": 0.12}
)

# Finalizar sessão
agentops.end_session(session.id, "Success")
```

### Metrics API

```python
# Enviar métrica customizada
agentops.record_metric(
    name="document_upload",
    value=1,
    tags={"bot_id": "123", "file_type": "pdf"}
)
```

### Feedback API

```python
# Registrar feedback do usuário
agentops.record_feedback(
    session_id=session.id,
    rating=5,
    comment="Ótima resposta!"
)
```

---

## Alertas e Notificações

Configure alertas no dashboard:

### 1. Custo Elevado
```
⚠️ Alerta: Custo > $10/dia
   → Enviar email para admin@empresa.com
```

### 2. Latência Alta
```
⚠️ Alerta: Latência > 5s
   → Notificar Slack #alerts
```

### 3. Taxa de Erro
```
⚠️ Alerta: Error rate > 5%
   → Criar ticket no Jira
```

---

## Comparação com Alternativas

| Feature | AgentOps | LangSmith | Helicone | Logs Manuais |
|---------|----------|-----------|----------|--------------|
| **Auto-tracking** | ✅ Sim | ✅ Sim | ✅ Sim | ❌ Não |
| **OpenAI** | ✅ | ✅ | ✅ | ⚠️ Parcial |
| **LangChain** | ✅ | ✅ | ❌ | ❌ |
| **Custo/Tokens** | ✅ | ✅ | ✅ | ❌ |
| **Traces** | ✅ | ✅ | ⚠️ | ❌ |
| **Dashboard** | ✅ Excelente | ✅ Bom | ✅ Básico | ❌ |
| **Preço** | Free tier | Pago | Free tier | Grátis |
| **Setup** | 2 linhas | 5 linhas | 3 linhas | 50+ linhas |

---

## Custos AgentOps

### Free Tier
- ✅ 10,000 events/mês
- ✅ 30 dias de retenção
- ✅ Dashboard completo
- ✅ 1 projeto

### Pro ($49/mês)
- ✅ 100,000 events/mês
- ✅ 90 dias de retenção
- ✅ Alertas customizados
- ✅ 5 projetos
- ✅ Suporte prioritário

### Enterprise (Custom)
- ✅ Events ilimitados
- ✅ Retenção customizada
- ✅ On-premise option
- ✅ SLA 99.9%

---

## Best Practices

### 1. Use Tags Consistentes
```python
agentops.init(
    api_key=key,
    default_tags=[
        "env:production",
        "app:teams-bot",
        "version:1.0.0"
    ]
)
```

### 2. Adicione Contexto
```python
@record_action("chat")
async def chat(bot_id, message):
    # Adiciona contexto útil
    agentops.set_context({
        "bot_id": bot_id,
        "bot_name": bot.name,
        "user_id": user.id,
        "message_length": len(message)
    })
```

### 3. Trate Erros Apropriadamente
```python
try:
    response = await chat_agent.chat(...)
    agentops.record_success()
except Exception as e:
    agentops.record_error(
        error_type=type(e).__name__,
        message=str(e),
        stack_trace=traceback.format_exc()
    )
    raise
```

---

## Troubleshooting

### AgentOps não rastreia

```python
# Verifique se inicializou
print(agentops.is_initialized())  # Deve ser True

# Verifique a API key
print(settings.agentops_api_key[:10])  # Primeiros 10 chars
```

### Dashboard vazio

```bash
# Aguarde 30-60 segundos após a chamada
# AgentOps processa em batches

# Forçar flush (desenvolvimento)
agentops.flush()
```

### Eventos duplicados

```python
# Não inicialize múltiplas vezes
# Inicialize apenas no main.py

# ❌ Errado
agentops.init(...)  # main.py
agentops.init(...)  # router.py (DUPLICADO!)

# ✅ Correto
agentops.init(...)  # apenas main.py
```

---

## Recursos

- 📚 **Docs:** https://docs.agentops.ai
- 🎮 **Dashboard:** https://app.agentops.ai
- 💬 **Discord:** https://discord.gg/agentops
- 📧 **Suporte:** support@agentops.ai
- 🐙 **GitHub:** https://github.com/AgentOps-AI/agentops

---

## Conclusão

AgentOps transforma seu bot de uma "caixa preta" em um sistema completamente observável:

- ✅ **Visibilidade** - Veja tudo que acontece
- ✅ **Debugging** - Identifique problemas rapidamente
- ✅ **Otimização** - Reduza custos e latência
- ✅ **Qualidade** - Melhore a experiência do usuário

**Setup:** 2 linhas de código  
**Benefício:** Observabilidade completa  

🚀 **Comece agora!**
