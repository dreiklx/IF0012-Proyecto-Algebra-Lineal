"""Módulo I — Métodos directos: eliminación de Gauss, Gauss-Jordan e inversa.

Procedimiento (S6-14/09 pp. 27-29 y S6-16/09 pp. 24-29; inversa: S3-24/08 pp. 6, 28):

1. Se forma la matriz aumentada [A | b].
2. Para cada columna se busca un pivote no nulo.  Si el elemento de la
   diagonal es cero se intercambian filas (Fi <-> Fj).  Si en toda la columna
   (desde la fila actual hacia abajo) no hay elemento no nulo, esa columna no
   tiene pivote: su variable será una variable libre.
3. Con operaciones elementales Fi -> Fi - m·Fr se anulan los elementos bajo
   el pivote (Gauss).  Gauss-Jordan además divide la fila del pivote entre
   el pivote y anula también los elementos de arriba (forma escalonada reducida).
4. Clasificación por rangos (criterio de Rouché-Frobenius):
     rango(A) < rango([A|b])            -> sistema inconsistente;
     rango(A) = rango([A|b]) = n        -> solución única;
     rango(A) = rango([A|b]) < n        -> infinitas soluciones,
                                           con n - rango variables libres.
   En la práctica: una fila [0 ... 0 | c] con c != 0 indica inconsistencia.

Toda la aritmética es exacta (fractions.Fraction), por lo que la
clasificación no depende de tolerancias: un pivote es nulo solo si es
exactamente 0.  Los números float que se reciban se convierten primero al
decimal que representan (por ejemplo 0.1 -> 1/10).
"""

from dataclasses import dataclass, field
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import (
    identidad,
    multiplicar_matrices,
    validar_cuadrada,
    validar_sistema,
)
from algebra.compartido.validacion import formatear_numero

UNICA = "UNICA"
INFINITAS = "INFINITAS"
INCONSISTENTE = "INCONSISTENTE"

PIVOTEO_PRIMER_NO_NULO = "primer_no_nulo"

# Umbral técnico de advertencia (no matemático): un pivote cuyo valor absoluto
# es menor que UMBRAL_PIVOTE_PEQUENO veces el mayor |a_ij| de la matriz
# original se señala como "numéricamente problemático".  Con aritmética exacta
# el resultado sigue siendo correcto, pero en punto flotante ese pivote
# amplificaría los errores de redondeo.
UMBRAL_PIVOTE_PEQUENO = Fraction(1, 10**10)


@dataclass
class Paso:
    """Una operación del procedimiento y el estado de la matriz después de ella.

    `notacion` es la misma operación escrita como la profesora en sus manuscritos
    (S3-24/08 pp. 4-5; S6-16/09 p. 29): el múltiplo de la fila pivote más la fila
    que cambia («−2F₁ + F₂»), la normalización del pivote («−⅓F₃» → «(−1/3)F₃»)
    y el intercambio «F₂ ↔ F₁».  Es solo texto: no interviene en el cálculo.
    """
    descripcion: str
    matriz: list
    notacion: str = ""


@dataclass
class ResultadoSistema:
    metodo: str
    clasificacion: str
    mensaje: str
    n_incognitas: int
    rango_A: int
    rango_aumentada: int
    solucion: list = None              # solo si la solución es única
    solucion_particular: list = None   # solo si hay infinitas soluciones
    direcciones: list = field(default_factory=list)   # x = xp + t1 v1 + ...
    variables_libres: list = field(default_factory=list)  # índices desde 0
    pasos: list = field(default_factory=list)
    sustitucion: list = field(default_factory=list)   # texto de la sustitución
    advertencias: list = field(default_factory=list)
    matriz_final: list = None
    determinante: Fraction = None      # solo si A es cuadrada


@dataclass
class ResultadoInversa:
    invertible: bool
    mensaje: str
    inversa: list = None
    determinante: Fraction = None
    pasos: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)
    verificacion_identidad: bool = None   # True si A·A^-1 = I exactamente


class ErrorSistema(ValueError):
    """El sistema no tiene solución única (lo usan otros módulos)."""

    def __init__(self, resultado):
        super().__init__(resultado.mensaje)
        self.resultado = resultado


# Utilidades internas

