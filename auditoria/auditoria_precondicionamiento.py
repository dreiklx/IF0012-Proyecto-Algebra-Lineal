r"""Auditoría independiente del precondicionador diagonal (03-nov-2026).

Uso (desde la raíz del proyecto):  .venv\Scripts\python auditoria/auditoria_precondicionamiento.py .

Oráculos escritos aparte del núcleo, con semilla fija:
  * B = D⁻¹A y b̃ = D⁻¹b calculados aquí a mano;
  * κ∞ con la inversa por adjunta y determinantes de Leibniz;
  * iteraciones de Jacobi sobre B (bucle propio) comparadas con las del sistema original;
  * T y c de Jacobi y Gauss-Seidel idénticos con y sin M = D (procedimiento de clase).
  Richardson se retiró de la aplicación (no aparece en los materiales del curso)."""
import itertools
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from algebra.modulo_IV_iterativos.ejecucion import ConfiguracionIterativa
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI
from algebra.modulo_IV_iterativos.precondicionamiento import analizar_precondicionador

random.seed(11)


def det(M):
    n = len(M)
    total = F(0)
    for p in itertools.permutations(range(n)):
        signo = (-1) ** sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        t = F(signo)
        for i in range(n):
            t *= M[i][p[i]]
        total += t
    return total


def kappa_adjunta(A):
    n = len(A)
    d = det(A)
    if d == 0:
        return None
    if n == 1:
        inv = [[1 / A[0][0]]]
    else:
        inv = [[(-1) ** (i + j) * det([[A[r][c] for c in range(n) if c != i]
                                       for r in range(n) if r != j]) / d for j in range(n)]
               for i in range(n)]
    norma = lambda M: max(sum(abs(v) for v in fila) for fila in M)
    return norma(A) * norma(inv)


def potencia_norma(T, k):
    n = len(T)
    P = [list(fila) for fila in T]
    for _ in range(k - 1):
        P = [[sum(P[i][m] * T[m][j] for m in range(n)) for j in range(n)] for i in range(n)]
    return max(sum(abs(v) for v in fila) for fila in P) ** (1 / k)


fallos = casos = 0
for _ in range(150):
    n = random.randint(1, 4)
    A = [[F(random.randint(-4, 4)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = F(random.choice([-9, -3, 2, 5, 7, 12]))
    b = [F(random.randint(-6, 6)) for _ in range(n)]
    r = analizar_precondicionador(A, b, ConfiguracionIterativa(tolerancia=1e-8, k_max=80))
    casos += 1
    errores = []
    B = [[A[i][j] / A[i][i] for j in range(n)] for i in range(n)]
    if r.B != B or r.b_tilde != [b[i] / A[i][i] for i in range(n)]:
        errores.append("B o b̃")
    if r.kappa_A != kappa_adjunta(A) or r.kappa_B != kappa_adjunta(B):
        errores.append("κ")
    por_metodo = {f.metodo: f for f in r.comparaciones}
    if not all(f.T_identicas for f in r.comparaciones if f.metodo in (JACOBI, GAUSS_SEIDEL)):
        errores.append("T distintas")
    if errores:
        fallos += 1
        print("FALLO", A, b, errores)
print(f"precondicionamiento: casos {casos} fallos {fallos}")
