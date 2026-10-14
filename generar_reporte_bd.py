from pathlib import Path
import pandas as pd
import datetime

# 1. Definir rutas exactas
escritorio = Path.home() / "Desktop"
carpeta_principal = escritorio / "Software Proyecto Minero"
carpeta_bd = carpeta_principal / "Base de Datos Proyecto Minero"

print("--------------------------------------------------")
print(" GENERANDO REPORTE DETALLADO DE LA BASE DE DATOS")
print("--------------------------------------------------")

reporte_datos = []

if carpeta_bd.exists():
    # Buscamos todos los archivos Excel, ignorando los archivos temporales de Office que empiezan con ~$
    archivos_excel = [f for f in carpeta_bd.glob("*.xlsx") if not f.name.startswith("~$")]
    print(f"[+] Se procesarán {len(archivos_excel)} archivos válidos.\n")
    
    for idx, archivo in enumerate(archivos_excel, 1):
        print(f"[{idx}/{len(archivos_excel)}] Analizando: {archivo.name}")
        
        info_archivo = {
            "Archivo": archivo.name,
            "Estado": "Exitoso",
            "Hojas": "",
            "Filas_1era_Hoja": 0,
            "Columnas_1era_Hoja": 0,
            "Primeras_Columnas": ""
        }
        
        try:
            # Leer las hojas del archivo
            excel_obj = pd.ExcelFile(archivo)
            info_archivo["Hojas"] = ", ".join(excel_obj.sheet_names)
            
            # Leer la primera hoja
            df = pd.read_excel(archivo, sheet_name=0)
            info_archivo["Filas_1era_Hoja"] = df.shape[0]
            info_archivo["Columnas_1era_Hoja"] = df.shape[1]
            info_archivo["Primeras_Columnas"] = " | ".join([str(c) for c in df.columns[:5]])
            
        except Exception as e:
            info_archivo["Estado"] = f"Error: {str(e)}"
            
        reporte_datos.append(info_archivo)
    
    # 2. Crear un DataFrame con el reporte consolidado
    df_reporte = pd.DataFrame(reporte_datos)
    
    # 3. Guardar el reporte en un archivo Excel dentro de la misma carpeta del proyecto
    ruta_salida = Path.home() / "Desktop" / "proyecto_ingenieria" / "Reporte_Consolidado_BaseDatos.xlsx"
    df_reporte.to_excel(ruta_salida, index=False)
    
    print("\n--------------------------------------------------")
    print(f"¡PROCESO FINALIZADO CON ÉXITO!")
    print(f"Reporte consolidado guardado en: {ruta_salida}")
    print("--------------------------------------------------")
    
else:
    print("[!] No se encontró la carpeta 'Base de Datos Proyecto Minero'.")

