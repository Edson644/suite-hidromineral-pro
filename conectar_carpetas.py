from pathlib import Path

# 1. Definimos la ruta principal en el Escritorio con los nombres exactos que indicaste
escritorio = Path.home() / "Desktop"
carpeta_principal = escritorio / "Software Proyecto Minero"
carpeta_bd = carpeta_principal / "Base de Datos Proyecto Minero"
carpeta_biblio = carpeta_principal / "Bibliografia Proyecto Minero"

print("--------------------------------------------------")
print(f"Buscando carpeta principal: {carpeta_principal.name}")
print("--------------------------------------------------")

# 2. Verificamos si existe la carpeta principal
if carpeta_principal.exists() and carpeta_principal.is_dir():
    print(" ¡Éxito! La carpeta principal 'Software Proyecto Minero' fue encontrada en el Escritorio.")
    
    # 3. Verificamos la subcarpeta de Base de Datos
    if carpeta_bd.exists() and carpeta_bd.is_dir():
        print(" Subcarpeta 'Base de Datos Proyecto Minero' encontrada correctamente.")
        archivos_bd = list(carpeta_bd.iterdir())
        if archivos_bd:
            print(f"    Archivos encontrados ({len(archivos_bd)}):")
            for arch in archivos_bd:
                print(f"      - {arch.name}")
        else:
            print("    (La subcarpeta de Base de Datos está vacía actualmente).")
    else:
        print(" ⚠️ No se encontró la subcarpeta 'Base de Datos Proyecto Minero'. Revisa el nombre.")

    # 4. Verificamos la subcarpeta de Bibliografía
    if carpeta_biblio.exists() and carpeta_biblio.is_dir():
        print(" Subcarpeta 'Bibliografia Proyecto Minero' encontrada correctamente.")
        archivos_biblio = list(carpeta_biblio.iterdir())
        if archivos_biblio:
            print(f"    Archivos encontrados ({len(archivos_biblio)}):")
            for arch in archivos_biblio:
                print(f"      - {arch.name}")
        else:
            print("    (La subcarpeta de Bibliografía está vacía actualmente).")
    else:
        print(" ⚠️ No se encontró la subcarpeta 'Bibliografia Proyecto Minero'. Revisa el nombre.")
        
else:
    print(" ⚠️ No se encontró la carpeta principal 'Software Proyecto Minero' en el Escritorio.")
    print("   Asegúrate de que esté creada exactamente con ese nombre en tu Escritorio.")

