> **OBSOLETO (13-nov-2026).** Este documento describe procedimientos que se retiraron de Ax por fidelidad académica (Richardson, Faddeev-LeVerrier, Durand-Kerner, matriz de SOR, pivoteo parcial). Estado vigente: `docs/guia_estudio_express.md` y `docs/auditoria/matriz_fidelidad_academica.md`.

# Investigación: el «método de Richardson» en Ax

**Fecha:** 09-nov-2026.

**Pregunta del equipo:** «En el proyecto aparece Richardson y no recordamos haberlo estudiado. ¿Qué es, por qué está y se puede defender?»

**Método:**

1. Búsqueda de «Richardson» en todo el repositorio: código, interfaz, gráficas, pruebas, auditoría y documentación.
2. Revisión de las 457 páginas de los PDF de la profesora (`referencia_oficial_procedimientos.md`).
3. Verificación numérica con el propio código.

---

## 1. Respuestas directas

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Qué aparece en la aplicación? | Una **iteración de Richardson**, x⁽ᵏ⁾ = x⁽ᵏ⁻¹⁾ + (b − A x⁽ᵏ⁻¹⁾), que se ejecuta **solo** dentro de la pestaña de precondicionamiento del Módulo IV, como cuarta fila de la tabla «original frente a precondicionado» |
| 2 | ¿Es una matriz de iteración o una matriz del sistema? | Es un **método iterativo** cuya **matriz de iteración** es **T_R = I − A**. Sobre el sistema precondicionado se convierte en T̃_R = I − D⁻¹A. No es una matriz del sistema: A, b y la solución x no cambian |
| 3 | ¿Qué fórmula utiliza? | Paso: x_nuevo[i] = x_anterior[i] + (b[i] − Σⱼ A[i][j]·x_anterior[j]). Matriz: T_R = I − A (exacta, con fracciones). Con M = D: x⁽ᵏ⁾ = x⁽ᵏ⁻¹⁾ + D⁻¹(b − Ax⁽ᵏ⁻¹⁾), que **es exactamente Jacobi** |
| 4 | ¿Dónde está implementada? | `algebra/modulo_IV_iterativos/metodos.py` (el paso) y `algebra/modulo_IV_iterativos/precondicionamiento.py` (la comparación y ρ). Las rutas exactas están en la sección 2 |
| 5 | ¿Qué función la calcula? | `paso_richardson` (densa), `paso_richardson_csr` (CSR), `ejecutar(..., metodo=RICHARDSON)` (bucle común) y `_rho` (ρ de I − A) |
| 6 | ¿En qué módulo aparece? | **Solo en el Módulo IV**, pestaña «Precondicionamiento». No se ofrece como método en «Ejecutar un método», ni en la comparación ni en convergencia |
| 7 | ¿Qué resultado produce? | En los 7 ejemplos precargados, Richardson **sin** precondicionar no converge: ρ(I − A) va de 4,25 a 12,37 y se detiene por máximo de iteraciones. **Con** M = D converge en 6 de 7, en 7 a 11 iteraciones (tabla 3). El séptimo es el ejemplo de clase donde ni Jacobi converge |
| 8 | ¿Para qué se usa? | Como **evidencia del efecto real del precondicionador diagonal**. Con M = D, Jacobi, Gauss-Seidel y SOR producen **iteraciones idénticas** (demostrado y verificado con fracciones). Richardson es el método estacionario más simple que **no** está normalizado por la diagonal, así que en él M = D sí cambia la convergencia |
| 9 | ¿Aparece en los PDF de la profesora? | **No.** Ninguna de las 457 páginas menciona Richardson. Lo más cercano está en S9-05/10 p. 20: «aplicar método iterativo (Jacobi, Gauss-Seidel, SOR, **etc.**)» al sistema precondicionado |
| 10 | ¿Aparece en el enunciado o en la rúbrica? | **No.** OFICIAL p. 2 exige Jacobi, Gauss-Seidel y SOR. El incentivo de OFICIAL p. 5 pide «implementación correcta de un precondicionador diagonal y **comparación documentada de su efecto**», sin nombrar métodos |
| 11 | ¿Obligatoria, incentivo o extensión voluntaria? | **Extensión voluntaria (categoría C)**, al servicio del incentivo «Precondicionamiento» (hasta 1,5 %). No sustituye ningún requisito |
| 12 | ¿Por qué se consideró correcto incluirla? | La lámina S9-05/10 p. 23 (diap. 19) afirma que M = D acelera Jacobi, y eso **no es reproducible**. Sin Richardson, la «comparación del efecto» solo mostraría «no cambia nada» en los tres métodos del curso. Con Richardson se muestra honestamente **dónde sí actúa** el precondicionador diagonal |
| 13 | ¿Se puede defender matemáticamente? | **Sí.** La demostración tiene tres líneas (sección 4) y la aplicación la verifica con fracciones exactas. Lo que **no** se puede decir es que la profesora lo enseñó |
| 14 | ¿Debe quedar visible o marcarse como extensión? | **Debe quedar, marcado claramente como extensión no vista en clase.** Desde esta revisión, la pestaña lo rotula así (sección 6). Es la pieza que hace defendible el incentivo |

