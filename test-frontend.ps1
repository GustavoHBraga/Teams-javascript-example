# Script para testar o Frontend do Teams Bot
# Este script inicia a API e o Frontend em terminais separados

Write-Host "`n=== 🎨 Teams Bot Frontend - Teste Completo ===" -ForegroundColor Cyan
Write-Host "`nEste script vai:" -ForegroundColor Yellow
Write-Host "  1. Verificar se MongoDB está rodando"
Write-Host "  2. Iniciar a API (porta 3001)"
Write-Host "  3. Iniciar o Frontend (porta 3000)"
Write-Host "  4. Abrir o navegador automaticamente`n"

# Verificar MongoDB
Write-Host "[1/4] Verificando MongoDB..." -ForegroundColor Cyan
try {
    $mongoTest = Invoke-WebRequest -Uri "http://localhost:27017" -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "✅ MongoDB está rodando!" -ForegroundColor Green
} catch {
    Write-Host "❌ MongoDB não está rodando!" -ForegroundColor Red
    Write-Host "`n💡 Para iniciar o MongoDB:" -ForegroundColor Yellow
    Write-Host "   docker run -d -p 27017:27017 --name mongodb mongo:latest`n"
    $continue = Read-Host "Deseja continuar mesmo assim? (s/N)"
    if ($continue -ne "s" -and $continue -ne "S") {
        exit
    }
}

# Verificar .env da API
Write-Host "`n[2/4] Verificando configuração da API..." -ForegroundColor Cyan
$envPath = "packages\api\.env"
if (Test-Path $envPath) {
    Write-Host "✅ Arquivo .env encontrado!" -ForegroundColor Green
    $envContent = Get-Content $envPath -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "✅ OPENAI_API_KEY configurada!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  OPENAI_API_KEY não está configurada no .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Arquivo .env não encontrado em packages/api/" -ForegroundColor Yellow
}

# Verificar .env do Frontend
Write-Host "`n[3/4] Verificando configuração do Frontend..." -ForegroundColor Cyan
$frontendEnvPath = "packages\frontend\.env"
if (Test-Path $frontendEnvPath) {
    Write-Host "✅ Arquivo .env do frontend encontrado!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Arquivo .env do frontend não encontrado" -ForegroundColor Yellow
}

# Iniciar API em novo terminal
Write-Host "`n[4/4] Iniciando serviços..." -ForegroundColor Cyan
Write-Host "🚀 Iniciando API (porta 3001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; Write-Host '=== API Server ===' -ForegroundColor Green; npm run dev:api"

# Aguardar API iniciar
Write-Host "⏳ Aguardando API inicializar (15 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Testar API
try {
    $apiHealth = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/health" -Method Get
    Write-Host "✅ API está respondendo!" -ForegroundColor Green
    Write-Host "   Status: $($apiHealth.data.status)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  API ainda não está respondendo (pode levar mais tempo)" -ForegroundColor Yellow
}

# Iniciar Frontend em novo terminal
Write-Host "`n🎨 Iniciando Frontend (porta 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; Write-Host '=== Frontend Server ===' -ForegroundColor Blue; npm run dev:frontend"

# Aguardar Frontend iniciar
Write-Host "⏳ Aguardando Frontend inicializar (10 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Abrir navegador
Write-Host "`n🌐 Abrindo navegador..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

Write-Host "`n✨ ==================================" -ForegroundColor Green
Write-Host "✨ Tudo pronto!" -ForegroundColor Green
Write-Host "✨ ==================================" -ForegroundColor Green
Write-Host "`nServiços rodando:" -ForegroundColor Cyan
Write-Host "  📡 API:      http://localhost:3001" -ForegroundColor White
Write-Host "  🎨 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "`n💡 Próximos passos:" -ForegroundColor Yellow
Write-Host "  1. Clique em 'Criar Bot' no frontend"
Write-Host "  2. Preencha o formulário e crie um bot"
Write-Host "  3. Clique em 'Conversar' para testar o chat"
Write-Host "`n⚠️  Para parar os servidores:" -ForegroundColor Yellow
Write-Host "  Feche os terminais da API e Frontend"
Write-Host "  Ou pressione Ctrl+C em cada terminal`n"

# Monitorar logs (opcional)
$monitor = Read-Host "Deseja monitorar os logs aqui? (s/N)"
if ($monitor -eq "s" -or $monitor -eq "S") {
    Write-Host "`n📊 Monitorando logs (Ctrl+C para sair)..." -ForegroundColor Cyan
    Write-Host "Acompanhe os terminais individuais para logs detalhados`n" -ForegroundColor Gray
    
    while ($true) {
        Start-Sleep -Seconds 5
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:3001/api/v1/health" -Method Get -ErrorAction SilentlyContinue
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] API: ✅ OK | Frontend: ✅ OK" -ForegroundColor Green
        } catch {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] API: ❌ DOWN" -ForegroundColor Red
        }
    }
}
