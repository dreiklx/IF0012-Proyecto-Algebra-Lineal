"""Interfaz del Módulo IV — Métodos iterativos y convergencia."""

import csv
import io

import streamlit as st

from algebra.espectral import CONVERGE, NO_CALCULADO, NO_CONVERGE, radio_espectral
from algebra.iterativos import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    CRITERIO_RESIDUO,
    DIAGONAL_CERO,
    ENTRADA_INVALIDA,
    ERROR_INTERNO,
    ERROR_NO_FINITO,
    GAUSS_SEIDEL,
    JACOBI,
    K_TOPE,
    MAXIMO_ITERACIONES,
    METODOS,
    SOR,
    ConfiguracionIterativa,
    comparar_metodos,
    configuraciones_homogeneas,
    dominancia_diagonal,
    ejecutar,
    vector_diagonal,
)
from algebra.matriz import ErrorMatriz
from algebra.validacion import (
    ErrorEntrada,
    formatear_numero,
    leer_entero_positivo,
    leer_omega,
    leer_tolerancia,
    leer_vector,
)
from interfaz import ejemplos
from interfaz.componentes import ayuda_formato, latex_matriz, latex_vector, leer_matriz_ui, leer_vector_ui
from visualizacion.graficos import cerrar, grafica_autovalores, grafica_comparacion, grafica_convergencia

ETIQUETAS_CRITERIO = {
    CRITERIO_CAMBIO: "A · Cambio entre iteraciones  ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε",
    CRITERIO_RESIDUO: "B · Residuo del sistema  ‖b − Ax⁽ᵏ⁾‖∞ < ε",
    CRITERIO_ITERACIONES: "C · Número fijo de iteraciones N",
}
CIFRAS = 8


def mostrar():
    st.header("Módulo IV · Métodos iterativos y convergencia")
    st.markdown(
        "Jacobi, Gauss-Seidel y SOR implementados desde cero, con criterio de parada, "
        "tolerancia, vector inicial, máximo de iteraciones y factor de relajación "
        "configurables. En cada iteración se registran **d_k** (cambio entre iteraciones) "
        "y **r_k** (residuo del sistema original).")

    nombre = st.selectbox("Cargar un ejemplo", list(ejemplos.ITERATIVOS), key="it_ejemplo")
    A_txt, b_txt = ejemplos.ITERATIVOS[nombre]
    col1, col2 = st.columns([3, 1])
    with col1:
        texto_A = st.text_area("Matriz A (n × n)", A_txt, height=130, key=f"it_A_{nombre}")
    with col2:
        texto_b = st.text_area("Vector b", b_txt.replace(" ", "\n"), height=130, key=f"it_b_{nombre}")
    ayuda_formato()

    st.subheader("Parámetros de ejecución y criterio de parada")
    criterio = st.radio("Criterio de parada", list(ETIQUETAS_CRITERIO),
                        format_func=ETIQUETAS_CRITERIO.get, key="it_criterio")
    c1, c2, c3 = st.columns(3)
    if criterio == CRITERIO_ITERACIONES:
        texto_n = c1.text_input("N (iteraciones a ejecutar)", "5", key="it_N")
        c2.caption("⚠️ Completar N iteraciones **no demuestra** convergencia.")
        texto_eps = texto_kmax = None
    else:
        texto_eps = c1.text_input("Tolerancia ε (> 0)", "1e-3", key="it_eps")
        texto_kmax = c2.text_input(f"Máximo de iteraciones (1 a {K_TOPE})", "50", key="it_kmax")
        texto_n = None
    texto_omega = c3.text_input("ω de SOR (0 < ω < 2)", "1.2", key="it_omega",
                                help="Solo se usa con SOR. El rango 0 < ω < 2 no garantiza "
                                     "por sí solo la convergencia.")
    tipo_x0 = st.radio("Vector inicial x⁽⁰⁾", ["Vector cero", "xᵢ⁽⁰⁾ = bᵢ / aᵢᵢ", "Personalizado"],
                       horizontal=True, key="it_x0_tipo")
    texto_x0 = st.text_input("x⁽⁰⁾ personalizado (n números)", "0 0 0", key="it_x0") \
        if tipo_x0 == "Personalizado" else None

    pestana_uno, pestana_comparar, pestana_conv = st.tabs(
        ["Ejecutar un método", "Comparar métodos", "Convergencia: dominancia y radio espectral"])

    def leer_todo(necesita_omega):
        """Lee A, b y los parámetros; devuelve un diccionario o None si hay errores."""
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is None or b is None:
            return None
        try:
            datos = {"A": A, "b": b, "criterio": criterio}
            if criterio == CRITERIO_ITERACIONES:
                datos["n_iteraciones"] = leer_entero_positivo(texto_n, "número de iteraciones N", K_TOPE)
            else:
                datos["tolerancia"] = leer_tolerancia(texto_eps)
                datos["k_max"] = leer_entero_positivo(texto_kmax, "máximo de iteraciones", K_TOPE)
            datos["omega"] = leer_omega(texto_omega) if necesita_omega else 1
            if tipo_x0 == "Vector cero":
                datos["x0"] = None
            elif tipo_x0 == "Personalizado":
                datos["x0"] = leer_vector(texto_x0, "vector inicial x⁽⁰⁾")
            else:
                datos["x0"] = vector_diagonal(A, b)
            return datos
        except (ErrorEntrada, ErrorMatriz) as error:
            st.error(f"❌ {error}")
            return None

    with pestana_uno:
        metodo = st.selectbox("Método", METODOS, key="it_metodo")
        if st.button("Ejecutar", type="primary", key="it_ejecutar"):
            st.session_state.pop("it_resultado", None)
            datos = leer_todo(metodo == SOR)
            if datos:
                config = ConfiguracionIterativa(
                    metodo=metodo, criterio=criterio, x0=datos["x0"],
                    tolerancia=datos.get("tolerancia", 1e-3), k_max=datos.get("k_max", 50),
                    n_iteraciones=datos.get("n_iteraciones", 5), omega=datos["omega"])
                st.session_state["it_resultado"] = ejecutar(datos["A"], datos["b"], config)
        if "it_resultado" in st.session_state:
            mostrar_ejecucion(st.session_state["it_resultado"])

    with pestana_comparar:
        comparar(leer_todo)

    with pestana_conv:
        convergencia(texto_A, texto_b, texto_omega)


