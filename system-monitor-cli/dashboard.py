import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuración de página con diseño profesional y responsive
st.set_page_config(
    page_title="DevOps System Monitor",
    page_icon="🖥️",
    layout="wide"
)

# Definir la URL de la API mediante variable de entorno o fallback local
API_URL = "http://127.0.0.1:8000/metrics"

st.markdown("""
<style>
    /* Estilos personalizados para mejorar la estética */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #64748B;
        margin-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("🖥️ DevOps System Monitor Dashboard")
st.markdown("<p class='subtitle'>Visualización en tiempo real del rendimiento del sistema local</p>", unsafe_allow_html=True)

# Función para obtener las métricas de la API de forma segura
def fetch_data():
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener métricas de la API: Código de estado {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("⚠️ No se puede conectar con la API de FastAPI. Asegúrate de que la API de FastAPI está corriendo en http://127.0.0.1:8000")
        return []
    except Exception as e:
        st.error(f"⚠️ Ocurrió un error inesperado al conectar con la API: {e}")
        return []

# Usamos st.fragment para auto-refrescar los datos de manera eficiente
@st.fragment(run_every="3s")
def render_dashboard():
    data = fetch_data()
    
    if not data:
        st.info("Esperando datos del sistema... Asegúrate de que el recolector (monitor.py) y la API (api.py) estén corriendo.")
        return

    # Convertir datos a DataFrame
    df = pd.DataFrame(data)
    
    # Procesar Timestamps de forma segura
    df['datetime'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='datetime')
    
    # Obtener el último registro
    latest = df.iloc[-1]
    
    # Calcular métricas de velocidad de Red en KB/s
    net_sent_kbps = 0.0
    net_recv_kbps = 0.0
    if len(df) > 1:
        p_row = df.iloc[-2]
        l_row = df.iloc[-1]
        
        # Calcular delta de tiempo en segundos
        t_delta = (l_row['datetime'] - p_row['datetime']).total_seconds()
        
        if t_delta > 0:
            # Obtener bytes desde los diccionarios anidados
            try:
                # Comprobar si network es un dict o una cadena JSON
                l_net = l_row['network']
                p_net = p_row['network']
                if isinstance(l_net, dict) and isinstance(p_net, dict):
                    sent_diff = l_net['bytes_sent'] - p_net['bytes_sent']
                    recv_diff = l_net['bytes_recv'] - p_net['bytes_recv']
                    
                    if sent_diff >= 0:
                        net_sent_kbps = (sent_diff / 1024) / t_delta
                    if recv_diff >= 0:
                        net_recv_kbps = (recv_diff / 1024) / t_delta
            except Exception:
                pass

    # Layout de Métricas Clave
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="💻 Uso de CPU", value=f"{latest['cpu']:.1f}%")
        
    with col2:
        st.metric(label="🧠 Uso de RAM", value=f"{latest['ram']:.1f}%")
        
    with col3:
        st.metric(label="💾 Uso de Disco", value=f"{latest['disk']:.1f}%")
        
    with col4:
        st.metric(
            label="🌐 Red (Subida / Bajada)",
            value=f"{net_sent_kbps:.1f} KB/s / {net_recv_kbps:.1f} KB/s"
        )
        
    st.markdown("---")
    
    # Gráficos Históricos y Procesos
    col_chart1, col_chart2 = st.columns(2)
    
    # Preparar el dataframe para gráficos (limitando a los últimos 50 registros para legibilidad)
    chart_df = df.tail(50).copy()
    chart_df['Hora'] = chart_df['datetime'].dt.strftime('%H:%M:%S')
    chart_df = chart_df.set_index('Hora')
    
    with col_chart1:
        st.subheader("📈 Histórico de Uso de Recursos (%)")
        st.line_chart(chart_df[['cpu', 'ram', 'disk']])
        
    with col_chart2:
        st.subheader("📋 Top Procesos (Consumo de CPU)")
        top_proc_list = latest.get('top_processes')
        if isinstance(top_proc_list, list) and len(top_proc_list) > 0:
            proc_df = pd.DataFrame(top_proc_list)
            # Reordenar y renombrar columnas si existen
            expected_cols = {'pid', 'name', 'cpu_percent'}
            if expected_cols.issubset(proc_df.columns):
                proc_df = proc_df[['pid', 'name', 'cpu_percent']]
                proc_df.columns = ['PID', 'Nombre del Proceso', 'CPU %']
                st.dataframe(proc_df, use_container_width=True, hide_index=True)
            else:
                st.dataframe(proc_df, use_container_width=True)
        else:
            st.write("No hay información de procesos disponible.")

# Ejecutar el renderizado
render_dashboard()
