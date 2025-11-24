# Dockerfile para CS-GradeCalculator
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY tests/ ./tests/
COPY pytest.ini .

# Crear directorio para reportes
RUN mkdir -p /app/reports

# Comando por defecto: ejecutar la aplicación
CMD ["python", "-m", "src.main"]

