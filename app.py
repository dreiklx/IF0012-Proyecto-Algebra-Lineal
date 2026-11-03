"""Aplicación integrada del proyecto final IF0012 — Álgebra Lineal (II Ciclo 2026).

Ejecutar con:   streamlit run app.py      (o con ejecutar.bat en Windows)

La aplicación es una sola interfaz con los cuatro módulos del enunciado
(OFICIAL p. 2).  Todos los cálculos se hacen en el paquete `algebra`
(implementado desde cero); este archivo solo organiza la navegación y la portada.
"""

import streamlit as st

from interfaz import (
    modulo_condicionamiento,
    modulo_directos,
    modulo_iterativos,
    modulo_minimos,
)
from interfaz.estilo import aplicar_estilo, bloque_lateral, insignias_html

st.set_page_config(page_title="IF0012 · Álgebra Lineal", page_icon="🧮", layout="wide")
aplicar_estilo()

INICIO = "🏠 Inicio"
PAGINAS = {
    INICIO: None,
    "I · Sistemas lineales (Gauss)": modulo_directos,
    "II · Condicionamiento": modulo_condicionamiento,
    "III · Mínimos cuadrados": modulo_minimos,
    "IV · Métodos iterativos": modulo_iterativos,
}
NOMBRES = list(PAGINAS)

MODULOS = [
    ("I", "Sistemas lineales y métodos directos", NOMBRES[1],
     ["Gauss y Gauss-Jordan con cada operación elemental",
      "Clasificación por rangos: única, infinitas o inconsistente",
      "Solución paramétrica, determinante e interpretación geométrica"]),
    ("II", "Condicionamiento y sensibilidad", NOMBRES[2],
     ["κ∞(A) = ‖A‖∞‖A⁻¹‖∞ con la inversa por Gauss-Jordan",
      "Escala del proyecto: baja, moderada o alta",
      "Perturbación de b (absoluta o porcentual) y errores relativos"]),
    ("III", "Mínimos cuadrados y ajuste lineal", NOMBRES[3],
     ["Ecuaciones normales AᵀA x̂ = Aᵀb resueltas con Gauss",
      "Residuo, ‖r‖₂ y comprobación Aᵀr = 0",
      "Recta y = mx + c con gráfica; verificación por Cramer"]),
    ("IV", "Métodos iterativos y convergencia", NOMBRES[4],
     ["Jacobi, Gauss-Seidel y SOR con criterios A, B y C",
      "Comparación con error final e gráfica de convergencia",
      "Dominancia diagonal, matriz de iteración y radio espectral"]),
]

# Cada incentivo de la rúbrica (OFICIAL p. 5) con la funcionalidad REAL que lo implementa.
INCENTIVOS = [
    ("Visualización avanzada", "hasta 1 %", NOMBRES[4],
     "Comparación superpuesta de los tres métodos, autovalores con el círculo unidad, "
     "barrido de ω y exportación del historial a CSV.",
     "IV → «Comparar métodos» y «Ejecutar un método» (botón CSV)"),
    ("Precondicionamiento", "hasta 1,5 %", NOMBRES[4],
     "Precondicionador diagonal M = D: κ∞(A) frente a κ∞(D⁻¹A), autovalores, iteraciones "
     "con y sin M y comparación exacta de la matriz de iteración.",
     "IV → pestaña «Precondicionamiento diagonal»"),
    ("Matrices dispersas", "hasta 1 %", NOMBRES[4],
     "Formato CSR propio: cada iteración recorre solo los no nulos (O(nnz)) y da las mismas "
     "iteraciones que el formato denso.",
     "IV → «Ejecutar un método» → casilla «Usar almacenamiento disperso (CSR)»"),
    ("Experiencia de usuario", "hasta 0,5 %", NOMBRES[1],
     "Ejemplos del curso precargados, errores con la celda exacta, ayudas en cada campo, "
     "sugerencia de reordenamiento y la interpretación geométrica.",
     "Todos los módulos; I → «Interpretación geométrica»"),
    ("Extensión matemática", "hasta 1 %", NOMBRES[4],
     "Radio espectral con autovalores complejos (Faddeev-LeVerrier y Durand-Kerner), "
     "decisiones exactas, matriz de iteración de SOR y Richardson.",
     "IV → «Convergencia: dominancia y radio espectral»"),
]


def ir_a(pagina):
    st.session_state["navegacion"] = pagina


