"""
Módulo Core: Electroobtención (EW)
Fundamento Electroquímico: Ley de Faraday, consumo específico y producción diaria.
"""

def calcular_consumo_especifico_ew(voltaje_celda: float, eficiencia_corriente: float) -> float:
    """
    Calcula el consumo específico de energía en kWh/kg de Cu depositado.
    Fórmula: kWh/kg = V / (1.186 * eta)
    Con 2.15 V y 92% (0.92) da aprox 1.97 kWh/kg.
    """
    if eficiencia_corriente <= 0 or eficiencia_corriente > 1.0:
        raise ValueError("La eficiencia de corriente debe expresarse en fracción (ej. 0.92).")
    if voltaje_celda <= 0:
        raise ValueError("El voltaje de celda debe ser mayor que cero.")

    constante_faraday = 1.186  # g/(A*h) aproximado
    kwh_kg = voltaje_celda / (constante_faraday * eficiencia_corriente)
    return round(kwh_kg, 4)

def calcular_produccion_diaria_ew(
    densidad_corriente_A_m2: float, 
    area_catodo_m2: float, 
    n_catodos_por_celda: int, 
    n_celdas: int, 
    eficiencia_corriente: float
) -> float:
    """
    Calcula la producción diaria de cátodos de cobre (t/d).
    Fórmula: Producción = j * A * 2 caras * N_cátodos * N_celdas * 1.186 * eta * 24 / 1e6
    """
    caras_catodo = 2
    horas_dia = 24
    factor_conversion = 1e6
    constante_prod = 1.186

    prod_diaria_g = (
        densidad_corriente_A_m2 * 
        area_catodo_m2 * 
        caras_catodo * 
        n_catodos_por_celda * 
        n_celdas * 
        constante_prod * 
        eficiencia_corriente * 
        horas_dia
    )
    prod_diaria_t = prod_diaria_g / factor_conversion
    return round(prod_diaria_t, 3)

