"""Interfaz del Módulo III — Mínimos cuadrados y ajuste lineal."""

import streamlit as st

from algebra.matriz import ErrorMatriz
from algebra.minimos import SOBREDETERMINADO, ErrorAjuste, ajuste_lineal, minimos_cuadrados
from algebra.validacion import formatear_numero
from interfaz import ejemplos
from interfaz.componentes import (
    ayuda_formato,
    latex_matriz,
    latex_vector,
    leer_matriz_ui,
    leer_vector_ui,
    tabla_vector,
)
from visualizacion.graficos import cerrar, grafica_ajuste


def mostrar():
    st.header("Módulo III · Mínimos cuadrados y ajuste lineal")
    st.markdown(
        r"Para un sistema sobredeterminado se resuelven las **ecuaciones normales** "
        r"$A^TA\,\hat x = A^Tb$ con nuestro método de Gauss y se calcula el residuo "
        r"$r=b-A\hat x$ con su norma $\|r\|_2$.")
    pestana_sistema, pestana_ajuste = st.tabs(["Sistema sobredeterminado", "Ajuste lineal de datos"])
    with pestana_sistema:
        sistema()
    with pestana_ajuste:
        ajuste()


def sistema():
    nombre = st.selectbox("Cargar un ejemplo", list(ejemplos.MINIMOS), key="mc_ejemplo")
    A_txt, b_txt = ejemplos.MINIMOS[nombre]
    col1, col2 = st.columns([3, 1])
    with col1:
        texto_A = st.text_area("Matriz A (m × n)", A_txt, height=120, key=f"mc_A_{nombre}")
    with col2:
        texto_b = st.text_area("Vector b (m)", b_txt.replace(" ", "\n"), height=120, key=f"mc_b_{nombre}")
    ayuda_formato()
    if st.button("Resolver por mínimos cuadrados", type="primary", key="mc_resolver"):
        st.session_state.pop("mc_resultado", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            try:
                st.session_state["mc_resultado"] = minimos_cuadrados(A, b)
            except ErrorMatriz as error:
                st.error(f"❌ {error}")
    if "mc_resultado" in st.session_state:
        mostrar_minimos(st.session_state["mc_resultado"])


def mostrar_minimos(r, nombres=None):
    if r.tipo == SOBREDETERMINADO:
        st.info("🔎 " + r.mensaje_tipo)
    else:
        st.warning("🔎 " + r.mensaje_tipo)
    st.markdown("**Ecuaciones normales** AᵀA x̂ = Aᵀb:")
    st.latex(r"A^TA = " + latex_matriz(r.AtA) + r",\qquad A^Tb = " + latex_vector(r.Atb))
    if r.solucion is None:
        for aviso in r.advertencias:
            st.error("🚫 " + aviso)
        return
    st.success("✅ " + r.mensaje)
    st.latex(r"\hat x = " + latex_vector(r.solucion))
    if nombres is None:
        st.table(tabla_vector(r.solucion, nombre="x̂"))
    else:
        st.table([{"Coeficiente": nombres[i], "Valor": formatear_numero(v),
                   "Decimal": f"{float(v):.10g}"} for i, v in enumerate(r.solucion)])
    filas = []
    for i in range(len(r.residuo)):
        b_i = r.estimados[i] + r.residuo[i]   # b = A x̂ + r (exacto)
        filas.append({"i": i + 1, "bᵢ": formatear_numero(b_i),
                      "(A x̂)ᵢ": formatear_numero(r.estimados[i]),
                      "rᵢ = bᵢ − (A x̂)ᵢ": formatear_numero(r.residuo[i])})
    st.table(filas)
    c1, c2, c3 = st.columns(3)
    c1.metric("‖r‖₂", f"{r.norma_residuo_2:.8g}")
    c2.metric("‖r‖₂² (exacto)", formatear_numero(r.norma_residuo_2_cuadrado))
    c3.metric("‖r‖∞", formatear_numero(r.norma_residuo_inf))
    st.caption("Comprobación: Aᵀr = (" + ", ".join(formatear_numero(v) for v in r.ortogonalidad)
               + ") — el residuo es ortogonal a las columnas de A, propiedad que caracteriza "
                 "a la solución de mínimos cuadrados.")
    with st.expander("Verificación con el procedimiento de clase (S8-30/09 pp. 6-7)"):
        if r.det_aumentada is not None:
            st.markdown(
                f"1. det([A | b]) = **{formatear_numero(r.det_aumentada)}** "
                + ("≠ 0: b no es combinación lineal de las columnas de A (no hay solución exacta)."
                   if r.det_aumentada != 0 else
                   "= 0: b es combinación lineal de las columnas de A (hay solución exacta)."))
        else:
            st.markdown("1. det([A | b]) solo aplica cuando m = n + 1; la consistencia se "
                        "decidió con el rango (Gauss).")
        st.markdown("2. Ecuaciones normales AᵀA x̂ = Aᵀb (arriba).")
        if r.cramer is not None:
            detalle = ", ".join(f"det(M_{j + 1}) = {formatear_numero(d)}"
                                for j, d in enumerate(r.cramer["dets"]))
            coincide = r.cramer["solucion"] == r.solucion
            st.markdown(
                f"3. Regla de Cramer: det(AᵀA) = {formatear_numero(r.cramer['det'])}, {detalle} → "
                f"x̂ = (" + ", ".join(formatear_numero(v) for v in r.cramer["solucion"]) + ")"
                + (" — **coincide exactamente** con Gauss." if coincide else " — ⚠️ no coincide."))
        else:
            st.markdown("3. Cramer se muestra como verificación para n ≤ 3 incógnitas.")
    st.info("💡 ‖r‖₂ mide la distancia entre b y el vector A x̂ más cercano del espacio "
            "columna de A: cuanto menor, mejor se aproximan los datos. ‖r‖₂ = 0 solo si el "
            "sistema tiene solución exacta.")


def ajuste():
    nombre = st.selectbox("Cargar un ejemplo", list(ejemplos.AJUSTE), key="aj_ejemplo")
    x_txt, y_txt = ejemplos.AJUSTE[nombre]
    col1, col2 = st.columns(2)
    with col1:
        texto_x = st.text_area("Valores de x", x_txt.replace(" ", "\n"), height=140, key=f"aj_x_{nombre}")
    with col2:
        texto_y = st.text_area("Valores de y", y_txt.replace(" ", "\n"), height=140, key=f"aj_y_{nombre}")
    st.caption("Un valor por línea (o separados por espacios). El punto i es (xᵢ, yᵢ).")
    if st.button("Calcular recta de ajuste", type="primary", key="aj_calcular"):
        st.session_state.pop("aj_resultado", None)
        xs = leer_vector_ui(texto_x, "vector x")
        ys = leer_vector_ui(texto_y, "vector y")
        if xs is not None and ys is not None:
            try:
                st.session_state["aj_resultado"] = ajuste_lineal(xs, ys)
            except ErrorAjuste as error:
                st.error(f"❌ {error}")
    if "aj_resultado" not in st.session_state:
        return
    r = st.session_state["aj_resultado"]
    st.success(f"✅ Recta de mejor ajuste: **{r.ecuacion}**  "
               f"(m ≈ {float(r.pendiente):.8g}, c ≈ {float(r.intercepto):.8g})")
    st.latex(r"A=\begin{bmatrix} x_1 & 1\\ \vdots & \vdots\\ x_k & 1\end{bmatrix},\quad "
             r"b=\begin{bmatrix} y_1\\ \vdots\\ y_k\end{bmatrix},\quad "
             r"A^TA\begin{bmatrix} m\\ c\end{bmatrix}=A^Tb")
    fig = grafica_ajuste(r.xs, r.ys, r.pendiente, r.intercepto, r.minimos.estimados)
    st.pyplot(fig)
    cerrar(fig)
    mostrar_minimos(r.minimos, nombres=["m (pendiente)", "c (intercepto)"])
