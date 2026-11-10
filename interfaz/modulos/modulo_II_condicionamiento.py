"""Interfaz del Módulo II — Condicionamiento y sensibilidad."""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, formatear_numero, leer_vector
from algebra.modulo_II_condicionamiento.condicion import (
    MATRIZ_SINGULAR,
    PERTURBACION_ABSOLUTA,
    PERTURBACION_PORCENTAJE,
    SENSIBILIDAD_ALTA,
    SENSIBILIDAD_BAJA,
    analizar_perturbacion,
    construir_delta_b,
    numero_condicion_infinito,
)
from algebra.modulo_I_sistemas.directos import ErrorSistema
from interfaz.compartido import ejemplos
from interfaz.compartido.componentes import (
    latex_matriz,
    latex_numero,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_pasos,
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
    escala_kappa,
    insignias,
    procedencia,
    seccion,
    tarjeta_resultado,
    valor_destacado,
)

ETIQUETA_SENSIBILIDAD = {SENSIBILIDAD_BAJA: ("Sensibilidad baja", "ok"),
                         SENSIBILIDAD_ALTA: ("Sensibilidad alta", "error")}


def mostrar():
    encabezado_modulo(
        "II", "Condicionamiento y sensibilidad",
        r"Calcula κ∞(A) = ‖A‖∞ · ‖A⁻¹‖∞ con la inversa obtenida por <b>nuestro</b> Gauss-Jordan "
        "y compara la solución de A x = b con la del sistema perturbado A x̃ = b + Δb.",
        [("Inversa propia [A | I] → [I | A⁻¹]", "info"), ("Norma ∞", ""), ("Escala 10 / 100", "")])
    procedencia([
        ("A", "κ(A) = ‖A‖ ‖A⁻¹‖ y sus 5 pasos", "S7-21/09 pp. 17 y 19"),
        ("A", "Inversa por Gauss-Jordan", "S3-24/08 pp. 6-8"),
        ("A", "Cota ‖Δx‖/‖x‖ ≤ κ ‖Δb‖/‖b‖", "S7-21/09 p. 18"),
        ("B", "Norma ∞ y escala 10 / 100", "OFICIAL p. 2; la lámina usa 5 niveles"),
        ("B", "Perturbación absoluta o porcentual", "OFICIAL p. 2"),
    ])

    seccion("1", "Matriz y vector", "A debe ser cuadrada (n × n) y b tener n componentes")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.CONDICION), key="cond_ejemplo")
    A_txt, b_txt, db_txt = ejemplos.CONDICION[nombre]
    boton.button("⟲ Cargar ejemplo", key="cond_cargar", width="stretch", on_click=restaurar,
                 args=(f"cond_A_{nombre}", f"cond_b_{nombre}"))
    col1, col2 = st.columns([3, 1.1])
    with col1:
        texto_A = editor(f"cond_A_{nombre}", "Matriz A (n × n)", A_txt, MATRIZ, nombre="matriz A",
                         css="cond_A", ayuda="Una fila por línea. A debe ser cuadrada e invertible para calcular κ.")
    with col2:
        texto_b = editor(f"cond_b_{nombre}", "Vector b", b_txt.replace(" ", "\n"), VECTOR,
                         nombre="vector b", css="cond_b", encabezados=["b"], etiqueta_fila="")
    bloqueado = aviso_dimensiones(problema_dimensiones(analizar(texto_A, MATRIZ, "matriz A")[0],
                                                      analizar(texto_b, VECTOR, "vector b")[0],
                                                      cuadrada=True))

    seccion("2", "Perturbación de b")
    modo = st.radio("Tipo de perturbación",
                    ["Valor absoluto (Δb)", "Porcentaje de cada componente de b"],
                    horizontal=True, key="cond_modo",
                    help="Absoluta: se suma Δb a b. Porcentual: Δbᵢ = p/100 · bᵢ en cada componente.")
    if modo.startswith("Valor"):
        texto_p = st.text_input(
            "Δb: un número (se suma a todas las componentes) o un vector de n números",
            db_txt, key=f"cond_db_{nombre}")
    else:
        texto_p = st.text_input(
            "Porcentaje p (Δbᵢ = p/100 · bᵢ): un número o un vector de n porcentajes",
            "1", key=f"cond_pct_{nombre}")

    if st.button("Calcular", type="primary", key="cond_calcular", disabled=bloqueado):
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
    seccion("3", "Número de condición")
    if c.clasificacion == MATRIZ_SINGULAR:
        with tarjeta_resultado("condicion"):
            insignias([("Matriz singular", "error"), ("κ no está definido", "error")])
            st.error("🚫 " + c.interpretacion)
            st.info("💡 Recomendación: una matriz singular no tiene inversa. Revise si alguna fila "
                    "es combinación de otras; el Módulo I muestra el rango y la clasificación del sistema.")
        with st.expander("Procedimiento de Gauss-Jordan (sin pivote en alguna columna)"):
            mostrar_pasos(c.resultado_inversa.pasos, separador=n)
        return

    with tarjeta_resultado("condicion"):
        izquierda, derecha = st.columns([2, 3])
        with izquierda:
            valor_destacado("κ∞(A)", formatear_numero(c.kappa),
                            f"≈ {float(c.kappa):.6g}" if formatear_numero(c.kappa) != f"{float(c.kappa):.6g}" else "")
            etiqueta = ETIQUETA_SENSIBILIDAD.get(c.clasificacion, ("Sensibilidad moderada", "aviso"))
            insignias([etiqueta, ("A·A⁻¹ = I verificado" if c.resultado_inversa.verificacion_identidad
                                  else "A·A⁻¹ ≠ I", "ok" if c.resultado_inversa.verificacion_identidad else "error")])
        with derecha:
            escala_kappa(c.kappa)
            c1, c2 = st.columns(2)
            c1.metric("‖A‖∞", formatear_numero(c.norma_A))
            c2.metric("‖A⁻¹‖∞", formatear_numero(c.norma_inversa))
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
    seccion("4", "Análisis de la perturbación")
    with tarjeta_resultado("perturbacion"):
        d1, d2, d3 = st.columns(3)
        d1.metric("‖Δb‖∞ / ‖b‖∞", formatear_numero(p.error_relativo_b) if p.error_relativo_b is not None else "no definido")
        d2.metric("‖Δx‖∞ / ‖x‖∞", formatear_numero(p.error_relativo_x) if p.error_relativo_x is not None else "no definido")
        d3.metric("Cota κ∞·‖Δb‖/‖b‖", formatear_numero(p.cota) if p.cota is not None else "no definida")
        if p.cumple_cota is not None:
            insignias([("La cota teórica se cumple", "ok") if p.cumple_cota else ("La cota NO se cumple", "error")]
                      + ([(f"Amplificación observada: {formatear_numero(p.amplificacion)}", "info")]
                         if p.amplificacion is not None else []))
        st.latex(r"\frac{\|\Delta x\|_\infty}{\|x\|_\infty} \le \kappa_\infty(A)\,"
                 r"\frac{\|\Delta b\|_\infty}{\|b\|_\infty}")
        st.info("💡 " + p.interpretacion)
    for aviso in p.avisos:
        st.warning("⚠️ " + aviso)
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
    if p.error_relativo_x is not None and p.error_relativo_b:
        st.caption(f"Valores exactos: ‖Δb‖/‖b‖ = {formatear_numero(p.error_relativo_b)}, "
                   f"‖Δx‖/‖x‖ = {formatear_numero(p.error_relativo_x)}.")
    st.markdown(rf"$x = ({', '.join(latex_numero(v) for v in p.x)})$, "
                rf"$\tilde x = ({', '.join(latex_numero(v) for v in p.x_perturbada)})$")
