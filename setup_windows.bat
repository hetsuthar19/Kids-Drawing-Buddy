@echo off
title Kids Drawing Buddy - Setup
cd /d "%~dp0"

echo ==========================================
echo   Kids Drawing Buddy - First Setup
echo ==========================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON_CMD=python
    ) else (
        echo ERROR: Python was not found.
        echo Please install Python 3.10 or newer from python.org
        echo IMPORTANT: tick "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :failed
) else (
    echo [1/4] Virtual environment already exists.
)

echo [2/4] Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed

echo [3/4] Installing project requirements...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo [4/4] Checking Flask imports...
".venv\Scripts\python.exe" -c "import flask; import werkzeug; print('OK - Flask and Werkzeug are installed correctly.')"
if errorlevel 1 goto :failed

echo.
echo ==========================================
echo SETUP COMPLETE
echo ==========================================
echo.
echo In VS Code:
echo 1. Open THIS project folder.
echo 2. Press Ctrl+Shift+P.
echo 3. Select: Python: Select Interpreter
echo 4. Pick: .venv\Scripts\python.exe
echo.
echo You can now double-click run_app.bat
echo.
pause
exit /b 0

:failed
echo.
echo ERROR: Setup did not finish successfully.
echo Please copy the error above and send it to ChatGPT.
pause
exit /b 1
