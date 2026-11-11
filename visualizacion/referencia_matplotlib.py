"""Figura de referencia con Matplotlib (no se muestra en la aplicación).

La aplicación dibuja con Plotly (interactivas.py).  Esta figura estática de la
convergencia se conserva como oráculo independiente: tests/interfaz/
test_graficas_interactivas.py comprueba que Plotly dibuja exactamente los mismos
puntos que Matplotlib.  Las etiquetas usan mathtext ($d_k$).
"""

import matplotlib

matplotlib.use("Agg")  # backend sin ventanas (servidor web)
import matplotlib.pyplot as plt  # noqa: E402

from visualizacion.datos_graficas import positivos  # noqa: E402
from visualizacion.tema import (  # noqa: E402
    COLOR_EPSILON,
    COLOR_RECTA,
    COLOR_RESIDUO,
    COLORES_METODOS,
    FONDO,
    FONDO_EJES,
    REJILLA,
    SUAVE,
    TEXTO,
)

COLORES = COLORES_METODOS
MATH = {"d": r"$d_k = \|x^{(k)} - x^{(k-1)}\|_\infty$", "r": r"$r_k = \|b - Ax^{(k)}\|_\infty$"}


def aplicar_tema():
    """Mismo aspecto oscuro que la interfaz.  Solo cambia colores y tipografía."""
    plt.rcParams.update({
        "figure.facecolor": FONDO, "axes.facecolor": FONDO_EJES, "savefig.facecolor": FONDO,
        "axes.edgecolor": REJILLA, "axes.labelcolor": TEXTO, "axes.titlecolor": TEXTO,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10.5,
        "axes.grid": True, "grid.color": REJILLA, "grid.alpha": 0.7, "grid.linewidth": 0.6,
        "xtick.color": SUAVE, "ytick.color": SUAVE, "xtick.labelsize": 9, "ytick.labelsize": 9,
        "text.color": TEXTO, "legend.facecolor": "#18223A", "legend.edgecolor": REJILLA,
        "legend.labelcolor": TEXTO, "legend.framealpha": 0.92, "legend.fontsize": 8.5,
        "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
        "lines.linewidth": 2.0, "lines.markersize": 5,
        "axes.spines.top": False, "axes.spines.right": False,
    })


aplicar_tema()


def _figura(ancho=7.6, alto=4.3):
    fig, ax = plt.subplots(figsize=(ancho, alto), dpi=120)
    return fig, ax


def _leyenda(ax, columnas=2):
    """Leyenda debajo de los ejes: no tapa ninguna curva."""
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=columnas, frameon=False)


def grafica_convergencia(historial, criterio, tolerancia=None):
    """d_k y r_k frente a k (escala logarítmica), con la línea ε sobre la métrica
    que actúa como criterio de parada."""
    fig, ax = _figura()
    ks = [f.k for f in historial]
    series = [(MATH["d"], [f.d for f in historial], "o-", COLOR_RECTA, "A"),
              (MATH["r"], [f.r for f in historial], "s--", COLOR_RESIDUO, "B")]
    hay_datos = False
    for nombre, valores, estilo, color, letra in series:
        puntos, ceros = positivos(ks, valores)
        etiqueta = nombre + (" (criterio de parada)" if criterio == letra else " (informativo)")
        if puntos:
            hay_datos = True
            ax.plot([p[0] for p in puntos], [p[1] for p in puntos], estilo, color=color,
                    markersize=4, label=etiqueta)
        if ceros:
            ax.scatter(ceros, [1e-17] * len(ceros), marker="v", color=color,
                       label=f"{nombre.split(' =')[0]}$ = 0 exactamente")   # «$d_k$ = 0»
            hay_datos = True
    if tolerancia is not None and criterio in ("A", "B"):
        ax.axhline(float(tolerancia), color=COLOR_EPSILON, linestyle="-.", linewidth=1.3,
                   label=f"ε = {float(tolerancia):.3g}")
    if hay_datos:
        ax.set_yscale("log")
    ax.set_xlabel("Iteración k")
    ax.set_ylabel("Valor (escala logarítmica)")
    ax.set_title("Evolución del cambio entre iteraciones y del residuo")
    _leyenda(ax, 3)
    fig.tight_layout()
    return fig


def cerrar(fig):
    """Libera la memoria de una figura ya mostrada."""
    plt.close(fig)
