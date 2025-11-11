# ==========================================
# Start Backend - Azure Edition
# ==========================================

Write-Host "`n🚀 Iniciando Backend..." -ForegroundColor Cyan

# Vai para pasta backend
Set-Location backend

# Verifica se ambiente virtual existe
if (-not (Test-Path "venv")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "   Execute: .\setup_v2.ps1" -ForegroundColor Yellow
    exit 1
}

# Ativa ambiente virtual
Write-Host "🔌 Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Verifica .env
if (-not (Test-Path "..\.env")) {
    Write-Host "⚠️  Arquivo .env não encontrado!" -ForegroundColor Yellow
    Write-Host "   Copie .env.example para .env e configure suas credenciais" -ForegroundColor Yellow
}

# Inicia servidor
Write-Host "🚀 Iniciando servidor FastAPI..." -ForegroundColor Green
Write-Host ""
python -m app.main