def _copiar(M):
    return [list(fila) for fila in M]


def _texto_fila(i):
    return f"F{i + 1}"


_SUBINDICES = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _fila_clase(i):
    """F₁, F₂, ... con subíndice, como en los manuscritos."""
    return "F" + str(i + 1).translate(_SUBINDICES)


def _coeficiente_clase(k):
    """Múltiplo escrito delante de la fila: 1 -> '', -1 -> '−', 1/3 -> '(1/3)'."""
    if k == 1:
        return ""
    if k == -1:
        return "−"
    texto = formatear_numero(k).replace("-", "−")
    return f"({texto})" if "/" in texto else texto


def _notacion_combinacion(i, factor, r):
    """Fi -> Fi - factor·Fr escrita como en clase: «(−factor)Fr + Fi»."""
    return f"{_coeficiente_clase(-factor)}{_fila_clase(r)} + {_fila_clase(i)}"


def _mayor_absoluto(A):
    mayor = Fraction(0)
    for fila in A:
        for valor in fila:
            if abs(valor) > mayor:
                mayor = abs(valor)
    return mayor


def _buscar_pivote(M, fila_inicio, columna, estrategia):
    """Devuelve el índice de la fila del pivote para `columna`, o None.

    primer_no_nulo: la primera fila (desde fila_inicio) con elemento no nulo,
                    como en los ejemplos de clase (solo se intercambia si hace falta).
    """
    for p in range(fila_inicio, len(M)):
        if M[p][columna] != 0:
            return p
    return None


def _describir_combinacion(i, factor, r):
    """Texto de Fi -> Fi - factor·Fr, escrito con el signo adecuado."""
    if factor < 0:
        return f"{_texto_fila(i)} → {_texto_fila(i)} + ({formatear_numero(-factor)})·{_texto_fila(r)}"
    return f"{_texto_fila(i)} → {_texto_fila(i)} − ({formatear_numero(factor)})·{_texto_fila(r)}"


def _escalonar(M, n_columnas_pivote, estrategia, reducida, pasos, advertencias, referencia):
    """Aplica eliminación sobre M (se modifica) en las primeras `n_columnas_pivote` columnas.

    Devuelve (pivotes, signo, producto_pivotes):
      pivotes          lista de (fila, columna) de cada pivote encontrado;
      signo            (-1)^(número de intercambios), para el determinante;
      producto_pivotes producto de los pivotes antes de normalizar.
    Si `reducida` es True hace Gauss-Jordan (pivote 1 y ceros arriba y abajo).
    """
    if estrategia != PIVOTEO_PRIMER_NO_NULO:
        raise ValueError(f"Estrategia de pivoteo desconocida: {estrategia}")
    m = len(M)
    fila = 0
    pivotes = []
    signo = 1
    producto = Fraction(1)
    for c in range(n_columnas_pivote):
        if fila >= m:
            break
        p = _buscar_pivote(M, fila, c, estrategia)
        if p is None:
            continue  # columna sin pivote -> variable libre
        if p != fila:
            M[fila], M[p] = M[p], M[fila]
            signo = -signo
            motivo = f"el elemento ({fila + 1}, {c + 1}) es 0"
            pasos.append(Paso(f"{_texto_fila(fila)} ↔ {_texto_fila(p)}  ({motivo})", _copiar(M),
                              f"{_fila_clase(fila)} ↔ {_fila_clase(p)}"))
        pivote = M[fila][c]
        producto = producto * pivote
        if referencia > 0 and abs(pivote) < UMBRAL_PIVOTE_PEQUENO * referencia:
            advertencias.append(
                f"Pivote numéricamente problemático en la columna {c + 1}: "
                f"|{formatear_numero(pivote)}| es muy pequeño respecto a los datos. "
                f"Con aritmética exacta el resultado es correcto, pero en punto "
                f"flotante este pivote amplificaría los errores de redondeo."
            )
        if reducida and pivote != 1:
            M[fila] = [valor / pivote for valor in M[fila]]
            pasos.append(Paso(
                f"{_texto_fila(fila)} → {_texto_fila(fila)} ÷ ({formatear_numero(pivote)})"
                f"  (pivote = 1)", _copiar(M),
                f"{_coeficiente_clase(1 / pivote)}{_fila_clase(fila)}"))
        filas_a_anular = range(m) if reducida else range(fila + 1, m)
        for i in filas_a_anular:
            if i == fila or M[i][c] == 0:
                continue
            factor = M[i][c] / M[fila][c]
            M[i] = [M[i][j] - factor * M[fila][j] for j in range(len(M[i]))]
            pasos.append(Paso(_describir_combinacion(i, factor, fila), _copiar(M),
                              _notacion_combinacion(i, factor, fila)))
        pivotes.append((fila, c))
        fila += 1
    return pivotes, signo, producto


