"""Interfaz del Módulo III — Mínimos cuadrados y ajuste lineal."""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_III_minimos.minimos import (
    ErrorAjuste,
    SOBREDETERMINADO,
    ajuste_lineal,
    minimos_cuadrados,
)
from interfaz.compartido import ejemplos
from interfaz.compartido.componentes import (
    leer_matriz_ui,
    leer_vector_ui,
    mostrar_interactiva,
)
from interfaz.compartido.formulas import (
    latex_matriz,
    latex_vector,
    tabla_vector,
)
from interfaz.compartido.editor import (
    MATRIZ,
    PUNTOS,
    VECTOR,
    analizar,
    aviso_dimensiones,
    editor,
    problema_dimensiones,
    restaurar,
)
from interfaz.compartido.estilo import (
    encabezado_modulo,
    insignias,
    procedencia,
    seccion,
    tarjeta_resultado,
    valor_destacado,
)
from visualizacion import notacion
from visualizacion.interactivas import ajuste as grafica_ajuste_interactiva


def mostrar():
    encabezado_modulo(
        "III", "Mínimos cuadrados y ajuste lineal",
        "Para un sistema sobredeterminado se resuelven las <b>ecuaciones normales</b> "
        "AᵀA x̂ = Aᵀb con nuestro método de Gauss y se calcula el residuo r = b − A x̂ con su "
        "norma ‖r‖₂. El ajuste lineal es el caso particular de la matriz de diseño [xᵢ 1].",
        [("Ecuaciones normales", "info"), ("Resueltas con Gauss", "info"), ("Fracciones exactas", "ok"),
         ("Verificación por Cramer", "")])
    procedencia([
        ("A", "det[A | b] ≠ 0: b no es combinación de las columnas", "S8-30/09 p. 6"),
        ("A", "Sistema normal AᵀA x = Aᵀb", "S8-30/09 pp. 5-7"),
        ("A", "Regla de Cramer (verificación)", "S8-30/09 pp. 4 y 7"),
        ("B", "Resolver con un método directo propio", "OFICIAL p. 2"),
        ("B", "Residuo r = b − A x̂ y ‖r‖₂", "OFICIAL p. 2"),
        ("B", "Recta de mejor ajuste y gráfica", "OFICIAL p. 2"),
    ])
    pestana_sistema, pestana_ajuste = st.tabs(["Sistema sobredeterminado", "Ajuste lineal de datos"])
    with pestana_sistema:
        sistema()
    with pestana_ajuste:
        ajuste()


def sistema():
    seccion("1", "Sistema A x ≈ b", "m ecuaciones y n incógnitas, con m > n")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.MINIMOS), key="mc_ejemplo")
    A_txt, b_txt = ejemplos.MINIMOS[nombre]
    boton.button("⟲ Cargar ejemplo", key="mc_cargar", width="stretch", on_click=restaurar,
                 args=(f"mc_A_{nombre}", f"mc_b_{nombre}"))
    col1, col2 = st.columns([3, 1.1])
    with col1:
        texto_A = editor(f"mc_A_{nombre}", "Matriz A (m × n)", A_txt, MATRIZ, nombre="matriz A",
                         css="mc_A", ayuda="Más filas (ecuaciones) que columnas (incógnitas).")
    with col2:
        texto_b = editor(f"mc_b_{nombre}", "Vector b (m)", b_txt.replace(" ", "\n"), VECTOR,
                         nombre="vector b", css="mc_b", encabezados=["b"], etiqueta_fila="")
    # A puede ser rectangular: solo se exige que b tenga m componentes.
    bloqueado = aviso_dimensiones(problema_dimensiones(analizar(texto_A, MATRIZ, "matriz A")[0],
                                                      analizar(texto_b, VECTOR, "vector b")[0]))
    if st.button("Resolver por mínimos cuadrados", type="primary", key="mc_resolver", disabled=bloqueado):
        st.session_state.pop("mc_resultado", None)
        A = leer_matriz_ui(texto_A, "matriz A")
        b = leer_vector_ui(texto_b, "vector b")
        if A is not None and b is not None:
            try:
                st.session_state["mc_resultado"] = minimos_cuadrados(A, b)
            except ErrorMatriz as error:
                st.error(f"❌ {notacion.md(str(error))}")
    if "mc_resultado" in st.session_state:
        mostrar_minimos(st.session_state["mc_resultado"])


