"""Módulo IV (convergencia) — Matrices de iteración y radio espectral.

Procedimiento del curso (S9-05/10 pp. 32-34, S9-07/10 pp. 3-7, Tarea II #4-5):
  1. Descomponer A = D + L + U  (D diagonal, L estrictamente inferior,
     U estrictamente superior, con los signos que tienen en A).
  2. Construir la matriz de iteración T y el vector c de x(k+1) = T x(k) + c:
        Jacobi        T_J  = -D⁻¹ (L + U)                 c = D⁻¹ b
        Gauss-Seidel  T_GS = -(D + L)⁻¹ U                 c = (D + L)⁻¹ b
        SOR           T_ω  = (D + ωL)⁻¹ [(1-ω) D - ωU]    c = ω (D + ωL)⁻¹ b
     (la fórmula de SOR no aparece en los PDF revisados; es la estándar,
      Burden & Faires, y con ω = 1 se reduce a Gauss-Seidel).
  3. Resolver det(T - λI) = 0 y tomar ρ(T) = max |λ|.
  4. Teorema: el método converge para todo x(0) si y solo si ρ(T) < 1.

Implementación (todo desde cero, sin bibliotecas de álgebra):
  * T se calcula con fracciones exactas; las inversas de D+L y D+ωL se
    obtienen con nuestro Gauss-Jordan (algebra/directos.py).
  * Polinomio característico p(λ) = det(λI - T) = λⁿ + c1 λⁿ⁻¹ + ... + cn
    con el método de Faddeev-LeVerrier (EXTENSIÓN NO VISTA EN CLASE, necesaria
    para n > 3, donde la regla de Sarrus no aplica):
        M0 = 0;   para k = 1..n:   M_k = T·M_{k-1} + c_{k-1}·I,   c_k = -tr(T·M_k) / k
    Con fracciones es exacto.  Para 3x3 coincide con el desarrollo de clase:
        det(T - λI) = -λ³ + tr(T) λ² - (suma de menores principales 2x2) λ + det(T).
  * Raíces:
      - las raíces λ = 0 se extraen de forma exacta (coeficientes finales nulos);
      - grado 1 y 2: fórmula directa (cuadrática con raíz compleja si el
        discriminante es negativo);
      - grado >= 3: método de Durand-Kerner (EXTENSIÓN NO VISTA EN CLASE),
        que aproxima simultáneamente todas las raíces complejas:
            z_i <- z_i - p(z_i) / Π_{j≠i} (z_i - z_j)
        No tiene garantía teórica de convergencia global; se verifica cada
        resultado (|p(λ)| pequeño, suma de raíces = -c1, producto = (-1)ⁿ cn)
        y se advierte si falla o si hay raíces casi repetidas (con raíces
        múltiples la precisión disminuye).
  * Si ρ está muy cerca de 1, la conclusión no es fiable numéricamente y se
    informa como indeterminada.  Para polinomios reducidos de grado <= 2 la
    decisión ρ < 1 se toma de forma exacta con las condiciones de Schur-Cohn:
        grado 1: |c1| < 1;   grado 2: |c2| < 1  y  |c1| < 1 + c2.
"""

import cmath
import math
from dataclasses import dataclass, field
from fractions import Fraction

from algebra.directos import a_fraccion, inversa_gauss_jordan
from algebra.iterativos import GAUSS_SEIDEL, JACOBI, SOR
from algebra.matriz import identidad, multiplicar_matrices, multiplicar_matriz_vector, validar_cuadrada
from algebra.validacion import ErrorEntrada, formatear_numero

N_MAX_ESPECTRAL = 8            # tamaño máximo para el que se calcula ρ
UMBRAL_RHO_UNO = 1e-9          # banda alrededor de 1 donde la conclusión es indeterminada
UMBRAL_RAICES_CERCANAS = 1e-6  # raíces más cercanas que esto: posible raíz múltiple

CONVERGE = "CONVERGE"
NO_CONVERGE = "NO_CONVERGE"
INDETERMINADO = "INDETERMINADO"
NO_CALCULADO = "NO_CALCULADO"


@dataclass
class MatrizIteracion:
    metodo: str
    D: list
    L: list
    U: list
    T: list
    c: list
    omega: Fraction = None


