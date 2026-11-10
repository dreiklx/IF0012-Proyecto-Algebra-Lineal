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
from interfaz.compartido.componentes import mostrar_interactiva
from interfaz.compartido.estilo import (
    insignias,
    marca_incentivo,
    tarjeta_resultado,
    valor_destacado,
)
from visualizacion import interactivas

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
            st.session_state["it_csr_info"] = a_csr(datos["A"]) if disperso else None
    if "it_resultado" in st.session_state:
        info = st.session_state.get("it_csr_info")
        if info is not None:
            memoria = info.memoria()
            st.info(f"🧩 Formato CSR: nnz = {info.nnz} de {info.n}² = {info.n * info.n} "
                    f"elementos (densidad {info.densidad:.1%}). Números almacenados: "
                    f"{memoria['csr']} (CSR) frente a {memoria['densa']} (denso).")
            explicar_csr(info)
        mostrar_ejecucion(st.session_state["it_resultado"])


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
        st.error("🚫 " + texto)
    elif r.codigo == MAXIMO_ITERACIONES:
        st.warning("⏱️ " + texto)
    elif r.configuracion.criterio == CRITERIO_ITERACIONES:
        st.info("ℹ️ " + texto)
    else:
        st.success("✅ " + texto)


def filas_tabla(r):
    criterio = r.configuracion.criterio
    etiqueta_d = "d_k (criterio de parada)" if criterio == CRITERIO_CAMBIO else "d_k (informativo)"
    etiqueta_r = "r_k (criterio de parada)" if criterio == CRITERIO_RESIDUO else "r_k (informativo)"
    filas = []
    for fila in r.historial:
        datos = {"k": fila.k}
        for i, valor in enumerate(fila.x, start=1):
            datos[f"x{i}"] = formatear_numero(valor, CIFRAS)
        datos[etiqueta_d] = "—" if fila.d is None else formatear_numero(fila.d, CIFRAS)
        datos[etiqueta_r] = formatear_numero(fila.r, CIFRAS)
        filas.append(datos)
    return filas


def csv_historial(r):
    """Tabla de iteraciones con precisión completa, para descargar (reporte exportable)."""
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


def mostrar_ejecucion(r):
    if r.codigo == ENTRADA_INVALIDA:
        st.error("❌ " + r.mensaje)
        return
    st.info("⚙️ " + r.configuracion.resumen())
    with tarjeta_resultado("ejecucion"):
        mostrar_motivo(r)
        tipo = {True: "ok", False: "error", None: "info"}[r.criterio_cumplido]
        insignias([(r.configuracion.metodo, "info"), (r.codigo, tipo),
                   ("Almacenamiento CSR" if r.configuracion.formato == "csr" else "Almacenamiento denso", "")])
        for aviso in r.advertencias:
            st.warning("⚠️ " + aviso)
        if not r.historial:
            if r.codigo == DIAGONAL_CERO:
                st.info("💡 Recomendación: reordene las ecuaciones para que ningún aᵢᵢ sea 0; la "
                        "pestaña «Convergencia» propone un orden si existe uno diagonalmente dominante.")
            return
        valor_destacado("Aproximación final x⁽ᵏ⁾",
                        "(" + ", ".join(formatear_numero(v, 8) for v in r.x_final) + ")",
                        f"tras {r.k_final} iteraciones")
        cumplido = {True: "Sí", False: "No", None: "No aplica"}[r.criterio_cumplido]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Iteraciones realizadas", r.k_final)
        c2.metric("Diferencia final d_k", "—" if r.d_final is None else formatear_numero(r.d_final, 6))
        c3.metric("Residuo final r_k", formatear_numero(r.r_final, 6))
        c4.metric("¿Se cumplió el criterio?", cumplido)
    if r.codigo in (MAXIMO_ITERACIONES, ERROR_NO_FINITO):
        st.info("💡 Recomendación: revise la pestaña «Convergencia» (dominancia diagonal y ρ(T)). "
                "Si ρ(T) < 1 el método converge y basta con más iteraciones; si ρ(T) ≥ 1, cambie de "
                "método, de ω o reordene las ecuaciones.")
    st.caption("d_k mide cuánto cambió la aproximación; r_k mide cuánto falla la ecuación "
               "A x = b. Ninguno de los dos es el error respecto a la solución exacta.")
    st.dataframe(filas_tabla(r), hide_index=True, width="stretch")
    marca_incentivo("Visualización avanzada: reporte exportable", "1 %")
    st.download_button("⬇️ Descargar tabla de iteraciones (CSV)", csv_historial(r),
                       file_name=f"iteraciones_{r.configuracion.metodo}.csv", mime="text/csv",
                       key=f"csv_{r.configuracion.metodo}")
    fig = interactivas.convergencia(r.historial, r.configuracion.criterio,
                               r.configuracion.tolerancia
                               if r.configuracion.criterio != CRITERIO_ITERACIONES else None)
    mostrar_interactiva(fig, "convergencia")
