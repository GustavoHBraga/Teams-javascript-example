# Setup Script - Teams Bot Automation
# Este script ajuda a configurar o ambiente de desenvolvimento

Write-Host "🤖 Teams Bot Automation - Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check Node.js
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js não encontrado. Instale em https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm instalado: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Instalando dependências..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependências instaladas" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔨 Compilando packages..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build concluído" -ForegroundColor Green
} else {
    Write-Host "❌ Erro no build" -ForegroundColor Red
    exit 1
}

# Check MongoDB
Write-Host "`n🔍 Verificando MongoDB..." -ForegroundColor Yellow
try {
    $mongoTest = Test-NetConnection -ComputerName localhost -Port 27017 -WarningAction SilentlyContinue
    if ($mongoTest.TcpTestSucceeded) {
        Write-Host "✅ MongoDB rodando na porta 27017" -ForegroundColor Green
    } else {
        throw "MongoDB não encontrado"
    }
} catch {
    Write-Host "⚠️  MongoDB não detectado. Opções:" -ForegroundColor Yellow
    Write-Host "   1. Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest" -ForegroundColor White
    Write-Host "   2. Local: Instale MongoDB Community Edition" -ForegroundColor White
    Write-Host "   3. Cloud: Use MongoDB Atlas (gratuito)" -ForegroundColor White
}

# Check .env
Write-Host "`n⚙️  Verificando configuração..." -ForegroundColor Yellow
$envPath = "packages\api\.env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath -Raw
    
    if ($envContent -match "OPENAI_API_KEY=\s*$" -and $envContent -match "AZURE_OPENAI_API_KEY=\s*$") {
        Write-Host "⚠️  Configure sua OpenAI API Key em $envPath" -ForegroundColor Yellow
        Write-Host "   Sem isso, o bot não poderá gerar respostas!" -ForegroundColor Yellow
    } else {
        Write-Host "✅ API Keys configuradas" -ForegroundColor Green
    }
} else {
    Write-Host "❌ Arquivo .env não encontrado em $envPath" -ForegroundColor Red
}

Write-Host "`n✨ Setup concluído!" -ForegroundColor Green
Write-Host "`n📝 Próximos passos:" -ForegroundColor Cyan
Write-Host "   1. Configure MongoDB (se ainda não fez)" -ForegroundColor White
Write-Host "   2. Adicione sua OPENAI_API_KEY em packages\api\.env" -ForegroundColor White
Write-Host "   3. Execute: npm run dev:api" -ForegroundColor White
Write-Host "   4. Teste: Invoke-RestMethod -Uri 'http://localhost:3001/api/v1/health'" -ForegroundColor White
Write-Host "`n📚 Documentação completa: docs\QUICK_START.md" -ForegroundColor Cyan
Write-Host "`nBoa codificação! 🚀`n" -ForegroundColor Green
