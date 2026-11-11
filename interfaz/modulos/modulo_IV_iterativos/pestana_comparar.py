"""Interfaz del Módulo IV — pestaña «Comparar métodos».

Jacobi, Gauss-Seidel y SOR con la misma configuración, error final y gráfica comparativa.
"""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, formatear_numero, leer_omega
from algebra.modulo_IV_iterativos.comparacion import comparar_metodos, configuraciones_homogeneas
from algebra.modulo_IV_iterativos.ejecucion import (
    ConfiguracionIterativa,
    ENTRADA_INVALIDA,
    ejecutar,
)
from algebra.modulo_IV_iterativos.espectral import radio_espectral
from algebra.modulo_IV_iterativos.metodos import SOR
from interfaz.compartido.componentes import iteracion_elegida, mostrar_interactiva
from interfaz.compartido.estilo import marca_incentivo
from visualizacion import interactivas, notacion
from visualizacion.notacion import D_K, E_K, E_K_DEF, R_K


def comparar(leer_todo, bloqueado=False):
    marca_incentivo("Visualización avanzada: gráficas comparativas", "1 %")
    st.markdown("Los tres métodos se ejecutan con **el mismo sistema, vector inicial, criterio, "
                "tolerancia y máximo de iteraciones**; SOR usa además su propio ω.")
    if st.button("Comparar Jacobi, Gauss-Seidel y SOR", type="primary", key="it_comparar",
                 disabled=bloqueado):
        st.session_state.pop("it_comparacion", None)
        datos = leer_todo(True)
        if datos:
            configs = configuraciones_homogeneas(
                criterio=datos["criterio"], tolerancia=datos.get("tolerancia", 1e-3),
                k_max=datos.get("k_max", 50), n_iteraciones=datos.get("n_iteraciones", 5),
                x0=datos["x0"], omega=datos["omega"])
            comparacion = comparar_metodos(datos["A"], datos["b"], configs)
            radios = []
            for c in configs:
                try:
                    radios.append(radio_espectral(datos["A"], datos["b"], c.metodo, c.omega))
                except (ErrorEntrada, ErrorMatriz):
                    radios.append(None)
            st.session_state["it_comparacion"] = (comparacion, radios)
    if "it_comparacion" not in st.session_state:
        return
    comp, radios = st.session_state["it_comparacion"]
    if comp.resultados[0].codigo == ENTRADA_INVALIDA:
        st.error("❌ " + notacion.md(comp.resultados[0].mensaje))
        return
    if comp.homogeneo:
        st.success("✅ Experimento homogéneo: mismas condiciones para los tres métodos.")
    else:
        st.warning("⚠️ Experimento no homogéneo: difiere(n) " + ", ".join(comp.diferencias))
    st.info("⚙️ " + comp.resultados[0].configuracion.resumen().split(" · ", 1)[1])
    filas = []
    for r, e, rho in zip(comp.resultados, comp.errores_finales, radios):
        filas.append({
            "Método": r.configuracion.metodo + (f" (ω = {formatear_numero(float(r.configuracion.omega))})"
                                                if r.configuracion.metodo == SOR else ""),
            "Iteraciones": r.k_final if r.k_final is not None else "—",
            "Motivo de parada": notacion.motivo(r.codigo),
            "¿Criterio cumplido?": {True: "Sí", False: "No", None: "No aplica"}[r.criterio_cumplido],
            f"{D_K.texto} final": "—" if r.d_final is None else formatear_numero(r.d_final, 6),
            f"{R_K.texto} final": "—" if r.r_final is None else formatear_numero(r.r_final, 6),
            f"Error final {E_K_DEF.texto}": "no disponible" if e is None else formatear_numero(e, 6),
            "ρ(T)": "—" if rho is None or rho.rho is None else formatear_numero(rho.rho, 6),
        })
    st.dataframe(filas, hide_index=True, width="stretch")
    st.caption("ℹ️ " + comp.nota)
    if comp.referencia is not None:
        st.caption("$x^*$ = solución del método directo (Gauss exacto): (" +
                   ", ".join(formatear_numero(v, 10) for v in comp.referencia) + "). "
                   f"El error final {E_K.md()} es el error respecto a esa solución, como en la tabla "
                   r"comparativa de la lámina S9-05/10 p. 17 ($\|x^{(k)} - x\|_\infty$); "
                   f"no es {D_K.md()} ni {R_K.md()}.")
    else:
        st.caption("No hay solución de referencia (el sistema no tiene solución única): "
                   f"{E_K.md()} final no está disponible.")
    for r in comp.resultados:
        if r.codigo not in ("TOLERANCIA_CAMBIO", "TOLERANCIA_RESIDUO", "N_COMPLETADAS"):
            st.warning(f"{r.configuracion.metodo}: {notacion.md(r.mensaje)}")
    # e_k primero: es el «error final ‖x⁽ᵏ⁾ − x‖∞» de la lámina S9-05/10 p. 17 (diapositiva 13).
    # Opciones de st.radio: renderizan LaTeX.
    opciones = {"e": f"Error respecto a la solución del método directo {E_K.md()}",
                "d": f"Cambio entre iteraciones {D_K.md()}", "r": f"Residuo {R_K.md()}"}
    metrica = st.radio("Métrica a graficar", list(opciones), format_func=opciones.get,
                       horizontal=True, key="it_metrica")
    if metrica == "e" and comp.referencia is None:
        st.info(f"No hay solución de referencia para graficar {E_K.md()}.")
    else:
        explorar_comparacion(comp, metrica)

    with st.expander("Influencia de ω en SOR (barrido)"):
        texto = st.text_input("Valores de ω a probar", "0.8 1 1.1 1.2 1.5 1.8", key="it_barrido")
        if st.button("Probar valores de ω", key="it_barrido_boton"):
            base = comp.resultados[2].configuracion
            try:
                omegas = [leer_omega(t) for t in texto.split()]
            except ErrorEntrada as error:
                st.error(f"❌ {error}")
                omegas = []
            datos = leer_todo(True) if omegas else None
            if datos:
                filas = []
                for w in omegas:
                    config = ConfiguracionIterativa(
                        metodo=SOR, criterio=base.criterio, x0=datos["x0"],
                        tolerancia=base.tolerancia, k_max=base.k_max,
                        n_iteraciones=base.n_iteraciones, omega=w)
                    r = ejecutar(datos["A"], datos["b"], config)
                    try:
                        rho = radio_espectral(datos["A"], datos["b"], SOR, w).rho
                    except (ErrorEntrada, ErrorMatriz):
                        rho = None
                    # st.table: sus encabezados sí renderizan LaTeX (ρ(T_ω) con subíndice)
                    filas.append({r"$\omega$": formatear_numero(w), "Iteraciones": r.k_final,
                                  "Motivo": notacion.motivo(r.codigo),
                                  f"{R_K.md()} final": "—" if r.r_final is None else formatear_numero(r.r_final, 6),
                                  r"$\rho(T_\omega)$": "—" if rho is None else formatear_numero(rho, 6)})
                st.table(filas)
                st.caption(r"Cuanto menor es $\rho(T_\omega)$, más rápida es la convergencia asintótica. "
                           "Con ω = 1, SOR coincide con Gauss-Seidel.")


