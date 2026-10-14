import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="M5 EW", layout="wide")
st.title("Módulo 5: Electroobtención (EW)")

st.markdown("""
Este módulo calcula la producción de cobre catódico y el consumo energético en la nave de electroobtención utilizando las **Leyes de Faraday**, 
evaluando el impacto de la densidad de corriente, la eficiencia de corriente y la configuración de las celdas.
""")

col1, col2 = st.columns(2)

with col1:
    densidad_corriente = st.number_input("Densidad de Corriente (A/m²)", min_value=100.0, max_value=500.0, value=300.0, step=10.0, key="ew_den")
    eficiencia_corriente = st.number_input("Eficiencia de Corriente (%)", min_value=50.0, max_value=100.0, value=92.0, step=1.0, key="ew_efi")
    voltaje_celda = st.number_input("Voltaje de Celda (V)", min_value=1.5, max_value=3.0, value=2.0, step=0.1, key="ew_vol")

with col2:
    num_celdas = st.number_input("Número de Celdas en Operación", min_value=1, max_value=1000, value=120, step=10, key="ew_cel")
    catodos_por_celda = st.number_input("Cátodos por Celda", min_value=10, max_value=100, value=60, step=1, key="ew_cat")
    area_catodo = st.number_input("Área Activa por Cátodo (m²)", min_value=1.0, max_value=3.0, value=2.0, step=0.1, key="ew_are")

# Equivalente electroquímico del cobre (Cu2+) = 1.185 g/Ah = 0.001185 kg/Ah
eq_cu = 0.001185 

try:
    # Cálculos Termodinámicos y Eléctricos
    corriente_total_celda = densidad_corriente * area_catodo * catodos_por_celda # Amperaje total por celda
    
    # Producción diaria (toneladas/día) usando Ley de Faraday
    prod_diaria_kg = corriente_total_celda * num_celdas * 24 * eq_cu * (eficiencia_corriente / 100.0)
    prod_diaria_t = prod_diaria_kg / 1000.0
    
    # Consumo Específico de Energía (kWh/kg Cu)
    consumo_energia = voltaje_celda / (eq_cu * (eficiencia_corriente / 100.0))

    st.divider()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Producción de Cátodos", f"{prod_diaria_t:,.2f} t/día".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Consumo Específico", f"{consumo_energia:,.2f} kWh/kg Cu".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi3.metric("Corriente por Celda", f"{corriente_total_celda:,.0f} A".replace(",", "X").replace(".", ",").replace("X", "."))

    st.subheader("1. Gráficos de Rendimiento y Sensibilidad Operativa")
    
    g1, g2 = st.columns(2)
    
    with g1:
        # Gráfico 1: Producción vs Densidad de corriente
        densidades = np.linspace(200, 400, 20)
        producciones = [(d * area_catodo * catodos_por_celda) * num_celdas * 24 * eq_cu * (eficiencia_corriente / 100.0) / 1000.0 for d in densidades]
        df_g1 = pd.DataFrame({"Densidad de Corriente (A/m²)": densidades, "Producción (t/día)": producciones})
        fig1 = px.line(df_g1, x="Densidad de Corriente (A/m²)", y="Producción (t/día)", title="Producción vs Densidad")
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        # Gráfico 2: Consumo Energético vs Eficiencia de Corriente
        eficiencias = np.linspace(80, 98, 20)
        consumos = [voltaje_celda / (eq_cu * (e / 100.0)) for e in eficiencias]
        df_g2 = pd.DataFrame({"Eficiencia de Corriente (%)": eficiencias, "Consumo (kWh/kg Cu)": consumos})
        fig2 = px.line(df_g2, x="Eficiencia de Corriente (%)", y="Consumo (kWh/kg Cu)", title="Consumo Energético vs Eficiencia")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - Operar a una densidad de **{densidad_corriente} A/m²** exige una inyección de **{corriente_total_celda:,.0f} Amperios** por celda.
    - Se proyecta una cosecha diaria de **{prod_diaria_t:.2f} toneladas** de cátodos grado A (99.99% Cu).
    - El gasto energético se sitúa en **{consumo_energia:.2f} kWh/kg Cu**, un valor netamente condicionado por la caída de tensión (voltaje) y la eficiencia del baño electrolítico.
    """)

    st.subheader("3. Recomendaciones Operativas")
    st.markdown("""
    - Realizar un mapeo térmico e infrarrojo constante para detectar cortocircuitos entre cátodos y ánodos que desplomen la eficiencia.
    - Mantener la concentración de reactivos niveladores (como el guar) y controlar el arrastre orgánico para garantizar la calidad superficial del cátodo.
    - Controlar la temperatura del electrolito (ideal entre 40°C - 45°C) para reducir la resistencia iónica del fluido y optimizar el voltaje de celda.
    """)

except Exception as e:
    st.error(f"Error en los cálculos electrometalúrgicos: {e}")
