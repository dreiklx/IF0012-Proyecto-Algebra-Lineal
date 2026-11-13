"""Interfaz del Módulo IV — vista principal.

Datos del sistema (sección 1), parámetros comunes (sección 2) y las cuatro
pestañas de análisis (sección 3), cada una en su propio archivo.
"""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import (
    ErrorEntrada,
    leer_entero_positivo,
    leer_omega,
    leer_tolerancia,
    leer_vector,
)
from algebra.modulo_IV_iterativos.ejecucion import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    CRITERIO_RESIDUO,
    K_TOPE,
    vector_diagonal,
)
from interfaz.compartido import ejemplos
from interfaz.compartido.componentes import leer_matriz_ui, leer_vector_ui
from interfaz.compartido.editor import (
    MATRIZ,
    VECTOR,
    analizar,
    aviso_dimensiones,
    editor,
    normalizar,
    problema_dimensiones,
    restaurar,
)
from interfaz.compartido.estilo import encabezado_modulo, procedencia, seccion
from interfaz.modulos.modulo_IV_iterativos.pestana_comparar import comparar
from interfaz.modulos.modulo_IV_iterativos.pestana_convergencia import convergencia
from interfaz.modulos.modulo_IV_iterativos.pestana_ejecutar import ejecutar_un_metodo
from interfaz.modulos.modulo_IV_iterativos.pestana_precondicionamiento import precondicionamiento
from visualizacion import notacion

ETIQUETAS_CRITERIO = {
    # Opciones de st.radio: renderizan LaTeX.
    CRITERIO_CAMBIO: r"A · Cambio entre iteraciones  $\|x^{(k)} - x^{(k-1)}\|_\infty < \varepsilon$",
    CRITERIO_RESIDUO: r"B · Residuo del sistema  $\|b - Ax^{(k)}\|_\infty < \varepsilon$",
    CRITERIO_ITERACIONES: "C · Número fijo de iteraciones $N$",
}