def mostrar_minimos(r, nombres=None):
    seccion("2" if nombres is None else "3", "Ecuaciones normales y solución")
    if r.tipo == SOBREDETERMINADO:
        st.info("🔎 " + notacion.md(r.mensaje_tipo))
    else:
        st.warning("🔎 " + notacion.md(r.mensaje_tipo))
    st.markdown("**Ecuaciones normales** AᵀA x̂ = Aᵀb:")
    st.latex(r"A^TA = " + latex_matriz(r.AtA) + r",\qquad A^Tb = " + latex_vector(r.Atb))
    if r.solucion is None:
        for aviso in r.advertencias:
            st.error("🚫 " + notacion.md(aviso))
        st.info("💡 Recomendación: elimine las columnas que sean combinación de otras (o agregue "
                "datos que las distingan) para que AᵀA sea invertible.")
        return
    with tarjeta_resultado("minimos" if nombres is None else "minimos_ajuste"):
        st.success("✅ " + notacion.md(r.mensaje))
        insignias([("Sobredeterminado" if r.tipo == SOBREDETERMINADO else r.tipo.capitalize(), "info"),
                   ("b ∈ Col(A): solución exacta" if r.b_en_espacio_columna else "b ∉ Col(A): aproximación",
                    "ok" if r.b_en_espacio_columna else "aviso"),
                   ("Aᵀr = 0 verificado" if all(v == 0 for v in r.ortogonalidad) else "Aᵀr ≠ 0",
                    "ok" if all(v == 0 for v in r.ortogonalidad) else "error")])
        izquierda, derecha = st.columns([3, 2])
        with izquierda:
            st.latex(r"\hat x = " + latex_vector(r.solucion))
        with derecha:
            valor_destacado("‖r‖₂ (error de ajuste)", f"{r.norma_residuo_2:.8g}",
                            f"‖r‖₂² = {formatear_numero(r.norma_residuo_2_cuadrado)} (exacto)")
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
    with st.expander("Procedimiento de clase (S8-30/09 pp. 5-7): det[A | b], ecuaciones normales y Cramer"):
        if r.det_aumentada is not None:
            st.markdown(notacion.md(
                rf"1. $\det[A \mid b]$ = **{formatear_numero(r.det_aumentada)}** "
                + (r"≠ 0: $b$ es linealmente independiente de las columnas de $A$, $b \notin \mathrm{Col}(A)$ "
                   "(no hay solución exacta)."
                   if r.det_aumentada != 0 else
                   "= 0: $b$ es combinación lineal de las columnas de $A$ (hay solución exacta).")))
        else:
            st.markdown(r"1. $\det[A \mid b]$ solo aplica cuando $m = n + 1$; la consistencia se "
                        "decidió con el rango (Gauss).")
        st.markdown(r"2. Sistema de ecuaciones normales asociado $A^TA\,\hat x = A^Tb$ (arriba).")
        if r.cramer is not None:
            # Notación de la lámina de Cramer (S8-30/09 p. 4): D = det(A), Dᵢ = det(Aᵢ), xᵢ = Dᵢ/D;
            # aquí la matriz del sistema es AᵀA y Aᵢ reemplaza su columna i por Aᵀb.
            detalle = ", ".join(f"$D_{{{j + 1}}}$ = {formatear_numero(d)}"
                                for j, d in enumerate(r.cramer["dets"]))
            coincide = r.cramer["solucion"] == r.solucion
            st.markdown(notacion.md(
                rf"3. Regla de Cramer: $D = \det(A^TA)$ = {formatear_numero(r.cramer['det'])}, {detalle} "
                r"→ $\hat x_i = D_i / D$ = (" + ", ".join(formatear_numero(v) for v in r.cramer["solucion"]) + ")"
                + (" — **coincide exactamente** con Gauss." if coincide else " — ⚠️ no coincide.")))
            st.caption(r"$D_i = \det(A_i)$, donde $A_i$ es $A^TA$ con la columna $i$ reemplazada por "
                       r"$A^Tb$ (en el manuscrito: $|A|$, $|A_x|$ y $|A_y|$).")
        else:
            st.markdown(r"3. Cramer se muestra como verificación para $n \le 3$ incógnitas.")
    st.info("💡 ‖r‖₂ mide la distancia entre b y el vector A x̂ más cercano del espacio "
            "columna de A: cuanto menor, mejor se aproximan los datos. ‖r‖₂ = 0 solo si el "
            "sistema tiene solución exacta.")


