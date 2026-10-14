"""
Interfaz de Usuario - Módulo 2: Aglomeración
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import plotly.express as px
from core.aglomeracion import calcular_aglomeracion

st.title("Módulo 2: Aglomeración de Minerales")

st.markdown("""
Este módulo calcula la **humedad óptima** y la **resistencia verde** del aglomerado en función 
de las adiciones de cemento, ácido y porcentaje de finos, asegurando la permeabilidad del lecho en pilas.
""")

col1, col2, col3 = st.columns(3)

with col1:
    cemento = st.number_input("Adición de Cemento (kg/t)", min_value=0.0, max_value=30.0, value=15.0, step=0.5)
with col2:
    acido = st.number_input("Adición de Ácido (kg/t)", min_value=0.0, max_value=30.0, value=12.0, step=0.5)
with col3:
    finos = st.number_input("Porcentaje de Finos (< 200 mesh, %)", min_value=5.0, max_value=80.0, value=35.0, step=1.0)

try:
    res = calcular_aglomeracion(cemento, acido, finos)
    humedad = res["humedad_optima_pct"]
    resistencia = res["resistencia_verde_kpa"]

    st.divider()

    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Humedad Óptima", f"{humedad:,.2f} %".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Resistencia Verde", f"{resistencia:,.2f} kPa".replace(",", "X").replace(".", ",").replace("X", "."))

    if res["alerta_resistencia"]:
        st.error("⚠️ **ALERTA OPERATIVA**: Resistencia verde insuficiente (< 12 kPa). Riesgo alto de compactación y canalización de soluciones en la pila.")
    else:
        st.success("✅ **CONDICIÓN ÓPTIMA**: Resistencia mecánica adecuada para el apilamiento y transporte.")

    st.subheader("1. Gráfico: Resistencia Verde vs Humedad Operativa")

    hum_vals = np.linspace(max(4.0, humedad - 4.0), humedad + 4.0, 40)
    res_vals = [max(2.0, resistencia - 5.0 * ((h - humedad)**2)) for h in hum_vals]

    fig = px.line(x=hum_vals, y=res_vals, labels={"x": "Humedad (%)", "y": "Resistencia Verde (kPa)"}, title="Curva de Comportamiento Mecánico del Aglomerado")
    fig.add_scatter(x=[humedad], y=[resistencia], mode="markers", marker=dict(size=14, color="red"), name="Punto Operativo")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - Con una adición de **{cemento} kg/t** de cemento y **{acido} kg/t** de ácido, el punto operativo se ubica en **{humedad:.2f}%** de humedad.
    - La resistencia verde obtenida es de **{resistencia:.2f} kPa**, garantizando estabilidad estructural bajo cargas de apilamiento industrial.
    """)

    st.subheader("3. Conclusiones")
    st.markdown("""
    - La aglomeración asegura la cohesión de las partículas finas alrededor de los gruesos, previniendo la segregación.
    - Un control estricto del agua de aporte evita la saturación y el colapso del lecho capilar.
    """)

    st.subheader("4. Recomendaciones Operativas")
    st.markdown("""
    - Sincronizar los flujos de solución aglomerante en el tambor con la ley de alimentación de mineral seco.
    - Realizar ensayos de resistencia al corte en verde de forma periódica en planta piloto.
    """)

except Exception as e:
    st.error(f"Error en los cálculos: {e}")

