# ==========================================
# Start All Services - Azure Edition
# ==========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 Teams Bot Automation - Iniciando" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verifica .env
if (-not (Test-Path ".env")) {
    Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "   Execute primeiro: .\setup_v2.ps1" -ForegroundColor Yellow
    Write-Host "   Depois configure: notepad .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "📝 Este script abrirá 2 terminais:" -ForegroundColor Yellow
Write-Host "   1️⃣  Backend (FastAPI) - http://localhost:8000" -ForegroundColor White
Write-Host "   2️⃣  Frontend (Streamlit) - http://localhost:8501" -ForegroundColor White
Write-Host ""

# Inicia Backend em nova janela
Write-Host "🔧 Iniciando Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start-backend-v2.ps1"

# Aguarda 3 segundos
Start-Sleep -Seconds 3

# Inicia Frontend em nova janela
Write-Host "🎨 Iniciando Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start-frontend-v2.ps1"

Write-Host ""
Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🎨 Interface: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "ℹ️  Feche as janelas para parar os serviços" -ForegroundColor Gray
Write-Host ""
