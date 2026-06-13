# 🛠️ DevOps Projects Sandbox

Este repositorio es un espacio de aprendizaje y experimentación práctica donde construyo, empaqueto y despliego pequeños proyectos enfocados en la cultura **DevOps, Automatización, Observabilidad y Cloud**.

Cada subproyecto está diseñado para aplicar y dominar conceptos clave como la administración de sistemas Linux, desarrollo de APIs, contenerización, CI/CD, monitorización y despliegue continuo.

---

## 📁 Proyectos en el Repositorio

### 🖥️ [1. System Monitor CLI](./system-monitor-cli)
Una plataforma de monitorización en tiempo real para métricas de hardware del sistema local.
* **Tecnologías:** Python (`psutil`), FastAPI, Streamlit, Bash.
* **Características:**
  * Recolector en segundo plano que escribe logs estructurados en JSON.
  * API backend en FastAPI que sirve las últimas métricas.
  * Dashboard interactivo en Streamlit con auto-refresco eficiente (`st.fragment`).
  * Automatización local con `start.sh` y un `Makefile`.
* **Próximos Pasos:** Dockerización (Docker Compose), CI/CD, Despliegue en VPS y Observabilidad con Prometheus/Grafana.

---

## ⚙️ Tecnologías & Herramientas
* **Lenguajes:** Python, Shell Scripting (Bash/Zsh).
* **Contenerización:** Docker, Docker Compose (En progreso).
* **CI/CD:** GitHub Actions (En progreso).
* **Observabilidad:** Prometheus, Grafana (En progreso).
* **Infraestructura:** Servidores VPS Linux (En progreso).

---

## 👤 Autor
* **Gabriel Trujillo** - [GitHub](https://github.com/gtrujillovdev-cyber)