def mostrar():
    encabezado_modulo(
        "IV", "Métodos iterativos y convergencia",
        "Jacobi, Gauss-Seidel y SOR implementados desde cero, con criterio de parada, tolerancia, "
        "vector inicial, máximo de iteraciones y factor de relajación configurables. En cada "
        "iteración se registran <b>d<sub>k</sub></b> (cambio entre iteraciones) y <b>r<sub>k</sub></b> (residuo del "
        "sistema original).",
        [("Jacobi", "info"), ("Gauss-Seidel", "info"), ("SOR", "info"), ("Radio espectral", ""),
         ("CSR", "incentivo"), ("Precondicionador M = D", "incentivo")])
    procedencia([
        ("A", "Jacobi, Gauss-Seidel y SOR por componentes", "S8-30/09 pp. 15-33"),
        ("A", "Parada por tolerancia o residuo (Ax: versión absoluta; la lámina usa la relativa)",
         "S8-28/09 p. 6; S8-30/09 p. 28"),
        ("A", "x⁽⁰⁾ = bᵢ/aᵢᵢ", "S8-30/09 pp. 19-20 y 24"),
        ("A", "Dominancia diagonal y reordenamiento", "S8-30/09 p. 37; S9-05/10 pp. 32-33"),
        ("A", "T<sub>J</sub>, T<sub>GS</sub> y ρ(T) por det(T − λI)", "S9-07/10 pp. 3-7"),
        ("B", "Tabla k, x⁽ᵏ⁾, error; motivo; comparación; gráfica", "OFICIAL p. 2"),
        ("C", "CSR y precondicionador M = D", "Incentivos, OFICIAL p. 5; S9-05/10"),
        ("C", "T de SOR, Faddeev-LeVerrier, Durand-Kerner, Richardson", "Extensiones no vistas en clase"),
    ])

    seccion("1", "Sistema A x = b", "A cuadrada, con diagonal no nula")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.ITERATIVOS), key="it_ejemplo")
    A_txt, b_txt = ejemplos.ITERATIVOS[nombre]
    boton.button("⟲ Cargar ejemplo", key="it_cargar", width="stretch", on_click=restaurar,
                 args=(f"it_A_{nombre}", f"it_b_{nombre}", f"it_x0_{nombre}"))
    col1, col2 = st.columns([3, 1.1])
    with col1:
        texto_A = editor(f"it_A_{nombre}", "Matriz A (n × n)", A_txt, MATRIZ, nombre="matriz A",
                         css="it_A", ayuda="Una fila por línea. Los métodos dividen entre cada aᵢᵢ: "
                                           "ningún elemento de la diagonal puede ser 0.")
    with col2:
        texto_b = editor(f"it_b_{nombre}", "Vector b", b_txt.replace(" ", "\n"), VECTOR,
                         nombre="vector b", css="it_b", encabezados=["b"], etiqueta_fila="")

    seccion("2", "Parámetros y criterio de parada", "comunes a las cuatro pestañas")
    criterio = st.radio("Criterio de parada", list(ETIQUETAS_CRITERIO),
                        format_func=ETIQUETAS_CRITERIO.get, key="it_criterio")
    if criterio == CRITERIO_CAMBIO:
        st.caption("Ax usa la diferencia **absoluta** ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞. La lámina S8-28/09 p. 6 escribe "
                   "la **relativa** ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ / ‖x⁽ᵏ⁾‖. Las dos son criterios válidos, pero paran "
                   "en iteraciones distintas. Ver docs/auditoria_procedimientos_pdf.md, sección 2.2.")
    c1, c2, c3 = st.columns(3)
    if criterio == CRITERIO_ITERACIONES:
        texto_n = c1.text_input("N (iteraciones a ejecutar)", "5", key="it_N")
        c2.caption("⚠️ Completar N iteraciones **no demuestra** convergencia.")
        texto_eps = texto_kmax = None
    else:
        texto_eps = c1.text_input("Tolerancia ε (> 0)", "1e-3", key="it_eps")
        texto_kmax = c2.text_input(rf"Máximo de iteraciones $k_{{\max}}$ (1 a {K_TOPE})", "50",
                                   key="it_kmax")
        texto_n = None
    texto_omega = c3.text_input("ω de SOR (0 < ω < 2)", "1.2", key="it_omega",
                                help="Solo se usa con SOR. El rango 0 < ω < 2 no garantiza "
                                     "por sí solo la convergencia.")
    tipo_x0 = st.radio("Vector inicial $x^{(0)}$", ["Vector cero", "xᵢ⁽⁰⁾ = bᵢ / aᵢᵢ", "Personalizado"],
                       horizontal=True, key="it_x0_tipo")
    A_previo = analizar(texto_A, MATRIZ, "matriz A")[0]
    texto_x0 = None
    if tipo_x0 == "Personalizado":
        dimension = len(A_previo[0]) if A_previo else len(A_txt.splitlines())
        x0_col, _ = st.columns([1.1, 3])
        with x0_col:
            texto_x0 = editor(f"it_x0_{nombre}", "x⁽⁰⁾ personalizado", "\n".join(["0"] * dimension),
                              VECTOR, nombre="vector inicial x⁽⁰⁾", css="it_x0", encabezados=["x⁽⁰⁾"],
                              etiqueta_fila="")
    bloqueado = aviso_dimensiones(problema_dimensiones(
        A_previo, analizar(texto_b, VECTOR, "vector b")[0], cuadrada=True,
        x0=analizar(texto_x0, VECTOR, "vector inicial x⁽⁰⁾")[0] if texto_x0 is not None else None))

    seccion("3", "Análisis", "elija una pestaña")
    pestana_uno, pestana_comparar, pestana_conv, pestana_prec = st.tabs(
        ["Ejecutar un método", "Comparar métodos", "Convergencia: dominancia y radio espectral",
         "Precondicionamiento diagonal"])

    def leer_todo(necesita_omega):
        """Lee A, b y los parámetros; devuelve un diccionario o None si hay errores."""
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is None or b is None:
            return None
        try:
            datos = {"A": A, "b": b, "criterio": criterio}
            if criterio == CRITERIO_ITERACIONES:
                datos["n_iteraciones"] = leer_entero_positivo(texto_n, "número de iteraciones N", K_TOPE)
            else:
                datos["tolerancia"] = leer_tolerancia(texto_eps)
                datos["k_max"] = leer_entero_positivo(texto_kmax, "máximo de iteraciones", K_TOPE)
            datos["omega"] = leer_omega(texto_omega) if necesita_omega else 1
            if tipo_x0 == "Vector cero":
                datos["x0"] = None
            elif tipo_x0 == "Personalizado":
                datos["x0"] = leer_vector(normalizar(texto_x0), "vector inicial x⁽⁰⁾")
            else:
                datos["x0"] = vector_diagonal(A, b)
            return datos
        except (ErrorEntrada, ErrorMatriz) as error:
            st.error(f"❌ {notacion.md(str(error))}")
            return None

    with pestana_uno:
        ejecutar_un_metodo(leer_todo, criterio, bloqueado)

    with pestana_comparar:
        comparar(leer_todo, bloqueado)

    with pestana_conv:
        convergencia(texto_A, texto_b, texto_omega, bloqueado)

    with pestana_prec:
        precondicionamiento(leer_todo, bloqueado)
