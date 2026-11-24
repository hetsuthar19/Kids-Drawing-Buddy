@echo off
title Kids Drawing Buddy - Easy Start
cd /d "%~dp0"

echo ==============================================
echo       LUMI KIDS COLORING APP - EASY START
echo ==============================================
echo.

REM 1) Find Python
where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PY=python
    ) else (
        echo Python is NOT installed or not added to PATH.
        echo.
        echo Please install Python 3.10 or newer.
        echo During installation, tick:
        echo     Add Python to PATH
        echo.
        pause
        exit /b 1
    )
)

REM 2) Create virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo Step 1/4 - Creating project environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :error
) else (
    echo Step 1/4 - Project environment already exists.
)

REM 3) Install packages
echo Step 2/4 - Installing Flask and Werkzeug...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error

REM 4) Verify imports
echo Step 3/4 - Checking imports...
".venv\Scripts\python.exe" -c "import flask; import werkzeug; print('Flask and Werkzeug are OK.')"
if errorlevel 1 goto :error

REM 5) Start app and browser
echo Step 4/4 - Starting the app...
echo.
echo Your app will open here:
echo http://127.0.0.1:5000
echo.
echo IMPORTANT:
echo Keep this black window OPEN while using the app.
echo Close this window when you want to stop the app.
echo.

start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
exit /b 0

:error
echo.
echo ==============================================
echo Setup failed.
echo Copy the error above and send it to ChatGPT.
echo ==============================================
pause
exit /b 1
