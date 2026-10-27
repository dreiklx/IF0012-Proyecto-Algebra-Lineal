"""Módulo IV — Métodos iterativos: Jacobi, Gauss-Seidel y SOR (OFICIAL p. 2).

Fórmulas por componentes (A = D + L + U; i = 1..n en orden):

  Jacobi        (S8-30/09 p. 15)
      x_i(k) = ( b_i - Σ_{j≠i} a_ij x_j(k-1) ) / a_ii

  Gauss-Seidel  (S8-30/09 p. 22) — usa los valores ya actualizados
      x_i(k) = ( b_i - Σ_{j<i} a_ij x_j(k) - Σ_{j>i} a_ij x_j(k-1) ) / a_ii

  SOR           (S8-30/09 p. 28) — combina el valor anterior y el de Gauss-Seidel
      x_i(k) = (1-ω) x_i(k-1) + ω · ( b_i - Σ_{j<i} a_ij x_j(k) - Σ_{j>i} a_ij x_j(k-1) ) / a_ii

Métricas que se registran en CADA iteración, sea cual sea el criterio:
  d_k = ||x(k) - x(k-1)||∞   (cambio entre iteraciones; no existe para k = 0)
  r_k = ||b - A x(k)||∞      (residuo del sistema ORIGINAL introducido)

Criterios de parada (elegidos por el usuario; desigualdad estricta):
  A  cambio:     se detiene en el primer k >= 1 con d_k < ε     (o al llegar a k_max)
  B  residuo:    se detiene en el primer k >= 0 con r_k < ε     (o al llegar a k_max)
  C  iteraciones: ejecuta exactamente N iteraciones (no demuestra convergencia)

El criterio A es el que la docente usa con más frecuencia
(S8-30/09 pp. 18, 23, 29, 34, 39, 40; S9-05/10 pp. 18, 26).

La aritmética de este módulo es de punto flotante (float): las iteraciones
son aproximaciones que se cortan por tolerancia.

El paso de cada método está separado del mecanismo común de iteración y
parada (función `ejecutar`), para no repetir tres veces la misma lógica.
"""

import math
from dataclasses import dataclass, field, replace

from algebra.directos import ErrorSistema, a_fraccion, solucion_unica
from algebra.dispersas import (
    a_csr,
    paso_gauss_seidel_csr,
    paso_jacobi_csr,
    paso_sor_csr,
    residuo_inf_csr,
)
from algebra.matriz import ErrorMatriz, es_numero, validar_cuadrada, validar_vector
from algebra.validacion import ErrorEntrada, formatear_numero

JACOBI = "Jacobi"
GAUSS_SEIDEL = "Gauss-Seidel"
SOR = "SOR"
METODOS = (JACOBI, GAUSS_SEIDEL, SOR)

CRITERIO_CAMBIO = "A"
CRITERIO_RESIDUO = "B"
CRITERIO_ITERACIONES = "C"
CRITERIOS = (CRITERIO_CAMBIO, CRITERIO_RESIDUO, CRITERIO_ITERACIONES)

DESCRIPCION_CRITERIO = {
    CRITERIO_CAMBIO: "‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε (cambio entre iteraciones)",
    CRITERIO_RESIDUO: "‖b − Ax⁽ᵏ⁾‖∞ < ε (residuo del sistema original)",
    CRITERIO_ITERACIONES: "número fijo de iteraciones N",
}

# Tope técnico (no académico) para k_max y N, para no congelar la interfaz.
K_TOPE = 100_000

# Códigos de terminación
TOLERANCIA_CAMBIO = "TOLERANCIA_CAMBIO"
TOLERANCIA_RESIDUO = "TOLERANCIA_RESIDUO"
N_COMPLETADAS = "N_COMPLETADAS"
MAXIMO_ITERACIONES = "MAXIMO_ITERACIONES"
ERROR_NO_FINITO = "ERROR_NO_FINITO"
DIAGONAL_CERO = "DIAGONAL_CERO"
ENTRADA_INVALIDA = "ENTRADA_INVALIDA"
ERROR_INTERNO = "ERROR_INTERNO"


