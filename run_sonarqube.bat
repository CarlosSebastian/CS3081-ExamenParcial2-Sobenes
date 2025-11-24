@echo off
REM Script para ejecutar análisis de SonarQube en Windows
REM Backend-Student-50

REM Configuración
set SONAR_PROJECT_KEY=Backend-Student-50
set SONAR_TOKEN=sqp_2b86c360d3c189e6b23577268e0a56685549b726
if "%SONAR_HOST_URL%"=="" set SONAR_HOST_URL=http://sonarqube.utec.edu.pe:9000

REM Ejecutar tests con cobertura primero
echo Ejecutando tests con cobertura...
pytest --cov=src --cov-report=xml --cov-report=html

REM Ejecutar SonarQube Scanner
echo Ejecutando análisis de SonarQube...
sonar-scanner ^
  -Dsonar.projectKey=%SONAR_PROJECT_KEY% ^
  -Dsonar.sources=src ^
  -Dsonar.tests=tests ^
  -Dsonar.python.coverage.reportPaths=coverage.xml ^
  -Dsonar.host.url=%SONAR_HOST_URL% ^
  -Dsonar.login=%SONAR_TOKEN%

echo Análisis completado. Revisa los resultados en SonarQube.
pause

