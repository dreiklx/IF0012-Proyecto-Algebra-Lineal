"""Gráficas 2D con Matplotlib: figuras de referencia (no se muestran en la app).

La aplicación dibuja con Plotly (visualizacion/interactivas.py).  Estas figuras
estáticas se conservan como oráculo independiente: las pruebas comprueban que
Plotly dibuja exactamente los mismos puntos.  Aquí también viven los datos que
comparten ambas versiones (serie_metrica, _positivos, MARCADORES, TITULOS_METRICA).
Las etiquetas usan mathtext de Matplotlib ($d_k$).  SOLO dibujan resultados ya
calculados por el núcleo (algebra/): no resuelven sistemas ni ajustan rectas.
"""

import math

import matplotlib.pyplot as plt

from visualizacion.tema import (
    COLOR_DATOS,
    COLOR_EPSILON,
    COLOR_RECTA,
    COLOR_RESIDUO,
    COLORES_METODOS,
    SUAVE,
)

COLORES = COLORES_METODOS
MARCADORES = {"Jacobi": "o", "Gauss-Seidel": "s", "SOR": "^", "Richardson": "D"}


def _figura(ancho=7.6, alto=4.3):
    fig, ax = plt.subplots(figsize=(ancho, alto), dpi=120)
    return fig, ax


def _leyenda(ax, columnas=2):
    """Leyenda debajo de los ejes: no tapa ninguna curva."""
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=columnas, frameon=False)


def grafica_ajuste(xs, ys, pendiente, intercepto, estimados):
    """Datos (xᵢ, yᵢ), recta y = m x + c y los residuos como segmentos verticales."""
    fig, ax = _figura()
    xs_f = [float(v) for v in xs]
    ys_f = [float(v) for v in ys]
    m, c = float(pendiente), float(intercepto)
    margen = (max(xs_f) - min(xs_f)) * 0.08 or 1.0
    x0, x1 = min(xs_f) - margen, max(xs_f) + margen
    for x, y, y_est in zip(xs_f, ys_f, estimados):
        ax.plot([x, x], [y, float(y_est)], color=COLOR_RESIDUO, linestyle=":", linewidth=1.3)
    ax.plot([], [], color=COLOR_RESIDUO, linestyle=":", linewidth=1.3, label="Residuos rᵢ")
    ax.scatter(xs_f, ys_f, color=COLOR_DATOS, edgecolor="#0B1020", linewidth=0.8, s=46, zorder=3,
               label="Datos (xᵢ, yᵢ)")
    ax.plot([x0, x1], [m * x0 + c, m * x1 + c], color=COLOR_RECTA, linewidth=2.4,
            label=f"Recta de mínimos cuadrados: y = {m:.6g}x {'+' if c >= 0 else '−'} {abs(c):.6g}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ajuste lineal por mínimos cuadrados")
    _leyenda(ax, 3)
    fig.tight_layout()
    return fig


def _positivos(ks, valores):
    """Separa los puntos representables en escala logarítmica (valor > 0)."""
    puntos = [(k, v) for k, v in zip(ks, valores) if v is not None and v > 0]
    ceros = [k for k, v in zip(ks, valores) if v == 0]
    return puntos, ceros


def grafica_convergencia(historial, criterio, tolerancia=None):
    """d_k y r_k frente a k (escala logarítmica), con la línea ε sobre la métrica
    que actúa como criterio de parada."""
    fig, ax = _figura()
    ks = [f.k for f in historial]
    series = [(MATH["d"], [f.d for f in historial], "o-", COLOR_RECTA, "A"),
              (MATH["r"], [f.r for f in historial], "s--", COLOR_RESIDUO, "B")]
    hay_datos = False
    for nombre, valores, estilo, color, letra in series:
        puntos, ceros = _positivos(ks, valores)
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


# Nombre de cada métrica en palabras; cada formato agrega su símbolo (mathtext o HTML).
TITULOS_METRICA = {"d": "Cambio entre iteraciones", "r": "Residuo",
                   "e": "Error respecto a la solución del método directo"}
MATH = {"d": r"$d_k = \|x^{(k)} - x^{(k-1)}\|_\infty$", "r": r"$r_k = \|b - Ax^{(k)}\|_\infty$",
        "e": r"$e_k = \|x^{(k)} - x^*\|_\infty$"}


def serie_metrica(r, indice, metrica, errores_historial=None):
    """(k, valores) de la métrica 'd', 'r' o 'e' de un resultado, o None si no hay datos.
    La comparten la gráfica Matplotlib y la interactiva (Plotly)."""
    if not r.historial:
        return None
    ks = [f.k for f in r.historial]
    if metrica == "d":
        return ks, [f.d for f in r.historial]
    if metrica == "r":
        return ks, [f.r for f in r.historial]
    if not errores_historial or errores_historial[indice] is None:
        return None
    return ks, errores_historial[indice]


