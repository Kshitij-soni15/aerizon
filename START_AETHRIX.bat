@echo off
setlocal
cd /d "%~dp0"
color 0B
echo.
echo ================================================
echo        AETHRIX - DRIVER DROWSINESS DEMO
echo ================================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3.11"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PY=python"
  ) else (
    echo Python is not installed.
    echo Please install Python 3.11.x from python.org and tick "Add Python to PATH".
    pause
    exit /b 1
  )
)
if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating project environment...
  %PY% -m venv .venv
  if errorlevel 1 goto :error
)
echo [2/3] Installing required libraries (first run only)...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error
echo [3/3] Starting AETHRIX dashboard...
echo.
echo Keep this window open while using the demo.
.venv\Scripts\python.exe -m streamlit run app.py
pause
exit /b 0
:error
echo.
echo Setup failed. Please send this window's screenshot to ChatGPT.
pause
exit /b 1
