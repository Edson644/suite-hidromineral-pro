from pathlib import Path
import pandas as pd

# 1. Definir rutas exactas
escritorio = Path.home() / "Desktop"
carpeta_principal = escritorio / "Software Proyecto Minero"
carpeta_bd = carpeta_principal / "Base de Datos Proyecto Minero"

print("--------------------------------------------------")
print(" ANÁLISIS GENERAL DE LA BASE DE DATOS PROYECTO MINERO")
print("--------------------------------------------------")

if carpeta_bd.exists():
    # Buscar todos los archivos Excel en la carpeta
    archivos_excel = list(carpeta_bd.glob("*.xlsx"))
    print(f"[+] Se encontraron {len(archivos_excel)} archivos Excel en total.\n")
    
    # Recorrer e inspeccionar cada archivo
    for idx, archivo in enumerate(archivos_excel, 1):
        print(f"--------------------------------------------------")
        print(f"[{idx}] Archivo: {archivo.name}")
        print(f"--------------------------------------------------")
        try:
            # Leer las hojas del archivo Excel
            excel_obj = pd.ExcelFile(archivo)
            print(f"    - Hojas internas: {excel_obj.sheet_names}")
            
            # Leer la primera hoja para ver tamaño y columnas principales
            df = pd.read_excel(archivo, sheet_name=0)
            print(f"    - Dimensiones (1era hoja): {df.shape[0]} filas x {df.shape[1]} columnas")
            
            # Mostrar las primeras columnas como referencia
            columnas_muestra = list(df.columns[:4])
            print(f"    - Primeras columnas: {columnas_muestra}")
            
        except Exception as e:
            print(f"    ⚠️ No se pudo procesar este archivo debido a un error: {e}")
else:
    print("[!] No se encontró la carpeta 'Base de Datos Proyecto Minero'.")

