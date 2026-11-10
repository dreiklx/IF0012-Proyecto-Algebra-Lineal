"""Componentes comunes de la interfaz Streamlit.

Aquí solo hay presentación: convertir resultados del núcleo a LaTeX o a
tablas y mostrar errores de entrada.  Ningún cálculo matemático vive aquí.
"""

from fractions import Fraction

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, formatear_numero, leer_matriz, leer_vector


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------

def latex_numero(valor, cifras=6):
    """Fracción exacta como \\frac{p}{q}; el resto como decimal."""
    if isinstance(valor, Fraction) and valor.denominator != 1:
        if len(str(valor)) <= 14:
            signo = "-" if valor < 0 else ""
            return rf"{signo}\frac{{{abs(valor.numerator)}}}{{{valor.denominator}}}"
        return formatear_numero(float(valor), cifras)
    if isinstance(valor, complex):
        return formatear_numero(valor, cifras).replace("−", "-").replace("i", r"\,i")
    return formatear_numero(valor, cifras)


def latex_matriz(M, separador=None, cifras=6):
    """Matriz entre corchetes; `separador` es el índice de columna antes del que
    se dibuja una línea vertical (para [A | b])."""
    n = len(M[0])
    columnas = "".join("c" if separador is None or j != separador else "|c" for j in range(n))
    # Las fracciones apiladas (\frac) quedan montadas entre filas si no se añade
    # espacio vertical (defecto visual detectado en la revisión manual).
    hay_fracciones = any(isinstance(v, Fraction) and v.denominator != 1 for fila in M for v in fila)
    salto = r" \\[6pt] " if hay_fracciones else r" \\ "
    filas = salto.join(" & ".join(latex_numero(v, cifras) for v in fila) for fila in M)
    return rf"\left[\begin{{array}}{{{columnas}}} {filas} \end{{array}}\right]"


def latex_vector(v, cifras=6):
    return latex_matriz([[x] for x in v], cifras=cifras)


def texto_vector(v, cifras=6):
    return "(" + ", ".join(formatear_numero(x, cifras) for x in v) + ")"


# ---------------------------------------------------------------------------
# Entrada de datos
# ---------------------------------------------------------------------------

