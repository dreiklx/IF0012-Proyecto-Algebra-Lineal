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
  8. Editor de matrices (interfaz/editor.py)
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
"""

import html
import math

import streamlit as st

COLORES = {
    "fondo": "#0B1020", "panel": "#141C30", "panel2": "#18223A", "borde": "#26324D",
    "texto": "#E6ECF7", "suave": "#93A1BC", "azul": "#4F8CFF", "cian": "#22D3EE",
    "violeta": "#A78BFA", "ok": "#34D399", "aviso": "#FBBF24", "error": "#F87171",
}

CSS = """
/* 1. Tokens ---------------------------------------------------------------- */
:root{
  --fondo:#0B1020;--barra:#0D1326;--panel:#141C30;--panel2:#18223A;--campo:#0E1528;
  --borde:#26324D;--regla:#1C2640;--texto:#E6ECF7;--claro:#C9D3E6;--suave:#93A1BC;--tenue:#6B7894;
  --azul:#4F8CFF;--cian:#22D3EE;--violeta:#A78BFA;--ok:#34D399;--aviso:#FBBF24;--error:#F87171;
  --f-titulo:"Bahnschrift","Segoe UI Variable Display","Segoe UI",system-ui,sans-serif;
  --f-mono:"Cascadia Code","Cascadia Mono","Consolas","SFMono-Regular",monospace;
  --r-s:6px;--r-m:10px;--r-l:14px;
  --t-rapida:140ms;--t-media:200ms;--t-larga:220ms;--curva:cubic-bezier(.2,.7,.2,1);
}

/* 2. Estructura: barra superior y ancho del contenido ---------------------- */
[data-testid="stAppViewContainer"]{background:var(--fondo)}
[data-testid="stHeader"]{background:var(--barra);border-bottom:1px solid var(--regla);height:3.6rem}
[data-testid="stToolbar"]{height:3.6rem}
[data-testid="stHeaderLogo"]{height:2.25rem !important;max-width:none !important;width:auto}
[data-testid="stTopNav"]{gap:.15rem;margin-left:1.2rem}
[data-testid="stTopNavLink"]{position:relative;padding:.45rem .8rem !important;border-radius:var(--r-s);
  background:transparent !important;transition:background-color var(--t-rapida) var(--curva)}
[data-testid="stTopNavLink"] p{color:var(--suave);font-size:.9rem;font-weight:550;
  transition:color var(--t-rapida) var(--curva)}
[data-testid="stTopNavLink"]::after{content:"";position:absolute;left:.8rem;right:.8rem;bottom:.12rem;height:2px;
  border-radius:2px;background:var(--cian);transform:scaleX(0);transition:transform var(--t-media) var(--curva)}
[data-testid="stTopNavLink"]:hover{background:rgba(147,161,188,.08) !important}
[data-testid="stTopNavLink"]:hover p{color:var(--texto)}
[data-testid="stTopNavLink"][aria-current="page"] p{color:var(--texto);font-weight:650}
[data-testid="stTopNavLink"][aria-current="page"]::after{transform:scaleX(1)}
[data-testid="stTopNavLink"]:focus-visible{outline:2px solid var(--cian);outline-offset:2px}
[data-testid="stMainBlockContainer"]{max-width:1320px;padding:5.2rem 2.5rem 4rem}

/* 3. Tipografía y fórmulas ------------------------------------------------- */
h1,h2,h3,h4{font-family:var(--f-titulo) !important;letter-spacing:-.012em}
h2{font-size:1.4rem !important}
h3{font-size:1.15rem !important;color:var(--texto)}
[data-testid="stCaptionContainer"]{color:var(--suave) !important}
[data-testid="stMarkdownContainer"] code{font-family:var(--f-mono)}
.katex{font-size:1.12em}
.katex-display{margin:.9em 0 !important;padding:.35em 0;overflow-x:auto;overflow-y:hidden}
[data-testid="stMetricValue"],[data-testid="stTable"] td,[data-testid="stDataFrame"]{font-variant-numeric:tabular-nums}
textarea{font-family:var(--f-mono) !important;font-size:.92rem !important}

