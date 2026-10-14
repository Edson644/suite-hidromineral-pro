"""
Módulo Core: Aglomeración
Fundamento Metalúrgico: Optimización de humedad, resistencia verde y aglutinantes (ácido/cemento).
"""

def calcular_aglomeracion(cemento_kg_t: float, acido_kg_t: float, finos_pct: float) -> dict:
    """
    Calcula la humedad óptima de aglomeración y la resistencia verde en función 
    de las adiciones de cemento, ácido y porcentaje de material fino.
    """
    if cemento_kg_t < 0 or acido_kg_t < 0 or finos_pct < 0:
        raise ValueError("Las adiciones y los finos no pueden ser negativos.")

    # Modelo metalúrgico empírico de referencia industrial
    humedad_optima = 8.5 + (0.15 * cemento_kg_t) - (0.05 * acido_kg_t) + (0.02 * finos_pct)
    resistencia_verde = 12.0 + (1.8 * cemento_kg_t) + (0.5 * acido_kg_t) - (0.1 * finos_pct)

    # Criterio de control operacional
    alerta_resistencia = resistencia_verde < 12.0

    return {
        "humedad_optima_pct": round(humedad_optima, 2),
        "resistencia_verde_kpa": round(resistencia_verde, 2),
        "alerta_resistencia": bool(alerta_resistencia)
    }

