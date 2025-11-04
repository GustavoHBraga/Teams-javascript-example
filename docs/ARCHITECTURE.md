# 🏗️ Arquitetura do Sistema

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                      Microsoft Teams                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Tab (React)  │  │  Bot Framework │  │  Message Ext.  │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
└───────────┼──────────────────┼──────────────────┼─────────────┘
            │                   │                   │
            │                   │                   │
            ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Frontend     │  │   Bot Service  │  │   API Gateway  │   │
│  │  (React App)   │  │  (Bot Framework)│  │   (Express)    │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
│           │                   │                   │              │
│           └───────────────────┴───────────────────┘              │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  Bot Service   │  │   AI Service   │  │   RAG Service  │   │
│  │   (CRUD ops)   │  │   (OpenAI)     │  │  (Vector DB)   │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
│           │                   │                   │              │
│           └───────────────────┴───────────────────┘              │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │    MongoDB     │  │  Azure Blob    │  │  Azure Search  │   │
│  │  (Bots, Chats) │  │  (Documents)   │  │  (Vector Index)│   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Frontend (@teams-bot/frontend)

**Tecnologias:**
- React 18 + TypeScript
- Fluent UI (Microsoft design system)
- React Query (estado assíncrono)
- React Router (navegação)

**Features:**
- 🎨 **Bot Gallery**: Visualização e busca de bots
- ✨ **Bot Creator**: Wizard para criar novos bots
- 💬 **Chat Interface**: Interface de conversação
- 📊 **Analytics Dashboard**: Métricas e insights

**Estrutura:**
```
frontend/
├── src/
│   ├── components/         # Componentes reutilizáveis
│   │   ├── BotCard/
│   │   ├── ChatMessage/
│   │   └── DocumentUpload/
│   ├── features/           # Features modulares
│   │   ├── bot-gallery/
│   │   ├── bot-creator/
│   │   ├── bot-chat/
│   │   └── analytics/
│   ├── hooks/              # Custom hooks
│   ├── services/           # API clients
│   └── utils/              # Utilitários
```

### 2. API Backend (@teams-bot/api)

**Tecnologias:**
- Node.js + Express
- TypeScript
- MongoDB + Mongoose
- OpenAI SDK
- LangChain (RAG)

**Responsabilidades:**
- 🔐 Autenticação e autorização
- 📝 CRUD de bots e conversas
- 🤖 Integração com OpenAI
- 📚 Processamento de documentos (RAG)
- 📊 Métricas e analytics

**Camadas:**
```
api/
├── controllers/      # Handlers de rotas
├── services/         # Lógica de negócio
│   ├── ai.service.ts
│   ├── rag.service.ts
│   └── bot.service.ts
├── database/         # Modelos e conexão
│   └── models/
├── middleware/       # Auth, validação, errors
└── routes/           # Definição de endpoints
```

### 3. Teams Bot (@teams-bot/bot)

**Tecnologias:**
- Bot Framework SDK v4
- Adaptive Cards
- Teams JS SDK

**Responsabilidades:**
- 🤝 Integração com Teams
- 💬 Processamento de mensagens
- 🎯 Commands e interações
- 📢 Notificações proativas

### 4. Shared (@teams-bot/shared)

**Conteúdo:**
- 📘 TypeScript types & interfaces
- ✅ Zod schemas (validação)
- 🔧 Constantes compartilhadas
- 🛠️ Utilitários comuns

## Fluxo de Dados

### Criação de Bot

```
Usuario (Teams Tab)
    │
    ▼
[Frontend] Valida formulário com Zod
    │
    ▼
[API] POST /api/v1/bots
    │
    ├─> [Middleware] Valida autenticação
    │
    ├─> [Controller] Processa request
    │
    ├─> [Service] Cria bot no banco
    │
    └─> [MongoDB] Persiste dados
        │
        ▼
    Retorna Bot criado
```

### Conversação com Bot (RAG)