/* 4. Portada --------------------------------------------------------------- */
.st-key-portada_hero{padding:.4rem 0 2.2rem;border-bottom:1px solid var(--regla);margin-bottom:.4rem}
.eyebrow{font-family:var(--f-mono);color:var(--cian);font-size:.76rem;letter-spacing:.06em}
.st-key-portada_hero h1{font-size:clamp(2.3rem,3.4vw,3.3rem) !important;font-weight:700;line-height:1.05;
  letter-spacing:-.025em;padding:.35rem 0 .2rem !important}
.lede{color:var(--claro);font-size:1.08rem;line-height:1.6;max-width:36em;margin:.4rem 0 1.4rem}
.hechos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:0}
.hechos div{border-left:1px solid var(--borde);padding-left:.8rem}
.hechos dt{font-family:var(--f-mono);font-size:.7rem;color:var(--suave);letter-spacing:.06em}
.hechos dd{margin:.15rem 0 0;font-size:.86rem;color:var(--texto);line-height:1.35}

.fm{margin:0;padding:1.6rem 1.4rem 1.2rem;border:1px solid var(--regla);border-radius:var(--r-l);
  background-color:#0D1427;
  background-image:linear-gradient(rgba(147,161,188,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(147,161,188,.055) 1px,transparent 1px);
  background-size:24px 24px;background-position:-1px -1px}
.fm-fila{display:flex;align-items:center;justify-content:center;gap:.9rem;flex-wrap:wrap}
.fm-matriz{position:relative;display:grid;column-gap:1.05rem;row-gap:.3rem;padding:.45rem .75rem;
  font-family:var(--f-mono);font-size:1.02rem;font-variant-numeric:tabular-nums;color:var(--claro)}
.fm-matriz::before,.fm-matriz::after{content:"";position:absolute;top:0;bottom:0;width:.4rem;
  border:1.5px solid var(--suave)}
.fm-matriz::before{left:0;border-right:none}
.fm-matriz::after{right:0;border-left:none}
.fm-c{text-align:right;min-width:1.6ch}
.fm-c.b{border-left:1px dashed var(--tenue);padding-left:.85rem}
.fm-matriz.final .fm-c{color:var(--tenue)}
.fm-matriz.final .fm-c.d{color:var(--texto)}
.fm-matriz.final .fm-c.b{color:var(--cian);font-weight:650}
.fm-flecha{display:flex;flex-direction:column;align-items:center;color:var(--suave);font-size:1.5rem;line-height:1}
.fm-flecha span{font-family:var(--f-mono);font-size:.66rem;letter-spacing:.05em;margin-bottom:.25rem}
.fm figcaption{display:flex;flex-direction:column;align-items:center;gap:.2rem;margin-top:1.1rem;text-align:center;
  font-size:.8rem;color:var(--suave)}
.fm-x{font-family:var(--f-mono);font-size:1rem;color:var(--cian)}
.fm-fuente{color:var(--tenue);font-size:.74rem}

h2.rotulo{font-size:1.2rem !important;margin:2.2rem 0 .9rem;padding:0 !important;font-weight:650}
h2.rotulo .rotulo-nota{font-family:var(--f-mono);font-size:.72rem;font-weight:400;color:var(--suave);
  letter-spacing:.03em;margin-left:.7rem}
.st-key-portada_modulos [data-testid="stColumn"]>[data-testid="stVerticalBlock"]{height:100%}
.st-key-portada_modulos [data-testid="stElementContainer"]:has([data-testid="stPageLink"]){margin-top:auto}
.mod{border-top:2px solid var(--borde);padding-top:.85rem;transition:border-color var(--t-media) var(--curva)}
.st-key-portada_modulos [data-testid="stColumn"]:hover .mod{border-top-color:var(--cian)}
.mod-num{font-family:var(--f-titulo);font-size:2rem;font-weight:300;color:var(--cian);line-height:1}
.mod h3{font-size:1.04rem !important;margin:.45rem 0 .35rem;padding:0 !important;line-height:1.25}
.mod p{color:var(--claro);font-size:.87rem;line-height:1.5;margin:0 0 .55rem}
.mod-claves{font-family:var(--f-mono);font-size:.7rem;color:var(--tenue);margin-bottom:.2rem}
.st-key-portada_incentivos [data-testid="stHorizontalBlock"]{border-top:1px solid var(--regla);padding:.75rem 0}
.st-key-portada_incentivos{border-bottom:1px solid var(--regla);gap:0 !important}
.inc-nombre{font-weight:650;font-size:.95rem}
.inc-max{font-family:var(--f-mono);font-size:.74rem;color:var(--violeta);margin-top:.1rem}
.inc-desc{color:var(--claro);font-size:.87rem;line-height:1.5}
.inc-donde{color:var(--suave);font-size:.78rem;margin-top:.2rem}
.nota{border-left:2px solid var(--azul);padding:.15rem 0 .15rem 1rem;color:var(--claro);font-size:.93rem;
  line-height:1.6;margin-bottom:.8rem}
.nota b{color:var(--texto)}
.pie{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;margin-top:3rem;padding-top:1rem;border-top:1px solid var(--regla);
  font-size:.78rem;color:var(--suave)}
.pie b{color:var(--claro)}

/* 5. Cabecera de módulo, secciones y chips --------------------------------- */
.cabecera{padding:.6rem 0 1.2rem;margin-bottom:.6rem;border-bottom:1px solid var(--regla)}
.cabecera-num{display:flex;align-items:center;gap:.6rem;font-family:var(--f-mono);font-size:.76rem;
  color:var(--cian);letter-spacing:.08em}
.cabecera-num::after{content:"";width:2.2rem;height:1px;background:var(--cian);opacity:.6}
.cabecera h1{font-size:clamp(1.75rem,2.4vw,2.25rem) !important;font-weight:700;margin:.3rem 0 0;padding:0 !important;
  line-height:1.15;letter-spacing:-.02em}
.cabecera p{margin:.45rem 0 .65rem;color:var(--claro);max-width:52em;line-height:1.55}

.seccion{display:flex;align-items:baseline;gap:.7rem;margin:1.9rem 0 .7rem}
.seccion-paso{font-family:var(--f-mono);font-size:.8rem;color:var(--cian)}
.seccion-titulo{font-family:var(--f-titulo);font-weight:650;font-size:1.12rem}
.seccion-ayuda{color:var(--suave);font-size:.84rem}
.seccion::after{content:"";flex:1;height:1px;background:var(--regla);align-self:center}

.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.2rem 0 .3rem}
.chip{display:inline-flex;align-items:center;gap:.3rem;border-radius:999px;padding:.14rem .6rem;font-size:.77rem;
  font-weight:600;border:1px solid var(--borde);background:var(--panel);color:var(--claro);
  transition:color var(--t-rapida),border-color var(--t-rapida),background-color var(--t-rapida)}
