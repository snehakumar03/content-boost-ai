@echo off
REM ContentBoost AI - Start Both Services (Windows)

echo 🚀 Starting ContentBoost AI (Windows)
echo.

REM Start Backend in new window
echo 📦 Starting Backend (FastAPI on port 8000)...
START "ContentBoost AI - Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python main.py"

timeout /t 2 /nobreak

REM Start Frontend in new window
echo 🎨 Starting Frontend (React on port 5173)...
START "ContentBoost AI - Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 2 /nobreak

echo.
echo ════════════════════════════════════════════════════
echo ✅ Both services are starting!
echo.
echo 🌐 Frontend: http://localhost:5173/
echo 🔗 Backend:  http://localhost:8000/
echo 🏥 Health:   http://localhost:8000/health
echo.
echo Two windows should have opened above:
echo  - One for Backend (FastAPI)
echo  - One for Frontend (npm)
echo.
echo Close the windows when you're done.
echo ════════════════════════════════════════════════════
echo.
pause
