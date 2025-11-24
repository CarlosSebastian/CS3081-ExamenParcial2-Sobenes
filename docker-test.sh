#!/bin/bash
# Script para ejecutar tests con Docker

echo "Verificando imagen Docker..."
if ! docker image inspect cs-gradecalculator >/dev/null 2>&1; then
    echo "Construyendo imagen Docker..."
    docker build -t cs-gradecalculator .
fi

echo "Ejecutando tests con cobertura..."
docker run --rm \
    -v "$(pwd)/src:/app/src" \
    -v "$(pwd)/tests:/app/tests" \
    -v "$(pwd)/reports:/app/reports" \
    cs-gradecalculator \
    python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-report=term-missing

echo ""
echo "Tests completados. Reportes en ./reports"

