"""Portada de la aplicación: presentación, acceso a los cuatro módulos e incentivos.

La figura matemática de la portada no es una ilustración: es la eliminación de
Gauss-Jordan del primer ejemplo del Módulo I, calculada por el núcleo (algebra/)
al abrir la página.
"""

import streamlit as st

from algebra.compartido.validacion import leer_matriz, leer_vector
from algebra.modulo_I_sistemas.directos import resolver_gauss_jordan
from interfaz import navegacion as nav
from interfaz.compartido import ejemplos
from interfaz.compartido.estilo import _e

MODULOS = [
    ("I", "Sistemas lineales y métodos directos", nav.SISTEMAS,
     "Gauss y Gauss-Jordan con cada operación elemental; clasificación por rangos, "
     "solución paramétrica e interpretación geométrica.",
     "Gauss · Gauss-Jordan · rango · det"),
    ("II", "Condicionamiento y sensibilidad", nav.CONDICIONAMIENTO,
     "κ<sub>∞</sub>(A) = ‖A‖<sub>∞</sub>‖A⁻¹‖<sub>∞</sub> con la inversa por Gauss-Jordan y el efecto de perturbar b "
     "en la solución.",
     "κ<sub>∞</sub> · inversa · perturbación"),
    ("III", "Mínimos cuadrados y ajuste lineal", nav.MINIMOS,
     "Ecuaciones normales AᵀA x̂ = Aᵀb, residuo y comprobación Aᵀr = 0; recta y = mx + c "
     "con verificación por Cramer.",
     "AᵀA · residuo · recta de ajuste"),
    ("IV", "Métodos iterativos y convergencia", nav.ITERATIVOS,
     "Jacobi, Gauss-Seidel y SOR con los criterios A, B y C; comparación, dominancia "
     "diagonal y radio espectral.",
     "Jacobi · Gauss-Seidel · SOR · ρ(T)"),
]

# Cada incentivo de la rúbrica (OFICIAL p. 5) con la funcionalidad REAL que lo implementa.
INCENTIVOS = [
    ("Visualización avanzada", "hasta 1 %", nav.ITERATIVOS,
     "Comparación superpuesta de los tres métodos, autovalores con el círculo unidad, "
     "barrido de ω y exportación del historial a CSV.",
     "IV → «Comparar métodos» y «Ejecutar un método» (botón CSV)"),
    ("Precondicionamiento", "hasta 1,5 %", nav.ITERATIVOS,
     "Precondicionador diagonal M = D: κ<sub>∞</sub>(A) frente a κ<sub>∞</sub>(D⁻¹A), autovalores, iteraciones "
     "con y sin M y comparación exacta de la matriz de iteración.",
     "IV → pestaña «Precondicionamiento diagonal»"),
    ("Matrices dispersas", "hasta 1 %", nav.ITERATIVOS,
     "Formato CSR propio: cada iteración recorre solo los no nulos (O(nnz)) y da las mismas "
     "iteraciones que el formato denso.",
     "IV → «Ejecutar un método» → casilla «Usar almacenamiento disperso (CSR)»"),
    ("Experiencia de usuario", "hasta 0,5 %", nav.SISTEMAS,
     "Editor de matrices con validación previa, ejemplos del curso precargados, ayudas en cada "
     "campo, sugerencia de reordenamiento y gráficas interactivas.",
     "Todos los módulos; I → «Interpretación geométrica»"),
    ("Extensión matemática", "hasta 1 %", nav.ITERATIVOS,
     "Radio espectral con autovalores complejos (Faddeev-LeVerrier y Durand-Kerner), "
     "decisiones exactas, matriz de iteración de SOR y Richardson (extensión no vista en clase).",
     "IV → «Convergencia: dominancia y radio espectral»"),
]


def _fraccion(valor):
    return f"{valor.numerator}/{valor.denominator}" if valor.denominator != 1 else str(valor.numerator)


def _matriz_aumentada(filas, n, clase=""):
    """Matriz aumentada [A | b] en HTML; las celdas de la diagonal y de b llevan su clase."""
    celdas = []
    for i, fila in enumerate(filas):
        for j, valor in enumerate(fila):
            tipo = "b" if j == n else ("d" if i == j else "")
            celdas.append(f'<span class="fm-c {tipo}">{_e(_fraccion(valor))}</span>')
    return (f'<div class="fm-matriz {clase}" style="grid-template-columns:repeat({n},auto) auto">'
            + "".join(celdas) + "</div>")


def _figura():
    """[A | b] → [I | x] del primer ejemplo del Módulo I, calculado por el núcleo."""
    nombre, (texto_A, texto_b) = next(iter(ejemplos.DIRECTOS.items()))
    A, b = leer_matriz(texto_A), leer_vector(texto_b)
    r = resolver_gauss_jordan(A, b)
    if r.solucion is None or r.matriz_final is None:
        return ""
    n = len(A)
    inicial = [list(fila) + [bi] for fila, bi in zip(A, b)]
    x = ", ".join(_fraccion(v) for v in r.solucion)
    return (
        '<figure class="fm">'
        '<div class="fm-fila">'
        f'{_matriz_aumentada(inicial, n)}'
        '<div class="fm-flecha"><span>Gauss-Jordan</span>∼</div>'
        f'{_matriz_aumentada(r.matriz_final, n, "final")}'
        '</div>'
        f'<figcaption><span class="fm-x">x = ({_e(x)})</span>'
        f'<span>rango {r.rango_A} · det(A) = {_e(_fraccion(r.determinante))} · {len(r.pasos)} pasos</span>'
        f'<span class="fm-fuente">Ejemplo del Módulo I ({_e(nombre.split(" — ")[0])}), '
        'resuelto por el núcleo al abrir esta página.</span></figcaption>'
        '</figure>')


