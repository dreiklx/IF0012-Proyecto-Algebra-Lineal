r"""Auditoría independiente del precondicionador diagonal (03-nov-2026).

Uso (desde la raíz del proyecto):  .venv\Scripts\python auditoria/auditoria_precondicionamiento.py .

Oráculos escritos aparte del núcleo, con semilla fija:
  * B = D⁻¹A y b̃ = D⁻¹b calculados aquí a mano;
  * κ∞ con la inversa por adjunta y determinantes de Leibniz;
  * iteraciones de Jacobi sobre B (bucle propio) comparadas con las del sistema original;
  * Richardson precondicionado (bucle propio x ← x + D⁻¹(b − Ax)) igual a Jacobi;
  * ρ(I − A) comparado con la fórmula de Gelfand ‖(I − A)ᵏ‖∞^(1/k)."""
import itertools
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from algebra.iterativos import ConfiguracionIterativa, JACOBI, RICHARDSON  # noqa: E402
from algebra.precondicionamiento import analizar_precondicionador  # noqa: E402

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
    if not all(f.T_identicas for f in r.comparaciones if f.metodo != RICHARDSON):
        errores.append("T distintas")
    # Richardson precondicionado (bucle propio) = Jacobi del núcleo, iteración a iteración
    jac = por_metodo[JACOBI].original
    x = [0.0] * n
    for fila in jac.historial[1:]:
        ax = [sum(float(A[i][j]) * x[j] for j in range(n)) for i in range(n)]
        x = [x[i] + (float(b[i]) - ax[i]) / float(A[i][i]) for i in range(n)]
        if max(abs(x[i] - fila.x[i]) for i in range(n)) > 1e-9 * max(1.0, max(map(abs, x))):
            errores.append("Richardson precondicionado ≠ Jacobi")
            break
    # ρ(I − A) frente a Gelfand (solo como cota de coherencia con k grande)
    T = [[float((1 if i == j else 0) - A[i][j]) for j in range(n)] for i in range(n)]
    gelfand = potencia_norma(T, 64)
    rho = por_metodo[RICHARDSON].rho_original
    if rho is not None and abs(gelfand - rho) > 0.08 * max(1.0, rho):
        errores.append(f"ρ(I−A) {rho} vs Gelfand {gelfand}")
    if errores:
        fallos += 1
        print("FALLO", A, b, errores)
print(f"precondicionamiento: casos {casos} fallos {fallos}")
