# 📘 API Reference

Base URL: `http://localhost:3001/api/v1`

## Authentication

Todas as rotas (exceto `/health`) requerem o header:

```
Authorization: Bearer <user-token>
```

## Endpoints

### Health Check

#### GET `/health`

Verifica se a API está funcionando.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-11-03T...",
  "service": "teams-bot-automation-api"
}
```

---

### Bots

#### POST `/bots`

Cria um novo bot.

**Request Body:**
```json
{
  "name": "Bot de Observabilidade",
  "description": "Bot especializado em métricas",
  "instructions": "Você é um especialista...",
  "scope": "squad",
  "squadId": "observability-team",
  "config": {
    "model": "gpt-4-turbo",
    "temperature": 0.7,
    "maxTokens": 2000,
    "enableRAG": true,
    "ragTopK": 5
  },
  "tags": ["observability", "monitoring"]
}
```

**Response: (201 Created)**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "name": "Bot de Observabilidade",
    "status": "active",
    "createdAt": "...",
    ...
  }
}
```

#### GET `/bots`

Lista todos os bots acessíveis pelo usuário.

**Query Parameters:**
- `page` (number): Página (padrão: 1)
- `pageSize` (number): Itens por página (padrão: 20)
- `scope` (string): Filtrar por escopo (personal/squad/organization)
- `status` (string): Filtrar por status (active/inactive/training/error)
- `search` (string): Busca por texto
- `tags` (string[]): Filtrar por tags
- `sortBy` (string): Campo de ordenação (createdAt/name/lastUsedAt)
- `sortOrder` (string): Ordem (asc/desc)

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 42,
    "page": 1,
    "pageSize": 20,
    "totalPages": 3
  }
}
```

#### GET `/bots/:botId`

Obtém detalhes de um bot específico.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "name": "Bot de Observabilidade",
    "description": "...",
    "instructions": "...",
    "scope": "squad",
    "status": "active",
    "config": {...},
    "documents": [...],
    "conversationCount": 42,
    "lastUsedAt": "..."
  }
}
```

#### PATCH `/bots/:botId`

Atualiza um bot existente.

**Request Body:** (Todos os campos são opcionais)
```json
{
  "name": "Novo Nome",
  "description": "Nova descrição",
  "config": {
    "temperature": 0.8
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": { /* bot atualizado */ }
}
```

#### DELETE `/bots/:botId`

Deleta um bot.

**Response: (204 No Content)**

---

### Chat

#### POST `/chat/messages`

Envia uma mensagem para um bot e recebe a resposta.

**Request Body:**
```json
{
  "botId": "bot-id-here",
  "content": "Como posso melhorar o monitoring?",
  "conversationId": "optional-conversation-id",
  "userId": "user-id"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": "...",
      "botId": "...",
      "userId": "...",
      "title": "Como posso melhorar..."
    },
    "userMessage": {
      "id": "...",
      "role": "user",
      "content": "Como posso melhorar o monitoring?",
      "createdAt": "..."
    },
    "assistantMessage": {
      "id": "...",
      "role": "assistant",
      "content": "Para melhorar o monitoring...",
      "metadata": {
        "sources": [...],
        "tokens": 450,
        "model": "gpt-4-turbo"
      },
      "createdAt": "..."
    }
  }
}
```

#### GET `/chat/conversations/:conversationId`

Obtém histórico completo de uma conversa.

**Response:**
```json
{
  "success": true,
  "data": {
    "conversation": {...},
    "messages": [
      {
        "id": "...",
        "role": "user",
        "content": "...",
        "createdAt": "..."
      },
      {
        "id": "...",
        "role": "assistant",
        "content": "...",
        "metadata": {...},
        "createdAt": "..."
      }
    ]
  }
}
```

#### GET `/chat/conversations`

Lista todas as conversas do usuário.

**Query Parameters:**
- `botId` (string): Filtrar por bot específico

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "botId": "...",
      "title": "...",
      "updatedAt": "..."
    }
  ]
}
```

#### DELETE `/chat/conversations/:conversationId`

Deleta (marca como inativa) uma conversa.

**Response: (204 No Content)**

---

## Error Responses

Todos os erros seguem o formato:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {...}
  },
  "metadata": {
    "timestamp": "...",
    "requestId": "..."
  }
}
```

### Common Error Codes

- `UNAUTHORIZED` (401): Missing or invalid authentication
- `FORBIDDEN` (403): No permission to access resource
- `NOT_FOUND` (404): Resource not found
- `VALIDATION_ERROR` (400): Invalid request data
- `BOT_NOT_FOUND` (404): Bot does not exist
- `AI_SERVICE_ERROR` (500): Error generating AI response
- `INTERNAL_ERROR` (500): Unexpected server error

---

## Rate Limiting

- **100 requests per minute** per user
- **30 chat messages per minute** per user
- **20 document uploads per hour** per user

---

## Examples (PowerShell)

### Complete Flow Example

```powershell
# Setup
$baseUrl = "http://localhost:3001/api/v1"
$headers = @{
    "Authorization" = "Bearer my-user-token"
    "Content-Type" = "application/json"
}

# 1. Create a Bot
$botBody = @{
    name = "DevOps Assistant"
    description = "Helps with DevOps tasks"
    instructions = "You are a DevOps expert..."
    scope = "personal"
    config = @{
        model = "gpt-4-turbo"
        temperature = 0.7
        maxTokens = 2000
        enableRAG = $false
    }
    tags = @("devops", "automation")
} | ConvertTo-Json

$bot = Invoke-RestMethod -Uri "$baseUrl/bots" -Method POST -Headers $headers -Body $botBody
$botId = $bot.data.id

Write-Host "✅ Bot created: $botId"

# 2. Chat with Bot
$chatBody = @{
    botId = $botId
    content = "What are best practices for CI/CD?"
    userId = "my-user-token"
} | ConvertTo-Json

$chat = Invoke-RestMethod -Uri "$baseUrl/chat/messages" -Method POST -Headers $headers -Body $chatBody
$conversationId = $chat.data.conversation.id

Write-Host "🤖 Bot response: $($chat.data.assistantMessage.content)"

# 3. Continue Conversation
$followUp = @{
    botId = $botId
    content = "Tell me more about automated testing"
    conversationId = $conversationId
    userId = "my-user-token"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$baseUrl/chat/messages" -Method POST -Headers $headers -Body $followUp

Write-Host "🤖 Follow-up response: $($response.data.assistantMessage.content)"

# 4. List All Bots
$allBots = Invoke-RestMethod -Uri "$baseUrl/bots" -Headers $headers

Write-Host "`n📋 All bots:"
$allBots.data.items | ForEach-Object {
    Write-Host "  - $($_.name) (conversations: $($_.conversationCount))"
}
```

---

## Webhook Events (Coming Soon)

Future support for webhooks to notify external systems of:
- New bot created
- Bot status changed
- New conversation started
- Message received

---

**Note:** Esta API está em desenvolvimento ativo. Novos endpoints e funcionalidades serão adicionados.
