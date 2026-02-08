#!/bin/bash

# ============================================================
# Shanyan AI - Complete System Setup & Startup Script
# ============================================================
# This script will:
#   1. Create Python virtual environment (if not exists)
#   2. Install Python dependencies
#   3. Install Node.js dependencies
#   4. Train the model (if not already trained)
#   5. Start the backend server
#   6. Start the frontend server
#   7. Open the browser
# ============================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/.venv"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           🚀 Shanyan AI - Auto Setup & Start               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================
# Step 1: Create Python Virtual Environment
# ============================================================
echo -e "${YELLOW}📦 Step 1: Setting up Python Virtual Environment...${NC}"

if [ -d "$VENV_DIR" ]; then
    echo -e "${GREEN}   ✅ Virtual environment already exists${NC}"
else
    echo -e "${BLUE}   Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}   ✅ Virtual environment created${NC}"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}   ✅ Virtual environment activated${NC}"
echo ""

# ============================================================
# Step 2: Install Python Dependencies
# ============================================================
echo -e "${YELLOW}📦 Step 2: Installing Python Dependencies...${NC}"
pip install --quiet --upgrade pip
pip install --quiet -r "$BACKEND_DIR/requirements.txt"
echo -e "${GREEN}   ✅ Python dependencies installed${NC}"
echo ""

# ============================================================
# Step 3: Check for .env file
# ============================================================
echo -e "${YELLOW}🔑 Step 3: Checking Environment Configuration...${NC}"

if [ -f "$BACKEND_DIR/.env" ]; then
    echo -e "${GREEN}   ✅ .env file found${NC}"
else
    echo -e "${RED}   ⚠️  .env file not found!${NC}"
    echo -e "${YELLOW}   Creating .env from .env.example...${NC}"
    cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
    echo -e "${RED}   ⚠️  Please edit backend/.env and add your GEMINI_API_KEY${NC}"
    echo -e "${BLUE}   Get your API key from: https://aistudio.google.com/api-keys${NC}"
fi
echo ""

# ============================================================
# Step 4: Train Model (if not already trained)
# ============================================================
echo -e "${YELLOW}🧠 Step 4: Checking ML Model...${NC}"

MODEL_PATH="$BACKEND_DIR/training/models/fine_tuned_bert"

if [ -d "$MODEL_PATH" ] && [ -f "$MODEL_PATH/config.json" ]; then
    echo -e "${GREEN}   ✅ Trained model found${NC}"
else
    echo -e "${BLUE}   Training DistilBERT model (this may take 10-30 minutes)...${NC}"
    cd "$SCRIPT_DIR"
    python "$BACKEND_DIR/training/train.py"
    echo -e "${GREEN}   ✅ Model training complete${NC}"
fi
echo ""

# ============================================================
# Step 5: Install Frontend Dependencies
# ============================================================
echo -e "${YELLOW}📦 Step 5: Installing Frontend Dependencies...${NC}"

cd "$FRONTEND_DIR"
if [ -d "node_modules" ]; then
    echo -e "${GREEN}   ✅ Node modules already installed${NC}"
else
    echo -e "${BLUE}   Running npm install...${NC}"
    npm install --silent
    echo -e "${GREEN}   ✅ Frontend dependencies installed${NC}"
fi
echo ""

# ============================================================
# Step 6: Start Backend Server
# ============================================================
echo -e "${YELLOW}🖥️  Step 6: Starting Backend Server...${NC}"

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}   ✅ Backend already running on port 8000${NC}"
else
    cd "$BACKEND_DIR"
    PYTHONPATH="$BACKEND_DIR" "$VENV_DIR/bin/python" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/shanyan-backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}   ✅ Backend started (PID: $BACKEND_PID)${NC}"
    echo -e "${BLUE}   Waiting for backend to initialize...${NC}"
    sleep 5
fi
echo ""

# ============================================================
# Step 7: Initialize Demo Users
# ============================================================
echo -e "${YELLOW}👥 Step 7: Initializing Demo Users...${NC}"
curl -s -X POST http://localhost:8000/api/init-users > /dev/null 2>&1 || true
echo -e "${GREEN}   ✅ Demo users ready${NC}"
echo ""

# ============================================================
# Step 8: Start Frontend Server
# ============================================================
echo -e "${YELLOW}🌐 Step 8: Starting Frontend Server...${NC}"

# Check if frontend is already running
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}   ✅ Frontend already running on port 5173${NC}"
else
    cd "$FRONTEND_DIR"
    npm run dev > /tmp/shanyan-frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}   ✅ Frontend started (PID: $FRONTEND_PID)${NC}"
    sleep 3
fi
echo ""

# ============================================================
# Step 9: Open Browser
# ============================================================
echo -e "${YELLOW}🌍 Step 9: Opening Browser...${NC}"
sleep 2

# Detect OS and open browser accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "http://localhost:5173"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "http://localhost:5173" 2>/dev/null || sensible-browser "http://localhost:5173" 2>/dev/null || true
fi
echo -e "${GREEN}   ✅ Browser opened${NC}"
echo ""

# ============================================================
# Success Message
# ============================================================
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              🎉 System Ready & Running!                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Demo Accounts:${NC}"
echo "   Admin:        admin / admin123"
echo "   Client:       client1 / client123 (Rajesh Kumar)"
echo "   Tech Support: tech1 / tech123 (Priya Sharma)"
echo "   Accounting:   acc1 / acc123 (Amit Patel)"
echo "   Sales:        sales1 / sales123 (Sneha Reddy)"
echo ""
echo -e "${BLUE}🔗 URLs:${NC}"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo "   Backend:   /tmp/shanyan-backend.log"
echo "   Frontend:  /tmp/shanyan-frontend.log"
echo ""
echo -e "${YELLOW}💡 To stop the servers:${NC}"
echo "   Backend:  kill \$(lsof -t -i:8000)"
echo "   Frontend: kill \$(lsof -t -i:5173)"
echo ""
echo "Created by Shankar Narayanan, Student, Dr MGR University"
echo ""
