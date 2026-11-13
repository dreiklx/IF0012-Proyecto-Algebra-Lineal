# Matriz de fidelidad académica (13-nov-2026)

Regla: cada procedimiento matemático activo en Ax debe tener una fuente verificable (PDF y página,
o requisito expreso del enunciado). Lo que no cumple, se retira.

Fuentes: OFICIAL = `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` (enunciado, rúbrica, lista
de cotejo). Láminas = los PDF de clase de `Desktop\ALGEBRA LINEAL`. «Visto» = leído en imagen en
esta revisión. «Solo OCR» no cuenta como verificado.

Estados: **Confirmado** · **Confirmado con diferencia de notación** · **Confirmado con simplificación
equivalente** · **Corregido** · **No aparece en clase** · **Requisito expreso** · **Pendiente de verificación**.

## Módulo I — Sistemas lineales

| Procedimiento | Fuente | Visto | Archivo / función Ax | Prueba | Estado |
|---|---|---|---|---|---|
| Matriz aumentada [A \| b] y eliminación con «−mF_k + F_i» | S6-16/09 p. 29; S3-24/08 pp. 4-5 | Sí (S6-16 p. 29) | `directos._escalonar` | `tests/referencia_profesora` (S6-16 p. 29) | Confirmado con simplificación equivalente: Ax no escribe el paso «−F₂» de normalización |
| Sustitución hacia atrás | S6-16/09 p. 29 | Sí | `directos._sustitucion_atras` | `TestS616SustitucionHaciaAtras` | Confirmado |
| Gauss-Jordan (forma reducida) | S3-24/08 pp. 4-5 y 6-8 | No | `directos.resolver_gauss_jordan` | `tests/modulo_I` | **Pendiente de verificación** (orden de operaciones en imagen) |
| Pivote: primer elemento no nulo, intercambio de filas | S6-14/09 p. 28-34; OFICIAL p. 2 (detección de pivotes nulos) | No | `directos._buscar_pivote` | `tests/modulo_I` | **Pendiente de verificación** en imagen; el requisito de detectar pivotes nulos es requisito expreso (OFICIAL p. 2) |
| Clasificación (rango de A y de [A \| b]) | OFICIAL p. 2 (clasificación automática); S6-14/09 p. 26 (interpretación) | No | `directos._rango_aumentada` | `tests/modulo_I` | Requisito expreso (OFICIAL p. 2). Interpretación geométrica: pendiente de verificar |
| det(A) por eliminación: (−1)^intercambios × producto de pivotes | S2-19/08 p. 38 (propiedades: intercambio, suma de múltiplos, triangular) | Sí | `directos.determinante` | `tests/modulo_I` | Confirmado con simplificación equivalente: la fórmula con pivotes es una consecuencia de las propiedades, no una fórmula escrita en la lámina |
| Validación de dimensiones y matriz singular | OFICIAL p. 3 | — | `validacion.py` | `tests/compartido` | Requisito expreso |

## Módulo II — Condicionamiento

