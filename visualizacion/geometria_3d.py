"""Visualización geométrica de sistemas de 2 y 3 incógnitas (Matplotlib).

Cada ecuación a_i1 x + a_i2 y + a_i3 z = b_i es un plano de R³ (o una recta
de R² si hay 2 incógnitas).  La clasificación del sistema (S6-14/09 p. 26):
  * solución única     -> los planos se cortan en un punto;
  * infinitas          -> comparten una recta o un plano;
  * inconsistente      -> no hay ningún punto común a todos.

La gráfica se construye con los datos y con el resultado de NUESTRO método
directo (punto o recta paramétrica); Matplotlib solo dibuja.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from visualizacion.tema import COLOR_SOLUCION, COLORES_PLANOS, FONDO_EJES


def _centro_y_radio(resultado):
    """Elige la región a dibujar alrededor de la solución (o del origen)."""
    if resultado.solucion is not None:
        centro = [float(v) for v in resultado.solucion]
    elif resultado.solucion_particular is not None:
        centro = [float(v) for v in resultado.solucion_particular]
    else:
        centro = [0.0] * resultado.n_incognitas
    radio = max(3.0, max(abs(v) for v in centro) * 0.6)
    return centro, radio


def _esquinas_plano(a, b_i, centro, radio):
    """Devuelve las 4 esquinas de una porción cuadrada del plano a·(x,y,z) = b_i.

    Se despeja la variable con mayor |coeficiente| para que también funcionen
    los planos verticales (por ejemplo, cuando el coeficiente de z es 0).
    Se usan listas de Python (Poly3DCollection las acepta), sin NumPy.
    """
    k = max(range(3), key=lambda j: abs(a[j]))
    otros = [j for j in range(3) if j != k]
    esquinas = []
    for u, v in ((-radio, -radio), (radio, -radio), (radio, radio), (-radio, radio)):
        punto = [0.0, 0.0, 0.0]
        punto[otros[0]] = centro[otros[0]] + u
        punto[otros[1]] = centro[otros[1]] + v
        punto[k] = (b_i - a[otros[0]] * punto[otros[0]] - a[otros[1]] * punto[otros[1]]) / a[k]
        esquinas.append(tuple(punto))
    return esquinas


def grafica_planos(A, b, resultado):
    """Planos de un sistema de 3 incógnitas y su intersección según `resultado`
    (ResultadoSistema de algebra.directos)."""
    fig = plt.figure(figsize=(7, 6), dpi=110)
    ax = fig.add_subplot(projection="3d")
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        eje.set_pane_color(FONDO_EJES)
    centro, radio = _centro_y_radio(resultado)
    for i, fila in enumerate(A):
        a = [float(v) for v in fila]
        if all(v == 0 for v in a):
            continue  # 0 = b_i no es un plano
        color = COLORES_PLANOS[i % len(COLORES_PLANOS)]
        esquinas = _esquinas_plano(a, float(b[i]), centro, radio)
        ax.add_collection3d(Poly3DCollection([esquinas], alpha=0.35, facecolor=color,
                                             edgecolor=color))
        ax.plot([], [], color=color, linewidth=6, label=f"Ecuación {i + 1}")
    if resultado.solucion is not None:
        x, y, z = (float(v) for v in resultado.solucion)
        ax.scatter([x], [y], [z], color=COLOR_SOLUCION, edgecolor="#0B1020", s=70, depthshade=False,
                   label=f"Solución única ({x:.4g}, {y:.4g}, {z:.4g})")
    elif resultado.solucion_particular is not None and len(resultado.direcciones) == 1:
        p = [float(v) for v in resultado.solucion_particular]
        v = [float(t) for t in resultado.direcciones[0]]
        escala = radio / max(1e-12, max(abs(t) for t in v))
        # Recta x = p + t v, dibujada para t entre -escala y +escala
        extremos = [[p[j] - escala * v[j], p[j] + escala * v[j]] for j in range(3)]
        ax.plot(extremos[0], extremos[1], extremos[2],
                color=COLOR_SOLUCION, linewidth=3, label="Recta de soluciones")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(centro[0] - radio, centro[0] + radio)
    ax.set_ylim(centro[1] - radio, centro[1] + radio)
    ax.set_zlim(centro[2] - radio, centro[2] + radio)
    ax.set_title("Interpretación geométrica: cada ecuación es un plano")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    return fig


def grafica_rectas(A, b, resultado):
    """Rectas de un sistema de 2 incógnitas y su intersección."""
    fig, ax = plt.subplots(figsize=(6.5, 5), dpi=110)
    centro, radio = _centro_y_radio(resultado)
    for i, fila in enumerate(A):
        a1, a2 = float(fila[0]), float(fila[1])
        bi = float(b[i])
        color = COLORES_PLANOS[i % len(COLORES_PLANOS)]
        if a2 != 0:
            xs = [centro[0] - radio, centro[0] + radio]
            ax.plot(xs, [(bi - a1 * x) / a2 for x in xs], color=color, label=f"Ecuación {i + 1}")
        elif a1 != 0:
            ax.axvline(bi / a1, color=color, label=f"Ecuación {i + 1}")
    if resultado.solucion is not None:
        x, y = (float(v) for v in resultado.solucion)
        ax.scatter([x], [y], color=COLOR_SOLUCION, edgecolor="#0B1020", s=60, zorder=3,
                   label=f"Solución ({x:.4g}, {y:.4g})")
    ax.set_xlim(centro[0] - radio, centro[0] + radio)
    ax.set_ylim(centro[1] - radio, centro[1] + radio)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interpretación geométrica: cada ecuación es una recta")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    return fig
