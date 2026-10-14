"""
Módulo Core: Chancado y conminución (Ley de Bond).
Fundamento físico: Tercera ley de la conminución de Fred C. Bond.
"""

import numpy as np

def calcular_trabajo_bond(wi: float, f80: float, p80: float, tonelaje_t_h: float) -> dict:
    """
    Calcula el consumo específico de energía (kWh/t) y la potencia requerida (kW)
    utilizando la Tercera Ley de Bond.
    """
    if f80 <= 0 or p80 <= 0 or wi <= 0 or tonelaje_t_h <= 0:
        raise ValueError("Los valores de entrada deben ser estrictamente mayores que cero.")
    
    w_kwh_t = 10.0 * wi * ((1.0 / np.sqrt(p80)) - (1.0 / np.sqrt(f80)))
    potencia_kw = w_kwh_t * tonelaje_t_h
    
    return {
        "w_kwh_t": round(w_kwh_t, 4),
        "potencia_kw": round(potencia_kw, 2)
    }

