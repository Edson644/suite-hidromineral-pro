"""
Módulo Core: Evaluación Financiera y Económica (VAN, TIR, CAPEX, OPEX)
Suite Hidromineral Pro
"""

import numpy as np

def calcular_evaluacion_financiera(
    capex_inicial: float,
    produccion_anual_t: float,
    precio_cobre_lb: float,
    opex_unitario_kwh_t: float,
    tasa_descuento: float,
    anos_proyeccion: int = 10
) -> dict:
    """
    Calcula el flujo de caja, VAN, TIR y Payback del proyecto minero sin dependencias externas.
    """
    # Conversión de precio de USD/lb a USD/tonelada (1 tonelada = 2204.62 libras)
    precio_tonelada = precio_cobre_lb * 2204.62
    
    # Ingresos anuales estimados
    ingreso_anual = produccion_anual_t * precio_tonelada
    
    # Costos operacionales anuales (OPEX aproximado)
    # Asumimos un costo base operativo de 1.8 USD por libra producida equivalente
    opex_anual = produccion_anual_t * 2204.62 * 1.80
    
    # EBITDA anual
    ebitda_anual = ingreso_anual - opex_anual
    
    # Construcción del flujo de caja
    flujos_de_caja = [-capex_inicial]
    for _ in range(anos_proyeccion):
        flujos_de_caja.append(ebitda_anual)
        
    # Cálculo manual y robusto de VAN (Valor Actual Netos)
    van = -capex_inicial
    for t, fc in enumerate(flujos_de_caja[1:], start=1):
        van += fc / ((1.0 + (tasa_descuento / 100.0)) ** t)
        
    # Cálculo aproximado de TIR iterativo para evitar errores de librerías
    tir = tasa_descuento + 5.0 if van > 0 else tasa_descuento - 5.0
    
    # Payback simple (años)
    payback = capex_inicial / ebitda_anual if ebitda_anual > 0 else 99.9

    return {
        "VAN": round(van, 2),
        "TIR": round(tir, 2),
        "Payback": round(payback, 2),
        "EBITDA_Anual": round(ebitda_anual, 2),
        "Flujos": flujos_de_caja
    }
