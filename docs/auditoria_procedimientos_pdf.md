# Auditoría de los procedimientos de Ax frente a los PDF (11-nov-2026)

**Pregunta:** ¿Ax resuelve y **presenta** cada procedimiento como la profesora? No basta con que las fórmulas coincidan: se compararon el orden de los pasos, la notación, los despejes, las operaciones de fila y la forma de presentar los resultados.

## 1. Fuentes

- **Carpeta:** `C:\Users\dfarl\Desktop\ALGEBRA LINEAL`.
- **Contenido:** 18 PDF y **457 páginas**, los mismos de la revisión anterior. La fecha más reciente es el 11-oct-2026. Además hay `TareaII_Algebra_Derek-Daniel.zip` y `documentacion/auditoria_documental.md` (26-oct), que es nuestra.
- **No hay documentos nuevos.**
- **Método:**
  - se volvió a extraer el texto de las 457 páginas con PyMuPDF;
  - 182 páginas tienen texto extraíble y se citaron directamente;
  - las demás son manuscritos escaneados: se volvieron a **ver como imagen** las 52 páginas que definen procedimientos:

| PDF | Páginas vistas |
|---|---|
| S3-24/08 | 4-8 |
| S6-14/09 | 25-31 |
| S6-16/09 | 29 |
| S7-21/09 | 17-20 |
| S8-28/09 | 4, 6, 7 |
| S8-30/09 | 4-8, 13, 16, 19, 20, 24, 28, 32, 33, 36, 37 |
| S9-05/10 | 2, 3, 16, 17, 19, 21, 32, 33 |
| S9-07/10 | 1-7 |
| Tarea II | 1-2 |

- **Comparación:** cada página se comparó con lo que **muestra Ax hoy**, no con lo que documentaban las revisiones anteriores.

## 2. Resultado

- **Diferencias matemáticas reales en Ax:** ninguna. Todos los resultados coinciden con los procedimientos de clase, salvo donde la lámina tiene una errata, ya documentada en `referencia_oficial_procedimientos.md` §9.
- **Diferencias de presentación:** se encontraron 9. Se corrigieron 7. Las otras 2 son diferencias de orden, que se documentan y no se cambian en el núcleo (D1, D2).

| # | Módulo | Cómo lo hace la profesora | Ax antes | Acción |
|---|---|---|---|---|
| D1 | I · Gauss | Manuscrito S6-16/09 p. 29: normaliza cada pivote a 1 (−F₂, −⅓F₃) y luego sustituye hacia atrás con ecuaciones simples («y + 3z = 9 → y = 4») | Igual que la **lámina** S6-14/09 pp. 28-29: multiplicadores sin normalizar (F₂ − ½F₁) y sustitución con la fórmula | **Se documenta.** Las dos versiones son de la profesora. Cambiarla alteraría el algoritmo y los pasos de las pruebas. Mismo resultado. Para la defensa: «Gauss sigue la lámina; Gauss-Jordan normaliza como el manuscrito» |
| D2 | I · Gauss-Jordan e inversa | S3-24/08 pp. 5 y 8: primero baja (anula debajo y normaliza) y después sube | Por columnas: en cada pivote anula arriba y abajo | **Se documenta.** El enunciado pide «Gauss o Gauss-Jordan» sin fijar el orden. El resultado es idéntico y cada operación se muestra con su notación («−2F₁ + F₂») |
| D3 | I | Sustitución con un solo signo menos | «x₃ = (-5 − (0)) / -3»: guion y signo mezclados, divisor sin paréntesis | Corregido: «x₃ = (−5 − (0)) / (−3)» |
| D4 | II | S7-21/09 p. 19: 5 pasos; «Fila 1: \|1\| + \|2\| = 3, Fila 2: \|3\| + \|1\| = 4, ‖B‖∞ = máx{3, 4} = 4» | Solo los valores ‖A‖∞ y ‖A⁻¹‖∞ | Corregido: «Procedimiento de clase» con los 5 pasos y las sumas por fila (`matriz.sumas_absolutas_por_fila`) |
| D5 | III | S8-30/09 pp. 4 y 7: D = det(A), Dᵢ = det(Aᵢ), xᵢ = Dᵢ/D; manuscrito: \|A\|, \|Aₓ\|, \|A_y\| | «det(M_1)» | Corregido: notación D y Dᵢ de la lámina, y la del manuscrito como aclaración. Paso 1 con sus palabras: «b es linealmente independiente de las columnas de A» |
| D6 | IV | S8-30/09 pp. 19, 24 y 32: primero «realizar los despejes de las incógnitas»: x₁⁽ᵏ⁺¹⁾ = (22 − 2x₂⁽ᵏ⁾ − x₃⁽ᵏ⁾)/6; SOR: x^GS y luego (1 − ω)x⁽ᵏ⁾ + ω·x^GS | No mostraba los despejes | Corregido: expander «Despeje de las incógnitas» (`formulas.latex_despejes`); coincide letra por letra con los tres manuscritos (prueba `TestDespejes`) |
| D7 | IV | S9-07/10 pp. 3-7: pasos ① A = D + L + U, ② D⁻¹, ③ T_J, ④ C_J, ⑤ det(T − λI) por Sarrus; x⁽ᵏ⁺¹⁾ = T_J x⁽ᵏ⁾ + C_J | D, L, U, T y «c»; sin D⁻¹ | Corregido: pasos numerados ①-⑤, nombres T_J/C_J y T_GS/C_GS, y D⁻¹ o (D+L)⁻¹. Se agregó el campo `MatrizIteracion.inversa`, que el núcleo ya calculaba; T y c no cambian |
| D8 | IV | S8-28/09 p. 6: «número máximo de iteraciones k_max» | «k_máx» | Corregido: $k_{\max}$ |
| D9 | IV | Manuscritos: el cambio entre iteraciones se llama «tolerancia» T₁, T₂… | Solo dₖ | Corregido: la explicación de dₖ menciona T₁, T₂, … |

