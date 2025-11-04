# 🤖 Teams Bot Automation Platform

Uma plataforma completa para criar e gerenciar agentes de automação com IA no Microsoft Teams. Crie bots personalizados com RAG (Retrieval Augmented Generation) para sua squad.

## ✨ Funcionalidades

- 🤖 **Criação de Bots Personalizados**: Crie bots com instruções específicas para sua squad
- 📚 **RAG (Retrieval Augmented Generation)**: Anexe documentações para treinar seus bots
- 💬 **Chat Interativo**: Converse com seus bots diretamente no Teams
- 👥 **Gestão de Squads**: Compartilhe bots com sua equipe
- 📊 **Analytics**: Acompanhe o uso e performance dos bots
- 🔒 **Seguro**: Autenticação e autorização integradas

## 🏗️ Arquitetura

Este é um monorepo TypeScript contendo:

```
teams-bot-automation/
├── packages/
│   ├── shared/      # Tipos, constantes e utilidades compartilhadas
│   ├── api/         # API REST (Express + MongoDB)
│   ├── bot/         # Bot do Teams (Bot Framework)
│   └── frontend/    # Interface Web (React + Fluent UI)
```

## 🚀 Começando

### Pré-requisitos

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0
- **MongoDB** (local ou Atlas)
- **Azure OpenAI** ou **OpenAI API Key**

### Instalação

1. **Clone o repositório**

```powershell
git clone <seu-repositorio>
cd teams
```

2. **Instale as dependências**

```powershell
npm install
```

3. **Configure as variáveis de ambiente**

Copie o arquivo de exemplo e configure:

```powershell
Copy-Item packages\api\.env.example packages\api\.env
```

Edite `packages/api/.env` com suas credenciais:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/teams-bot-automation

# Azure OpenAI (ou OpenAI)
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
# OU
OPENAI_API_KEY=your-openai-key
```

4. **Inicie o MongoDB** (se estiver usando localmente)

```powershell
# Com Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Ou instale o MongoDB Community Edition
# https://www.mongodb.com/try/download/community
```

5. **Compile os pacotes**

```powershell
npm run build
```

6. **Inicie os serviços em modo desenvolvimento**

```powershell
# Inicia todos os serviços simultaneamente
npm run dev

# Ou inicie individualmente:
npm run dev:api      # API na porta 3001
npm run dev:bot      # Bot do Teams
npm run dev:frontend # Frontend na porta 3000
```

## 🧪 Testando Localmente

### 1. Teste o Health Check da API

Abra o PowerShell e execute:

```powershell
Invoke-RestMethod -Uri "http://localhost:3001/api/v1/health"
```

Você deve ver:

```json
{
  "status": "ok",
  "timestamp": "2025-11-03T...",
  "service": "teams-bot-automation-api"
}
```

### 2. Teste a Criação de um Bot

```powershell
$headers = @{
    "Authorization" = "Bearer test-user-123"
    "Content-Type" = "application/json"
}

