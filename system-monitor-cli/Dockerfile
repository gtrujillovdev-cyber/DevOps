# ==============================================================================
# Dockerfile Multi-stage Optimizado para System Monitor CLI
# ==============================================================================

# Etapa Base con dependencias instaladas
FROM python:3.12-slim AS base

WORKDIR /app

# Instalar dependencias comunes del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del proyecto
COPY . .

# ------------------------------------------------------------------------------
# Etapa 1: Collector (Recolector de Métricas)
# ------------------------------------------------------------------------------
FROM base AS collector
CMD ["python", "monitor.py"]

# ------------------------------------------------------------------------------
# Etapa 2: Backend API (FastAPI)
# ------------------------------------------------------------------------------
FROM base AS api
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# ------------------------------------------------------------------------------
# Etapa 3: Frontend Dashboard (Streamlit)
# ------------------------------------------------------------------------------
FROM base AS dashboard
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
