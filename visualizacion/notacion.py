"""Notación matemática: cómo se escribe cada símbolo según dónde se muestra.

Solo presentación.  Cada parte de la interfaz renderiza la matemática de forma
distinta (comprobado en Brave con Streamlit 1.66 y Plotly 6.3):

| Dónde se muestra                                               | Formato        |
|----------------------------------------------------------------|----------------|
| st.markdown, st.caption, avisos (info/success/warning/error),  | LaTeX ($d_k$)  |
| etiquetas de métricas y widgets, opciones de st.radio,         |                |
| pestañas, expanders y encabezados de st.table                  |                |
| Plotly (títulos, ejes, leyendas, anotaciones, cursor)          | HTML (d<sub>k</sub>); Plotly no carga MathJax |
| st.dataframe (encabezados), opciones de st.selectbox,          | Unicode (dₖ)   |
| componentes HTML propios de Ax que escapan el texto            |                |

Por eso cada símbolo tiene sus tres formas.  La notación sigue a la profesora
(docs/referencia_oficial_procedimientos.md §2): x⁽ᵏ⁾, T_J, T_GS, ρ(T) = máx|λ|,
κ(A) = ‖A‖‖A⁻¹‖, Fᵢ para las filas, aᵢᵢ para la diagonal.

El núcleo (algebra/) escribe sus mensajes en texto plano («a_11 = 0», «F2 → F2 −
(2)·F1», códigos como TOLERANCIA_CAMBIO).  `md()` y `unicode()` los convierten al
mostrarlos, sin tocar el núcleo ni sus pruebas.
"""

import re
from typing import NamedTuple


class Simbolo(NamedTuple):
    latex: str      # sin los $ que lo rodean
    html: str       # para Plotly
    texto: str      # Unicode, para tablas y selectores

    def md(self):
        return f"${self.latex}$"


D_K = Simbolo(r"d_k", "d<sub>k</sub>", "dₖ")
R_K = Simbolo(r"r_k", "r<sub>k</sub>", "rₖ")
E_K = Simbolo(r"e_k", "e<sub>k</sub>", "eₖ")
# Como la lámina S8-28/09 p. 6: «número máximo de iteraciones k_max».
K_MAX = Simbolo(r"k_{\max}", "k<sub>max</sub>", "kₘₐₓ")
X_K = Simbolo(r"x^{(k)}", "x<sup>(k)</sup>", "x⁽ᵏ⁾")
T_J = Simbolo(r"T_J", "T<sub>J</sub>", "T de Jacobi")
T_GS = Simbolo(r"T_{GS}", "T<sub>GS</sub>", "T de Gauss-Seidel")

# d_k, r_k y e_k completos (la definición junto al símbolo)
D_K_DEF = Simbolo(r"d_k = \|x^{(k)} - x^{(k-1)}\|_\infty",
                  "d<sub>k</sub> = ‖x<sup>(k)</sup> − x<sup>(k−1)</sup>‖<sub>∞</sub>",
                  "dₖ = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞")
R_K_DEF = Simbolo(r"r_k = \|b - Ax^{(k)}\|_\infty",
                  "r<sub>k</sub> = ‖b − Ax<sup>(k)</sup>‖<sub>∞</sub>",
                  "rₖ = ‖b − Ax⁽ᵏ⁾‖∞")
E_K_DEF = Simbolo(r"e_k = \|x^{(k)} - x^*\|_\infty",
                  "e<sub>k</sub> = ‖x<sup>(k)</sup> − x*‖<sub>∞</sub>",
                  "eₖ = ‖x⁽ᵏ⁾ − x*‖∞")
METRICAS = {"d": (D_K, D_K_DEF), "r": (R_K, R_K_DEF), "e": (E_K, E_K_DEF)}

# Motivos de terminación del Módulo IV (los códigos de algebra/.../ejecucion.py)
# en palabras: nunca se muestra el código interno.
MOTIVOS = {
    "TOLERANCIA_CAMBIO": "Criterio A cumplido",
    "TOLERANCIA_RESIDUO": "Criterio B cumplido",
    "N_COMPLETADAS": "N iteraciones completadas",
    "MAXIMO_ITERACIONES": "Máximo de iteraciones sin cumplir el criterio",
    "ERROR_NO_FINITO": "Valores no finitos (se detuvo)",
    "DIAGONAL_CERO": "Elemento diagonal nulo",
    "ENTRADA_INVALIDA": "Entrada inválida",
    "ERROR_INTERNO": "Error interno",
}

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def subindice(numero):
    """12 → ₁₂ (para F₁, x₂, a₁₁ en texto Unicode)."""
    return str(numero).translate(_SUB)


def motivo(codigo):
    return MOTIVOS.get(codigo, codigo)


