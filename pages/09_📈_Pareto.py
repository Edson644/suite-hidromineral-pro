import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Consolidado de Paretos | Suite Hidromineral", page_icon="📈", layout="wide")

st.title("📈 Consolidado de Análisis de Pareto por Módulo")
st.markdown("Centro de análisis de criticidad y factores de mayor impacto (Principio 80/20) para cada etapa del proceso hidromineral.")

# --- SELECTOR DE MÓDULOS ---
modulo_seleccionado = st.selectbox(
    "Seleccione el Módulo Operacional o Financiero a Analizar:",
    [
        "Módulo 1: Chancado y Harneado",
        "Módulo 2: Aglomeración",
        "Módulo 3: Lixiviación (Pilas)",
        "Módulo 4: Extracción por Solventes (SX)",
        "Módulo 5: Electroobtención (EW)",
        "Módulo 6: Pulpas y Reología",
        "Módulo 7: Balances Metalúrgicos",
        "Módulo 8: Finanzas y Evaluación Económica"
    ]
)

st.markdown("---")

# --- DICCIONARIO DE DATOS PARA CADA PARETO ---
pareto_data = {
    "Módulo 1: Chancado y Harneado": {
        "titulo": "Diagrama de Pareto - Pérdidas y Restricciones en Chancado",
        "causas": [
            "Desgaste prematuro de blindajes / martillos",
            "Sobrecarga por material ultra-fino o humedad",
            "Atascamientos en tolvas y chutes de transferencia",
            "Fallas en sistemas hidráulicos de ajuste",
            "Baja eficiencia de clasificación en harneros",
            "Otros tiempos muertos mecánicos"
        ],
        "impacto": [36.0, 28.0, 18.0, 10.0, 5.0, 3.0]
    },
    "Módulo 2: Aglomeración": {
        "titulo": "Diagrama de Pareto - Desviaciones Operativas en Aglomeración",
        "causas": [
            "Variación en la dosificación de ácido y aglomerante",
            "Humedad deficiente en el tambor aglomerador",
            "Segregación granulométrica en la formación de pilas",
            "Rotura de glóbulos por transporte excesivo",
            "Variación en las propiedades físico-químicas del mineral",
            "Problemas de alimentación en correas"
        ],
        "impacto": [40.0, 24.0, 18.0, 10.0, 5.0, 3.0]
    },
    "Módulo 3: Lixiviación (Pilas)": {
        "titulo": "Diagrama de Pareto - Pérdidas y Restricciones en Lixiviación",
        "causas": [
            "Canales Preferenciales / Compactación",
            "Granulometría Gruesa (Sub-chancado)",
            "Tasa de Riego Insuficiente / Taponamiento",
            "Baja Cinética por Temperatura de Solución",
            "Fallas en Sistema de Impermeabilización",
            "Otros Factores Operacionales"
        ],
        "impacto": [38.0, 26.0, 18.0, 10.0, 5.0, 3.0]
    },
    "Módulo 4: Extracción por Solventes (SX)": {
        "titulo": "Diagrama de Pareto - Pérdidas y Criticidad en Trenes SX",
        "causas": [
            "Arrastre Orgánico en PLS / Acuoso",
            "Formación de Emulsiones / Barros en Interfaces",
            "Desviación en Relación Operativa O/A",
            "Baja Eficiencia de Transferencia en Mixer",
            "Degradación del Reactivo (Oxima)",
            "Problemas de Coalescencia en Settler"
        ],
        "impacto": [40.0, 25.0, 15.0, 10.0, 7.0, 3.0]
    },
    "Módulo 5: Electroobtención (EW)": {
        "titulo": "Diagrama de Pareto - Pérdidas Energéticas y Operacionales en EW",
        "causas": [
            "Cortocircuitos por Nodulación en Cátodos",
            "Aumento de Resistencia en Contactos Eléctricos",
            "Baja Eficiencia Farádica por Aditivos",
            "Fluctuaciones en Voltaje por Celda",
            "Contaminación del Electrolito (Fe/Cloruros)",
            "Mantenimiento de Barras y Celdas"
        ],
        "impacto": [35.0, 28.0, 17.0, 11.0, 6.0, 3.0]
    },
    "Módulo 6: Pulpas y Reología": {
        "titulo": "Diagrama de Pareto - Restricciones Hidráulicas y de Transporte",
        "causas": [
            "Operación bajo la Velocidad Límite de Depósito",
            "Variación Abrupta en Concentración (Cp)",
            "Aumento de Viscosidad Aparente por Fino",
            "Desgaste Abrasivo en Tuberías / Codos",
            "Sedimentación en Tramos Horizontales",
            "Variación Granulométrica (D50)"
        ],
        "impacto": [42.0, 24.0, 16.0, 10.0, 5.0, 3.0]
    },
    "Módulo 7: Balances Metalúrgicos": {
        "titulo": "Diagrama de Pareto - Errores y Desviaciones en Balance Masivo",
        "causas": [
            "Inconsistencia en Muestreo de Leyes de Cabeza",
            "Errores en Medición de Caudales (PLS / Raff)",
            "Sesgo en Ensayos de Laboratorio",
            "Acumulación de Inventario no Controlado en Pila",
            "Pérdidas por Evaporación o Filtraciones",
            "Discrepancias en Pesaje de Cátodos EW"
        ],
        "impacto": [39.0, 27.0, 16.0, 10.0, 5.0, 3.0]
    },
    "Módulo 8: Finanzas y Evaluación Económica": {
        "titulo": "Diagrama de Pareto - Sensibilidad y Riesgos Financieros",
        "causas": [
            "Fluctuación en el Precio Internacional del Cobre",
            "Desviación en el Costo Operacional Unitario (OPEX)",
            "Variación en la Recuperación Metalúrgica Global",
            "Aumento en el CAPEX Inicial de Inversión",
            "Tasa de Descuento / WACC Aplicado",
            "Costos de Energía y Suministros Críticos"
        ],
        "impacto": [45.0, 25.0, 14.0, 9.0, 4.0, 3.0]
    }
}

