"""Módulo III — Mínimos cuadrados y ajuste lineal (OFICIAL p. 2; S8-30/09 pp. 5-8).

Un sistema A x = b con A de m x n y m > n (más ecuaciones que incógnitas) es
sobredeterminado y en general inconsistente (b no pertenece al espacio
columna de A).  La solución de mínimos cuadrados x̂ minimiza ||b - A x||_2 y
satisface las ecuaciones normales

    Aᵀ A x̂ = Aᵀ b,

que se resuelven con nuestra eliminación de Gauss ("un método directo ya
implementado", OFICIAL p. 2).  Después se calcula el residuo

    r = b - A x̂     y su norma euclidiana  ||r||_2 = raíz( suma de r_i² ).

Propiedad de comprobación: Aᵀ r = 0 (el residuo es ortogonal a las columnas de A).

Si las columnas de A son linealmente dependientes, AᵀA es singular y la
solución de mínimos cuadrados no es única: se informa y no se devuelve un x̂.

Procedimiento de clase (S8-30/09 pp. 6-7), que la aplicación muestra como
verificación además del procedimiento exigido por el enunciado:
  1. si m = n + 1, det([A | b]) ≠ 0 demuestra que b no es combinación lineal de
     las columnas de A (la docente lo calcula con Sarrus para 3x2);
  2. ecuaciones normales AᵀA x = Aᵀb;
  3. resolución por la regla de Cramer: x_j = det((AᵀA)_j) / det(AᵀA), donde
     (AᵀA)_j es AᵀA con la columna j reemplazada por Aᵀb (aquí se usa para n <= 3).
La solución presentada es la de Gauss (OFICIAL p. 2: «con un método directo ya
implementado»); Cramer se calcula aparte y debe coincidir exactamente.

Ajuste lineal y = m x + c a partir de puntos (x_i, y_i): es el caso particular
con A = [[x_1, 1], ..., [x_k, 1]] (matriz de diseño) y b = (y_1, ..., y_k).
"""

import math
from dataclasses import dataclass, field

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import (
    multiplicar_matrices,
    multiplicar_matriz_vector,
    norma_2_cuadrado_vector,
    norma_infinito_vector,
    restar_vectores,
    transpuesta,
    validar_sistema,
)
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_I_sistemas.directos import (
    INCONSISTENTE,
    INFINITAS,
    UNICA,
    determinante,
    resolver_gauss,
)

SOBREDETERMINADO = "SOBREDETERMINADO"
CUADRADO = "CUADRADO"
SUBDETERMINADO = "SUBDETERMINADO"


@dataclass
class ResultadoMinimos:
    tipo: str                    # SOBREDETERMINADO / CUADRADO / SUBDETERMINADO
    mensaje_tipo: str
    b_en_espacio_columna: bool   # True si A x = b tiene solución exacta
    At: list
    AtA: list
    Atb: list
    ecuaciones_normales: object  # ResultadoSistema de Aᵀ A x = Aᵀ b
    solucion: list = None        # x̂, solo si es única
    estimados: list = None       # A x̂
    residuo: list = None         # r = b - A x̂
    norma_residuo_2_cuadrado: object = None   # exacta
    norma_residuo_2: float = None
    norma_residuo_inf: object = None
    ortogonalidad: list = None   # Aᵀ r (debe ser el vector cero)
    mensaje: str = ""
    advertencias: list = field(default_factory=list)
    det_aumentada: object = None     # det([A | b]) si m = n + 1 (procedimiento de clase)
    cramer: dict = None              # {"det": det(AᵀA), "dets": [det((AᵀA)_j)], "solucion": x}


@dataclass
class ResultadoAjuste:
    pendiente: object
    intercepto: object
    ecuacion: str
    minimos: ResultadoMinimos
    xs: list
    ys: list


class ErrorAjuste(ValueError):
    """Los datos no permiten calcular una recta de ajuste."""


def clasificar_forma(m, n):
    """Clasifica A (m x n) según la relación entre ecuaciones e incógnitas."""
    if m > n:
        return SOBREDETERMINADO, (
            f"Sistema sobredeterminado: {m} ecuaciones y {n} incógnitas (m > n).")
    if m == n:
        return CUADRADO, (
            f"Sistema cuadrado ({m} x {n}): no es sobredeterminado; si A es invertible, "
            f"la solución de mínimos cuadrados coincide con la solución exacta.")
    return SUBDETERMINADO, (
        f"Sistema subdeterminado: {m} ecuaciones y {n} incógnitas (m < n); "
        f"las ecuaciones normales no tendrán solución única.")


