"""Interfaz del Módulo IV — pestaña «Convergencia».

Dominancia diagonal, reordenamiento de ecuaciones, matriz de iteración T y ρ(T).
"""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, formatear_numero, leer_omega
from algebra.modulo_IV_iterativos.convergencia import dominancia_diagonal, reordenamiento_dominante
from algebra.modulo_IV_iterativos.espectral import (
    CONVERGE,
    NO_CALCULADO,
    NO_CONVERGE,
    desarrollo_sarrus,
    radio_espectral,
)
from algebra.modulo_IV_iterativos.metodos import GAUSS_SEIDEL, JACOBI, METODOS, SOR
from interfaz.compartido.componentes import (
    latex_matriz,
    latex_polinomio,
    latex_vector,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_interactiva,
)
from interfaz.compartido.estilo import (
    insignias,
    marca_incentivo,
    tarjeta_resultado,
    valor_destacado,
)
from visualizacion import interactivas, notacion


def convergencia(texto_A, texto_b, texto_omega, bloqueado=False):
    metodo = st.selectbox("Método a analizar", METODOS, key="it_conv_metodo")
    if st.button("Analizar convergencia", type="primary", key="it_conv", disabled=bloqueado):
        st.session_state.pop("it_convergencia", None)
        st.session_state.pop("it_reorden", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            # La dominancia y el reordenamiento se muestran aunque T no se pueda
            # construir (por ejemplo, con un a_ii = 0, que es cuando más ayuda reordenar).
            try:
                st.session_state["it_convergencia"] = (dominancia_diagonal(A), None, None)
                st.session_state["it_reorden"] = reordenamiento_dominante(A, b)
                omega = leer_omega(texto_omega) if metodo == SOR else None
                st.session_state["it_convergencia"] = (
                    dominancia_diagonal(A), radio_espectral(A, b, metodo, omega), None)
            except (ErrorEntrada, ErrorMatriz) as error:
                if "it_convergencia" in st.session_state:
                    st.session_state["it_convergencia"] = (
                        st.session_state["it_convergencia"][0], None, str(error))
                else:
                    st.error(f"❌ {notacion.md(str(error))}")
    if "it_convergencia" not in st.session_state:
        return
    dom, esp, error_T = st.session_state["it_convergencia"]

    marca_incentivo("Extensión matemática: radio espectral con autovalores complejos", "1 %")
    st.subheader("1. Dominancia diagonal estricta por filas")
    # Encabezados de st.table: renderizan LaTeX.
    st.table([{"Fila $i$": f[0] + 1, r"$|a_{ii}|$": formatear_numero(f[1]),
               r"$\sum_{j \ne i} |a_{ij}|$": formatear_numero(f[2]),
               r"¿$|a_{ii}| > \sum_{j \ne i} |a_{ij}|$?": "✔" if f[3] else "✘"}
              for f in dom.filas])
    (st.success if dom.estricta else st.warning)(notacion.md(dom.mensaje))
    if not dom.estricta:
        reorden = st.session_state.get("it_reorden")
        if reorden is not None:
            A_r, b_r, orden = reorden
            st.info("🔀 Reordenando las ecuaciones como en clase (Tarea II #2-3), la matriz SÍ es "
                    "estrictamente dominante con el orden " +
                    ", ".join(f"E{notacion.subindice(i + 1)}" for i in orden) + ":")
            st.latex(r"A' = " + latex_matriz(A_r) + r",\quad b' = " + latex_vector(b_r))
            st.caption("La aplicación no reordena por su cuenta: copie A' y b' en los campos "
                       "de entrada si desea usar ese orden.")
        else:
            st.caption("Ningún reordenamiento de las ecuaciones logra dominancia diagonal estricta.")

    if esp is None:
        st.error(f"❌ {notacion.md(error_T)}")
        return
    it = esp.iteracion
    st.subheader(f"2. Matriz de iteración de {it.metodo}")
    formulas = {
        JACOBI: r"T_J=-D^{-1}(L+U),\qquad c=D^{-1}b",
        GAUSS_SEIDEL: r"T_{GS}=-(D+L)^{-1}U,\qquad c=(D+L)^{-1}b",
        SOR: r"T_\omega=(D+\omega L)^{-1}\left[(1-\omega)D-\omega U\right],\qquad c=\omega(D+\omega L)^{-1}b",
    }
    st.latex(formulas[it.metodo])
    if it.metodo == SOR:
        st.caption("Cat. C · La matriz de iteración de SOR no aparece en los PDF del curso (en clase "
                   "SOR se calcula por componentes): es una extensión, necesaria para obtener ρ(T).")
    else:
        st.caption("Cat. A · Como en los manuscritos de clase (S9-07/10 pp. 3-7): A = D + L + U, "
                   "T y c, y ρ(T) = máx |λ| con det(T − λI) = 0.")
    st.latex(r"D=" + latex_matriz(it.D) + r",\; L=" + latex_matriz(it.L) + r",\; U=" + latex_matriz(it.U))
    st.latex(r"T=" + latex_matriz(it.T) + r",\qquad c=" + latex_vector(it.c))

    st.subheader("3. Polinomio característico, autovalores y radio espectral")
    if esp.conclusion == NO_CALCULADO:
        st.warning(notacion.md(esp.mensaje))
        return
    # El mismo polinomio que esp.polinomio_curso, con fracciones apiladas (−4/9λ era ambiguo).
    st.latex(r"\det(T - \lambda I) = " + latex_polinomio(esp.coeficientes) + " = 0")
    if len(it.T) == 3:
        traza, menores, det = desarrollo_sarrus(it.T)
        coincide = [-1, traza, -menores, det] == [-c for c in esp.coeficientes]
        st.caption(
            r"Desarrollo de clase (Sarrus): $\det(T - \lambda I) = -\lambda^3 + \operatorname{tr}(T)\lambda^2 - (\Sigma\ \text{menores } 2\times 2)\lambda + \det(T)$, "
            f"con tr(T) = {formatear_numero(traza)}, Σ menores = {formatear_numero(menores)} y "
            f"det(T) = {formatear_numero(det)} — "
            + ("coincide con el polinomio calculado." if coincide else "⚠️ no coincide."))
    st.caption("Coeficientes calculados de forma exacta con el método de Faddeev-LeVerrier "
               "(Cat. C, extensión no vista en clase; para 3×3 coincide con el desarrollo por Sarrus "
               "visto en clase). Raíces: λ = 0 exactas, fórmula cuadrática o método de Durand-Kerner "
               "(Cat. C, extensión no vista en clase; ver guía matemática).")
    st.table([{"λ": formatear_numero(z, 8), "Parte real": f"{z.real:.8g}",
               "Parte imaginaria": f"{z.imag:.8g}", "|λ|": f"{abs(z):.8g}"}
              for z in esp.autovalores])
    with tarjeta_resultado("espectral"):
        izquierda, derecha = st.columns([2, 3])
        with izquierda:
            valor_destacado(f"ρ(T) de {it.metodo}", formatear_numero(esp.rho, 8), "máx |λ<sub>i</sub>| de T")
        with derecha:
            insignias([{CONVERGE: ("Converge para todo x⁽⁰⁾", "ok"),
                        NO_CONVERGE: ("No converge para todo x⁽⁰⁾", "error")}.get(
                           esp.conclusion, ("Indeterminado", "aviso")),
                       ("Decisión exacta" if esp.decision_exacta else
                        ("Cálculo fiable" if esp.fiable else "Cálculo no fiable"),
                        "ok" if esp.decision_exacta or esp.fiable else "aviso"),
                       ("Dominante" if dom.estricta else "No dominante", "ok" if dom.estricta else "")])
            if esp.conclusion == CONVERGE:
                st.success("✅ " + notacion.md(esp.mensaje))
            elif esp.conclusion == NO_CONVERGE:
                st.error("🚫 " + notacion.md(esp.mensaje))
            else:
                st.warning("⚠️ " + notacion.md(esp.mensaje))
    for aviso in esp.advertencias:
        st.warning("⚠️ " + notacion.md(aviso))
    v = esp.verificaciones
    st.caption(f"Verificación: suma de autovalores = {formatear_numero(v['suma de autovalores'], 8)}, "
               f"traza(T) = {formatear_numero(v['traza de T'], 8)}; "
               f"máx |p(λ)| relativo = {v['max |p(λ)| relativo']:.2e}.")
    grafica, texto = st.columns([3, 2])
    with grafica:
        mostrar_interactiva(interactivas.autovalores(esp.autovalores, esp.rho), "autovalores",
                            mostrar_ayuda=False)
    with texto:
        st.markdown("**Cómo leer el diagrama**")
        st.markdown("- Cada punto es un autovalor λ de T en el plano complejo.\n"
                    "- El círculo verde es |λ| = 1: la frontera de convergencia.\n"
                    "- El círculo discontinuo tiene radio ρ(T) = máx |λ|.\n"
                    "- Si todos los autovalores quedan dentro del círculo verde, el método "
                    "converge para cualquier x⁽⁰⁾; cuanto menor es ρ(T), más rápido.")
    st.info(r"💡 Teorema: $x^{(k+1)} = Tx^{(k)} + c$ converge para todo $x^{(0)}$ si y solo si $\rho(T) < 1$. "
            "La dominancia diagonal es solo una condición suficiente.")
