"""PROTOTIPO AISLADO (opcional): planos de un sistema 3x3 con PyVista.

No forma parte de la aplicación obligatoria ni está en requirements.txt.
Sirve para evaluar PyVista (https://docs.pyvista.org/).

    python -m venv venv_pv
    venv_pv\\Scripts\\python -m pip install pyvista==0.49.1
    venv_pv\\Scripts\\python prototipos\\pyvista_planos.py   (desde la raíz del proyecto)

El sistema se resuelve con NUESTRO Gauss (algebra/directos.py); PyVista solo
dibuja: un pyvista.Plane por ecuación (centro = un punto del plano, dirección =
vector normal (a, b, c)) y una esfera en la solución única.
Genera prototipos/planos_pyvista.png en modo fuera de pantalla (off_screen).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyvista as pv  # noqa: E402

from algebra.modulo_I_sistemas.directos import resolver_gauss

A = [[1, 1, 1], [2, 1, -1], [-1, 1, 2]]
b = [6, 3, 7]
COLORES = ["#1f77b4", "#ff7f0e", "#2ca02c"]


def punto_del_plano(normal, d):
    """Punto del plano n·x = d más cercano al origen: x = d n / ||n||²."""
    cuadrado = sum(v * v for v in normal)
    return [d * v / cuadrado for v in normal]


def main():
    resultado = resolver_gauss(A, b)
    print("Clasificación (núcleo propio):", resultado.clasificacion, resultado.solucion)
    plotter = pv.Plotter(off_screen=True, window_size=(900, 700))
    for i, fila in enumerate(A):
        normal = [float(v) for v in fila]
        centro = punto_del_plano(normal, float(b[i]))
        if resultado.solucion is not None:      # centrar los planos cerca de la solución
            centro = [float(v) for v in resultado.solucion]
        plano = pv.Plane(center=centro, direction=normal, i_size=8, j_size=8)
        plotter.add_mesh(plano, color=COLORES[i], opacity=0.45, label=f"Ecuación {i + 1}")
    if resultado.solucion is not None:
        punto = [float(v) for v in resultado.solucion]
        plotter.add_mesh(pv.Sphere(radius=0.25, center=punto), color="black", label="Solución")
    plotter.add_legend()
    plotter.show_axes()
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planos_pyvista.png")
    plotter.screenshot(destino)
    plotter.close()
    print("Imagen generada:", destino, os.path.getsize(destino), "bytes")


if __name__ == "__main__":
    main()
