"""Gráficas 2D con Matplotlib.

Estas funciones SOLO dibujan resultados ya calculados por el núcleo
(algebra/): no resuelven sistemas ni ajustan rectas.  Devuelven una figura
de Matplotlib que la interfaz muestra con st.pyplot.
"""

import math

import matplotlib

matplotlib.use("Agg")  # backend sin ventanas (servidor web)
import matplotlib.pyplot as plt  # noqa: E402

COLORES = {"Jacobi": "#1f77b4", "Gauss-Seidel": "#d62728", "SOR": "#2ca02c"}


def _figura(ancho=7.0, alto=4.2):
    fig, ax = plt.subplots(figsize=(ancho, alto), dpi=110)
    ax.grid(True, alpha=0.3)
    return fig, ax


def grafica_ajuste(xs, ys, pendiente, intercepto, estimados):
    """Datos (x_i, y_i), recta y = m x + c y los residuos como segmentos verticales."""
    fig, ax = _figura()
    xs_f = [float(v) for v in xs]
    ys_f = [float(v) for v in ys]
    m, c = float(pendiente), float(intercepto)
    margen = (max(xs_f) - min(xs_f)) * 0.08 or 1.0
    x0, x1 = min(xs_f) - margen, max(xs_f) + margen
    for x, y, y_est in zip(xs_f, ys_f, estimados):
        ax.plot([x, x], [y, float(y_est)], color="#999999", linestyle=":", linewidth=1)
    ax.scatter(xs_f, ys_f, color="#d62728", zorder=3, label="Datos (xᵢ, yᵢ)")
    ax.plot([x0, x1], [m * x0 + c, m * x1 + c], color="#1f77b4", linewidth=2,
            label=f"Recta de mínimos cuadrados: y = {m:.6g}x {'+' if c >= 0 else '−'} {abs(c):.6g}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Ajuste lineal por mínimos cuadrados (líneas punteadas: residuos)")
    ax.legend(loc="best", fontsize=8)
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
    series = [("d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞", [f.d for f in historial], "o-", "#1f77b4", "A"),
              ("r_k = ‖b − Ax⁽ᵏ⁾‖∞", [f.r for f in historial], "s--", "#ff7f0e", "B")]
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
                       label=f"{nombre.split(' =')[0]} = 0 exactamente")
            hay_datos = True
    if tolerancia is not None and criterio in ("A", "B"):
        ax.axhline(float(tolerancia), color="#2ca02c", linestyle="-.", linewidth=1.2,
                   label=f"ε = {float(tolerancia):.3g}")
    if hay_datos:
        ax.set_yscale("log")
    ax.set_xlabel("Iteración k")
    ax.set_ylabel("Valor (escala logarítmica)")
    ax.set_title("Evolución del cambio entre iteraciones y del residuo")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    return fig


def grafica_comparacion(resultados, metrica, errores_historial=None):
    """Curvas superpuestas de Jacobi, Gauss-Seidel y SOR para la métrica elegida:
    'd' (cambio), 'r' (residuo) o 'e' (error respecto a la solución del método directo)."""
    fig, ax = _figura()
    titulos = {"d": "Cambio entre iteraciones d_k", "r": "Residuo r_k",
               "e": "Error respecto a la solución del método directo e_k"}
    hay_datos = False
    for indice, r in enumerate(resultados):
        if not r.historial:
            continue
        ks = [f.k for f in r.historial]
        if metrica == "d":
            valores = [f.d for f in r.historial]
        elif metrica == "r":
            valores = [f.r for f in r.historial]
        else:
            if not errores_historial or errores_historial[indice] is None:
                continue
            valores = errores_historial[indice]
        puntos, _ = _positivos(ks, valores)
        if not puntos:
            continue
        hay_datos = True
        nombre = r.configuracion.metodo
        if nombre == "SOR":
            nombre += f" (ω = {float(r.configuracion.omega):.3g})"
        ax.plot([p[0] for p in puntos], [p[1] for p in puntos], "o-", markersize=3,
                color=COLORES.get(r.configuracion.metodo), label=nombre)
    if hay_datos:
        ax.set_yscale("log")
    ax.set_xlabel("Iteración k")
    ax.set_ylabel(titulos[metrica] + " (escala log.)")
    ax.set_title("Comparación de métodos: " + titulos[metrica])
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    return fig


def grafica_autovalores(autovalores, rho):
    """Autovalores de T en el plano complejo junto con el círculo unidad |λ| = 1."""
    fig, ax = _figura(5.0, 5.0)
    angulos = [2 * math.pi * k / 200 for k in range(201)]
    ax.plot([math.cos(t) for t in angulos], [math.sin(t) for t in angulos],
            color="#2ca02c", label="|λ| = 1")
    ax.plot([rho * math.cos(t) for t in angulos], [rho * math.sin(t) for t in angulos],
            color="#d62728", linestyle="--", linewidth=1, label=f"|λ| = ρ(T) = {rho:.4g}")
    ax.scatter([z.real for z in autovalores], [z.imag for z in autovalores],
               color="#1f77b4", zorder=3, label="Autovalores de T")
    limite = max(1.2, rho * 1.2)
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_aspect("equal")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginaria")
    ax.set_title("Autovalores de la matriz de iteración")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def cerrar(fig):
    """Libera la memoria de una figura ya mostrada."""
    plt.close(fig)
