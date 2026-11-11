"""Identidad visual de la aplicación: sistema de diseño y componentes de presentación.

Solo presentación: aquí no hay ningún cálculo.  Los valores que se muestran
llegan ya calculados desde el núcleo (algebra/).  La paleta coincide con
.streamlit/config.toml y con visualizacion/tema.py.

Todo el estilo de la aplicación está en este archivo (una sola hoja, CSS):
  1. Tokens: colores, tipografías, radios y duraciones (variables en :root)
  2. Estructura: barra superior de navegación, ancho del contenido
  3. Tipografía y fórmulas
  4. Portada (interfaz/portada.py)
  5. Cabecera de módulo, rótulos de sección, chips
  6. Resultado principal, métricas, escala de κ
  7. Controles: botones, enlaces, pestañas, campos, expansores
  8. Editor de matrices (interfaz/compartido/editor.py)
  9. Movimiento (120-220 ms, una sola vez) y prefers-reduced-motion
 10. Anchos intermedios (1024-1366 px)

Las animaciones solo usan opacity y transform y se reproducen cuando un elemento
aparece por primera vez (resultado nuevo, cambio de página o de pestaña), no en
cada ejecución de Streamlit: los elementos que ya están en pantalla se conservan.

Componentes:
  aplicar_estilo()       inyecta la hoja de estilos (una vez por ejecución)
  encabezado_modulo()    cabecera de cada módulo (número, título, descripción, etiquetas)
  seccion()              rótulo numerado de cada etapa: datos, configuración, resultados
  tarjeta_resultado()    contenedor destacado para el resultado principal
  valor_destacado()      título, valor grande y detalle dentro de una tarjeta
  insignias()            «chips» de estado (converge, singular, exacto, ...)
  escala_kappa()         barra de la escala del proyecto (κ < 10, < 100, ≥ 100)
  marca_incentivo()      indica qué funcionalidad real corresponde a un incentivo
  procedencia()          categorías A/B/C/D: de dónde sale cada procedimiento
"""

import html
import math
import pathlib

import streamlit as st

COLORES = {
    "fondo": "#0B1020", "panel": "#141C30", "panel2": "#18223A", "borde": "#26324D",
    "texto": "#E6ECF7", "suave": "#93A1BC", "azul": "#4F8CFF", "cian": "#22D3EE",
    "violeta": "#A78BFA", "ok": "#34D399", "aviso": "#FBBF24", "error": "#F87171",
}

# Hoja de estilos: interfaz/recursos/estilo.css (tokens, barra superior, portada,
# chips, métricas, editor de matrices y animaciones).
CSS = (pathlib.Path(__file__).resolve().parent.parent / "recursos" / "estilo.css").read_text(encoding="utf-8")


def aplicar_estilo():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


_ETIQUETAS_MATEMATICAS = {f"&lt;{e}&gt;": f"<{e}>" for e in ("sub", "/sub", "sup", "/sup")}


def _e(texto):
    """Escapa el texto, pero deja pasar <sub> y <sup> (subíndices y superíndices: T<sub>J</sub>,
    κ<sub>∞</sub>).  Ninguna otra etiqueta HTML sobrevive."""
    seguro = html.escape(str(texto), quote=False)
    for escapada, etiqueta in _ETIQUETAS_MATEMATICAS.items():
        seguro = seguro.replace(escapada, etiqueta)
    return seguro


def insignias_html(lista):
    """lista de (texto, tipo) con tipo en ok, aviso, error, info, incentivo o ''."""
    partes = "".join(f'<span class="chip chip-{t}">{_e(x)}</span>' if t else f'<span class="chip">{_e(x)}</span>'
                     for x, t in lista)
    return f'<div class="chips">{partes}</div>'


def insignias(lista):
    st.markdown(insignias_html(lista), unsafe_allow_html=True)


def encabezado_modulo(numero, titulo, descripcion, etiquetas=()):
    st.markdown(
        f'<div class="cabecera"><div class="cabecera-num">MÓDULO {_e(numero)}</div>'
        f'<h1>{_e(titulo)}</h1><p>{descripcion}</p>{insignias_html(etiquetas)}</div>',
        unsafe_allow_html=True)


def seccion(paso, titulo, ayuda=""):
    paso = str(paso).zfill(2) if str(paso).isdigit() else paso
    extra = f'<span class="seccion-ayuda">{_e(ayuda)}</span>' if ayuda else ""
    st.markdown(f'<div class="seccion"><span class="seccion-paso">{_e(paso)}</span>'
                f'<span class="seccion-titulo">{_e(titulo)}</span>{extra}</div>',
                unsafe_allow_html=True)


def tarjeta_resultado(clave):
    """Contenedor destacado; el CSS lo reconoce por la clave res_<clave>."""
    return st.container(border=True, key=f"res_{clave}")


def valor_destacado(titulo, valor, detalle=""):
    st.markdown(f'<div class="valor-titulo">{_e(titulo)}</div><div class="valor-grande">{_e(valor)}</div>'
                + (f'<div class="valor-detalle">{_e(detalle)}</div>' if detalle else ""),
                unsafe_allow_html=True)


def escala_kappa(kappa):
    """Barra de la escala operativa del proyecto (10 y 100); la posición usa log10(κ)
    entre 1 y 1000 (κ ≥ 1000 se dibuja en el extremo).  Solo visual: la clasificación
    la decide algebra.condicion.clasificar_kappa."""
    valor = float(kappa)
    posicion = 0.0 if valor <= 1 else min(1.0, math.log10(valor) / 3)
    st.markdown(
        f'<div class="escala"><div class="escala-barra"><div class="escala-marca" '
        f'style="left:calc({posicion * 100:.1f}% - 2px)"></div></div>'
        f'<div class="escala-rotulos"><span>1 · baja</span><span>10 · moderada</span>'
        f'<span>100 · alta</span><span>≥ 1000</span></div></div>', unsafe_allow_html=True)


def marca_incentivo(nombre, maximo):
    """Indica junto a una funcionalidad real a qué incentivo de la rúbrica corresponde."""
    insignias([(f"Incentivo · {nombre} (hasta {maximo})", "incentivo")])


# Categorías de procedencia (docs/auditoria_textos_profesora.md, sección 3).
PROCEDENCIA = {
    "A": ("Visto en clase", "ok"),
    "B": ("Exigido por el enunciado", "info"),
    "C": ("Extensión o incentivo", "incentivo"),
    "D": ("Sin respaldo en el material", "aviso"),
}
LEYENDA_PROCEDENCIA = " · ".join(f"Cat. {k}: {v[0].lower()}" for k, v in PROCEDENCIA.items())


def procedencia(lista):
    """lista de (categoría, procedimiento, fuente).  Cada chip muestra la categoría y el
    procedimiento; al pasar el cursor se ve la categoría completa y la fuente."""
    partes = []
    for categoria, texto, fuente in lista:
        nombre, tipo = PROCEDENCIA[categoria]
        partes.append(f'<span class="chip chip-{tipo}" title="{html.escape(f"{nombre} — {fuente}")}">'
                      f'Cat. {_e(categoria)} · {_e(texto)}</span>')
    st.markdown(f'<div class="procedencia" title="{html.escape(LEYENDA_PROCEDENCIA)}">'
                f'<span>Procedencia:</span>{"".join(partes)}</div>', unsafe_allow_html=True)
