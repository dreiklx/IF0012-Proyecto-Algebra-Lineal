"""Visualizaciones complementarias del Módulo II (normas y sensibilidad).

Son figuras de Plotly que DIBUJAN valores ya calculados por el núcleo (algebra/): las
sumas de fila y columna de `matriz.py` y los errores relativos de `analizar_perturbacion`.
No se calcula ningún método nuevo aquí.

La interpretación del determinante como factor de área se eliminó: no aparece en los
materiales de la profesora (ver docs/auditoria/decision_graficas.md).

Ninguna de estas figuras es un procedimiento de la profesora.  El título de cada una
indica si es complementaria; ver docs/auditoria/decision_graficas.md.
"""

import plotly.graph_objects as go

from visualizacion.interactivas import FUENTE, _base, _eje
from visualizacion.tema import COLOR_DATOS, COLOR_RECTA, COLOR_RESIDUO, FONDO, FONDO_EJES, TEXTO

COLOR_MAXIMO = "#F59E0B"


def normas_filas(sumas_A, sumas_inversa=None):
    """Sumas absolutas por FILA de A (y de A⁻¹) en un solo eje; el máximo de cada serie está
    destacado.  Es la norma ∞ (S7-21/09 p. 19, pasos 2 y 4 de κ∞).  Un solo eje permite
    desplazar y acercar con MediaPipe sin ambigüedad."""
    fig = go.Figure()
    series = [("‖A‖∞ · sumas de fila de A", sumas_A, COLOR_RECTA)]
    if sumas_inversa is not None:
        series.append(("‖A⁻¹‖∞ · sumas de fila de A⁻¹", sumas_inversa, COLOR_DATOS))
    n = len(sumas_A)
    for nombre, valores, color in series:
        indice_max = max(range(len(valores)), key=lambda i: valores[i])
        colores = [COLOR_MAXIMO if i == indice_max else color for i in range(len(valores))]
        fig.add_trace(go.Bar(x=list(range(len(valores))),
                             y=[float(v) for v in valores], name=nombre, marker_color=colores,
                             text=[f"{float(v):.6g}" for v in valores], textposition="outside",
                             hovertemplate="%{x}: suma = %{y:.6g}<extra></extra>"))
    _estilo(fig, "Visualización complementaria · sumas de fila (la barra naranja es el máximo = norma ∞)", n)
    fig.update_layout(barmode="group", xaxis=_eje("fila", range=[-0.5, n - 0.5],
                                                  tickvals=list(range(n)),
                                                  ticktext=[f"Fila {i + 1}" for i in range(n)]))
    return fig


def normas_columnas(sumas_columnas):
    """Sumas absolutas por COLUMNA de A: norma 1 (S7-21/09 p. 19, cálculo con la norma 1).
    Es referencia: no interviene en κ∞."""
    fig = go.Figure()
    indice_max = max(range(len(sumas_columnas)), key=lambda i: sumas_columnas[i])
    colores = [COLOR_MAXIMO if i == indice_max else COLOR_RESIDUO for i in range(len(sumas_columnas))]
    fig.add_trace(go.Bar(x=list(range(len(sumas_columnas))),
                         y=[float(v) for v in sumas_columnas], marker_color=colores,
                         text=[f"{float(v):.6g}" for v in sumas_columnas], textposition="outside",
                         hovertemplate="%{x}: suma = %{y:.6g}<extra></extra>"))
    _estilo(fig, "Referencia · sumas de columna (máximo = norma 1; no se usa en κ∞)", len(sumas_columnas))
    fig.update_layout(xaxis=_eje("columna", range=[-0.5, len(sumas_columnas) - 0.5],
                                 tickvals=list(range(len(sumas_columnas))),
                                 ticktext=[f"Columna {i + 1}" for i in range(len(sumas_columnas))]))
    return fig


def _estilo(fig, titulo, n):
    fig.update_layout(title=dict(text=titulo, x=0.01, font=dict(size=15, color=TEXTO)),
                      paper_bgcolor=FONDO, plot_bgcolor=FONDO_EJES,
                      font=dict(family=FUENTE, color=TEXTO, size=12),
                      height=380, margin=dict(l=60, r=30, t=70, b=40),
                      xaxis=_eje("", range=[-0.5, n - 0.5]),
                      yaxis=_eje("suma de valores absolutos", zeroline=True, rangemode="tozero"),
                      legend=dict(orientation="h", y=-0.2))


def rango_normas_inicial(sumas_A, sumas_inversa=None):
    """Rango por defecto del gráfico de filas: categorías y sumas con un 20 % de margen."""
    valores = list(sumas_A) + (list(sumas_inversa) if sumas_inversa is not None else [])
    return (-0.5, len(sumas_A) - 0.5, 0.0, float(max(valores)) * 1.2)


def sensibilidad_barras(error_b, error_x, cota):
    """Compara en una gráfica el error relativo de b, el de x y la cota κ·error_b.

    Complementaria: muestra la desigualdad ‖Δx‖/‖x‖ ≤ κ·‖Δb‖/‖b‖ con los valores de
    la perturbación introducida; no es un método nuevo."""
    fig = _base("Visualización complementaria · perturbación frente a la cota κ∞ · ‖Δb‖/‖b‖", alto=380)
    etiquetas = ["‖Δb‖∞/‖b‖∞ (dato)", "‖Δx‖∞/‖x‖∞ (solución)", "Cota κ∞ · ‖Δb‖∞/‖b‖∞"]
    valores = [float(error_b) * 100, float(error_x) * 100, float(cota) * 100]
    colores = [COLOR_DATOS, COLOR_RESIDUO, COLOR_RECTA]
    fig.add_trace(go.Bar(x=etiquetas, y=valores, marker_color=colores,
                         text=[f"{v:.4g} %" for v in valores], textposition="outside",
                         hovertemplate="%{x}: %{y:.4g} %<extra></extra>"))
    fig.update_layout(yaxis=_eje("porcentaje (%)", zeroline=True, rangemode="tozero"), showlegend=False)
    return fig