def _rango_aumentada(M, rango_A, n):
    """rango([A|b]) = rango(A) + 1 si existe una fila [0 ... 0 | c] con c != 0."""
    for i in range(rango_A, len(M)):
        if all(M[i][j] == 0 for j in range(n)) and M[i][n] != 0:
            return rango_A + 1, i
    return rango_A, None


def _sustitucion_atras(U, pivotes, n, libres_valores, columna_b=True):
    """Resuelve un sistema escalonado por sustitución hacia atrás.

    `libres_valores` fija el valor de cada variable libre (dict índice -> valor).
    Si columna_b es False se resuelve el sistema homogéneo (lado derecho 0).
    Devuelve (x, textos) con la explicación de cada despeje.
    """
    x = [None] * n
    for j, valor in libres_valores.items():
        x[j] = valor
    textos = []
    for fila, c in reversed(pivotes):
        lado = U[fila][n] if columna_b else Fraction(0)
        suma = Fraction(0)
        for j in range(c + 1, n):
            suma = suma + U[fila][j] * x[j]
        x[c] = (lado - suma) / U[fila][c]
        textos.append(
            f"x{c + 1} = ({formatear_numero(lado)} − ({formatear_numero(suma)})) / "
            f"{formatear_numero(U[fila][c])} = {formatear_numero(x[c])}"
        )
    return x, textos


# Resolución de sistemas

def _resolver(A, b, metodo, estrategia):
    m, n = validar_sistema(A, b)
    A_exacta = [[a_fraccion(v) for v in fila] for fila in A]
    b_exacto = [a_fraccion(v) for v in b]
    M = [A_exacta[i] + [b_exacto[i]] for i in range(m)]
    pasos = [Paso("Matriz aumentada inicial [A | b]", _copiar(M))]
    advertencias = []
    reducida = metodo == "Gauss-Jordan"
    pivotes, signo, producto = _escalonar(
        M, n, estrategia, reducida, pasos, advertencias, _mayor_absoluto(A_exacta))
    rango_A = len(pivotes)
    rango_Ab, fila_inconsistente = _rango_aumentada(M, rango_A, n)

    determinante = None
    if m == n:
        determinante = signo * producto if rango_A == n else Fraction(0)

    columnas_pivote = [c for _, c in pivotes]
    libres = [j for j in range(n) if j not in columnas_pivote]
    resultado = ResultadoSistema(
        metodo=metodo, clasificacion="", mensaje="", n_incognitas=n,
        rango_A=rango_A, rango_aumentada=rango_Ab, variables_libres=libres,
        pasos=pasos, advertencias=advertencias, matriz_final=_copiar(M),
        determinante=determinante)

    if rango_Ab > rango_A:
        resultado.clasificacion = INCONSISTENTE
        resultado.mensaje = (
            f"Sistema inconsistente (sin solución): la fila {fila_inconsistente + 1} "
            f"quedó como [0 … 0 | {formatear_numero(M[fila_inconsistente][n])}], es decir "
            f"0 = {formatear_numero(M[fila_inconsistente][n])}. "
            f"rango(A) = {rango_A} < rango([A|b]) = {rango_Ab}."
        )
        return resultado

    x, textos = _sustitucion_atras(M, pivotes, n, {j: Fraction(0) for j in libres})
    if not libres:
        resultado.clasificacion = UNICA
        resultado.solucion = x
        resultado.sustitucion = textos
        resultado.mensaje = (
            f"Solución única: rango(A) = rango([A|b]) = {rango_A} = número de incógnitas."
        )
        return resultado

    resultado.clasificacion = INFINITAS
    resultado.solucion_particular = x
    resultado.sustitucion = textos
    for j in libres:
        # Dirección: solución del sistema homogéneo con la libre j = 1 y las demás = 0.
        valores = {k: Fraction(1 if k == j else 0) for k in libres}
        v, _ = _sustitucion_atras(M, pivotes, n, valores, columna_b=False)
        resultado.direcciones.append(v)
    nombres = ", ".join(f"x{j + 1}" for j in libres)
    resultado.mensaje = (
        f"Infinitas soluciones: rango(A) = rango([A|b]) = {rango_A} < {n} incógnitas. "
        f"Hay {len(libres)} variable(s) libre(s): {nombres}."
    )
    return resultado


