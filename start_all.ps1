# AgentMonitor Startup Script for PowerShell
# Starts MongoDB and the full stack (Backend + Frontend)

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "AgentMonitor - Full Stack Startup" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB data directory exists
$mongoDataPath = "C:\data\db"
if (-Not (Test-Path $mongoDataPath)) {
    Write-Host "Creating MongoDB data directory: $mongoDataPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $mongoDataPath | Out-Null
}

# Check if mongod is installed
$mongodPath = "C:\Program Files\MongoDB\Server\*\bin\mongod.exe" | Get-Item -ErrorAction SilentlyContinue | Select-Object -Last 1
if ($null -eq $mongodPath) {
    Write-Host "⚠️  MongoDB not found in Program Files" -ForegroundColor Red
    Write-Host "Please install MongoDB from: https://www.mongodb.com/try/download/community" -ForegroundColor Red
    Write-Host "Or ensure mongod is in your PATH" -ForegroundColor Red
    Read-Host "Press Enter to continue anyway (database will be unavailable)"
} else {
    Write-Host "✅ Found MongoDB at: $mongodPath" -ForegroundColor Green
    Write-Host "📦 Starting MongoDB..." -ForegroundColor Cyan
    Start-Process -FilePath $mongodPath -ArgumentList "--dbpath `"$mongoDataPath`"" -NoNewWindow -PassThru | Out-Null
    Start-Sleep -Seconds 3
    Write-Host "✅ MongoDB started on localhost:27017" -ForegroundColor Green
}

Write-Host ""
Write-Host "📡 Starting Backend (FastAPI)..." -ForegroundColor Cyan
$backendPath = Join-Path (Split-Path -Parent $PSScriptRoot) "backend"
Push-Location $backendPath

# Activate virtual environment if it exists
$activateScript = ".\\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & $activateScript
}

# Start backend in a new PowerShell window
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "python app.py" -WindowStyle Normal
Write-Host "✅ Backend started (check new PowerShell window)" -ForegroundColor Green

Pop-Location

Write-Host ""
Write-Host "🎨 Starting Frontend (React)..." -ForegroundColor Cyan
$frontendPath = Join-Path (Split-Path -Parent $PSScriptRoot) "frontend"
Push-Location $frontendPath

# Start frontend in a new PowerShell window
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal
Write-Host "✅ Frontend started (check new PowerShell window)" -ForegroundColor Green

Pop-Location

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "🚀 AgentMonitor is starting!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "📍 Backend:   http://localhost:8080" -ForegroundColor Cyan
Write-Host "📍 MongoDB:   localhost:27017" -ForegroundColor Cyan
Write-Host ""
Write-Host "Give it 10-15 seconds for services to fully initialize." -ForegroundColor Yellow
Write-Host "This window will close automatically..." -ForegroundColor Yellow
Write-Host ""

Start-Sleep -Seconds 5
