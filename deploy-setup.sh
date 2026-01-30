#!/bin/bash
# =============================================================================
# Render Deployment Setup Script
# =============================================================================
# This script prepares your project for deployment to Render
# Run this BEFORE pushing to GitHub and deploying to Render

set -e  # Exit on error

echo "🚀 Genetic Risk Coach - Render Deployment Setup"
echo "=============================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the project root
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 This script will:${NC}"
echo "  1. Verify all required files exist"
echo "  2. Create missing __init__.py files"
echo "  3. Fix file naming issues"
echo "  4. Create .env files for reference"
echo "  5. Validate project structure"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${GREEN}Step 1: Creating missing __init__.py files...${NC}"

# Create __init__.py files
touch backend/app/routers/__init__.py
touch backend/app/services/__init__.py
touch backend/app/schemas/__init__.py
touch ai/ocr/__init__.py

echo "  ✅ Created backend/app/routers/__init__.py"
echo "  ✅ Created backend/app/services/__init__.py"
echo "  ✅ Created backend/app/schemas/__init__.py"
echo "  ✅ Created ai/ocr/__init__.py"

echo ""
echo -e "${GREEN}Step 2: Fixing OCR filename...${NC}"

if [ -f "ai/ocr/ocr-pipeline.py" ]; then
    mv ai/ocr/ocr-pipeline.py ai/ocr/ocr_pipeline.py
    echo "  ✅ Renamed ocr-pipeline.py → ocr_pipeline.py"
else
    echo "  ⚠️  ocr-pipeline.py not found (may already be fixed)"
fi

echo ""
echo -e "${GREEN}Step 3: Creating local .env files...${NC}"

# Backend .env
if [ ! -f "backend/.env" ]; then
    cat > backend/.env << 'EOF'
# Local Development Environment
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
EOF
    echo "  ✅ Created backend/.env"
else
    echo "  ⚠️  backend/.env already exists"
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    cat > frontend/.env << 'EOF'
# Local Development - Leave empty to use Vite proxy
# VITE_API_URL=
EOF
    echo "  ✅ Created frontend/.env"
else
    echo "  ⚠️  frontend/.env already exists"
fi

echo ""
echo -e "${GREEN}Step 4: Validating project structure...${NC}"

# Check critical files
ERRORS=0

check_file() {
    if [ -f "$1" ]; then
        echo "  ✅ $1"
    else
        echo -e "  ${RED}❌ MISSING: $1${NC}"
        ERRORS=$((ERRORS + 1))
    fi
}

echo ""
echo "Backend files:"
check_file "backend/app/main.py"
check_file "backend/app/config.py"
check_file "backend/app/__init__.py"
check_file "backend/app/routers/__init__.py"
check_file "backend/app/services/__init__.py"
check_file "backend/app/schemas/__init__.py"
check_file "backend/requirements.txt"

echo ""
echo "AI module files:"
check_file "ai/__init__.py"
check_file "ai/risk/risk_model.py"
check_file "ai/requirements.txt"

echo ""
echo "Frontend files:"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/src/main.jsx"
check_file "frontend/src/App.jsx"
check_file "frontend/src/index.css"

echo ""
echo "Deployment files:"
check_file "render.yaml"
check_file ".gitignore"

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All critical files present!${NC}"
else
    echo -e "${RED}❌ $ERRORS file(s) missing. Please create them before deploying.${NC}"
    exit 1
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=============================================="
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo ""
echo "1️⃣  Commit and push to GitHub:"
echo "    git add ."
echo "    git commit -m 'Prepare for Render deployment'"
echo "    git push origin main"
echo ""
echo "2️⃣  Deploy Backend on Render:"
echo "    - Go to render.com → New Web Service"
echo "    - Connect your GitHub repo"
echo "    - Root Directory: backend"
echo "    - Build: pip install -r requirements.txt && pip install -r ../ai/requirements.txt"
echo "    - Start: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "    - Copy the backend URL (e.g., https://xxx.onrender.com)"
echo ""
echo "3️⃣  Deploy Frontend on Render:"
echo "    - Go to render.com → New Static Site"
echo "    - Connect same GitHub repo"
echo "    - Root Directory: frontend"
echo "    - Build: npm install && npm run build"
echo "    - Publish Directory: dist"
echo "    - Add Environment Variable:"
echo "      VITE_API_URL = <your-backend-url>"
echo ""
echo "4️⃣  Update Backend CORS:"
echo "    - Go to backend service → Environment"
echo "    - Add: CORS_ORIGINS = <your-frontend-url>"
echo ""
echo -e "${GREEN}🎉 Your project is ready for deployment!${NC}"
echo ""
