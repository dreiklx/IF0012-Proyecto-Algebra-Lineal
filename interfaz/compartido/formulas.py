"""Cómo se escribe cada resultado en LaTeX (matrices, vectores, fracciones,
polinomio característico y despejes de los métodos iterativos).

Solo presentación: recibe valores que ya calculó el núcleo (algebra/) y devuelve
texto LaTeX para st.latex o st.markdown.  Ningún cálculo matemático vive aquí.
"""

from fractions import Fraction

from algebra.compartido.validacion import formatear_numero
from visualizacion import notacion


def latex_numero(valor, cifras=6):
    """Fracción exacta como \\frac{p}{q}; el resto como decimal."""
    if isinstance(valor, Fraction) and valor.denominator != 1:
        if len(str(valor)) <= 14:
            signo = "-" if valor < 0 else ""
            return rf"{signo}\frac{{{abs(valor.numerator)}}}{{{valor.denominator}}}"
        return formatear_numero(float(valor), cifras)
    if isinstance(valor, complex):
        return formatear_numero(valor, cifras).replace("−", "-").replace("i", r"\,i")
    return formatear_numero(valor, cifras)


def latex_matriz(M, separador=None, cifras=6):
    """Matriz entre corchetes; `separador` es el índice de columna antes del que
    se dibuja una línea vertical (para [A | b])."""
    n = len(M[0])
    columnas = "".join("c" if separador is None or j != separador else "|c" for j in range(n))
    # Las fracciones apiladas (\frac) quedan montadas entre filas si no se añade
    # espacio vertical (defecto visual detectado en la revisión manual).
    hay_fracciones = any(isinstance(v, Fraction) and v.denominator != 1 for fila in M for v in fila)
    salto = r" \\[6pt] " if hay_fracciones else r" \\ "
    filas = salto.join(" & ".join(latex_numero(v, cifras) for v in fila) for fila in M)
    return rf"\left[\begin{{array}}{{{columnas}}} {filas} \end{{array}}\right]"


def latex_vector(v, cifras=6):
    return latex_matriz([[x] for x in v], cifras=cifras)


def latex_polinomio(coeficientes):
    """det(T − λI) = (−1)ⁿ p(λ) en LaTeX, con el mismo signo y los mismos términos que
    algebra/.../espectral.py::texto_polinomio_curso (aquí con fracciones apiladas).
    `coeficientes` son los de p(λ), de mayor a menor grado."""
    n = len(coeficientes) - 1
    signo = -1 if n % 2 else 1
    terminos = []
    for k, c in enumerate(coeficientes):
        valor = signo * c
        if valor == 0:
            continue
        grado = n - k
        potencia = "" if grado == 0 else (r"\lambda" if grado == 1 else rf"\lambda^{{{grado}}}")
        magnitud = latex_numero(abs(valor))
        texto = potencia if (abs(valor) == 1 and grado > 0) else magnitud + potencia
        terminos.append(("-" if valor < 0 else "+", texto))
    if not terminos:
        return "0"
    primero = ("-" if terminos[0][0] == "-" else "") + terminos[0][1]
    return primero + "".join(f" {s} {t}" for s, t in terminos[1:])


def tabla_vector(v, nombre="x", cifras=6):
    """Filas para st.table: componente, valor exacto (si es fracción) y decimal."""
    filas = []
    for i, valor in enumerate(v, start=1):
        fila = {"Componente": f"{nombre}{notacion.subindice(i)}", "Valor": formatear_numero(valor, cifras)}
        if isinstance(valor, Fraction):
            fila["Decimal"] = f"{float(valor):.10g}"
        filas.append(fila)
    return filas


def latex_despejes(A, b, metodo, omega=None):
    """Despeje de cada incógnita, como lo escribe la profesora antes de iterar
    (S8-30/09 p. 19 Jacobi, p. 24 Gauss-Seidel, p. 32 SOR).  Solo escribe A, b y ω:
    no calcula ninguna iteración.  Devuelve una línea LaTeX por incógnita (SOR: dos)."""
    n = len(A)
    lineas = []
    for i in range(n):
        numerador = latex_numero(b[i])
        for j in range(n):
            if j == i or A[i][j] == 0:
                continue
            nuevo = metodo != "Jacobi" and j < i       # Gauss-Seidel y SOR usan lo ya calculado
            indice = "(k+1)" if nuevo else "(k)"
            magnitud = abs(A[i][j])
            coeficiente = "" if magnitud == 1 else latex_numero(magnitud)
            numerador += (" - " if A[i][j] > 0 else " + ") + rf"{coeficiente}x_{{{j + 1}}}^{{{indice}}}"
        cociente = rf"\dfrac{{{numerador}}}{{{latex_numero(A[i][i])}}}"
        if metodo == "SOR":
            w = latex_numero(omega)
            lineas.append(rf"x_{{{i + 1}}}^{{GS}} = {cociente}")
            lineas.append(rf"x_{{{i + 1}}}^{{(k+1)}} = (1 - {w})\,x_{{{i + 1}}}^{{(k)}} + {w}\,x_{{{i + 1}}}^{{GS}}")
        else:
            lineas.append(rf"x_{{{i + 1}}}^{{(k+1)}} = {cociente}")
    return lineas
