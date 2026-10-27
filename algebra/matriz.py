"""Operaciones matriciales básicas del proyecto IF0012.

Representación utilizada en todo el núcleo matemático:

* Una **matriz** m x n es una lista de m filas; cada fila es una lista de
  n números.  Ejemplo: [[1, 2], [3, 4]] es una matriz 2 x 2.
* Un **vector** de n componentes es una lista plana de n números.
  Ejemplo: [1, 2, 3].

Se aceptan como números los enteros (int), los reales (float) y las
fracciones exactas (fractions.Fraction).  Las operaciones conservan el tipo:
si todos los datos son enteros o fracciones, el resultado es exacto.

Ninguna función modifica sus argumentos: siempre se devuelve una lista nueva.
Todas las operaciones se implementan con ciclos explícitos y aritmética
elemental (+, -, *, abs), sin bibliotecas externas.
"""

from fractions import Fraction
import math


class ErrorMatriz(ValueError):
    """Error de entrada: el dato no es una matriz o un vector válido."""


class ErrorDimension(ErrorMatriz):
    """Error de dimensiones: los tamaños de los operandos no son compatibles."""


# ---------------------------------------------------------------------------
# Validación
# ---------------------------------------------------------------------------

def es_numero(valor):
    """Indica si `valor` es un número aceptado por el núcleo.

    Se aceptan int, float y Fraction.  Se rechazan:
    * bool, porque True/False no son datos numéricos del problema;
    * float no finitos (inf, -inf, nan), porque no representan datos válidos.
    """
    if isinstance(valor, bool):
        return False
    if isinstance(valor, (int, Fraction)):
        return True
    if isinstance(valor, float):
        return math.isfinite(valor)
    return False


def validar_vector(v, nombre="vector"):
    """Comprueba que `v` es un vector no vacío de números y devuelve su longitud.

    Lanza ErrorMatriz si no es una lista, está vacío o contiene algo que no es
    un número válido.
    """
    if not isinstance(v, list):
        raise ErrorMatriz(f"El {nombre} debe ser una lista de números.")
    if len(v) == 0:
        raise ErrorMatriz(f"El {nombre} está vacío.")
    for i in range(len(v)):
        if not es_numero(v[i]):
            raise ErrorMatriz(
                f"La componente {i + 1} del {nombre} no es un número válido: {v[i]!r}."
            )
    return len(v)


def validar_matriz(A, nombre="matriz"):
    """Comprueba que `A` es una matriz rectangular no vacía y devuelve (m, n).

    Requisitos: lista de filas, al menos una fila, todas las filas son listas
    con la misma cantidad (al menos una) de números válidos.
    """
    if not isinstance(A, list):
        raise ErrorMatriz(f"La {nombre} debe ser una lista de filas.")
    if len(A) == 0:
        raise ErrorMatriz(f"La {nombre} está vacía.")
    m = len(A)
    n = None
    for i in range(m):
        fila = A[i]
        if not isinstance(fila, list):
            raise ErrorMatriz(f"La fila {i + 1} de la {nombre} no es una lista.")
        if len(fila) == 0:
            raise ErrorMatriz(f"La fila {i + 1} de la {nombre} está vacía.")
        if n is None:
            n = len(fila)
        elif len(fila) != n:
            raise ErrorDimension(
                f"La fila {i + 1} de la {nombre} tiene {len(fila)} elementos; "
                f"se esperaban {n} (todas las filas deben tener el mismo tamaño)."
            )
        for j in range(n):
            if not es_numero(fila[j]):
                raise ErrorMatriz(
                    f"El elemento ({i + 1}, {j + 1}) de la {nombre} no es un "
                    f"número válido: {fila[j]!r}."
                )
    return m, n


def dimensiones(A):
    """Devuelve (filas, columnas) de una matriz válida."""
    return validar_matriz(A)


def es_cuadrada(A):
    """Indica si la matriz (válida) tiene el mismo número de filas y columnas."""
    m, n = validar_matriz(A)
    return m == n


