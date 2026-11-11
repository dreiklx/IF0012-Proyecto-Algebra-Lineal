"""Interfaz del Módulo IV — pestaña «Ejecutar un método».

Tabla de iteraciones, motivo de terminación, reporte CSV y gráfica de convergencia.
"""

import csv
import io

import streamlit as st

from algebra.compartido.validacion import formatear_numero
from algebra.modulo_IV_iterativos.dispersas import a_csr
from algebra.modulo_IV_iterativos.ejecucion import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    CRITERIO_RESIDUO,
    ConfiguracionIterativa,
    DIAGONAL_CERO,
    ENTRADA_INVALIDA,
    ERROR_INTERNO,
    ERROR_NO_FINITO,
    MAXIMO_ITERACIONES,
    ejecutar,
)
from algebra.modulo_IV_iterativos.metodos import METODOS, SOR
from interfaz.compartido.componentes import (
    iteracion_elegida,
    iteraciones_seleccionadas,
    latex_despejes,
    mostrar_interactiva,
)
from interfaz.compartido.estilo import (
    insignias,
    marca_incentivo,
    tarjeta_resultado,
    valor_destacado,
)
from visualizacion import interactivas, notacion
from visualizacion.notacion import D_K, D_K_DEF, R_K, R_K_DEF

CIFRAS = 8


def ejecutar_un_metodo(leer_todo, criterio, bloqueado=False):
    """Pestaña «Ejecutar un método»: un método con la configuración común."""
    metodo = st.selectbox("Método", METODOS, key="it_metodo")
    marca_incentivo("Matrices dispersas", "1 %")
    disperso = st.checkbox(
        "Usar almacenamiento disperso (CSR)", key="it_csr",
        help="Guarda solo los elementos no nulos y cada iteración recorre únicamente "
             "esos elementos (O(nnz) en lugar de O(n²)). Produce exactamente las "
             "mismas iteraciones que el almacenamiento denso.")
    if st.button("Ejecutar", type="primary", key="it_ejecutar", disabled=bloqueado):
        st.session_state.pop("it_resultado", None)
        datos = leer_todo(metodo == SOR)
        if datos:
            config = ConfiguracionIterativa(
                metodo=metodo, criterio=criterio, x0=datos["x0"],
                tolerancia=datos.get("tolerancia", 1e-3), k_max=datos.get("k_max", 50),
                n_iteraciones=datos.get("n_iteraciones", 5), omega=datos["omega"],
                formato="csr" if disperso else "densa")
            st.session_state["it_resultado"] = ejecutar(datos["A"], datos["b"], config)
            st.session_state["it_sistema"] = (datos["A"], datos["b"])
            st.session_state["it_csr_info"] = a_csr(datos["A"]) if disperso else None
    if "it_resultado" in st.session_state:
        info = st.session_state.get("it_csr_info")
        if info is not None:
            memoria = info.memoria()
            st.info(f"🧩 Formato CSR: nnz = {info.nnz} de {info.n}² = {info.n * info.n} "
                    f"elementos (densidad {info.densidad:.1%}). Números almacenados: "
                    f"{memoria['csr']} (CSR) frente a {memoria['densa']} (denso).")
            explicar_csr(info)
        mostrar_ejecucion(st.session_state["it_resultado"], st.session_state.get("it_sistema"))


def explicar_csr(info):
    """Muestra las tres listas del formato CSR y la estrategia (incentivo «Matrices dispersas»)."""
    with st.expander("¿Cómo se guarda la matriz en CSR y por qué es eficiente?"):
        st.markdown(
            "**Estrategia (S9-05/10 pp. 9 y 13).** Solo se guardan los elementos no nulos, fila "
            "por fila, en tres listas. En cada iteración, la fila *i* de Jacobi, Gauss-Seidel o "
            "SOR recorre únicamente las posiciones `inicio[i]` … `inicio[i+1] − 1`, así que el "
            "costo por iteración es O(nnz) en lugar de O(n²). Los ceros nunca se multiplican, y "
            "por eso las iteraciones son idénticas a las del formato denso.")
        st.table({
            "Lista": ["valores (aᵢⱼ no nulos)", "columnas (j de cada valor)",
                      "inicio (dónde empieza cada fila)"],
            "Contenido": [", ".join(formatear_numero(v) for v in info.valores),
                          ", ".join(str(j + 1) for j in info.columnas),
                          ", ".join(str(k) for k in info.inicio)],
            "Tamaño": [info.nnz, info.nnz, info.n + 1]})
        st.caption("Las columnas se muestran numeradas desde 1, como en clase; en el código "
                   "empiezan en 0. Memoria: 2·nnz + n + 1 números frente a n².")


