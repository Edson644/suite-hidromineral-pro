"""
Punto de Entrada Principal - Suite Hidromineral Pro
Gestión Integral de Procesos Hidrometalúrgicos y Financieros
"""

import streamlit as st

st.set_page_config(
    page_title="Suite Hidromineral Pro",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de la navegación ordenada del M1 al M10
pg = st.navigation({
    "Módulos Operativos de Ingeniería": [
        st.Page("pages/m1_chancado.py", title="M1 Chancado", icon="⚙️"),
        st.Page("pages/m2_aglomeracion.py", title="M2 Aglomeración", icon="🔄"),
        st.Page("pages/m3_lixiviacion.py", title="M3 Lixiviación", icon="💧"),
        st.Page("pages/m4_sx.py", title="M4 SX", icon="🧪"),
        st.Page("pages/m5_ew.py", title="M5 Electro Winning", icon="⚡"),
        st.Page("pages/m6_pulpas.py", title="M6 Pulpas y Relaves", icon="🌊"),
        st.Page("pages/m7_balances.py", title="M7 Balances Metalúrgicos", icon="⚖️"),
        st.Page("pages/m8_finanzas.py", title="M8 Finanzas", icon="💰"),
        st.Page("pages/m9_pareto.py", title="M9 Pareto", icon="📈"),
        st.Page("pages/m10_reportes.py", title="M10 Informes y Memorias", icon="📑")
    ]
})

# Ejecutar la página seleccionada
pg.run()
