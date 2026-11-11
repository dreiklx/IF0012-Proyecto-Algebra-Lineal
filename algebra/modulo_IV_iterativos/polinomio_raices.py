"""Módulo IV (convergencia) — Polinomio característico y sus raíces.

EXTENSIONES NO VISTAS EN CLASE (Cat. C).  En clase det(T - λI) se desarrolla por
Sarrus (3x3) y las raíces se obtienen a mano; para cualquier n la aplicación usa:

  * Faddeev-LeVerrier: p(λ) = det(λI - T) = λⁿ + c1 λⁿ⁻¹ + ... + cn, exacto con
    fracciones:
        M0 = 0;   para k = 1..n:   M_k = T·M_{k-1} + c_{k-1}·I,   c_k = -tr(T·M_k) / k
    Para 3x3 coincide con el desarrollo de clase:
        det(T - λI) = -λ³ + tr(T) λ² - (suma de menores principales 2x2) λ + det(T).
  * Raíces:
      - las raíces λ = 0 se extraen de forma exacta (coeficientes finales nulos);
      - grado 1 y 2: fórmula directa (cuadrática con raíz compleja si el
        discriminante es negativo); con fracciones, la decisión |λ| < 1 es exacta
        (condiciones de Schur-Cohn: grado 1 |c1| < 1; grado 2 |c2| < 1 y |c1| < 1 + c2);
      - grado >= 3: método de Durand-Kerner, que aproxima a la vez todas las raíces
        complejas:  z_i <- z_i - p(z_i) / Π_{j≠i} (z_i - z_j).
        No tiene garantía teórica de convergencia global: espectral.py verifica cada
        resultado (|p(λ)| pequeño, suma de raíces = traza) y avisa si falla o si hay
        raíces casi repetidas (con raíces múltiples la precisión disminuye).
"""

import cmath
import math
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import identidad, multiplicar_matrices, validar_cuadrada
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_IV_iterativos.matriz_iteracion import escalar, sumar

UMBRAL_RAICES_CERCANAS = 1e-6  # raíces más cercanas que esto: posible raíz múltiple
AVISO_CASI_REPETIDOS = ("Hay autovalores casi repetidos: con raíces múltiples la "
                        "precisión numérica disminuye.")


def polinomio_caracteristico(T):
    """Coeficientes [1, c1, ..., cn] de p(λ) = det(λI - T), exactos."""
    n = validar_cuadrada(T, "matriz T")
    T_ex = [[a_fraccion(v) for v in fila] for fila in T]
    I = [[Fraction(v) for v in fila] for fila in identidad(n)]
    coeficientes = [Fraction(1)]
    M = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        M = sumar(multiplicar_matrices(T_ex, M), escalar(coeficientes[-1], I))
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

def evaluar(coeficientes, z):
    """Evalúa el polinomio en z por el esquema de Horner."""
    valor = 0
    for c in coeficientes:
        valor = valor * z + c
    return valor

def durand_kerner(coeficientes, max_iter=2000, tol=1e-12):
    """Aproxima todas las raíces de un polinomio mónico de grado >= 1.

    Devuelve (raices, convergio).  coeficientes: [1, c1, ..., cd] (float o Fraction).

    La tolerancia relativa 1e-12 es alcanzable con raíces simples: al evaluar el
    polinomio en punto flotante las correcciones se estancan en un ruido de
    ~1e-15, por lo que una tolerancia de 1e-15 fallaba aleatoriamente (defecto
    corregido en la auditoría final).  Con raíces múltiples la convergencia es
    lenta y la precisión baja a ~eps^(1/m): no se alcanza 1e-12 y se informa.
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
            correccion = evaluar(c, z[i]) / producto
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
                "autovalores pueden ser imprecisos (lo más probable es un autovalor "
                "múltiple, para el que la precisión numérica disminuye).")
        escala = max(1.0, max(abs(z) for z in aproximadas))
        autovalores.extend(_limpiar(z, escala) for z in aproximadas)
        for i in range(len(aproximadas)):
            for j in range(i + 1, len(aproximadas)):
                if abs(aproximadas[i] - aproximadas[j]) < UMBRAL_RAICES_CERCANAS * escala:
                    advertencias.append(AVISO_CASI_REPETIDOS)
                    break
            else:
                continue
            break
    return autovalores, ceros, fiable, advertencias, decision
