#!/bin/bash
# Script completo para ejecutar tests y análisis de SonarQube usando solo Docker
# Este script usa el contenedor oficial de sonar-scanner de Docker

set -e

echo "=========================================="
echo "CS-GradeCalculator - Análisis SonarQube"
echo "Usando contenedores Docker"
echo "=========================================="
echo ""

# Configuración
SONAR_PROJECT_KEY="Backend-Student-50"
SONAR_TOKEN="sqp_2b86c360d3c189e6b23577268e0a56685549b726"
SONAR_HOST_URL="${SONAR_HOST_URL:-http://sonarqube.utec.edu.pe:9000}"

# Verificar que Docker está disponible
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado o no está en el PATH"
    exit 1
fi

# Paso 1: Construir imagen si no existe
echo "Paso 1: Verificando imagen Docker..."
if ! docker image inspect cs-gradecalculator >/dev/null 2>&1; then
    echo "Construyendo imagen Docker..."
    docker build -t cs-gradecalculator .
fi

# Paso 2: Ejecutar tests con cobertura
echo ""
echo "Paso 2: Ejecutando tests con cobertura..."
docker run --rm \
    -v "$(pwd)/src:/app/src" \
    -v "$(pwd)/tests:/app/tests" \
    -v "$(pwd):/app/workspace" \
    -w /app/workspace \
    cs-gradecalculator \
    python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-report=term-missing

if [ $? -ne 0 ]; then
    echo "Error: Los tests fallaron"
    exit 1
fi

echo ""
echo "Tests completados exitosamente"
echo ""

# Paso 3: Ejecutar análisis de SonarQube usando contenedor oficial
echo "Paso 3: Ejecutando análisis de SonarQube..."
echo "Usando contenedor: sonarsource/sonar-scanner-cli"

docker run --rm \
    -v "$(pwd):/usr/src" \
    -w /usr/src \
    sonarsource/sonar-scanner-cli \
    -Dsonar.projectKey="${SONAR_PROJECT_KEY}" \
    -Dsonar.sources=src \
    -Dsonar.tests=tests \
    -Dsonar.python.coverage.reportPaths=coverage.xml \
    -Dsonar.host.url="${SONAR_HOST_URL}" \
    -Dsonar.login="${SONAR_TOKEN}"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Análisis completado exitosamente"
    echo "Revisa los resultados en: ${SONAR_HOST_URL}"
    echo "Proyecto: ${SONAR_PROJECT_KEY}"
    echo "=========================================="
else
    echo ""
    echo "Error: El análisis de SonarQube falló"
    exit 1
fi

