"""
Módulo Core: Análisis de Pareto (80/20) para Confiabilidad Operacional
Fundamento Industrial: Identificación de causas raíz de detenciones y pérdidas por área.
"""
import pandas as pd

def calcular_pareto(datos_detenciones: list) -> pd.DataFrame:
    """
    Recibe una lista de diccionarios con causa y horas/pérdida, 
    ordena de mayor a menor y calcula el porcentaje acumulado.
    """
    df = pd.DataFrame(datos_detenciones)
    if df.empty:
        return df

    # Ordenar de mayor a menor impacto
    df = df.sort_values(by="Impacto_Horas", ascending=False).reset_index(drop=True)

    # Calcular porcentaje acumulado
    total_impacto = df["Impacto_Horas"].sum()
    df["Porcentaje"] = (df["Impacto_Horas"] / total_impacto) * 100.0 if total_impacto > 0 else 0.0
    df["Porcentaje_Acumulado"] = df["Porcentaje"].cumsum()

    return df

