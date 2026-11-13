"""Interfaz del Módulo I — Sistemas lineales y métodos directos."""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz, residuo
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_I_sistemas.directos import (
    INFINITAS,
    PIVOTEO_PRIMER_NO_NULO,
    UNICA,
    resolver_gauss,
    resolver_gauss_jordan,
)
from interfaz.compartido import control_gestual, ejemplos
from interfaz.compartido.componentes import (
    CONTROLES_2D,
    CONTROLES_3D,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_interactiva,
    mostrar_pasos,
)
from interfaz.compartido.formulas import (
    latex_matriz,
    latex_numero,
    latex_vector,
    tabla_vector,
)
from interfaz.compartido.editor import (
    MATRIZ,
    VECTOR,
    analizar,
    aviso_dimensiones,
    editor,
    problema_dimensiones,
    restaurar,
)
from interfaz.compartido.estilo import (
    encabezado_modulo,
    insignias,
    marca_incentivo,
    procedencia,
    seccion,
    tarjeta_resultado,
)
from visualizacion import notacion
from visualizacion.interactivas import planos_3d, rectas_2d


def mostrar():
    encabezado_modulo(
        "I", "Sistemas lineales y métodos directos",
        "Resuelve <b>A x = b</b> con eliminación de Gauss o Gauss-Jordan (implementadas desde cero, "
        "con aritmética de fracciones exactas), muestra cada operación elemental y clasifica el "
        "sistema según los rangos de A y de [A | b].",
        [("Gauss", "info"), ("Gauss-Jordan", "info"), ("Fracciones exactas", "ok"),
         ("Paso a paso", "")])
    procedencia([
        ("A", "[A | b] y operaciones elementales", "S2-19/08 p. 27; S6-14/09 pp. 25-27"),
        ("A", "Gauss y sustitución hacia atrás", "S6-14/09 pp. 28-32; S6-16/09 p. 29"),
        ("A", "Gauss-Jordan", "S3-24/08 pp. 4-5; S6-14/09 p. 30"),
        ("A", "Tipos de solución", "S6-14/09 p. 26; S6-16/09 p. 29"),
        ("B", "Pivotes nulos o problemáticos", "OFICIAL p. 2"),
        ("C", "Gráfica de rectas y planos", "UX; interpretación de S6-14/09 p. 26"),
    ])

    seccion("1", "Datos del sistema", "Construya A y b en el editor, péguelos o cargue un ejemplo del curso")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.DIRECTOS), key="dir_ejemplo")
    A_txt, b_txt = ejemplos.DIRECTOS[nombre]
    boton.button("⟲ Cargar ejemplo", key="dir_cargar", width="stretch", on_click=restaurar,
                 args=(f"dir_A_{nombre}", f"dir_b_{nombre}"),
                 help="Vuelve a cargar el ejemplo seleccionado (descarta los cambios).")
    col1, col2 = st.columns([3, 1.1])
    with col1:
        texto_A = editor(f"dir_A_{nombre}", "Matriz A (m × n)", A_txt, MATRIZ, nombre="matriz A",
                         css="dir_A", ayuda="Una fila por línea. Ejemplo: «2 1 -1» en la primera línea.")
    with col2:
        texto_b = editor(f"dir_b_{nombre}", "Vector b (m)", b_txt.replace(" ", "\n"), VECTOR,
                         nombre="vector b", css="dir_b", encabezados=["b"], etiqueta_fila="")
    bloqueado = aviso_dimensiones(problema_dimensiones(analizar(texto_A, MATRIZ, "matriz A")[0],
                                                      analizar(texto_b, VECTOR, "vector b")[0]))

    seccion("2", "Método")
    col3, _ = st.columns(2)
    with col3:
        metodo = st.radio("Método", ["Gauss", "Gauss-Jordan"], horizontal=True, key="dir_metodo",
                          help="Gauss: forma escalonada y sustitución hacia atrás. "
                               "Gauss-Jordan: forma escalonada reducida.")
    if st.button("Resolver", type="primary", key="dir_resolver", disabled=bloqueado):
        st.session_state.pop("dir_resultado", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            resolver = resolver_gauss if metodo == "Gauss" else resolver_gauss_jordan
            try:
                st.session_state["dir_resultado"] = (A, b, resolver(A, b, PIVOTEO_PRIMER_NO_NULO))
            except ErrorMatriz as error:
                st.error(f"❌ {notacion.md(str(error))}")
    # El resultado se guarda en la sesión para que no desaparezca al interactuar.
    if "dir_resultado" in st.session_state:
        mostrar_resultado(*st.session_state["dir_resultado"])


def mostrar_resultado(A, b, r):
    n = r.n_incognitas
    seccion("3", "Resultado")
    with tarjeta_resultado("directos"):
        if r.clasificacion == UNICA:
            st.success("✅ " + notacion.md(r.mensaje))
            estado = [("Solución única", "ok")]
        elif r.clasificacion == INFINITAS:
            st.warning("♾️ " + notacion.md(r.mensaje))
            estado = [("Infinitas soluciones", "aviso"),
                      (f"{len(r.variables_libres)} variable(s) libre(s)", "")]
        else:
            st.error("🚫 " + notacion.md(r.mensaje))
            estado = [("Sistema inconsistente", "error")]
        insignias(estado + [(r.metodo, "info"), ("Resultado exacto", "ok")])
        for aviso in r.advertencias:
            st.warning("⚠️ " + notacion.md(aviso))

        st.caption(clasificacion_de_clase(r))
        if r.clasificacion == UNICA:
            st.latex(r"x = " + latex_vector(r.solucion))
            st.latex(r"\text{Sol} = \left\{\left(" + ", ".join(latex_numero(v) for v in r.solucion)
                     + r"\right)\right\}")
        elif r.clasificacion == INFINITAS:
            terminos = latex_vector(r.solucion_particular)
            for indice, (_, v) in enumerate(zip(r.variables_libres, r.direcciones), start=1):
                terminos += rf" + t_{{{indice}}}\,{latex_vector(v)}"
            st.latex(r"x = " + terminos + r",\quad t_i \in \mathbb{R}")
        c1, c2, c3 = st.columns(3)
        c1.metric("rango(A)", r.rango_A)
        c2.metric("rango([A | b])", r.rango_aumentada)
        c3.metric("det(A)", formatear_numero(r.determinante) if r.determinante is not None
                  else "no aplica (A no es cuadrada)")

    if r.clasificacion == UNICA:
        st.subheader("Solución")
        st.table(tabla_vector(r.solucion))
        if r.sustitucion and r.metodo == "Gauss":
            with st.expander("Sustitución hacia atrás"):
                for linea in r.sustitucion:
                    st.markdown(f"- {notacion.md(linea)}")
        verificar(A, b, r.solucion)
    elif r.clasificacion == INFINITAS:
        st.subheader("Solución general (forma paramétrica)")
        libres = ", ".join(f"$t_{{{i}}} = x_{{{j + 1}}}$" for i, j in enumerate(r.variables_libres, start=1))
        st.caption(f"Parámetros: {libres}. Con todos los parámetros en 0 se obtiene una "
                   f"solución particular.")
        verificar(A, b, r.solucion_particular)
    else:
        st.info("💡 Recomendación: revise los datos; si el modelo es correcto, el sistema no tiene "
                "solución. Para obtener la mejor aproximación de un sistema con más ecuaciones que "
                "incógnitas, use el Módulo III (mínimos cuadrados).")

    with st.expander("Procedimiento paso a paso", expanded=True):
        mostrar_pasos(r.pasos, separador=n)
        st.markdown("**Matriz final** "
                    + ("(forma escalonada reducida)" if r.metodo == "Gauss-Jordan" else "(forma escalonada)"))
        st.latex(latex_matriz(r.matriz_final, separador=n))

    if n in (2, 3) and len(A) <= 6:
        with st.expander("Interpretación geométrica", expanded=False):
            marca_incentivo("Experiencia de usuario", "0,5 %")
            grafica, texto = st.columns([5, 2])
            with grafica:
                if n == 2:
                    mostrar_interactiva(rectas_2d(A, b, r), "rectas", mostrar_ayuda=False)
                else:
                    figura = planos_3d(A, b, r)
                    camara = control_gestual.camara_para_figura()
                    if camara is not None:
                        figura.update_layout(scene_camera=camara)
                    mostrar_interactiva(figura, "planos", tres_d=True, mostrar_ayuda=False)
            texto.caption("🖱️ " + (CONTROLES_2D if n == 2 else CONTROLES_3D))
            texto.caption("Cada ecuación es una recta (2 incógnitas) o un plano (3 incógnitas). "
                       "Solución única: se cortan en un punto; infinitas: comparten una recta "
                       "o un plano; inconsistente: no hay punto común a todos.")
            if n == 3:
                control_gestual.panel("graf_planos")


def clasificacion_de_clase(r):
    """La misma clasificación con las palabras de los manuscritos (S6-16/09 p. 29):
    ecuaciones no nulas de la forma escalonada frente al número de incógnitas."""
    if r.clasificacion == UNICA:
        return (f"Como en clase: {r.rango_A} ecuaciones no nulas, {r.n_incognitas} incógnitas "
                f"→ solución única.")
    if r.clasificacion == INFINITAS:
        return (f"Como en clase: {r.rango_A} ecuaciones no nulas < {r.n_incognitas} incógnitas "
                f"→ infinitas soluciones.")
    return "Como en clase: aparece una ecuación 0 = c con c ≠ 0 → el sistema no tiene solución."


def verificar(A, b, x):
    r = residuo(A, x, b)
    exacto = all(v == 0 for v in r)
    st.caption("Verificación: $b - Ax$ = " + "(" + ", ".join(formatear_numero(v) for v in r) + ")"
               + (" → la solución satisface exactamente el sistema." if exacto else ""))
