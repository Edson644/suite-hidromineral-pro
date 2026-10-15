import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Módulo 6: Pulpas y Reología | Suite Hidromineral", page_icon="📈", layout="wide")

st.title("📈 Módulo 6: Pulpas, Reología y Transporte de Sedimentos")
st.markdown("Control de concentración volumétrica, viscosidad, tensión de fluencia, velocidad límite de depósito y regímenes de flujo.")

# --- ENTRADAS OPERACIONALES ---
st.markdown("### 📥 Parámetros Físico-Químicos de la Pulpa")
col1, col2 = st.columns(2)

with col1:
    cp = st.number_input("Concentración en Peso (Cp %)", value=65.0, step=1.0)
    d50 = st.number_input("Tamaño de Partícula D50 (µm)", value=75.0, step=5.0)
    sg_solido = st.number_input("Gravedad Específica del Sólido (SG)", value=2.72, step=0.01)

with col2:
    diametro_tuberia = st.number_input("Diámetro de la Tubería (pulgadas)", value=10.0, step=1.0)
    velocidad_operacion = st.number_input("Velocidad Actual en Línea (m/s)", value=2.2, step=0.1)
    viscosidad_vehiculo = st.number_input("Viscosidad del Fluido Portador (cP)", value=1.0, step=0.1)

# Cálculos reológicos y de velocidad límite (Modelo de Durand / Wasp simplificado)
cv = (cp / sg_solido) / ((cp / sg_solido) + ((100 - cp) / 1.0)) * 100  # Concentración volumétrica aprox
# Estimación empírica de la velocidad límite de depositación (Velocidad Crítica Vc)
d_m = diametro_tuberia * 0.0254 # convertir a metros
vc_limite = 1.34 * (2 * 9.81 * d_m * (sg_solido - 1)) ** 0.5 * (cv / 100) ** 0.17
if vc_limite < 1.2: vc_limite = 1.2

st.markdown("---")
st.markdown("### 📊 Resultados y Balances Reológicos")
m1, m2, m3 = st.columns(3)
m1.metric("Concentración Volumétrica (Cv)", f"{cv:.1f}%")
m2.metric("Velocidad Límite de Depósito (Vc)", f"{vc_limite:.2f} m/s")
m3.metric("Margen Operativo (V_op - Vc)", f"{velocidad_operacion - vc_limite:+.2f} m/s")

st.markdown("---")

# --- GRÁFICOS TÉCNICOS DE INGENIERÍA ---
st.markdown("### 📈 Análisis Visual e Ingeniería de Transporte")

# Gráfico 1: Pérdida de Carga y Regímenes de Flujo (Curva de los Tres Estados / Velocidad Límite)
st.markdown("#### 1. Curva de Pérdida de Carga y Velocidad Límite de Depósito")

# Generar rango de velocidades para la curva característica de pulpas
v_range = np.linspace(0.5, 4.5, 50)
# Modelo de pérdida de carga hidráulica (fluidos no newtonianos / sedimentables)
# Zona 1: Lecho móvil / Depositación (izq de Vc), Zona 2: Suspensión Heterogénea, Zona 3: Suspensión Homogénea (der)
perdida_carga = 0.05 * (v_range ** -1.8) * (cv / 50) + 0.03 * (v_range ** 1.8)

fig_transporte = go.Figure()

fig_transporte.add_trace(go.Scatter(
    x=v_range, y=perdida_carga,
    mode='lines',
    name='Pérdida de Carga (It/m)',
    line=dict(color='#00e5ff', width=3)
))

# Línea vertical de la velocidad límite de depósito
fig_transporte.add_vline(
    x=vc_limite, line_dash="dash", line_color="#ff9100",
    annotation_text=f"Velocidad Límite (Vc = {vc_limite:.2f} m/s)", annotation_position="top right"
)

# Línea de velocidad de operación actual
fig_transporte.add_vline(
    x=velocidad_operacion, line_dash="solid", line_color="#b6ff00",
    annotation_text=f"Operación ({velocidad_operacion} m/s)", annotation_position="top left"
)

fig_transporte.update_layout(
    title="Curva Operativa y Transición de Regímenes (Velocidad Límite)",
    xaxis_title="Velocidad de Pulpa en Tubería (m/s)",
    yaxis_title="Pérdida de Carga (m.c.a. / m)",
    plot_bgcolor="#161b22", paper_bgcolor="#0b0f12", font_color="#f0f2f5",
    xaxis=dict(showgrid=True, gridcolor="#30363d"),
    yaxis=dict(showgrid=True, gridcolor="#30363d"),
    height=420,
    legend=dict(x=0.05, y=0.92)
)
st.plotly_chart(fig_transporte, use_container_width=True)

st.markdown("---")

# --- ANÁLISIS TÉCNICO Y CONCLUSIONES ---
st.markdown("### 2. Análisis Técnico")
st.markdown(f"""
- El cálculo estima una **velocidad límite de depositación de {vc_limite:.2f} m/s** para una tubería de {diametro_tuberia} pulgadas con un Cp de {cp}%.
- Con la velocidad de operación actual de **{velocidad_operacion} m/s**, el sistema se encuentra {'operando en régimen seguro por encima del límite crítico de sedimento' if velocidad_operacion >= vc_limite else 'EN ZONA DE RIESGO DE ATASCAMIENTO por debajo de la velocidad crítica'}.
""")

st.markdown("### 3. Conclusiones y Recomendaciones Operativas")
st.markdown("""
- **Zonas de Estado Operativo**: El gráfico de fricción evidencia las tres zonas críticas (flujo con lecho móvil a bajas velocidades, transición heterogénea y suspensión homogénea a altas velocidades).
- Se recomienda mantener la velocidad de bombeo al menos un 15% por encima de la velocidad límite calculada para evitar asentamientos imprevistos en tramos horizontales de la cañería.
""")
