"""
Interfaz de Usuario - Módulo 6: Pulpas y Relaves
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from core.pulpas import calcular_sistema_bombeo_pulpa

st.title("Módulo 6: Transporte de Pulpas y Relaves")

st.markdown("""
Este módulo calcula la **hidráulica de tuberías** para pulpas mineras, evaluando la gravedad específica, 
la velocidad operacional frente a la velocidad límite de depósito y la potencia requerida de bombeo.
""")

col1, col2 = st.columns(2)

with col1:
    m_solidos = st.number_input("Tonelaje de Sólidos (t/h)", min_value=50.0, max_value=5000.0, value=2330.0, step=50.0, key="m_sol")
    dens_sol = st.number_input("Densidad de Sólidos (t/m3)", min_value=2.0, max_value=5.0, value=2.68, step=0.05, key="dens_sol")
    cw = st.number_input("Concentración en Peso (Cw, %)", min_value=10.0, max_value=75.0, value=50.0, step=1.0, key="cw_in")
with col2:
    diam_pipe = st.number_input("Diámetro de Tubería (mm)", min_value=100.0, max_value=1200.0, value=500.0, step=25.0, key="diam_in")
    long_pipe = st.number_input("Longitud de Tubería (m)", min_value=10.0, max_value=20000.0, value=55.0, step=10.0, key="long_in")
    alt_est = st.number_input("Altura Estática (m)", min_value=0.0, max_value=500.0, value=18.4, step=1.0, key="alt_in")

try:
    res = calcular_sistema_bombeo_pulpa(
        m_solidos_tph=m_solidos,
        densidad_solidos=dens_sol,
        cw_porcentaje=cw,
        diametro_tuberia_mm=diam_pipe,
        longitud_tuberia_m=long_pipe,
        altura_estatica_m=alt_est,
        d85_mm=0.67
    )
    
    st.divider()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Gravedad Específica (Sm)", f"{res['Gravedad_Especifica_Sm']:,.3f}".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Velocidad Operacional", f"{res['Velocidad_Operativa_ms']:,.2f} m/s".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi3.metric("Potencia de Bombeo", f"{res['Potencia_Requerida_kW']:,.1f} kW".replace(",", "X").replace(".", ",").replace("X", "."))

    if "SEGURO" in res["Estado_Transporte"]:
        st.success(f"ESTADO HIDRÁULICO: {res['Estado_Transporte']}. (Velocidad límite: {res['Velocidad_Limite_Dep_ms']} m/s)")
    else:
        st.error(f"ALERTA OPERATIVA: {res['Estado_Transporte']}. Riesgo inminente de atollo en la línea.")

    st.subheader("1. Velocidad Operacional vs Diámetro de Tubería")
    diam_arr = np.linspace(300, 800, 40)
    vel_arr = []
    vel_lim_arr = []
    for d in diam_arr:
        tmp = calcular_sistema_bombeo_pulpa(m_solidos, dens_sol, cw, d, long_pipe, alt_est, 0.67)
        vel_arr.append(tmp["Velocidad_Operativa_ms"])
        vel_lim_arr.append(tmp["Velocidad_Limite_Dep_ms"])
        
    df_hidro = pd.DataFrame({
        "Diámetro (mm)": np.tile(diam_arr, 2),
        "Velocidad (m/s)": vel_arr + vel_lim_arr,
        "Tipo": ["Velocidad Operacional"]*40 + ["Velocidad Límite (Depósito)"]*40
    })
    fig_hidro = px.line(df_hidro, x="Diámetro (mm)", y="Velocidad (m/s)", color="Tipo", title="Criterio de Velocidad No-Sedimentante en Tubería")
    st.plotly_chart(fig_hidro, use_container_width=True, key="fig_hidro_pulpas")

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - La pulpa presenta una gravedad específica de **{res['Gravedad_Especifica_Sm']}** con un caudal volumétrico de **{res['Caudal_Volumetrico_m3h']:,.2f} m3/h**.
    - La velocidad en la tubería de {diam_pipe} mm es de **{res['Velocidad_Operativa_ms']} m/s**, superior al límite de depósito de **{res['Velocidad_Limite_Dep_ms']} 
m/s**.
    - La presión total en el sistema alcanza **{res['Presion_Sistema_bar']} bar** con una carga dinámica total de **{res['Altura_Total_Head_m']} m**.
    """)

    st.subheader("3. Conclusiones y Recomendaciones Operativas")
    st.markdown("""
    - Mantener el control estricto de la concentración en peso (Cw) para evitar aumentos desproporcionados de viscosidad aparente.
    - Monitorear el desgaste por abrasión en codos y tramos rectos de la línea de descarga de relaves.
    """)

except Exception as e:
    st.error(f"Error en los cálculos hidráulicos: {e}")