## 2. Referencias exactas: archivo → función → líneas → fórmula

| Archivo | Función / bloque | Líneas* | Fórmula o papel |
|---|---|---|---|
| `algebra/modulo_IV_iterativos/metodos.py` | constante `RICHARDSON` y comentario | 29-32 | «Richardson no es uno de los métodos del enunciado: solo se usa en el análisis del precondicionador diagonal» |
| `algebra/modulo_IV_iterativos/metodos.py` | `paso_richardson(A, b, x_anterior)` | 75-87 | x⁽ᵏ⁾ = x⁽ᵏ⁻¹⁾ + (b − Ax⁽ᵏ⁻¹⁾); el docstring indica que T_R = I − A y que con D⁻¹A es Jacobi |
| `algebra/modulo_IV_iterativos/dispersas.py` | `paso_richardson_csr` | 131-134 | El mismo paso, recorriendo solo los no nulos (CSR) |
| `algebra/modulo_IV_iterativos/ejecucion.py` | `PASOS`, `PASOS_CSR` | 141-144 | Registra el paso para que `ejecutar` lo use con los mismos criterios de parada |
| `algebra/modulo_IV_iterativos/ejecucion.py` | `_ejecutar` | 280 | Richardson no divide entre aᵢᵢ, así que no exige diagonal no nula |
| `algebra/modulo_IV_iterativos/precondicionamiento.py` | docstring del módulo | 1-30 | Demostración de T̃ = T para Jacobi, GS y SOR; T_R = I − A frente a T̃_R = I − D⁻¹A = T_J |
| `algebra/modulo_IV_iterativos/precondicionamiento.py` | `_rho(A, b, metodo, omega)` | 103-115 | Si el método es Richardson, T = I − A (exacta) y ρ con `analizar_matriz` |
| `algebra/modulo_IV_iterativos/precondicionamiento.py` | `analizar_precondicionador` | 128-162 | Recorre `METODOS + (RICHARDSON,)` sobre (A, b) y sobre (D⁻¹A, D⁻¹b) con la misma configuración |
| `algebra/modulo_IV_iterativos/precondicionamiento.py` | `_conclusiones` | 188-196 | Texto «Richardson: ρ(I − A) = … y ρ(I − D⁻¹A) = …» con iteraciones y motivo |
| `interfaz/modulos/modulo_IV_iterativos/pestana_precondicionamiento.py` | `precondicionamiento()` | 18-93 (aviso de extensión: 85) | Chips, tabla, conclusiones, aviso de extensión y gráfica |
| `visualizacion/interactivas.py` | `precondicionador()` | 259-290 | Curvas d_k «Richardson (original)» y «(con M = D)»; la vista se acota cuando una curva diverge |
| `visualizacion/datos_graficas.py`, `visualizacion/tema.py` | `MARCADORES`, `COLORES_METODOS` | — | Marcador y color de cada método |
| `interfaz/portada.py` | lista de incentivos | 55 | Menciona Richardson en «Extensión matemática» |
| `tests/modulo_IV/test_precondicionamiento.py` | `TestPrecondicionadorDiagonal`, `TestRichardson` | 44-108 (Richardson: 77-86 y 98-108) | ρ(I − A) = 3 + 2cos(π/5); Richardson con M = D da las iteraciones de Jacobi; no exige aᵢᵢ ≠ 0 |
| `tests/interfaz/test_graficas_interactivas.py` | prueba de la gráfica | 118-124 | La traza de Richardson conserva los datos completos |
| `auditoria/auditoria_precondicionamiento.py` | auditoría independiente | 9, 74-90 | Bucle propio x ← x + D⁻¹(b − Ax), comparado con Jacobi en cada iteración |
| `casos_prueba/modulo_IV.md` | IV-23 | 67 | Caso documentado: 4,618 → 0,405 |

