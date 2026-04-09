#!/bin/bash

# ContentBoost AI - Start Script
# Runs both backend and frontend in separate processes

echo "🚀 Starting ContentBoost AI..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Start Backend
echo "📦 Starting Backend (FastAPI on port 8000)..."
cd backend
source venv/bin/activate || . venv/Scripts/activate
python main.py &
BACKEND_PID=$!
sleep 2

# Start Frontend
echo "🎨 Starting Frontend (React on port 5173)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
sleep 2

echo ""
echo "════════════════════════════════════════════════════"
echo "✅ Both services are running!"
echo ""
echo "🌐 Frontend: http://localhost:5173/"
echo "🔗 Backend:  http://localhost:8000/"
echo "🏥 Health:   http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all services"
echo "════════════════════════════════════════════════════"
echo ""

# Wait for all background processes
wait $BACKEND_PID $FRONTEND_PID