def mostrar():
    with st.container(key="portada_hero"):
        texto, figura = st.columns([1.15, 1], gap="large", vertical_alignment="center")
        with texto:
            st.markdown('<div class="eyebrow">IF0012 · Universidad de Costa Rica · II Ciclo 2026</div>',
                        unsafe_allow_html=True)
            st.title("Álgebra Lineal Numérica")
            st.markdown(
                '<p class="lede">Modelar, resolver y analizar sistemas lineales: métodos directos, '
                'condicionamiento, mínimos cuadrados y métodos iterativos. Cada resultado llega con '
                'el procedimiento que lo produce y con su interpretación.</p>'
                '<dl class="hechos">'
                '<div><dt>Núcleo</dt><dd>Python puro, implementado desde cero</dd></div>'
                '<div><dt>Directos</dt><dd>Fracciones exactas, sin redondeo</dd></div>'
                '<div><dt>Iterativos</dt><dd>Punto flotante con tolerancia</dd></div>'
                '</dl>', unsafe_allow_html=True)
        with figura:
            st.markdown(_figura(), unsafe_allow_html=True)

    st.markdown('<h2 class="rotulo">Módulos</h2>', unsafe_allow_html=True)
    with st.container(key="portada_modulos"):
        for columna, (numero, titulo, pagina, descripcion, claves) in zip(st.columns(4, gap="medium"), MODULOS):
            with columna:
                st.markdown(f'<div class="mod"><div class="mod-num">{numero}</div><h3>{_e(titulo)}</h3>'
                            f'<p>{_e(descripcion)}</p><div class="mod-claves">{_e(claves)}</div></div>',
                            unsafe_allow_html=True)
                st.page_link(pagina, label=f"Abrir el módulo {numero}  →")

    st.markdown('<h2 class="rotulo">Incentivos implementados <span class="rotulo-nota">OFICIAL p. 5 · el puntaje lo '
                'asigna la docente</span></h2>', unsafe_allow_html=True)
    with st.container(key="portada_incentivos"):
        for nombre, maximo, pagina, descripcion, donde in INCENTIVOS:
            nom, desc, ir = st.columns([2.1, 5, 1.25], vertical_alignment="center")
            nom.markdown(f'<div class="inc-nombre">{_e(nombre)}</div><div class="inc-max">{_e(maximo)}</div>',
                         unsafe_allow_html=True)
            desc.markdown(f'<div class="inc-desc">{_e(descripcion)}</div>'
                          f'<div class="inc-donde">Dónde verlo: {_e(donde)}</div>', unsafe_allow_html=True)
            with ir:
                st.page_link(pagina, label="Ver →")

    st.markdown(
        '<div class="nota"><b>Procedencia de cada procedimiento.</b> En cada módulo, los distintivos '
        '«Cat.» indican de dónde sale lo que se calcula: <b>Cat. A</b>, visto en clase (con la página '
        'del PDF al pasar el cursor); <b>Cat. B</b>, exigido por el enunciado del proyecto; <b>Cat. C</b>, '
        'extensión o incentivo no visto en clase (por ejemplo Richardson, Faddeev-LeVerrier y '
        'Durand-Kerner); <b>Cat. D</b>, sin respaldo en el material.</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="rotulo">Cómo introducir los datos</h2>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        st.markdown(
            "Cada módulo tiene un **editor de matrices**: una celda por elemento, con botones para "
            "agregar o quitar filas y columnas. En la pestaña «Pegar» se escribe **una fila por línea**, "
            "con los números separados por espacios. Se aceptan enteros, decimales (`2.5` o `2,5`), "
            "fracciones (`1/3`) y notación científica (`1e-3`). Cada módulo incluye **ejemplos del curso** "
            "para cargar con un clic.")
        st.code("Matriz A          Vector b\n2 1 -1            1\n1 -3 2            4\n3 2 1             0",
                language=None)
    with c2:
        st.markdown(
            '<div class="nota">Los métodos directos, la inversa, el condicionamiento y los mínimos '
            'cuadrados usan <b>fracciones exactas</b>: los resultados no tienen errores de redondeo. '
            'Los métodos iterativos usan <b>punto flotante</b>, porque son aproximaciones que se '
            'detienen por tolerancia.</div>', unsafe_allow_html=True)
        st.caption(
            "Algunos ejemplos numéricos de las láminas del curso contienen errores aritméticos; "
            "la aplicación muestra los resultados correctos, verificados de forma independiente "
            "(ver docs/guia_matematica.md y casos_prueba/).")

    st.markdown(
        '<footer class="pie"><span><b>Universidad de Costa Rica</b> · Sede del Caribe · II Ciclo 2026</span>'
        '<span>Proyecto final · Grupo 01</span>'
        '<span>Núcleo: Python puro (biblioteca estándar) · Interfaz: Streamlit · '
        'Gráficas: Plotly</span></footer>', unsafe_allow_html=True)
