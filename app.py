"""Aplicación integrada del proyecto final IF0012 — Álgebra Lineal (II Ciclo 2026).

Ejecutar con:   streamlit run app.py      (o con ejecutar.bat en Windows)

La aplicación es una sola interfaz con los cuatro módulos del enunciado
(OFICIAL p. 2).  Todos los cálculos se hacen en el paquete `algebra`
(implementado desde cero); este archivo solo organiza la navegación.
"""

import streamlit as st

from interfaz import (
    modulo_condicionamiento,
    modulo_directos,
    modulo_iterativos,
    modulo_minimos,
)

st.set_page_config(page_title="IF0012 · Álgebra Lineal", page_icon="🧮", layout="wide")

PAGINAS = {
    "🏠 Inicio": None,
    "I · Sistemas lineales (Gauss)": modulo_directos,
    "II · Condicionamiento": modulo_condicionamiento,
    "III · Mínimos cuadrados": modulo_minimos,
    "IV · Métodos iterativos": modulo_iterativos,
}


def inicio():
    st.title("🧮 Álgebra Lineal Numérica — Proyecto IF0012")
    st.markdown(
        """
Aplicación integrada para **modelar, resolver y analizar** problemas de álgebra lineal
y análisis numérico. Todos los algoritmos centrales se implementaron **desde cero**
en Python, sin bibliotecas de álgebra lineal.

| Módulo | Qué hace |
|---|---|
| **I · Sistemas lineales** | Gauss y Gauss-Jordan paso a paso, clasificación (única / infinitas / inconsistente), interpretación geométrica |
| **II · Condicionamiento** | κ∞(A) con inversa propia, perturbación de b, errores relativos e interpretación |
| **III · Mínimos cuadrados** | Ecuaciones normales AᵀA x̂ = Aᵀb, residuo, ‖r‖₂ y ajuste lineal con gráfica |
| **IV · Métodos iterativos** | Jacobi, Gauss-Seidel y SOR con criterios de parada configurables, comparación, dominancia diagonal (con sugerencia de reordenamiento), radio espectral y precondicionador diagonal |

**Cómo introducir datos:** una fila de la matriz por línea, con los números separados por
espacios. Se aceptan enteros, decimales (`2.5` o `2,5`), fracciones (`1/3`) y notación
científica (`1e-3`). Cada módulo incluye ejemplos del curso para cargar con un clic.
"""
    )
    st.info(
        "Los métodos directos, la inversa, el condicionamiento y los mínimos cuadrados usan "
        "**fracciones exactas**: los resultados no tienen errores de redondeo. Los métodos "
        "iterativos usan **punto flotante**, porque son aproximaciones que se detienen por tolerancia.")
    st.caption(
        "Algunos ejemplos numéricos de las láminas del curso contienen errores aritméticos; "
        "la aplicación muestra los resultados correctos, verificados de forma independiente "
        "(ver docs/guia_matematica.md y casos_prueba/).")


st.sidebar.title("IF0012 · Álgebra Lineal")
pagina = st.sidebar.radio("Módulos", list(PAGINAS), key="navegacion")
st.sidebar.divider()
st.sidebar.caption("Universidad de Costa Rica · II Ciclo 2026\n\n"
                   "Núcleo matemático: Python puro (biblioteca estándar). "
                   "Interfaz: Streamlit. Gráficas: Matplotlib.")

modulo = PAGINAS[pagina]
if modulo is None:
    inicio()
else:
    modulo.mostrar()