@dataclass
class ConfiguracionIterativa:
    """Parámetros de una ejecución.

    tolerancia y k_max se usan con los criterios A y B; n_iteraciones con C;
    omega solo con SOR.  x0 es el vector inicial.
    """
    metodo: str = JACOBI
    criterio: str = CRITERIO_CAMBIO
    x0: list = None
    tolerancia: float = 1e-3
    k_max: int = 50
    n_iteraciones: int = 5
    omega: float = 1.2
    formato: str = "densa"    # "densa" o "csr" (almacenamiento disperso, algebra/dispersas.py)

    def resumen(self):
        """Texto del encabezado que muestra la configuración usada."""
        metodo = f"SOR (ω = {formatear_numero(float(a_fraccion(self.omega)))})" if self.metodo == SOR else self.metodo
        x0 = "(" + ", ".join(formatear_numero(v) for v in (self.x0 or [])) + ")"
        if self.criterio == CRITERIO_ITERACIONES:
            criterio = f"N = {self.n_iteraciones} iteraciones fijas"
            return f"Método: {metodo} · x⁽⁰⁾ = {x0} · Criterio: {criterio}"
        texto = DESCRIPCION_CRITERIO[self.criterio].split(" (")[0]
        texto = texto.replace("ε", f"ε = {formatear_numero(float(a_fraccion(self.tolerancia)))}")
        return (f"Método: {metodo} · x⁽⁰⁾ = {x0} · Criterio: {texto} · "
                f"Máximo: {self.k_max} iteraciones")


@dataclass
class FilaIteracion:
    k: int
    x: list
    d: float      # None en k = 0
    r: float


@dataclass
class ResultadoIterativo:
    configuracion: ConfiguracionIterativa
    codigo: str
    mensaje: str
    criterio_cumplido: object          # True / False / None ("no aplica")
    historial: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)
    k_error: int = None                # iteración donde aparecieron valores no finitos

    @property
    def ultima(self):
        return self.historial[-1] if self.historial else None

    @property
    def k_final(self):
        return self.ultima.k if self.ultima else None

    @property
    def x_final(self):
        return self.ultima.x if self.ultima else None

    @property
    def d_final(self):
        return self.ultima.d if self.ultima else None

    @property
    def r_final(self):
        return self.ultima.r if self.ultima else None


# ---------------------------------------------------------------------------
# Pasos de cada método (una iteración)
# ---------------------------------------------------------------------------

