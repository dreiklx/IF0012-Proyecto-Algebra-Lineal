# Auditoría de textos frente al material de la profesora

**Fecha:** 10-nov-2026 · **Rama:** `feature/textos-profesora`.

**Objetivo.** Comprobar que Ax habla como la profesora: mismos nombres, la misma notación y el mismo orden de pasos. Además, marcar en la interfaz de dónde sale cada procedimiento.

**Reglas de esta revisión:**

- **Ninguna fórmula correcta se cambió por estética.** Las adaptaciones son de texto y de presentación.
- **Volcado de resultados:** después de los cambios se volcaron los 273 resultados de los ejemplos precargados. Son idénticos a la línea base. La única diferencia es el campo de texto nuevo `Paso.notacion`, que se comprobó quitándolo del volcado.
- **Los PDF no se modificaron.** Solo se leyeron.

Complementa:

- [referencia_oficial_procedimientos.md](referencia_oficial_procedimientos.md): qué enseña cada PDF, página por página;
- [comparacion_procedimientos.md](comparacion_procedimientos.md): enunciado, PDF y código.

## 1. Inventario y control de la revisión

Carpeta: `%USERPROFILE%\Desktop\ALGEBRA LINEAL`.

**Inventario del 10-nov:** se calculó de nuevo el MD5 de cada archivo y se comparó con el inventario del 09-nov.

- No hay PDF nuevos ni modificados.
- Los 18 PDF suman 457 páginas.
- El único archivo que no estaba en el inventario anterior es `documentacion/auditoria_documental.md`. Es el informe propio del 26-oct, no material de la profesora.

| PDF | Págs. | Examinadas | Estado |
|---|---:|---:|---|
| IF0012-IITarea (T2) | 3 | 3 | Revisado en imagen y texto |
| Programa del curso (PROG) | 12 | 12 | Revisado en imagen y texto |
| INSTRUCCIONES proyecto final (OFICIAL) | 5 | 5 | Revisado en imagen y texto |
| S1-10/08 | 24 | 24 | Revisado en imagen (Tema 1) |
| S1-12/08 | 28 | 28 | Revisado en imagen (Tema 1) |
| S2-17/08 | 40 | 40 | Revisado en imagen (Tema 1) |
| S2-19/08 | 48 | 48 | Revisado en imagen: OEF, Sarrus, cofactores, inversa |
| S3-24/08 | 32 | 32 | Revisado; manuscritos pp. 4-5 y 8 vueltos a examinar el 10-nov |
| S3-26/08 | 38 | 38 | Revisado: normas de vectores |
| S4-02/09 | 32 | 32 | Revisado (Tema 1) |
| S5 Resolución I Quiz | 8 | 8 | Revisado |
| S6-14/09 | 35 | 35 | Revisado: sistemas, Gauss, LU |
| S6-16/09 | 36 | 36 | Revisado; manuscritos pp. 29 y 34 vueltos a examinar el 10-nov |
| S7-21/09 | 20 | 20 | Revisado; pp. 7 y 19 vueltas a examinar el 10-nov |
| S8-28/09 | 15 | 15 | Revisado: marco iterativo, κ en norma 2 |
| S8-30/09 | 40 | 40 | Revisado; manuscritos pp. 5-7, 19-20, 24 y 32-33 vueltos a examinar el 10-nov |
| S9-05/10 | 34 | 34 | Revisado; manuscritos pp. 32-34 vueltos a examinar el 10-nov |
| S9-07/10 | 7 | 7 | Revisado; pp. 3-7 vueltas a examinar el 10-nov |
| **Total** | **457** | **457** | Las 457 páginas se examinaron en imagen el 09-nov. Las 23 páginas manuscritas de procedimiento se volvieron a examinar a 1400 px el 10-nov |
| ZIP Tarea II (8 JPEG de estudiantes) | — | 8/8 | Revisado. No se transcribe porque contiene nombres y carnés |

## 2. Cómo resuelve la profesora (lo que se observa en los manuscritos)

