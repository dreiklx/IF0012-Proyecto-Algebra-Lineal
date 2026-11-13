"""Visualizaciones complementarias del Módulo II (determinante, normas y sensibilidad).

Son figuras de Plotly que DIBUJAN valores ya calculados por el núcleo (algebra/): el
determinante sale de `determinante`, las sumas de fila y columna de `matriz.py` y los
errores relativos de `analizar_perturbacion`.  No se calcula ningún método nuevo aquí.

Ninguna de estas figuras es un procedimiento de la profesora.  El título de cada una
indica si es complementaria; ver docs/auditoria/decision_graficas.md.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from visualizacion.interactivas import FUENTE, _base, _eje
from visualizacion.tema import COLOR_DATOS, COLOR_RECTA, COLOR_RESIDUO, FONDO, FONDO_EJES, TEXTO

REJILLA_K = 3          # líneas de la cuadrícula: x = k e y = k para k = −3…3
COLOR_CUADRADO = "#94A3B8"
COLOR_PARALELOGRAMO = "#22D3EE"
COLOR_MAXIMO = "#F59E0B"


def _puntos_transformados(A):
    """Vértices del cuadrado unitario y de su imagen A·(cuadrado) como lista de (x, y)."""
    (a, b), (c, d) = A
    cuadrado = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    imagen = [(a * x + b * y, c * x + d * y) for x, y in cuadrado]
    return cuadrado, imagen


def area_shoelace(vertices):
    """Área de un polígono simple por la fórmula de los lazos (cordones); se usa para comprobar
    que el área del paralelogramo imagen coincide con |det(A)|."""
    n = len(vertices)
    doble = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        doble += x1 * y2 - x2 * y1
    return abs(doble) / 2


def transformacion_2x2(A, det):
    """Cuadrícula original y transformada por A, el cuadrado unitario y su imagen.

    `det` es det(A) ya calculado por el núcleo; aparece como texto y determina el caso
    degenerado (det = 0: la imagen es un segmento y el área es 0).
    """
    fig = _base("Visualización complementaria · el determinante como factor de área",
                alto=520)
    # Solo el dibujo usa flotantes (Plotly no admite Fraction); det y área son los del núcleo.
    A = [[float(v) for v in fila] for fila in A]
    (a, b), (c, d) = A
    cuadrado, imagen = _puntos_transformados(A)
    xs = [p[0] for p in cuadrado + imagen]
    ys = [p[1] for p in cuadrado + imagen]
    for k in range(-REJILLA_K, REJILLA_K + 1):
        # Líneas originales: x = k e y = k.
        fig.add_trace(go.Scatter(x=[k, k], y=[-REJILLA_K, REJILLA_K], mode="lines", hoverinfo="skip",
                                 line=dict(color="rgba(148,163,184,0.35)", width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[-REJILLA_K, REJILLA_K], y=[k, k], mode="lines", hoverinfo="skip",
                                 line=dict(color="rgba(148,163,184,0.35)", width=1), showlegend=False))
        # Imágenes de esas mismas líneas: la cuadrícula deformada por A.
        p1 = (a * k + b * -REJILLA_K, c * k + d * -REJILLA_K)
        p2 = (a * k + b * REJILLA_K, c * k + d * REJILLA_K)
        q1 = (a * -REJILLA_K + b * k, c * -REJILLA_K + d * k)
        q2 = (a * REJILLA_K + b * k, c * REJILLA_K + d * k)
        fig.add_trace(go.Scatter(x=[p1[0], p2[0]], y=[p1[1], p2[1]], mode="lines", hoverinfo="skip",
                                 line=dict(color="rgba(34,211,238,0.35)", width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[q1[0], q2[0]], y=[q1[1], q2[1]], mode="lines", hoverinfo="skip",
                                 line=dict(color="rgba(34,211,238,0.35)", width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=[p[0] for p in cuadrado + [cuadrado[0]]],
                             y=[p[1] for p in cuadrado + [cuadrado[0]]], mode="lines", name="Cuadrado unitario",
                             line=dict(color=COLOR_CUADRADO, width=2.5, dash="dash")))
    fig.add_trace(go.Scatter(x=[p[0] for p in imagen + [imagen[0]]],
                             y=[p[1] for p in imagen + [imagen[0]]], mode="lines",
                             name="Imagen A·(cuadrado) (paralelogramo)",
                             fill="toself", fillcolor="rgba(34,211,238,0.18)",
                             line=dict(color=COLOR_PARALELOGRAMO, width=2.5)))
    area = area_shoelace(imagen)
    margen = max(max(xs) - min(xs), max(ys) - min(ys), 1.0) * 0.12
    fig.update_layout(
        xaxis=_eje("x", range=[min(xs) - margen, max(xs) + margen], zeroline=True),
        yaxis=_eje("y", range=[min(ys) - margen, max(ys) + margen], zeroline=True, scaleanchor="x"))
    texto_det = f"det(A) = {float(det):.6g}"
    if det == 0:
        mensaje = ("det(A) = 0: el paralelogramo degenera en un segmento; el área es 0 y A no tiene inversa.")
    else:
        mensaje = (f"{texto_det}. Área del paralelogramo = |det(A)| · 1 = {area:.6g}; "
                   f"factor de cambio de área = |det(A)| = {abs(float(det)):.6g}")
    fig.add_annotation(text=mensaje, xref="paper", yref="paper", x=0, y=1.06, showarrow=False,
                       xanchor="left", font=dict(size=12, color=COLOR_PARALELOGRAMO))
    return fig, area


def normas_barras(sumas_filas, sumas_inversa=None, sumas_columnas=None):
    """Sumas absolutas por fila de A (y de A⁻¹), con la máxima destacada: es la norma ∞.

    Si se pasan `sumas_columnas`, se añade un panel de referencia con la norma 1
    (complementaria: no interviene en κ∞)."""
    paneles = 1 + (sumas_inversa is not None) + (sumas_columnas is not None)
    fig = make_subplots(rows=1, cols=paneles, horizontal_spacing=0.12,
                        subplot_titles=_titulos_normas(sumas_inversa is not None, sumas_columnas is not None))
    _barras(fig, 1, sumas_filas, "Fila")
    col = 2
    if sumas_inversa is not None:
        _barras(fig, col, sumas_inversa, "Fila")
        col += 1
    if sumas_columnas is not None:
        _barras(fig, col, sumas_columnas, "Columna", color=COLOR_RESIDUO)
    fig.update_layout(title=dict(text="Visualización complementaria · sumas absolutas de filas (norma ∞) "
                                      "y de columnas (referencia)", x=0.01, font=dict(size=15, color=TEXTO)),
                      paper_bgcolor=FONDO, plot_bgcolor=FONDO_EJES,
                      font=dict(family=FUENTE, color=TEXTO, size=12),
                      height=380, showlegend=False, margin=dict(l=60, r=30, t=80, b=40))
    return fig


def _titulos_normas(con_inversa, con_columnas):
    titulos = ["‖A‖∞ = máx. suma de fila"]
    if con_inversa:
        titulos.append("‖A⁻¹‖∞ = máx. suma de fila")
    if con_columnas:
        titulos.append("Referencia: norma 1 (complementaria)")
    return titulos


def _barras(fig, col, valores, etiqueta, color=COLOR_RECTA):
    indice_max = max(range(len(valores)), key=lambda i: valores[i])
    etiquetas = [f"{etiqueta} {i + 1}" for i in range(len(valores))]
    colores = [COLOR_MAXIMO if i == indice_max else color for i in range(len(valores))]
    fig.add_trace(go.Bar(x=etiquetas, y=[float(v) for v in valores], marker_color=colores,
                         text=[f"{float(v):.6g}" for v in valores], textposition="outside",
                         hovertemplate="%{x}: suma = %{y:.6g}<extra></extra>"), row=1, col=col)
    fig.update_yaxes(title_text="suma de |valores|", row=1, col=col, rangemode="tozero")


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
