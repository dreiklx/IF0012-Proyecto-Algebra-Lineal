"""Datos que se dibujan, preparados sin ninguna biblioteca de gráficos.

Las gráficas de Plotly (interactivas.py) y la figura de referencia de Matplotlib
(referencia_matplotlib.py) usan estas mismas funciones, así que dibujan exactamente
los mismos puntos.  Aquí no se calcula ningún resultado matemático: solo se
seleccionan y ordenan datos que ya calculó el núcleo (algebra/).
"""


MARCADORES = {"Jacobi": "o", "Gauss-Seidel": "s", "SOR": "^", "Richardson": "D"}


def positivos(ks, valores):
    """Separa los puntos representables en escala logarítmica (valor > 0)."""
    puntos = [(k, v) for k, v in zip(ks, valores) if v is not None and v > 0]
    ceros = [k for k, v in zip(ks, valores) if v == 0]
    return puntos, ceros


# Nombre de cada métrica en palabras; cada formato agrega su símbolo (mathtext o HTML).
TITULOS_METRICA = {"d": "Cambio entre iteraciones", "r": "Residuo",
                   "e": "Error respecto a la solución del método directo"}


def serie_metrica(r, indice, metrica, errores_historial=None):
    """(k, valores) de la métrica 'd', 'r' o 'e' de un resultado, o None si no hay datos.
    La usa la gráfica comparativa de interactivas.py."""
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


# ---------------------------------------------------------------------------
# Geometría de la interpretación del Módulo I (rectas y planos)
# ---------------------------------------------------------------------------

def centro_y_radio(resultado):
    """Elige la región a dibujar alrededor de la solución (o del origen)."""
    if resultado.solucion is not None:
        centro = [float(v) for v in resultado.solucion]
    elif resultado.solucion_particular is not None:
        centro = [float(v) for v in resultado.solucion_particular]
    else:
        centro = [0.0] * resultado.n_incognitas
    radio = max(3.0, max(abs(v) for v in centro) * 0.6)
    return centro, radio


def esquinas_plano(a, b_i, centro, radio):
    """Devuelve las 4 esquinas de una porción cuadrada del plano a·(x,y,z) = b_i.

    Se despeja la variable con mayor |coeficiente| para que también funcionen
    los planos verticales (por ejemplo, cuando el coeficiente de z es 0).
    Se usan listas de Python, sin NumPy.
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
