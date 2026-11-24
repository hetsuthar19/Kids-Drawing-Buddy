#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Setting up Kids Drawing Buddy..."

PYTHON_CMD="python3"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

"$PYTHON_CMD" -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -c "import flask; import werkzeug; print('OK - imports work')"

echo "Setup complete."
echo "Run with: .venv/bin/python app.py"
