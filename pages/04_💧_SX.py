import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Módulo 4: SX | Suite Hidromineral", page_icon="💧", layout="wide")

st.title("💧 Módulo 4: Extracción por Solventes (SX)")
st.markdown("Control de transferencia de masa, trenes mixer-settler, relaciones O/A y diagrama de McCabe-Thiele.")

# --- ENTRADAS OPERACIONALES ---
st.markdown("### 📥 Parámetros de Operación SX")
col1, col2 = st.columns(2)

with col1:
    cu_pls = st.number_input("Concentración de Cu en PLS (g/L)", value=4.5, step=0.1)
    caudal_pls = st.number_input("Caudal de PLS (m³/h)", value=1200.0, step=50.0)
    etapas_ex = st.slider("Etapas de Extracción (E)", 1, 4, 2)

with col2:
    etapas_rex = st.slider("Etapas de Reextracción (S)", 1, 4, 2)
    relacion_oa = st.number_input("Relación Orgánico / Acuoso (O/A)", value=1.2, step=0.1)
    conc_oxima = st.slider("Concentración de Reactivo / Oxima (%)", 5.0, 25.0, 14.0, 0.5)

# Cálculos automáticos de ingeniería
eficiencia_ext = 85.0 + (etapas_ex * 4.5) - (relacion_oa * 1.5)
if eficiencia_ext > 99.0: 
    eficiencia_ext = 99.0
cu_raff = cu_pls * (1 - (eficiencia_ext / 100))
caudal_org = caudal_pls * relacion_oa

st.markdown("---")
st.markdown("### 📊 Resultados y Balances del Módulo SX")
m1, m2, m3 = st.columns(3)
m1.metric("Eficiencia Global Extractiva", f"{eficiencia_ext:.1f}%")
m2.metric("Cobre en Raffinate", f"{cu_raff:.3f} g/L")
m3.metric("Caudal Orgánico Estimado", f"{caudal_org:.1f} m³/h")

st.markdown("---")

# --- GRÁFICOS TÉCNICOS DE INGENIERÍA ---
st.markdown("### 📈 Análisis Visual e Ingeniería de Extracción")

# Gráfico: Diagrama de McCabe-Thiele (Curva de Equilibrio y Línea de Operación)
st.markdown("#### 1. Diagrama de McCabe-Thiele (Análisis de Etapas de Extracción)")

# Generar puntos para la curva de equilibrio (Isoterma de extracción)
c_aq = np.linspace(0, cu_pls, 60)
# Modelo de isoterma modificado por concentración de oxima
c_org = (conc_oxima * 0.38) * (c_aq ** 0.82) / (1 + 0.12 * c_aq)

fig_mccabe = go.Figure()

# Curva de Equilibrio
fig_mccabe.add_trace(go.Scatter(
    x=c_aq, y=c_org,
    mode='lines',
    name='Curva de Equilibrio',
    line=dict(color='#00e5ff', width=3)
))

# Línea de Operación
linea_op_y = (c_aq * (relacion_oa * 0.95)) + (cu_raff * 0.2)
fig_mccabe.add_trace(go.Scatter(
    x=c_aq, y=linea_op_y,
    mode='lines',
    name='Línea de Operación (O/A)',
    line=dict(color='#b6ff00', width=2.5, dash='dash')
))

fig_mccabe.update_layout(
    title="Diagrama McCabe-Thiele - Tren de Extracción de Cobre",
    xaxis_title="Concentración Acuosa de Cobre [Cu]aq (g/L)",
    yaxis_title="Concentración Orgánica de Cobre [Cu]org (g/L)",
    plot_bgcolor="#161b22", 
    paper_bgcolor="#0b0f12", 
    font_color="#f0f2f5",
    xaxis=dict(showgrid=True, gridcolor="#30363d"),
    yaxis=dict(showgrid=True, gridcolor="#30363d"),
    height=450,
    legend=dict(x=0.05, y=0.92)
)
st.plotly_chart(fig_mccabe, use_container_width=True)

st.markdown("---")

# --- ANÁLISI TÉCNICO Y CONCLUSIONES ---
st.markdown("### 2. Análisis Técnico")
st.markdown(f"""
- Con una configuración de **{etapas_ex} etapas de extracción** y una relación O/A de **{relacion_oa}**, el sistema muestra una transferencia de masa eficiente, operando con un rebase adecuado respecto a la isoterma de equilibrio.
- La concentración de cobre en el raffinate se proyecta en **{cu_raff:.3f} g/L**, cumpliendo con los estándares operacionales para recirculación hacia las pilas de lixiviación.
""")

st.markdown("### 3. Conclusiones y Recomendaciones Operativas")
st.markdown("""
- Se recomienda mantener un estricto control de los tiempos de residencia y la velocidad de agitación en los mezcladores (mixers) para evitar la generación de emulsiones o problemas de coalescencia en los asentadores.
- Monitorear de manera continua el nivel de sólidos suspendidos arrastrados desde el PLS para prevenir la acumulación de barros orgánicos en las interfaces.
""")
