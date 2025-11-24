@echo off
REM Script para ejecutar tests con Docker en Windows

echo Verificando imagen Docker...
docker image inspect cs-gradecalculator >nul 2>&1
if errorlevel 1 (
    echo Construyendo imagen Docker...
    docker build -t cs-gradecalculator .
    if errorlevel 1 (
        echo Error al construir la imagen Docker
        pause
        exit /b 1
    )
)

echo Ejecutando tests con cobertura...
docker run --rm ^
    -v "%cd%/src:/app/src" ^
    -v "%cd%/tests:/app/tests" ^
    -v "%cd%/reports:/app/reports" ^
    cs-gradecalculator ^
    python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-report=term-missing

echo.
echo Tests completados. Reportes en .\reports
pause

