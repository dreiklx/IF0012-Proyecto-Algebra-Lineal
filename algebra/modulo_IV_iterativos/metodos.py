"""Módulo IV — Fórmulas de Jacobi, Gauss-Seidel y SOR (OFICIAL p. 2).

Cada función hace UNA iteración, x(k-1) -> x(k).  El bucle, los criterios de
parada y la tabla de iteraciones están en ejecucion.py (comunes a los tres).

Fórmulas por componentes (A = D + L + U; i = 1..n en orden):

  Jacobi        (S8-30/09 p. 15)
      x_i(k) = ( b_i - Σ_{j≠i} a_ij x_j(k-1) ) / a_ii

  Gauss-Seidel  (S8-30/09 p. 22) — usa los valores ya actualizados
      x_i(k) = ( b_i - Σ_{j<i} a_ij x_j(k) - Σ_{j>i} a_ij x_j(k-1) ) / a_ii

  SOR           (S8-30/09 p. 28) — combina el valor anterior y el de Gauss-Seidel
      x_i(k) = (1-ω) x_i(k-1) + ω · ( b_i - Σ_{j<i} a_ij x_j(k) - Σ_{j>i} a_ij x_j(k-1) ) / a_ii

  Richardson    (EXTENSIÓN NO VISTA EN CLASE; solo para el incentivo de
                precondicionamiento, ver docs/investigacion_richardson.md)
      x(k) = x(k-1) + (b - A x(k-1))

La aritmética es de punto flotante (float): las iteraciones son aproximaciones.
Las versiones que recorren solo los no nulos (formato CSR) están en dispersas.py.
"""

JACOBI = "Jacobi"
GAUSS_SEIDEL = "Gauss-Seidel"
SOR = "SOR"
METODOS = (JACOBI, GAUSS_SEIDEL, SOR)
# Richardson no es uno de los métodos del enunciado: solo se usa en el análisis del
# precondicionador diagonal (precondicionamiento.py), porque es el método
# estacionario más simple sobre el que M = D sí tiene efecto.
RICHARDSON = "Richardson"


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


def paso_richardson(A, b, x_anterior, omega=None):
    """Una iteración de Richardson (paso 1): x(k) = x(k-1) + (b - A x(k-1)).

    Su matriz de iteración es T_R = I - A.  Aplicado al sistema precondicionado
    D⁻¹A x = D⁻¹b da x(k) = x(k-1) + D⁻¹(b - A x(k-1)), que es exactamente Jacobi."""
    n = len(A)
    x_nuevo = [0.0] * n
    for i in range(n):
        ax = 0.0
        for j in range(n):
            ax += A[i][j] * x_anterior[j]
        x_nuevo[i] = x_anterior[i] + (b[i] - ax)
    return x_nuevo
