# Resumen de la lógica por módulo — material de estudio para la defensa

**Versión:** 03-nov-2026. Es la versión condensada de [guia_defensa_equipo.md](guia_defensa_equipo.md); allí están las demostraciones y las 34 preguntas con su respuesta completa.
**Regla de oro:** la docente elige al menos dos módulos y puede pedir un caso no preparado. **Estudien los cuatro.**

## Lo que hay que saber de memoria en cualquier módulo

1. **Arquitectura.** `algebra/` (matemática en Python puro, sin NumPy) → `interfaz/` (Streamlit: lee el texto y muestra los resultados) → `visualizacion/` (Matplotlib: solo dibuja).
2. **Aritmética.**
   - Exacta (`Fraction`) en los Módulos I, II y III y en la matriz T.
   - `float` en las iteraciones y en las raíces del polinomio.
   - El porqué: la clasificación sin redondeos; los iterativos son aproximaciones.
3. **Validación.** `leer_numero` convierte texto en `Fraction` y señala la celda errónea. `validar_sistema` y `validar_cuadrada` comprueban las dimensiones. Nunca se cierra la aplicación.
4. **Autoverificación que se puede mostrar en vivo:**

   | Módulo | Comprobación |
   |---|---|
   | I | b − Ax = 0 |
   | II | A·A⁻¹ = I |
   | III | Aᵀr = 0 |
   | IV | r_k pequeño; Σλ = traza(T) |

5. **Evidencia.** 228 pruebas OK y la auditoría aleatoria con 0 fallos. Los valores esperados son independientes: **no** salen de las láminas, varias de las cuales tienen errores.

---

## Módulo I — Sistemas lineales (`algebra/directos.py`)

**Qué hace.** Resuelve Ax = b (m×n cualquiera) con Gauss o Gauss-Jordan, muestra cada operación y clasifica el sistema.

**Funciones que hay que identificar:**

- `resolver_gauss` y `resolver_gauss_jordan` llaman a `_resolver`, que usa `_escalonar`, `_rango_aumentada` y `_sustitucion_atras`;
- `inversa_gauss_jordan`, `determinante` y `solucion_unica` (esta la usan los otros módulos).

**Lógica de `_escalonar`** (hay que poder explicarla línea por línea):

1. Para cada columna, `_buscar_pivote` busca, desde la fila actual hacia abajo, un elemento ≠ 0 (o el mayor con pivoteo parcial).
2. Si no lo encuentra, la columna no tiene pivote y su variable es **libre**.
3. Si el pivote está en otra fila, intercambia las filas: el `Paso` registra el motivo y `signo = −signo`.
4. `producto *= pivote`, para el determinante.
5. Aviso si |pivote| < 10⁻¹⁰·máx|aᵢⱼ|.
6. Gauss anula debajo con Fᵢ → Fᵢ − (aᵢc/a_rc)·F_r. Gauss-Jordan además divide la fila entre el pivote y anula arriba.

**Fórmulas:**

