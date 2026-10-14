"""
Módulo Core: Pulpas y Relaves
Fundamento Hidráulico: Relación S/L, Gravedad Específica de la pulpa, velocidad de operación y velocidad límite de depósito.
"""
import numpy as np

def calcular_sistema_bombeo_pulpa(
    m_solidos_tph: float, 
    densidad_solidos: float, 
    cw_porcentaje: float, 
    diametro_tuberia_mm: float, 
    longitud_tuberia_m: float, 
    altura_estatica_m: float, 
    d85_mm: float, 
    parametro_fl: float = 1.1
) -> dict:
    """
    Calcula la densidad de la pulpa, caudal volumétrico, velocidad operacional,
    velocidad límite de depósito (Wasp/Durand), pérdidas por fricción y potencia de frenado.
    """
    if m_solidos_tph <= 0 or densidad_solidos <= 1.0 or cw_porcentaje <= 0 or cw_porcentaje >= 100:
        raise ValueError("Los parámetros físicos de la pulpa están fuera de rango válido.")

    # 1. Gravedad Específica de la pulpa (Sm)
    # 1 / Sm = (Cw / 100 / S_solidos) + ((100 - Cw) / 100 / 1.0)
    frac_cw = cw_porcentaje / 100.0
    sm = 1.0 / ((frac_cw / densidad_solidos) + ((1.0 - frac_cw) / 1.0))

    # Concentración volumétrica (Cv)
    cv_pct = cw_porcentaje * (sm / densidad_solidos)

    # 2. Caudal Másico y Volumétrico
    # Q_m3_h = (M_solidos / Cw_fracción) / Sm (aproximación industrial de caudal de pulpa)
    m_solidos_kg_s = (m_solidos_tph * 1000.0) / 3600.0
    # Caudal volumétrico total Q (m3/h)
    # Q = M_solidos / (Cw * rho_agua * Cv_fraccion) aprox, o usando densidad de pulpa
    vol_total_m3_s = m_solidos_kg_s / (frac_cw * sm * 1000.0) if frac_cw > 0 else 0
    q_m3_h = vol_total_m3_s * 3600.0

    # 3. Velocidad Operacional en la tubería (V_velocity)
    # Área de la tubería en m2
    d_m = diametro_tuberia_mm / 1000.0
    area_pipe = (np.pi * (d_m ** 2)) / 4.0
    v_velocity = vol_total_m3_s / area_pipe if area_pipe > 0 else 0.0

    # Velocidad Límite de Depósito (Correlación simplificada de Durand-Condolios)
    # V_limit = F_L * sqrt(2 * g * D * (Sm - 1))
    g = 9.81
    v_limit = parametro_fl * np.sqrt(2.0 * g * d_m * max(0.0, sm - 1.0))

    # Estado de transporte
    estado_transporte = "SEGURO (Suspensión Completa)" if v_velocity > v_limit else "ALERTA: Riesgo de Sedimentación"

    # 4. Pérdidas por fricción (Darcy-Weisbach modificado con factor de pulpa)
    darcy_f = 0.025
    h_friction = darcy_f * (longitud_tuberia_m / d_m) * ((v_velocity ** 2) / (2.0 * g)) * sm

    # Altura Total de Impulsión (Total Head)
    total_head_m = altura_estatica_m + h_friction

    # Presión de trabajo en el sistema
    presion_kpa = sm * g * total_head_m

    # 5. Potencia al Freno (Brake Power) con Eficiencia estimada del Impulsor (75%) y Margen de Seguridad (20%)
    eficiencia_pompa = 0.75
    # Potencia hidráulica en kW = (Q_m3_s * Sm * 1000 * g * Total_Head) / 1000
    potencia_hidraulica_kw = (vol_total_m3_s * sm * 1000.0 * g * total_head_m) / 1000.0
    potencia_freno_kw = (potencia_hidraulica_kw / eficiencia_pompa) * 1.20

    return {
        "Gravedad_Especifica_Sm": round(sm, 3),
        "Concentracion_Volumen_Cv_pct": round(cv_pct * 100.0, 2),
        "Caudal_Volumetrico_m3h": round(q_m3_h, 2),
        "Velocidad_Operativa_ms": round(v_velocity, 2),
        "Velocidad_Limite_Dep_ms": round(v_limit, 2),
        "Estado_Transporte": estado_transporte,
        "Perdidas_Friccion_m": round(h_friction, 2),
        "Altura_Total_Head_m": round(total_head_m, 2),
        "Presion_Sistema_bar": round(presion_kpa / 100.0, 2),
        "Potencia_Requerida_kW": round(potencia_freno_kw, 2)
    }

