"""Módulo IV (convergencia) — Polinomio característico y sus raíces, solo con procedimientos de clase.

  * det(T − λI) se desarrolla por Sarrus (3×3), como en S9-07/10 p. 5 y S9-07/10 p. 6, y en
    2×2 por la fórmula directa.  Los coeficientes son exactos (fracciones).
  * Las raíces se obtienen como en clase: se extrae λ = 0 (factor común) y se resuelve el
    resto de grado 1 o 2 (fórmula cuadrática).

Para n ≥ 4, o si el polinomio restante tiene grado ≥ 3 (sin factorización elemental), el
radio espectral no se calcula: OFICIAL p. 2 exige ρ(T) «cuando el procedimiento estudiado lo
permita».  No se usan métodos numéricos de búsqueda de raíces.
"""

import math
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import validar_cuadrada
from algebra.compartido.validacion import formatear_numero

N_MAX_CARACTERISTICO = 3   # Sarrus: solo matrices 2×2 y 3×3 (procedimiento de clase)


class ErrorNoCalculable(ValueError):
    """El procedimiento del curso no permite obtener el polinomio o sus raíces."""


# --- polinomios con coeficientes exactos: lista [a0, a1, ...] de menor a mayor grado ---

def _pmul(p, q):
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def _padd(p, q, signo=1):
    n = max(len(p), len(q))
    p = p + [Fraction(0)] * (n - len(p))
    q = q + [Fraction(0)] * (n - len(q))
    return [a + signo * b for a, b in zip(p, q)]


def _sarrus(M):
    """Regla de Sarrus para una matriz 3×3 con entradas polinomiales."""
    t1 = _pmul(_pmul(M[0][0], M[1][1]), M[2][2])
    t2 = _pmul(_pmul(M[0][1], M[1][2]), M[2][0])
    t3 = _pmul(_pmul(M[0][2], M[1][0]), M[2][1])
    s1 = _pmul(_pmul(M[0][2], M[1][1]), M[2][0])
    s2 = _pmul(_pmul(M[0][0], M[1][2]), M[2][1])
    s3 = _pmul(_pmul(M[0][1], M[1][0]), M[2][2])
    return _padd(_padd(_padd(t1, t2), t3), _padd(_padd(s1, s2), s3), -1)


def polinomio_caracteristico(T):
    """Coeficientes [1, c1, ..., cn] de p(λ) = det(λI − T) en orden de grado descendente.

    Calculado con Sarrus (3×3) o con la fórmula de 2×2: det(T − λI) = (−1)ⁿ p(λ)."""
    n = validar_cuadrada(T, "matriz T")
    if n > N_MAX_CARACTERISTICO:
        raise ErrorNoCalculable(
            f"Para n > {N_MAX_CARACTERISTICO} el polinomio característico no se obtiene con "
            "el procedimiento del curso (Sarrus solo cubre 2×2 y 3×3).")
    M = [[[a_fraccion(T[i][j]), Fraction(0)] if i != j else [a_fraccion(T[i][j]), Fraction(-1)]
          for j in range(n)] for i in range(n)]
    if n == 1:
        det = M[0][0]
    elif n == 2:
        det = _padd(_pmul(M[0][0], M[1][1]), _pmul(M[0][1], M[1][0]), -1)
    else:
        det = _sarrus(M)
    while len(det) > 1 and det[-1] == 0:
        det.pop()
    # det(T − λI) = (−1)ⁿ p(λ): se normaliza a p mónico de grado n, en orden descendente.
    signo = -1 if n % 2 else 1
    mon = [Fraction(signo) * c for c in reversed(det)]
    if mon[0] != 1:
        mon = [c / mon[0] for c in mon]
    return mon


def texto_polinomio_curso(coeficientes):
    """Escribe det(T − λI) como en los apuntes, por ejemplo −λ³ − (4/9)λ + 4/3."""
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


def evaluar(coeficientes, z):
    """Evalúa el polinomio en z por Horner (solo para verificar raíces ya calculadas)."""
    valor = 0
    for c in coeficientes:
        valor = valor * z + c
    return valor


def raices(coeficientes):
    """Raíces de p(λ) con los procedimientos del curso.

    Devuelve (autovalores, multiplicidad_cero) si se pueden obtener, o (None, ceros) si el
    polinomio restante tiene grado ≥ 3 sin factorización elemental.
    """
    reducido = list(coeficientes)
    ceros = 0
    while len(reducido) > 1 and reducido[-1] == 0:      # factor común λ
        reducido.pop()
        ceros += 1
    grado = len(reducido) - 1
    autovalores = [complex(0)] * ceros
    if grado == 0:
        return autovalores, ceros
    if grado == 1:
        autovalores.append(complex(float(-reducido[1])))
        return autovalores, ceros
    if grado == 2:
        c1, c2 = reducido[1], reducido[2]
        discriminante = c1 * c1 - 4 * c2
        if discriminante >= 0:
            raiz = math.sqrt(float(discriminante))
            autovalores += [complex((-float(c1) + raiz) / 2), complex((-float(c1) - raiz) / 2)]
        else:
            parte = math.sqrt(float(-discriminante))
            autovalores += [complex(-float(c1) / 2, parte / 2), complex(-float(c1) / 2, -parte / 2)]
        return autovalores, ceros
    return None, ceros
