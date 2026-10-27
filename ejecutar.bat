@echo off
rem ======================================================================
rem  Proyecto IF0012 - Algebra Lineal: inicia la aplicacion web local.
rem  La primera vez crea el entorno virtual .venv e instala dependencias.
rem ======================================================================
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto iniciar

echo Creando el entorno virtual (solo la primera vez)...
py -3 -m venv .venv >nul 2>&1
if not exist ".venv\Scripts\python.exe" python -m venv .venv
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [ERROR] No se encontro Python 3.11 o superior.
    echo Instale Python desde https://www.python.org/downloads/ y vuelva a intentarlo.
    pause
    exit /b 1
)
echo Instalando dependencias (requiere internet solo esta vez)...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudieron instalar las dependencias. Revise la conexion a internet.
    pause
    exit /b 1
)

:iniciar
echo.
echo Iniciando la aplicacion en http://localhost:8501
echo Para detenerla, cierre esta ventana o pulse Ctrl+C.
echo.
if "%IF0012_SIN_NAVEGADOR%"=="" start "" cmd /c "timeout /t 5 /nobreak >nul & start http://localhost:8501"
".venv\Scripts\python.exe" -m streamlit run app.py
pause
