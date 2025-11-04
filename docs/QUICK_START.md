# Quick Start Guide - Teams Bot Automation

## 🚀 Instalação Rápida (5 minutos)

### 1. Instalar Dependências

```powershell
# No diretório raiz do projeto
npm install
```

### 2. Configurar MongoDB

**Opção A: Docker (Recomendado)**

```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Opção B: MongoDB Atlas (Cloud)**

1. Crie uma conta em https://www.mongodb.com/cloud/atlas
2. Crie um cluster gratuito
3. Copie a connection string

### 3. Configurar Variáveis de Ambiente

```powershell
# Copie o arquivo de exemplo
Copy-Item packages\api\.env.example packages\api\.env

# Edite o arquivo .env
notepad packages\api\.env
```

**Mínimo necessário:**

```env
MONGODB_URI=mongodb://localhost:27017/teams-bot-automation
OPENAI_API_KEY=sk-your-openai-key-here
```

### 4. Build e Start

```powershell
# Build todos os packages
npm run build

# Inicie a API
npm run dev:api
```

### 5. Teste!

Abra outro terminal PowerShell e execute:

```powershell
# Health Check
Invoke-RestMethod -Uri "http://localhost:3001/api/v1/health"

# Criar um Bot
$headers = @{
    "Authorization" = "Bearer test-user"
    "Content-Type" = "application/json"
}

$body = @{
    name = "Meu Primeiro Bot"
    description = "Bot de teste para desenvolvimento"
    instructions = "Você é um assistente útil que ajuda com programação."
    scope = "personal"
    config = @{
        model = "gpt-4-turbo"
        temperature = 0.7
        maxTokens = 2000
        enableRAG = $false
    }
    tags = @("teste", "dev")
} | ConvertTo-Json

$bot = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/bots" -Method POST -Headers $headers -Body $body

Write-Host "Bot criado com ID: $($bot.data.id)"
```

## 🎯 Próximos Passos

### Testar Chat

```powershell
$chatBody = @{
    botId = "<cole-o-id-do-bot-aqui>"
    content = "Olá! Como você pode me ajudar?"
    userId = "test-user"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/chat/messages" -Method POST -Headers $headers -Body $chatBody

Write-Host "Resposta do Bot: $($response.data.assistantMessage.content)"
```

### Listar Bots

```powershell
$bots = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/bots" -Headers $headers

$bots.data.items | ForEach-Object {
    Write-Host "- $($_.name) (ID: $($_.id))"
}
```

## 🔥 Comandos Úteis

```powershell
# Ver logs da API em tempo real
npm run dev:api

# Rebuild após mudanças
npm run build

# Verificar erros de TypeScript
npm run type-check

# Formatar código
npm run format

# Limpar e reinstalar
npm run clean; npm install; npm run build
```

## ⚠️ Problemas Comuns

### "Cannot find module '@teams-bot/shared'"

**Solução:**
```powershell
npm run build
```

### "ECONNREFUSED 127.0.0.1:27017"

**Solução:**
```powershell
# Verifique se MongoDB está rodando
docker ps | Select-String mongodb

# Se não, inicie
docker start mongodb
```

### "Port 3001 already in use"

**Solução:**
```powershell
# Encontre e mate o processo
Get-NetTCPConnection -LocalPort 3001 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}
```

## 📚 Documentação Adicional

- [README Principal](../README.md) - Documentação completa
- [API Endpoints](./API.md) - Referência da API
- [Architecture](./ARCHITECTURE.md) - Arquitetura do sistema

## 🎉 Pronto!

Agora você tem:
- ✅ API rodando na porta 3001
- ✅ MongoDB conectado
- ✅ Bot criado e funcionando
- ✅ Sistema pronto para desenvolvimento

**Próximo:** Inicie o frontend com `npm run dev:frontend` e comece a desenvolver!
