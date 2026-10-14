"""
Interfaz de Usuario - Módulo 8: Evaluación Financiera (CAPEX, OPEX, VAN y TIR)
Suite Hidromineral Pro
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from core.finanzas import calcular_evaluacion_financiera

st.title("Módulo 8: Evaluación Financiera (CAPEX, OPEX, VAN y TIR)")

st.markdown("""
Este módulo evalúa la viabilidad económica del proyecto minero, integrando la inversión inicial (CAPEX), los costos operacionales (OPEX), 
el flujo de caja descontado, el Valor Actual Neto (VAN) y la Tasa Interna de Retorno (TIR).
""")

col1, col2 = st.columns(2)

with col1:
    capex = st.number_input("Inversión Inicial CAPEX (MUSD)", min_value=1.0, max_value=1000.0, value=120.0, step=5.0, key="fin_capex")
    prod_anual = st.number_input("Producción Anual de Cátodos (t/año)", min_value=1000.0, max_value=200000.0, value=18500.0, step=500.0, key="fin_prod")
    precio_cu = st.number_input("Precio del Cobre (USD/lb)", min_value=1.0, max_value=10.0, value=3.85, step=0.05, key="fin_prec")

with col2:
    opex_unit = st.number_input("Costo Operacional OPEX (USD/lb)", min_value=0.5, max_value=5.0, value=2.20, step=0.05, key="fin_opex")
    tasa_desc = st.number_input("Tasa de Descuento WACC (%)", min_value=1.0, max_value=25.0, value=10.0, step=0.5, key="fin_tasa")
    vida_util = st.number_input("Vida Útil del Proyecto (Años)", min_value=1, max_value=50, value=10, step=1, key="fin_vida")

try:
    # Llamada sincronizada con el core financiero
    res = calcular_evaluacion_financiera(
        capex_inicial=capex * 1000000.0,  # Convertido a USD totales
        produccion_anual_t=prod_anual,
        precio_cobre_lb=precio_cu,
        opex_unitario_kwh_t=opex_unit,
        tasa_descuento=tasa_desc,
        anos_proyeccion=int(vida_util)
    )

    st.divider()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("VAN del Proyecto", f"${res['VAN']:,.0f} USD".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("TIR Estimada", f"{res['TIR']}%")
    kpi3.metric("Payback Simple", f"{res['Payback']} Años")

    if res['VAN'] > 0:
        st.success("EVALUACIÓN ECONÓMICA RENTABLE: El Valor Actual Neto (VAN) es positivo, lo que indica que el proyecto genera valor por sobre la tasa de descuento exigida.")
    else:
        st.error("ALERTA FINANCIERA: El proyecto presenta un VAN negativo bajo las condiciones de costos y precios ingresados.")

    st.subheader("1. Proyección de Flujos de Caja Acumulados")
    
    anos_eje = list(range(len(res['Flujos'])))
    df_flujos = pd.DataFrame({
        "Año": anos_eje,
        "Flujo de Caja (USD)": res['Flujos']
    })
    
    fig = px.bar(df_flujos, x="Año", y="Flujo de Caja (USD)", title="Flujo de Caja Anual del Proyecto Minero")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("2. Análisis Técnico y Económico")
    st.markdown(f"""
    - Con una inversión inicial de **{capex} MUSD** y un precio de cobre de **${precio_cu} USD/lb**, el proyecto muestra capacidad de generación de caja.
    - El EBITDA anual estimado se sitúa en un rango competitivo frente a operaciones de mediana minería.
    - El periodo de recuperación de la inversión (Payback) se calcula en **{res['Payback']} años**.
    """)

    st.subheader("3. Recomendaciones Financieras")
    st.markdown("""
    - Monitorear de cerca las fluctuaciones del precio internacional del cobre para mitigar riesgos de volatilidad en los ingresos.
    - Optimizar los consumos unitarios de energía y reactivos químicos para mantener el OPEX bajo control.
    """)

except Exception as e:
    st.error(f"Error en la evaluación financiera: {e}")
