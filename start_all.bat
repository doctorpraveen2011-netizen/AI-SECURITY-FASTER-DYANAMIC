@echo off
echo ========================================================
echo Starting AI SECURITY FASTER (Backend + Frontend)
echo ========================================================

start "AI Security Faster - Backend" cmd /k ".\backend\venv\Scripts\python run_backend.py"
timeout /t 3 >nul
start "AI Security Faster - Frontend" cmd /k "npm run dev --prefix frontend"

echo.
echo Both servers started!
echo Frontend: http://localhost:5173
echo Backend API: http://127.0.0.1:8000
echo ========================================================
pause
