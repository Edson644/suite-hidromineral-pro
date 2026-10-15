import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Suite Hidromineral Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Estética Oscura / Neón / Alta Gama) ---
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #0b0f12;
        color: #f0f2f5;
    }
    
    /* Personalización de la barra lateral nativa de páginas */
    [data-testid="stSidebar"] {
        background-color: #12161c;
        border-right: 1px solid #1f2937;
    }
    
    /* Tarjetas de métricas ejecutivas */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        border-color: #b6ff00;
    }
    
    /* Tipografía y títulos */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Alertas y contenedores de bienvenida */
    .welcome-box {
        background: linear-gradient(135deg, #161b22 0%, #1f2937 100%);
        border-left: 4px solid #b6ff00;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL ---
st.title("⚡ Suite Hidromineral Pro — Ingeniería y Procesos")
st.markdown("Plataforma avanzada de cálculo, simulación y control prescriptivo para operaciones hidrometalúrgicas.")

# Caja de bienvenida estilizada en lugar del texto plano anterior
st.markdown("""
    <div class="welcome-box">
        <h4 style="margin: 0 0 5px 0; color: #b6ff00;">Control Operativo Global Activo</h4>
        <p style="margin: 0; color: #a0aec0;">Selecciona un módulo en el menú lateral izquierdo (desde Resumen hasta Reportes) para acceder a los cálculos específicos de planta.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Indicadores Clave de Planta en Tiempo Real")

# --- TARJETAS DE MÉTRICAS EJECUTIVAS (Estilo Dashboard Gerencial) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; font-size: 12px; margin: 0; font-weight: bold;">PRODUCCIÓN TPD</p>
            <h3 style="color: #b6ff00; margin: 8px 0 0 0;">4,250 T</h3>
            <p style="color: #3fb950; font-size: 11px; margin: 4px 0 0 0;">▲ +3.4% vs meta diaria</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; font-size: 12px; margin: 0; font-weight: bold;">CUELLO DE BOTELLA</p>
            <h3 style="color: #f85149; margin: 8px 0 0 0;">SX - Etapa E2</h3>
            <p style="color: #8b949e; font-size: 11px; margin: 4px 0 0 0;">Impacto: $950 USD/hr</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; font-size: 12px; margin: 0; font-weight: bold;">RECUPERACIÓN GLOBAL</p>
            <h3 style="color: #b6ff00; margin: 8px 0 0 0;">88.2%</h3>
            <p style="color: #3fb950; font-size: 11px; margin: 4px 0 0 0;">▲ Óptimo operacional</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; font-size: 12px; margin: 0; font-weight: bold;">ESTADO DEL SISTEMA</p>
            <h3 style="color: #3fb950; margin: 8px 0 0 0;">ESTABLE</h3>
            <p style="color: #8b949e; font-size: 11px; margin: 4px 0 0 0;">0 alarmas críticas</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sección inferior informativa para los mandos altos y gerentes
col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.subheader("⚙️ Módulos de Proceso Disponibles")
    st.markdown("""
        * **Conminución y Chancado:** Evaluación de circuitos y harneros.
        * **Aglomeración y Lixiviación:** Control de humedad, ácido y ciclos en pilas.
        * **SX - EW:** Análisis de perfiles de extracción, reextracción y celdas.
        * **Pulpes y Balances:** Masas, leyes y distribuciones metalúrgicas.
    """)

with col_inf2:
    st.subheader("🎯 Enfoque Prescriptivo")
    st.info("Este software no solo almacena datos: evalúa desviaciones operacionales en tiempo real, calcula costos de oportunidad y asiste en la toma de decisiones gerenciales críticas.")
