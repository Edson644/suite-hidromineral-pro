from pathlib import Path

# Ruta principal de la carpeta en el Escritorio
escritorio = Path.home() / "Desktop"
carpeta_proyecto = escritorio / "Software Proyecto minero"
carpeta_bibliografia = carpeta_proyecto / "Bibliografía Proyecto Minero"

print("--------------------------------------------------")
print(f"Ruta principal: {carpeta_proyecto}")
print("--------------------------------------------------")

if carpeta_proyecto.exists():
    print("¡Éxito! Carpeta principal encontrada.")

    # Verificamos la subcarpeta de bibliografía
    if carpeta_bibliografia.exists() and carpeta_bibliografia.is_dir():
        print("\n📚 Contenido de 'Bibliografía Proyecto Minero':")
        archivos_bib = list(carpeta_bibliografia.iterdir())

        if len(archivos_bib) == 0:
            print("  (La carpeta de bibliografía está vacía. ¡Agrega tus PDFs aquí!)")
        else:
            for archivo in archivos_bib:
                print(f"  📄 {archivo.name}")
    else:
        print("\n⚠️ No se encontró la subcarpeta 'Bibliografía Proyecto Minero'.")
else:
    print("⚠️ No se encontró la carpeta principal.")

