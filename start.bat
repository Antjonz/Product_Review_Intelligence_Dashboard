@echo off
echo Starting Product Review Intelligence Dashboard...
echo.

start "Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Backend running at http://localhost:8000
echo Frontend running at http://localhost:5173
echo.
echo Close the terminal windows to stop the servers.
