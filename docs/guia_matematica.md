# Guía matemática del proyecto

Referencias:

- «OFICIAL»: instrucciones del proyecto.
- «S8-30/09 p. 16»: archivo de clase y página del PDF.
- **[Extensión]**: procedimiento que no aparece en los materiales del curso. Se explica por qué fue necesario.

---

## 1. Operaciones básicas (`algebra/compartido/matriz.py`)

- **Producto:** si A es m×p y B es p×n, (AB)ᵢⱼ = Σₖ aᵢₖ bₖⱼ. Requiere que las columnas de A coincidan con las filas de B.
- **Norma infinito de un vector:** ‖v‖∞ = máxᵢ |vᵢ|. Es el **máximo**, no la suma. La suma Σ|vᵢ| es la norma 1. Se cumple ‖v‖∞ ≤ ‖v‖₂ ≤ ‖v‖₁.
- **Norma infinito de una matriz:** ‖A‖∞ = máxᵢ Σⱼ |aᵢⱼ|, la mayor suma de fila (S7-21/09 p. 17).
- **Residuo:** r = b − Ax. r = 0 si y solo si x es solución exacta.

Ejemplo comprobado: ‖(−2, 1, 7)‖∞ = 7 (S3-26/08 p. 25); ‖[[1, 2], [3, 1]]‖∞ = 4.

## 2. Eliminación de Gauss y Gauss-Jordan (`algebra/modulo_I_sistemas/directos.py`)

**Objetivo:** resolver A x = b y clasificar el sistema (OFICIAL p. 2, Módulo I).

**Procedimiento** (S6-14/09 pp. 27-29; S6-16/09 pp. 24-29):

1. Formar la matriz aumentada [A | b].
2. Para cada columna c, buscar un pivote no nulo desde la fila actual hacia abajo.
   - Si el elemento diagonal es 0, se **intercambian filas** (Fᵣ ↔ Fₚ).
   - Si no hay ningún elemento no nulo, la columna no tiene pivote y su variable es **libre**.
