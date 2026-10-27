@echo off
rem Ejecuta todas las pruebas automaticas del proyecto IF0012.
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Primero ejecute ejecutar.bat para crear el entorno virtual.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m unittest -v
pause
