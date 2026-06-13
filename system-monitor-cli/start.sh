#!/bin/bash

# ==============================================================================
# Script de inicio para desarrollo local de System Monitor CLI
# Levanta el recolector, la API y el Dashboard en paralelo y maneja su cierre.
# ==============================================================================

# Colores para salida en terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando entorno de desarrollo local...${NC}"

# Activar el entorno virtual si existe
if [ -d ".venv" ]; then
    echo -e "${CYAN}🔄 Activando entorno virtual (.venv)...${NC}"
    source .venv/bin/activate
else
    echo -e "${RED}⚠️ No se encontró la carpeta .venv. Asegúrate de tener las dependencias instaladas.${NC}"
fi

# Variables para almacenar los PIDs de los procesos
MONITOR_PID=""
API_PID=""
DASHBOARD_PID=""

# Función de limpieza al terminar (Ctrl+C)
cleanup() {
    echo -e "\n${RED}🛑 Deteniendo todos los servicios...${NC}"
    
    if [ -n "$MONITOR_PID" ]; then
        echo -e "${CYAN}Deteniendo Recolector (PID: $MONITOR_PID)...${NC}"
        kill $MONITOR_PID 2>/dev/null
    fi
    
    if [ -n "$API_PID" ]; then
        echo -e "${CYAN}Deteniendo API (PID: $API_PID)...${NC}"
        kill $API_PID 2>/dev/null
    fi
    
    if [ -n "$DASHBOARD_PID" ]; then
        echo -e "${CYAN}Deteniendo Dashboard (PID: $DASHBOARD_PID)...${NC}"
        kill $DASHBOARD_PID 2>/dev/null
    fi
    
    echo -e "${GREEN}✨ Servicios detenidos limpiamente.${NC}"
    exit 0
}

# Capturar señales de terminación (SIGINT = Ctrl+C, SIGTERM)
trap cleanup SIGINT SIGTERM

# 1. Iniciar Recolector
echo -e "${GREEN}🟢 1/3 Iniciando Recolector (monitor.py)...${NC}"
python monitor.py > /dev/null 2>&1 &
MONITOR_PID=$!

# 2. Iniciar API (FastAPI)
echo -e "${GREEN}🟢 2/3 Iniciando API (FastAPI)...${NC}"
python -m uvicorn api:app --port 8000 --log-level warning > /dev/null 2>&1 &
API_PID=$!

# Esperar un momento a que la API esté lista antes de lanzar el dashboard
sleep 1.5

# 3. Iniciar Dashboard (Streamlit)
echo -e "${GREEN}🟢 3/3 Iniciando Dashboard (Streamlit)...${NC}"
streamlit run dashboard.py --server.headless true --server.port 8501 > /dev/null 2>&1 &
DASHBOARD_PID=$!

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}✅ Todos los servicios están corriendo en segundo plano!${NC}"
echo -e "   - Recolector guardando en logs/system.log"
echo -e "   - API corriendo en http://127.0.0.1:8000"
echo -e "   - Dashboard activo en http://localhost:8501"
echo -e "${BLUE}====================================================${NC}"
echo -e "${CYAN}Presiona [Ctrl+C] para apagar todos los servicios de forma segura.${NC}"

# Mantener el script activo esperando el Ctrl+C
while true; do
    sleep 1
done