def grafica_comparacion(resultados, metrica, errores_historial=None):
    """Curvas superpuestas de Jacobi, Gauss-Seidel y SOR para la métrica elegida:
    'd' (cambio), 'r' (residuo) o 'e' (error respecto a la solución del método directo)."""
    fig, ax = _figura()
    titulos = TITULOS_METRICA
    hay_datos = False
    for indice, r in enumerate(resultados):
        serie = serie_metrica(r, indice, metrica, errores_historial)
        if serie is None:
            continue
        ks, valores = serie
        puntos, _ = _positivos(ks, valores)
        if not puntos:
            continue
        hay_datos = True
        nombre = r.configuracion.metodo
        if nombre == "SOR":
            nombre += f" (ω = {float(r.configuracion.omega):.3g})"
        ax.plot([p[0] for p in puntos], [p[1] for p in puntos], "-",
                marker=MARCADORES.get(r.configuracion.metodo, "o"), markersize=4,
                color=COLORES.get(r.configuracion.metodo), label=nombre)
    if hay_datos:
        ax.set_yscale("log")
    ax.set_xlabel("Iteración k")
    ax.set_ylabel(MATH[metrica] + "  (escala log.)")
    ax.set_title("Comparación de métodos: " + titulos[metrica])
    _leyenda(ax, 3)
    fig.tight_layout()
    return fig


def grafica_autovalores(autovalores, rho):
    """Autovalores de T en el plano complejo junto con el círculo unidad |λ| = 1."""
    fig, ax = _figura(5.4, 5.4)
    ax.add_patch(plt.Circle((0, 0), 1, color=COLOR_EPSILON, alpha=0.07, zorder=0))
    angulos = [2 * math.pi * k / 200 for k in range(201)]
    ax.plot([math.cos(t) for t in angulos], [math.sin(t) for t in angulos],
            color=COLOR_EPSILON, label="|λ| = 1 (frontera de convergencia)")
    ax.plot([rho * math.cos(t) for t in angulos], [rho * math.sin(t) for t in angulos],
            color="#F472B6", linestyle="--", linewidth=1.3, label=f"|λ| = ρ(T) = {rho:.4g}")
    ax.scatter([z.real for z in autovalores], [z.imag for z in autovalores],
               color=COLOR_DATOS, edgecolor="#0B1020", s=55, zorder=3, label="Autovalores de T")
    limite = max(1.2, rho * 1.2)
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_aspect("equal")
    ax.axhline(0, color=SUAVE, linewidth=0.6)
    ax.axvline(0, color=SUAVE, linewidth=0.6)
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginaria")
    ax.set_title("Autovalores de la matriz de iteración")
    _leyenda(ax, 1)
    fig.tight_layout()
    return fig


def cerrar(fig):
    """Libera la memoria de una figura ya mostrada."""
    plt.close(fig)


TOPE_GRAFICA = 1e6


def grafica_precondicionador(comparaciones):
    """d_k de cada método sobre el sistema original (línea continua) y sobre el
    precondicionado con M = D (línea discontinua).  Recibe la lista de
    ComparacionMetodo de algebra.precondicionamiento."""
    fig, ax = _figura()
    colores = COLORES
    hay_datos = False
    minimo = None
    recortado = False
    for f in comparaciones:
        for resultado, estilo, sufijo in ((f.original, "o-", "original"),
                                          (f.precondicionado, "s--", "con M = D")):
            puntos, _ = _positivos([fila.k for fila in resultado.historial],
                                   [fila.d for fila in resultado.historial])
            if not puntos:
                continue
            hay_datos = True
            recortado = recortado or max(p[1] for p in puntos) > TOPE_GRAFICA
            minimo = min([p[1] for p in puntos] + ([minimo] if minimo else []))
            ax.plot([p[0] for p in puntos], [p[1] for p in puntos], estilo, markersize=3,
                    color=colores.get(f.metodo), label=f"{f.metodo} ({sufijo})")
    if hay_datos:
        ax.set_yscale("log")
        if recortado:
            # Una curva divergente (p. ej. Richardson sin precondicionar) taparía a las demás.
            ax.set_ylim(min(minimo, 1.0) / 10, TOPE_GRAFICA)
            ax.text(0.99, 0.02, f"Eje recortado en {TOPE_GRAFICA:.0e}: hay una curva que diverge",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color=SUAVE)
    ax.set_xlabel("Iteración k")
    ax.set_ylabel(MATH["d"] + " (escala log.)")
    ax.set_title("Efecto del precondicionador diagonal M = D")
    _leyenda(ax, 4)
    fig.tight_layout()
    return fig
