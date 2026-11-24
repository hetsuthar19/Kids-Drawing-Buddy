$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=========================================="
Write-Host " Kids Drawing Buddy - First Setup"
Write-Host "=========================================="

$pythonCmd = $null

if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} else {
    Write-Host "Python was not found." -ForegroundColor Red
    Write-Host "Install Python 3.10+ and tick 'Add Python to PATH'."
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[1/4] Creating virtual environment..."
    & $pythonCmd -m venv .venv
} else {
    Write-Host "[1/4] Virtual environment already exists."
}

Write-Host "[2/4] Updating pip..."
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip

Write-Host "[3/4] Installing requirements..."
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "[4/4] Verifying Flask and Werkzeug..."
& ".\.venv\Scripts\python.exe" -c "import flask; import werkzeug; print('OK - Flask and Werkzeug are installed correctly.')"

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "In VS Code select: .venv\Scripts\python.exe"
Write-Host "Then run: .\run_app.bat"