| Procedimiento | Fuente | Visto | Archivo / función Ax | Prueba | Estado |
|---|---|---|---|---|---|
| κ∞(A) = ‖A‖∞ ‖A⁻¹‖∞ en 5 pasos | S7-21/09 p. 19 | Sí | `condicion.numero_condicion_infinito`; `modulo_II_condicionamiento.procedimiento_de_clase` | `TestS721Condicionamiento` (16/5) | Confirmado |
| Norma ∞ = máxima suma de valores absolutos por fila | S7-21/09 p. 19 (pasos 2 y 4) | Sí (p. 19) | `matriz.norma_infinito_matriz`, `sumas_absolutas_por_fila` | `TestS721Condicionamiento` | Confirmado |
| Norma 1 = máxima suma por columna (solo referencia en la gráfica) | S7-21/09 p. 19 («Cálculo con la norma 1») | Sí | `matriz.sumas_absolutas_por_columna` | `tests/modulo_II` | Confirmado (solo visual; no interviene en κ∞) |
| Cota ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ | S7-21/09 p. 18 | Sí | `condicion.analizar_perturbacion` | `tests/modulo_II` | Confirmado |
| Escala 10 / 100 | OFICIAL p. 2 | — | `condicion.clasificar_kappa` | `tests/modulo_II` | Requisito expreso. La lámina S7-21/09 p. 18 usa 5 niveles: diferencia justificada por el enunciado |
| Perturbación absoluta o porcentual de b | OFICIAL p. 2 | — | `condicion.construir_delta_b` | `tests/modulo_II` | Requisito expreso |
| Inversa por Gauss-Jordan [A \| I] → [I \| A⁻¹] | OFICIAL p. 2 («algoritmo implementado por el grupo»); S3-24/08 pp. 6-8 | No | `directos.inversa_gauss_jordan` | `tests/modulo_II` | Requisito expreso para la inversa; orden de pasos: **pendiente de verificación** |
| Gráfica de sumas de fila y columna; gráfica de sensibilidad | Visualización complementaria (autorizada por el usuario) | — | `visualizacion/geometria_modulo_II.py` | `tests/modulo_II/test_visualizaciones.py` | Complementaria. No introduce cálculos: usa las sumas y los errores del núcleo |
| Interpretación geométrica del determinante como área | — | — | — | — | **Retirada**: no aparece en los materiales (S2-19/08 p. 38 solo tiene propiedades) |

## Módulo III — Mínimos cuadrados

| Procedimiento | Fuente | Visto | Archivo / función Ax | Prueba | Estado |
|---|---|---|---|---|---|
| Detección de sistema sobredeterminado y comprobación de b ∈ Col(A) | OFICIAL p. 2; S8-30/09 p. 6 | Sí (p. 6) | `minimos.clasificar_forma` | `TestS830MinimosCuadrados` | Confirmado |
| Matriz de diseño [xᵢ 1] para la recta | S8-30/09 p. 8 (datos en forma de sistema «x + y = 2» …) | Sí (p. 8) | `minimos.ajuste_lineal` | `tests/modulo_III` | Confirmado |
| AᵀA y Aᵀb | S8-30/09 p. 6 y 7 | Sí | `minimos.minimos_cuadrados` (AtA, Atb) | `TestS830MinimosCuadrados` | Confirmado |
| Ecuaciones normales AᵀAx̂ = Aᵀb | S8-30/09 p. 7 | Sí | `minimos.minimos_cuadrados` | `TestS830MinimosCuadrados` | Confirmado |
| Resolución por método directo (Gauss) | OFICIAL p. 2 («método directo ya implementado») | — | `directos.solucion_unica` | `TestS830MinimosCuadrados` | Requisito expreso |
| Regla de Cramer (verificación): det A = 363, det Aₓ = 715, det A_y = −319 | S8-30/09 p. 7 | Sí | `minimos.cramer` | `TestS830MinimosCuadrados` | Confirmado |
| Residual r = b − Ax̂ y ‖r‖₂ | OFICIAL p. 2 («vector residual r y … error») | — | `minimos.minimos_cuadrados` (residuo) | `tests/modulo_III` | Requisito expreso |
| Recta de mejor ajuste y = mx + c | OFICIAL p. 2 | — | `minimos.ajuste_lineal` | `TestS830…` (datos de S8-30 p. 8) | Requisito expreso. La recta del ejemplo (0,75x + 1,2) se calcula; **no aparece en la página 8** |
| Gráfica de datos y recta (obligatoria) con residuos verticales | OFICIAL p. 2; residuo: OFICIAL p. 2 | — | `visualizacion/interactivas.ajuste` | `tests/interfaz`, `tests/modulo_III` | Requisito expreso (gráfica). Los segmentos verticales son representación del residuo |
| Tabla yᵢ, ŷᵢ, rᵢ | — | — | `interfaz/modulos/modulo_III_minimos.tabla_ajuste` | `tests/modulo_III` | Complementaria (mismos valores que el procedimiento) |

## Módulo IV — Métodos iterativos

