"""Componentes comunes de la interfaz Streamlit: lectura de datos con mensajes de
error, procedimiento paso a paso y gráficas interactivas (barra de herramientas,
selección de puntos).  Las fórmulas LaTeX están en formulas.py.

Aquí solo hay presentación.  Ningún cálculo matemático vive aquí.
"""

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, leer_matriz, leer_vector
from interfaz.compartido.formulas import latex_matriz
from visualizacion import notacion


# Entrada de datos

def leer_matriz_ui(texto, nombre):
    """Lee una matriz; si hay error lo muestra y devuelve None."""
    try:
        return leer_matriz(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {notacion.md(str(error))}")
        return None


def leer_vector_ui(texto, nombre):
    try:
        return leer_vector(texto, nombre)
    except (ErrorEntrada, ErrorMatriz) as error:
        st.error(f"❌ {notacion.md(str(error))}")
        return None


def mostrar_pasos(pasos, separador):
    """Muestra el procedimiento paso a paso (descripción + matriz).

    Si el paso trae la notación de clase («−2F₁ + F₂»), se muestra primero y la
    forma Fᵢ → Fᵢ − m·Fⱼ queda como aclaración."""
    for numero, paso in enumerate(pasos):
        de_clase = getattr(paso, "notacion", "")
        descripcion = notacion.md(paso.descripcion)        # F2 → F₂, x3 → x₃
        if de_clase:
            st.markdown(f"**Paso {numero}.** {de_clase} &nbsp;·&nbsp; <small>{descripcion}</small>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"**Paso {numero}.** {descripcion}")
        st.latex(latex_matriz(paso.matriz, separador=separador))


# Gráficas interactivas (Plotly)

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


