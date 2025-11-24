#!/bin/bash
# Script para ejecutar la aplicación con Docker

echo "Construyendo imagen Docker..."
docker build -t cs-gradecalculator .

echo "Ejecutando aplicación..."
docker run -it --rm cs-gradecalculator

