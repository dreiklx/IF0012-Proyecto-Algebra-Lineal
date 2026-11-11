# Notación matemática en Ax

**Revisión del 11-nov-2026.** Objetivo: que ninguna pantalla muestre notación de programación (`d_k`, `k_max`, `x^(k)`, `||A||`, `TOLERANCIA_CAMBIO`) donde corresponde un subíndice, un superíndice o una palabra.

**Regla:** solo cambió la **presentación**. Las fórmulas y los cálculos de `algebra/` son los mismos: el volcado de 273 resultados salió idéntico.

## 1. Qué renderiza cada parte (comprobado en Brave)

Se probó cada elemento con una página de ensayo y Streamlit 1.66.1 / Plotly 6.3.0:

| Elemento | LaTeX `$d_k$` | HTML `d<sub>k</sub>` | Unicode `dₖ` | Forma usada |
|---|---|---|---|---|
| `st.markdown`, `st.caption`, `st.info/success/warning/error` | ✅ | solo con `unsafe_allow_html` | ✅ | **LaTeX** |
| Etiqueta de `st.metric` | ✅ (tras corregir el CSS, ver abajo) | ❌ se ve el código | ✅ | **LaTeX** |
| Etiquetas de `st.radio`, `st.slider`, `st.text_input`, `st.checkbox`; opciones de `st.radio` | ✅ | ❌ | ✅ | **LaTeX** |
| Pestañas (`st.tabs`), `st.expander` | ✅ | ❌ | ✅ | LaTeX o Unicode |
| Encabezados de `st.table` | ✅ | ❌ | ✅ | **LaTeX** |
| Encabezados de `st.dataframe` | ❌ se ve `$d_k$` | ❌ | ✅ | **Unicode** |
| Opciones de `st.selectbox` | ❌ | ❌ | ✅ | **Unicode** |
| Plotly: títulos, ejes, leyenda, anotaciones, cursor | ❌ (Streamlit no carga MathJax) | ✅ | ✅ (subíndices pequeños) | **HTML** |
| Componentes HTML propios (chips, valor destacado) | ❌ | ✅ (solo `<sub>` y `<sup>`) | ✅ | **HTML** |
| Archivo CSV descargable | — | — | — | ASCII (`d_k`, `x1`): es un archivo de datos |

**Decisión:** no se agregó ninguna biblioteca. Streamlit ya trae KaTeX y Plotly entiende `<sub>`/`<sup>`. MathJax no se cargó: cambiaría el HTML de la gráfica 3D y no aporta nada que `<sub>` no resuelva.

**Corrección de CSS.** La regla que impide truncar números en las métricas (`white-space:normal; overflow-wrap:anywhere`) también partía las fórmulas KaTeX: $d_k$ se veía como «d» arriba y «k» abajo. Ahora excluye `.katex` (`interfaz/recursos/estilo.css`).

## 2. Cómo está implementado

`visualizacion/notacion.py` reúne toda la notación:

- **Cada símbolo en tres formas:** `Simbolo(latex, html, texto)`. Por ejemplo `D_K`, `R_K`, `E_K`, `K_MAX`, `X_K`, `D_K_DEF` (dₖ = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞).
- **`md(texto)`:** convierte los textos del núcleo en markdown con LaTeX. Por ejemplo «a_11 = 0» → $a_{11} = 0$, «d_7» → $d_{7}$, «||A||∞» → $\|A\|_\infty$, «κ∞(A)» → $\kappa_\infty(A)$, «F2 → F2 − (2)·F1» → «F₂ → F₂ − (2)·F₁», «(-5) / -3» → «(−5) / (−3)», y los códigos internos en palabras (TOLERANCIA_CAMBIO → «criterio A cumplido»). Respeta lo que ya está entre `$…$` y nunca cambia un número.
- **`unicode(texto)`:** lo mismo, sin LaTeX, para tablas y selectores.
- **`MOTIVOS`:** los códigos de terminación en palabras.
- **`ecuacion()`:** escribe «2x − y + 3z = 5» y no «2·x + -1·y + 3·z = 5».

El núcleo sigue escribiendo sus mensajes en texto simple; la conversión ocurre solo al mostrarlos. Así las pruebas del núcleo no cambiaron.

## 3. Errores de notación encontrados y corregidos

