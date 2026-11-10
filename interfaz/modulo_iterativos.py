"""Interfaz del Módulo IV — Métodos iterativos y convergencia."""

import csv
import io

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import (
    ErrorEntrada,
    formatear_numero,
    leer_entero_positivo,
    leer_omega,
    leer_tolerancia,
    leer_vector,
)
from algebra.dispersas import a_csr
from algebra.espectral import (
    CONVERGE,
    NO_CALCULADO,
    NO_CONVERGE,
    desarrollo_sarrus,
    radio_espectral,
)
from algebra.iterativos import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    CRITERIO_RESIDUO,
    ConfiguracionIterativa,
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
    comparar_metodos,
    configuraciones_homogeneas,
    dominancia_diagonal,
    ejecutar,
    reordenamiento_dominante,
    vector_diagonal,
)
from algebra.precondicionamiento import analizar_precondicionador
from interfaz import ejemplos
from interfaz.componentes import (
    latex_matriz,
    latex_vector,
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_interactiva,
)
from interfaz.editor import (
    MATRIZ,
    VECTOR,
    analizar,
    aviso_dimensiones,
    editor,
    normalizar,
    problema_dimensiones,
    restaurar,
)
from interfaz.estilo import (
    encabezado_modulo,
    insignias,
    marca_incentivo,
    seccion,
    tarjeta_resultado,
    valor_destacado,
)
from visualizacion import interactivas

ETIQUETAS_CRITERIO = {
    CRITERIO_CAMBIO: "A · Cambio entre iteraciones  ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε",
    CRITERIO_RESIDUO: "B · Residuo del sistema  ‖b − Ax⁽ᵏ⁾‖∞ < ε",
    CRITERIO_ITERACIONES: "C · Número fijo de iteraciones N",
}
CIFRAS = 8


def mostrar():
    encabezado_modulo(
        "IV", "Métodos iterativos y convergencia",
        "Jacobi, Gauss-Seidel y SOR implementados desde cero, con criterio de parada, tolerancia, "
        "vector inicial, máximo de iteraciones y factor de relajación configurables. En cada "
        "iteración se registran <b>d_k</b> (cambio entre iteraciones) y <b>r_k</b> (residuo del "
        "sistema original).",
        [("Jacobi", "info"), ("Gauss-Seidel", "info"), ("SOR", "info"), ("Radio espectral", ""),
         ("CSR", "incentivo"), ("Precondicionador M = D", "incentivo")])

    seccion("1", "Sistema A x = b", "A cuadrada, con diagonal no nula")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.ITERATIVOS), key="it_ejemplo")
    A_txt, b_txt = ejemplos.ITERATIVOS[nombre]
    boton.button("⟲ Cargar ejemplo", key="it_cargar", width="stretch", on_click=restaurar,
                 args=(f"it_A_{nombre}", f"it_b_{nombre}", f"it_x0_{nombre}"))
    col1, col2 = st.columns([3, 1.1])
    with col1:
        texto_A = editor(f"it_A_{nombre}", "Matriz A (n × n)", A_txt, MATRIZ, nombre="matriz A",
                         css="it_A", ayuda="Una fila por línea. Los métodos dividen entre cada aᵢᵢ: "
                                           "ningún elemento de la diagonal puede ser 0.")
    with col2:
        texto_b = editor(f"it_b_{nombre}", "Vector b", b_txt.replace(" ", "\n"), VECTOR,
                         nombre="vector b", css="it_b", encabezados=["b"], etiqueta_fila="")

    seccion("2", "Parámetros y criterio de parada", "comunes a las cuatro pestañas")
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
    A_previo = analizar(texto_A, MATRIZ, "matriz A")[0]
    texto_x0 = None
    if tipo_x0 == "Personalizado":
        dimension = len(A_previo[0]) if A_previo else len(A_txt.splitlines())
        x0_col, _ = st.columns([1.1, 3])
        with x0_col:
            texto_x0 = editor(f"it_x0_{nombre}", "x⁽⁰⁾ personalizado", "\n".join(["0"] * dimension),
                              VECTOR, nombre="vector inicial x⁽⁰⁾", css="it_x0", encabezados=["x⁽⁰⁾"],
                              etiqueta_fila="")
    bloqueado = aviso_dimensiones(problema_dimensiones(
        A_previo, analizar(texto_b, VECTOR, "vector b")[0], cuadrada=True,
        x0=analizar(texto_x0, VECTOR, "vector inicial x⁽⁰⁾")[0] if texto_x0 is not None else None))

    seccion("3", "Análisis", "elija una pestaña")
    pestana_uno, pestana_comparar, pestana_conv, pestana_prec = st.tabs(
        ["Ejecutar un método", "Comparar métodos", "Convergencia: dominancia y radio espectral",
         "Precondicionamiento diagonal"])

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
                datos["x0"] = leer_vector(normalizar(texto_x0), "vector inicial x⁽⁰⁾")
            else:
                datos["x0"] = vector_diagonal(A, b)
            return datos
        except (ErrorEntrada, ErrorMatriz) as error:
            st.error(f"❌ {error}")
            return None

    with pestana_uno:
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
            mostrar_ejecucion(st.session_state["it_resultado"])

    with pestana_comparar:
        comparar(leer_todo, bloqueado)

    with pestana_conv:
        convergencia(texto_A, texto_b, texto_omega, bloqueado)

    with pestana_prec:
        precondicionamiento(leer_todo, bloqueado)


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
    st.markdown("**Aproximación final** x⁽ᵏ⁾ = (" +
                ", ".join(formatear_numero(v, 10) for v in r.x_final) + ")")
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