def ajuste():
    seccion("1", "Datos (xᵢ, yᵢ)", "al menos 2 puntos con x distintos")
    sel, boton = st.columns([4, 1], vertical_alignment="bottom")
    nombre = sel.selectbox("Ejemplo del curso", list(ejemplos.AJUSTE), key="aj_ejemplo")
    x_txt, y_txt = ejemplos.AJUSTE[nombre]
    pares = "\n".join(f"{x} {y}" for x, y in zip(x_txt.split(), y_txt.split()))
    boton.button("⟲ Cargar ejemplo", key="aj_cargar", width="stretch", on_click=restaurar,
                 args=(f"aj_xy_{nombre}",))
    izquierda, derecha = st.columns([2, 1.3])
    with izquierda:
        texto_xy = editor(f"aj_xy_{nombre}", "Tabla de puntos (xᵢ, yᵢ)", pares, PUNTOS,
                          nombre="tabla de puntos", css="aj_xy", encabezados=["x", "y"],
                          ayuda="Un punto por línea: x y (por ejemplo «2 2.5»).")
    with derecha:
        st.caption("Cada fila es un punto (xᵢ, yᵢ). Use «＋ Punto» para agregar datos o pegue "
                   "dos columnas copiadas de una hoja de cálculo en la pestaña «Pegar».")
    if st.button("Calcular recta de ajuste", type="primary", key="aj_calcular"):
        st.session_state.pop("aj_resultado", None)
        puntos = leer_matriz_ui(texto_xy, "tabla de puntos")
        xs = ys = None
        if puntos is not None:
            if len(puntos[0]) != 2:
                st.error("❌ Cada punto debe tener exactamente 2 valores (x e y).")
            else:
                xs, ys = [p[0] for p in puntos], [p[1] for p in puntos]
        if xs is not None and ys is not None:
            try:
                st.session_state["aj_resultado"] = ajuste_lineal(xs, ys)
            except ErrorAjuste as error:
                st.error(f"❌ {notacion.md(str(error))}")
    if "aj_resultado" not in st.session_state:
        return
    r = st.session_state["aj_resultado"]
    seccion("2", "Recta de mejor ajuste")
    with tarjeta_resultado("ajuste"):
        st.success(f"✅ Recta de mejor ajuste: **{r.ecuacion}**  "
                   f"(m ≈ {float(r.pendiente):.8g}, c ≈ {float(r.intercepto):.8g})")
        valor_destacado("Ecuación", r.ecuacion,
                        f"m ≈ {float(r.pendiente):.8g} · c ≈ {float(r.intercepto):.8g} · "
                        f"‖r‖₂ ≈ {r.minimos.norma_residuo_2:.6g}")
        mostrar_interactiva(grafica_ajuste_interactiva(r.xs, r.ys, r.pendiente, r.intercepto,
                                                       r.minimos.estimados), "ajuste")
    st.latex(r"A=\begin{bmatrix} x_1 & 1\\ \vdots & \vdots\\ x_k & 1\end{bmatrix},\quad "
             r"b=\begin{bmatrix} y_1\\ \vdots\\ y_k\end{bmatrix},\quad "
             r"A^TA\begin{bmatrix} m\\ c\end{bmatrix}=A^Tb")
    mostrar_minimos(r.minimos, nombres=["m (pendiente)", "c (intercepto)"])