| # | Dónde | Se veía | Ahora |
|---|---|---|---|
| 1 | Gráfica de convergencia (IV): leyenda, cursor, anotaciones | `d_k = ‖x⁽ᵏ⁾…`, `r_k`, «Se alcanzó k_max = 50», «d_k < ε» | d<sub>k</sub>, r<sub>k</sub>, k<sub>max</sub> |
| 2 | Gráfica comparativa (IV): título, eje, cursor | «Cambio entre iteraciones d_k», `d_k`, `e_k = ‖x⁽ᵏ⁾ − x*‖∞` | d<sub>k</sub>, e<sub>k</sub> con ‖·‖<sub>∞</sub> |
| 3 | Gráfica del precondicionador | `d_k` en el eje y en el cursor | d<sub>k</sub> |
| 4 | Métricas del Módulo IV | «Diferencia final d_k», «Residuo final r_k» | $d_k$, $r_k$ en LaTeX |
| 5 | Tablas de iteraciones y comparación | columnas `x1`, `d_k (criterio de parada)`, `r_k`, `e_k`, `d final` | x₁, dₖ, rₖ, eₖ |
| 6 | Insignias de resultado | `TOLERANCIA_CAMBIO`, `MAXIMO_ITERACIONES` | «Criterio A cumplido», «Máximo de iteraciones sin cumplir el criterio» |
| 7 | Tablas «Motivo» (comparar, barrido de ω, precondicionador) y chips de Richardson | códigos internos | palabras |
| 8 | Mensaje de parada | «Criterio satisfecho: d_7 = …» | $d_{7}$ |
| 9 | Diagonal nula | «a_11 = 0 … x_i(0) = b_i / a_ii» | $a_{11}$, $x_i^{(0)} = b_i/a_{ii}$ |
| 10 | Conclusiones del precondicionador | «λ(T_J)», «ρ(T_J)», «a_ii», «(TOLERANCIA_CAMBIO)» | $T_J$, $a_{ii}$, palabras |
| 11 | Barrido de ω | encabezado `ρ(T_ω)` en st.dataframe | $\rho(T_\omega)$ en st.table |
| 12 | Tabla de dominancia | `Σ_{j≠i} \|aᵢⱼ\|` (llaves visibles) | $\sum_{j\ne i}\|a_{ij}\|$ |
| 13 | Polinomio característico | `` `det(T − λI) = −λ³ − 4/9λ + 4/3 = 0` `` en fuente de código; «4/9λ» ambiguo | LaTeX con fracciones apiladas |
| 14 | Pasos de Gauss y Gauss-Jordan | «F2 → F2 − (2)·F1» | «F₂ → F₂ − (2)·F₁» |
| 15 | Sustitución hacia atrás | «x3 = (-5 − (0)) / -3» (dos signos menos distintos, divisor negativo sin paréntesis) | «x₃ = (−5 − (0)) / (−3)» |
| 16 | Solución paramétrica | «t1 = x3» | $t_1 = x_3$ |
| 17 | Módulo II | «‖A‖∞», «κ∞(A)», «||A||∞» (barras ASCII en el mensaje) | $\|A\|_\infty$, $\kappa_\infty(A)$ con subíndice |
| 18 | Cramer (III) | «det(M_1)» | $D_1 = \det(A_1)$, la notación de la lámina |
| 19 | Rectas y planos (I) | «2·x + -1·y + 3·z = 5» | «2x − y + 3z = 5» |
| 20 | Ajuste (III): leyenda y cursor | «Residuos rᵢ», «r = y − ŷ» | r<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub> |
| 21 | Etiquetas de parámetros (IV) | «Máximo de iteraciones», «x⁽⁰⁾» en texto | «Máximo de iteraciones $k_{\max}$», $x^{(0)}$ |
| 22 | Criterios A y B (radio) | ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε en Unicode | LaTeX |

**k_max:** se escribe $k_{\max}$, como en la lámina S8-28/09 p. 6 («número máximo de iteraciones k_max»).

## 4. Verificación

- **Pantallas:** un guion con AppTest recorrió los 4 módulos con todos los ejemplos, los criterios A/B/C y todos los botones. Revisó **7819 textos visibles**: markdown, avisos, métricas, encabezados de tablas, etiquetas de widgets y todos los textos de Plotly. Encontró 0 con notación de programación. Un caso de control con «k_max» y «TOLERANCIA_CAMBIO» sí se detectó, lo que confirma que la búsqueda funciona.
- **Mensajes del núcleo:** 337 textos distintos del núcleo (ejemplos y casos límite), revisados después de `md()`.
- **Pruebas:** `tests/interfaz/test_notacion.py`.
- **Brave:** revisión visual de los cuatro módulos a 1440, 1366 y 1024 px.
