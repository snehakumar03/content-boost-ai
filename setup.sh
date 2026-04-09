#!/bin/bash

# ContentBoost AI - Setup Script
# This script automates the initial setup of the project

echo "🚀 ContentBoost AI - Automated Setup"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
echo "📋 Checking Prerequisites..."
echo ""

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found. Install from https://nodejs.org/"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: $NPM_VERSION"
else
    print_error "npm not found"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    print_success "Python found: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python not found. Install from https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "🔧 Setting up Backend..."
echo ""

# Setup Backend
cd backend

# Check if venv exists
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
else
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
print_success "Virtual environment activated"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

# Check .env file
if [ -f ".env" ]; then
    if grep -q "sk-" .env; then
        print_success ".env file exists with API key"
    else
        print_warning ".env file exists but API key not set"
        echo "Please edit backend/.env and add your OpenAI API key"
    fi
else
    print_warning ".env file not found"
    cp .env.example .env
    print_success "Created .env from template"
    echo "📝 Please edit backend/.env and add your OpenAI API key"
fi

echo ""
echo "🎨 Setting up Frontend..."
echo ""

# Setup Frontend
cd ../frontend

# Install npm dependencies
echo "Installing npm packages..."
npm install > /dev/null 2>&1
print_success "npm dependencies installed"

echo ""
echo "✅ Setup Complete!"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
echo "🚀 To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  $ cd backend"
echo "  $ source venv/bin/activate"
echo "  $ python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  $ cd frontend"
echo "  $ npm run dev"
echo ""
echo "Then open: http://localhost:5173/"
echo ""
echo "📚 For detailed instructions, see RUN_GUIDE.md"
echo ""
echo "════════════════════════════════════════════════════════"