def resolver_gauss(A, b, pivoteo=PIVOTEO_PRIMER_NO_NULO):
    """Resuelve A x = b por eliminación de Gauss y sustitución hacia atrás."""
    return _resolver(A, b, "Gauss", pivoteo)


def resolver_gauss_jordan(A, b, pivoteo=PIVOTEO_PRIMER_NO_NULO):
    """Resuelve A x = b llevando [A|b] a la forma escalonada reducida."""
    return _resolver(A, b, "Gauss-Jordan", pivoteo)


def solucion_unica(A, b, pivoteo=PIVOTEO_PRIMER_NO_NULO):
    """Devuelve la solución de A x = b o lanza ErrorSistema si no es única.

    La usan los módulos de condicionamiento y mínimos cuadrados, que exigen
    solución única ("con un método directo ya implementado", OFICIAL p. 2).
    """
    resultado = resolver_gauss(A, b, pivoteo)
    if resultado.clasificacion != UNICA:
        raise ErrorSistema(resultado)
    return resultado.solucion


# Inversa por Gauss-Jordan

def inversa_gauss_jordan(A, pivoteo=PIVOTEO_PRIMER_NO_NULO):
    """Calcula A^-1 llevando [A | I] a [I | A^-1] (S3-24/08 pp. 6 y 28).

    Si en alguna columna no existe pivote no nulo, A es singular y no tiene
    inversa ("si no existe pivote no nulo, A^-1 no existe").
    """
    n = validar_cuadrada(A, "matriz A")
    A_exacta = [[a_fraccion(v) for v in fila] for fila in A]
    I = identidad(n)
    M = [A_exacta[i] + [Fraction(v) for v in I[i]] for i in range(n)]
    pasos = [Paso("Matriz inicial [A | I]", _copiar(M))]
    advertencias = []
    pivotes, signo, producto = _escalonar(
        M, n, pivoteo, True, pasos, advertencias, _mayor_absoluto(A_exacta))
    if len(pivotes) < n:
        columna = next(c for c in range(n) if c not in [c2 for _, c2 in pivotes])
        return ResultadoInversa(
            invertible=False,
            mensaje=(f"A es singular (no invertible): la columna {columna + 1} no tiene "
                     f"pivote no nulo. rango(A) = {len(pivotes)} < {n}; det(A) = 0."),
            determinante=Fraction(0), pasos=pasos, advertencias=advertencias)
    inversa = [fila[n:] for fila in M]
    verificacion = multiplicar_matrices(A_exacta, inversa) == [
        [Fraction(v) for v in fila] for fila in I]
    return ResultadoInversa(
        invertible=True,
        mensaje="A es invertible; se verificó A·A⁻¹ = I." if verificacion
        else "Se obtuvo una inversa pero A·A⁻¹ ≠ I (error interno).",
        inversa=inversa, determinante=signo * producto, pasos=pasos,
        advertencias=advertencias, verificacion_identidad=verificacion)


def determinante(A):
    """det(A) por eliminación: (−1)^intercambios · producto de los pivotes.

    Usa la propiedad "sumar a una fila un múltiplo de otra no cambia el
    determinante" (S3-24/08 p. 22).  Devuelve 0 si A es singular.
    """
    n = validar_cuadrada(A, "matriz A")
    M = [[a_fraccion(v) for v in fila] for fila in A]
    pivotes, signo, producto = _escalonar(M, n, PIVOTEO_PRIMER_NO_NULO, False, [], [], Fraction(0))
    return signo * producto if len(pivotes) == n else Fraction(0)