def paso_jacobi(A, b, x_anterior, omega=None):
    """Una iteración de Jacobi: todas las componentes usan x(k-1)."""
    n = len(A)
    x_nuevo = [0.0] * n
    for i in range(n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x_anterior[j]
        x_nuevo[i] = (b[i] - suma) / A[i][i]
    return x_nuevo


def paso_gauss_seidel(A, b, x_anterior, omega=None):
    """Una iteración de Gauss-Seidel: usa los valores ya actualizados (j < i)."""
    n = len(A)
    x = list(x_anterior)
    for i in range(n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x[j]   # x[j] ya es x_j(k) si j < i
        x[i] = (b[i] - suma) / A[i][i]
    return x


def paso_sor(A, b, x_anterior, omega):
    """Una iteración de SOR: x_i = (1-ω)·x_i(k-1) + ω·(valor de Gauss-Seidel)."""
    n = len(A)
    x = list(x_anterior)
    for i in range(n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x[j]
        valor_gs = (b[i] - suma) / A[i][i]
        x[i] = (1 - omega) * x_anterior[i] + omega * valor_gs
    return x


PASOS = {JACOBI: paso_jacobi, GAUSS_SEIDEL: paso_gauss_seidel, SOR: paso_sor}
PASOS_CSR = {JACOBI: paso_jacobi_csr, GAUSS_SEIDEL: paso_gauss_seidel_csr, SOR: paso_sor_csr}
FORMATOS = ("densa", "csr")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _a_float(valor, nombre):
    try:
        resultado = float(a_fraccion(valor))
    except OverflowError:
        raise ErrorEntrada(f"El {nombre} es demasiado grande para representarse.") from None
    return resultado


def _norma_inf(v):
    mayor = 0.0
    for valor in v:
        if abs(valor) > mayor or math.isnan(valor):
            mayor = abs(valor)
    return mayor


def _residuo_inf(A, b, x):
    """r = ||b - A x||∞ con la A y la b originales (en float)."""
    mayor = 0.0
    for i in range(len(A)):
        ax = 0.0
        for j in range(len(x)):
            ax += A[i][j] * x[j]
        valor = abs(b[i] - ax)
        if valor > mayor or math.isnan(valor):
            mayor = valor
    return mayor


def _es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def vector_cero(n):
    """Vector inicial por defecto: x(0) = 0."""
    return [0.0] * n


def vector_diagonal(A, b):
    """Vector inicial x_i(0) = b_i / a_ii (usado en S8-30/09 pp. 19 y 24)."""
    n = validar_cuadrada(A, "matriz A")
    for i in range(n):
        if A[i][i] == 0:
            raise ErrorEntrada(f"a_{i + 1}{i + 1} = 0: no se puede usar x_i(0) = b_i / a_ii.")
    return [_a_float(b[i], "b") / _a_float(A[i][i], "a_ii") for i in range(n)]


# ---------------------------------------------------------------------------
# Validación de la configuración
# ---------------------------------------------------------------------------

def validar_configuracion(A, b, config):
    """Valida A, b y la configuración.  Lanza ErrorEntrada/ErrorMatriz si algo falla.

    Devuelve (A_float, b_float, x0_float, advertencias).
    """
    if config.metodo not in METODOS:
        raise ErrorEntrada(f"Método desconocido: {config.metodo}.")
    if config.criterio not in CRITERIOS:
        raise ErrorEntrada(f"Criterio de parada desconocido: {config.criterio}.")
    if config.formato not in FORMATOS:
        raise ErrorEntrada(f"Formato de almacenamiento desconocido: {config.formato}.")
    n = validar_cuadrada(A, "matriz A")
    if validar_vector(b, "vector b") != n:
        raise ErrorEntrada(f"b debe tener {n} componentes (A es {n}x{n}).")
    x0 = config.x0 if config.x0 is not None else vector_cero(n)
    if validar_vector(x0, "vector inicial x⁽⁰⁾") != n:
        raise ErrorEntrada(f"El vector inicial debe tener {n} componentes.")
    A_f = [[_a_float(v, "elemento de A") for v in fila] for fila in A]
    b_f = [_a_float(v, "elemento de b") for v in b]
    x0_f = [_a_float(v, "elemento de x⁽⁰⁾") for v in x0]

    advertencias = []
    if config.criterio in (CRITERIO_CAMBIO, CRITERIO_RESIDUO):
        if not es_numero(config.tolerancia):
            raise ErrorEntrada("La tolerancia debe ser un número mayor que 0.")
        tol_f = _a_float(config.tolerancia, "tolerancia")
        if not math.isfinite(tol_f) or tol_f <= 0:
            raise ErrorEntrada("La tolerancia debe ser un número mayor que 0.")
        if not _es_entero(config.k_max) or not (1 <= config.k_max <= K_TOPE):
            raise ErrorEntrada(f"El máximo de iteraciones debe ser un entero entre 1 y {K_TOPE}.")
        escala = max(1.0, _norma_inf(b_f))
        if tol_f < 1e-14 * escala:
            advertencias.append(
                "La tolerancia puede ser inalcanzable en aritmética de punto flotante.")
    else:
        if not _es_entero(config.n_iteraciones) or not (1 <= config.n_iteraciones <= K_TOPE):
            raise ErrorEntrada(f"N debe ser un entero positivo entre 1 y {K_TOPE}.")
    if config.metodo == SOR:
        if not es_numero(config.omega):
            raise ErrorEntrada("Debe indicar un factor de relajación ω numérico.")
        omega_f = _a_float(config.omega, "factor de relajación ω")
        if not (math.isfinite(omega_f) and 0 < omega_f < 2):
            raise ErrorEntrada(
                "ω debe cumplir 0 < ω < 2. Este rango no garantiza la convergencia.")
    return A_f, b_f, x0_f, advertencias


# ---------------------------------------------------------------------------
# Mecanismo común de iteración y parada
# ---------------------------------------------------------------------------

def ejecutar(A, b, config):
    """Ejecuta el método configurado.  Nunca lanza excepciones: todo problema
    se devuelve como un código de terminación con su mensaje."""
    try:
        return _ejecutar(A, b, config)
    except (ErrorEntrada, ErrorMatriz, OverflowError) as error:
        return ResultadoIterativo(configuracion=config, codigo=ENTRADA_INVALIDA,
                                  mensaje=str(error), criterio_cumplido=None)
    except Exception as error:  # error inesperado: se informa sin cerrar la aplicación
        return ResultadoIterativo(
            configuracion=config, codigo=ERROR_INTERNO, criterio_cumplido=None,
            mensaje=f"Ocurrió un error inesperado ({type(error).__name__}); "
                    f"los datos introducidos no se perdieron.")


def _ejecutar(A, b, config):
    A_f, b_f, x0, advertencias = validar_configuracion(A, b, config)
    # Se trabaja sobre una copia para no modificar la configuración del usuario;
    # la copia guarda el x(0) efectivamente usado (por defecto, el vector cero).
    config = replace(config, x0=list(x0))
    n = len(A_f)
    for i in range(n):
        if A_f[i][i] == 0:
            return ResultadoIterativo(
                configuracion=config, codigo=DIAGONAL_CERO, criterio_cumplido=None,
                advertencias=advertencias,
                mensaje=f"a_{i + 1}{i + 1} = 0 en la fila {i + 1}: el método no puede "
                        f"iniciarse. Considere reordenar las ecuaciones.")

    # Con formato CSR solo se recorren los elementos no nulos (mismas iteraciones).
    if config.formato == "csr":
        matriz = a_csr(A_f)
        paso = PASOS_CSR[config.metodo]
        residuo = residuo_inf_csr
    else:
        matriz = A_f
        paso = PASOS[config.metodo]
        residuo = _residuo_inf
    omega = _a_float(config.omega, "ω") if config.metodo == SOR else None
    tol = _a_float(config.tolerancia, "tolerancia") if config.criterio != CRITERIO_ITERACIONES else None
    limite = config.n_iteraciones if config.criterio == CRITERIO_ITERACIONES else config.k_max

    x = list(x0)
    r0 = residuo(matriz, b_f, x)
    historial = [FilaIteracion(k=0, x=list(x), d=None, r=r0)]

    def resultado(codigo, mensaje, cumplido, k_error=None):
        return ResultadoIterativo(configuracion=config, codigo=codigo, mensaje=mensaje,
                                  criterio_cumplido=cumplido, historial=historial,
                                  advertencias=advertencias, k_error=k_error)

    if config.criterio == CRITERIO_RESIDUO and r0 < tol:
        return resultado(
            TOLERANCIA_RESIDUO,
            f"El vector inicial ya satisface el criterio del residuo "
            f"(r₀ = {formatear_numero(r0)} < ε = {formatear_numero(tol)}); "
            f"no se realizaron iteraciones.", True)

    for k in range(1, limite + 1):
        x_nuevo = paso(matriz, b_f, x, omega)
        d = r = None
        if all(math.isfinite(v) for v in x_nuevo):
            d = _norma_inf([x_nuevo[i] - x[i] for i in range(n)])
            r = residuo(matriz, b_f, x_nuevo)
        if d is None or not (math.isfinite(d) and math.isfinite(r)):
            return resultado(
                ERROR_NO_FINITO,
                f"Error numérico: en la iteración {k} se obtuvieron valores no finitos "
                f"(desbordamiento). Se detuvo el cálculo. Esto no constituye por sí solo "
                f"una demostración matemática de divergencia.", False, k_error=k)
        x = x_nuevo
        historial.append(FilaIteracion(k=k, x=list(x), d=d, r=r))
        if config.criterio == CRITERIO_CAMBIO and d < tol:
            return resultado(
                TOLERANCIA_CAMBIO,
                f"Criterio satisfecho: d_{k} = {formatear_numero(d)} < ε = "
                f"{formatear_numero(tol)} en la iteración {k}.", True)
        if config.criterio == CRITERIO_RESIDUO and r < tol:
            return resultado(
                TOLERANCIA_RESIDUO,
                f"Criterio satisfecho: r_{k} = {formatear_numero(r)} < ε = "
                f"{formatear_numero(tol)} en la iteración {k}.", True)

    if config.criterio == CRITERIO_ITERACIONES:
        return resultado(
            N_COMPLETADAS,
            f"Se completaron las {limite} iteraciones solicitadas. Completar N "
            f"iteraciones no demuestra convergencia.", True)
    return resultado(
        MAXIMO_ITERACIONES,
        "Se alcanzó el máximo de iteraciones sin satisfacer el criterio de parada.", False)


# ---------------------------------------------------------------------------
# Dominancia diagonal (S8-30/09 p. 37)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Comparación entre métodos
# ---------------------------------------------------------------------------

CAMPOS_HOMOGENEOS = ("criterio", "tolerancia", "k_max", "n_iteraciones", "x0")


@dataclass
class ResultadoComparacion:
    resultados: list
    homogeneo: bool
    diferencias: list
    referencia: list = None          # solución del método directo, si existe
    errores_finales: list = None     # ||x_final - x*||∞ por método (o None)
    errores_historial: list = None   # lista por método de e_k
    nota: str = ("El número de iteraciones solo es comparable entre métodos que "
                 "terminaron por el mismo motivo.")


def _valor_campo(config, campo):
    valor = getattr(config, campo)
    if campo == "x0" and valor is not None:
        return tuple(float(a_fraccion(v)) for v in valor)
    if campo in ("tolerancia",):
        return float(a_fraccion(valor))
    return valor


def comparar_metodos(A, b, configuraciones):
    """Ejecuta varias configuraciones sobre el mismo A x = b y las compara.

    Se considera homogéneo si coinciden criterio, tolerancia, k_max, N y x(0)
    (los que corresponden al criterio).  ω solo afecta a SOR y no se compara.
    """
    resultados = [ejecutar(A, b, c) for c in configuraciones]
    diferencias = []
    base = configuraciones[0]
    campos = list(CAMPOS_HOMOGENEOS)
    if base.criterio == CRITERIO_ITERACIONES:
        campos.remove("tolerancia")
        campos.remove("k_max")
    else:
        campos.remove("n_iteraciones")
    for campo in campos:
        try:
            valores = {_valor_campo(c, campo) for c in configuraciones}
        except Exception:
            valores = {None, "?"}
        if len(valores) > 1:
            diferencias.append(campo)

    referencia = None
    try:
        referencia = [float(v) for v in solucion_unica(
            [[a_fraccion(v) for v in fila] for fila in A], [a_fraccion(v) for v in b])]
    except (ErrorSistema, ErrorMatriz, ErrorEntrada, OverflowError, ValueError):
        referencia = None

    errores_finales = []
    errores_historial = []
    for r in resultados:
        if referencia is None or not r.historial:
            errores_finales.append(None)
            errores_historial.append(None)
            continue
        historia = [_norma_inf([fila.x[i] - referencia[i] for i in range(len(referencia))])
                    for fila in r.historial]
        errores_historial.append(historia)
        errores_finales.append(historia[-1])
    return ResultadoComparacion(
        resultados=resultados, homogeneo=not diferencias, diferencias=diferencias,
        referencia=referencia, errores_finales=errores_finales,
        errores_historial=errores_historial)


def configuraciones_homogeneas(criterio=CRITERIO_CAMBIO, tolerancia=1e-3, k_max=50,
                               n_iteraciones=5, x0=None, omega=1.2):
    """Devuelve las tres configuraciones (Jacobi, Gauss-Seidel, SOR) con los mismos
    parámetros; SOR usa además su propio ω."""
    return [ConfiguracionIterativa(metodo=m, criterio=criterio, tolerancia=tolerancia,
                                   k_max=k_max, n_iteraciones=n_iteraciones,
                                   x0=list(x0) if x0 is not None else None, omega=omega)
            for m in METODOS]
