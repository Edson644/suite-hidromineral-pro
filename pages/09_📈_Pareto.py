"""
Interfaz de Usuario - Módulo 9: Análisis de Pareto y Confiabilidad Operacional por Módulos
Suite Hidromineral Pro
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Módulo 9: Análisis de Pareto y Confiabilidad por Módulos")

st.markdown("""
Este módulo presenta el análisis de fallas y tiempos de detención (Ley de Pareto 80/20) para cada área crítica del proceso hidrometalúrgico, 
permitiendo enfocar los planes de mantenimiento y confiabilidad operacional en las causas vitales.
""")

# Selector de módulo para navegar entre los Paretos de cada área
modulo_seleccionado = st.selectbox(
    "Seleccione el Módulo Operativo a Analizar:",
    [
        "1. Chancado y Conminución",
        "2. Aglomeración",
        "3. Lixiviación en Pilas",
        "4. Extracción por Solvente (SX)",
        "5. Electroobtención (EW)",
        "6. Pulpas y Relaves",
        "7. Balances y Recuperación Global"
    ]
)

st.divider()

# Diccionario con los datos de Pareto específicos para cada módulo
datos_paretos = {
    "1. Chancado y Conminución": {
        "Fallas": ["Desgaste de Blindajes / Liners", "Atasco en Alimentador / Grizzly", "Falla Sistema Hidráulico", "Temperatura Alta en Cojinetes", "Corte de Energía Menor"],
        "Horas": [42.5, 26.0, 12.0, 6.5, 3.0]
    },
    "2. Aglomeración": {
        "Fallas": ["Variación de humedad en tambor", "Desgaste de paletas mezcladoras", "Colmatación de boquillas de ácido", "Segregación de finos en correa"],
        "Horas": [28.0, 21.0, 15.0, 8.0]
    },
    "3. Lixiviación en Pilas": {
        "Fallas": ["Canalización y compactación de lecho", "Obstrucción de goteros / Emisores", "Rotura de tuberías de solución madre", "Disminución de potencial redox (Eh)"],
        "Horas": [47.0, 29.0, 14.0, 10.0]
    },
    "4. Extracción por Solvente (SX)": {
        "Fallas": ["Formación de emulsiones / Cruds", "Arrastre orgánico hacia electrolito", "Descalibración de medidores de pH", "Falla en sellos de bombas centrífugas"],
        "Horas": [37.5, 25.0, 13.0, 5.0]
    },
    "5. Electroobtención (EW)": {
        "Fallas": ["Cortocircuitos ánodo-cátodo", "Contaminación orgánica en celdas", "Desgaste de contactos eléctricos", "Baja temperatura del electrolito"],
        "Horas": [45.0, 28.0, 13.0, 7.0]
    },
    "6. Pulpas y Relaves": {
        "Fallas": ["Abrasión y desgaste en codos de tubería", "Cavitación en impulsor de bomba", "Sedimentación en línea por baja velocidad", "Falla en instrumentación de densidad"],
        "Horas": [44.0, 29.0, 15.0, 4.0]
    },
    "7. Balances y Recuperación Global": {
        "Fallas": ["Desviación en ley de cabeza", "Errores de muestreo en correa principal", "Inconsistencia en flujómetros de PLS"],
        "Horas": [35.0, 23.0, 12.0]
    }
}

# Obtener los datos del módulo seleccionado
datos_actuales = datos_paretos[modulo_seleccionado]
df_pareto = pd.DataFrame({
    "Falla": datos_actuales["Fallas"],
    "Horas": datos_actuales["Horas"]
})

# Cálculos de Pareto (Porcentaje y Acumulado)
df_pareto = df_pareto.sort_values(by='Horas', ascending=False).reset_index(drop=True)
df_pareto['Porcentaje'] = (df_pareto['Horas'] / df_pareto['Horas'].sum()) * 100.0
df_pareto['Porcentaje Acumulado'] = df_pareto['Porcentaje'].cumsum()

st.subheader(f"Diagrama de Pareto para: {modulo_seleccionado}")

# Construcción del Gráfico de Doble Eje con Plotly
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_pareto['Falla'],
        y=df_pareto['Horas'],
        name="Horas de Detención",
        marker_color='#e74c3c',
        yaxis='y'
    )
)

fig.add_trace(
    go.Scatter(
        x=df_pareto['Falla'],
        y=df_pareto['Porcentaje Acumulado'],
        name="Porcentaje Acumulado (%)",
        mode='lines+markers',
        line=dict(color='#3498db', width=3),
        yaxis='y2'
    )
)

fig.update_layout(
    title=f"Análisis 80/20 de Fallas - {modulo_seleccionado}",
    xaxis=dict(title="Causas de Detención / Falla"),
    yaxis=dict(title="Impacto (Horas / Mes)", side='left', showgrid=True),
    yaxis2=dict(title="Acumulado (%)", overlaying='y', side='right', range=[0, 105], showgrid=False),
    legend=dict(x=0.01, y=0.99),
    template="plotly_dark",
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("2. Análisis de Causas Raíz y Foco de Mejora")
st.markdown(f"""
- **Principio 80/20 en {modulo_seleccionado}:** Las principales causas identificadas concentran el mayor impacto operacional del área.
- **Dónde hincarle el diente (Causas VITALES):** Se debe enfocar el plan de acción prioritario en: **{df_pareto.loc[0, 'Falla']}**.
""")

st.subheader("3. Recomendaciones de Confiabilidad y Mantenimiento")
st.markdown("""
- Implementar mantenimiento predictivo y monitoreo de condición en los equipos críticos identificados en el primer quintil de Pareto.
- Realizar auditorías operacionales semanales y registrar las detenciones por turno para mitigar la aparición recurrente de estas causas raíz.
""")
