"""Renderiza cada página de los PDF fuente a PNG para la auditoría visual.

Uso: python herramientas/renderizar_fuentes.py <carpeta_pdf> <carpeta_salida>
Las imágenes no se guardan en el repositorio (tamaño); el manifiesto sí se genera en la salida.
"""
import glob
import json
import os
import sys

import pymupdf

ANCHO_PX = 1600


def main(carpeta_pdf: str, carpeta_salida: str) -> None:
    os.makedirs(carpeta_salida, exist_ok=True)
    manifiesto = []
    for i, ruta in enumerate(sorted(glob.glob(os.path.join(carpeta_pdf, "*.pdf")))):
        documento = pymupdf.open(ruta)
        nombre = os.path.basename(ruta)
        prefijo = f"doc{i:02d}"
        for n, pagina in enumerate(documento, 1):
            zoom = ANCHO_PX / pagina.rect.width
            pix = pagina.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
            png = os.path.join(carpeta_salida, f"{prefijo}_p{n:03d}.png")
            pix.save(png)
            manifiesto.append({"doc": prefijo, "archivo": nombre, "pagina": n, "png": png})
    with open(os.path.join(carpeta_salida, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=1)
    print(f"Páginas renderizadas: {len(manifiesto)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