# ---------------------------------------------------------------------------
# Comparación
# ---------------------------------------------------------------------------

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
            "Error final e = ‖x⁽ᵏ⁾ − x*‖∞": "no disponible" if e is None else formatear_numero(e, 6),
            "ρ(T)": "—" if rho is None or rho.rho is None else formatear_numero(rho.rho, 6),
        })
    st.dataframe(filas, hide_index=True, width="stretch")
    st.caption("ℹ️ " + comp.nota)
    if comp.referencia is not None:
        st.caption("x* = solución del método directo (Gauss exacto): (" +
                   ", ".join(formatear_numero(v, 10) for v in comp.referencia) + "). "
                   "El error final e es el error respecto a esa solución, como en la tabla "
                   "comparativa de la lámina S9-05/10 p. 17 (‖x⁽ᵏ⁾ − x‖∞); no es d_k ni r_k.")
    else:
        st.caption("No hay solución de referencia (el sistema no tiene solución única): "
                   "e final no está disponible.")
    for r in comp.resultados:
        if r.codigo not in ("TOLERANCIA_CAMBIO", "TOLERANCIA_RESIDUO", "N_COMPLETADAS"):
            st.warning(f"{r.configuracion.metodo}: {r.mensaje}")
    # e_k primero: es el «error final ‖x⁽ᵏ⁾ − x‖∞» de la lámina S9-05/10 p. 17 (diapositiva 13).
    opciones = {"e": "Error respecto a la solución del método directo e_k",
                "d": "Cambio entre iteraciones d_k", "r": "Residuo r_k"}
    metrica = st.radio("Métrica a graficar", list(opciones), format_func=opciones.get,
                       horizontal=True, key="it_metrica")
    if metrica == "e" and comp.referencia is None:
        st.info("No hay solución de referencia para graficar e_k.")
    else:
        mostrar_interactiva(interactivas.comparacion(comp.resultados, metrica, comp.errores_historial),
                            "comparacion")

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
                    st.error(f"❌ {error}")
    if "it_convergencia" not in st.session_state:
        return
    dom, esp, error_T = st.session_state["it_convergencia"]

    marca_incentivo("Extensión matemática: radio espectral con autovalores complejos", "1 %")
    st.subheader("1. Dominancia diagonal estricta por filas")
    st.table([{"Fila": f[0] + 1, "|aᵢᵢ|": formatear_numero(f[1]),
               "Σ_{j≠i} |aᵢⱼ|": formatear_numero(f[2]), "¿|aᵢᵢ| > Σ?": "✔" if f[3] else "✘"}
              for f in dom.filas])
    (st.success if dom.estricta else st.warning)(dom.mensaje)
    if not dom.estricta:
        reorden = st.session_state.get("it_reorden")
        if reorden is not None:
            A_r, b_r, orden = reorden
            st.info("🔀 Reordenando las ecuaciones como en clase (Tarea II #2-3), la matriz SÍ es "
                    "estrictamente dominante con el orden " +
                    ", ".join(f"E{i + 1}" for i in orden) + ":")
            st.latex(r"A' = " + latex_matriz(A_r) + r",\quad b' = " + latex_vector(b_r))
            st.caption("La aplicación no reordena por su cuenta: copie A' y b' en los campos "
                       "de entrada si desea usar ese orden.")
        else:
            st.caption("Ningún reordenamiento de las ecuaciones logra dominancia diagonal estricta.")

    if esp is None:
        st.error(f"❌ {error_T}")
        return
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
    if len(it.T) == 3:
        traza, menores, det = desarrollo_sarrus(it.T)
        coincide = [-1, traza, -menores, det] == [-c for c in esp.coeficientes]
        st.caption(
            "Desarrollo de clase (Sarrus): det(T − λI) = −λ³ + tr(T)λ² − (Σ menores 2×2)λ + det(T), "
            f"con tr(T) = {formatear_numero(traza)}, Σ menores = {formatear_numero(menores)} y "
            f"det(T) = {formatear_numero(det)} — "
            + ("coincide con el polinomio calculado." if coincide else "⚠️ no coincide."))
    st.caption("Coeficientes calculados de forma exacta (método de Faddeev-LeVerrier; para 3×3 "
               "coincide con el desarrollo por Sarrus visto en clase). Raíces: λ = 0 exactas, "
               "fórmula cuadrática o método de Durand-Kerner (ver guía matemática).")
    st.table([{"λ": formatear_numero(z, 8), "Parte real": f"{z.real:.8g}",
               "Parte imaginaria": f"{z.imag:.8g}", "|λ|": f"{abs(z):.8g}"}
              for z in esp.autovalores])
    with tarjeta_resultado("espectral"):
        izquierda, derecha = st.columns([2, 3])
        with izquierda:
            valor_destacado(f"ρ(T) de {it.metodo}", formatear_numero(esp.rho, 8), "máx |λᵢ| de T")
        with derecha:
            insignias([{CONVERGE: ("Converge para todo x⁽⁰⁾", "ok"),
                        NO_CONVERGE: ("No converge para todo x⁽⁰⁾", "error")}.get(
                           esp.conclusion, ("Indeterminado", "aviso")),
                       ("Decisión exacta" if esp.decision_exacta else
                        ("Cálculo fiable" if esp.fiable else "Cálculo no fiable"),
                        "ok" if esp.decision_exacta or esp.fiable else "aviso"),
                       ("Dominante" if dom.estricta else "No dominante", "ok" if dom.estricta else "")])
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
    st.info("💡 Teorema: x⁽ᵏ⁺¹⁾ = T x⁽ᵏ⁾ + c converge para todo x⁽⁰⁾ si y solo si ρ(T) < 1. "
            "La dominancia diagonal es solo una condición suficiente.")


