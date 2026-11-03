"""Tema común de las gráficas (Matplotlib), coherente con la interfaz oscura.

Solo cambia el aspecto (colores, tipografía, cuadrícula): no altera ningún dato.
Se aplica al importar visualizacion.graficos o visualizacion.geometria_3d.
"""

import matplotlib

matplotlib.use("Agg")  # backend sin ventanas (servidor web)
import matplotlib.pyplot as plt  # noqa: E402

FONDO = "#141C30"
FONDO_EJES = "#101729"
TEXTO = "#E6ECF7"
SUAVE = "#93A1BC"
REJILLA = "#2A3653"

# Un color por método, el mismo en todas las gráficas.
COLORES_METODOS = {"Jacobi": "#4F8CFF", "Gauss-Seidel": "#F472B6", "SOR": "#22D3EE",
                   "Richardson": "#FBBF24"}
COLOR_DATOS = "#22D3EE"
COLOR_RECTA = "#4F8CFF"
COLOR_EPSILON = "#34D399"
COLOR_RESIDUO = "#FBBF24"
COLOR_SOLUCION = "#FFFFFF"
COLORES_PLANOS = ["#4F8CFF", "#F472B6", "#22D3EE", "#FBBF24", "#A78BFA", "#34D399"]


def aplicar():
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


aplicar()