\* Líneas al 10-nov-2026, después de la reorganización de carpetas (`docs/arquitectura.md`).

## 3. Resultados en los ejemplos precargados (configuración por defecto: criterio A, ε = 10⁻³, k_max = 50)

| Ejemplo | ρ(I − A) | ρ(I − D⁻¹A) = ρ(T_J) | Richardson original | Richardson con M = D | κ∞(A) → κ∞(D⁻¹A) |
|---|---:|---:|---|---|---|
| S8-30/09 10x−y+2z=6 | 12,0 | 0,268 | máximo (50) | tolerancia, 7 | 1,725 → 1,735 |
| S8-30/09 p. 32 (SOR manuscrito) | 12,372 | 0,337 | máximo (50) | tolerancia, 8 | 2,059 → 2,059 |
| S8-30/09 p. 19, solución (2,3,4) | 6,393 | 0,303 | máximo (50) | tolerancia, 8 | 2,385 → 2,078 |
| Tarea II #4/#5 | 5,834 | 0,469 | máximo (50) | tolerancia, 11 | 3,897 → 2,907 |
| S9-07/10 (Jacobi no converge) | 4,713 | 1,174 | máximo (50) | máximo (50) | 108 → 108 |
| Tarea II #3 reordenada | 4,247 | 0,382 | máximo (50) | tolerancia, 10 | 2,927 → 2,634 |
| Tridiagonal [−1, 4, −1] | 4,618 | 0,405 | máximo (50) | tolerancia, 7 | 2,727 → 2,727 |

Lectura correcta:

- M = D **no siempre** baja κ∞. En el primer ejemplo sube ligeramente, y la aplicación lo informa con el chip «κ aumenta».
- Richardson con M = D converge exactamente cuando converge Jacobi, porque es Jacobi.

## 4. Fundamento matemático (para la defensa)

Notación de clase: A = D + L + U (S8-28/09 p. 7) y B = D⁻¹A, b̃ = D⁻¹b (S9-05/10 p. 22).

1. **B tiene diagonal I**, y sus partes estrictas son D⁻¹L y D⁻¹U.
2. **Jacobi sobre B:** T̃_J = −I⁻¹(D⁻¹L + D⁻¹U) = −D⁻¹(L + U) = T_J, y c̃ = b̃ = D⁻¹b = c. Las mismas T y c dan las mismas iteraciones.
   - Lo mismo ocurre con Gauss-Seidel: −(I + D⁻¹L)⁻¹D⁻¹U = −(D + L)⁻¹U.
   - Y con SOR, por el mismo argumento.
   - Intuición: los tres métodos **ya dividen entre aᵢᵢ** en cada componente; volver a dividir no cambia nada.
3. **Richardson:** x⁽ᵏ⁾ = x⁽ᵏ⁻¹⁾ + (b − Ax⁽ᵏ⁻¹⁾) ⇒ T_R = I − A. **No** divide entre aᵢᵢ, así que el escalado sí le afecta.
   - Sobre B: T̃_R = I − D⁻¹A = I − D⁻¹(D + L + U) = −D⁻¹(L + U) = **T_J**.
   - Por eso «Richardson precondicionado con el precondicionador de Jacobi es el método de Jacobi».
4. **Criterio de clase (S8-30/09 p. 36):** ρ(T) < 1 ⇒ converge. En la tridiagonal [−1, 4, −1]:
   - ρ(I − A) = 3 + 2cos(π/5) ≈ 4,618 > 1, así que diverge;
   - ρ(T_J) = cos(π/5)/2 ≈ 0,405 < 1, así que converge.

