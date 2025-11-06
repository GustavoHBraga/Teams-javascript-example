# ========================================
# Start Frontend - Teams Bot Python
# ========================================

Write-Host "🚀 Iniciando Frontend..." -ForegroundColor Cyan

cd frontend

# Ativa ambiente virtual
Write-Host "📌 Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Verifica .env
if (!(Test-Path "../.env")) {
    Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "   Execute: .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Inicia Streamlit
Write-Host "✅ Iniciando Streamlit..." -ForegroundColor Green
Write-Host ""
Write-Host "📝 Frontend rodando em:" -ForegroundColor Cyan
Write-Host "   http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