# ---------------------------------------------------------------------------
# Una ejecución
# ---------------------------------------------------------------------------

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
    mostrar_motivo(r)
    for aviso in r.advertencias:
        st.warning("⚠️ " + aviso)
    if not r.historial:
        return
    cumplido = {True: "Sí", False: "No", None: "No aplica"}[r.criterio_cumplido]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Iteraciones realizadas", r.k_final)
    c2.metric("Diferencia final d_k", "—" if r.d_final is None else formatear_numero(r.d_final, 6))
    c3.metric("Residuo final r_k", formatear_numero(r.r_final, 6))
    c4.metric("¿Se cumplió el criterio?", cumplido)
    st.markdown("**Aproximación final** x⁽ᵏ⁾ = (" +
                ", ".join(formatear_numero(v, 10) for v in r.x_final) + ")")
    st.caption("d_k mide cuánto cambió la aproximación; r_k mide cuánto falla la ecuación "
               "A x = b. Ninguno de los dos es el error respecto a la solución exacta.")
    st.dataframe(filas_tabla(r), hide_index=True, width="stretch")
    st.download_button("⬇️ Descargar tabla de iteraciones (CSV)", csv_historial(r),
                       file_name=f"iteraciones_{r.configuracion.metodo}.csv", mime="text/csv",
                       key=f"csv_{r.configuracion.metodo}")
    fig = grafica_convergencia(r.historial, r.configuracion.criterio,
                               r.configuracion.tolerancia
                               if r.configuracion.criterio != CRITERIO_ITERACIONES else None)
    st.pyplot(fig)
    cerrar(fig)


# ---------------------------------------------------------------------------
# Comparación
# ---------------------------------------------------------------------------

def comparar(leer_todo):
    st.markdown("Los tres métodos se ejecutan con **el mismo sistema, vector inicial, criterio, "
                "tolerancia y máximo de iteraciones**; SOR usa además su propio ω.")
    if st.button("Comparar Jacobi, Gauss-Seidel y SOR", type="primary", key="it_comparar"):
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
        st.error("❌ " + comp.resultados[0].mensaje)
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
            "Motivo de parada": r.codigo,
            "¿Criterio cumplido?": {True: "Sí", False: "No", None: "No aplica"}[r.criterio_cumplido],
            "d final": "—" if r.d_final is None else formatear_numero(r.d_final, 6),
            "r final": "—" if r.r_final is None else formatear_numero(r.r_final, 6),
            "e final = ‖x⁽ᵏ⁾ − x*‖∞": "no disponible" if e is None else formatear_numero(e, 6),
            "ρ(T)": "—" if rho is None or rho.rho is None else formatear_numero(rho.rho, 6),
        })
    st.dataframe(filas, hide_index=True, width="stretch")
    st.caption("ℹ️ " + comp.nota)
    if comp.referencia is not None:
        st.caption("x* = solución del método directo (Gauss exacto): (" +
                   ", ".join(formatear_numero(v, 10) for v in comp.referencia) + "). "
                   "e final es el error respecto a esa solución; no es d_k ni r_k.")
    else:
        st.caption("No hay solución de referencia (el sistema no tiene solución única): "
                   "e final no está disponible.")
    for r in comp.resultados:
        if r.codigo not in ("TOLERANCIA_CAMBIO", "TOLERANCIA_RESIDUO", "N_COMPLETADAS"):
            st.warning(f"{r.configuracion.metodo}: {r.mensaje}")
    opciones = {"d": "Cambio entre iteraciones d_k", "r": "Residuo r_k",
                "e": "Error respecto a la solución del método directo e_k"}
    metrica = st.radio("Métrica a graficar", list(opciones), format_func=opciones.get,
                       horizontal=True, key="it_metrica")
    if metrica == "e" and comp.referencia is None:
        st.info("No hay solución de referencia para graficar e_k.")
    else:
        fig = grafica_comparacion(comp.resultados, metrica, comp.errores_historial)
        st.pyplot(fig)
        cerrar(fig)

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
                    filas.append({"ω": formatear_numero(w), "Iteraciones": r.k_final,
                                  "Motivo": r.codigo,
                                  "r final": "—" if r.r_final is None else formatear_numero(r.r_final, 6),
                                  "ρ(T_ω)": "—" if rho is None else formatear_numero(rho, 6)})
                st.dataframe(filas, hide_index=True, width="stretch")
                st.caption("Cuanto menor es ρ(T_ω), más rápida es la convergencia asintótica. "
                           "Con ω = 1, SOR coincide con Gauss-Seidel.")


