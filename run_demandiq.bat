@echo off
echo ===================================================
echo             Starting DemandIQ Servers
echo ===================================================
echo.

echo Starting FastAPI Backend Server...
start "DemandIQ Backend" cmd /k "cd /d %~dp0 && call venv\Scripts\activate && python backend\app\main.py"

echo Starting React Frontend Dashboard...
start "DemandIQ Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo Servers are booting up in separate windows!
echo - Backend API: http://localhost:8000
echo - Frontend Dashboard: http://localhost:5173
echo.
echo You can now open http://localhost:5173 in your browser.
pause
