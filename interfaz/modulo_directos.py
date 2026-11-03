"""Interfaz del Módulo I — Sistemas lineales y métodos directos."""

import streamlit as st

from algebra.directos import (
    INCONSISTENTE,
    INFINITAS,
    PIVOTEO_PARCIAL,
    PIVOTEO_PRIMER_NO_NULO,
    UNICA,
    resolver_gauss,
    resolver_gauss_jordan,
)
from algebra.matriz import ErrorMatriz, residuo
from algebra.validacion import formatear_numero
from interfaz import ejemplos
from interfaz.componentes import (
    ayuda_formato,
    latex_matriz,
    latex_vector,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_pasos,
    tabla_vector,
)
from interfaz.estilo import encabezado_modulo, insignias, marca_incentivo, seccion, tarjeta_resultado
from visualizacion.geometria_3d import grafica_planos, grafica_rectas
from visualizacion.graficos import cerrar


def mostrar():
    encabezado_modulo(
        "I", "Sistemas lineales y métodos directos",
        "Resuelve <b>A x = b</b> con eliminación de Gauss o Gauss-Jordan (implementadas desde cero, "
        "con aritmética de fracciones exactas), muestra cada operación elemental y clasifica el "
        "sistema según los rangos de A y de [A | b].",
        [("Gauss", "info"), ("Gauss-Jordan", "info"), ("Fracciones exactas", "ok"),
         ("Paso a paso", "")])

    seccion("1", "Datos del sistema", "Cargue un ejemplo del curso o escriba A y b")
    nombre = st.selectbox("Cargar un ejemplo", list(ejemplos.DIRECTOS), key="dir_ejemplo")
    A_txt, b_txt = ejemplos.DIRECTOS[nombre]
    col1, col2 = st.columns([3, 1])
    with col1:
        texto_A = st.text_area("Matriz A (m × n)", A_txt, height=140, key=f"dir_A_{nombre}",
                               help="Una fila por línea. Ejemplo: «2 1 -1» en la primera línea.")
    with col2:
        texto_b = st.text_area("Vector b (m)", b_txt.replace(" ", "\n"), height=140, key=f"dir_b_{nombre}",
                               help="Un número por línea (o separados por espacios).")
    ayuda_formato()

    seccion("2", "Método")
    col3, col4 = st.columns(2)
    with col3:
        metodo = st.radio("Método", ["Gauss", "Gauss-Jordan"], horizontal=True, key="dir_metodo",
                          help="Gauss: forma escalonada y sustitución hacia atrás. "
                               "Gauss-Jordan: forma escalonada reducida.")
    with col4:
        pivoteo = st.radio(
            "Elección del pivote",
            ["Primer elemento no nulo (como en clase)", "Pivoteo parcial (mayor |elemento|)"],
            key="dir_pivoteo",
            help="Con aritmética exacta ambos dan la misma solución; el pivoteo parcial "
                 "es la estrategia recomendada cuando se trabaja en punto flotante.")

    if st.button("Resolver", type="primary", key="dir_resolver"):
        st.session_state.pop("dir_resultado", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            estrategia = PIVOTEO_PARCIAL if pivoteo.startswith("Pivoteo") else PIVOTEO_PRIMER_NO_NULO
            resolver = resolver_gauss if metodo == "Gauss" else resolver_gauss_jordan
            try:
                st.session_state["dir_resultado"] = (A, b, resolver(A, b, estrategia))
            except ErrorMatriz as error:
                st.error(f"❌ {error}")
    # El resultado se guarda en la sesión para que no desaparezca al interactuar.
    if "dir_resultado" in st.session_state:
        mostrar_resultado(*st.session_state["dir_resultado"])


def mostrar_resultado(A, b, r):
    n = r.n_incognitas
    seccion("3", "Resultado")
    with tarjeta_resultado("directos"):
        if r.clasificacion == UNICA:
            st.success("✅ " + r.mensaje)
            estado = [("Solución única", "ok")]
        elif r.clasificacion == INFINITAS:
            st.warning("♾️ " + r.mensaje)
            estado = [("Infinitas soluciones", "aviso"),
                      (f"{len(r.variables_libres)} variable(s) libre(s)", "")]
        else:
            st.error("🚫 " + r.mensaje)
            estado = [("Sistema inconsistente", "error")]
        insignias(estado + [(r.metodo, "info"), ("Resultado exacto", "ok")])
        for aviso in r.advertencias:
            st.warning("⚠️ " + aviso)

        if r.clasificacion == UNICA:
            st.latex(r"x = " + latex_vector(r.solucion))
        elif r.clasificacion == INFINITAS:
            terminos = latex_vector(r.solucion_particular)
            for indice, (libre, v) in enumerate(zip(r.variables_libres, r.direcciones), start=1):
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
                    st.markdown(f"- {linea}")
        verificar(A, b, r.solucion)
    elif r.clasificacion == INFINITAS:
        st.subheader("Solución general (forma paramétrica)")
        libres = ", ".join(f"t{i} = x{j + 1}" for i, j in enumerate(r.variables_libres, start=1))
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
            grafica, texto = st.columns([3, 2])
            with grafica:
                fig = grafica_rectas(A, b, r) if n == 2 else grafica_planos(A, b, r)
                st.pyplot(fig)
                cerrar(fig)
            texto.caption("Cada ecuación es una recta (2 incógnitas) o un plano (3 incógnitas). "
                       "Solución única: se cortan en un punto; infinitas: comparten una recta "
                       "o un plano; inconsistente: no hay punto común a todos.")


def verificar(A, b, x):
    r = residuo(A, x, b)
    exacto = all(v == 0 for v in r)
    st.caption("Verificación: b − A x = " + "(" + ", ".join(formatear_numero(v) for v in r) + ")"
               + (" → la solución satisface exactamente el sistema." if exacto else ""))
