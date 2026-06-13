# ==============================================================================
# Makefile para automatización de comandos del System Monitor CLI
# ==============================================================================

.PHONY: dev clean install help

# Comando por defecto
help:
	@echo "Comandos disponibles:"
	@echo "  make dev      - Inicia todos los servicios localmente en paralelo"
	@echo "  make clean    - Elimina archivos temporales de Python y logs locales"
	@echo "  make install  - Instala dependencias desde requirements.txt"

# Iniciar entorno de desarrollo local
dev:
	@chmod +x start.sh
	@./start.sh

# Limpieza de archivos generados por la app
clean:
	@echo "🧹 Limpiando archivos temporales y logs..."
	@rm -f logs/*.log
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✨ Limpieza completada."

# Instalación rápida de dependencias
install:
	@echo "📦 Instalando dependencias..."
	@pip install -r requirements.txt
