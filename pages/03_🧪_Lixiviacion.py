"""
Interfaz de Usuario - Módulo 3: Lixiviación y Nanoburbujas
Suite Hidromineral Pro
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from core.lixiviacion import calcular_cinetica_paño, simular_90_panos

st.title("Módulo 3: Lixiviación en Pilas y Nanoburbujas")

st.markdown("""
Este módulo implementa el **motor cinético de primer orden modificado** para la gestión de los 90 paños, 
incorporando tecnología de nanoburbujas para incrementar la recuperación metalúrgica y reducir el consumo de ácido.
""")

col1, col2 = st.columns(2)

with col1:
    tasa_riego = st.number_input("Tasa de Riego (L/h/m²)", min_value=5.0, max_value=25.0, value=10.0, step=0.5, key="tasa_riego_input")
    r_max = st.number_input("Recuperación Máxima Teórica (Rmax, %)", min_value=50.0, max_value=95.0, value=85.0, step=1.0, key="rmax_input")
with col2:
    dias_sim = st.slider("Días de Operación / Antigüedad de Ciclo", min_value=10, max_value=90, value=45, key="dias_slider")
    nanoburbujas = st.toggle("Activar Inyección de Nanoburbujas (+6% Rec. / -6% Ácido)", value=False, key="nano_toggle")

try:
    conv = calcular_cinetica_paño(float(dias_sim), r_max=r_max, tasa_riego=tasa_riego, nanoburbujas_activo=False)
    nano = calcular_cinetica_paño(float(dias_sim), r_max=r_max, tasa_riego=tasa_riego, nanoburbujas_activo=nanoburbujas)
    
    st.divider()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Recuperación Convencional", f"{conv['recuperacion_pct']:,.2f} %".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi2.metric("Recuperación con Nanoburbujas", f"{nano['recuperacion_pct']:,.2f} %".replace(",", "X").replace(".", ",").replace("X", "."))
    kpi3.metric("Ahorro de Ácido Estimado", f"{nano['ahorro_acido_pct']:,.1f} %".replace(",", "X").replace(".", ",").replace("X", "."))

    if nanoburbujas:
        st.success("TECNOLOGÍA NANOBURBUJAS ACTIVA: Mejora en cinética de mojabilidad y transferencia de oxígeno disuelto aplicada.")
    else:
        st.info("Operación bajo régimen cinético convencional estándar.")

    st.subheader("1. Curvas de Cinética: Convencional vs Nanoburbujas")
    dias_rango = np.linspace(1, 90, 90)
    rec_conv_arr = [calcular_cinetica_paño(float(d), r_max=r_max, tasa_riego=tasa_riego, nanoburbujas_activo=False)['recuperacion_pct'] for d in dias_rango]
    rec_nano_arr = [calcular_cinetica_paño(float(d), r_max=r_max, tasa_riego=tasa_riego, nanoburbujas_activo=True)['recuperacion_pct'] for d in dias_rango]
    
    df_curvas = pd.DataFrame({
        "Días": np.tile(dias_rango, 2),
        "Recuperación (%)": rec_conv_arr + rec_nano_arr,
        "Modelo": ["Convencional"]*90 + ["Con Nanoburbujas"]*90
    })
    fig_curvas = px.line(df_curvas, x="Días", y="Recuperación (%)", color="Modelo", title="Evolución de la Recuperación de Cobre en el Tiempo")
    st.plotly_chart(fig_curvas, use_container_width=True, key="fig_curvas_lix")

    st.subheader("2. Estado Actual de los 90 Paños en Pila")
    paños_df = pd.DataFrame(simular_90_panos(num_panos=90, dias_operacion=dias_sim, nanoburbujas_activo=nanoburbujas))
    fig_paños = px.bar(paños_df, x="pano", y="recuperacion_pct", color="estado", title="Distribución de Recuperación por Paño en Operación")
    st.plotly_chart(fig_paños, use_container_width=True, key="fig_panos_lix")

    st.subheader("3. Análisis Técnico")
    st.markdown(f"""
    - A los **{dias_sim} días** de ciclo, el sistema convencional alcanza una recuperación del **{conv['recuperacion_pct']:.2f}%**.
    - La incorporación de nanoburbujas eleva la eficiencia extractiva a **{nano['recuperacion_pct']:.2f}%**, optimizando la cinética de lixiviación en profundidad.
    """)

    st.subheader("4. Conclusiones y Recomendaciones Operativas")
    st.markdown("""
    - El desfase operativo de los 90 paños garantiza una producción constante de cátodos en la planta SX-EW.
    - Se recomienda mantener un monitoreo riguroso del potencial redox (Eh) y el pH en las soluciones arrojadas por los paños más antiguos.
    """)

except Exception as e:
    st.error(f"Error en el cálculo cinético: {e}")

