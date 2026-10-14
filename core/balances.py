"""
Módulo Core: Balances Metalúrgicos y Saldos
Fundamento Metalúrgico: Balance de masa global, ley de cabeza, ley de colas y recuperación global.
"""

def calcular_balance_global(
    tonelaje_alimentacion_tph: float, 
    ley_cabeza_cu_pct: float, 
    ley_colas_pct: float, 
    recuperacion_lix_pct: float, 
    eficiencia_sx_pct: float, 
    eficiencia_ew_pct: float
) -> dict:
    """
    Calcula el balance masivo global, el metal fino alimentado, recuperado en pilas,
    transferido en SX y depositado como cátodos comerciales en EW.
    """
    if tonelaje_alimentacion_tph <= 0 or ley_cabeza_cu_pct <= 0 or ley_colas_pct < 0:
        raise ValueError("Los valores de alimentación y leyes deben ser válidos.")

    # Fino alimentado (t/h de Cu contenido)
    fino_alimentado_tph = tonelaje_alimentacion_tph * (ley_cabeza_cu_pct / 100.0)

    # Recuperación global combinada (%)
    rec_global_pct = (recuperacion_lix_pct / 100.0) * (eficiencia_sx_pct / 100.0) * (eficiencia_ew_pct / 100.0) * 100.0

    # Fino producido en cátodos (t/h y t/día)
    fino_producido_tph = fino_alimentado_tph * (rec_global_pct / 100.0)
    produccion_catodos_t_d = fino_producido_tph * 24.0

    # Pérdidas en colas / ripios
    fino_perdido_tph = fino_alimentado_tph - fino_producido_tph

    return {
        "Fino_Alimentado_tph": round(fino_alimentado_tph, 3),
        "Recuperacion_Global_pct": round(rec_global_pct, 2),
        "Produccion_Catodos_t_d": round(produccion_catodos_t_d, 2),
        "Fino_Perdido_tph": round(fino_perdido_tph, 3)
    }