def explorar_comparacion(comp, metrica):
    """Comparación explorable: destacar un método y ver los tres en una misma iteración.
    Los valores salen de los historiales del núcleo y de comp.errores_historial."""
    base = comp.resultados[0].configuracion
    metodos = [r.configuracion.metodo for r in comp.resultados if r.historial]
    if not metodos:
        st.info("Ningún método produjo iteraciones que graficar.")
        return
    ks = list(range(0, max(r.k_final for r in comp.resultados if r.historial) + 1))
    firma = (base.criterio, metrica, tuple(r.k_final for r in comp.resultados), tuple(metodos))
    k = iteracion_elegida("comparacion", "it_k_comp", ks, firma) if len(ks) > 1 else ks[-1]
    destacado = st.radio("Destacar método", ["Todos"] + metodos, horizontal=True, key="it_destacar",
                         help="Atenúa los demás métodos para seguir una sola curva.")
    tolerancia = base.tolerancia if base.criterio in ("A", "B") else None
    fig = interactivas.comparacion(comp.resultados, metrica, comp.errores_historial,
                                   destacado=None if destacado == "Todos" else destacado, k_destacada=k,
                                   criterio=base.criterio, tolerancia=tolerancia)
    mostrar_interactiva(fig, "comparacion", seleccion=True)
    if len(ks) > 1:
        st.slider("Iteración a comparar", min_value=ks[0], max_value=ks[-1], key="it_k_comp",
                  help="También puede hacer clic en un punto de la gráfica.")
    filas = []
    for r, errores in zip(comp.resultados, comp.errores_historial or [None] * len(comp.resultados)):
        nombre = r.configuracion.metodo + (f" (ω = {float(r.configuracion.omega):g})"
                                           if r.configuracion.metodo == SOR else "")
        fila = next((f for f in r.historial if f.k == k), None)
        if fila is None:
            filas.append({"Método": nombre, f"Estado en k = {k}": f"ya terminó en k = {r.k_final}",
                          D_K.texto: "—", R_K.texto: "—", E_K.texto: "—"})
            continue
        e = errores[r.historial.index(fila)] if errores else None
        filas.append({"Método": nombre,
                      f"Estado en k = {k}": "última iteración" if fila.k == r.k_final else "iterando",
                      D_K.texto: "—" if fila.d is None else formatear_numero(fila.d, 6),
                      R_K.texto: formatear_numero(fila.r, 6),
                      E_K.texto: "—" if e is None else formatear_numero(e, 6)})
    st.dataframe(filas, hide_index=True, width="stretch")