def inicio():
    with st.container(key="hero_portada"):
        st.markdown('<div class="hero-eyebrow">IF0012 · Álgebra Lineal para Informática '
                    'Empresarial · UCR · II Ciclo 2026</div>', unsafe_allow_html=True)
        st.title("Álgebra Lineal Numérica")
        st.markdown(
            '<p class="hero-texto">Aplicación integrada para <b>modelar, resolver y analizar</b> '
            'sistemas lineales: métodos directos, condicionamiento, mínimos cuadrados y métodos '
            'iterativos. Cada resultado se acompaña del procedimiento que lo produce y de su '
            'interpretación.</p>'
            + insignias_html([("Algoritmos implementados desde cero", "info"),
                              ("Fracciones exactas en los métodos directos", "ok"),
                              ("Punto flotante con tolerancia en los iterativos", ""),
                              ("Sin bibliotecas de álgebra lineal", "")]),
            unsafe_allow_html=True)

    st.markdown("### Módulos")
    columnas = st.columns(2)
    for indice, (numero, titulo, pagina, puntos) in enumerate(MODULOS):
        with columnas[indice % 2]:
            with st.container(border=True):
                lista = "".join(f"<li>{p}</li>" for p in puntos)
                st.markdown(f'<div class="tarjeta" style="border:none;background:none;padding:.2rem 0">'
                            f'<div class="num">MÓDULO {numero}</div><h4>{titulo}</h4>'
                            f'<ul>{lista}</ul></div>', unsafe_allow_html=True)
                st.button(f"Abrir el módulo {numero}", key=f"ir_{numero}", on_click=ir_a,
                          args=(pagina,), type="primary", width="stretch")

    st.markdown("### Incentivos implementados (OFICIAL p. 5)")
    st.caption("Cada incentivo corresponde a una funcionalidad real de la aplicación; la tarjeta "
               "indica dónde demostrarla. El puntaje lo asigna la docente.")
    columnas = st.columns(3)
    for indice, (nombre, maximo, pagina, descripcion, donde) in enumerate(INCENTIVOS):
        with columnas[indice % 3]:
            with st.container(border=True):
                st.markdown(f'<div class="tarjeta" style="border:none;background:none;padding:.2rem 0">'
                            + insignias_html([(maximo, "incentivo")])
                            + f'<h4>{nombre}</h4><p>{descripcion}</p>'
                            f'<div class="donde">Dónde verlo: <b>{donde}</b></div></div>',
                            unsafe_allow_html=True)
                st.button("Ir a la demostración", key=f"inc_{indice}", on_click=ir_a,
                          args=(pagina,), width="stretch")

    st.markdown("### Cómo introducir los datos")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            "Una **fila de la matriz por línea**, con los números separados por espacios. Se aceptan "
            "enteros, decimales (`2.5` o `2,5`), fracciones (`1/3`) y notación científica (`1e-3`). "
            "Cada módulo incluye **ejemplos del curso** para cargar con un clic.")
        st.code("Matriz A          Vector b\n2 1 -1            1\n1 -3 2            4\n3 2 1             0",
                language=None)
    with c2:
        st.info(
            "Los métodos directos, la inversa, el condicionamiento y los mínimos cuadrados usan "
            "**fracciones exactas**: los resultados no tienen errores de redondeo. Los métodos "
            "iterativos usan **punto flotante**, porque son aproximaciones que se detienen por tolerancia.")
        st.caption(
            "Algunos ejemplos numéricos de las láminas del curso contienen errores aritméticos; "
            "la aplicación muestra los resultados correctos, verificados de forma independiente "
            "(ver docs/guia_matematica.md y casos_prueba/).")


st.sidebar.markdown(
    '<div class="marca"><div class="marca-logo">Ax</div><div><div class="marca-titulo">'
    'IF0012 · Álgebra Lineal</div><div class="marca-sub">Proyecto final · Grupo 01</div></div></div>',
    unsafe_allow_html=True)
pagina = st.sidebar.radio("Módulos", NOMBRES, key="navegacion")
bloque_lateral("<b>Entrada:</b> una fila por línea; números separados por espacios. "
               "Fracciones (1/3), decimales (2,5) y notación científica (1e-3).")
bloque_lateral("<b>Universidad de Costa Rica</b> · Sede del Caribe · II Ciclo 2026<br>"
               "Núcleo matemático: Python puro (biblioteca estándar). "
               "Interfaz: Streamlit. Gráficas: Matplotlib.")

modulo = PAGINAS[pagina]
if modulo is None:
    inicio()
else:
    modulo.mostrar()