def mostrar_motivo(r):
    texto = r.mensaje
    if r.codigo in (ENTRADA_INVALIDA, DIAGONAL_CERO, ERROR_INTERNO, ERROR_NO_FINITO):
        st.error("🚫 " + notacion.md(texto))
    elif r.codigo == MAXIMO_ITERACIONES:
        st.warning("⏱️ " + notacion.md(texto))
    elif r.configuracion.criterio == CRITERIO_ITERACIONES:
        st.info("ℹ️ " + notacion.md(texto))
    else:
        st.success("✅ " + notacion.md(texto))


def filas_tabla(r):
    """Filas de st.dataframe: sus encabezados no renderizan LaTeX, por eso van en Unicode."""
    criterio = r.configuracion.criterio
    etiqueta_d = D_K.texto + (" (criterio de parada)" if criterio == CRITERIO_CAMBIO else " (informativo)")
    etiqueta_r = R_K.texto + (" (criterio de parada)" if criterio == CRITERIO_RESIDUO else " (informativo)")
    filas = []
    for fila in r.historial:
        datos = {"k": fila.k}
        for i, valor in enumerate(fila.x, start=1):
            datos[f"x{notacion.subindice(i)}"] = formatear_numero(valor, CIFRAS)
        datos[etiqueta_d] = "—" if fila.d is None else formatear_numero(fila.d, CIFRAS)
        datos[etiqueta_r] = formatear_numero(fila.r, CIFRAS)
        filas.append(datos)
    return filas


def csv_historial(r):
    """Tabla de iteraciones con precisión completa, para descargar (reporte exportable).

    Es un archivo de datos: los nombres de columna (x1, d_k, r_k) quedan en ASCII para
    que cualquier hoja de cálculo o programa los lea sin problemas de codificación."""
    salida = io.StringIO()
    escritor = csv.writer(salida)
    n = len(r.historial[0].x)
    escritor.writerow(["# " + r.configuracion.resumen()])
    escritor.writerow(["# Motivo de terminación: " + r.mensaje])
    escritor.writerow(["k"] + [f"x{i}" for i in range(1, n + 1)] + ["d_k", "r_k"])
    for fila in r.historial:
        escritor.writerow([fila.k] + [repr(v) for v in fila.x]
                          + ["" if fila.d is None else repr(fila.d), repr(fila.r)])
    return salida.getvalue()


def mostrar_ejecucion(r, sistema=None):
    if r.codigo == ENTRADA_INVALIDA:
        st.error("❌ " + notacion.md(r.mensaje))
        return
    st.info("⚙️ " + r.configuracion.resumen())
    with tarjeta_resultado("ejecucion"):
        mostrar_motivo(r)
        tipo = {True: "ok", False: "error", None: "info"}[r.criterio_cumplido]
        insignias([(r.configuracion.metodo, "info"), (notacion.motivo(r.codigo), tipo),
                   ("Almacenamiento CSR" if r.configuracion.formato == "csr" else "Almacenamiento denso", "")])
        for aviso in r.advertencias:
            st.warning("⚠️ " + notacion.md(aviso))
        if not r.historial:
            if r.codigo == DIAGONAL_CERO:
                st.info("💡 Recomendación: reordene las ecuaciones para que ningún $a_{ii}$ sea 0; la "
                        "pestaña «Convergencia» propone un orden si existe uno diagonalmente dominante.")
            return
        valor_destacado("Aproximación final x⁽ᵏ⁾",
                        "(" + ", ".join(formatear_numero(v, 8) for v in r.x_final) + ")",
                        f"tras {r.k_final} iteraciones")
        cumplido = {True: "Sí", False: "No", None: "No aplica"}[r.criterio_cumplido]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Iteraciones realizadas", r.k_final)
        c2.metric(f"Diferencia final {D_K.md()}", "—" if r.d_final is None else formatear_numero(r.d_final, 6))
        c3.metric(f"Residuo final {R_K.md()}", formatear_numero(r.r_final, 6))
        c4.metric("¿Se cumplió el criterio?", cumplido)
    if r.codigo in (MAXIMO_ITERACIONES, ERROR_NO_FINITO):
        st.info("💡 Recomendación: revise la pestaña «Convergencia» (dominancia diagonal y ρ(T)). "
                "Si ρ(T) < 1 el método converge y basta con más iteraciones; si ρ(T) ≥ 1, cambie de "
                "método, de ω o reordene las ecuaciones.")
    if sistema is not None and r.historial and len(sistema[0]) <= 6:
        mostrar_despejes(*sistema, r.configuracion)
    st.caption(f"{D_K_DEF.md()} mide cuánto cambió la aproximación; {R_K_DEF.md()} mide cuánto "
               "falla la ecuación $Ax = b$. Ninguno de los dos es el error respecto a la solución exacta.")
    st.dataframe(filas_tabla(r), hide_index=True, width="stretch")
    marca_incentivo("Visualización avanzada: reporte exportable", "1 %")
    st.download_button("⬇️ Descargar tabla de iteraciones (CSV)", csv_historial(r),
                       file_name=f"iteraciones_{r.configuracion.metodo}.csv", mime="text/csv",
                       key=f"csv_{r.configuracion.metodo}")
    explorar_convergencia(r)


