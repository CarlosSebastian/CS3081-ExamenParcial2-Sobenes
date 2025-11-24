@echo off
REM Script completo para ejecutar tests y análisis de SonarQube usando solo Docker
REM Este script usa el contenedor oficial de sonar-scanner de Docker

setlocal enabledelayedexpansion

echo ==========================================
echo CS-GradeCalculator - Análisis SonarQube
echo Usando contenedores Docker
echo ==========================================
echo.

REM Configuración
set SONAR_PROJECT_KEY=Backend-Student-50
set SONAR_TOKEN=sqp_2b86c360d3c189e6b23577268e0a56685549b726
if "%SONAR_HOST_URL%"=="" set SONAR_HOST_URL=http://sonarqube.utec.edu.pe:9000

REM Verificar que Docker está disponible
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Paso 1: Construir imagen si no existe
echo Paso 1: Verificando imagen Docker...
docker image inspect cs-gradecalculator >nul 2>&1
if errorlevel 1 (
    echo Construyendo imagen Docker...
    docker build -t cs-gradecalculator .
    if errorlevel 1 (
        echo Error: No se pudo construir la imagen Docker
        pause
        exit /b 1
    )
)

REM Paso 2: Ejecutar tests con cobertura
echo.
echo Paso 2: Ejecutando tests con cobertura...
docker run --rm ^
    -v "%cd%/src:/app/src" ^
    -v "%cd%/tests:/app/tests" ^
    -v "%cd%:/app/workspace" ^
    -w /app/workspace ^
    cs-gradecalculator ^
    python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-report=term-missing

if errorlevel 1 (
    echo Error: Los tests fallaron
    pause
    exit /b 1
)

echo.
echo Tests completados exitosamente
echo.

REM Paso 3: Ejecutar análisis de SonarQube usando contenedor oficial
echo Paso 3: Ejecutando análisis de SonarQube...
echo Usando contenedor: sonarsource/sonar-scanner-cli
echo.

docker run --rm ^
    -v "%cd%:/usr/src" ^
    -w /usr/src ^
    sonarsource/sonar-scanner-cli ^
    -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^
    -Dsonar.sources=src ^
    -Dsonar.tests=tests ^
    -Dsonar.python.coverage.reportPaths=coverage.xml ^
    -Dsonar.host.url=%SONAR_HOST_URL% ^
    -Dsonar.login=%SONAR_TOKEN%

if errorlevel 1 (
    echo.
    echo Error: El análisis de SonarQube falló
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Análisis completado exitosamente
echo Revisa los resultados en: %SONAR_HOST_URL%
echo Proyecto: %SONAR_PROJECT_KEY%
echo ==========================================
echo.

pause