# ---------------------------------------------------------------------------
# Precondicionamiento diagonal (incentivo, OFICIAL p. 5)
# ---------------------------------------------------------------------------

def precondicionamiento(leer_todo, bloqueado=False):
    marca_incentivo("Precondicionamiento", "1,5 %")
    st.markdown(
        "Precondicionador diagonal de clase (S9-05/10, diapositivas 16-18): "
        r"$M = D = \mathrm{diag}(a_{11},\dots,a_{nn})$ y sistema equivalente "
        r"$M^{-1}Ax = M^{-1}b$. Se comparan κ∞, los autovalores y las iteraciones del sistema "
        "original y del precondicionado con **la misma** configuración (criterio, ε, k_max, x⁽⁰⁾ y ω).")
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
                st.error(f"❌ {error}")
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
            chips.append((f"Richardson: {f.original.codigo} → {f.precondicionado.codigo}",
                          "ok" if f.precondicionado.criterio_cumplido else "aviso"))
        insignias(chips)
        c1, c2 = st.columns(2)
        c1.metric("κ∞(A)", "singular" if r.kappa_A is None else formatear_numero(r.kappa_A))
        c2.metric("κ∞(D⁻¹A)", "singular" if r.kappa_B is None else formatear_numero(r.kappa_B))
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
            "Motivo (original)": f.original.codigo,
            "Iteraciones (precondicionado)":
                "—" if f.precondicionado.k_final is None else f.precondicionado.k_final,
            "Motivo (precondicionado)": f.precondicionado.codigo,
            "ρ(T) original": "—" if f.rho_original is None else formatear_numero(f.rho_original, 6),
            "ρ(T) precondicionado":
                "—" if f.rho_precondicionado is None else formatear_numero(f.rho_precondicionado, 6),
            "¿T y c idénticas?": {True: "Sí (exacto)", False: "No", None: "—"}[f.T_identicas],
            "¿Mismas iteraciones?": "Sí" if f.mismas_iteraciones else "No",
        })
    st.dataframe(filas, hide_index=True, width="stretch")
    for texto in r.conclusiones:
        st.info("💡 " + texto)
    st.warning("**Extensión no vista en clase — método de Richardson.** "
               "La fila «Richardson» (x ← x + (b − Ax), matriz de iteración I − A) no es uno de los "
               "métodos del enunciado ni aparece en los PDF del curso: se incluye como herramienta "
               "de demostración, porque es el método estacionario más simple sobre el que M = D sí "
               "tiene efecto. Richardson precondicionado con M = D es exactamente Jacobi. La lámina "
               "de la diapositiva 19 (S9-05/10 p. 23) muestra una mejora para Jacobi que no se puede "
               "reproducir, porque Jacobi, Gauss-Seidel y SOR ya están normalizados por la diagonal.",
               icon="🧪")
    mostrar_interactiva(interactivas.precondicionador(r.comparaciones), "precondicionador")