| Procedimiento | Fuente | Visto | Archivo / función Ax | Prueba | Estado |
|---|---|---|---|---|---|
| Descomposición A = D + L + U | S9-07/10 p. 4 y 6 | Sí | `matriz_iteracion.descomponer` | `TestS907Jacobi` | Confirmado |
| Jacobi: T_J = −D⁻¹(L+U), c_J = D⁻¹b | S9-07/10 p. 4 | Sí | `matriz_iteracion.matriz_iteracion(JACOBI)`; `metodos.paso_jacobi` | `TestS907Jacobi` | Confirmado |
| Jacobi: iteraciones x⁽¹⁾ y x⁽²⁾ | S9-07/10 p. 4-5 | Sí (x⁽²⁾₃ no legible con seguridad) | `ejecucion.ejecutar` | `TestS907Jacobi` | Confirmado (la tercera componente de x⁽²⁾: pendiente) |
| Gauss-Seidel: T_GS = −(D+L)⁻¹U | S9-07/10 p. 6 | Sí | `matriz_iteracion(GAUSS_SEIDEL)` | `TestS907GaussSeidel` | Confirmado |
| Gauss-Seidel: c_GS = (D+L)⁻¹b | S9-07/10 p. 7 | Sí | ídem | `TestS907GaussSeidel` | **Corregido**: la lámina escribe «−(D+L)⁻¹b» y calcula T·b (errata) |
| Gauss-Seidel: componentes (usa valores nuevos) | S8-30/09 p. 22 | No | `metodos.paso_gauss_seidel` | `tests/modulo_IV` | **Pendiente de verificación** en imagen |
| SOR por componentes: x = (1−ω)x⁽ᵏ⁻¹⁾ + ω·x^GS | S8-30/09 pp. 28, 32-33 | No | `metodos.paso_sor` | `tests/modulo_IV` | **Pendiente de verificación** en imagen. Requisito expreso de SOR y de ω ∈ (0,2) (OFICIAL p. 2-3) |
| Criterio A: ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε | S8-28/09 p. 6 (fórmula visto) | Sí | `ejecucion` (CRITERIO_CAMBIO) | `tests/interfaz` | Confirmado. (La versión anterior «relativa» era un error de OCR.) Errata interna de la lámina: ε = 10⁻³ vs 0,01 |
| Criterio B: ‖b − Ax⁽ᵏ⁾‖∞ < ε | S8-28/09 p. 6 | Sí | `ejecucion` (CRITERIO_RESIDUO) | `tests/modulo_IV` | Confirmado |
| Criterio C: N iteraciones y máximo k_max | S8-28/09 p. 6 («número máximo de iteraciones») | Sí | `ejecucion` | `tests/modulo_IV` | Confirmado |
| Dominancia diagonal estricta por filas (suficiente) | S9-07/10 p. 2; S8-30/09 p. 37 | Sí (p. 2) | `convergencia.dominancia_diagonal` | `tests/modulo_IV` | Confirmado (p. 2). p. 37: pendiente |
| Reordenamiento para dominancia | Tarea II #2-3; S9-05/10 pp. 32-33 | No | `convergencia.reordenamiento_dominante` | `tests/modulo_IV` | **Pendiente de verificación** en imagen |
| Radio espectral ρ(T) = máx|λ| | S9-07/10 pp. 3 y 5-7 | Sí | `espectral.radio_espectral` | `tests/modulo_IV/test_espectral.py` | Confirmado, con alcance: solo cuando el polinomio se obtiene y factoriza con procedimientos del curso (ver limitación) |
| det(T − λI) por Sarrus (3×3) | S9-07/10 p. 5-6 | Sí | `polinomio_raices.polinomio_caracteristico` | `TestS907Jacobi`, `test_espectral` | Confirmado |
| Raíces: factor λ y fórmula cuadrática | S9-07/10 p. 7 (λ(...) = 0 y solución) | Sí | `polinomio_raices.raices` | `test_espectral` | Confirmado. (Valores 0,9351 y −0,7129 de la lámina) |
| Teorema: converge ⇔ ρ(T) < 1 | S9-07/10 p. 3 | Sí | `espectral.concluir` | `test_espectral` | Confirmado |
| Error final ‖x⁽ᵏ⁾ − x*‖∞ en la comparación | S9-05/10 p. 17 (auditoría anterior: OCR y visual parcial) | Parcial | `comparacion.comparar_metodos` | `tests/modulo_IV` | **Pendiente de verificación** visual |
| Precondicionador M = D: B = D⁻¹A, b̃ = D⁻¹b | S9-05/10 pp. 19-22 | Solo p. 19 | `precondicionamiento.precondicionar_diagonal` | `tests/modulo_IV/test_precondicionamiento.py` | Confirmado (p. 19 visto; pp. 20-22 pendientes). Efecto: T y c idénticas en Jacobi y GS (exacto) |
| Comparación de κ(A) y κ(D⁻¹A) | S9-05/10 p. 21 (OCR) | No | `precondicionamiento.analizar_precondicionador` | `tests/modulo_IV` | **Pendiente de verificación** en imagen |
| Matrices dispersas CSR | S9-05/10 (OCR: «Compressed Sparse Row») | No | `dispersas.MatrizCSR` | `tests/modulo_IV/test_dispersas.py` | **Pendiente de verificación** en imagen (incentivo, no requisito) |

