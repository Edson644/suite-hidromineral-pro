"""
Módulo Core: Lixiviación (Cinética de 90 paños y Nanoburbujas)
Fundamento Metalúrgico: Modelo cinético de primer orden modificado con tasa de riego y lag time.
"""
import numpy as np

def calcular_cinetica_paño(
    t_dias: float, 
    r_max: float = 85.0, 
    k_base: float = 0.05, 
    tasa_riego: float = 10.0, 
    tasa_ref: float = 10.0, 
    alpha: float = 0.5, 
    lag_dias: float = 2.0,
    nanoburbujas_activo: bool = False,
    delta_rec_nb: float = 6.0,
    delta_acido_nb: float = -6.0
) -> dict:
    """
    Calcula la recuperación fraccional R(t) para un tiempo dado considerando nanoburbujas.
    k_eff = k_base * (tasa_riego / tasa_ref)**alpha
    """
    if t_dias <= lag_dias:
        recuperacion = 0.0
    else:
        k_eff = k_base * ((tasa_riego / tasa_ref) ** alpha)
        recuperacion = r_max * (1.0 - np.exp(-k_eff * (t_dias - lag_dias)))

    # Aplicar mejora por nanoburbujas si está activo
    ahorro_acido_pct = 0.0
    if nanoburbujas_activo:
        recuperacion += delta_rec_nb
        ahorro_acido_pct = abs(delta_acido_nb)

    recuperacion = min(recuperacion, r_max)

    return {
        "recuperacion_pct": round(recuperacion, 2),
        "k_eff": round(k_eff if t_dias > lag_dias else 0.0, 4),
        "ahorro_acido_pct": ahorro_acido_pct
    }

def simular_90_panos(
    num_panos: int = 90, 
    dias_operacion: int = 60, 
    nanoburbujas_activo: bool = False
) -> list:
    """
    Simula el estado de los 90 paños con fechas de inicio desfasadas.
    """
    paños_data = []
    for i in range(1, num_panos + 1):
        # Cada paño tiene una antigüedad desfasada en el ciclo de riego
        edad_paño = max(1, (dias_operacion + i) % 90)
        res = calcular_cinetica_paño(float(edad_paño), nanoburbujas_activo=nanoburbujas_activo)

        estado = "Activo Riego" if edad_paño < 75 else "En Drenaje / Cosecha"
        paños_data.append({
            "pano": f"Paño {i}",
            "edad_dias": edad_paño,
            "recuperacion_pct": res["recuperacion_pct"],
            "estado": estado
        })
    return paños_data