@dataclass
class ResultadoEspectral:
    iteracion: MatrizIteracion
    conclusion: str
    mensaje: str
    coeficientes: list = None      # [1, c1, ..., cn] de det(λI - T)
    polinomio_curso: str = ""      # det(T - λI) escrito como en clase
    autovalores: list = None       # complejos
    multiplicidad_cero: int = 0
    rho: float = None
    fiable: bool = False
    decision_exacta: bool = False
    verificaciones: dict = field(default_factory=dict)
    advertencias: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# 1-2. Descomposición y matrices de iteración (exactas)
# ---------------------------------------------------------------------------

def descomponer(A):
    """Devuelve (D, L, U) con A = D + L + U, conservando los signos de A."""
    n = validar_cuadrada(A, "matriz A")
    A_ex = [[a_fraccion(v) for v in fila] for fila in A]
    D = [[A_ex[i][j] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    L = [[A_ex[i][j] if i > j else Fraction(0) for j in range(n)] for i in range(n)]
    U = [[A_ex[i][j] if i < j else Fraction(0) for j in range(n)] for i in range(n)]
    return D, L, U


def _escalar(k, M):
    return [[k * v for v in fila] for fila in M]


def _sumar(M, N):
    return [[M[i][j] + N[i][j] for j in range(len(M[0]))] for i in range(len(M))]


def matriz_iteracion(A, b, metodo, omega=None):
    """Construye T y c del método indicado con aritmética exacta.

    Lanza ErrorEntrada si algún a_ii = 0 (D, D+L o D+ωL no serían invertibles).
    """
    n = validar_cuadrada(A, "matriz A")
    D, L, U = descomponer(A)
    if any(D[i][i] == 0 for i in range(n)):
        raise ErrorEntrada("Hay un elemento diagonal nulo: no se puede construir la matriz de iteración.")
    b_ex = [a_fraccion(v) for v in b]
    if metodo == JACOBI:
        D_inv = [[1 / D[i][i] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        T = _escalar(-1, multiplicar_matrices(D_inv, _sumar(L, U)))
        c = multiplicar_matriz_vector(D_inv, b_ex)
        w = None
    elif metodo == GAUSS_SEIDEL:
        DL_inv = inversa_gauss_jordan(_sumar(D, L)).inversa
        T = _escalar(-1, multiplicar_matrices(DL_inv, U))
        c = multiplicar_matriz_vector(DL_inv, b_ex)
        w = None
    elif metodo == SOR:
        if omega is None:
            raise ErrorEntrada("SOR requiere el factor de relajación ω.")
        w = a_fraccion(omega)
        if not (0 < w < 2):
            raise ErrorEntrada("ω debe cumplir 0 < ω < 2.")
        DwL_inv = inversa_gauss_jordan(_sumar(D, _escalar(w, L))).inversa
        derecha = _sumar(_escalar(1 - w, D), _escalar(-w, U))
        T = multiplicar_matrices(DwL_inv, derecha)
        c = [w * v for v in multiplicar_matriz_vector(DwL_inv, b_ex)]
    else:
        raise ErrorEntrada(f"Método desconocido: {metodo}.")
    return MatrizIteracion(metodo=metodo, D=D, L=L, U=U, T=T, c=c, omega=w)


# ---------------------------------------------------------------------------
# 3. Polinomio característico (Faddeev-LeVerrier, exacto)
# ---------------------------------------------------------------------------

def polinomio_caracteristico(T):
    """Coeficientes [1, c1, ..., cn] de p(λ) = det(λI - T), exactos."""
    n = validar_cuadrada(T, "matriz T")
    T_ex = [[a_fraccion(v) for v in fila] for fila in T]
    I = [[Fraction(v) for v in fila] for fila in identidad(n)]
    coeficientes = [Fraction(1)]
    M = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        M = _sumar(multiplicar_matrices(T_ex, M), _escalar(coeficientes[-1], I))
        TM = multiplicar_matrices(T_ex, M)
        traza = sum(TM[i][i] for i in range(n))
        coeficientes.append(-traza / k)
    return coeficientes


def texto_polinomio_curso(coeficientes):
    """Escribe det(T - λI) = (-1)ⁿ p(λ) como en los apuntes (por ejemplo -λ³ + ...)."""
    n = len(coeficientes) - 1
    signo = -1 if n % 2 else 1
    terminos = []
    for k, c in enumerate(coeficientes):
        valor = signo * c
        if valor == 0:
            continue
        grado = n - k
        potencia = "" if grado == 0 else ("λ" if grado == 1 else f"λ{_superindice(grado)}")
        magnitud = abs(valor)
        texto_mag = "" if (magnitud == 1 and grado > 0) else formatear_numero(magnitud)
        terminos.append(("−" if valor < 0 else "+", f"{texto_mag}{potencia}"))
    if not terminos:
        return "det(T − λI) = 0"
    primero = ("−" if terminos[0][0] == "−" else "") + terminos[0][1]
    resto = "".join(f" {s} {t}" for s, t in terminos[1:])
    return f"det(T − λI) = {primero}{resto}"


def _superindice(n):
    return str(n).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))


# ---------------------------------------------------------------------------
# Raíces del polinomio
# ---------------------------------------------------------------------------

def _evaluar(coeficientes, z):
    """Evalúa el polinomio en z por el esquema de Horner."""
    valor = 0
    for c in coeficientes:
        valor = valor * z + c
    return valor


def durand_kerner(coeficientes, max_iter=2000, tol=1e-15):
    """Aproxima todas las raíces de un polinomio mónico de grado >= 1.

    Devuelve (raices, convergio).  coeficientes: [1, c1, ..., cd] (float o Fraction).
    """
    c = [complex(float(v)) for v in coeficientes]
    d = len(c) - 1
    cota = 1 + max(abs(v) for v in c[1:])        # todas las raíces cumplen |z| <= cota
    semilla = complex(0.4, 0.9)
    z = [cota * 0.5 * semilla ** k for k in range(d)]
    for _ in range(max_iter):
        mayor_cambio = 0.0
        for i in range(d):
            producto = complex(1)
            for j in range(d):
                if j != i:
                    producto *= (z[i] - z[j])
            if producto == 0:
                producto = complex(1e-300)
            correccion = _evaluar(c, z[i]) / producto
            z[i] -= correccion
            mayor_cambio = max(mayor_cambio, abs(correccion))
        if mayor_cambio <= tol * max(1.0, max(abs(v) for v in z)):
            return z, True
    return z, False


def _limpiar(z, escala):
    """Anula partes imaginarias o reales despreciables (ruido de redondeo)."""
    real, imag = z.real, z.imag
    if abs(imag) < 1e-12 * escala:
        imag = 0.0
    if abs(real) < 1e-12 * escala:
        real = 0.0
    return complex(real, imag)


def _schur_cohn(reducido):
    """Decide de forma exacta si todas las raíces del polinomio mónico de grado
    <= 2 cumplen |λ| < 1.  Devuelve True/False."""
    if len(reducido) == 2:
        return abs(reducido[1]) < 1
    c1, c2 = reducido[1], reducido[2]
    return abs(c2) < 1 and abs(c1) < 1 + c2


def raices(coeficientes):
    """Calcula las raíces de p(λ) = det(λI - T).

    Devuelve (autovalores, multiplicidad_cero, fiable, advertencias, decision_exacta)
    donde decision_exacta es True/False (todas |λ|<1) si se pudo decidir exactamente,
    o None.
    """
    advertencias = []
    reducido = list(coeficientes)
    ceros = 0
    while len(reducido) > 1 and reducido[-1] == 0:   # extracción exacta de λ = 0
        reducido.pop()
        ceros += 1
    grado = len(reducido) - 1
    autovalores = [complex(0)] * ceros
    fiable = True
    decision = None
    if grado == 0:
        return autovalores, ceros, True, advertencias, True
    if grado <= 2 and all(isinstance(v, Fraction) for v in reducido):
        decision = _schur_cohn(reducido)
    if grado == 1:
        autovalores.append(complex(float(-reducido[1])))
    elif grado == 2:
        c1, c2 = reducido[1], reducido[2]
        discriminante = c1 * c1 - 4 * c2       # exacto
        raiz = cmath.sqrt(float(discriminante)) if discriminante >= 0 else complex(0, math.sqrt(float(-discriminante)))
        autovalores.append((-float(c1) + raiz) / 2)
        autovalores.append((-float(c1) - raiz) / 2)
        if discriminante == 0:
            advertencias.append("Raíz doble (discriminante = 0).")
    else:
        aproximadas, convergio = durand_kerner(reducido)
        if not convergio:
            fiable = False
            advertencias.append(
                "El método de Durand-Kerner no alcanzó la precisión pedida: los "
                "autovalores pueden ser imprecisos.")
        escala = max(1.0, max(abs(z) for z in aproximadas))
        autovalores.extend(_limpiar(z, escala) for z in aproximadas)
        for i in range(len(aproximadas)):
            for j in range(i + 1, len(aproximadas)):
                if abs(aproximadas[i] - aproximadas[j]) < UMBRAL_RAICES_CERCANAS * escala:
                    advertencias.append(
                        "Hay autovalores casi repetidos: con raíces múltiples la "
                        "precisión numérica disminuye.")
                    break
            else:
                continue
            break
    return autovalores, ceros, fiable, advertencias, decision


# ---------------------------------------------------------------------------
# Análisis completo
# ---------------------------------------------------------------------------

def radio_espectral(A, b, metodo, omega=None):
    """Construye T, su polinomio característico, sus autovalores y ρ(T)."""
    n = validar_cuadrada(A, "matriz A")
    iteracion = matriz_iteracion(A, b, metodo, omega)
    if n > N_MAX_ESPECTRAL:
        return ResultadoEspectral(
            iteracion=iteracion, conclusion=NO_CALCULADO,
            mensaje=(f"No se calcula ρ(T) para n > {N_MAX_ESPECTRAL}: el procedimiento "
                     f"por polinomio característico pierde fiabilidad. Use la dominancia "
                     f"diagonal y el comportamiento observado de las iteraciones."))
    coeficientes = polinomio_caracteristico(iteracion.T)
    autovalores, ceros, fiable, advertencias, decision = raices(coeficientes)
    rho = max(abs(z) for z in autovalores) if autovalores else 0.0

    # Verificaciones independientes de las raíces
    escala = max(1.0, max(abs(float(c)) for c in coeficientes))
    residuos = [abs(_evaluar([float(c) for c in coeficientes], z)) / escala for z in autovalores]
    suma = sum(autovalores)
    traza = sum(iteracion.T[i][i] for i in range(n))
    verificaciones = {
        "max |p(λ)| relativo": max(residuos) if residuos else 0.0,
        "suma de autovalores": suma,
        "traza de T": float(traza),
    }
    if abs(suma - float(traza)) > 1e-8 * max(1.0, abs(float(traza)), rho * n):
        fiable = False
        advertencias.append("La suma de los autovalores no coincide con la traza de T.")
    if residuos and max(residuos) > 1e-8:
        fiable = False
        advertencias.append("Algún autovalor no anula el polinomio con la precisión esperada.")

    resultado = ResultadoEspectral(
        iteracion=iteracion, conclusion="", mensaje="", coeficientes=coeficientes,
        polinomio_curso=texto_polinomio_curso(coeficientes), autovalores=autovalores,
        multiplicidad_cero=ceros, rho=rho, fiable=fiable, verificaciones=verificaciones,
        advertencias=advertencias)

    if decision is not None:
        resultado.decision_exacta = True
        resultado.conclusion = CONVERGE if decision else NO_CONVERGE
    elif not fiable or abs(rho - 1) < UMBRAL_RHO_UNO:
        resultado.conclusion = INDETERMINADO
    else:
        resultado.conclusion = CONVERGE if rho < 1 else NO_CONVERGE

    rho_txt = formatear_numero(rho)
    if resultado.conclusion == CONVERGE:
        resultado.mensaje = (f"ρ(T) = {rho_txt} < 1: el método {metodo} converge para "
                             f"cualquier vector inicial.")
    elif resultado.conclusion == NO_CONVERGE:
        resultado.mensaje = (f"ρ(T) = {rho_txt} ≥ 1: el método {metodo} no converge para "
                             f"todo vector inicial (la convergencia no está garantizada y, "
                             f"en general, los errores no disminuyen).")
    else:
        resultado.mensaje = (f"ρ(T) ≈ {rho_txt}: no es posible decidir con fiabilidad si "
                             f"ρ(T) < 1 (valor muy cercano a 1 o cálculo numérico poco fiable).")
    if resultado.decision_exacta:
        resultado.mensaje += " (Decisión verificada de forma exacta.)"
    return resultado