> **Interpretación (externa):** el método de Richardson (L. F. Richardson, 1911) es la iteración estacionaria x ← x + α(b − Ax). Aquí se usa con α = 1. Es el esquema con el que la bibliografía numérica suele presentar el precondicionamiento: «Richardson precondicionado» es x ← x + M⁻¹(b − Ax). Este marco **no** está en los PDF del curso; se usa como herramienta de demostración.

## 5. Clasificación de TODOS los procedimientos del proyecto

Categorías pedidas por el equipo:

- **A:** enseñado por la profesora (PDF).
- **B:** exigido por el enunciado o la rúbrica.
- **C:** extensión o incentivo.
- **D:** no respaldado por enunciado, rúbrica ni materiales.

| Procedimiento | Categoría | Fuente o justificación |
|---|---|---|
| Ax = b, matriz aumentada | A + B | S6-14/09 pp. 22-25; OFICIAL p. 2 |
| Eliminación de Gauss y sustitución hacia atrás | A + B | S6-14/09 pp. 28-31; OFICIAL p. 2 |
| Gauss-Jordan (RREF) | A + B | S6-14/09 p. 30; S3-24/08 pp. 4-5; OFICIAL p. 2 |
| Pivote «primer no nulo» con intercambio de filas | A | S2-19/08 p. 27 (Fᵢ ↔ Fⱼ); S2-19/08 p. 44 |
| Aviso de pivote numéricamente pequeño (umbral 10⁻¹⁰) | B (umbral propio) | OFICIAL p. 2: «pivotes nulos o numéricamente problemáticos» |
| Pivoteo parcial (opción) | C | Solo se menciona PA = LU (S6-14/09 p. 34); no se enseña |
| Clasificación única / infinitas / inconsistente | A + B | S6-14/09 p. 26; OFICIAL p. 2 |
| Determinante = ± producto de pivotes | A (propiedades) | S2-19/08 p. 38 |
| Inversa por Gauss-Jordan [A \| I] | A + B | S2-19/08 p. 44; OFICIAL p. 2 |
| κ∞ = ‖A‖∞‖A⁻¹‖∞ | A + B | S7-21/09 pp. 17-19; OFICIAL p. 2 |
| Escala de 3 niveles | B | OFICIAL p. 2 (la lámina usa 5) |
| Perturbación absoluta y porcentual, errores relativos ∞ | B | OFICIAL p. 2 |
| Cota ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ | A | S7-21/09 p. 18 |
| Ecuaciones normales resueltas con Gauss | B (A: AᵀAx = Aᵀb) | OFICIAL p. 2; S8-30/09 pp. 5-7 |
| det([A \| b]) ≠ 0 y Cramer como verificación | A | S8-30/09 pp. 4, 6-7 |
| Residuo r y ‖r‖₂ | B | OFICIAL p. 2 |
| Control Aᵀr = 0 | C (pequeña) | Propiedad estándar; no está en los PDF |
| Ajuste lineal y gráfica | B | OFICIAL p. 2; S8-30/09 p. 8 (planteamiento) |
| Jacobi, Gauss-Seidel y SOR por componentes | A + B | S8-30/09 pp. 15, 22, 28; OFICIAL p. 2 |
| x⁽⁰⁾ = bᵢ/aᵢᵢ (opción) | A | S8-30/09 pp. 19, 24 (convención manuscrita) |
| Criterio A ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε y k_max | A + B | S8-30/09 pp. 13, 18; OFICIAL p. 2 |
| Criterio B (residuo) | A | S8-28/09 p. 6; S8-30/09 p. 28 |
| Criterio C (N iteraciones fijas) | C | Práctica de clase («realice 5 iteraciones», S8-30/09 p. 31), no un criterio de parada formal |
| Validación 0 < ω < 2 | B | OFICIAL p. 3 |
| Dominancia diagonal por filas | A + B | S8-30/09 p. 37; OFICIAL p. 2 |
| Reordenar ecuaciones para lograr dominancia | A | S8-30/09 p. 37; S9-05/10 p. 32; T2 #3 |
| A = D + L + U; T_J = −D⁻¹(L+U), c = D⁻¹b; T_GS = −(D+L)⁻¹U | A + B | S9-07/10 pp. 3-7; OFICIAL p. 2 |
| T_ω de SOR en forma matricial | C (requerida en espíritu por B) | No está en los PDF; OFICIAL p. 2 pide «la matriz de iteración correspondiente» |
| det(T − λI) = 0 y ρ = máx\|λ\|; desarrollo de Sarrus en 3×3 | A + B | S9-05/10 pp. 32-34; S9-07/10 p. 4 |
| Polinomio característico por Faddeev-LeVerrier | C | Necesario para n > 3; coincide con Sarrus en 3×3 |
| Raíces por Durand-Kerner y decisión exacta por Schur-Cohn | C | En clase las raíces se obtienen a mano o con calculadora |
| Comparación por iteraciones y error final ‖x⁽ᵏ⁾ − x‖∞ | A + B | S9-05/10 p. 17; OFICIAL p. 2 |
| Gráfica de error frente a iteración | B | OFICIAL p. 2 |
| Almacenamiento CSR y pasos O(nnz) | A (mencionado) + C (incentivo) | S9-05/10 pp. 9, 13; OFICIAL p. 5 |
| Precondicionador M = D, κ(B) frente a κ(A), valores propios de B | A + C | S9-05/10 pp. 19-22; OFICIAL p. 5 |
| Verificación exacta de que T̃ = T | C | Necesaria para documentar el efecto (la lámina p. 23 no es reproducible) |
| **Richardson x ← x + (b − Ax) y T_R = I − A** | **C** (extensión **no vista en clase**) | No está en los PDF, el enunciado ni la rúbrica. Sirve de evidencia del incentivo de precondicionamiento |
| Exportar el historial a CSV y gráficas comparativas adicionales | C | Incentivo «Visualización avanzada», OFICIAL p. 5 |
| Interpretación geométrica 2D/3D (rectas y planos) | A + C | S6-14/09 p. 26 («intersección de planos»); incentivo de visualización |
| Editor de matrices, ejemplos precargados, ayudas | C | Incentivo «Experiencia de usuario», OFICIAL p. 5 |