| Tema | Su forma de resolver | Fuente |
|---|---|---|
| Operaciones elementales | Anota la operación junto a la flecha, con el múltiplo de la fila pivote primero y la fila que cambia después: «−2F₁ + F₂», «F₁ + F₃». Normaliza el pivote: «−F₂», «−⅓F₃», «1/13 F₂». Intercambia con «F₂ ↔ F₁». Resalta el pivote y los elementos que va a anular | S3-24/08 pp. 4-5; S6-16/09 p. 29 |
| Gauss | [A\|b] → ceros bajo cada pivote → pivotes normalizados a 1 → sustitución hacia atrás, escribiendo cada ecuación y sustituyendo (z = 5/3; y + 3(5/3) = 9; …). Cierra con «Sol = {(1/3, 4, 5/3)}» | S6-16/09 p. 29 |
| Clasificación | «3 ecuaciones no nulas, 3 incógnitas → Única solución» | S6-16/09 p. 29 |
| Mínimos cuadrados | Sigue tres pasos numerados. (1) Comprueba que b no es combinación lineal de las columnas: det[A\|b] por Sarrus = −11 ≠ 0. (2) Arma el sistema normal AᵀAx = Aᵀb. (3) Lo resuelve por la regla de Cramer: \|A\|, \|Aₓ\|, \|A_y\| | S8-30/09 pp. 5-7 |
| Condicionamiento | 5 pasos: elegir la norma, ‖A‖, A⁻¹ (verificar que es invertible), ‖A⁻¹‖, multiplicar | S7-21/09 p. 19 |
| Jacobi | x⁽⁰⁾ = bᵢ/aᵢᵢ. «Cálculo de la tolerancia T₁ = ‖x⁽¹⁾ − x⁽⁰⁾‖∞» y comparación «T₁ ≮ 0,01». Usa coma decimal | S8-30/09 pp. 19-20 |
| SOR | Calcula primero x^GS y luego (1 − ω)x⁽ᵏ⁾ + ω·x^GS, componente a componente. La norma es «máx{\|xᵏ⁺¹ − xᵏ\|, …}» | S8-30/09 pp. 32-33 |
| Convergencia | Pasos numerados: (1) A = D + L + U, (2) D⁻¹, (3) T_J = −D⁻¹(L+U), (4) C_J = D⁻¹b, (5) ρ(T) = máx{\|λ\|} con det(T − λI) por Sarrus. Para GS usa T_GS = −(D+L)⁻¹U | S9-07/10 pp. 3-7 |

## 3. Categorías de procedencia (A/B/C/D)

En la interfaz aparecen como distintivos «Cat. A», «Cat. B», etc., bajo la cabecera de cada módulo. Al pasar el cursor por un distintivo se ve la fuente. Se escribe «Cat.» para no confundirlas con los criterios de parada A/B/C del Módulo IV.

- **A — Visto en clase:** el procedimiento aparece en los PDF.
- **B — Exigido por el enunciado:** lo pide OFICIAL aunque no se haya resuelto en clase, o lo pide de otra forma.
- **C — Extensión o incentivo:** no se vio en clase. Se incluye por un incentivo o porque hace falta para un requisito.
- **D — Sin respaldo:** ni el material ni el enunciado lo sustentan.

