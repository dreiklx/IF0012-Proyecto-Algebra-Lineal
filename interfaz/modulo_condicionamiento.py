"""Interfaz del Módulo II — Condicionamiento y sensibilidad."""

import streamlit as st

from algebra.condicion import (
    MATRIZ_SINGULAR,
    PERTURBACION_ABSOLUTA,
    PERTURBACION_PORCENTAJE,
    SENSIBILIDAD_ALTA,
    SENSIBILIDAD_BAJA,
    analizar_perturbacion,
    construir_delta_b,
    numero_condicion_infinito,
)
from algebra.directos import ErrorSistema
from algebra.matriz import ErrorMatriz
from algebra.validacion import ErrorEntrada, formatear_numero, leer_vector
from interfaz import ejemplos
from interfaz.componentes import (
    ayuda_formato,
    latex_matriz,
    latex_numero,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_pasos,
)


def mostrar():
    st.header("Módulo II · Condicionamiento y sensibilidad")
    st.markdown(
        r"Calcula $\kappa_\infty(A)=\|A\|_\infty\,\|A^{-1}\|_\infty$ con la inversa obtenida "
        "por **nuestro** Gauss-Jordan, y compara la solución de $Ax=b$ con la del sistema "
        r"perturbado $A\tilde x=b+\Delta b$.")

    nombre = st.selectbox("Cargar un ejemplo", list(ejemplos.CONDICION), key="cond_ejemplo")
    A_txt, b_txt, db_txt = ejemplos.CONDICION[nombre]
    col1, col2 = st.columns([3, 1])
    with col1:
        texto_A = st.text_area("Matriz A (n × n)", A_txt, height=120, key=f"cond_A_{nombre}")
    with col2:
        texto_b = st.text_area("Vector b", b_txt.replace(" ", "\n"), height=120, key=f"cond_b_{nombre}")
    ayuda_formato()

    st.subheader("Perturbación de b")
    modo = st.radio("Tipo de perturbación",
                    ["Valor absoluto (Δb)", "Porcentaje de cada componente de b"],
                    horizontal=True, key="cond_modo")
    if modo.startswith("Valor"):
        texto_p = st.text_input(
            "Δb: un número (se suma a todas las componentes) o un vector de n números",
            db_txt, key=f"cond_db_{nombre}")
    else:
        texto_p = st.text_input(
            "Porcentaje p (Δbᵢ = p/100 · bᵢ): un número o un vector de n porcentajes",
            "1", key=f"cond_pct_{nombre}")

    if st.button("Calcular", type="primary", key="cond_calcular"):
        st.session_state.pop("cond_resultado", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            try:
                valores = leer_vector(texto_p, "perturbación")
                valor = valores[0] if len(valores) == 1 else valores
                modo_nucleo = PERTURBACION_ABSOLUTA if modo.startswith("Valor") else PERTURBACION_PORCENTAJE
                condicion = numero_condicion_infinito(A)
                perturbacion = None
                if condicion.clasificacion != MATRIZ_SINGULAR:
                    delta_b = construir_delta_b(b, modo_nucleo, valor)
                    perturbacion = analizar_perturbacion(A, b, delta_b)
                st.session_state["cond_resultado"] = (A, condicion, perturbacion)
            except (ErrorEntrada, ErrorMatriz, ErrorSistema) as error:
                st.error(f"❌ {error}")
    if "cond_resultado" in st.session_state:
        mostrar_resultado(*st.session_state["cond_resultado"])


def mostrar_resultado(A, c, p):
    n = len(A)
    if c.clasificacion == MATRIZ_SINGULAR:
        st.error("🚫 " + c.interpretacion)
        with st.expander("Procedimiento de Gauss-Jordan (sin pivote en alguna columna)"):
            mostrar_pasos(c.resultado_inversa.pasos, separador=n)
        return

    st.subheader("Número de condición")
    c1, c2, c3 = st.columns(3)
    c1.metric("‖A‖∞", formatear_numero(c.norma_A))
    c2.metric("‖A⁻¹‖∞", formatear_numero(c.norma_inversa))
    c3.metric("κ∞(A)", formatear_numero(c.kappa))
    if c.clasificacion == SENSIBILIDAD_BAJA:
        st.success("🟢 " + c.interpretacion)
    elif c.clasificacion == SENSIBILIDAD_ALTA:
        st.error("🔴 " + c.interpretacion)
    else:
        st.warning("🟠 " + c.interpretacion)
    st.latex(r"A^{-1} = " + latex_matriz(c.inversa))
    st.caption("Verificación: A·A⁻¹ = I se comprobó de forma exacta."
               if c.resultado_inversa.verificacion_identidad else "⚠️ A·A⁻¹ ≠ I")
    with st.expander("Cálculo de la inversa por Gauss-Jordan: [A | I] → [I | A⁻¹]"):
        mostrar_pasos(c.resultado_inversa.pasos, separador=n)

    if p is None:
        return
    st.subheader("Análisis de la perturbación")
    filas = []
    for i in range(n):
        filas.append({
            "i": i + 1,
            "bᵢ": formatear_numero(p.b[i]), "b̃ᵢ = bᵢ + Δbᵢ": formatear_numero(p.b_perturbado[i]),
            "xᵢ (original)": formatear_numero(p.x[i]),
            "x̃ᵢ (perturbada)": formatear_numero(p.x_perturbada[i]),
            "Δxᵢ = x̃ᵢ − xᵢ": formatear_numero(p.delta_x[i]),
        })
    st.table(filas)
    d1, d2, d3 = st.columns(3)
    d1.metric("‖Δb‖∞ / ‖b‖∞", formatear_numero(p.error_relativo_b) if p.error_relativo_b is not None else "no definido")
    d2.metric("‖Δx‖∞ / ‖x‖∞", formatear_numero(p.error_relativo_x) if p.error_relativo_x is not None else "no definido")
    d3.metric("Cota κ∞·‖Δb‖/‖b‖", formatear_numero(p.cota) if p.cota is not None else "no definida")
    for aviso in p.avisos:
        st.warning("⚠️ " + aviso)
    st.latex(r"\frac{\|\Delta x\|_\infty}{\|x\|_\infty} \le \kappa_\infty(A)\,"
             r"\frac{\|\Delta b\|_\infty}{\|b\|_\infty}")
    st.info("💡 " + p.interpretacion)
    if p.error_relativo_x is not None and p.error_relativo_b:
        st.caption(f"Valores exactos: ‖Δb‖/‖b‖ = {formatear_numero(p.error_relativo_b)}, "
                   f"‖Δx‖/‖x‖ = {formatear_numero(p.error_relativo_x)}.")
    st.markdown(rf"$x = ({', '.join(latex_numero(v) for v in p.x)})$, "
                rf"$\tilde x = ({', '.join(latex_numero(v) for v in p.x_perturbada)})$")