# Notación en texto plano que usa el núcleo → (LaTeX, Unicode).  Se reemplaza en una
# sola pasada (una expresión con alternativas), para que una regla no vuelva a
# tocar lo que escribió otra.
_FIJAS = {
    "x_i(0)": (r"x_i^{(0)}", "xᵢ⁽⁰⁾"),
    "a_ii": (r"a_{ii}", "aᵢᵢ"),
    "b_i": (r"b_i", "bᵢ"),
    "x_i": (r"x_i", "xᵢ"),
    "T_GS": (r"T_{GS}", "T_GS"),
    "T_J": (r"T_J", "T_J"),
    "k_max": (r"k_{\max}", "kₘₐₓ"),
    "d_k": (r"d_k", "dₖ"),
    "r_k": (r"r_k", "rₖ"),
    "e_k": (r"e_k", "eₖ"),
}
_PATRON = re.compile(
    r"\b(?:" + "|".join(re.escape(t) for t in sorted(_FIJAS, key=len, reverse=True)) + r")(?![\w(])"
    r"|\bx_i\(0\)"
    r"|\b(?P<a>a)_(?P<ij>\d+)\b"           # a_11, a_23 (elemento de la diagonal o de A)
    r"|\b(?P<v>[dre])_(?P<m>\d+)\b"        # d_7, r_12: valor de la iteración k = 7
    r"|\b(?P<l>[FxtM])_?(?P<n>\d+)\b")      # F2, x3, t1, M_1: filas, incógnitas, parámetros


def _signos(texto):
    """Un solo signo menos (−, no el guion -) y divisores negativos entre paréntesis:
    «(-5 − (0)) / -3» → «(−5 − (0)) / (−3)».  No toca «1e-3» ni «S9-07/10»."""
    texto = texto.replace("||", "‖")                       # ||A||∞ → ‖A‖∞
    texto = re.sub(r"(?<![\w)\]])-(?=\d)", "−", texto)
    return re.sub(r"/ −(\d+(?:[./]\d+)*)", r"/ (−\1)", texto)


# Normas y número de condición escritos en Unicode por el núcleo: ‖A⁻¹‖∞, κ∞(D⁻¹A), ‖r‖₂.
_NORMA = re.compile(r"‖([A-Za-zΔ·⁻¹ ]{1,6})‖([∞₁₂])?|κ([∞₁₂])\(([A-Za-z⁻¹]{1,5})\)|κ∞")
_INDICE_NORMA = {"∞": r"_\infty", "₁": "_1", "₂": "_2", None: "", "": ""}


def _latex_simple(texto):
    return texto.replace("⁻¹", "^{-1}").replace("Δ", r"\Delta ").replace("·", r"\cdot")


def _normas(texto):
    def cambio(m):
        if m.group(0) == "κ∞":
            return r"$\kappa_\infty$"
        if m.group(3):
            return rf"$\kappa{_INDICE_NORMA[m.group(3)]}({_latex_simple(m.group(4))})$"
        return rf"$\|{_latex_simple(m.group(1))}\|{_INDICE_NORMA[m.group(2)]}$"
    return _NORMA.sub(cambio, texto)


def _reemplazar(texto, latex):
    texto = _signos(texto)
    if latex:
        texto = _normas(texto)

    def cambio(m):
        if m.group("a"):
            return f"$a_{{{m.group('ij')}}}$" if latex else "a" + subindice(m.group("ij"))
        if m.group("v"):
            return f"${m.group('v')}_{{{m.group('m')}}}$" if latex else m.group("v") + subindice(m.group("m"))
        if m.group("l"):
            return m.group("l") + subindice(m.group("n"))
        forma = _FIJAS[m.group(0)][0 if latex else 1]
        return f"${forma}$" if latex else forma
    return _PATRON.sub(cambio, _codigos(texto))


def md(texto):
    """Texto del núcleo → markdown de Streamlit (LaTeX entre $), con los códigos de
    terminación en palabras.  No altera ningún número.  Lo que ya está entre $…$ se
    deja igual, así que también sirve para textos que mezclan prosa y LaTeX."""
    partes = re.split(r"(\$[^$]*\$)", texto)
    return "".join(p if p.startswith("$") and p.endswith("$") and len(p) > 1 else _reemplazar(p, latex=True)
                   for p in partes)



def unicode(texto):
    """Como md(), pero solo con Unicode (para st.dataframe, selectores y HTML propio)."""
    return _reemplazar(texto, latex=False)


def _codigos(texto):
    """«(TOLERANCIA_CAMBIO)» dentro de una frase → «(criterio A cumplido)»."""
    def palabras(m):
        if m.group(0) not in MOTIVOS:
            return m.group(0)
        frase = MOTIVOS[m.group(0)]
        return frase[0].lower() + frase[1:]
    return re.sub(r"\b[A-Z]+(?:_[A-Z]+)+\b", palabras, texto)



def ecuacion(coeficientes, variables, independiente):
    """«2x − y + 3z = 5» con signos correctos (nunca «+ -1y»).  Formato :g."""
    terminos = []
    for valor, nombre in zip(coeficientes, variables):
        if valor == 0:
            continue
        magnitud = abs(valor)
        texto = nombre if magnitud == 1 else f"{magnitud:g}{nombre}"
        if not terminos:
            terminos.append(("−" if valor < 0 else "") + texto)
        else:
            terminos.append(("− " if valor < 0 else "+ ") + texto)
    izquierda = " ".join(terminos) if terminos else "0"
    derecha = f"{independiente:g}".replace("-", "−")
    return f"{izquierda} = {derecha}"