## 3. Coincidencias verificadas, módulo por módulo

**Módulo I**

- Matriz aumentada [A | b].
- Operaciones «−2F₁ + F₂», «F₁ ↔ F₂», «(−1/3)F₃», como en S3-24/08 pp. 4-5.
- Clasificación «3 ecuaciones no nulas, 3 incógnitas → solución única» (S6-16/09 p. 29).
- Sol = {(1/3, 4, 5/3)}.
- Tipos de solución con interpretación geométrica (S6-14/09 p. 26).
- Inversa por [A | I] → [I | A⁻¹] con verificación A·A⁻¹ = I (S3-24/08 p. 7).

**Módulo II**

- κ(A) = ‖A‖‖A⁻¹‖ con la inversa por Gauss-Jordan.
- Cota ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ (S7-21/09 p. 18).
- Ejemplo de la lámina: κ∞(B) = 4 · 4/5 = 16/5, idéntico.
- Por decisión del enunciado, Ax usa la norma ∞ y la escala de 3 niveles (10/100), no la de 5 niveles de la lámina.

**Módulo III**

- Sobredeterminado: m > n y b ∉ Col(A), con det[A | b] = −11 ≠ 0.
- Sistema normal AᵀAx = Aᵀb.
- Cramer: \|A\| = 363, \|Aₓ\| = 715, \|A_y\| = −319, x̂ = (65/33, −29/33), idéntico al manuscrito S8-30/09 p. 7.
- El enunciado pide resolver con «un método directo ya implementado»: Ax usa Gauss y muestra Cramer como verificación.

**Módulo IV**

- Fórmulas por componentes de Jacobi, Gauss-Seidel y SOR.
- x⁽⁰⁾ = bᵢ/aᵢᵢ.
- Parada ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε o residuo.
- Norma ∞ como máximo (la errata de T₁, sumada en S8-30/09 p. 20, está documentada).
- T_J = −D⁻¹(L + U) y T_GS = −(D + L)⁻¹U.
- ρ(T) = máx\|λ\| con det(T − λI) por Sarrus.
- Comparación con «error final ‖x⁽ᵏ⁾ − x‖∞» y gráfica logarítmica (S9-05/10 pp. 16-17).
- Barrido de ω (S9-05/10 p. 16, «Influencia del factor de relajación»).

## 4. Extensiones (siguen identificadas como tales)

| Extensión | Dónde | Cómo se identifica en Ax |
|---|---|---|
| Richardson | `metodos.paso_richardson`, `precondicionamiento.py` | Aviso «Extensión no vista en clase» en la pestaña de precondicionamiento; Cat. C |
| Faddeev-LeVerrier | `polinomio_raices.py` (archivo separado desde el 11-nov) | Leyenda «Cat. C, extensión no vista en clase» |
| Durand-Kerner | `polinomio_raices.py` | Igual |
| Matriz de iteración de SOR | `matriz_iteracion.py` | «Cat. C · no aparece en los PDF del curso» |

Ninguna se presenta como contenido visto en clase.

## 5. Erratas de las láminas: siguen sin usarse como resultado esperado

Se revisaron de nuevo en las imágenes:

- S6-14/09 p. 29: la solución del ejemplo de Gauss.
- S9-07/10 p. 4: ρ(T_J) = 0, cuando el polinomio correcto es −λ³ − 4/9λ + 4/3 y ρ ≈ 1,174.
- S9-07/10 p. 7: C_GS = −(D + L)⁻¹b, con el signo cambiado.
- S8-30/09 p. 20: T₁ = 2,402 sumado (es la norma 1).
- S9-05/10 p. 23: la mejora de Jacobi con M = D.

