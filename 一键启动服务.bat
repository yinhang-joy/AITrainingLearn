@echo off
setlocal
chcp 65001 >nul
title AITraining Services
pushd "%~dp0"
if errorlevel 1 exit /b 1

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Project Python environment was not found.
    echo Create .venv and install requirements.txt first.
    popd
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -X utf8 "scripts\start_services.py" %*
set "service_exit=%errorlevel%"
popd
if not "%service_exit%"=="0" pause
exit /b %service_exit%
