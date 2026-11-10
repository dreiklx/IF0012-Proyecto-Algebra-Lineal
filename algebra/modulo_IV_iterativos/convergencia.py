"""Módulo IV — Dominancia diagonal y reordenamiento de ecuaciones.

Criterio de clase (S8-30/09 p. 37): A es estrictamente diagonalmente dominante
por filas si |a_ii| > Σ_{j≠i} |a_ij| para todo i.  Es una condición SUFICIENTE
de convergencia de Jacobi y Gauss-Seidel.  Si no se cumple, la docente
reordena las ecuaciones (Tarea II #2-3; S9-05/10 p. 32).

El otro criterio, ρ(T) < 1, está en espectral.py.
"""

from dataclasses import dataclass

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import validar_cuadrada, validar_vector
from algebra.compartido.validacion import ErrorEntrada


@dataclass
class ResultadoDominancia:
    estricta: bool
    filas: list          # (i, |a_ii|, suma |a_ij| j≠i, cumple)
    mensaje: str


def dominancia_diagonal(A):
    """Comprueba la dominancia diagonal estricta por filas: |a_ii| > Σ_{j≠i} |a_ij|.

    Es una condición SUFICIENTE (no necesaria): si se cumple, Jacobi y
    Gauss-Seidel convergen para cualquier x(0); si no se cumple, no se puede
    concluir nada y hace falta otro análisis (por ejemplo el radio espectral).
    """
    n = validar_cuadrada(A, "matriz A")
    filas = []
    for i in range(n):
        diagonal = abs(a_fraccion(A[i][i]))
        suma = sum(abs(a_fraccion(A[i][j])) for j in range(n) if j != i)
        filas.append((i, diagonal, suma, diagonal > suma))
    estricta = all(f[3] for f in filas)
    if estricta:
        mensaje = ("A es estrictamente diagonalmente dominante por filas: Jacobi y "
                   "Gauss-Seidel convergen para cualquier vector inicial (condición suficiente).")
    else:
        malas = ", ".join(str(f[0] + 1) for f in filas if not f[3])
        mensaje = (f"A no es estrictamente diagonalmente dominante por filas (fallan las filas "
                   f"{malas}). Esto NO implica que los métodos diverjan: la dominancia es solo "
                   f"una condición suficiente; analice el radio espectral o reordene las ecuaciones.")
    return ResultadoDominancia(estricta=estricta, filas=filas, mensaje=mensaje)


def reordenamiento_dominante(A, b):
    """Busca un reordenamiento de las ECUACIONES (filas de A y de b) que haga A
    estrictamente diagonalmente dominante por filas, como en clase (Tarea II #2-3;
    S9-05/10 p. 32).  No modifica nada: devuelve (A_reordenada, b_reordenado, orden)
    o None si no existe.

    Si la fila i es dominante con el elemento de la columna j, entonces
    2|a_ij| > Σ_k |a_ik|; como esto solo lo cumple a lo sumo una columna por fila,
    basta con asignar a cada fila su única columna candidata y comprobar que la
    asignación es una permutación (coste O(n²), sin búsqueda exhaustiva)."""
    n = validar_cuadrada(A, "matriz A")
    if validar_vector(b, "vector b") != n:
        raise ErrorEntrada(f"b debe tener {n} componentes (A es {n}x{n}).")
    posicion = [None] * n          # posicion[j] = fila original que irá a la fila j
    for i in range(n):
        fila = [abs(a_fraccion(v)) for v in A[i]]
        total = sum(fila)
        candidatas = [j for j in range(n) if 2 * fila[j] > total]
        if not candidatas or posicion[candidatas[0]] is not None:
            return None
        posicion[candidatas[0]] = i
    return [list(A[i]) for i in posicion], [b[i] for i in posicion], posicion
