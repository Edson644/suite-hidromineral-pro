import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Aglomeración y Pilas | Suite Hidromineral Pro", page_icon="🧪", layout="wide")

# --- ESTILOS CSS CONSISTENTES (Estética Oscura / Neón) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f12; color: #f0f2f5; }
    [data-testid="stSidebar"] { background-color: #12161c; border-right: 1px solid #1f2937; }
    .card { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Módulo 2: Preparación y Tambor de Aglomeración")
st.markdown("Control avanzado de humectación, adición de ácido sulfúrico, cinética de aglomerado y prevención de segregación en pilas.")

# --- SECCIÓN 1: VARIABLES OPERACIONALES DEL TAMBOR ---
st.markdown("### 📥 1. Parámetros Operacionales y Cinéticos del Tambor")
col1, col2, col3 = st.columns(3)

with col1:
    tph_mineral = st.number_input("Alimentación de Mineral Seco (TPH)", min_value=100.0, max_value=10000.0, value=1500.0, step=50.0)
    humedad_inicial = st.slider("Humedad Inicial del Mineral (%)", min_value=0.5, max_value=10.0, value=3.2, step=0.1)

with col2:
    humedad_objetivo = st.slider("Humedad Objetivo en Tambor (%)", min_value=4.0, max_value=15.0, value=8.5, step=0.1)
    dosificacion_acido = st.number_input("Dosificación de Ácido Concentrado (kg/t)", min_value=0.0, max_value=30.0, value=6.5, step=0.5)

with col3:
    vel_tambor = st.slider("Velocidad de Giro del Tambor (RPM)", min_value=4.0, max_value=20.0, value=9.5, step=0.5)
    concentracion_acido = st.slider("Pureza del Ácido de Aporte (%)", min_value=50.0, max_value=98.0, value=93.0, step=1.0)

# --- LÓGICA DE CÁLCULO TÉCNICO (BALANCE DE MASA Y AGUA) ---
agua_inicial_tph = tph_mineral * (humedad_inicial / 100.0)
agua_meta_tph = tph_mineral * (humedad_objetivo / 100.0)
delta_agua_tph = max(0.0, agua_meta_tph - agua_inicial_tph)

# Consumo horario de ácido y cálculo del caudal volumétrico de la solución de aspersión
acido_kg_h = tph_mineral * dosificacion_acido
caudal_solucion_l_min = ((delta_agua_tph * 1000.0) + (acido_kg_h / (concentracion_acido / 100.0))) / 60.0

# Índice de Calidad de Aglomeración (Evaluación de estabilidad del grumo)
indice_aglomeracion = max(40.0, min(99.5, 100.0 - abs(humedad_objetivo - 8.2) * 6.5))

st.markdown("---")
st.markdown("### 📊 2. Resultados del Balance Hidrometalúrgico y Calidad de Grumo")

c_res1, c_res2, c_res3, c_res4 = st.columns(4)

with c_res1:
    st.markdown(f"""
        <div class="card">
            <p style="color: #8b949e; font-size: 11px; margin: 0;">AGUA DE APORTE A SPRAY</p>
            <h3 style="color: #b6ff00; margin: 6px 0 0 0;">{delta_agua_tph * 1000:.1f} kg/h</h3>
            <p style="color: #3fb950; font-size: 10px; margin: 2px 0 0 0;">Requerimiento hídrico</p>
        </div>
    """, unsafe_allow_html=True)

with c_res2:
    st.markdown(f"""
        <div class="card">
            <p style="color: #8b949e; font-size: 11px; margin: 0;">CONSUMO TOTAL DE ÁCIDO</p>
            <h3 style="color: #ffffff; margin: 6px 0 0 0;">{acido_kg_h:.1f} kg/h</h3>
            <p style="color: #8b949e; font-size: 10px; margin: 2px 0 0 0;">Curado en tambor</p>
        </div>
    """, unsafe_allow_html=True)

with c_res3:
    st.markdown(f"""
        <div class="card">
            <p style="color: #8b949e; font-size: 11px; margin: 0;">CAUDAL SPRAY COMBINADO</p>
            <h3 style="color: #b6ff00; margin: 6px 0 0 0;">{caudal_solucion_l_min:.1f} L/min</h3>
            <p style="color: #3fb950; font-size: 10px; margin: 2px 0 0 0;">Flujo inyectado en boquillas</p>
        </div>
    """, unsafe_allow_html=True)

with c_res4:
    st.markdown(f"""
        <div class="card">
            <p style="color: #8b949e; font-size: 11px; margin: 0;">ESTABILIDAD DE GRUMOS</p>
            <h3 style="color: {'#3fb950' if indice_aglomeracion > 85 else '#f85149'}; margin: 6px 0 0 0;">{indice_aglomeracion:.1f}%</h3>
            <p style="color: #8b949e; font-size: 10px; margin: 2px 0 0 0;">Índice de aglomeración</p>
        </div>
    """, unsafe_allow_html=True)

st.info("💡 **Subetapa Crítica — Criterio Operativo:** Si el índice de aglomeración baja del 80%, se incrementa drásticamente el riesgo de segregación de finos en la pila, compactación del lecho y canalización preferencial de las soluciones de riego.")
