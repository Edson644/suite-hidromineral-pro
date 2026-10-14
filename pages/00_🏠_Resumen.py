"""
Interfaz de Usuario - Resumen Ejecutivo Global
Suite Hidromineral Pro
"""

import streamlit as st
import pandas as pd

st.title("🏠 Resumen Ejecutivo Global - Planta Hidromineral")
st.markdown("""
Bienvenido al panel maestro de la **Suite Hidromineral Pro**. Este módulo consolida los KPIs globales 
de toda la cadena de valor del cobre y las prioridades de mejora por área.
""")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Tonelaje Tratado", "2.330 t/h")
kpi2.metric("Recuperación Global", "81,45 %")
kpi3.metric("Producción de Cátodos", "438,20 t/d")
kpi4.metric("VAN del Proyecto", "145,50 MUSD")

st.divider()
st.subheader("📊 Resumen de Rendimiento e Identificación de Cuellos de Botella (Pareto)")

df_resumen = pd.DataFrame({
    "Área Operativa": [
        "1. Chancado", "2. Aglomeración", "3. Lixiviación", 
        "4. SX", "5. Electro Winning", "6. Pulpas y Relaves", 
        "7. Balances", "8. Finanzas", "9. Pareto"
    ],
    "Principal Foco de Mejora (80/20)": [
        "Blindajes / Liners", "Humedad en Tambor", "Compactación de Lecho", 
        "Control de Cruds", "Cortocircuitos", "Desgaste en Codos", 
        "Control de Leyes", "Optimización OPEX", "Gestión de Detenciones"
    ],
    "Estado": ["Monitoreo", "Óptimo", "En Acción", "Estable", "Alto Rendimiento", "Seguro", "Confiable", "Rentable", "Activo"]
})

st.dataframe(df_resumen, use_container_width=True)