| Módulo | Procedimiento | Cat. | Fuente |
|---|---|:-:|---|
| I | [A\|b] y operaciones elementales | A | S2-19/08 p. 27; S6-14/09 pp. 25-27 |
| I | Gauss y sustitución hacia atrás | A | S6-14/09 pp. 28-32; S6-16/09 p. 29 |
| I | Gauss-Jordan e inversa [A\|I] → [I\|A⁻¹] | A | S3-24/08 pp. 4-8; S6-14/09 p. 30 |
| I | Tipos de solución (única, infinitas, ninguna) | A | S6-14/09 p. 26 |
| I | Detección de pivotes nulos o numéricamente problemáticos | B | OFICIAL p. 2 (el umbral 10⁻¹⁰ es una decisión técnica propia) |
| I | Pivoteo parcial (opcional) | C | S6-14/09 p. 34 solo menciona PA = LU |
| I | Determinante por eliminación | A | Propiedades del determinante, S2-19/08 p. 38 |
| I | Gráfica de rectas y planos | C | Incentivo UX; interpretación geométrica de S6-14/09 p. 26 |
| II | κ = ‖A‖ ‖A⁻¹‖ en 5 pasos; inversa por Gauss-Jordan | A | S7-21/09 pp. 17-19 |
| II | Norma ∞ y escala 10 / 100 | B | OFICIAL p. 2 (la lámina usa 5 niveles) |
| II | Cota ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ | A | S7-21/09 p. 18 |
| II | Perturbación absoluta o porcentual | B | OFICIAL p. 2 |
| III | det[A\|b] ≠ 0 (para m = n + 1) | A | S8-30/09 p. 6 |
| III | Sistema normal AᵀAx = Aᵀb | A | S8-30/09 pp. 5-7 |
| III | Resolverlo con un método directo propio (Gauss) | B | OFICIAL p. 2 |
| III | Regla de Cramer (verificación, n ≤ 3) | A | S8-30/09 pp. 4 y 7 |
| III | Residuo r = b − Ax̂ y ‖r‖₂; recta de mejor ajuste y su gráfica | B | OFICIAL p. 2 |
| IV | Jacobi, Gauss-Seidel y SOR por componentes | A | S8-30/09 pp. 15-33 |
| IV | Parada ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε, o por residuo | A | S8-28/09 p. 6; S8-30/09 p. 28 |
| IV | Parada por número fijo de iteraciones | B | OFICIAL p. 2 («máximo de iteraciones») |
| IV | x⁽⁰⁾ = bᵢ/aᵢᵢ | A | S8-30/09 pp. 19-20 y 24 |
| IV | Dominancia diagonal y reordenamiento de ecuaciones | A | S8-30/09 p. 37; S9-05/10 pp. 32-33 |
| IV | T_J, T_GS, det(T − λI) por Sarrus y ρ(T) | A | S9-07/10 pp. 3-7 |
| IV | Tabla k, x⁽ᵏ⁾, error; motivo de parada; comparación; gráfica del error | B | OFICIAL p. 2 |
| IV | Error final ‖x⁽ᵏ⁾ − x‖∞ en la comparación | A | S9-05/10 p. 17 |
| IV | Matriz de iteración de SOR (T_ω) | C | No aparece en los PDF |
| IV | Faddeev-LeVerrier (coeficientes de det(T − λI) para n > 3) | C | Extensión no vista en clase |
| IV | Durand-Kerner (raíces del polinomio) | C | Extensión no vista en clase |
| IV | CSR y pasos O(nnz) | C | Incentivo; formato visto en S9-05/10 p. 9 |
| IV | Precondicionador M = D y comparación | C | Incentivo; visto en S9-05/10 pp. 19-23 |
| IV | Richardson | C | Extensión no vista en clase (`investigacion_richardson.md`) |
| IV | Reporte CSV | C | Incentivo de visualización |

**Categoría D:** no se encontró ningún procedimiento en esta categoría. Los dos casos que más se acercan son interpretaciones propias documentadas de un requisito B:

- el umbral del pivote «problemático»;
- la perturbación porcentual.

**Extensiones:** ninguna se eliminó. Todas quedan rotuladas como Cat. C en la interfaz, en los documentos y en los comentarios del código.

## 4. Cambios hechos en Ax para hablar como la profesora

| Dónde | Antes | Ahora | Motivo |
|---|---|---|---|
| Pasos de Gauss y Gauss-Jordan (y de la inversa) | «F2 → F2 − (2)·F1» | «−2F₁ + F₂ · F2 → F2 − (2)·F1». Su notación va primero y la forma formal queda como aclaración | S3-24/08 pp. 4-5; S6-16/09 p. 29 |
| Normalización del pivote | «F3 → F3 ÷ (−3)» | «(−1/3)F₃ · F3 → F3 ÷ (−3)» | Escribe «−⅓F₃» |
| Resultado del Módulo I | x = vector | Además: «Sol = {(1/3, 4, 5/3)}» | Cierra así sus ejercicios |
| Clasificación | Rangos | Además: «Como en clase: 3 ecuaciones no nulas, 3 incógnitas → solución única» | S6-16/09 p. 29. Los rangos se mantienen porque son equivalentes y cubren m ≠ n |
| Editor de matrices | Filas «f1, f2…» | «F1, F2…» | Ella numera las filas como F |
| Cabecera de los 4 módulos | — | Distintivos de procedencia Cat. A/B/C | Pedido de esta revisión |
| Convergencia | Faddeev y Durand-Kerner mencionados sin rótulo | «Cat. C, extensión no vista en clase». La fórmula de T de SOR también lleva su rótulo | Pedido de esta revisión |
| Portada | — | Leyenda de las categorías | — |

