"""
Interfaz de Usuario - Módulo 4: Extracción por Solvente (SX)
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from core.sx import calcular_sx

st.title("Módulo 4: Extracción por Solvente (SX) y McCabe-Thiele")

st.markdown("""
Este módulo calcula la **transferencia neta de cobre**, la recuperación en extracción y modela el 
**diagrama McCabe-Thiele** para determinar las etapas teóricas y reales de contacto orgánico-acuoso.
""")

col1, col2 = st.columns(2)

with col1:
    cu_pls = st.number_input("Cobre en PLS (g/L)", min_value=1.0, max_value=10.0, value=3.5, step=0.1, key="pls_in")
    cu_raff = st.number_input("Cobre en Refino (g/L)", min_value=0.01, max_value=1.0, value=0.15, step=0.01, key="raff_in")
with col2:
    oa_ratio = st.number_input("Relación Orgánico / Acuoso (O/A)", min_value=0.5, max_value=4.0, value=1.2, step=0.1, key="oa_in")
    carga_max = st.number_input("Carga Máxima Orgánico (g/L)", min_value=2.0, max_value=10.0, value=5.5, step=0.1, key="carga_in")

try:
    res = calcular_sx(cu_pls, cu_raff, oa_ratio, carga_max)
    trans = res["transferencia_neta_g_l"]
    rec = res["recuperacion_sx_pct"]
    et_t = res["etapas_teoricas"]
    et_r = res["etapas_reales"]

    st.divider()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Transferencia Neta", f"{trans:,.2f} g/L".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Recuperación SX", f"{rec:,.2f} %".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi3.metric("Etapas Reales / Teóricas", f"{et_r} (Teor: {et_t})")

    if rec >= 95.0:
        st.success("EXCELENTE EFICIENCIA: Alta tasa de extracción y agotamiento eficiente del PLS.")
    else:
        st.warning("ATENCIÓN OPERATIVA: Recuperación de SX bajo el estándar óptimo (>95%). Revisar relación O/A.")

    # Gráfico: Diagrama McCabe-Thiele simulado
    st.subheader("1. Diagrama McCabe-Thiele (Isoterma y Línea de Operación)")

    aq_vals = np.linspace(0.0, cu_pls, 50)
    # Isoterma de equilibrio Langmuir modificada
    org_equil = (carga_max * aq_vals) / (1.0 + 0.5 * aq_vals)
    # Línea de operación
    org_oper = cu_raff + (oa_ratio * (aq_vals - cu_raff))

    df_mccabe = pd.DataFrame({
        "Cobre Acuoso (g/L)": np.tile(aq_vals, 2),
        "Cobre Orgánico (g/L)": list(org_equil) + list(org_oper),
        "Curva": ["Isoterma de Equilibrio"]*50 + ["Línea de Operación"]*50
    })

    fig_mc = px.line(df_mccabe, x="Cobre Acuoso (g/L)", y="Cobre Orgánico (g/L)", color="Curva", title="Construcción McCabe-Thiele para Extracción de Cobre")
    st.plotly_chart(fig_mc, use_container_width=True, key="fig_mccabe_sx")

    st.subheader("2. Análisis Técnico")
    st.markdown(f"""
    - La solución PLS con **{cu_pls} g/L** de Cu es despojada hasta **{cu_raff} g/L** en el refino, logrando una transferencia neta de **{trans:.2f} g/L**.
    - El número de etapas reales estimadas es **{et_r}**, operando con una relación O/A de **{oa_ratio}**.
    """)

    st.subheader("3. Conclusiones y Recomendaciones Operativas")
    st.markdown("""
    - Controlar estrictamente el arrastre orgánico (entrampamiento) hacia el electrolito para evitar problemas de polarización en EW.
    - Mantener el pH de extracción en el rango óptimo para maximizar la selectividad del extractante (oxima).
    """)

except Exception as e:
    st.error(f"Error en los cálculos de SX: {e}")