3. Anular los elementos bajo el pivote con Fᵢ → Fᵢ − mᵢᵣ·Fᵣ, donde mᵢᵣ = aᵢc / aᵣc.
4. **Gauss-Jordan** además divide la fila del pivote entre el pivote, para que valga 1, y anula también los elementos de arriba. El resultado es la forma escalonada reducida.
5. **Gauss** termina con sustitución hacia atrás: xc = (b'ᵣ − Σ_{j>c} uᵣⱼ xⱼ) / uᵣc.

**Clasificación** (criterio de Rouché-Frobenius), con n = número de incógnitas:

| Condición | Tipo |
|---|---|
| rango(A) < rango([A\|b]) | inconsistente: hay una fila [0 … 0 \| c] con c ≠ 0 |
| rango(A) = rango([A\|b]) = n | solución única |
| rango(A) = rango([A\|b]) < n | infinitas soluciones, con n − rango variables libres |

**Infinitas soluciones.**

- La solución general es x = xₚ + t₁v₁ + … + t_q v_q.
- xₚ se obtiene dando el valor 0 a las variables libres.
- Cada vᵢ resuelve el sistema homogéneo con la libre i igual a 1 y las demás iguales a 0.

**Decisiones numéricas.**

- **Aritmética exacta** con `fractions.Fraction`: un pivote es nulo solo si es exactamente 0. Por eso la clasificación no depende de ninguna tolerancia, y un sistema singular nunca se convierte en uno de solución única por redondeo.
- **Pivote:** por defecto, la primera fila con elemento no nulo, como en clase. Opcionalmente, **pivoteo parcial** (el mayor |elemento|), que en punto flotante reduce el error de redondeo. Con fracciones exactas ambos dan la misma solución. Cada intercambio queda registrado con su motivo.
- **Pivote «numéricamente problemático»:** se advierte si |pivote| < 10⁻¹⁰·máx|aᵢⱼ|. Es un **umbral técnico**, no matemático: la solución exacta sigue siendo correcta, pero en punto flotante ese pivote amplificaría los errores.
- **Determinante:** det(A) = (−1)^(número de intercambios) · Π pivotes. Se basa en la propiedad de que sumar a una fila un múltiplo de otra no cambia el determinante (S3-24/08 p. 22).

**Ejemplo comprobado.** x + y + z = 6, 2x + y − z = 3, −x + y + 2z = 7 da x = (1/3, 4, 5/3) (S6-16/09 p. 29).

**Lámina corregida.** S6-14/09 p. 29: 2x + y − z = 1, x − 3y + 2z = 4, 3x + 2y + z = 0.

- La lámina da (1/2, −1, −1), que no cumple la 2.ª ecuación: 0.5 + 3 − 2 = 1.5 ≠ 4.
- La solución correcta es **(19/20, −5/4, −7/20)**. En el paso F3 → F3 + (1/7)F2 la fila resultante es [0, 0, 20/7 | −1], no −10/7.

## 3. Inversa por Gauss-Jordan

**Procedimiento:** [A | I] → [I | A⁻¹] (S3-24/08 pp. 6 y 28). Si alguna columna no tiene pivote no nulo, A es **singular** y no tiene inversa.

**Verificación:** A·A⁻¹ = I. Se comprueba exactamente en cada cálculo.

**Ejemplo:** [[2, 1], [1, 1]]⁻¹ = [[1, −1], [−1, 2]].

**Corrección del manuscrito S3-24/08 p. 8:** la inversa de [[1, 2, 3], [2, −1, −1], [3, 0, −1]] es [[1/8, 1/4, 1/8], [−1/8, −5/4, 7/8], [3/8, 3/4, −5/8]].

## 4. Número de condición y sensibilidad (`algebra/modulo_II_condicionamiento/condicion.py`)

**Fórmula** (OFICIAL p. 2):

> κ∞(A) = ‖A‖∞ · ‖A⁻¹‖∞

A⁻¹ se calcula con nuestro Gauss-Jordan.

**Propiedades:** κ ≥ 1; κ(I) = 1.

**Clasificación operativa del proyecto** (OFICIAL p. 2):

| κ∞ | Sensibilidad |
|---|---|
| κ < 10 | baja |
| 10 ≤ κ < 100 | moderada |
| κ ≥ 100 | alta |

Es un criterio del proyecto, no una frontera matemática universal. Las láminas (S7-21/09 p. 18) usan otra escala de 5 niveles.

**Perturbación de b:** se resuelven A x = b y A x̃ = b + Δb, y se calcula Δx = x̃ − x.

**Errores relativos:** ‖Δb‖∞/‖b‖∞ y ‖Δx‖∞/‖x‖∞. Si un denominador es 0, el cociente no está definido y se informa.

**Cota teórica** (S7-21/09 p. 18):

> ‖Δx‖/‖x‖ ≤ κ(A) · ‖Δb‖/‖b‖

κ es el **peor caso**: según la dirección de Δb, la amplificación observada puede ser menor.

**Singular frente a mal condicionada:**

- Si A es singular, κ no está definido (es infinito) y el sistema no tiene solución única.
- Si A es invertible con κ grande, el sistema tiene solución única, pero esa solución es muy sensible a los datos.

**Ejemplos comprobados:**

- A = [[4, 1], [1, 3]]: κ∞ = 5·(5/11) = 25/11. Con Δb = (0.01, −0.01), x̃ = (26/275, 139/220) ≈ (0.0945, 0.6318). **La lámina S7-21/09 p. 20 da 0.6309, por un error aritmético.**
- A = I + 10J (3×3): (I + 10J)⁻¹ = I − (10/31)J, κ∞ = 41. Con Δb = (1, −1, 1) la amplificación es exactamente 41 = κ: es el caso peor.

## 5. Mínimos cuadrados (`algebra/modulo_III_minimos/minimos.py`)

**Planteamiento.** Si A es m×n con m > n, el sistema es **sobredeterminado** y en general b ∉ Col(A) (S8-30/09 p. 5). La solución de mínimos cuadrados x̂ minimiza ‖b − Ax‖₂ y cumple las **ecuaciones normales**:

> AᵀA x̂ = Aᵀb

**Procedimiento** (OFICIAL p. 2):

1. Detectar la forma del sistema (sobredeterminado, cuadrado o subdeterminado).
2. Calcular Aᵀ, AᵀA y Aᵀb con productos propios.
3. Resolver las ecuaciones normales con **nuestro Gauss**. En clase se usó Cramer (S8-30/09 p. 7); el enunciado exige «un método directo ya implementado».
4. Calcular r = b − Ax̂ y ‖r‖₂ = √(Σ rᵢ²). ‖r‖₂² es exacta; solo la raíz final se calcula en punto flotante.

**Propiedad de control:** Aᵀr = 0. El residuo es ortogonal a las columnas de A.

**Caso especial.** Si las columnas de A son dependientes, AᵀA es singular y x̂ no es único. Se informa y no se presenta ningún x̂.

**Ajuste lineal y = m x + c:**

- Matriz de diseño A = [[x₁, 1], …, [x_k, 1]] y b = (y₁, …, y_k).
- Requiere al menos 2 puntos con x distintos.

**Ejemplos comprobados:**

- S8-30/09 pp. 6-7: x̂ = (65/33, −29/33) y r = (−1/3, 1/3, 1/3).
- Tarea II #1: x̂ = (4/11, 15/11).
- Puntos (1, 2), (2, 2.5), (3, 3.7), (4, 4.1): y = 0.75x + 1.2.

## 6. Métodos iterativos (`algebra/modulo_IV_iterativos/`)

**Descomposición:** A = D + L + U, con L y U estrictamente inferior y superior y **los signos que tienen en A**.

**Fórmulas por componentes** (i = 1…n):

- **Jacobi** (S8-30/09 p. 15):
  xᵢ⁽ᵏ⁾ = (bᵢ − Σ_{j≠i} aᵢⱼ xⱼ⁽ᵏ⁻¹⁾) / aᵢᵢ
- **Gauss-Seidel** (S8-30/09 p. 22), que usa los valores ya actualizados:
  xᵢ⁽ᵏ⁾ = (bᵢ − Σ_{j<i} aᵢⱼ xⱼ⁽ᵏ⁾ − Σ_{j>i} aᵢⱼ xⱼ⁽ᵏ⁻¹⁾) / aᵢᵢ
- **SOR** (S8-30/09 p. 28):
  xᵢ⁽ᵏ⁾ = (1 − ω) xᵢ⁽ᵏ⁻¹⁾ + ω · [valor de Gauss-Seidel]

Con ω = 1, SOR coincide con Gauss-Seidel. Hay una prueba automática que lo verifica bit a bit.

**Métricas registradas en cada iteración:**

- d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞: cambio entre iteraciones. No existe en k = 0.
- r_k = ‖b − Ax⁽ᵏ⁾‖∞: residuo con la A y la b **originales**.
- e_k = ‖x⁽ᵏ⁾ − x*‖∞: error respecto a la solución x* del método directo. Solo se calcula en la comparación.

**Las tres métricas miden cosas distintas.** d pequeño no implica e pequeño: cuando ‖T‖ < 1, ‖x − x⁽ᵏ⁾‖ ≤ ‖T‖/(1 − ‖T‖)·d_k. Tampoco r pequeño implica e pequeño: ‖e‖/‖x‖ ≤ κ·‖r‖/‖b‖.

**Criterios de parada** (configurables por el usuario; desigualdad estricta):

| Criterio | Regla | Fuente |
|---|---|---|
| A (predeterminado) | primer k ≥ 1 con d_k < ε, o k_max | El más frecuente en las clases: S8-30/09 pp. 18, 23, 29, 34, 39, 40; S9-05/10 pp. 18, 26 |
| B | primer k ≥ 0 con r_k < ε, o k_max | S8-28/09 p. 6; S8-30/09 p. 28 |
| C | exactamente N iteraciones; no demuestra convergencia | S8-30/09 p. 31; S9-05/10 pp. 14-16, 26 |

**Atención:** los manuscritos S8-30/09 pp. 19-20 y 24 **suman** las diferencias y escriben ∞. La aplicación usa el máximo, que es la definición de la norma ∞. Ejemplo: d₁ = 1.8889, no 2.402.

**Motivos de terminación:**

- tolerancia satisfecha (por el cambio o por el residuo);
- N completadas;
- **máximo de iteraciones sin satisfacer el criterio**, que no se presenta como divergencia;
- valores no finitos, que se presentan como error numérico y no como demostración de divergencia;
- diagonal cero;
- entrada inválida.

**Ejemplo comprobado.** Sistema S, 10x − y + 2z = 6, −x + 11y − z = 25, 2x − y + 10z = −11, con x⁽⁰⁾ = 0 y ε = 10⁻³:

| Método | Iteraciones |
|---|---|
| Jacobi | 7 |
| Gauss-Seidel | 4 |
| SOR (ω = 1.2) | 6 |

La solución exacta es (217/208, 59/26, −225/208). **Las láminas de S8 dan para este sistema tres soluciones distintas, todas incorrectas.**

## 7. Dominancia diagonal (`dominancia_diagonal`)

**Definición:** A es estrictamente diagonalmente dominante por filas si |aᵢᵢ| > Σ_{j≠i} |aᵢⱼ| para todo i (S8-30/09 p. 37).

**Qué permite concluir:**

- Si se cumple, Jacobi y Gauss-Seidel convergen para cualquier x⁽⁰⁾.
- Es una condición **suficiente, no necesaria**. Si no se cumple, no se concluye nada; por ejemplo, el GS de S9-07/10 converge sin dominancia.
- Reordenar las ecuaciones puede lograr la dominancia (Tarea II #2 y #3). La aplicación no reordena automáticamente.

## 8. Matrices de iteración y radio espectral (`algebra/modulo_IV_iterativos/espectral.py`)

**Matrices de iteración.** x⁽ᵏ⁺¹⁾ = T x⁽ᵏ⁾ + c, con:

| Método | T | c |
|---|---|---|
| Jacobi | T_J = −D⁻¹(L + U) | D⁻¹b |
| Gauss-Seidel | T_GS = −(D + L)⁻¹ U | (D + L)⁻¹ b |
| SOR **[Extensión]** | T_ω = (D + ωL)⁻¹[(1 − ω)D − ωU] | ω(D + ωL)⁻¹b |

La fórmula de T_ω es la estándar (Burden & Faires); no aparece en los PDF revisados.

**Convención de signos:** la lámina S8-30/09 p. 36 escribe B_J = D⁻¹(L + U) y B_GS = (D − L)⁻¹U, que es la convención A = D − L − U. Con A = D + L + U (la de la lámina p. 16, los manuscritos y la Tarea II) lo correcto es lo que figura en la tabla.

**Teorema:** el método converge para todo x⁽⁰⁾ si y solo si **ρ(T) = máx |λᵢ| < 1**.

**Procedimiento del curso** (S9-05/10 pp. 32-34; S9-07/10): det(T − λI) = 0 por Sarrus (3×3), luego las raíces y luego el máximo módulo.

**Implementación:**

1. **T exacta** con fracciones. Las inversas de D + L y D + ωL se calculan con nuestro Gauss-Jordan.
2. **Polinomio característico** p(λ) = det(λI − T) = λⁿ + c₁λⁿ⁻¹ + … + cₙ con **Faddeev-LeVerrier [Extensión]**:
   - M₀ = 0;
   - para k = 1…n: Mₖ = T·Mₖ₋₁ + cₖ₋₁·I y cₖ = −tr(T·Mₖ)/k.

   **Por qué hace falta:** Sarrus solo vale para 3×3. Con fracciones el cálculo es exacto, y en 3×3 coincide con el desarrollo de clase, det(T − λI) = −λ³ + tr(T)λ² − (Σ menores principales)λ + det(T). Hay una prueba que lo verifica.
3. **Raíces:**
   - las λ = 0 se extraen de forma exacta (coeficientes finales nulos);
   - grado 1 y 2: fórmula directa, con discriminante exacto;
   - grado ≥ 3: **Durand-Kerner [Extensión]**, zᵢ ← zᵢ − p(zᵢ)/Π_{j≠i}(zᵢ − zⱼ).

   **Por qué hace falta:** aparecen **autovalores complejos**. En S9-07/10, ρ = 1.174 viene precisamente de un par complejo; el método de la potencia no converge en ese caso.
4. **Verificaciones de cada resultado:**
   - |p(λ)| ≈ 0;
   - Σλ = traza(T);
   - aviso si hay raíces casi repetidas, que reducen la precisión;
   - aviso si Durand-Kerner no converge.
   **Corrección de la auditoría final:** la tolerancia de parada de Durand-Kerner es 10⁻¹². Con 10⁻¹⁵, el ruido de redondeo (~10⁻¹⁵) impedía a veces declarar la convergencia incluso con raíces simples.
5. **Conclusión** (función `concluir`):
   - Si λ = 1 o λ = −1 anulan p(λ) **exactamente** (con fracciones), entonces ρ ≥ 1 y el método no converge. La decisión es exacta.
   - Con raíces casi repetidas, la banda de indeterminación se amplía a 10⁻⁶.
   - Si |ρ − 1| < 10⁻⁹ o el cálculo no es fiable, el resultado es «indeterminado».
   - Para polinomios reducidos de grado ≤ 2 se decide de forma **exacta** con las condiciones de Schur-Cohn **[Extensión]**: |c₂| < 1 y |c₁| < 1 + c₂.
   - Para n > 8 no se calcula ρ y se informa la limitación.

**Limitaciones:**

- Durand-Kerner no tiene garantía teórica de convergencia global.
- Con raíces múltiples la precisión baja: ≈ 10⁻⁸ con raíces dobles y ≈ 10⁻⁵ con triples (error ≈ ε_máquina^(1/m)). Con raíces triples o de mayor multiplicidad Durand-Kerner no suele alcanzar la tolerancia, y el resultado queda «indeterminado».
- Por eso la aplicación verifica cada resultado y advierte cuando no es fiable, en lugar de mostrar un número engañoso.

**Ejemplos comprobados:**

| Caso | Polinomio y ρ | Conclusión |
|---|---|---|
| Tarea II #4 (Jacobi) | −λ³ + (1/6)λ + 1/40; ρ ≈ 0.4690 | converge |
| Tarea II #5 (Gauss-Seidel) | ρ = (11 + √241)/120 ≈ 0.2210 | converge |
| S9-07/10 (Jacobi) | −λ³ − (4/9)λ + **4/3**; raíces 0.967 y −0.483 ± 1.070i; ρ ≈ 1.174 | **no converge** |
| S9-07/10 (Gauss-Seidel) | −λ³ + (2/9)λ² + (2/3)λ; ρ = (2 + √220)/18 ≈ 0.935 | converge, lentamente |

En el caso de Jacobi de S9-07/10, la hoja omite el término 4/3 y concluye ρ = 0.

## 9. Matrices dispersas: formato CSR (`algebra/modulo_IV_iterativos/dispersas.py`) [Incentivo]

**Qué es una matriz dispersa.** Es una matriz en la que casi todos los elementos son cero: nnz ≪ n² (S9-05/10 p. 8).

**Formato CSR** (S9-05/10 p. 9). Guarda tres listas:

- `valores`: los aᵢⱼ no nulos, fila por fila;
- `columnas`: la columna j de cada valor;
- `inicio`: dónde empieza cada fila dentro de las otras dos listas.

**Estrategia.** Jacobi, GS y SOR solo necesitan recorrer los no nulos de cada fila, así que cada iteración cuesta O(nnz) en lugar de O(n²). La memoria pasa de n² a 2·nnz + n + 1 números.

**Comprobaciones:**

- Los pasos recorren los no nulos en el mismo orden de columnas que la versión densa, de modo que las iteraciones son **idénticas** (verificado por una prueba).
- En una tridiagonal 400×400 el paso CSR fue 52 veces más rápido (medido el 27-oct-2026).
- El tiempo total incluye convertir la entrada densa, que cuesta O(n²).

**Ejemplo:** la tridiagonal 5×5 tiene nnz = 5 + 4 + 4 = 13 (S9-05/10 p. 8).

## 10. Precondicionamiento diagonal (`algebra/modulo_IV_iterativos/precondicionamiento.py`) [Incentivo]

**Procedimiento de clase** (S9-05/10, diapositivas 16-18):

- M = D = diag(a₁₁, …, aₙₙ);
- sistema equivalente M⁻¹Ax = M⁻¹b, es decir, B x = b̃ con B = D⁻¹A y b̃ = D⁻¹b (misma solución);
- la lámina propone comparar κ(B) con κ(A), y ρ y los valores propios de A con los de B.

**Qué hace la aplicación** (`analizar_precondicionador`):

1. Construye M, M⁻¹, B y b̃ con fracciones exactas (`precondicionar_diagonal`).
2. Calcula κ∞(A) y κ∞(B) con la inversa del Módulo II.
3. Calcula los autovalores de A y de B (`analizar_matriz`).
4. Ejecuta Jacobi, GS, SOR y Richardson sobre los dos sistemas con la misma configuración.
5. Compara **exactamente** la matriz de iteración T y el vector c de cada método.

**Resultado 1: Jacobi, GS y SOR no cambian.** En B la diagonal es I, L̃ = D⁻¹L y Ũ = D⁻¹U. Entonces:

- T̃_J = −(L̃ + Ũ) = −D⁻¹(L + U) = T_J;
- T̃_GS = −(I + D⁻¹L)⁻¹D⁻¹U = −(D(I + D⁻¹L))⁻¹U = −(D + L)⁻¹U = T_GS;
- T̃_ω = (I + ωD⁻¹L)⁻¹[(1 − ω)I − ωD⁻¹U] = (D + ωL)⁻¹[(1 − ω)D − ωU] = T_ω;
- los vectores c coinciden por el mismo razonamiento.

Las iteraciones son, por tanto, las mismas. La aplicación lo verifica con fracciones en cada caso.

**Resultado 2: lo que sí cambia.**

- **κ:** con una diagonal uniforme (aᵢᵢ = a), B = A/a y κ(B) = κ(A). Con una diagonal no uniforme κ cambia y puede bajar mucho: en [[100, 1], [1, 1/50]] pasa de κ∞ = 10201 a 5202. También puede subir.
- **Residuo:** r̃ = D⁻¹r, así que el criterio B puede parar en otra iteración.
- **Richardson**, x ← x + (b − Ax), con T_R = I − A. Precondicionado se convierte en x ← x + D⁻¹(b − Ax), que **es Jacobi** (T̃_R = I − D⁻¹A = T_J).
  - Ejemplo con la tridiagonal [−1, 4, −1]: ρ(I − A) = 3 + 2cos(π/5) ≈ 4.618, de modo que no converge.
  - Con M = D: ρ(T_J) = cos(π/5)/2 ≈ 0.405, de modo que converge.
  - Richardson no se vio en clase; cabe en el «Jacobi, Gauss-Seidel, SOR, etc.» de la lámina p. 21.

**Valores propios.** Como T_J = I − D⁻¹A, los autovalores de B son μ = 1 − λ(T_J). Están cerca de 1 exactamente cuando ρ(T_J) es pequeño: es el «agrupados cerca de 1» de la lámina.

**Discrepancia con la lámina.** La diapositiva 19 (S9-05/10 p. 23) muestra para Jacobi «con precondicionamiento» un error que se reduce más rápido. Por el resultado 1 eso no puede ocurrir: la aplicación muestra las mismas iteraciones con y sin M = D. Además, la columna «sin precondicionamiento» de esa tabla no corresponde a Jacobi: el x⁽²⁾ real es (0.25, 0.0625, 0.0625, 0.25).
