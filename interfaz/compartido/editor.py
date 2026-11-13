"""Editor interactivo de matrices, vectores y tablas de puntos (solo interfaz).

Cada editor tiene una única fuente de verdad: el TEXTO de siempre (una fila por
línea, números separados por espacios), guardado en st.session_state con la
misma clave que usaban los antiguos campos de texto.  La rejilla de celdas es
una vista sincronizada de ese texto:

  * al editar una celda o pulsar un botón se reescribe el texto;
  * al pegar o escribir el texto se reconstruye la rejilla.

Así las funciones del núcleo reciben exactamente el mismo formato y los mismos
valores que antes: el texto se lee con algebra.validacion.leer_matriz /
leer_vector (sin cambios), que validan cada número y señalan su posición.

Separadores aceptados al pegar: espacios, tabulaciones, «;» y comas seguidas de
espacio («1, 2, 3»).  Una coma sin espacio sigue siendo coma decimal («2,5»).
"""

import html
import re

import streamlit as st

from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada, leer_matriz, leer_vector
from interfaz.compartido.formulas import latex_matriz
from interfaz.compartido.estilo import insignias

MAX_VISUAL_FILAS = 12      # por encima de esto la rejilla se reemplaza por el texto
MAX_VISUAL_COLUMNAS = 10
MAX_DIMENSION = 60         # tope de los selectores de dimensión
VACIA = "?"                # marca en el texto de una celda sin valor

MATRIZ, VECTOR, PUNTOS = "matriz", "vector", "puntos"


# Conversión texto <-> celdas (funciones puras, probadas en tests/interfaz/test_editor.py)

def normalizar(texto):
    """Unifica los separadores admitidos en espacios, sin tocar los números."""
    lineas = []
    for linea in str(texto or "").splitlines():
        linea = re.sub(r"[\[\]]", " ", linea)        # corchetes de una matriz pegada
        linea = linea.replace(";", " ").replace("\t", " ")
        linea = re.sub(r",(\s+|$)", " ", linea)       # «1, 2, 3» -> «1 2 3»; «2,5» se conserva
        lineas.append(" ".join(linea.split()))
    return "\n".join(lineas).strip("\n")


def celdas_de_texto(texto, columnas_fijas=None):
    """Texto -> lista de filas de cadenas (rectangular; rellena con "" si hace falta)."""
    filas = [linea.split() for linea in normalizar(texto).splitlines() if linea.strip()]
    filas = [[("" if c == VACIA else c) for c in fila] for fila in filas] or [[""]]
    ancho = columnas_fijas or max(len(f) for f in filas)
    return [(f + [""] * ancho)[:ancho] for f in filas]


def texto_de_celdas(celdas):
    """Celdas -> texto; una celda vacía se escribe como «?» para que la lectura
    indique exactamente su posición en lugar de desplazar los números."""
    return "\n".join(" ".join((c.strip() or VACIA) for c in fila) for fila in celdas)


def celdas_vacias(celdas):
    return [(i + 1, j + 1) for i, fila in enumerate(celdas) for j, c in enumerate(fila) if not c.strip()]


def redimensionar(celdas, filas, columnas):
    celdas = [list(f) for f in celdas]
    celdas = (celdas + [[""] * columnas for _ in range(filas)])[:filas]
    return [(f + [""] * columnas)[:columnas] for f in celdas]


def identidad(n):
    return [["1" if i == j else "0" for j in range(n)] for i in range(n)]


def ceros(filas, columnas):
    return [["0"] * columnas for _ in range(filas)]


# Estado en session_state

def _k(clave, sufijo):
    return f"{clave}__{sufijo}"


def _celda(clave, i, j):
    return f"{clave}__c{i}_{j}"


def _escribir(clave, celdas, actualizar_texto=True):
    """Guarda las celdas (claves de los widgets), sus dimensiones y, si se pide, el texto."""
    ss = st.session_state
    m, n = len(celdas), len(celdas[0])
    for i in range(m):
        for j in range(n):
            ss[_celda(clave, i, j)] = celdas[i][j]
    ss[_k(clave, "dim")] = (m, n)
    ss[_k(clave, "nf")] = m
    ss[_k(clave, "nc")] = n
    if actualizar_texto:
        ss[clave] = texto_de_celdas(celdas)
    ss[_k(clave, "firma")] = ss[clave]


