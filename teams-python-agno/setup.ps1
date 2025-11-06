# ========================================
# Script de Setup - Teams Bot Python
# ========================================

Write-Host "🚀 Configurando Teams Bot Automation (Python)" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
Write-Host "📌 Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python não encontrado! Instale Python 3.11+" -ForegroundColor Red
    exit 1
}

# Verifica MongoDB
Write-Host ""
Write-Host "📌 Verificando MongoDB..." -ForegroundColor Yellow
$mongoRunning = Get-Process mongod -ErrorAction SilentlyContinue
if ($mongoRunning) {
    Write-Host "✅ MongoDB rodando" -ForegroundColor Green
} else {
    Write-Host "⚠️  MongoDB não encontrado. Iniciando..." -ForegroundColor Yellow
    Start-Service MongoDB -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ MongoDB iniciado" -ForegroundColor Green
    } else {
        Write-Host "❌ Não foi possível iniciar MongoDB. Inicie manualmente." -ForegroundColor Red
    }
}

# Cria .env se não existir
Write-Host ""
Write-Host "📌 Configurando .env..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Arquivo .env criado. EDITE com suas credenciais!" -ForegroundColor Green
    Write-Host "   - OPENAI_API_KEY" -ForegroundColor Yellow
    Write-Host "   - AGENTOPS_API_KEY (https://agentops.ai)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Arquivo .env já existe" -ForegroundColor Green
}

# Backend
Write-Host ""
Write-Host "📌 Configurando Backend..." -ForegroundColor Yellow
cd backend

if (!(Test-Path "venv")) {
    Write-Host "   Criando ambiente virtual..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
}

Write-Host "   Ativando ambiente virtual..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "   Instalando dependências..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend configurado" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências do backend" -ForegroundColor Red
}

cd ..

# Frontend
Write-Host ""
Write-Host "📌 Configurando Frontend..." -ForegroundColor Yellow
cd frontend

if (!(Test-Path "venv")) {
    Write-Host "   Criando ambiente virtual..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
}

Write-Host "   Ativando ambiente virtual..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

Write-Host "   Instalando dependências..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend configurado" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências do frontend" -ForegroundColor Red
}

cd ..

# Resumo
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Concluído!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Edite o arquivo .env com suas credenciais:" -ForegroundColor White
Write-Host "   - OPENAI_API_KEY=sk-..." -ForegroundColor Gray
Write-Host "   - AGENTOPS_API_KEY=..." -ForegroundColor Gray
Write-Host ""
Write-Host "2. Inicie o Backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python -m app.main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Inicie o Frontend (outro terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   streamlit run app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 URLs:" -ForegroundColor Yellow
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