- multiplicador m = aᵢc / a_rc;
- x_c = (b'_r − Σ_{j>c} u_rj x_j) / u_rc;
- det = (−1)^intercambios · Π pivotes;
- [A | I] → [I | A⁻¹].

**Clasificación (rangos = número de pivotes):**

| Condición | Resultado | Señal en la matriz |
|---|---|---|
| rango(A) < rango([A\|b]) | INCONSISTENTE | fila [0 … 0 \| c], c ≠ 0 |
| rango(A) = rango([A\|b]) = n | UNICA | — |
| rango(A) = rango([A\|b]) < n | INFINITAS | x = xₚ + Σ tⱼvⱼ; xₚ con libres = 0; vⱼ resuelve Av = 0 con la libre j = 1 |

**Ejemplos para practicar:**

| Ejemplo | Resultado |
|---|---|
| «Pivote nulo» | F1 ↔ F2; x = (1, 1, 1); det = −1 |
| «Infinitas» | x = (1/2, 1/2, 0) + t(−1/2, −1/2, 1) |
| «Inconsistente» | rangos 2 < 3 |
| 2x + y = 5, x − y = 1 | F2 → F2 − ½F1; x = (2, 1); det = −3 |

**Preguntas clave:**

- ¿Qué pasa con un pivote 0? → Se intercambian filas; si no hay ninguna fila disponible, la variable es libre.
- ¿Por qué cambia el signo del determinante al intercambiar filas?
- ¿Qué aporta el pivoteo parcial? → Estabilidad en punto flotante; con fracciones, la misma solución.
- ¿Cómo se obtiene la forma paramétrica?
- ¿Por qué A singular ⇔ falta un pivote ⇔ det = 0?

---

## Módulo II — Condicionamiento (`algebra/condicion.py`)

**Qué hace.** Calcula κ∞(A), lo interpreta y compara x con x̃ cuando b se perturba.

**Funciones:**

- `numero_condicion_infinito`, que usa `norma_infinito_matriz`, `inversa_gauss_jordan` y `clasificar_kappa`;
- `construir_delta_b`;
- `analizar_perturbacion`, que resuelve con `solucion_unica` dos veces y llama a `_interpretar`.

**Fórmulas:**

- ‖A‖∞ = máxᵢ Σⱼ|aᵢⱼ| (mayor suma de fila) y ‖v‖∞ = máx|vᵢ|;
- **κ∞ = ‖A‖∞‖A⁻¹‖∞**, con κ ≥ 1;
- escala del proyecto: κ < 10 baja, 10 ≤ κ < 100 moderada, κ ≥ 100 alta;
- **‖Δx‖/‖x‖ ≤ κ·‖Δb‖/‖b‖**;
- porcentual: Δbᵢ = p/100·bᵢ, de modo que ‖Δb‖/‖b‖ = p/100.

**Demostración de la cota** (hay que saberla):

1. Δx = A⁻¹Δb, de modo que ‖Δx‖ ≤ ‖A⁻¹‖‖Δb‖.
2. ‖b‖ ≤ ‖A‖‖x‖.
3. Se multiplican ambas desigualdades.

**Casos especiales:**

- A singular → `MATRIZ_SINGULAR`: κ no está definido y no es lo mismo que κ grande.
- ‖b‖ = 0 o ‖x‖ = 0 → el error relativo no está definido y se avisa.

**Ejemplos:**

| Ejemplo | Resultado |
|---|---|
| [[1, 2], [3, 1]] | ‖A‖ = 4, A⁻¹ = [[−1/5, 2/5], [3/5, −1/5]], ‖A⁻¹‖ = 4/5, κ = 16/5 (baja) |
| [[4, 1], [1, 3]] | κ = 25/11 ≈ 2.27 |
| [[1, 1], [1, 1.0001]] | κ ≈ 40004; x pasa de (1, 1) a (0, 2) con Δb₂ = 0.0001 |
| I + 10J | κ = 41; con Δb = (1, −1, 1) la amplificación es exactamente 41 (peor caso) |

**Preguntas clave:**

- ¿Qué indica κ?
- ¿Por qué la amplificación observada puede ser menor que κ?
- ¿Singular o mal condicionada?
- ¿Por qué κ ≥ 1?
- ¿Cómo se calcula la inversa? → Con nuestro Gauss-Jordan, verificando A·A⁻¹ = I.

---

## Módulo III — Mínimos cuadrados (`algebra/minimos.py`)

**Qué hace.** Para m > n busca x̂ que minimiza ‖b − Ax‖₂, y ajusta rectas y = mx + c.

**Funciones:**

- `clasificar_forma`;
- `minimos_cuadrados`, que usa `transpuesta`, `multiplicar_matrices`, `resolver_gauss` y `norma_2_cuadrado_vector`;
- `ajuste_lineal`, que construye la matriz de diseño `[[xᵢ, 1]]`;
- `cramer` y el campo `det_aumentada`: el **procedimiento de clase** (S8-30/09 pp. 6-7), mostrado como verificación;
- la gráfica, `grafica_ajuste`.

**Fórmulas:**

- **AᵀA x̂ = Aᵀb**;
- r = b − Ax̂; ‖r‖₂ = √Σrᵢ² (‖r‖₂² es exacta, solo la raíz es `float`);
- **Aᵀr = 0**;
- para la recta: AᵀA = [[Σx², Σx], [Σx, k]] y Aᵀb = [Σxy, Σy].

**Por qué (hay que saberlo):**

- ∇‖b − Ax‖² = −2Aᵀ(b − Ax) = 0.
- Geométricamente, Ax̂ es la proyección de b sobre Col(A), de modo que r ⟂ columnas.
- La solución es única ⇔ las columnas son independientes ⇔ AᵀA es invertible.

**Casos especiales:**

- AᵀA singular → no se presenta x̂.
- Menos de 2 puntos, todos los x iguales o listas de distinto largo → `ErrorAjuste`.
- Si b ∈ Col(A), el residuo es 0 y x̂ es la solución exacta.

**Ejemplos:**

| Ejemplo | Resultado |
|---|---|
| A = [[1, 3], [3, −2], [−2, 5]], b = (−1, 8, −8) | x̂ = (65/33, −29/33), r = (−1/3, 1/3, 1/3), ‖r‖₂ ≈ 0.577 |
| Puntos (1, 2), (2, 2.5), (3, 3.7), (4, 4.1) | [[30, 10], [10, 4]]·(m, c) = (34.5, 12.3), de modo que **y = 3/4 x + 6/5** |

**Preguntas clave:**

- ¿Por qué las ecuaciones normales?
- ¿Qué significa Aᵀr = 0?
- ¿Qué indica ‖r‖₂?
- ¿Cuándo no hay x̂ único?
- ¿Con qué método se resuelven? → El Gauss propio del Módulo I, porque lo exige el enunciado. Cramer, que usa la docente, se muestra como verificación y coincide: det([A|b]) = −11; 363, 715 y −319.

---

## Módulo IV — Métodos iterativos y convergencia (`algebra/iterativos.py`, `algebra/espectral.py`, `algebra/dispersas.py`)

**Qué hace.** Jacobi, Gauss-Seidel y SOR con criterios configurables; comparación homogénea; dominancia diagonal; matriz de iteración y ρ(T).

**Funciones:**

- pasos: `paso_jacobi`, `paso_gauss_seidel`, `paso_sor`;
- `validar_configuracion` y `ejecutar`/`_ejecutar`, el bucle común;
- `dominancia_diagonal`, `reordenamiento_dominante` (sugiere el orden de las ecuaciones, como en la Tarea II), y `comparar_metodos` con `configuraciones_homogeneas`;
- `matriz_iteracion`, `polinomio_caracteristico`, `desarrollo_sarrus` (procedimiento de clase en 3×3), `raices`/`durand_kerner`, `analizar_matriz`, `concluir` y `radio_espectral`;
- `a_csr` y `paso_*_csr`;
- incentivo: `precondicionar_diagonal`, `analizar_precondicionador` y `paso_richardson`.

**Fórmulas por componentes:**

- Jacobi: xᵢ⁽ᵏ⁾ = (bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁻¹⁾)/aᵢᵢ.
- Gauss-Seidel: lo mismo, pero con xⱼ⁽ᵏ⁾ para j < i (en el código: actualiza sobre la misma lista).
- SOR: xᵢ⁽ᵏ⁾ = (1 − ω)xᵢ⁽ᵏ⁻¹⁾ + ω·[valor de GS]. Con ω = 1 es GS.

**Matrices de iteración** (A = D + L + U con los signos de A; x⁽ᵏ⁾ = Tx⁽ᵏ⁻¹⁾ + c):

| Método | T | c | De dónde sale |
|---|---|---|---|
| Jacobi | −D⁻¹(L + U) | D⁻¹b | Dx = b − (L + U)x |
| Gauss-Seidel | −(D + L)⁻¹U | (D + L)⁻¹b | (D + L)x = b − Ux |
| SOR | (D + ωL)⁻¹[(1 − ω)D − ωU] | ω(D + ωL)⁻¹b | La fórmula por componentes multiplicada por aᵢᵢ |

**Métricas** (no son lo mismo):

- d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞;
- r_k = ‖b − Ax⁽ᵏ⁾‖∞ (sistema original);
- e_k = ‖x⁽ᵏ⁾ − x*‖∞ (x* del Gauss exacto; solo en la comparación). Es el **«Error final (‖x⁽ᵏ⁾ − x‖∞)»** de la tabla de la lámina S9-05/10 p. 17.

**Criterios de parada** (desigualdad estricta):

- A: d_k < ε (predeterminado);
- B: r_k < ε (puede parar en k = 0);
- C: N fijas, que **no** demuestran convergencia.

La norma ∞ es el **máximo**, no la suma.

**Códigos:**

| Código | Significado |
|---|---|
| `TOLERANCIA_CAMBIO` / `TOLERANCIA_RESIDUO` | Se cumplió el criterio |
| `N_COMPLETADAS` | Se hicieron las N iteraciones |
| `MAXIMO_ITERACIONES` | **No** significa que diverja |
| `ERROR_NO_FINITO` | Desbordamiento; **no** es una prueba de divergencia |
| `DIAGONAL_CERO` | Algún aᵢᵢ = 0 |
| `ENTRADA_INVALIDA` / `ERROR_INTERNO` | `ejecutar` nunca lanza excepciones |

**Convergencia:**

- **Teorema:** e⁽ᵏ⁾ = Tᵏe⁽⁰⁾; el método converge para todo x⁽⁰⁾ ⇔ **ρ(T) = máx|λ| < 1**. Cuanto menor es ρ, más rápido.
- **Dominancia diagonal estricta** (|aᵢᵢ| > Σ_{j≠i}|aᵢⱼ|) ⇒ ‖T_J‖∞ < 1 ⇒ converge. Es **suficiente, no necesaria**.
- **A singular** ⇒ Av = 0 ⇒ Tv = v (porque T = I − M⁻¹A) ⇒ λ = 1 ⇒ no converge.

**Cálculo de ρ(T)** (paso a paso):

1. T exacta con fracciones (inversas con nuestro Gauss-Jordan).
2. **Faddeev-LeVerrier:** M₀ = 0; Mₖ = TMₖ₋₁ + cₖ₋₁I; cₖ = −tr(TMₖ)/k. Da p(λ) = det(λI − T) exacto, igual que Sarrus en 3×3.
3. Raíces:
   - λ = 0, exactas;
   - grado ≤ 2: fórmula cuadrática y **Schur-Cohn** exacto (|c₂| < 1 y |c₁| < 1 + c₂);
   - grado ≥ 3: **Durand-Kerner**, zᵢ ← zᵢ − p(zᵢ)/Π_{j≠i}(zᵢ − zⱼ), que encuentra también las raíces complejas.
4. Verificar: |p(λ)| ≈ 0 y Σλ = traza(T).
5. `concluir`:
   - p(±1) = 0 exacto → no converge;
   - si hay decisión exacta, se usa esa;
   - si el cálculo no es fiable o |ρ − 1| < 10⁻⁹ (10⁻⁶ con raíces casi repetidas) → INDETERMINADO;
   - si n > 8, no se calcula.

**Ejemplos** (ε = 10⁻³, x⁽⁰⁾ = 0, ω = 1.2):

| Ejemplo | Iteraciones J / GS / SOR | ρ_J / ρ_GS / ρ_SOR | Nota |
|---|---|---|---|
| S: 10x − y + 2z = 6, … | 7 / 4 / 6 | 0.268 / 0.043 / 0.217 | Dominante; x* = (217/208, 59/26, −225/208) |
| S9-07/10 [[3, 3, 3], [3, 3, 2], [−3, −2, 3]] | 50 / 50 / 50 (k_max) | 1.174 / 0.935 / ≥ 1 | J: par complejo, polinomio −λ³ − 4/9λ + 4/3. GS converge lento. SOR (ω = 6/5): λ = −1 exacto |
| 2×2 [[4, 1], [2, 5]] | — | √0.1 ≈ 0.316 / 0.1 | Faddeev: c₁ = 0, c₂ = −1/10; Schur-Cohn exacto |

**Preguntas clave:**

- Diferencias entre los tres pasos en el código.
- ¿Qué criterio y qué norma se usan?
- ¿Llegar a k_max significa divergencia? → No.
- ¿La dominancia garantiza convergencia? ¿Y si no se cumple?
- ¿Cómo se calcula ρ sin bibliotecas?
- ¿Por qué no el método de la potencia? → Falla con pares complejos y con ±μ.
- ¿Qué pasa con raíces múltiples o con ρ ≈ 1? → Indeterminado en lugar de una conclusión falsa.
- ¿Qué es «error final»? → ‖x⁽ᵏ⁾ − x*‖∞, igual que en la lámina S9-05/10 p. 17; también se muestran d y r.
- ¿Cómo sigue la aplicación el procedimiento de clase del radio espectral? → En 3×3 muestra tr(T), Σ menores y det(T) por Sarrus, y comprueba que el polinomio coincide.
- ¿Qué hace ω y por qué 0 < ω < 2 no basta?
- ¿Qué aporta CSR? → O(nnz) por iteración, con las mismas iteraciones.
- ¿Por qué el precondicionador M = D no cambia las iteraciones? → En D⁻¹A la diagonal es I, así que T̃_J = −D⁻¹(L + U) = T_J, y lo mismo pasa con GS y SOR. Sí cambian κ (si la diagonal no es uniforme), el residuo y Richardson (que se convierte en Jacobi).

**Precondicionamiento** (pestaña «Precondicionamiento diagonal»), ejemplo con la tridiagonal [−1, 4, −1]:

| | Original | Con M = D |
|---|---|---|
| κ∞ | 30/11 | 30/11 (B = A/4) |
| Jacobi / GS / SOR | 7 / 5 / 7 | 7 / 5 / 7, idénticas (T y c iguales, exacto) |
| Richardson | no converge (ρ(I − A) ≈ 4.618) | converge (ρ = ρ(T_J) ≈ 0.405) |

La diapositiva 19 de S9-05/10 afirma que Jacobi mejora: no es reproducible y hay que saber explicar por qué.

---

## Limitaciones que hay que defender (sin ocultarlas)

1. **Autovalores múltiples:**
   - raíz doble: precisión ≈10⁻⁸; se avisa y se decide con la banda de 10⁻⁶;
   - raíz triple o mayor: Durand-Kerner no suele converger, así que es «no fiable» → **indeterminado**.
2. **ρ ≈ 1** → indeterminado dentro de la banda, salvo con una decisión exacta.
3. **n > 8** → no se calcula ρ.
4. **Durand-Kerner y Faddeev-LeVerrier no se vieron en clase.** Son una extensión verificada; el alcance está pendiente con la docente (P-5 en [pendientes_docente.md](pendientes_docente.md)).
5. **Iterativos en `float`:** las diferencias se justifican por ε.
6. **Precondicionador M = D:** no acelera Jacobi, GS ni SOR. Es un teorema y no una falla.
7. **Uso de IA:** está declarado. No hay requisito de autorización previa; lo exigible es declararlo y defender el trabajo. No digan que la docente lo autorizó expresamente.

## Lista de comprobación personal antes de la defensa

- [ ] Instalé y abrí la aplicación en mi computadora con `ejecutar.bat`.
- [ ] Ejecuté las pruebas (204 OK).
- [ ] Hice la demostración de los cuatro módulos (guion en la guía, parte F) y obtuve los resultados esperados.
- [ ] Sé explicar `_escalonar`, `analizar_perturbacion`, `minimos_cuadrados`, `_ejecutar` y `radio_espectral` sin leer.
- [ ] Sé deducir la cota de κ, las ecuaciones normales y las tres matrices T, y enunciar el teorema de ρ.
- [ ] Practiqué un caso no preparado: escribir los datos, interpretar y verificar.
