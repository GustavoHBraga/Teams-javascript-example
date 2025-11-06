# ========================================
# Start Backend - Teams Bot Python
# ========================================

Write-Host "🚀 Iniciando Backend..." -ForegroundColor Cyan

cd backend

# Ativa ambiente virtual
Write-Host "📌 Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Verifica .env
if (!(Test-Path "../.env")) {
    Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "   Execute: .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Inicia servidor
Write-Host "✅ Iniciando FastAPI..." -ForegroundColor Green
Write-Host ""
Write-Host "📝 Backend rodando em:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000" -ForegroundColor White
Write-Host "   http://localhost:8000/docs (Swagger)" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python -m app.main