$body = @{
    name = "Bot de Observabilidade"
    description = "Bot especializado em métricas e monitoring"
    instructions = "Você é um especialista em observabilidade de sistemas. Ajude a equipe com métricas, logs e alertas."
    scope = "squad"
    squadId = "observability-team"
    config = @{
        model = "gpt-4-turbo"
        temperature = 0.7
        maxTokens = 2000
        enableRAG = $true
    }
    tags = @("observability", "monitoring", "sre")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:3001/api/v1/bots" -Method POST -Headers $headers -Body $body
```

### 3. Teste uma Conversa com o Bot

```powershell
$chatBody = @{
    botId = "<bot-id-do-passo-anterior>"
    content = "Como posso melhorar o monitoring da nossa aplicação?"
    userId = "test-user-123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:3001/api/v1/chat/messages" -Method POST -Headers $headers -Body $chatBody
```

## 📦 Estrutura dos Packages

### @teams-bot/shared

Biblioteca compartilhada com tipos, schemas de validação e utilitários.

```typescript
import { Bot, BotStatus, createBotSchema } from '@teams-bot/shared';
```

### @teams-bot/api

API REST com endpoints para:

- `/api/v1/bots` - CRUD de bots
- `/api/v1/chat` - Conversas e mensagens
- `/api/v1/documents` - Upload de documentos
- `/api/v1/squads` - Gestão de equipes

### @teams-bot/bot

Bot do Microsoft Teams usando Bot Framework SDK.

### @teams-bot/frontend

Interface React com Fluent UI para:

- Gallery de bots
- Creator de bots
- Chat interface
- Analytics dashboard

## 🛠️ Scripts Disponíveis

```powershell
# Desenvolvimento
npm run dev              # Inicia todos os serviços
npm run dev:api          # Apenas API
npm run dev:bot          # Apenas Bot
npm run dev:frontend     # Apenas Frontend

# Build
npm run build            # Build de todos os packages
npm run clean            # Limpa arquivos de build

# Testes
npm run test             # Roda todos os testes
npm run test:watch       # Testes em modo watch

# Qualidade de Código
npm run lint             # ESLint
npm run lint:fix         # ESLint com auto-fix
npm run format           # Prettier
npm run format:check     # Verifica formatação
npm run type-check       # TypeScript type checking
```

## 🔧 Configuração Avançada

### Azure Services (Produção)

Para produção, recomendamos usar os serviços Azure:

1. **Azure OpenAI Service**: IA com compliance empresarial
2. **Azure Cosmos DB**: Banco de dados escalável
3. **Azure Blob Storage**: Armazenamento de documentos
4. **Azure AI Search**: Busca vetorial para RAG
5. **Azure Bot Service**: Hospedagem do bot

### RAG Configuration

O sistema de RAG está configurado para:

- Máximo de 50 documentos por bot
- Limite de 10MB por documento
- Suporta: PDF, TXT, MD, DOCX

## 📝 Desenvolvimento

### Adicionando uma Nova Feature

1. Crie uma branch:
```powershell
git checkout -b feature/minha-feature
```

2. Faça suas alterações

3. Execute os testes e linting:
```powershell
npm run test
npm run lint
npm run type-check
```

4. Commit (Husky vai rodar pre-commit hooks):
```powershell
git add .
git commit -m "feat: adiciona minha feature"
```

5. Push e crie um Pull Request:
```powershell
git push origin feature/minha-feature
```

### Code Style

- **ESLint** para linting
- **Prettier** para formatação
- **TypeScript** com strict mode
- **Conventional Commits** para mensagens de commit

## 🐛 Troubleshooting

### MongoDB Connection Error

```
Error: connect ECONNREFUSED 127.0.0.1:27017
```

**Solução**: Certifique-se de que o MongoDB está rodando:

```powershell
# Verifique se o container está rodando
docker ps | Select-String mongodb

# Se não estiver, inicie
docker start mongodb
```

### Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::3001
```

**Solução**: Mate o processo na porta:

```powershell
# Encontre o processo
Get-NetTCPConnection -LocalPort 3001 | Select-Object -ExpandProperty OwningProcess

# Mate o processo (substitua PID)
Stop-Process -Id <PID> -Force
```

### TypeScript Errors

Se você ver erros de módulos não encontrados, rebuild o projeto:

```powershell
npm run clean
npm install
npm run build
```

## 📚 Documentação Completa

### **🚀 Guias de Início**
- [Quick Start](./docs/QUICK_START.md) - Começar em 5 minutos
- [Arquitetura](./docs/ARCHITECTURE.md) - Visão geral do sistema
- [Project Summary](./docs/PROJECT_SUMMARY.md) - Resumo executivo

### **💻 APIs e Desenvolvimento**
- [API Documentation](./docs/API.md) - Endpoints e exemplos de uso
- [Frontend Guide](./docs/FRONTEND_GUIDE.md) - Desenvolvimento React + Fluent UI

### **🧠 RAG e Vector Databases**
- [📄 Document Upload](./docs/DOCUMENT_UPLOAD.md) - Upload e RAG básico
- [🧠 Vector Database Guide](./docs/VECTOR_DATABASE_GUIDE.md) - ChromaDB implementação completa
- [⚡ Quick ChromaDB Setup](./docs/QUICK_CHROMADB.md) - Setup ChromaDB em 5 minutos
- [📊 Vector DB Comparison](./docs/VECTOR_DB_COMPARISON.md) - Comparação: ChromaDB vs Pinecone vs outros
- [💻 ChromaDB Implementation](./docs/CHROMADB_IMPLEMENTATION.md) - Código pronto para copiar

---

## 📚 Próximos Passos

- [x] Implementar frontend React
- [x] Adicionar upload de documentos
- [ ] Configurar Bot do Teams
- [ ] Adicionar autenticação com Azure AD
- [ ] Implementar ChromaDB para RAG avançado
- [ ] Integrar Azure AI Search (alternativa)
- [ ] Adicionar testes unitários e E2E
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Deploy para Azure

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie sua feature branch
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é proprietário e confidencial.

## 👥 Time

Desenvolvido com ❤️ para automação no Teams

---

**Dúvidas?** Abra uma issue ou entre em contato com o time de desenvolvimento.
