@echo off
REM Script para ejecutar la aplicación con Docker en Windows

echo Construyendo imagen Docker...
docker build -t cs-gradecalculator .

if %ERRORLEVEL% NEQ 0 (
    echo Error al construir la imagen Docker
    pause
    exit /b 1
)

echo Ejecutando aplicación...
docker run -it --rm cs-gradecalculator

pause