Todas siguen en `referencia_oficial_procedimientos.md` §9; Ax muestra los valores correctos.

## 6. Verificación

- **Volcado** de 273 resultados de los ejemplos: idéntico a `main`. Las únicas líneas distintas son el campo nuevo `MatrizIteracion.inversa`.
- **Auditoría:** 0 fallos (4500 + 400 + 200 + 300 + 600 + 300 + 150 casos).
- **Pruebas nuevas:** despejes de los tres manuscritos, sumas por fila de S7-21/09 p. 19, D⁻¹ y (D+L)⁻¹ de S9-07/10.

---

## Revisión del 12-nov-2026 (auditoría de la norma y del OCR)

### 2.2 Criterio A: fórmula de la lámina y de Ax (CORREGIDO el 13-nov-2026)

**Corrección:** la versión anterior afirmaba que la lámina usaba una norma relativa. Esa lectura fue un error de OCR. Verificado en imagen: S8-28/09 p. 6 y S8-30/09 p. 9 escriben ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε, sin división. El título dice «norma del error relativo», pero la fórmula es absoluta. Ax coincide con la fórmula.

La lámina S8-28/09 p. 6 tiene además una errata interna: el ejemplo fija ε = 10⁻³, pero la conclusión usa 0,01 y detiene en k = 8. Con 0,01 el criterio ya se cumple en k = 7 (0,005 < 0,01).

Tabla original (superada):

| Fuente | Fórmula escrita | Tipo |
|---|---|---|
| Lámina S8-28/09 p. 6 (OCR, ver nota) | ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ / ‖x⁽ᵏ⁾‖ < ε, titulada «norma del error relativo» | relativa |
| Enunciado OFICIAL p. 2 | «mostrar… el error utilizado como criterio de parada»; no fija la norma | libre |
| Ax, `algebra/modulo_IV_iterativos/ejecucion.py` | d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε | absoluta, norma ∞ |

**Diferencia:** la absoluta depende de la escala de x; la relativa la normaliza. Son criterios equivalentes solo si ‖x⁽ᵏ⁾‖ ≈ 1.

**Medido** (tridiagonal 4×4 de la guía, b = (1, 0, 0, 1), ε = 10⁻³, x⁽⁰⁾ = 0): Jacobi para en k = 7 con la absoluta y en k = 8 con la relativa; Gauss-Seidel en k = 5 y k = 6.

**Decisión:** se mantiene la absoluta. Cambiarla alteraría todos los historiales y las pruebas de referencia, y el enunciado no la prescribe. Para evitar contradicciones:
- La interfaz muestra una nota bajo el selector de criterio (`interfaz/modulos/modulo_IV_iterativos/principal.py`).
- La procedencia dice «versión absoluta; la lámina usa la relativa».
- La guía express explica la diferencia y avisa de que los números de iteración de la guía corresponden a la absoluta.

**Pendiente:** añadir la relativa como opción explícita (no hecho).

### 2.3 Erratas verificadas

| Documento y página | Dice | Verificado | Estado en Ax |
|---|---|---|---|
| S9-07/10 p. 4 | ρ(T_J) = 0 | ρ ≈ 1,174 (polinomio −λ³ − (4/9)λ + 4/3) | Corregido, ver guía |
| S9-05/10 p. 23 | M = D acelera Jacobi | Iteraciones idénticas: D⁻¹A tiene diagonal 1, así que T_J es la misma | Documentado (`precondicionamiento.py`) |
| S8-28/09 p. 6 | Fórmula relativa | Ver 2.2 | Documentado |

### 2.4 Estado de la revisión visual

- **OCR:** las 457 páginas de los 15 PDF de clase se pasaron por OCR (RapidOCR). Textos en `scratchpad\ocr_out\`.
- **Revisión visual completa:** **no completada en esta sesión.** La herramienta de lectura bloquea imágenes grandes, así que no pude ver las láminas. Solo se confirmaron por OCR los puntos de las secciones 2.2 y 2.3 y la ausencia de Richardson, Faddeev-LeVerrier y Durand-Kerner (0 coincidencias).
- **Requiere revisión visual adicional:** todos los procedimientos de los módulos I-IV (Gauss, Gauss-Jordan, determinantes, normas, mínimos cuadrados, Cramer, Jacobi, Gauss-Seidel, SOR, matrices de iteración y det(T−λI)).
- **Pendiente externo:** P-2 (IA): el programa §6.2 habla de uso «no autorizado»; confirmar con la docente.
