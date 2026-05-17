# Quick diagnostic script to check AgentMonitor services

Write-Host "AgentMonitor Service Health Check" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check MongoDB
Write-Host "📊 Checking MongoDB..." -ForegroundColor Yellow
try {
    $mongoTest = Test-NetConnection -ComputerName localhost -Port 27017 -WarningAction SilentlyContinue
    if ($mongoTest.TcpTestSucceeded) {
        Write-Host "✅ MongoDB is running on localhost:27017" -ForegroundColor Green
    } else {
        Write-Host "❌ MongoDB is NOT running on localhost:27017" -ForegroundColor Red
        Write-Host "   Start MongoDB with: mongod --dbpath C:\data\db" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error checking MongoDB: $_" -ForegroundColor Red
}

Write-Host ""

# Check Backend
Write-Host "📡 Checking Backend (FastAPI)..." -ForegroundColor Yellow
try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8080/docs" -Method GET -ErrorAction SilentlyContinue
    if ($backendTest.StatusCode -eq 200) {
        Write-Host "✅ Backend is running on http://localhost:8080" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend returned status: $($backendTest.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Backend is NOT running on localhost:8080" -ForegroundColor Red
    Write-Host "   Start from: cd backend && python app.py" -ForegroundColor Yellow
}

Write-Host ""

# Check Frontend
Write-Host "🎨 Checking Frontend (React)..." -ForegroundColor Yellow
try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -ErrorAction SilentlyContinue
    if ($frontendTest.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running on http://localhost:3000" -ForegroundColor Green
    } else {
        Write-Host "❌ Frontend returned status: $($frontendTest.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Frontend is NOT running on localhost:3000" -ForegroundColor Red
    Write-Host "   Start from: cd frontend && npm start" -ForegroundColor Yellow
}

Write-Host ""

# Check Analytics Database Endpoint
Write-Host "📈 Checking Analytics API..." -ForegroundColor Yellow
try {
    $analyticsTest = Invoke-WebRequest -Uri "http://localhost:8080/admin/all_runs" -Method GET -ErrorAction SilentlyContinue
    if ($analyticsTest.StatusCode -eq 200) {
        Write-Host "✅ Analytics API is responding" -ForegroundColor Green
        $data = $analyticsTest.Content | ConvertFrom-Json
        Write-Host "   Found $($data.total) runs in database" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Analytics API returned status: $($analyticsTest.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Analytics API error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Diagnostic check complete." -ForegroundColor Cyan