**Categoría D (sin respaldo):** **ningún procedimiento matemático** del proyecto cae en D.

- Lo más cercano es Richardson: no está en los materiales, pero tiene un propósito claro dentro de un incentivo del enunciado. Por eso es C y no D, con la advertencia de que es **material externo**.
- Los elementos puramente visuales (animaciones, navegación) no son procedimientos matemáticos.

## 6. Decisión y cambios realizados

- **Se conserva.** Quitarlo dejaría la «comparación documentada del efecto» limitada a mostrar efecto nulo en Jacobi, GS y SOR y un κ que a veces no cambia. Así el incentivo de 1,5 % quedaría más débil y la lámina p. 23 sin contrapunto.
- **Se identifica como extensión en la interfaz.**
  - La pestaña «Precondicionamiento» muestra un aviso visible, no solo una nota al pie, que dice que Richardson **no se vio en clase** y que es una herramienta de demostración.
  - La portada lo describe como «extensión».
  - No se cambió ninguna fórmula ni resultado.
- **Cómo explicarlo en la defensa (30 segundos):**

  > «El enunciado pide comparar el efecto del precondicionador diagonal. Al hacerlo encontramos que, con M = D, Jacobi, Gauss-Seidel y SOR dan exactamente las mismas iteraciones, porque ya dividen entre la diagonal; la aplicación lo verifica con fracciones. Para mostrar dónde sí actúa M = D usamos la iteración de Richardson, x ← x + (b − Ax), que no vimos en clase y que no divide entre la diagonal: sin precondicionar su ρ(I − A) es mayor que 1 y diverge; con M = D su matriz pasa a ser −D⁻¹(L + U), la de Jacobi, y converge.»

- **Pregunta para la profesora (opcional, P-8 en `pendientes_docente.md`):** ¿prefiere que la comparación del incentivo se limite a Jacobi, GS y SOR, aunque muestre efecto nulo?
