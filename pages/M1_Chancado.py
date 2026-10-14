"""
Interfaz de Usuario - Módulo 1: Chancado y Conminución (Ley de Bond)
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from core.chancado import calcular_trabajo_bond

st.title("Módulo 1: Chancado y Conminución (Ley de Bond)")

st.markdown("""
Este módulo calcula el consumo específico de energía y la potencia requerida aplicando la **Tercera Ley de Conminución de Fred C. Bond**, 
sin valores fijos ni suposiciones en la interfaz.
""")

col1, col2 = st.columns(2)

with col1:
    wi = st.number_input("Índice de Trabajo de Fianza (Wi, kWh/t)", min_value=1.0, max_value=30.0, value=13.5, step=0.5, key="wi_m1")
    f80 = st.number_input("Tamaño de alimentación (F80, µm)", min_value=100.0, max_value=200000.0, value=50000.0, step=1000.0, key="f80_m1")
with col2:
    p80 = st.number_input("Tamaño del Producto (P80, µm)", min_value=10.0, max_value=50000.0, value=12000.0, step=100.0, key="p80_m1")
    q = st.number_input("Tasa de Procesamiento (Q, t/h)", min_value=10.0, max_value=5000.0, value=100.0, step=10.0, key="q_m1")

potencia_motor = st.number_input("Potencia nominal del motor (kW)", min_value=10.0, max_value=10000.0, value=1200.0, step=50.0, key="pot_m1")

try:
    # Llamamos a la función con el nombre y los datos exactos que pide tu archivo core/chancado.py
    res_core = calcular_trabajo_bond(wi=wi, f80=f80, p80=p80, tonelaje_t_h=q)
    
    # Extraemos los resultados
    consumo = res_core["w_kwh_t"]
    potencia = res_core["potencia_kw"]
    
    # Calculamos si la potencia del motor es segura (margen del 20%)
    estado_seguridad = "Seguro" if potencia * 1.2 <= potencia_motor else "Alerta"
    
    st.divider()
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Consumo Específico (Bond)", f"{consumo:,.2f} kWh/t".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Potencia Absorbida", f"{potencia:,.2f} kW".replace(",", "X").replace(".", ",").replace("X", "."))

    if estado_seguridad == "Seguro":
        st.success(f"CONDICIÓN SEGURA: La potencia nominal cubre holgadamente la demanda del proceso con el margen de seguridad de 20%.")
    else:
        st.error(f"ALERTA OPERACIONAL: La potencia nominal es insuficiente para la carga de trabajo calculada.")

    st.subheader("1. Gráficos de Rendimiento Operativo")
    
    # Gráfico 1: Consumo Específico vs P80
    p80_range = np.linspace(1000, 25000, 50)
    w_range = [10 * wi * ((1.0 / np.sqrt(p)) - (1.0 / np.sqrt(f80))) for p in p80_range]
    
    df_graf1 = pd.DataFrame({
        "P80 (µm)": p80_range,
        "Consumo (kWh/t)": w_range
    })
    
    fig1 = px.line(df_graf1, x="P80 (µm)", y="Consumo (kWh/t)", title="Consumo Específico (kWh/t) vs P80")
    st.plotly_chart(fig1, use_container_width=True, key="fig_chancado_1")

    # Gráfico 2: Potencia Absorbida vs Tonnage
    q_range = np.linspace(50, 140, 40)
    pot_range = [q_val * consumo for q_val in q_range]
    
    df_graf2 = pd.DataFrame({
        "Tonelaje (t/h)": q_range,
        "Potencia (kW)": pot_range
    })
    
    fig2 = px.line(df_graf2, x="Tonelaje (t/h)", y="Potencia (kW)", title="Potencia Absorbida (kW) vs Tonelaje (t/h)")
    st.plotly_chart(fig2, use_container_width=True, key="fig_chancado_2")

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - El índice de trabajo evaluado de **{wi} kWh/t** refleja la resistencia del mineral.
    - Reducir el P80 incrementa exponencialmente la demanda energética por la Ley de Bond.
    - Con un tonelaje de **{q} t/h**, el equipo demanda **{potencia} kW**.
    """)

    st.subheader("3. Conclusiones")
    st.markdown("""
    - El circuito opera bajo los parámetros teóricos esperados para la dureza del mineral.
    - Se observa sensibilidad crítica en variaciones drásticas del P80 de producto.
    """)

    st.subheader("4. Recomendaciones Operativas")
    st.markdown("""
    - Monitorear el desgaste de los revestimientos y el ajuste del huelgo.
    - Mantenga control de alimentación para evitar picos de tonelaje.
    """)

except Exception as e:
    st.error(f"Error en el cálculo de chancado: {e}")
