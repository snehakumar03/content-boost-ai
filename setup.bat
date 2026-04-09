@echo off
REM ContentBoost AI - Setup Script for Windows

echo 🚀 ContentBoost AI - Automated Setup (Windows)
echo ===============================================
echo.

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Node.js not found. Install from https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo ✓ Node.js found: %NODE_VERSION%

REM Check npm
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ npm not found
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo ✓ npm found: %NPM_VERSION%

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Python not found. Install from https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%

echo.
echo 🔧 Setting up Backend...
echo.

cd backend

REM Check if venv exists
if exist venv (
    echo ⚠ Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo ✓ Python dependencies installed

REM Check .env file
if exist .env (
    echo ✓ .env file exists
) else (
    echo ⚠ .env file not found
    copy .env.example .env
    echo ✓ Created .env from template
    echo 📝 Please edit backend\.env and add your OpenAI API key
)

echo.
echo 🎨 Setting up Frontend...
echo.

REM Setup Frontend
cd ..\frontend

REM Install npm dependencies
echo Installing npm packages...
npm install >nul 2>&1
echo ✓ npm dependencies installed

echo.
echo ✅ Setup Complete!
echo.
echo ════════════════════════════════════════════════════════
echo.
echo 🚀 To run the application:
echo.
echo Terminal 1 (Backend):
echo   $ cd backend
echo   $ venv\Scripts\activate
echo   $ python main.py
echo.
echo Terminal 2 (Frontend):
echo   $ cd frontend
echo   $ npm run dev
echo.
echo Then open: http://localhost:5173/
echo.
echo 📚 For detailed instructions, see RUN_GUIDE.md
echo.
echo ════════════════════════════════════════════════════════
echo.
pause
