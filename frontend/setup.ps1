# Frontend Setup Script
# Creates React app with all dependencies

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "  AgentMonitor Frontend Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if in correct directory
$currentDir = Get-Location
if ($currentDir.Path -notlike "*\frontend") {
    Write-Host "❌ Please run this from the frontend folder!" -ForegroundColor Red
    Write-Host "   cd frontend" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Creating React app..." -ForegroundColor Green
npx create-react-app . --template typescript

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ React app creation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Installing dependencies..." -ForegroundColor Green
npm install axios react-router-dom recharts @types/react-router-dom

Write-Host "`n✅ Frontend setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. npm start" -ForegroundColor White
Write-Host "  2. Open http://localhost:3000" -ForegroundColor White
Write-Host "`n================================`n" -ForegroundColor Cyan
