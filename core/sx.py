"""
Módulo Core: Extracción por Solventes (SX)
Fundamento Metalúrgico: Isoterma de extracción, etapas teóricas (McCabe-Thiele) y transferencia neta.
"""
import numpy as np

def calcular_sx(
    cu_plop_g_l: float, 
    cu_raff_g_l: float, 
    oa_ratio: float, 
    carga_max_org: float = 5.5
) -> dict:
    """
    Calcula la transferencia neta de cobre, la recuperación de SX y estima las 
    etapas teóricas y reales para el diagrama McCabe-Thiele.
    """
    if cu_plop_g_l <= cu_raff_g_l:
        raise ValueError("El cobre en PLS debe ser mayor que el cobre en el refino.")
    if oa_ratio <= 0:
        raise ValueError("La relación Orgánico/Acuoso (O/A) debe ser mayor que cero.")

    # Transferencia neta de cobre (g/L)
    transferencia_neta = cu_plop_g_l - cu_raff_g_l

    # Recuperación de la sección de extracción (%)
    recuperacion_sx = ((cu_plop_g_l - cu_raff_g_l) / cu_plop_g_l) * 100.0

    # Estimación de etapas teóricas basadas en balance y relación de pendientes (McCabe-Thiele simplificado)
    # Pendiente de la línea de operación = O/A
    # Asumiendo eficiencia de etapa mixtura-sedimentación industrial ~ 85-90% (eficiencia Murphree)
    etapas_teoricas = max(1, int(np.ceil(transferencia_neta / (carga_max_org * 0.8))))
    eficiencia_etapas = 0.85
    etapas_reales = int(np.ceil(etapas_teoricas / eficiencia_etapas))

    return {
        "transferencia_neta_g_l": round(transferencia_neta, 2),
        "recuperacion_sx_pct": round(recuperacion_sx, 2),
        "etapas_teoricas": etapas_teoricas,
        "etapas_reales": etapas_reales
    }

