# AgentMonitor Startup Script
# Run this to start both backend and frontend servers

Write-Host "🚀 Starting AgentMonitor..." -ForegroundColor Green
Write-Host ""

# Check if already running
$backendRunning = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "*app.py*"}
$frontendRunning = Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*react-scripts*"}

if ($backendRunning) {
    Write-Host "⚠️  Backend already running (PID: $($backendRunning.Id))" -ForegroundColor Yellow
} else {
    Write-Host "📡 Starting Backend Server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python app.py"
    Start-Sleep -Seconds 2
}

if ($frontendRunning) {
    Write-Host "⚠️  Frontend already running (PID: $($frontendRunning.Id))" -ForegroundColor Yellow
} else {
    Write-Host "🌐 Starting Frontend Server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm start"
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "✅ Servers starting..." -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access points:" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8080" -ForegroundColor Gray
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host ""
Write-Host "👤 Default credentials:" -ForegroundColor White
Write-Host "   User:  user / user123" -ForegroundColor Gray
Write-Host "   Admin: admin / admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to open browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:3000"
