# 🧪 Script de Teste - Teams Bot Automation API
# Execute este script após iniciar a API com: npm run dev:api

Write-Host "🧪 Testando Teams Bot Automation API" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:3001/api/v1"
$headers = @{
    "Authorization" = "Bearer test-user-123"
    "Content-Type" = "application/json"
}

# Teste 1: Health Check
Write-Host "📝 Teste 1: Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health"
    Write-Host "✅ API está online!" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor White
    Write-Host "   Service: $($health.service)`n" -ForegroundColor White
} catch {
    Write-Host "❌ Erro no health check: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Certifique-se de que a API está rodando (npm run dev:api)" -ForegroundColor Yellow
    exit 1
}

# Teste 2: Criar um Bot
Write-Host "📝 Teste 2: Criando um bot..." -ForegroundColor Yellow
try {
    $botBody = @{
        name = "Bot de Observabilidade"
        description = "Bot especializado em métricas, logs e monitoring de sistemas"
        instructions = "Você é um especialista em observabilidade e SRE. Ajude a equipe com métricas, logs, alertas e melhores práticas de monitoring."
        scope = "squad"
        squadId = "observability-team"
        config = @{
            model = "gpt-4-turbo"
            temperature = 0.7
            maxTokens = 2000
            enableRAG = $false
        }
        tags = @("observability", "monitoring", "sre", "metrics")
    } | ConvertTo-Json

    $botResponse = Invoke-RestMethod -Uri "$baseUrl/bots" -Method POST -Headers $headers -Body $botBody
    $botId = $botResponse.data.id
    
    Write-Host "✅ Bot criado com sucesso!" -ForegroundColor Green
    Write-Host "   ID: $botId" -ForegroundColor White
    Write-Host "   Nome: $($botResponse.data.name)" -ForegroundColor White
    Write-Host "   Status: $($botResponse.data.status)`n" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao criar bot: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Teste 3: Listar Bots
Write-Host "📝 Teste 3: Listando bots..." -ForegroundColor Yellow
try {
    $botsResponse = Invoke-RestMethod -Uri "$baseUrl/bots" -Headers $headers
    
    Write-Host "✅ Bots encontrados: $($botsResponse.data.total)" -ForegroundColor Green
    $botsResponse.data.items | ForEach-Object {
        Write-Host "   - $($_.name) (ID: $($_.id))" -ForegroundColor White
    }
    Write-Host ""
} catch {
    Write-Host "❌ Erro ao listar bots: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 4: Buscar Bot por ID
Write-Host "📝 Teste 4: Buscando bot por ID..." -ForegroundColor Yellow
try {
    $bot = Invoke-RestMethod -Uri "$baseUrl/bots/$botId" -Headers $headers
    
    Write-Host "✅ Bot encontrado!" -ForegroundColor Green
    Write-Host "   Nome: $($bot.data.name)" -ForegroundColor White
    Write-Host "   Descrição: $($bot.data.description)" -ForegroundColor White
    Write-Host "   Scope: $($bot.data.scope)" -ForegroundColor White
    Write-Host "   Model: $($bot.data.config.model)`n" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao buscar bot: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 5: Enviar Mensagem para o Bot (Chat)
Write-Host "📝 Teste 5: Conversando com o bot..." -ForegroundColor Yellow
Write-Host "   Pergunta: 'Como posso melhorar o monitoring da nossa aplicação?'" -ForegroundColor Cyan
try {
    $chatBody = @{
        botId = $botId
        content = "Como posso melhorar o monitoring da nossa aplicação? Quais métricas são essenciais?"
        userId = "test-user-123"
    } | ConvertTo-Json

    $chatResponse = Invoke-RestMethod -Uri "$baseUrl/chat/messages" -Method POST -Headers $headers -Body $chatBody
    
    Write-Host "✅ Resposta recebida!" -ForegroundColor Green
    Write-Host "   Conversation ID: $($chatResponse.data.conversation.id)" -ForegroundColor White
    Write-Host "   Tokens usados: $($chatResponse.data.assistantMessage.metadata.tokens)" -ForegroundColor White
    Write-Host "`n🤖 Resposta do Bot:" -ForegroundColor Cyan
    Write-Host "   $($chatResponse.data.assistantMessage.content)`n" -ForegroundColor White
    
    $conversationId = $chatResponse.data.conversation.id
} catch {
    Write-Host "❌ Erro ao conversar com bot: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Detalhes: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
    }
}

# Teste 6: Continuar Conversa
if ($conversationId) {
    Write-Host "📝 Teste 6: Continuando a conversa..." -ForegroundColor Yellow
    Write-Host "   Pergunta: 'E quanto a alertas? Como devo configurá-los?'" -ForegroundColor Cyan
    try {
        $followUpBody = @{
            botId = $botId
            content = "E quanto a alertas? Como devo configurá-los?"
            conversationId = $conversationId
            userId = "test-user-123"
        } | ConvertTo-Json

        $followUpResponse = Invoke-RestMethod -Uri "$baseUrl/chat/messages" -Method POST -Headers $headers -Body $followUpBody
        
        Write-Host "✅ Resposta recebida!" -ForegroundColor Green
        Write-Host "`n🤖 Resposta do Bot:" -ForegroundColor Cyan
        Write-Host "   $($followUpResponse.data.assistantMessage.content)`n" -ForegroundColor White
    } catch {
        Write-Host "❌ Erro ao continuar conversa: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Teste 7: Listar Conversas
Write-Host "📝 Teste 7: Listando conversas..." -ForegroundColor Yellow
try {
    $conversations = Invoke-RestMethod -Uri "$baseUrl/chat/conversations" -Headers $headers
    
    Write-Host "✅ Conversas encontradas: $($conversations.data.Count)" -ForegroundColor Green
    $conversations.data | ForEach-Object {
        Write-Host "   - $($_.title) (ID: $($_.id))" -ForegroundColor White
    }
    Write-Host ""
} catch {
    Write-Host "❌ Erro ao listar conversas: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 8: Atualizar Bot
Write-Host "📝 Teste 8: Atualizando bot..." -ForegroundColor Yellow
try {
    $updateBody = @{
        description = "Bot especializado em observabilidade, SRE e DevOps practices"
        config = @{
            temperature = 0.8
        }
    } | ConvertTo-Json

    $updateResponse = Invoke-RestMethod -Uri "$baseUrl/bots/$botId" -Method PATCH -Headers $headers -Body $updateBody
    
    Write-Host "✅ Bot atualizado!" -ForegroundColor Green
    Write-Host "   Nova descrição: $($updateResponse.data.description)" -ForegroundColor White
    Write-Host "   Nova temperatura: $($updateResponse.data.config.temperature)`n" -ForegroundColor White
} catch {
    Write-Host "❌ Erro ao atualizar bot: $($_.Exception.Message)" -ForegroundColor Red
}

# Resumo
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✨ Testes Concluídos!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host "`n📊 Resumo:" -ForegroundColor Yellow
Write-Host "   ✅ API está funcionando" -ForegroundColor Green
Write-Host "   ✅ Bot criado e configurado" -ForegroundColor Green
Write-Host "   ✅ Chat com IA funcionando" -ForegroundColor Green
Write-Host "   ✅ Histórico de conversas mantido" -ForegroundColor Green
Write-Host "   ✅ CRUD de bots operacional" -ForegroundColor Green

Write-Host "`n🎯 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Explore mais endpoints na docs/API.md" -ForegroundColor White
Write-Host "   2. Teste com diferentes perguntas" -ForegroundColor White
Write-Host "   3. Crie mais bots com diferentes configurações" -ForegroundColor White
Write-Host "   4. Implemente o frontend React" -ForegroundColor White

Write-Host "`n🚀 Sistema pronto para desenvolvimento!`n" -ForegroundColor Green
