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
	@echo "  make test     - Ejecuta pruebas unitarias con pytest"

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
	@if [ -f ".venv/bin/pip" ]; then \
		.venv/bin/pip install -r requirements.txt; \
	else \
		pip3 install -r requirements.txt || pip install -r requirements.txt; \
	fi

# Ejecutar pruebas unitarias
test:
	@echo "🧪 Ejecutando pruebas unitarias con pytest..."
	@if [ -f ".venv/bin/pytest" ]; then \
		PYTHONPATH=. .venv/bin/pytest; \
	else \
		PYTHONPATH=. pytest; \
	fi

