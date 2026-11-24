@echo off
title Kids Drawing Buddy
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Running first-time setup...
    call setup_windows.bat
    if errorlevel 1 exit /b 1
)

".venv\Scripts\python.exe" -c "import flask; import werkzeug" >nul 2>nul
if errorlevel 1 (
    echo Flask dependencies are missing. Repairing installation...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Could not install dependencies.
        pause
        exit /b 1
    )
)

echo.
echo Starting Kids Drawing Buddy...
echo Open this in your browser:
echo http://127.0.0.1:5000
echo.
".venv\Scripts\python.exe" app.py

pause