# ---------------------------------------------------------------------------
# Convergencia: dominancia diagonal y radio espectral
# ---------------------------------------------------------------------------

def convergencia(texto_A, texto_b, texto_omega):
    metodo = st.selectbox("Método a analizar", METODOS, key="it_conv_metodo")
    if st.button("Analizar convergencia", type="primary", key="it_conv"):
        st.session_state.pop("it_convergencia", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            try:
                omega = leer_omega(texto_omega) if metodo == SOR else None
                st.session_state["it_convergencia"] = (
                    dominancia_diagonal(A), radio_espectral(A, b, metodo, omega))
            except (ErrorEntrada, ErrorMatriz) as error:
                st.error(f"❌ {error}")
    if "it_convergencia" not in st.session_state:
        return
    dom, esp = st.session_state["it_convergencia"]

    st.subheader("1. Dominancia diagonal estricta por filas")
    st.table([{"Fila": f[0] + 1, "|aᵢᵢ|": formatear_numero(f[1]),
               "Σ_{j≠i} |aᵢⱼ|": formatear_numero(f[2]), "¿|aᵢᵢ| > Σ?": "✔" if f[3] else "✘"}
              for f in dom.filas])
    (st.success if dom.estricta else st.warning)(dom.mensaje)

    it = esp.iteracion
    st.subheader(f"2. Matriz de iteración de {it.metodo}")
    formulas = {
        JACOBI: r"T_J=-D^{-1}(L+U),\qquad c=D^{-1}b",
        GAUSS_SEIDEL: r"T_{GS}=-(D+L)^{-1}U,\qquad c=(D+L)^{-1}b",
        SOR: r"T_\omega=(D+\omega L)^{-1}\left[(1-\omega)D-\omega U\right],\qquad c=\omega(D+\omega L)^{-1}b",
    }
    st.latex(formulas[it.metodo])
    st.latex(r"D=" + latex_matriz(it.D) + r",\; L=" + latex_matriz(it.L) + r",\; U=" + latex_matriz(it.U))
    st.latex(r"T=" + latex_matriz(it.T) + r",\qquad c=" + latex_vector(it.c))

    st.subheader("3. Polinomio característico, autovalores y radio espectral")
    if esp.conclusion == NO_CALCULADO:
        st.warning(esp.mensaje)
        return
    st.markdown(f"`{esp.polinomio_curso} = 0`")
    st.caption("Coeficientes calculados de forma exacta (método de Faddeev-LeVerrier; para 3×3 "
               "coincide con el desarrollo por Sarrus visto en clase). Raíces: λ = 0 exactas, "
               "fórmula cuadrática o método de Durand-Kerner (ver guía matemática).")
    st.table([{"λ": formatear_numero(z, 8), "Parte real": f"{z.real:.8g}",
               "Parte imaginaria": f"{z.imag:.8g}", "|λ|": f"{abs(z):.8g}"}
              for z in esp.autovalores])
    if esp.conclusion == CONVERGE:
        st.success("✅ " + esp.mensaje)
    elif esp.conclusion == NO_CONVERGE:
        st.error("🚫 " + esp.mensaje)
    else:
        st.warning("⚠️ " + esp.mensaje)
    for aviso in esp.advertencias:
        st.warning("⚠️ " + aviso)
    v = esp.verificaciones
    st.caption(f"Verificación: suma de autovalores = {formatear_numero(v['suma de autovalores'], 8)}, "
               f"traza(T) = {formatear_numero(v['traza de T'], 8)}; "
               f"máx |p(λ)| relativo = {v['max |p(λ)| relativo']:.2e}.")
    fig = grafica_autovalores(esp.autovalores, esp.rho)
    st.pyplot(fig)
    cerrar(fig)
    st.info("💡 Teorema: x⁽ᵏ⁺¹⁾ = T x⁽ᵏ⁾ + c converge para todo x⁽⁰⁾ si y solo si ρ(T) < 1. "
            "La dominancia diagonal es solo una condición suficiente.")