def _leer_celdas(clave):
    ss = st.session_state
    m, n = ss[_k(clave, "dim")]
    return [[str(ss.get(_celda(clave, i, j), "")) for j in range(n)] for i in range(m)]


def _sincronizar(clave, columnas_fijas):
    """Si el texto cambió (pegado, ejemplo nuevo, prueba automática), rehace la rejilla."""
    ss = st.session_state
    if ss.get(_k(clave, "firma")) != ss[clave] or _k(clave, "dim") not in ss:
        _escribir(clave, celdas_de_texto(ss[clave], columnas_fijas), actualizar_texto=False)


# Acciones (callbacks: se ejecutan antes de dibujar los widgets)

def _al_editar_celda(clave):
    _escribir(clave, _leer_celdas(clave))


def _accion(clave, accion, columnas_fijas=None):
    ss = st.session_state
    celdas = _leer_celdas(clave)
    m, n = len(celdas), len(celdas[0])
    if accion == "mas_fila":
        celdas = redimensionar(celdas, min(m + 1, MAX_DIMENSION), n)
    elif accion == "menos_fila":
        celdas = redimensionar(celdas, max(m - 1, 1), n)
    elif accion == "mas_col" and not columnas_fijas:
        celdas = redimensionar(celdas, m, min(n + 1, MAX_DIMENSION))
    elif accion == "menos_col" and not columnas_fijas:
        celdas = redimensionar(celdas, m, max(n - 1, 1))
    elif accion == "dimension":
        celdas = redimensionar(celdas, int(ss[_k(clave, "nf")]),
                               columnas_fijas or int(ss.get(_k(clave, "nc"), n)))
    elif accion == "identidad":
        celdas = identidad(m)
    elif accion == "ceros":
        celdas = ceros(m, n)
    elif accion == "limpiar":
        celdas = [[""] * n for _ in range(m)]
    elif accion == "restaurar":
        celdas = celdas_de_texto(ss[_k(clave, "ejemplo")], columnas_fijas)
        ss[_k(clave, "cargado")] = True
    _escribir(clave, celdas)


def restaurar(*claves):
    """Vuelve a cargar el ejemplo seleccionado en los editores indicados (botón del módulo)."""
    for clave in claves:
        if _k(clave, "ejemplo") in st.session_state:
            _escribir(clave, celdas_de_texto(st.session_state[_k(clave, "ejemplo")],
                                             st.session_state.get(_k(clave, "fijas"))))
            st.session_state[_k(clave, "cargado")] = True


# Estado de validación (antes de calcular)

def analizar(texto, tipo, nombre):
    """Devuelve (valor_leido_o_None, mensaje, tipo_de_chip) sin mostrar nada."""
    if not normalizar(texto).strip():
        return None, f"La {nombre} está vacía." if tipo != VECTOR else f"El {nombre} está vacío.", "aviso"
    vacias = celdas_vacias(celdas_de_texto(texto))
    if vacias:
        lista = ", ".join(f"({i}, {j})" if tipo != VECTOR else str(i) for i, j in vacias[:6])
        mas = "…" if len(vacias) > 6 else ""
        return None, f"Faltan valores: {lista}{mas}.", "aviso"
    try:
        if tipo == VECTOR:
            valor = leer_vector(normalizar(texto), nombre)
            return valor, f"Vector de {len(valor)} componentes listo.", "ok"
        valor = leer_matriz(normalizar(texto), nombre)
        if tipo == PUNTOS:
            if len(valor[0]) != 2:
                return None, "Cada punto debe tener exactamente 2 valores: x e y.", "error"
            return valor, f"{len(valor)} puntos listos.", "ok"
        m, n = len(valor), len(valor[0])
        forma = "cuadrada" if m == n else ("más filas que columnas" if m > n else "más columnas que filas")
        return valor, f"Matriz {m}×{n} lista ({forma}).", "ok"
    except (ErrorEntrada, ErrorMatriz) as error:
        return None, str(error), "error"


