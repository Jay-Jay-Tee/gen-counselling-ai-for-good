# =============================================================================
# Render Deployment Setup Script
# =============================================================================
# This script prepares your project for deployment to Render
# Run this BEFORE pushing to GitHub and deploying to Render

$ErrorActionPreference = "Stop"  # Exit on error

Write-Host "Genetic Risk Coach - Render Deployment Setup"
Write-Host "=============================================="
Write-Host ""

# Color codes
$GREEN  = "Green"
$YELLOW = "Yellow"
$RED    = "Red"
$NC     = "White" # No Color

# Check if we're in the project root
if (!(Test-Path -Path "README.md" -PathType Leaf)) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor $RED
    exit 1
}

Write-Host "This script will:" -ForegroundColor $YELLOW
Write-Host "  1. Verify all required files exist"
Write-Host "  2. Create missing __init__.py files"
Write-Host "  3. Fix file naming issues"
Write-Host "  4. Create .env files for reference"
Write-Host "  5. Validate project structure"
Write-Host ""

$reply = Read-Host "Continue? (y/n)"
if ($reply -notmatch '^[Yy]$') {
    Write-Host "Aborted."
    exit 0
}

Write-Host ""
Write-Host "Step 1: Creating missing __init__.py files..." -ForegroundColor $GREEN

# Create __init__.py files
New-Item -ItemType File -Force "backend/app/routers/__init__.py" | Out-Null
New-Item -ItemType File -Force "backend/app/services/__init__.py" | Out-Null
New-Item -ItemType File -Force "backend/app/schemas/__init__.py" | Out-Null
New-Item -ItemType File -Force "ai/ocr/__init__.py" | Out-Null

Write-Host "  Created backend/app/routers/__init__.py"
Write-Host "  Created backend/app/services/__init__.py"
Write-Host "  Created backend/app/schemas/__init__.py"
Write-Host "  Created ai/ocr/__init__.py"

Write-Host ""
Write-Host "Step 2: Fixing OCR filename..." -ForegroundColor $GREEN

if (Test-Path -Path "ai/ocr/ocr-pipeline.py" -PathType Leaf) {
    Move-Item -Path "ai/ocr/ocr-pipeline.py" -Destination "ai/ocr/ocr_pipeline.py"
    Write-Host "  Renamed ocr-pipeline.py -> ocr_pipeline.py"
} else {
    Write-Host "  ocr-pipeline.py not found (may already be fixed)"
}

Write-Host ""
Write-Host "Step 3: Creating local .env files..." -ForegroundColor $GREEN

# Backend .env
if (!(Test-Path -Path "backend/.env" -PathType Leaf)) {
    $backendEnv = @"
# Local Development Environment
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
"@
    $backendEnv | Set-Content -Path "backend/.env" -Encoding UTF8
    Write-Host "  Created backend/.env"
} else {
    Write-Host "  backend/.env already exists"
}

# Frontend .env
if (!(Test-Path -Path "frontend/.env" -PathType Leaf)) {
    $frontendEnv = @"
# Local Development - Leave empty to use Vite proxy
# VITE_API_URL=
"@
    $frontendEnv | Set-Content -Path "frontend/.env" -Encoding UTF8
    Write-Host "  Created frontend/.env"
} else {
    Write-Host "  frontend/.env already exists"
}

Write-Host ""
Write-Host "Step 4: Validating project structure..." -ForegroundColor $GREEN

# Check critical files
$ERRORS = 0

function check_file($path) {
    if (Test-Path -Path $path -PathType Leaf) {
        Write-Host "  OK: $path"
    } else {
        Write-Host "  MISSING: $path" -ForegroundColor $RED
        $script:ERRORS++
    }
}

Write-Host ""
Write-Host "Backend files:"
check_file "backend/app/main.py"
check_file "backend/app/config.py"
check_file "backend/app/__init__.py"
check_file "backend/app/routers/__init__.py"
check_file "backend/app/services/__init__.py"
check_file "backend/app/schemas/__init__.py"
check_file "backend/requirements.txt"

Write-Host ""
Write-Host "AI module files:"
check_file "ai/__init__.py"
check_file "ai/risk/risk_model.py"
check_file "ai/requirements.txt"

Write-Host ""
Write-Host "Frontend files:"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/src/main.jsx"
check_file "frontend/src/App.jsx"
check_file "frontend/src/index.css"

Write-Host ""
Write-Host "Deployment files:"
check_file "render.yaml"
check_file ".gitignore"

Write-Host ""
if ($ERRORS -eq 0) {
    Write-Host "All critical files present!" -ForegroundColor $GREEN
} else {
    Write-Host "$ERRORS file(s) missing. Please create them before deploying." -ForegroundColor $RED
    exit 1
}

Write-Host ""
Write-Host "=============================================="
Write-Host "Setup Complete!" -ForegroundColor $GREEN
Write-Host "=============================================="
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor $YELLOW
Write-Host ""

Write-Host @'
1) Commit and push to GitHub:
    git add .
    git commit -m 'Prepare for Render deployment'
    git push origin main

2) Deploy Backend on Render:
    - Go to render.com -> New Web Service
    - Connect your GitHub repo
    - Root Directory: backend
    - Build: pip install -r requirements.txt && pip install -r ../ai/requirements.txt
    - Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    - Copy the backend URL (e.g., https://xxx.onrender.com)

3) Deploy Frontend on Render:
    - Go to render.com -> New Static Site
    - Connect same GitHub repo
    - Root Directory: frontend
    - Build: npm install && npm run build
    - Publish Directory: dist
    - Add Environment Variable:
      VITE_API_URL = <your-backend-url>

4) Update Backend CORS:
    - Go to backend service -> Environment
    - Add: CORS_ORIGINS = <your-frontend-url>

Your project is ready for deployment!
'@