**Lo que se mantuvo distinto a propósito:**

- **Orden de Gauss-Jordan.** Ax anula arriba y abajo de cada pivote en la misma columna. La profesora suele bajar primero (Gauss) y luego subir, o pasa a sustitución hacia atrás. Las operaciones y el resultado son los mismos; cambiar el orden modificaría el núcleo sin ganancia matemática.
- **Error del criterio de parada.** Ax usa el máximo, que es la definición de ‖·‖∞. Los manuscritos suman las diferencias y lo rotulan ∞ (ver la errata 8).
- **Mínimos cuadrados.** Ax resuelve con Gauss, como exige el enunciado («con un método directo ya implementado»). Cramer, que es el método de clase, se muestra como verificación.
- **Condicionamiento.** Ax usa κ∞ y la escala de 3 niveles del enunciado, no la de 5 niveles de la lámina.
- **Coma decimal.** Ax acepta `2,5` en la entrada. La salida usa punto, porque la aplicación muestra muchas cifras y tablas y así es uniforme con las gráficas. Es un aspecto visual, no matemático.

## 5. Erratas re-verificadas el 10-nov

Se recalcularon todas de forma independiente, sin usar código de Ax:

- con fracciones exactas y la regla de Cramer o Sarrus;
- con NumPy, solo como herramienta de auditoría, fuera de la aplicación.

| # | Fuente | Dice | Valor recalculado |
|---|---|---|---|
| 1 | S2-19/08 pp. 42-43 | det = 42 | **15** |
| 2 | S3-26/08 p. 26 | ‖x‖₂ ≤ ‖x‖∞ ≤ ‖x‖₁ | ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁; con x = (3, −4): 4 ≤ 5 ≤ 7 |
| 3 | S6-14/09 p. 29 | (1/2, −1, −1) | **(19/20, −5/4, −7/20)** |
| 4 | S7-21/09 p. 14 | (100, −97) | **(100/101, 203/101) ≈ (0,990, 2,010)** |
| 5 | S8-28/09 p. 12 | (AᵀA)₂₂ = 4 | **10** |
| 6 | S9-07/10 p. 4 | ρ(T_J) = 0 | **≈ 1,1744 (no converge)** |
| 7 | S9-07/10 pp. 6-7 | ρ(T_GS) = 0,9351; C_GS = −(D+L)⁻¹b | ρ correcto (0,9351; λ = 0, 0,9351, −0,7129); **C_GS = (D+L)⁻¹b = (3, 0, 7/3)** |
| 8 | S8-30/09 p. 20 | T₁ = 2,402 rotulado ‖·‖∞ | x⁽¹⁾ = (16/9, 13/4, 277/72) es correcto. La suma 2,4028 es la norma 1; **‖·‖∞ = 1,8889** |
| 9 | S9-05/10 p. 23 | Jacobi con M = D converge más rápido | **Las iteraciones son idénticas.** La columna «sin» tampoco es Jacobi; x⁽²⁾ real = (0,25, 0,0625, 0,0625, 0,25) |
| 10 | S8-30/09 pp. 6-7 | MC: det[A\|b] = −11, x = 65/33, y = −29/33 | **Correcto** (control: el procedimiento que se copia está bien) |

## 6. Pendientes

- **Cuaderno de la profesora.** Si se quisiera reproducir exactamente el orden «bajar y luego subir» de Gauss-Jordan, habría que tocar `_escalonar`. No se recomienda tan cerca de la entrega.
- **Respaldo de la Cat. C ante la docente.** Para la defensa conviene saber explicar Faddeev-LeVerrier y Durand-Kerner, o decir que son extensiones rotuladas. Ver `guia_defensa_equipo.md`.
