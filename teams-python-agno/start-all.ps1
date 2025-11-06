# ========================================
# Start All - Teams Bot Python
# ========================================

Write-Host "🚀 Iniciando Backend + Frontend..." -ForegroundColor Cyan
Write-Host ""

# Inicia Backend em background
Write-Host "📌 Iniciando Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start-backend.ps1"

# Aguarda 5 segundos
Start-Sleep -Seconds 5

# Inicia Frontend
Write-Host "📌 Iniciando Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start-frontend.ps1"

Write-Host ""
Write-Host "✅ Aplicação iniciada!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesse:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