def leer_matriz_ui(texto, nombre):
    """Lee una matriz; si hay error lo muestra y devuelve None."""
    try:
        return leer_matriz(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {error}")
        return None


def leer_vector_ui(texto, nombre):
    try:
        return leer_vector(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {error}")
        return None


def ayuda_formato():
    st.caption(
        "Formato: una fila por línea y los números separados por espacios. "
        "Se aceptan enteros, decimales con punto o coma (2.5 o 2,5), fracciones (1/3) "
        "y notación científica (1e-3).")


def tabla_vector(v, nombre="x", cifras=6):
    """Filas para st.table: componente, valor exacto (si es fracción) y decimal."""
    filas = []
    for i, valor in enumerate(v, start=1):
        fila = {"Componente": f"{nombre}{i}", "Valor": formatear_numero(valor, cifras)}
        if isinstance(valor, Fraction):
            fila["Decimal"] = f"{float(valor):.10g}"
        filas.append(fila)
    return filas


def mostrar_pasos(pasos, separador):
    """Muestra el procedimiento paso a paso (descripción + matriz).

    Si el paso trae la notación de clase («−2F₁ + F₂»), se muestra primero y la
    forma Fᵢ → Fᵢ − m·Fⱼ queda como aclaración."""
    for numero, paso in enumerate(pasos):
        notacion = getattr(paso, "notacion", "")
        if notacion:
            st.markdown(f"**Paso {numero}.** {notacion} &nbsp;·&nbsp; <small>{paso.descripcion}</small>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"**Paso {numero}.** {paso.descripcion}")
        st.latex(latex_matriz(paso.matriz, separador=separador))


# ---------------------------------------------------------------------------
# Gráficas interactivas (Plotly)
# ---------------------------------------------------------------------------

CONTROLES_2D = ("Controles: ⛶ (arriba a la derecha) amplía la gráfica a pantalla completa y Esc la "
                "devuelve · arrastre para ampliar una región · rueda para acercar o alejar · "
                "botones ＋/－ de zoom, «Desplazar», «Autoescala» y «Restablecer» en la barra vertical "
                "de la derecha · pase el cursor para ver los valores · clic en la leyenda para ocultar o "
                "mostrar una serie (doble clic: solo esa serie).")
CONTROLES_SELECCION = (" · clic en un punto para ver esa iteración · «Seleccionar zona» (barra derecha) "
                       "y arrastre para listar varias iteraciones.")
CONTROLES_3D = ("Controles: arrastre para rotar · rueda para acercar o alejar · botones «Órbita», "
                "«Girar», «Desplazar» y «Restablecer vista» en la barra vertical de la derecha · pase el "
                "cursor sobre un plano o la solución para ver sus coordenadas · clic en la leyenda "
                "para ocultar un plano.")


def mostrar_interactiva(fig, clave, tres_d=False, mostrar_ayuda=True, seleccion=False):
    """Muestra una figura de Plotly con la barra de herramientas siempre visible.

    Con `seleccion=True` (solo 2D) un clic o un recuadro selecciona puntos; Streamlit
    vuelve a ejecutar la página y la selección queda en st.session_state[f"graf_{clave}"].
    Solo presentación: la figura ya contiene los datos calculados por el núcleo."""
    botones = (["orbitRotation", "tableRotation", "pan3d", "zoom3d", "resetCameraDefault3d",
                "resetCameraLastSave3d", "toImage"] if tres_d else
               ["zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d", "toImage"]
               + (["select2d"] if seleccion else []))
    todos = {"zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
             "resetScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines",
             "orbitRotation", "tableRotation", "pan3d", "zoom3d", "resetCameraDefault3d",
             "resetCameraLastSave3d", "hoverClosest3d", "toImage"}
    config = {
        "displayModeBar": True, "displaylogo": False, "scrollZoom": True, "responsive": True,
        "modeBarButtonsToRemove": sorted(todos - set(botones)),
        "toImageButtonOptions": {"format": "png", "filename": f"IF0012_{clave}", "scale": 2},
        "doubleClick": "reset+autosize",
    }
    if seleccion and not tres_d:
        st.plotly_chart(fig, key=f"graf_{clave}", config=config, theme=None, width="stretch",
                        on_select="rerun", selection_mode=("points", "box"))
    else:
        st.plotly_chart(fig, key=f"graf_{clave}", config=config, theme=None, width="stretch")
    if mostrar_ayuda:
        st.caption("🖱️ " + (CONTROLES_3D if tres_d else CONTROLES_2D + (CONTROLES_SELECCION if seleccion else "")))


def iteraciones_seleccionadas(clave):
    """Valores de k (eje x) de los puntos elegidos en la gráfica `clave`, sin repetir."""
    estado = st.session_state.get(f"graf_{clave}") or {}
    puntos = (estado.get("selection") or {}).get("points") or []
    return sorted({int(round(p["x"])) for p in puntos if isinstance(p.get("x"), (int, float))})


def iteracion_elegida(clave, clave_deslizador, ks, firma):
    """Sincroniza el clic en la gráfica con el deslizador de iteración y devuelve la k elegida.

    - Un clic sobre un punto (selección nueva de un solo k) mueve el deslizador a esa k.
    - Si cambió el resultado (otra `firma`), el deslizador vuelve a la última iteración.
    Debe llamarse ANTES de dibujar la gráfica y el deslizador."""
    marca = f"{clave_deslizador}__firma"
    ultima_sel = f"{clave_deslizador}__seleccion"
    if st.session_state.get(marca) != firma or st.session_state.get(clave_deslizador) not in ks:
        st.session_state[marca] = firma
        st.session_state[clave_deslizador] = ks[-1]
        st.session_state[ultima_sel] = None
    elegidas = iteraciones_seleccionadas(clave)
    if len(elegidas) == 1 and elegidas != st.session_state.get(ultima_sel) and elegidas[0] in ks:
        st.session_state[clave_deslizador] = elegidas[0]
    st.session_state[ultima_sel] = elegidas
    return st.session_state[clave_deslizador]
