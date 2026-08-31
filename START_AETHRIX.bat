@echo off
setlocal
cd /d "%~dp0"
title AETHRIX - Driver Drowsiness Demo
color 0B
echo.
echo ================================================
echo        AETHRIX - DRIVER DROWSINESS DEMO
echo ================================================
echo.
if not exist ".venv\Scripts\python.exe" goto noenv
echo Starting AETHRIX dashboard...
echo.
echo Keep this window open while using the demo.
echo.
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto error
exit /b 0
:noenv
echo Project environment not found.
echo Please contact the project team before the demo.
pause
exit /b 1
:error
echo.
echo AETHRIX stopped unexpectedly.
pause
exit /b 1