def validar_cuadrada(A, nombre="matriz"):
    """Comprueba que `A` es cuadrada y devuelve su orden n."""
    m, n = validar_matriz(A, nombre)
    if m != n:
        raise ErrorDimension(f"La {nombre} es {m}x{n}: debe ser cuadrada.")
    return n


def validar_sistema(A, b):
    """Comprueba que A x = b tiene dimensiones compatibles y devuelve (m, n).

    A es m x n y b debe tener m componentes (una por ecuación).
    """
    m, n = validar_matriz(A, "matriz A")
    largo_b = validar_vector(b, "vector b")
    if largo_b != m:
        raise ErrorDimension(
            f"A tiene {m} filas pero b tiene {largo_b} componentes: deben coincidir."
        )
    return m, n


# ---------------------------------------------------------------------------
# Operaciones
# ---------------------------------------------------------------------------

def transpuesta(A):
    """Devuelve la transpuesta de A: el elemento (i, j) pasa a la posición (j, i).

    Si A es m x n, el resultado es n x m.
    """
    m, n = validar_matriz(A)
    T = []
    for j in range(n):
        fila_nueva = []
        for i in range(m):
            fila_nueva.append(A[i][j])
        T.append(fila_nueva)
    return T


def _comprobar_mismo_tamano(A, B, operacion):
    """Valida A y B y exige que tengan las mismas dimensiones."""
    dim_a = validar_matriz(A, "primera matriz")
    dim_b = validar_matriz(B, "segunda matriz")
    if dim_a != dim_b:
        raise ErrorDimension(
            f"No se puede {operacion} una matriz {dim_a[0]}x{dim_a[1]} con una "
            f"{dim_b[0]}x{dim_b[1]}: deben tener las mismas dimensiones."
        )
    return dim_a


def sumar_matrices(A, B):
    """Devuelve A + B, sumando elemento a elemento.  Requiere el mismo tamaño."""
    m, n = _comprobar_mismo_tamano(A, B, "sumar")
    C = []
    for i in range(m):
        fila = []
        for j in range(n):
            fila.append(A[i][j] + B[i][j])
        C.append(fila)
    return C


def restar_matrices(A, B):
    """Devuelve A - B, restando elemento a elemento.  Requiere el mismo tamaño."""
    m, n = _comprobar_mismo_tamano(A, B, "restar")
    C = []
    for i in range(m):
        fila = []
        for j in range(n):
            fila.append(A[i][j] - B[i][j])
        C.append(fila)
    return C


def multiplicar_matrices(A, B):
    """Devuelve el producto A B.

    Si A es m x p y B es p x n, el resultado C es m x n con
        C[i][j] = suma de A[i][k] * B[k][j] para k = 0, ..., p-1.
    El número de columnas de A debe coincidir con el número de filas de B.
    """
    m, p = validar_matriz(A, "primera matriz")
    p_b, n = validar_matriz(B, "segunda matriz")
    if p != p_b:
        raise ErrorDimension(
            f"No se puede multiplicar una matriz {m}x{p} por una {p_b}x{n}: "
            f"las columnas de la primera ({p}) deben coincidir con las filas "
            f"de la segunda ({p_b})."
        )
    C = []
    for i in range(m):
        fila = []
        for j in range(n):
            acumulado = 0
            for k in range(p):
                acumulado = acumulado + A[i][k] * B[k][j]
            fila.append(acumulado)
        C.append(fila)
    return C


def multiplicar_matriz_vector(A, x):
    """Devuelve el vector A x.

    Si A es m x n y x tiene n componentes, el resultado y tiene m componentes:
        y[i] = suma de A[i][j] * x[j] para j = 0, ..., n-1.
    """
    m, n = validar_matriz(A, "matriz")
    largo_x = validar_vector(x, "vector")
    if largo_x != n:
        raise ErrorDimension(
            f"No se puede multiplicar una matriz {m}x{n} por un vector de "
            f"{largo_x} componentes: el vector debe tener {n}."
        )
    y = []
    for i in range(m):
        acumulado = 0
        for j in range(n):
            acumulado = acumulado + A[i][j] * x[j]
        y.append(acumulado)
    return y


