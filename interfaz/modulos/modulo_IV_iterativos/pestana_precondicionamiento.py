"""Interfaz del Módulo IV — pestaña «Precondicionamiento diagonal» (incentivo).

M = D, sistema equivalente D⁻¹Ax = D⁻¹b y comparación documentada de su efecto.
"""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, formatear_numero
from algebra.modulo_IV_iterativos.ejecucion import ConfiguracionIterativa
from algebra.modulo_IV_iterativos.metodos import METODOS
from algebra.modulo_IV_iterativos.precondicionamiento import analizar_precondicionador
from interfaz.compartido.componentes import latex_matriz, latex_vector, mostrar_interactiva
from interfaz.compartido.estilo import insignias, marca_incentivo, tarjeta_resultado
from visualizacion import interactivas, notacion


def precondicionamiento(leer_todo, bloqueado=False):
    marca_incentivo("Precondicionamiento", "1,5 %")
    st.markdown(
        "Precondicionador diagonal de clase (S9-05/10, diapositivas 16-18): "
        r"$M = D = \mathrm{diag}(a_{11},\dots,a_{nn})$ y sistema equivalente "
        r"$M^{-1}Ax = M^{-1}b$. Se comparan $\kappa_\infty$, los autovalores y las iteraciones del sistema "
        "original y del precondicionado con **la misma** configuración "
        r"(criterio, $\varepsilon$, $k_{\max}$, $x^{(0)}$ y $\omega$).")
    if st.button("Analizar el precondicionador M = D", type="primary", key="it_prec",
                 disabled=bloqueado):
        st.session_state.pop("it_precondicionado", None)
        datos = leer_todo(True)
        if datos:
            config = ConfiguracionIterativa(
                criterio=datos["criterio"], x0=datos["x0"],
                tolerancia=datos.get("tolerancia", 1e-3), k_max=datos.get("k_max", 50),
                n_iteraciones=datos.get("n_iteraciones", 5))
            try:
                st.session_state["it_precondicionado"] = analizar_precondicionador(
                    datos["A"], datos["b"], config, datos["omega"])
            except (ErrorEntrada, ErrorMatriz) as error:
                st.error(f"❌ {notacion.md(str(error))}")
    if "it_precondicionado" not in st.session_state:
        return
    r = st.session_state["it_precondicionado"]
    st.latex(r"M = " + latex_matriz(r.M) + r",\quad B = M^{-1}A = " + latex_matriz(r.B)
             + r",\quad \tilde b = M^{-1}b = " + latex_vector(r.b_tilde))
    clasicos = [f for f in r.comparaciones if f.metodo in METODOS]
    richardson = [f for f in r.comparaciones if f.metodo not in METODOS]
    with tarjeta_resultado("precondicionador"):
        identicas = all(f.T_identicas for f in clasicos)
        chips = [("Jacobi, GS y SOR: T y c idénticas (exacto)" if identicas else
                  "Jacobi, GS y SOR: T cambia", "info" if identicas else "aviso")]
        if r.kappa_A is not None and r.kappa_B is not None:
            chips.append(("κ disminuye" if r.kappa_B < r.kappa_A else
                          ("κ aumenta" if r.kappa_B > r.kappa_A else "κ no cambia"),
                          "ok" if r.kappa_B < r.kappa_A else ("aviso" if r.kappa_B > r.kappa_A else "")))
        for f in richardson:
            chips.append((f"Richardson: {notacion.motivo(f.original.codigo)} → "
                          f"{notacion.motivo(f.precondicionado.codigo).lower()}",
                          "ok" if f.precondicionado.criterio_cumplido else "aviso"))
        insignias(chips)
        c1, c2 = st.columns(2)
        c1.metric(r"$\kappa_\infty(A)$", "singular" if r.kappa_A is None else formatear_numero(r.kappa_A))
        c2.metric(r"$\kappa_\infty(D^{-1}A)$", "singular" if r.kappa_B is None else formatear_numero(r.kappa_B))
    if r.analisis_A is not None:
        st.table([{"Matriz": nombre,
                   "Autovalores": ", ".join(formatear_numero(z.real if z.imag == 0 else z, 6)
                                            for z in a.autovalores),
                   "ρ (máx |λ|)": formatear_numero(a.rho, 6)}
                  for nombre, a in (("A", r.analisis_A), ("B = D⁻¹A", r.analisis_B))])
    filas = []
    for f in r.comparaciones:
        filas.append({
            "Método": f.metodo,
            "Iteraciones (original)": "—" if f.original.k_final is None else f.original.k_final,
            "Motivo (original)": notacion.motivo(f.original.codigo),
            "Iteraciones (precondicionado)":
                "—" if f.precondicionado.k_final is None else f.precondicionado.k_final,
            "Motivo (precondicionado)": notacion.motivo(f.precondicionado.codigo),
            "ρ(T) original": "—" if f.rho_original is None else formatear_numero(f.rho_original, 6),
            "ρ(T) precondicionado":
                "—" if f.rho_precondicionado is None else formatear_numero(f.rho_precondicionado, 6),
            "¿T y c idénticas?": {True: "Sí (exacto)", False: "No", None: "—"}[f.T_identicas],
            "¿Mismas iteraciones?": "Sí" if f.mismas_iteraciones else "No",
        })
    st.dataframe(filas, hide_index=True, width="stretch")
    for texto in r.conclusiones:
        st.info("💡 " + notacion.md(texto))
    st.warning("**Extensión no vista en clase — método de Richardson.** "
               r"La fila «Richardson» ($x^{(k+1)} = x^{(k)} + (b - Ax^{(k)})$, matriz de iteración $I - A$) no es uno de los "
               "métodos del enunciado ni aparece en los PDF del curso: se incluye como herramienta "
               "de demostración, porque es el método estacionario más simple sobre el que M = D sí "
               "tiene efecto. Richardson precondicionado con M = D es exactamente Jacobi. La lámina "
               "de la diapositiva 19 (S9-05/10 p. 23) muestra una mejora para Jacobi que no se puede "
               "reproducir, porque Jacobi, Gauss-Seidel y SOR ya están normalizados por la diagonal.",
               icon="🧪")
    mostrar_interactiva(interactivas.precondicionador(r.comparaciones), "precondicionador")
