"""Incentivo «Precondicionamiento» (OFICIAL p. 5): precondicionador diagonal M = D.

Procedimiento de clase (S9-05/10 pp. 19-22, diapositivas 15-18):
    M = D = diag(a_11, ..., a_nn),   B = M⁻¹A,   b̃ = M⁻¹b,
y se aplica el método iterativo al sistema equivalente B x = b̃, que tiene la
misma solución.  La lámina de la diapositiva 17 propone comparar
    κ(B) frente a κ(A)   y   ρ(B) frente a ρ(A),
y observar si los valores propios de B = D⁻¹A se agrupan cerca de 1.

Comparación que se implementa (todo con nuestro código, sin bibliotecas):
  1. κ∞(A) y κ∞(D⁻¹A), con la inversa del Módulo II.
  2. Autovalores y radio espectral de A y de B (polinomio característico exacto).
  3. Iteraciones de Jacobi, Gauss-Seidel y SOR sobre el sistema original y el
     precondicionado, con la misma configuración, y sus matrices de iteración.
  4. Iteraciones de Richardson, x ← x + (b − Ax), sobre ambos sistemas
     (EXTENSIÓN NO VISTA EN CLASE; ver docs/investigacion_richardson.md).

Resultado matemático que la aplicación verifica de forma EXACTA:
  * En B = D⁻¹A la diagonal es I, L̃ = D⁻¹L y Ũ = D⁻¹U, de modo que
        T̃_J = −(L̃ + Ũ) = −D⁻¹(L + U) = T_J,
        T̃_GS = −(I + D⁻¹L)⁻¹D⁻¹U = −(D + L)⁻¹U = T_GS,
        T̃_ω = (I + ωD⁻¹L)⁻¹[(1−ω)I − ωD⁻¹U] = T_ω,
    y los vectores c también coinciden.  Por tanto, M = D NO cambia las
    iteraciones de Jacobi, Gauss-Seidel ni SOR (son invariantes al escalado de
    las filas).  Las tablas de la diapositiva 19, que muestran una mejora para
    Jacobi, no se pueden reproducir: la aplicación lo muestra con evidencia.
  * Donde M = D sí tiene efecto es en el condicionamiento (κ), en el residuo
    (r̃ = D⁻¹r) y en un método que no se escala solo, como Richardson:
        T_R = I − A   frente a   T̃_R = I − D⁻¹A = T_J.
    Richardson precondicionado con M = D es exactamente Jacobi.
"""

from dataclasses import dataclass, field, replace
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import identidad, validar_cuadrada, validar_vector
from algebra.compartido.validacion import ErrorEntrada, formatear_numero
from algebra.modulo_II_condicionamiento.condicion import numero_condicion_infinito
from algebra.modulo_IV_iterativos.espectral import (
    AVISO_CASI_REPETIDOS,
    N_MAX_ESPECTRAL,
    analizar_matriz,
    concluir,
    matriz_iteracion,
)
from algebra.modulo_IV_iterativos.iterativos import (
    ConfiguracionIterativa,
    METODOS,
    RICHARDSON,
    SOR,
    ejecutar,
)


@dataclass
class ComparacionMetodo:
    metodo: str
    original: object                  # ResultadoIterativo sobre A x = b
    precondicionado: object           # ResultadoIterativo sobre (D⁻¹A) x = D⁻¹b
    rho_original: float = None
    rho_precondicionado: float = None
    conclusion_original: str = None
    conclusion_precondicionado: str = None
    T_identicas: bool = None          # T y c exactamente iguales (solo Jacobi, GS, SOR)
    mismas_iteraciones: bool = None   # x⁽ᵏ⁾ iguales salvo redondeo (≤ 1e-10 relativo)


@dataclass
class ResultadoPrecondicionamiento:
    M: list
    M_inv: list
    B: list
    b_tilde: list
    kappa_A: Fraction = None          # None si A es singular
    kappa_B: Fraction = None
    analisis_A: object = None         # AnalisisMatriz (autovalores de A), si n <= 8
    analisis_B: object = None
    comparaciones: list = field(default_factory=list)
    conclusiones: list = field(default_factory=list)