.chip-ok{color:#6EE7B7;border-color:rgba(52,211,153,.4);background:rgba(52,211,153,.08)}
.chip-aviso{color:#FCD34D;border-color:rgba(251,191,36,.4);background:rgba(251,191,36,.08)}
.chip-error{color:#FCA5A5;border-color:rgba(248,113,113,.4);background:rgba(248,113,113,.08)}
.chip-info{color:#93C5FD;border-color:rgba(79,140,255,.4);background:rgba(79,140,255,.08)}
.chip-incentivo{color:#DDD6FE;border-color:rgba(167,139,250,.45);background:rgba(167,139,250,.09)}

/* 6. Resultado principal, métricas y escala de κ --------------------------- */
div[class*="st-key-res_"]{border:1px solid rgba(34,211,238,.32) !important;border-radius:var(--r-l) !important;
  background:var(--panel) !important;box-shadow:inset 3px 0 0 var(--cian);padding:.5rem .6rem .5rem .8rem}
div[class*="st-key-res_"] .katex-display .katex{font-size:1.45em}
.valor-titulo{color:var(--suave);font-size:.84rem;font-weight:650}
.valor-grande{font-family:var(--f-titulo);font-size:2.1rem;font-weight:700;line-height:1.15;margin:.15rem 0;
  color:var(--texto);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.valor-detalle{color:var(--claro);font-size:.9rem}

[data-testid="stMetric"]{background:none;border:none;border-left:1px solid var(--borde);border-radius:0;
  padding:.15rem 0 .15rem .9rem}
[data-testid="stMetricLabel"] p{color:var(--suave) !important;font-size:.8rem !important}
[data-testid="stMetricValue"]{font-family:var(--f-titulo);font-size:1.55rem !important;color:var(--texto)}
/* Nunca truncar un valor numérico con «…»: si no cabe, pasa a la línea siguiente */
[data-testid="stMetricValue"] *,[data-testid="stMetricLabel"] *{white-space:normal !important;
  overflow:visible !important;text-overflow:clip !important;overflow-wrap:anywhere}

.escala{margin:.6rem 0 .2rem}
.escala-barra{position:relative;height:10px;border-radius:999px;
  background:linear-gradient(90deg,#34D399 0%,#34D399 33.3%,#FBBF24 33.3%,#FBBF24 66.6%,#F87171 66.6%,#F87171 100%);
  opacity:.85}
.escala-marca{position:absolute;top:-6px;width:4px;height:22px;border-radius:3px;background:#fff;
  box-shadow:0 0 0 3px rgba(11,16,32,.85)}
.escala-rotulos{display:flex;justify-content:space-between;color:var(--suave);font-size:.75rem;margin-top:.35rem}

/* 7. Controles ------------------------------------------------------------- */
.stButton>button,.stDownloadButton>button,[data-testid="stPopover"] button{font-weight:600;
  transition:background-color var(--t-rapida) var(--curva),border-color var(--t-rapida) var(--curva),
             color var(--t-rapida) var(--curva),transform var(--t-rapida) var(--curva)}
.stButton>button[kind="primary"],.stDownloadButton>button{border:1px solid transparent;background:var(--azul);color:#fff}
.stButton>button[kind="primary"]:hover,.stDownloadButton>button:hover{background:#6A9DFF;color:#fff}
.stButton>button:hover:not(:disabled){transform:translateY(-1px)}
.stButton>button:active:not(:disabled){transform:translateY(0)}

[data-testid="stPageLink-NavLink"]{border:1px solid var(--borde);border-radius:var(--r-s);padding:.3rem .7rem !important;
  background:transparent;transition:background-color var(--t-rapida) var(--curva),border-color var(--t-rapida) var(--curva)}
[data-testid="stPageLink-NavLink"] p{color:var(--cian) !important;font-size:.85rem;font-weight:600}
[data-testid="stPageLink-NavLink"]:hover{background:rgba(34,211,238,.08) !important;border-color:rgba(34,211,238,.5)}

/* Pestañas (react-aria en Streamlit 1.66): el indicador inferior se desliza al cambiar */
[data-testid="stTabs"] [role="tablist"]{gap:.2rem;flex-wrap:wrap;border-bottom:1px solid var(--borde)}
[data-testid="stTab"]{padding:.55rem .9rem !important;border-radius:var(--r-s) var(--r-s) 0 0;
  transition:background-color var(--t-rapida) var(--curva)}
[data-testid="stTab"] p{font-size:.92rem !important;font-weight:600;color:var(--suave);transition:color var(--t-rapida)}
[data-testid="stTab"]:hover{background:rgba(147,161,188,.07)}
[data-testid="stTab"][data-selected="true"] p{color:var(--texto)}
[data-testid="stTab"] .react-aria-SelectionIndicator{background:var(--cian) !important;
  transition:translate var(--t-media) var(--curva),width var(--t-media) var(--curva)}

[data-baseweb="input"],[data-baseweb="select"]>div,[data-baseweb="textarea"]{
  transition:border-color var(--t-rapida) var(--curva),background-color var(--t-rapida) var(--curva)}
[data-testid="stRadio"] label,[data-testid="stCheckbox"] label{transition:color var(--t-rapida)}

[data-testid="stExpander"] details{border-radius:var(--r-m) !important;background:rgba(20,28,48,.45);
  border-color:var(--regla) !important}
[data-testid="stExpander"] summary{transition:background-color var(--t-rapida)}
[data-testid="stExpander"] summary:hover{background:rgba(147,161,188,.06)}
[data-testid="stExpander"] summary p{font-weight:600}
[data-testid="stTable"] table{font-size:.9rem}
[data-testid="stTable"] th{background:var(--panel2) !important;color:var(--claro) !important}
[data-testid="stAlert"]{border-radius:var(--r-m)}
[data-testid="stPlotlyChart"]{border-top:1px solid var(--regla);padding-top:.4rem}

/* 8. Editor de matrices (interfaz/editor.py) ------------------------------- */
div[class*="st-key-editor_"]{border:1px solid var(--borde);border-radius:var(--r-l);padding:.55rem .75rem .85rem;
  background:#111830;transition:border-color var(--t-media) var(--curva)}
div[class*="st-key-editor_"]:focus-within{border-color:#34446A}
.ed-titulo{font-family:var(--f-titulo);font-weight:650;font-size:.98rem;color:var(--texto);margin:.1rem 0}
.ed-col{text-align:center;font-family:var(--f-mono);color:var(--cian);font-size:.74rem;letter-spacing:.04em}
.ed-fila{text-align:right;font-family:var(--f-mono);color:var(--suave);font-size:.76rem;padding-right:.15rem;
  transform:translateY(-.5rem)}
div[class*="st-key-editor_"] [data-testid="stTextInput"] input{text-align:center;
  font-family:var(--f-mono);font-size:1.02rem;font-weight:600;padding:.45rem .2rem;font-variant-numeric:tabular-nums;
  min-height:2.45rem;color:#F1F5FF;background:var(--campo);transition:background-color var(--t-rapida)}
div[class*="st-key-editor_"] [data-testid="stTextInput"] input:focus{background:#13203A}
div[class*="st-key-editor_"] [data-testid="stHorizontalBlock"]{gap:.35rem !important}
div[class*="st-key-editor_"] .stButton>button{padding:.2rem .4rem;min-height:2.1rem;font-size:.85rem}
div[class*="st-key-editor_"] [data-testid="stTab"]{padding:.3rem .7rem !important}
div[class*="st-key-editor_"] [data-testid="stTab"] p{font-size:.85rem !important}
/* marca invisible que el editor agrega solo en la ejecución en que se cargó un ejemplo */
[data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] .ed-marca){display:none}
div[class*="st-key-editor_"]:has(.ed-cargado){animation:ax-carga var(--t-larga) var(--curva)}

/* 9. Movimiento ------------------------------------------------------------ */
@keyframes ax-entrada{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes ax-fundido{from{opacity:0}to{opacity:1}}
@keyframes ax-carga{from{border-color:var(--cian);transform:scale(.996)}to{transform:none}}
div[class*="st-key-res_"]{animation:ax-entrada var(--t-larga) var(--curva) both}
.cabecera,.st-key-portada_hero{animation:ax-entrada var(--t-media) var(--curva) both}
[data-testid="stTabPanel"]:not([inert]){animation:ax-fundido var(--t-media) var(--curva)}
.fm-matriz.final,.fm figcaption{animation:ax-fundido var(--t-larga) var(--curva) 120ms both}
@media (prefers-reduced-motion: reduce){
  :root{--t-rapida:0ms;--t-media:0ms;--t-larga:0ms}
  .fm-matriz.final,.fm figcaption{animation-delay:0ms}
  .stButton>button:hover:not(:disabled){transform:none}
}

/* 10. Anchos intermedios --------------------------------------------------- */
@media (max-width: 1280px){
  [data-testid="stMainBlockContainer"]{padding-left:2rem;padding-right:2rem}
  [data-testid="stMetricValue"]{font-size:1.2rem !important}
  [data-testid="stTopNavLink"]{padding:.45rem .55rem !important}
  [data-testid="stTopNavLink"]::after{left:.55rem;right:.55rem}
  [data-testid="stTopNavLink"] p{font-size:.86rem}
}
@media (max-width: 1100px){
  .hechos{grid-template-columns:1fr;gap:.55rem}
  .fm-matriz{column-gap:.8rem;font-size:.95rem}
}
@media (max-width: 900px){
  .valor-grande{font-size:1.6rem}
}
"""


def aplicar_estilo():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def _e(texto):
    return html.escape(str(texto), quote=False)


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
