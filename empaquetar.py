"""Genera el archivo comprimido de entrega del proyecto (OFICIAL p. 1).

Uso:
    python empaquetar.py 01        ->  dist/Grupo01-IF0012-Proyecto-IIC.zip
    python empaquetar.py 02        ->  dist/Grupo02-IF0012-Proyecto-IIC.zip

El enunciado pide el formato "Grupo(01-02)-IF0012-Proyecto-IIC.zip"; se
interpreta como Grupo01 o Grupo02 según el grupo del curso (pendiente de
confirmar con la docente).

Se incluyen el código fuente completo, las pruebas, los casos de prueba, la
documentación y los archivos de ejecución.  Se excluyen el entorno virtual,
las cachés de Python, el repositorio .git y los archivos generados.
"""

import os
import sys
import zipfile

RAIZ = os.path.dirname(os.path.abspath(__file__))

INCLUIR = [
    "app.py", "README.md", "requirements.txt", "requirements-bloqueado.txt",
    "ejecutar.bat", "ejecutar_pruebas.bat", "empaquetar.py", ".gitignore", ".gitattributes",
    ".streamlit", "algebra", "interfaz", "visualizacion", "tests", "casos_prueba", "docs", "auditoria",
    "prototipos",
]
OBLIGATORIOS = [
    "app.py", "README.md", "requirements.txt", "ejecutar.bat",
    os.path.join("docs", "manual_usuario.md"), "casos_prueba",
]
EXCLUIR_DIRECTORIOS = {"__pycache__", ".venv", "venv", ".git", "dist", ".pytest_cache"}
EXCLUIR_EXTENSIONES = {".pyc", ".pyo", ".zip", ".png"}
EXCLUIR_ARCHIVOS = {"secrets.toml"}


def archivos_a_incluir():
    for entrada in INCLUIR:
        ruta = os.path.join(RAIZ, entrada)
        if os.path.isfile(ruta):
            yield entrada
        elif os.path.isdir(ruta):
            for carpeta, subcarpetas, archivos in os.walk(ruta):
                subcarpetas[:] = [d for d in subcarpetas if d not in EXCLUIR_DIRECTORIOS]
                for nombre in sorted(archivos):
                    if os.path.splitext(nombre)[1] in EXCLUIR_EXTENSIONES or nombre in EXCLUIR_ARCHIVOS:
                        continue
                    yield os.path.relpath(os.path.join(carpeta, nombre), RAIZ)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("01", "02"):
        print("Uso: python empaquetar.py 01   (o 02, según el número de grupo)")
        return 1
    faltan = [r for r in OBLIGATORIOS if not os.path.exists(os.path.join(RAIZ, r))]
    if faltan:
        print("Faltan elementos obligatorios:", ", ".join(faltan))
        return 1
    nombre_zip = f"Grupo{sys.argv[1]}-IF0012-Proyecto-IIC.zip"
    destino = os.path.join(RAIZ, "dist", nombre_zip)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    carpeta_interna = nombre_zip[:-4]
    cantidad = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zf:
        for relativo in archivos_a_incluir():
            zf.write(os.path.join(RAIZ, relativo), os.path.join(carpeta_interna, relativo))
            cantidad += 1
    print(f"Creado {destino} con {cantidad} archivos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