def minimos_cuadrados(A, b):
    """Resuelve A x ≈ b por mínimos cuadrados mediante las ecuaciones normales."""
    m, n = validar_sistema(A, b)
    A_exacta = [[a_fraccion(v) for v in fila] for fila in A]
    b_exacto = [a_fraccion(v) for v in b]
    tipo, mensaje_tipo = clasificar_forma(m, n)

    # ¿b está en el espacio columna de A?  Equivale a que A x = b sea consistente.
    consistente = resolver_gauss(A_exacta, b_exacto).clasificacion != INCONSISTENTE

    At = transpuesta(A_exacta)
    AtA = multiplicar_matrices(At, A_exacta)
    Atb = multiplicar_matriz_vector(At, b_exacto)
    normales = resolver_gauss(AtA, Atb)

    resultado = ResultadoMinimos(
        tipo=tipo, mensaje_tipo=mensaje_tipo, b_en_espacio_columna=consistente,
        At=At, AtA=AtA, Atb=Atb, ecuaciones_normales=normales)
    if m == n + 1:
        resultado.det_aumentada = determinante([A_exacta[i] + [b_exacto[i]] for i in range(m)])

    if normales.clasificacion != UNICA:
        # Las ecuaciones normales siempre son consistentes; si no hay solución
        # única es porque AᵀA es singular (columnas de A dependientes).
        resultado.mensaje = (
            "AᵀA es singular: las columnas de A son linealmente dependientes y la "
            "solución de mínimos cuadrados no es única. No se presenta un x̂.")
        resultado.advertencias.append(resultado.mensaje)
        if normales.clasificacion == INFINITAS:
            resultado.advertencias.append(
                f"Las ecuaciones normales tienen infinitas soluciones "
                f"({len(normales.variables_libres)} variable(s) libre(s)).")
        return resultado

    x = normales.solucion
    if n <= 3:
        resultado.cramer = cramer(AtA, Atb)
    estimados = multiplicar_matriz_vector(A_exacta, x)
    r = restar_vectores(b_exacto, estimados)
    resultado.solucion = x
    resultado.estimados = estimados
    resultado.residuo = r
    resultado.norma_residuo_2_cuadrado = norma_2_cuadrado_vector(r)
    resultado.norma_residuo_2 = math.sqrt(resultado.norma_residuo_2_cuadrado)
    resultado.norma_residuo_inf = norma_infinito_vector(r)
    resultado.ortogonalidad = multiplicar_matriz_vector(At, r)
    if consistente:
        resultado.mensaje = (
            "b pertenece al espacio columna de A: el sistema tiene solución exacta, "
            "x̂ la reproduce y el residuo es cero.")
    else:
        resultado.mensaje = (
            "b no pertenece al espacio columna de A (el sistema es inconsistente); "
            "x̂ es la mejor aproximación en el sentido de mínimos cuadrados.")
    return resultado


def cramer(M, v):
    """Regla de Cramer (S8-30/09 p. 7) para M x = v con M cuadrada invertible.

    Devuelve {"det": det(M), "dets": [det(M_j)], "solucion": [det(M_j)/det(M)]};
    M_j es M con la columna j reemplazada por v."""
    n = len(M)
    d = determinante(M)
    if d == 0:
        return None
    dets = [determinante([[v[i] if j == k else M[i][j] for j in range(n)] for i in range(n)])
            for k in range(n)]
    return {"det": d, "dets": dets, "solucion": [dk / d for dk in dets]}


def ajuste_lineal(xs, ys):
    """Calcula la recta y = m x + c de mínimos cuadrados para los puntos (x_i, y_i)."""
    if not isinstance(xs, list) or not isinstance(ys, list):
        raise ErrorAjuste("Los datos x e y deben ser listas de números.")
    if len(xs) != len(ys):
        raise ErrorAjuste(f"Hay {len(xs)} valores de x y {len(ys)} valores de y: deben coincidir.")
    if len(xs) < 2:
        raise ErrorAjuste("Se necesitan al menos 2 puntos para ajustar una recta.")
    xs_exactos = [a_fraccion(v) for v in xs]
    ys_exactos = [a_fraccion(v) for v in ys]
    if all(v == xs_exactos[0] for v in xs_exactos):
        raise ErrorAjuste(
            "Todos los valores de x son iguales: los puntos están en una recta vertical "
            "y no existe una recta y = m x + c que los ajuste (AᵀA sería singular).")
    diseno = [[x, 1] for x in xs_exactos]
    resultado = minimos_cuadrados(diseno, ys_exactos)
    m, c = resultado.solucion
    signo = "+" if c >= 0 else "−"
    ecuacion = f"y = {formatear_numero(m)} x {signo} {formatear_numero(abs(c))}"
    return ResultadoAjuste(pendiente=m, intercepto=c, ecuacion=ecuacion,
                           minimos=resultado, xs=xs_exactos, ys=ys_exactos)
