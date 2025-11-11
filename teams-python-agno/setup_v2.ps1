# ==========================================
# Teams Bot Automation - Setup Script
# Azure OpenAI Edition v2.0.0
# ==========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🤖 Teams Bot Automation - Setup" -ForegroundColor Cyan
Write-Host "Azure OpenAI Edition" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verifica Python
Write-Host "📦 Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python não encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python 3.11+ de: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Cria .env se não existir
if (-not (Test-Path ".env")) {
    Write-Host "`n📝 Criando arquivo .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Arquivo .env criado" -ForegroundColor Green
    Write-Host "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais Azure!" -ForegroundColor Yellow
    Write-Host "   Abra: notepad .env" -ForegroundColor Yellow
} else {
    Write-Host "`n✅ Arquivo .env já existe" -ForegroundColor Green
}

# Cria diretórios necessários
Write-Host "`n📁 Criando diretórios..." -ForegroundColor Yellow
$directories = @("data", "data\chromadb", "data\uploads", "logs")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Criado: $dir" -ForegroundColor Green
    }
}

# ==================== BACKEND ====================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🔧 Configurando Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Set-Location backend

# Ambiente virtual backend
if (-not (Test-Path "venv")) {
    Write-Host "`n📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
} else {
    Write-Host "`n✅ Ambiente virtual já existe" -ForegroundColor Green
}

# Ativa ambiente
Write-Host "`n🔌 Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instala dependências
Write-Host "`n📦 Instalando dependências do backend..." -ForegroundColor Yellow
Write-Host "   (Isso pode levar alguns minutos...)" -ForegroundColor Gray
pip install --upgrade pip -q
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

# Volta para raiz
Set-Location ..

# ==================== FRONTEND ====================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🎨 Configurando Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Set-Location frontend

# Ambiente virtual frontend
if (-not (Test-Path "venv")) {
    Write-Host "`n📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
} else {
    Write-Host "`n✅ Ambiente virtual já existe" -ForegroundColor Green
}

# Ativa ambiente
Write-Host "`n🔌 Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instala dependências
Write-Host "`n📦 Instalando dependências do frontend..." -ForegroundColor Yellow
Write-Host "   (Isso pode levar alguns minutos...)" -ForegroundColor Gray
pip install --upgrade pip -q
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

# Volta para raiz
Set-Location ..

# ==================== FINALIZAÇÃO ====================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Concluído!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`n📝 Próximos Passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  Configure suas credenciais Azure OpenAI:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  Inicie o backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python -m app.main" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Em outro terminal, inicie o frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   streamlit run app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Acesse:" -ForegroundColor White
Write-Host "   📚 API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   🎨 UI:  http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Documentação completa: README_NEW.md" -ForegroundColor Yellow
Write-Host ""