def explorar_convergencia(r):
    """Gráfica de convergencia explorable: hitos reales, iteración elegida (clic o
    deslizador) con su detalle y tabla de una zona seleccionada.  Todo sale de r.historial
    y de r.codigo; aquí no se calcula nada nuevo."""
    config = r.configuracion
    ks = [f.k for f in r.historial]
    firma = (config.metodo, config.criterio, r.codigo, len(ks), r.historial[-1].r)
    k = iteracion_elegida("convergencia", "it_k_conv", ks, firma) if len(ks) > 1 else ks[-1]
    tolerancia = config.tolerancia if config.criterio != CRITERIO_ITERACIONES else None
    fig = interactivas.convergencia(r.historial, config.criterio, tolerancia, metodo=config.metodo,
                                    codigo=r.codigo, k_destacada=k)
    mostrar_interactiva(fig, "convergencia", seleccion=True)
    if len(ks) > 1:
        st.slider("Iteración a explorar", min_value=ks[0], max_value=ks[-1], key="it_k_conv",
                  help="También puede hacer clic en un punto de la gráfica.")
    detalle_iteracion(r, r.historial[ks.index(k)], tolerancia)
    elegidas = [kk for kk in iteraciones_seleccionadas("convergencia") if kk in ks]
    if len(elegidas) > 1:
        st.markdown(f"**Zona seleccionada:** iteraciones {elegidas[0]} a {elegidas[-1]}")
        st.dataframe([fila for fila in filas_tabla(r) if fila["k"] in elegidas],
                     hide_index=True, width="stretch")


def detalle_iteracion(r, fila, tolerancia):
    """Panel con los valores de una iteración (los mismos de la tabla)."""
    config = r.configuracion
    with st.container(border=True, key="it_detalle_k"):
        c1, c2, c3, c4 = st.columns([1.2, 0.8, 1.4, 1.4])
        c1.metric("Método", config.metodo + (f" (ω = {config.omega:g})" if config.metodo == SOR else ""))
        c2.metric("Iteración k", fila.k)
        c3.metric(D_K_DEF.md(), "—" if fila.d is None else formatear_numero(fila.d, 6))
        c4.metric(R_K_DEF.md(), formatear_numero(fila.r, 6))
        st.markdown("x⁽ᵏ⁾ = (" + ", ".join(formatear_numero(v, CIFRAS) for v in fila.x) + ")")
        notas = []
        if fila.k == r.historial[0].k:
            notas.append(("Vector inicial x⁽⁰⁾" if fila.k == 0 else "Primera iteración", ""))
        if fila.k == r.k_final:
            texto = interactivas.estado_final(r.codigo, fila.k) or "Última iteración"   # insignias admiten <sub>
            notas.append((texto, "ok" if r.criterio_cumplido else "aviso"))
        if tolerancia is not None:
            valor = fila.d if config.criterio == CRITERIO_CAMBIO else fila.r
            if valor is not None:
                nombre = (D_K if config.criterio == CRITERIO_CAMBIO else R_K).html   # insignia: admite <sub>
                notas.append((f"{nombre} {'<' if valor < tolerancia else '≥'} ε = {tolerancia:g}",
                              "ok" if valor < tolerancia else ""))
        if notas:
            insignias(notas)


def mostrar_despejes(A, b, config):
    """Primer paso de clase: despejar cada incógnita (S8-30/09 pp. 19, 24 y 32)."""
    fuente = {"Jacobi": "S8-30/09 p. 19", "Gauss-Seidel": "S8-30/09 p. 24", "SOR": "S8-30/09 p. 32"}
    with st.expander(f"Despeje de las incógnitas ({config.metodo}, como en {fuente.get(config.metodo, 'clase')})"):
        for linea in latex_despejes(A, b, config.metodo, config.omega):
            st.latex(linea)
        if config.metodo == "Gauss-Seidel":
            st.caption("Los valores con (k+1) ya se calcularon en esta misma iteración.")
        elif config.metodo == "SOR":
            st.caption("Primero se calcula el valor de Gauss-Seidel x^GS y luego se combina con ω, "
                       "componente por componente, como en el manuscrito.")