def precondicionar_diagonal(A, b):
    """Devuelve (M, M⁻¹, B = M⁻¹A, b̃ = M⁻¹b) exactos, con M = D = diag(a_ii)."""
    n = validar_cuadrada(A, "matriz A")
    if validar_vector(b, "vector b") != n:
        raise ErrorEntrada(f"b debe tener {n} componentes (A es {n}x{n}).")
    A_ex = [[a_fraccion(v) for v in fila] for fila in A]
    b_ex = [a_fraccion(v) for v in b]
    for i in range(n):
        if A_ex[i][i] == 0:
            raise ErrorEntrada(f"a_{i + 1}{i + 1} = 0: M = D no es invertible y no se puede "
                               f"precondicionar. Considere reordenar las ecuaciones.")
    M = [[A_ex[i][i] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    M_inv = [[1 / A_ex[i][i] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    B = [[A_ex[i][j] / A_ex[i][i] for j in range(n)] for i in range(n)]
    b_tilde = [b_ex[i] / A_ex[i][i] for i in range(n)]
    return M, M_inv, B, b_tilde


def _rho(A, b, metodo, omega):
    """ρ de la matriz de iteración del método y su conclusión (o (None, None) si n > 8)."""
    n = len(A)
    if n > N_MAX_ESPECTRAL:
        return None, None
    if metodo == RICHARDSON:
        I = identidad(n)
        T = [[I[i][j] - a_fraccion(A[i][j]) for j in range(n)] for i in range(n)]
    else:
        T = matriz_iteracion(A, b, metodo, omega).T
    analisis = analizar_matriz(T)
    return analisis.rho, concluir(analisis.rho, analisis.fiable, analisis.decision,
                                  AVISO_CASI_REPETIDOS in analisis.advertencias)


def _mismas_iteraciones(r1, r2):
    if r1.k_final != r2.k_final or not r1.historial or not r2.historial:
        return False
    for f1, f2 in zip(r1.historial, r2.historial):
        for u, v in zip(f1.x, f2.x):
            if abs(u - v) > 1e-10 * max(1.0, abs(u)):
                return False
    return True


def analizar_precondicionador(A, b, configuracion=None, omega=Fraction(6, 5)):
    """Compara el sistema original con el precondicionado por M = D (ver docstring del módulo).

    `configuracion` (ConfiguracionIterativa) fija criterio, ε, k_max, N y x⁽⁰⁾; el método
    se sustituye por cada uno de Jacobi, Gauss-Seidel, SOR (con `omega`) y Richardson."""
    M, M_inv, B, b_tilde = precondicionar_diagonal(A, b)
    A_ex = [[a_fraccion(v) for v in fila] for fila in A]
    b_ex = [a_fraccion(v) for v in b]
    n = len(A_ex)
    base = configuracion or ConfiguracionIterativa()
    resultado = ResultadoPrecondicionamiento(M=M, M_inv=M_inv, B=B, b_tilde=b_tilde)

    cond_A = numero_condicion_infinito(A_ex)
    cond_B = numero_condicion_infinito(B)
    resultado.kappa_A, resultado.kappa_B = cond_A.kappa, cond_B.kappa
    if n <= N_MAX_ESPECTRAL:
        resultado.analisis_A = analizar_matriz(A_ex)
        resultado.analisis_B = analizar_matriz(B)

    for metodo in METODOS + (RICHARDSON,):
        config = replace(base, metodo=metodo, omega=omega)
        fila = ComparacionMetodo(metodo=metodo, original=ejecutar(A_ex, b_ex, config),
                                 precondicionado=ejecutar(B, b_tilde, config))
        fila.rho_original, fila.conclusion_original = _rho(A_ex, b_ex, metodo, omega)
        fila.rho_precondicionado, fila.conclusion_precondicionado = _rho(B, b_tilde, metodo, omega)
        if metodo != RICHARDSON:
            w = omega if metodo == SOR else None
            original = matriz_iteracion(A_ex, b_ex, metodo, w)
            nueva = matriz_iteracion(B, b_tilde, metodo, w)
            fila.T_identicas = original.T == nueva.T and original.c == nueva.c
        fila.mismas_iteraciones = _mismas_iteraciones(fila.original, fila.precondicionado)
        resultado.comparaciones.append(fila)

    resultado.conclusiones = _conclusiones(resultado)
    return resultado


def _conclusiones(r):
    textos = []
    if r.kappa_A is not None and r.kappa_B is not None:
        if r.kappa_B < r.kappa_A:
            efecto = "mejora (disminuye)"
        elif r.kappa_B > r.kappa_A:
            efecto = "empeora (aumenta)"
        else:
            efecto = "no cambia"
        textos.append(
            f"Condicionamiento: κ∞(A) = {formatear_numero(r.kappa_A)} y κ∞(D⁻¹A) = "
            f"{formatear_numero(r.kappa_B)}; el precondicionador {efecto} el número de condición."
            + (" Si todos los a_ii son iguales, D⁻¹A es un múltiplo de A y κ no cambia."
               if efecto == "no cambia" else ""))
    else:
        textos.append("A es singular: el número de condición no está definido.")
    clasicos = [f for f in r.comparaciones if f.metodo != RICHARDSON]
    if all(f.T_identicas for f in clasicos):
        textos.append(
            "Jacobi, Gauss-Seidel y SOR: la matriz de iteración T y el vector c del sistema "
            "precondicionado son EXACTAMENTE los mismos que los del original (verificado con "
            "fracciones). Por eso las iteraciones x⁽ᵏ⁾ coinciden: M = D no acelera estos "
            "métodos, porque ya están normalizados por la diagonal.")
    richardson = next(f for f in r.comparaciones if f.metodo == RICHARDSON)
    if richardson.rho_original is not None:
        textos.append(
            f"Richardson: ρ(I − A) = {formatear_numero(richardson.rho_original)} sin "
            f"precondicionar y ρ(I − D⁻¹A) = {formatear_numero(richardson.rho_precondicionado)} "
            f"con M = D (es la matriz de Jacobi). Aquí el precondicionador sí cambia la "
            f"convergencia: {richardson.original.k_final} iteraciones "
            f"({richardson.original.codigo}) frente a {richardson.precondicionado.k_final} "
            f"({richardson.precondicionado.codigo}).")
    if r.analisis_B is not None:
        textos.append(
            "Valores propios: los de B = D⁻¹A cumplen μ = 1 − λ(T_J); quedan agrupados cerca "
            "de 1 exactamente cuando ρ(T_J) es pequeño, que es lo que ilustra la lámina.")
    return textos
