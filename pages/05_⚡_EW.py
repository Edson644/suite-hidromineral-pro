import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Módulo 5: Electrowinning (EW) | Suite Hidromineral", page_icon="⚡", layout="wide")

st.title("⚡ Módulo 5: Electroobtención (EW)")
st.markdown("Control de corriente, ley de Faraday, consumo energético específico, rendimiento de cátodos y sensibilidad operativa.")

# --- ENTRADAS OPERACIONALES ---
st.markdown("### 📥 Parámetros de Operación EW")
col1, col2 = st.columns(2)

with col1:
    current_density = st.number_input("Densidad de Corriente (A/m²)", value=320.0, step=10.0)
    cell_voltage = st.number_input("Voltaje por Celda (V)", value=2.15, step=0.05)
    num_celdas = st.number_input("Número de Celdas en Operación", value=60, step=1)

with col2:
    current_efficiency = st.slider("Eficiencia de Corriente (%)", 85.0, 98.0, 92.5, 0.5)
    area_catinica = st.number_input("Área Útil por Cátodo (m²)", value=1.45, step=0.05)
    catodos_por_celda = st.number_input("Cátodos por Celda", value=32, step=1)

# Cálculos metalúrgicos y energéticos según Ley de Faraday
# Equivalente electroquímico del cobre (g/A*h) = 1.186
prod_diaria_ton = (current_density * area_catinica * catodos_por_celda * num_celdas * current_efficiency * 1.186 * 24) / 1e6
consumo_energetico_kwh_ton = (cell_voltage * 24 * 1000) / (current_efficiency * 1.186 * 10)

st.markdown("---")
st.markdown("### 📊 Resultados y Balances Energéticos EW")
m1, m2, m3 = st.columns(3)
m1.metric("Producción Estimada (TPD)", f"{prod_diaria_ton:.2f} ton Cu/día")
m2.metric("Consumo Específico", f"{consumo_energetico_kwh_ton:.1f} kWh/ton Cu")
m3.metric("Eficiencia Farádica", f"{current_efficiency}%")

st.markdown("---")

# --- GRÁFICOS TÉCNICOS DE INGENIERÍA ---
st.markdown("### 📈 Análisis Visual e Ingeniería de Electroobtención")

# Gráfico 1: Rendimiento y Producción (TPD vs. Densidad de Corriente)
st.markdown("#### 1. Gráfico de Rendimiento: Producción Diaria vs. Densidad de Corriente")
ds_range = np.linspace(250, 400, 40)
prod_range = (ds_range * area_catinica * catodos_por_celda * num_celdas * current_efficiency * 1.186 * 24) / 1e6

fig_rend = go.Figure()
fig_rend.add_trace(go.Scatter(
    x=ds_range, y=prod_range,
    mode='lines+markers',
    name='Producción TPD',
    line=dict(color='#00e5ff', width=3),
    marker=dict(size=6)
))
fig_rend.add_trace(go.Scatter(
    x=[current_density], y=[prod_diaria_ton],
    mode='markers',
    name='Punto de Operación Actual',
    marker=dict(color='#b6ff00', size=14, symbol='diamond')
))
fig_rend.update_layout(
    title="Curva de Rendimiento Productivo en Nave EW",
    xaxis_title="Densidad de Corriente (A/m²)",
    yaxis_title="Producción (ton Cu / día)",
    plot_bgcolor="#161b22", paper_bgcolor="#0b0f12", font_color="#f0f2f5",
    xaxis=dict(showgrid=True, gridcolor="#30363d"),
    yaxis=dict(showgrid=True, gridcolor="#30363d"),
    height=400
)
st.plotly_chart(fig_rend, use_container_width=True)

st.markdown("---")

# Gráfico 2: Sensibilidad Operativa (Consumo Energético kWh/ton vs. Voltaje y Eficiencia)
st.markdown("#### 2. Gráfico de Sensibilidad Operativa: Consumo Específico vs. Voltaje de Celda")
voltage_range = np.linspace(1.8, 2.6, 40)
energetic_sens = (voltage_range * 24 * 1000) / (current_efficiency * 1.186 * 10)

fig_sens = go.Figure()
fig_sens.add_trace(go.Scatter(
    x=voltage_range, y=energetic_sens,
    mode='lines',
    name='Consumo Específico (kWh/ton)',
    line=dict(color='#ff9100', width=3)
))
fig_sens.add_trace(go.Scatter(
    x=[cell_voltage], y=[consumo_energetico_kwh_ton],
    mode='markers',
    name='Operación Actual',
    marker=dict(color='#b6ff00', size=14, symbol='star')
))
fig_sens.update_layout(
    title="Sensibilidad Energética ante Variaciones de Voltaje",
    xaxis_title="Voltaje de Celda (V)",
    yaxis_title="Consumo Energético (kWh/ton Cu)",
    plot_bgcolor="#161b22", paper_bgcolor="#0b0f12", font_color="#f0f2f5",
    xaxis=dict(showgrid=True, gridcolor="#30363d"),
    yaxis=dict(showgrid=True, gridcolor="#30363d"),
    height=400
)
st.plotly_chart(fig_sens, use_container_width=True)

st.markdown("---")

# --- ANÁLISIS TÉCNICO Y CONCLUSIONES ---
st.markdown("### 3. Análisis Técnico")
st.markdown(f"""
- Operando a una densidad de corriente de **{current_density} A/m²** y un voltaje de celda de **{cell_voltage} V**, la planta EW alcanza una tasa de producción estimada de **{prod_diaria_ton:.2f} TPD**.
- El consumo energético específico se sitúa en **{consumo_energetico_kwh_ton:.1f} kWh/ton**, reflejando el impacto directo de la eficiencia de corriente (**{current_efficiency}%**) sobre los costos operacionales de electroobtención.
""")

st.markdown("### 4. Conclusiones y Recomendaciones Operativas")
st.markdown("""
- Se recomienda mantener un control riguroso de aditivos (goma guar y cloruros) en el electrolito para prevenir la formación de nodulaciones y cortocircuitos en las celdas.
- Vigilar de cerca el estado de los contactos eléctricos y barras nodrizas para evitar aumentos innecesarios en la caída de potencial y el voltaje de celda.
""")
