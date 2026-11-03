"""Identidad visual de la aplicación: hoja de estilos y componentes de presentación.

Solo presentación: aquí no hay ningún cálculo.  Los valores que se muestran
llegan ya calculados desde el núcleo (algebra/).  La paleta coincide con
.streamlit/config.toml y con visualizacion/tema.py.

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
:root{--fondo:#0B1020;--panel:#141C30;--panel2:#18223A;--borde:#26324D;--texto:#E6ECF7;
--suave:#93A1BC;--azul:#4F8CFF;--cian:#22D3EE;--violeta:#A78BFA;--ok:#34D399;--aviso:#FBBF24;--error:#F87171}

/* Fondo: grafito azulado con un halo muy tenue arriba */
[data-testid="stAppViewContainer"]{background:
  radial-gradient(1200px 500px at 70% -10%, rgba(79,140,255,.10), transparent 60%),
  radial-gradient(900px 400px at 0% 0%, rgba(167,139,250,.07), transparent 55%), var(--fondo);}
[data-testid="stHeader"]{background:transparent}
[data-testid="stMainBlockContainer"]{max-width:1240px;padding-top:2.2rem;padding-bottom:4rem}

/* Tipografía y jerarquía */
h1,h2,h3{letter-spacing:-.01em}
h2{font-size:1.45rem !important}
h3{font-size:1.15rem !important;color:var(--texto)}
[data-testid="stCaptionContainer"]{color:var(--suave) !important}
.katex{font-size:1.12em}
.katex-display{margin:.6em 0 !important;overflow-x:auto;overflow-y:hidden;padding:.2em 0}

/* Barra lateral: marca y navegación por módulos */
[data-testid="stSidebar"]{border-right:1px solid #1F2A44}
.marca{display:flex;gap:.7rem;align-items:center;margin:.2rem 0 1.1rem}
.marca-logo{width:42px;height:42px;border-radius:11px;display:grid;place-items:center;
  background:linear-gradient(135deg,#4F8CFF,#22D3EE);color:#06101f;font-weight:800;font-size:1.05rem;
  box-shadow:0 6px 18px rgba(79,140,255,.35)}
.marca-titulo{font-weight:700;font-size:1.02rem;line-height:1.15}
.marca-sub{color:var(--suave);font-size:.78rem}
[data-testid="stSidebar"] [role="radiogroup"]{gap:.3rem !important;flex-direction:column}
[data-testid="stSidebar"] [role="radiogroup"] label{display:flex !important;width:100% !important;
  box-sizing:border-box;padding:.55rem .75rem !important;border-radius:10px;min-height:0 !important;
  border:1px solid transparent;transition:background .15s,border-color .15s;margin:0 !important}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(79,140,255,.08);border-color:#26324D}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){
  background:linear-gradient(90deg,rgba(79,140,255,.22),rgba(34,211,238,.06));border-color:rgba(79,140,255,.55);
  box-shadow:inset 3px 0 0 var(--cian)}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-size:.93rem}
.lateral-bloque{border:1px solid #1F2A44;background:rgba(20,28,48,.6);border-radius:12px;padding:.7rem .8rem;
  font-size:.8rem;color:var(--suave);margin-top:.4rem;line-height:1.45}
.lateral-bloque b{color:var(--texto)}

/* Portada */
.st-key-hero_portada,.hero{border:1px solid var(--borde);border-radius:18px;padding:1.7rem 1.9rem;margin-bottom:1.4rem;
  background:linear-gradient(135deg,rgba(79,140,255,.16),rgba(167,139,250,.08) 55%,rgba(20,28,48,.6));
  box-shadow:0 18px 50px rgba(0,0,0,.35)}
.hero-eyebrow{color:var(--cian);font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.hero h1,.st-key-hero_portada h1{font-size:2.3rem !important;margin:.1rem 0 .2rem;padding:0 !important;line-height:1.15}
.hero p,.hero-texto{color:#C9D3E6;margin:.2rem 0 .5rem;max-width:860px;font-size:1.02rem}
.rejilla{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:.9rem;margin:.6rem 0 1rem}
.tarjeta{border:1px solid var(--borde);border-radius:14px;background:rgba(20,28,48,.75);padding:1rem 1.1rem;
  height:100%;transition:border-color .15s,transform .15s}
.tarjeta:hover{border-color:rgba(79,140,255,.6)}
.tarjeta .num{font-size:.75rem;font-weight:700;color:var(--cian);letter-spacing:.12em}
.tarjeta h4{margin:.2rem 0 .35rem;font-size:1.05rem;padding:0}
.tarjeta p,.tarjeta li{color:#C3CDE0;font-size:.88rem;margin:.15rem 0}
.tarjeta ul{padding-left:1.05rem;margin:.3rem 0 0}
.tarjeta .donde{margin-top:.55rem;font-size:.8rem;color:var(--suave)}
.tarjeta .donde b{color:var(--texto)}

/* Cabecera de módulo */
.cabecera{display:flex;gap:1.1rem;align-items:flex-start;border:1px solid var(--borde);border-radius:16px;
  padding:1.15rem 1.3rem;margin-bottom:1.2rem;
  background:linear-gradient(120deg,rgba(79,140,255,.13),rgba(20,28,48,.55) 60%)}
.cabecera-num{min-width:56px;height:56px;border-radius:14px;display:grid;place-items:center;font-weight:800;
  font-size:1.35rem;color:#06101f;background:linear-gradient(135deg,#4F8CFF,#22D3EE)}
.cabecera h1{font-size:1.6rem;margin:0;padding:0;line-height:1.2}
.cabecera p{margin:.3rem 0 .5rem;color:#C9D3E6}

/* Rótulos de sección */
.seccion{display:flex;align-items:center;gap:.6rem;margin:1.5rem 0 .55rem}
.seccion-paso{font-size:.72rem;font-weight:800;letter-spacing:.12em;color:#06101f;background:var(--cian);
  border-radius:6px;padding:.1rem .45rem}
.seccion-titulo{font-weight:700;font-size:1.05rem}
.seccion-ayuda{color:var(--suave);font-size:.85rem}
.seccion::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--borde),transparent)}

/* Chips de estado */
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.2rem 0 .3rem}
.chip{display:inline-flex;align-items:center;gap:.3rem;border-radius:999px;padding:.16rem .65rem;font-size:.78rem;
  font-weight:600;border:1px solid var(--borde);background:rgba(24,34,58,.9);color:#C9D3E6}
.chip-ok{color:#6EE7B7;border-color:rgba(52,211,153,.45);background:rgba(52,211,153,.10)}
.chip-aviso{color:#FCD34D;border-color:rgba(251,191,36,.45);background:rgba(251,191,36,.10)}
.chip-error{color:#FCA5A5;border-color:rgba(248,113,113,.45);background:rgba(248,113,113,.10)}
.chip-info{color:#93C5FD;border-color:rgba(79,140,255,.45);background:rgba(79,140,255,.10)}
.chip-incentivo{color:#DDD6FE;border-color:rgba(167,139,250,.5);background:rgba(167,139,250,.12)}

/* Tarjeta del resultado principal (contenedores con clave res_...) */
div[class*="st-key-res_"]{border:1px solid rgba(79,140,255,.45) !important;border-radius:16px !important;
  background:linear-gradient(160deg,rgba(79,140,255,.10),rgba(20,28,48,.85) 45%) !important;
  box-shadow:0 12px 34px rgba(0,0,0,.30);padding:.4rem .5rem}
div[class*="st-key-res_"] .katex-display .katex{font-size:1.45em}
.valor-titulo{color:var(--suave);font-size:.85rem;font-weight:700;letter-spacing:.02em}
.valor-grande{font-size:2.05rem;font-weight:750;line-height:1.15;margin:.15rem 0;
  background:linear-gradient(90deg,#E6ECF7,#9CC2FF);-webkit-background-clip:text;background-clip:text;color:transparent}
.valor-detalle{color:#C3CDE0;font-size:.9rem}

/* Métricas como tarjetas */
[data-testid="stMetric"]{background:rgba(20,28,48,.8);border:1px solid var(--borde);border-radius:12px;
  padding:.7rem .9rem}
[data-testid="stMetricLabel"] p{color:var(--suave) !important;font-size:.82rem !important}
[data-testid="stMetricValue"]{font-size:1.55rem !important;color:var(--texto)}
/* Nunca truncar un valor numérico con «…»: si no cabe, pasa a la línea siguiente */
[data-testid="stMetricValue"] *,[data-testid="stMetricLabel"] *{white-space:normal !important;
  overflow:visible !important;text-overflow:clip !important;overflow-wrap:anywhere}
@media (max-width: 1280px){[data-testid="stMetricValue"]{font-size:1.2rem !important}}

/* Pestañas como selector segmentado */
[data-baseweb="tab-list"]{gap:.35rem;flex-wrap:wrap;border-bottom:1px solid var(--borde)}
[data-baseweb="tab"]{border-radius:10px 10px 0 0;padding:.5rem .9rem !important}
[data-baseweb="tab"][aria-selected="true"]{background:rgba(79,140,255,.14)}
[data-baseweb="tab"] p{font-size:.92rem !important;font-weight:600}

/* Botones */
.stButton>button[kind="primary"],.stDownloadButton>button{border:none;font-weight:650;
  background:linear-gradient(135deg,#4F8CFF,#3B6FE0);box-shadow:0 6px 18px rgba(79,140,255,.28)}
.stButton>button[kind="primary"]:hover{filter:brightness(1.08)}
.stButton>button[kind="secondary"]{font-weight:600}

/* Expansores, tablas y avisos */
[data-testid="stExpander"] details{border-radius:12px !important;background:rgba(20,28,48,.55)}
[data-testid="stExpander"] summary p{font-weight:600}
[data-testid="stTable"] table{font-size:.9rem}
[data-testid="stTable"] th{background:#18223A !important;color:#C9D3E6 !important}
[data-testid="stAlert"]{border-radius:12px}
textarea{font-family:'Cascadia Code','Consolas',monospace !important;font-size:.92rem !important}

/* Escala del número de condición */
.escala{margin:.6rem 0 .2rem}
.escala-barra{position:relative;height:12px;border-radius:999px;
  background:linear-gradient(90deg,#34D399 0%,#34D399 33.3%,#FBBF24 33.3%,#FBBF24 66.6%,#F87171 66.6%,#F87171 100%);
  opacity:.85}
.escala-marca{position:absolute;top:-6px;width:4px;height:24px;border-radius:3px;background:#fff;
  box-shadow:0 0 0 3px rgba(11,16,32,.85)}
.escala-rotulos{display:flex;justify-content:space-between;color:var(--suave);font-size:.75rem;margin-top:.35rem}

/* Editor interactivo de matrices (interfaz/editor.py) */
div[class*="st-key-editor_"]{border:1px solid var(--borde);border-radius:14px;padding:.55rem .7rem .85rem;
  background:linear-gradient(180deg,rgba(24,34,58,.85),rgba(16,23,41,.85))}
.ed-titulo{font-weight:700;font-size:.95rem;color:var(--texto);margin:.1rem 0 .1rem}
.ed-col{text-align:center;color:var(--cian);font-size:.75rem;font-weight:700;letter-spacing:.06em}
.ed-fila{text-align:right;color:var(--suave);font-size:.78rem;font-weight:700;padding-right:.15rem;
  transform:translateY(-.5rem)}
div[class*="st-key-editor_"] [data-testid="stTextInput"] input{text-align:center;
  font-family:'Cascadia Code','Consolas',monospace;font-size:1.02rem;font-weight:600;padding:.45rem .2rem;
  min-height:2.45rem;color:#F1F5FF;background:#0E1528}
div[class*="st-key-editor_"] [data-testid="stTextInput"] input:focus{background:#13203A}
div[class*="st-key-editor_"] [data-testid="stHorizontalBlock"]{gap:.35rem !important}
div[class*="st-key-editor_"] .stButton>button{padding:.2rem .4rem;min-height:2.1rem;font-size:.85rem}
div[class*="st-key-editor_"] [data-baseweb="tab"]{padding:.3rem .7rem !important}
div[class*="st-key-editor_"] [data-baseweb="tab"] p{font-size:.85rem !important}

@media (max-width: 900px){
  .hero{padding:1.2rem}.hero h1{font-size:1.6rem}
  .cabecera{flex-direction:column;gap:.6rem}.cabecera h1{font-size:1.3rem}
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
        f'<div class="cabecera"><div class="cabecera-num">{_e(numero)}</div><div>'
        f'<h1>{_e(titulo)}</h1><p>{descripcion}</p>{insignias_html(etiquetas)}</div></div>',
        unsafe_allow_html=True)


def seccion(paso, titulo, ayuda=""):
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


def bloque_lateral(html_contenido):
    st.sidebar.markdown(f'<div class="lateral-bloque">{html_contenido}</div>', unsafe_allow_html=True)