```
Usuario envia mensagem
    │
    ▼
[Frontend/Bot] POST /api/v1/chat/messages
    │
    ▼
[Chat Controller]
    │
    ├─> [Bot Service] Busca configuração do bot
    │
    ├─> [RAG Service] Busca documentos relevantes
    │   └─> [Vector DB] Similarity search
    │       └─> Retorna top-K documentos
    │
    ├─> [AI Service] Gera resposta
    │   │
    │   ├─> Monta prompt com contexto
    │   │
    │   └─> [OpenAI API] Gera completion
    │       └─> Retorna resposta
    │
    └─> [MongoDB] Salva mensagens
        │
        ▼
    Retorna resposta ao usuário
```

## Segurança

### Autenticação

```
[Teams Client]
    │
    ├─> Azure AD B2C / Teams SSO
    │   └─> JWT Token
    │
    ▼
[API Middleware]
    │
    ├─> Valida token
    ├─> Extrai user info
    └─> Attach req.user
        │
        ▼
    Processa request
```

### Autorização

- **Personal Bots**: Apenas o criador pode editar/deletar
- **Squad Bots**: Membros da squad podem visualizar/usar
- **Organization Bots**: Todos podem visualizar/usar

### Segurança de Dados

- ✅ Helmet.js (security headers)
- ✅ CORS configurado
- ✅ Rate limiting
- ✅ Input validation (Zod)
- ✅ SQL injection protection (Mongoose)
- ✅ XSS protection

## Escalabilidade

### Horizontal Scaling

```
          Load Balancer
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
  API-1    API-2    API-3
    │         │         │
    └─────────┼─────────┘
              │
              ▼
          MongoDB
         (Replica Set)
```

### Caching Strategy

```
Request
    │
    ▼
┌─────────┐
│  Redis  │ ◄─── Cache hit? → Return
│  Cache  │
└─────────┘
    │
    │ Cache miss
    ▼
┌─────────┐
│   API   │
│ Service │
└─────────┘
    │
    ▼
Update cache
Return response
```

## Monitoramento

### Métricas Coletadas

- 📊 **Application Metrics**
  - Request rate
  - Response time
  - Error rate
  - Active users

- 🤖 **Bot Metrics**
  - Conversations per bot
  - Average tokens used
  - Success rate
  - Popular queries

- 💰 **Cost Metrics**
  - OpenAI API usage
  - Storage costs
  - Database operations

### Logging

```typescript
logger.info('Bot created', {
  botId,
  userId,
  scope,
  timestamp,
});

logger.error('AI service error', {
  error,
  botId,
  userId,
  request,
});
```

## Performance

### Otimizações

1. **Database Indexes**
   - Compound indexes para queries comuns
   - Text search index para busca

2. **API Response**
   - Pagincação default
   - Field projection
   - Lazy loading

3. **AI/RAG**
   - Embeddings cache
   - Streaming responses
   - Batch processing

## Deployment

### Desenvolvimento

```powershell
npm run dev       # Todos os serviços
npm run dev:api   # Apenas API
npm run dev:bot   # Apenas Bot
npm run dev:frontend  # Apenas Frontend
```

### Produção (Azure)

```
┌─────────────────────────────────────────┐
│        Azure App Service (API)          │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ API Node │  │ Bot Node │           │
│  └──────────┘  └──────────┘           │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Azure Services                   │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │ CosmosDB │  │   Blob   │  │Search│ │
│  └──────────┘  └──────────┘  └──────┘ │
└─────────────────────────────────────────┘
```

## Design Patterns

### Repository Pattern
```typescript
class BotRepository {
  async create(data): Promise<Bot>
  async findById(id): Promise<Bot>
  async update(id, data): Promise<Bot>
  async delete(id): Promise<void>
}
```

### Service Layer
```typescript
class BotService {
  constructor(
    private botRepo: BotRepository,
    private aiService: AIService
  ) {}
  
  async createBot(input) {
    // Business logic
    return this.botRepo.create(data);
  }
}
```

### Middleware Chain
```typescript
router.post(
  '/bots',
  authenticate,
  validateBody(schema),
  botController.create
);
```

## Testing Strategy

- **Unit Tests**: Services, utilities
- **Integration Tests**: API endpoints
- **E2E Tests**: User flows completos
- **Load Tests**: Performance e escalabilidade

---

**Última atualização:** Novembro 2025