# Obtener datos del módulo seleccionado
datos_actuales = pareto_data[modulo_seleccionado]
causas = datos_actuales["causas"]
impactos = datos_actuales["impacto"]

# Calcular acumulado para la curva de Pareto
df_p = pd.DataFrame({
    'Causa': causas,
    'Impacto (%)': impactos
})
df_p['Acumulado (%)'] = df_p['Impacto (%)'].cumsum()

# Lógica de colores dinámica: Rojo para las barras dentro del rango crítico (acumulado previo < 80%) y celeste para el resto
colores_barras = []
for i, val in enumerate(df_p['Acumulado (%)']):
    prev_val = df_p['Acumulado (%)'].iloc[i-1] if i > 0 else 0
    if prev_val < 80.0:
        colores_barras.append('#ff5252')  # Rojo crítico (zona vital 80/20)
    else:
        colores_barras.append('#29b6f6')  # Celeste normal (triviales)

# Crear figura combinada de Pareto (Barras + Línea acumulada)
fig = go.Figure()

# Barras de impacto individual con colores condicionales
fig.add_trace(go.Bar(
    x=df_p['Causa'],
    y=df_p['Impacto (%)'],
    name='Impacto Individual (%)',
    marker_color=colores_barras
))

# Línea de porcentaje acumulado
fig.add_trace(go.Scatter(
    x=df_p['Causa'],
    y=df_p['Acumulado (%)'],
    name='Acumulado (%)',
    mode='lines+markers',
    line=dict(color='#ff9100', width=3),
    yaxis='y2'
))

# Configuración de doble eje y diseño visual
fig.update_layout(
    title=datos_actuales["titulo"],
    plot_bgcolor="#161b22",
    paper_bgcolor="#0b0f12",
    font_color="#f0f2f5",
    xaxis=dict(showgrid=False, tickangle=-20),
    yaxis=dict(
        title="Impacto Individual (%)",
        showgrid=True,
        gridcolor="#30363d",
        range=[0, 105]
    ),
    yaxis2=dict(
        title="Impacto Acumulado (%)",
        overlaying='y',
        side='right',
        showgrid=False,
        range=[0, 105]
    ),
    height=480,
    legend=dict(x=0.02, y=0.95)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🔍 Análisis de Criticidad 80/20")
st.text(
    f"Enfoque Operacional para '{modulo_seleccionado}': Las barras destacadas en rojo representan los factores críticos "
    "que concentran el mayor impacto acumulado según el principio de Pareto."
)
st.text(
    "Regla del 80/20: Enfocar los esfuerzos de ingeniería y control operacional en estas causas principales garantiza la mitigación "
    "efectiva de las principales pérdidas de la planta."
)
