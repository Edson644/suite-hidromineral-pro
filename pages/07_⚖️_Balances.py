"""
Interfaz de Usuario - Módulo 7: Balances Metalúrgicos y Saldos
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from core.balances import calcular_balance_global

st.title("Módulo 7: Balances Metalúrgicos y Saldos Globales")

st.markdown("""
Este módulo consolida el **balance de masa integral** de la planta, desde el mineral alimentado en chancado 
hasta la producción final de cátodos de cobre, evaluando la recuperación global del circuito.
""")

col1, col2 = st.columns(2)

with col1:
    ton_alim = st.number_input("Tonelaje de Alimentación (t/h)", min_value=100.0, max_value=10000.0, value=2330.0, step=50.0, key="ton_bal")
    ley_cab = st.number_input("Ley de Cabeza Cu (%)", min_value=0.2, max_value=5.0, value=0.85, step=0.05, key="cab_bal")
    ley_col = st.number_input("Ley en Colas / Ripios (%)", min_value=0.01, max_value=1.0, value=0.10, step=0.01, key="col_bal")
with col2:
    rec_lix = st.number_input("Recuperación Lixiviación (%)", min_value=50.0, max_value=95.0, value=82.0, step=1.0, key="rec_lix_bal")
    ef_sx = st.number_input("Eficiencia Extracción SX (%)", min_value=85.0, max_value=99.9, value=96.5, step=0.5, key="ef_sx_bal")
    ef_ew = st.number_input("Eficiencia Corriente EW (%)", min_value=75.0, max_value=98.0, value=92.0, step=0.5, key="ef_ew_bal")

try:
    res = calcular_balance_global(
        tonelaje_alimentacion_tph=ton_alim,
        ley_cabeza_cu_pct=ley_cab,
        ley_colas_pct=ley_col,
        recuperacion_lix_pct=rec_lix,
        eficiencia_sx_pct=ef_sx,
        eficiencia_ew_pct=ef_ew
    )
    
    st.divider()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Recuperación Global", f"{res['Recuperacion_Global_pct']:,.2f} %".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Producción de Cátodos", f"{res['Produccion_Catodos_t_d']:,.2f} t/d".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi3.metric("Fino Alimentado", f"{res['Fino_Alimentado_tph']:,.2f} t/h Cu".replace(",", "X").replace(".", ",").replace("X", "."))

    if res['Recuperacion_Global_pct'] >= 75.0:
        st.success("BALANCE METALÚRGICO FAVORABLE: Alta eficiencia en la recuperación global del cobre fino.")
    else:
        st.warning("ATENCIÓN: Recuperación global bajo los objetivos de diseño. Revisar etapas de lixiviación y SX.")

    st.subheader("1. Distribución Masiva del Fino de Cobre en el Circuito")
    fino_prod_tph = res['Produccion_Catodos_t_d'] / 24.0
    fino_perd = res['Fino_Perdido_tph']
    
    df_balance = pd.DataFrame({
        "Destino": ["Cobre Producido (Cátodos)", "Cobre en Ripios / Pérdidas"],
        "Tonelaje Fino (t/h)": [fino_prod_tph, fino_perd]
    })
    
    fig_bal = px.pie(df_balance, names="Destino", values="Tonelaje Fino (t/h)", title="Destino del Cobre Fino Alimentado a Planta")
    st.plotly_chart(fig_bal, use_container_width=True, key="fig_pie_balance")

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - Procesando **{ton_alim} t/h** con una ley de cabeza de **{ley_cab}% Cu**, ingresan **{res['Fino_Alimentado_tph']} t/h** de cobre fino a la planta.
    - La recuperación global integrada (Lixiviación x SX x EW) alcanza un **{res['Recuperacion_Global_pct']:.2f}%**.
    - La producción comercial estimada es de **{res['Produccion_Catodos_t_d']:,.2f} toneladas diarias** de cátodos.
    """)

    st.subheader("3. Conclusiones y Recomendaciones Operativas")
    st.markdown("""
    - El balance masivo demuestra consistencia entre el mineral tratado y la oferta de solución rica (PLS).
    - Realizar muestreos estériles continuos en la escombrera para auditar las desviaciones de ley en colas.
    """)

except Exception as e:
    st.error(f"Error en el balance metalúrgico: {e}")