# Componente

def editor(clave, etiqueta, ejemplo, tipo=MATRIZ, nombre=None, css="ed", encabezados=None,
           etiqueta_fila=None, ayuda=None, altura=130):
    """Dibuja el editor y devuelve el texto normalizado (listo para leer_matriz/leer_vector).

    clave   clave del texto en session_state (la misma que el antiguo campo de texto)
    ejemplo texto inicial y valor de «Restaurar ejemplo»
    tipo    MATRIZ, VECTOR (una columna) o PUNTOS (dos columnas: x, y)
    css     identificador ASCII para el contenedor (estilo y pruebas)
    """
    ss = st.session_state
    columnas_fijas = 1 if tipo == VECTOR else (2 if tipo == PUNTOS else None)
    nombre = nombre or etiqueta
    if clave not in ss:
        ss[clave] = ejemplo
    ss[_k(clave, "ejemplo")] = ejemplo
    ss[_k(clave, "fijas")] = columnas_fijas
    _sincronizar(clave, columnas_fijas)
    m, n = ss[_k(clave, "dim")]

    with st.container(key=f"editor_{css}"):
        st.markdown(f'<div class="ed-titulo">{html.escape(etiqueta)}</div>', unsafe_allow_html=True)
        visual, texto = st.tabs(["✏️ Editor", "📋 Pegar"])
        with visual:
            _controles(clave, tipo, columnas_fijas)
            if m > MAX_VISUAL_FILAS or n > MAX_VISUAL_COLUMNAS:
                st.info(f"La {nombre} es de {m}×{n}: es demasiado grande para la rejilla. "
                        "Edítela en la pestaña «Pegar».")
            else:
                _rejilla(clave, m, n, tipo, encabezados, etiqueta_fila)
        with texto:
            st.text_area(etiqueta, key=clave, height=altura, label_visibility="collapsed",
                         help=ayuda or "Una fila por línea. Separe los números con espacios, "
                                       "tabulaciones, «;» o «, ».")
            st.caption("Pegue o escriba: una fila por línea; separadores: espacio, tabulación, "
                       "«;» o coma seguida de espacio. Decimales con punto o coma (2.5 o 2,5), "
                       "fracciones (1/3), notación científica (1e-3).")
            valor, _, estado = analizar(ss[clave], tipo, nombre)
            if valor is not None and tipo != PUNTOS:
                st.latex(r"\text{Interpretado: }" + latex_matriz(valor if tipo == MATRIZ else [[v] for v in valor]))
        _, mensaje, estado = analizar(ss[clave], tipo, nombre)
        cargado = ss.pop(_k(clave, "cargado"), False)
        insignias([(("✔ " if estado == "ok" else "⚠ ") + ("Ejemplo cargado · " if cargado else "") + mensaje,
                     estado)])
        # marca invisible: el CSS destaca el editor solo en la ejecución en que se cargó el ejemplo
        st.markdown(f'<span class="ed-marca{" ed-cargado" if cargado else ""}"></span>', unsafe_allow_html=True)
    return normalizar(ss[clave])