def norma_infinito_vector(v):
    """Devuelve la norma infinito de v: el mayor valor absoluto de sus componentes.

        ||v||_inf = max |v_i|

    Ejemplo: ||(-2, 1, 7)||_inf = 7.
    """
    validar_vector(v)
    mayor = abs(v[0])
    for i in range(1, len(v)):
        if abs(v[i]) > mayor:
            mayor = abs(v[i])
    return mayor


def norma_infinito_matriz(A):
    """Devuelve la norma infinito de A: la mayor suma de valores absolutos por fila.

        ||A||_inf = max_i  sum_j |a_ij|

    (S7-21/09 p. 17: "norma inf = máxima suma de fila").
    Ejemplo: A = [[1, 2], [3, 1]]  ->  filas: 1+2 = 3, 3+1 = 4  ->  ||A||_inf = 4.
    """
    m, n = validar_matriz(A)
    mayor = None
    for i in range(m):
        suma_fila = 0
        for j in range(n):
            suma_fila = suma_fila + abs(A[i][j])
        if mayor is None or suma_fila > mayor:
            mayor = suma_fila
    return mayor


def producto_escalar(u, v):
    """Devuelve u · v = suma de u_i v_i.  Ambos vectores deben tener la misma longitud."""
    n = validar_vector(u, "primer vector")
    if validar_vector(v, "segundo vector") != n:
        raise ErrorDimension(
            f"El producto escalar requiere vectores de la misma longitud "
            f"({n} y {len(v)})."
        )
    acumulado = 0
    for i in range(n):
        acumulado = acumulado + u[i] * v[i]
    return acumulado


def sumar_vectores(u, v):
    """Devuelve u + v componente a componente."""
    n = validar_vector(u, "primer vector")
    if validar_vector(v, "segundo vector") != n:
        raise ErrorDimension(f"No se pueden sumar vectores de longitud {n} y {len(v)}.")
    return [u[i] + v[i] for i in range(n)]


def restar_vectores(u, v):
    """Devuelve u - v componente a componente."""
    n = validar_vector(u, "primer vector")
    if validar_vector(v, "segundo vector") != n:
        raise ErrorDimension(f"No se pueden restar vectores de longitud {n} y {len(v)}.")
    return [u[i] - v[i] for i in range(n)]


def norma_2_cuadrado_vector(v):
    """Devuelve ||v||_2^2 = suma de v_i^2.  Es exacta si v tiene enteros o fracciones."""
    validar_vector(v)
    acumulado = 0
    for i in range(len(v)):
        acumulado = acumulado + v[i] * v[i]
    return acumulado


def norma_2_vector(v):
    """Devuelve la norma euclidiana ||v||_2 = raíz de (suma de v_i^2), como float.

    La raíz cuadrada (math.sqrt) es la única operación no exacta; por eso
    también se ofrece norma_2_cuadrado_vector, que conserva el valor exacto.
    """
    return math.sqrt(norma_2_cuadrado_vector(v))


def identidad(n):
    """Devuelve la matriz identidad n x n (enteros 1 en la diagonal, 0 fuera)."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ErrorMatriz("El orden de la identidad debe ser un entero positivo.")
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def copiar_matriz(A):
    """Devuelve una copia independiente de A (modificarla no altera A)."""
    validar_matriz(A)
    return [list(fila) for fila in A]


def residuo(A, x, b):
    """Devuelve el vector residuo r = b - A x del sistema A x = b.

    Si x es una solución exacta, r es el vector cero.
    Requiere A de m x n, x de n componentes y b de m componentes.
    """
    m, n = validar_sistema(A, b)
    Ax = multiplicar_matriz_vector(A, x)
    r = []
    for i in range(m):
        r.append(b[i] - Ax[i])
    return r


def norma_residuo_infinito(A, x, b):
    """Devuelve ||b - A x||_inf, la medida del residuo usada en el proyecto."""
    return norma_infinito_vector(residuo(A, x, b))
