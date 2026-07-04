@echo off
python --version
IF ERRORLEVEL 1 (
  echo Python no fue encontrado. Instala Python y marca Add Python to PATH.
  pause
  exit /b 1
)
python -m pip install --upgrade pip
pip install -r requirements.txt
pause
