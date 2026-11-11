"""Módulo IV (convergencia) — Matriz de iteración: el procedimiento de clase.

Cat. A, visto en clase (S9-05/10 pp. 32-34; S9-07/10 pp. 3-7; Tarea II #4-5):
  1. Descomponer A = D + L + U  (D diagonal, L estrictamente inferior,
     U estrictamente superior, con los signos que tienen en A).
  2. Calcular la inversa que corresponde: D⁻¹ (Jacobi), (D + L)⁻¹ (Gauss-Seidel).
  3-4. Construir T y c de x(k+1) = T x(k) + c:
        Jacobi        T_J  = -D⁻¹ (L + U)                 C_J  = D⁻¹ b
        Gauss-Seidel  T_GS = -(D + L)⁻¹ U                 C_GS = (D + L)⁻¹ b
        SOR           T_ω  = (D + ωL)⁻¹ [(1-ω) D - ωU]    C_ω  = ω (D + ωL)⁻¹ b
     La fórmula de SOR no aparece en los PDF revisados (Cat. C): es la estándar,
     Burden & Faires, y con ω = 1 se reduce a Gauss-Seidel.
  5. det(T - λI) por la regla de Sarrus para 3x3 (desarrollo_sarrus); el
     polinomio general y sus raíces están en polinomio_raices.py y ρ(T) en espectral.py.

Todo con fracciones exactas; las inversas de D + L y D + ωL se obtienen con
nuestro Gauss-Jordan (algebra/modulo_I_sistemas/directos.py).
"""

from dataclasses import dataclass
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import multiplicar_matrices, multiplicar_matriz_vector, validar_cuadrada
from algebra.compartido.validacion import ErrorEntrada
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI, SOR
from algebra.modulo_I_sistemas.directos import inversa_gauss_jordan


@dataclass
class MatrizIteracion:
    metodo: str
    D: list
    L: list
    U: list
    T: list
    c: list
    omega: Fraction = None
    inversa: list = None     # D⁻¹, (D+L)⁻¹ o (D+ωL)⁻¹: el paso 2 de clase (S9-07/10 pp. 3 y 6)

def descomponer(A):
    """Devuelve (D, L, U) con A = D + L + U, conservando los signos de A."""
    n = validar_cuadrada(A, "matriz A")
    A_ex = [[a_fraccion(v) for v in fila] for fila in A]
    D = [[A_ex[i][j] if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    L = [[A_ex[i][j] if i > j else Fraction(0) for j in range(n)] for i in range(n)]
    U = [[A_ex[i][j] if i < j else Fraction(0) for j in range(n)] for i in range(n)]
    return D, L, U

def escalar(k, M):
    return [[k * v for v in fila] for fila in M]

def sumar(M, N):
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
        T = escalar(-1, multiplicar_matrices(D_inv, sumar(L, U)))
        c = multiplicar_matriz_vector(D_inv, b_ex)
        w = None
        inversa = D_inv
    elif metodo == GAUSS_SEIDEL:
        DL_inv = inversa_gauss_jordan(sumar(D, L)).inversa
        T = escalar(-1, multiplicar_matrices(DL_inv, U))
        c = multiplicar_matriz_vector(DL_inv, b_ex)
        w = None
        inversa = DL_inv
    elif metodo == SOR:
        if omega is None:
            raise ErrorEntrada("SOR requiere el factor de relajación ω.")
        w = a_fraccion(omega)
        if not (0 < w < 2):
            raise ErrorEntrada("ω debe cumplir 0 < ω < 2.")
        DwL_inv = inversa_gauss_jordan(sumar(D, escalar(w, L))).inversa
        derecha = sumar(escalar(1 - w, D), escalar(-w, U))
        T = multiplicar_matrices(DwL_inv, derecha)
        c = [w * v for v in multiplicar_matriz_vector(DwL_inv, b_ex)]
        inversa = DwL_inv
    else:
        raise ErrorEntrada(f"Método desconocido: {metodo}.")
    return MatrizIteracion(metodo=metodo, D=D, L=L, U=U, T=T, c=c, omega=w, inversa=inversa)

def desarrollo_sarrus(T):
    """Procedimiento de clase para 3x3 (S9-05/10 pp. 32-34; S9-07/10 p. 4):
    det(T - λI) = -λ³ + tr(T) λ² - (suma de menores principales 2x2) λ + det(T),
    con det(T) por la regla de Sarrus.  Devuelve (traza, suma_menores, det) exactos.

    Es independiente de Faddeev-LeVerrier y sirve para mostrar y verificar el
    polinomio tal como se calcula en clase."""
    if validar_cuadrada(T, "matriz T") != 3:
        raise ErrorEntrada("El desarrollo por Sarrus solo aplica a matrices 3x3.")
    t = [[a_fraccion(v) for v in fila] for fila in T]
    traza = t[0][0] + t[1][1] + t[2][2]
    menores = ((t[0][0] * t[1][1] - t[0][1] * t[1][0])
               + (t[0][0] * t[2][2] - t[0][2] * t[2][0])
               + (t[1][1] * t[2][2] - t[1][2] * t[2][1]))
    det = (t[0][0] * t[1][1] * t[2][2] + t[0][1] * t[1][2] * t[2][0] + t[0][2] * t[1][0] * t[2][1]
           - t[0][2] * t[1][1] * t[2][0] - t[0][0] * t[1][2] * t[2][1] - t[0][1] * t[1][0] * t[2][2])
    return traza, menores, det