def _controles(clave, tipo, columnas_fijas):
    etiquetas = {MATRIZ: ("Filas", "fila"), VECTOR: ("Dimensión", "elemento"), PUNTOS: ("Puntos", "punto")}
    rotulo, unidad = etiquetas[tipo]
    if tipo == MATRIZ:
        c1, c2, c3 = st.columns([1, 1, 1.25], vertical_alignment="bottom")
        c1.number_input(rotulo, min_value=1, max_value=MAX_DIMENSION, step=1, key=_k(clave, "nf"),
                        on_change=_accion, args=(clave, "dimension"))
        c2.number_input("Columnas", min_value=1, max_value=MAX_DIMENSION, step=1, key=_k(clave, "nc"),
                        on_change=_accion, args=(clave, "dimension"))
    else:
        c1, c3 = st.columns([1, 1.2], vertical_alignment="bottom")
        c1.number_input(rotulo, min_value=1, max_value=MAX_DIMENSION, step=1, key=_k(clave, "nf"),
                        on_change=_accion, args=(clave, "dimension", columnas_fijas))
    with c3.popover("⋯ Más", width="stretch"):
        if tipo == MATRIZ:
            st.button("Matriz identidad", key=_k(clave, "identidad"), on_click=_accion,
                      args=(clave, "identidad"), width="stretch",
                      help="Identidad cuadrada del número de filas actual.")
        st.button("Matriz de ceros" if tipo == MATRIZ else "Todo en cero", key=_k(clave, "ceros"),
                  on_click=_accion, args=(clave, "ceros", columnas_fijas), width="stretch")
        st.button("Limpiar (vaciar celdas)", key=_k(clave, "limpiar"), on_click=_accion,
                  args=(clave, "limpiar", columnas_fijas), width="stretch")
        st.button("Restaurar el ejemplo", key=_k(clave, "restaurar"), on_click=_accion,
                  args=(clave, "restaurar", columnas_fijas), width="stretch")
    botones = st.columns(4 if tipo == MATRIZ else 2)
    botones[0].button(f"＋ {unidad.capitalize()}", key=_k(clave, "mas_fila"), on_click=_accion,
                      args=(clave, "mas_fila", columnas_fijas), width="stretch",
                      help=f"Agregar {unidad}")
    botones[1].button(f"－ {unidad.capitalize()}", key=_k(clave, "menos_fila"), on_click=_accion,
                      args=(clave, "menos_fila", columnas_fijas), width="stretch",
                      help=f"Eliminar la última {unidad}" if unidad != "elemento" else "Eliminar el último elemento")
    if tipo == MATRIZ:
        botones[2].button("＋ Columna", key=_k(clave, "mas_col"), on_click=_accion,
                          args=(clave, "mas_col"), width="stretch", help="Agregar columna")
        botones[3].button("－ Columna", key=_k(clave, "menos_col"), on_click=_accion,
                          args=(clave, "menos_col"), width="stretch", help="Eliminar la última columna")


def _rejilla(clave, m, n, tipo, encabezados, etiqueta_fila):
    if encabezados is None:
        encabezados = [f"c{j + 1}" for j in range(n)] if tipo == MATRIZ else [""] * n
    etiqueta_fila = etiqueta_fila or ("F" if tipo == MATRIZ else ("p" if tipo == PUNTOS else ""))
    anchos = [0.45] + [1] * n
    if any(encabezados):
        cabecera = st.columns(anchos)
        for j in range(n):
            cabecera[j + 1].markdown(f'<div class="ed-col">{html.escape(encabezados[j])}</div>',
                                     unsafe_allow_html=True)
    for i in range(m):
        fila = st.columns(anchos, vertical_alignment="center")
        fila[0].markdown(f'<div class="ed-fila">{etiqueta_fila}{i + 1}</div>', unsafe_allow_html=True)
        for j in range(n):
            fila[j + 1].text_input(f"({i + 1}, {j + 1})", key=_celda(clave, i, j), placeholder="·",
                                   label_visibility="collapsed", on_change=_al_editar_celda, args=(clave,))


def problema_dimensiones(A, b, cuadrada=False, x0=None):
    """Comprobación previa (solo para avisar y bloquear el botón): las mismas condiciones
    que después validan el núcleo y la lectura.  Devuelve un mensaje o None."""
    if A is None:
        return None
    m, n = len(A), len(A[0])
    if cuadrada and m != n:
        return f"Este método requiere una matriz cuadrada y A es {m}×{n}."
    if b is not None and len(b) != m:
        return (f"Dimensiones incompatibles: A tiene {m} filas y b tiene {len(b)} componentes; "
                f"b debe tener {m}.")
    if x0 is not None and len(x0) != n:
        return f"El vector inicial x⁽⁰⁾ tiene {len(x0)} componentes y debe tener {n}."
    return None


def aviso_dimensiones(problema):
    """Muestra el problema de dimensiones (si existe) y devuelve True si hay que bloquear."""
    if problema:
        st.error("📐 " + problema + " Corrija las dimensiones para habilitar el cálculo.")
    return bool(problema)
