"""Componentes comunes de la interfaz Streamlit.

Aquí solo hay presentación: convertir resultados del núcleo a LaTeX o a
tablas y mostrar errores de entrada.  Ningún cálculo matemático vive aquí.
"""

from fractions import Fraction

import streamlit as st

from algebra.matriz import ErrorMatriz
from algebra.validacion import ErrorEntrada, formatear_numero, leer_matriz, leer_vector


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------

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
    filas = r" \\ ".join(" & ".join(latex_numero(v, cifras) for v in fila) for fila in M)
    return rf"\left[\begin{{array}}{{{columnas}}} {filas} \end{{array}}\right]"


def latex_vector(v, cifras=6):
    return latex_matriz([[x] for x in v], cifras=cifras)


def texto_vector(v, cifras=6):
    return "(" + ", ".join(formatear_numero(x, cifras) for x in v) + ")"


# ---------------------------------------------------------------------------
# Entrada de datos
# ---------------------------------------------------------------------------

def leer_matriz_ui(texto, nombre):
    """Lee una matriz; si hay error lo muestra y devuelve None."""
    try:
        return leer_matriz(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {error}")
        return None


def leer_vector_ui(texto, nombre):
    try:
        return leer_vector(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {error}")
        return None


def ayuda_formato():
    st.caption(
        "Formato: una fila por línea y los números separados por espacios. "
        "Se aceptan enteros, decimales con punto o coma (2.5 o 2,5), fracciones (1/3) "
        "y notación científica (1e-3).")


def tabla_vector(v, nombre="x", cifras=6):
    """Filas para st.table: componente, valor exacto (si es fracción) y decimal."""
    filas = []
    for i, valor in enumerate(v, start=1):
        fila = {"Componente": f"{nombre}{i}", "Valor": formatear_numero(valor, cifras)}
        if isinstance(valor, Fraction):
            fila["Decimal"] = f"{float(valor):.10g}"
        filas.append(fila)
    return filas


def mostrar_pasos(pasos, separador):
    """Muestra el procedimiento paso a paso (descripción + matriz)."""
    for numero, paso in enumerate(pasos):
        st.markdown(f"**Paso {numero}.** {paso.descripcion}")
        st.latex(latex_matriz(paso.matriz, separador=separador))