## Retirados (13-nov-2026)

| Procedimiento | Motivo | Dónde estaba |
|---|---|---|
| Método de Richardson, x⁽ᵏ⁺¹⁾ = x⁽ᵏ⁾ + (b − Ax⁽ᵏ⁾) | No aparece en ninguna lámina (búsqueda OCR en las 457 páginas: 0 coincidencias) | `metodos.py`, `ejecucion.py`, `dispersas.py`, `precondicionamiento.py`, interfaz |
| Faddeev-LeVerrier (coeficientes de det(λI − T) para n ≥ 4) | No aparece en clase | `polinomio_raices.py` |
| Durand-Kerner (raíces de polinomios de grado ≥ 3) | No aparece en clase | `polinomio_raices.py` |
| Decisión exacta de convergencia por Schur-Cohn y λ = ±1 | No aparece en clase | `polinomio_raices.py`, `espectral.py` |
| Matriz de iteración de SOR T_ω y su ρ | No aparece en clase (solo por componentes) | `matriz_iteracion.py`, `espectral.py`, comparación |
| Pivoteo parcial (mayor |elemento|) | No aparece en clase (solo PA = LU) | `directos.py`, interfaz de Módulo I |
| Análisis de convergencia de grado ≥ 3 sin factor λ | El procedimiento de clase no lo resuelve; ρ se declara «no calculado» | `espectral.py` |
| Autovalores de los métodos de Richardson en el precondicionador | Se retira junto con Richardson | `precondicionamiento.py` |

## Limitaciones que quedan (y su efecto)

- **ρ(T_J) del ejemplo S9-07/10 no se calcula:** el polinomio −λ³ − (4/9)λ + 4/3 no tiene factor λ ni factorización por fórmula cuadrática. La lámina daba ρ = 0 por errata. Ax muestra el polinomio y declara que ρ no se calcula con el procedimiento del curso. La conclusión de no convergencia de ese ejemplo no se puede demostrar con ρ.
- **Incentivo «Extensión matemática» (1 %):** las extensiones en las que se basaba (Faddeev-LeVerrier, Durand-Kerner, SOR matricial, decisiones exactas) se retiraron. **No se reclama.** Impacto: pérdida del incentivo de hasta 1 %. La rúbrica exige extensiones «pertinentes, correctamente implementadas y defendidas»; sin respaldo en clase no cumplen la regla de fidelidad.
- **Incentivo «Precondicionamiento» (1,5 %):** se mantiene con M = D (S9-05/10). La demostración con Richardson se retiró; la verificación se hace con Jacobi y Gauss-Seidel.
- **Procedimientos aún sin verificación visual:** ver las filas «Pendiente de verificación». Son obligatorios para el 100 % de fidelidad.

## Estado global

- Procedimientos activos con fuente: ver tabla.
- Pendientes de verificación visual: Gauss-Jordan, pivote, inversa, componentes de Gauss-Seidel y SOR, reordenamiento, error final, κ del precondicionador, CSR y las páginas listadas en `pruebas_ejemplos_profesora.md`.
- No se afirma una fidelidad del 100 %: quedan páginas y procedimientos sin verificar visualmente.
