# Comparación de procedimientos: enunciado ↔ PDF de clase ↔ código

**Fecha:** 03-nov-2026.

**Fuentes.** Los PDF originales de `C:\Users\dfarl\Desktop\algebra lineal` (no se modificaron). Citas:

- **OFICIAL p. N:** enunciado del proyecto (5 págs.).
- **PROG p. N:** programa del curso.
- **S8-30/09 p. N:** archivo de clase y página del PDF. Entre paréntesis va el número de diapositiva impreso en la lámina, cuando es distinto.

**Regla:** no se atribuye a la docente nada que no aparezca en sus PDF. Cuando el código usa un procedimiento que no está en el material, se marca **[Extensión]** y se justifica con el enunciado.

**Sobre la evidencia:**

- **Releído el 03-nov, en imagen:**
  - S9-05/10 pp. 16-17 (diap. 12-13) y pp. 21-24 (diap. 17-20);
  - S9-07/10 pp. 4 y 6;
  - S7-21/09 pp. 17-18;
  - S8-30/09 pp. 6-7;
  - PROG p. 9.
- **OFICIAL pp. 1-5:** releído en texto.
- **Resto de las páginas citadas:** se apoya en la auditoría documental del 26-oct (`algebra lineal/documentacion/auditoria_documental.md`), hecha con lectura visual de cada página.
- **No inspeccionados visualmente:** S1-10/08, S1-12/08, S2-17/08, S2-19/08, S4-02/09 y el Quiz S5. Son del Tema 1 (vectores, matrices, subespacios) y no contienen procedimientos que el proyecto implemente.

## Resumen

| Módulo | ¿Coincide el procedimiento? | Diferencias (todas documentadas) |
|---|---|---|
| I | **Sí.** Eliminación con operaciones elementales, pivote «primer no nulo» con intercambio, sustitución hacia atrás, Gauss-Jordan, inversa [A\|I] → [I\|A⁻¹] | (a) La clasificación usa rangos (Rouché-Frobenius); la lámina usa filas no nulas frente al número de incógnitas, que es lo mismo. (b) El determinante se calcula por eliminación (propiedad S3-24/08 p. 22) y no por Sarrus o cofactores. (c) El pivoteo parcial es una opción adicional |
| II | **Sí.** κ = ‖A‖‖A⁻¹‖ en norma ∞, con la inversa propia | (a) Se usa la escala del enunciado (3 niveles) y no la de la lámina S7-21/09 p. 18 (5 niveles). (b) Los manuscritos usan la norma 2 y el proyecto exige la ∞ |
| III | **Sí**, y desde esta revisión se muestran **los tres pasos de clase** | La solución se obtiene con Gauss (lo exige el enunciado). La docente usa Cramer, que la aplicación ahora calcula como verificación |
| IV iterativos | **Sí.** Mismas fórmulas por componentes y el mismo criterio ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε | Los manuscritos S8-30/09 pp. 19-20 y 24 suman las diferencias y lo rotulan ∞; el código usa el máximo, que es la definición |
| IV convergencia | **Sí.** A = D + L + U, T_J = −D⁻¹(L+U), T_GS = −(D+L)⁻¹U, det(T − λI) = 0, ρ = máx\|λ\|; en 3×3 se muestra el desarrollo por Sarrus | (a) **[Extensión]** T_ω de SOR no está en los PDF. (b) **[Extensión]** Faddeev-LeVerrier y Durand-Kerner para n > 3 y para las raíces (pendiente P-5). (c) La lámina S8-30/09 p. 36 usa otra convención de signos |
| IV comparación | **Sí.** «Error final» = ‖x⁽ᵏ⁾ − x‖∞, como en la tabla de S9-05/10 p. 17 | Ninguna. La aplicación muestra además d y r |
| Incentivo: precondicionamiento | **Sí** en la construcción (M = D, M⁻¹Ax = M⁻¹b) y en lo que se compara (κ(B) frente a κ(A) y valores propios, S9-05/10 p. 21) | La mejora de Jacobi que muestra la lámina de la p. 23 **no es reproducible**: con M = D, T no cambia. Se documenta con una demostración exacta |

---

## Módulo I — Sistemas lineales y métodos directos

| Aspecto | Enunciado (OFICIAL p. 2) | PDF de clase | Código | Conclusión |
|---|---|---|---|---|
| Entrada | Ax = b en forma matricial | Matriz aumentada [A\|b] (S6-14/09 pp. 21-25) | `leer_matriz`, `leer_vector`; `_resolver` arma `M = [A \| b]` | Coincide |
| Método | Gauss o Gauss-Jordan desde cero | Algoritmo de Gauss en 4 pasos: pivote, anular abajo, sustitución hacia atrás (S6-14/09 pp. 28-29; S6-16/09 pp. 25-26). Gauss-Jordan: forma escalonada reducida (S6-14/09 p. 30) | `_escalonar(..., reducida=False/True)`, `_sustitucion_atras` | Coincide. Mismo orden: columna por columna, anulando debajo del pivote con Fᵢ → Fᵢ − m·Fᵣ |
| Pivote nulo | Detectar pivotes nulos | Si el pivote es 0 se intercambian filas (S3-24/08 p. 5; S6-14/09 p. 28) | `_buscar_pivote` con `PIVOTEO_PRIMER_NO_NULO` (opción por defecto) | Coincide. El pivoteo parcial es una opción extra; las láminas mencionan PA = LU, pero sus ejemplos no pivotean |
| Pivote problemático | Detectar pivotes «numéricamente problemáticos» | No hay un umbral en los PDF | Aviso si \|p\| < 10⁻¹⁰·máx\|aᵢⱼ\| (`UMBRAL_PIVOTE_PEQUENO`) | Umbral técnico propio, documentado (decisiones_tecnicas #6) |
| Clasificación | Única, infinitas o inconsistente | Filas no nulas frente a número de incógnitas, más la interpretación geométrica (S6-14/09 p. 26; S6-16/09 p. 29) | `rango_A` = número de pivotes; `_rango_aumentada` detecta [0 … 0 \| c] | Equivalente: rango = número de filas no nulas de la escalonada |
| Inversa | La que exige el Módulo II | [A\|I] → [I\|A⁻¹]; «si no existe pivote no nulo, A⁻¹ no existe» (S3-24/08 pp. 6 y 28) | `inversa_gauss_jordan` y la verificación A·A⁻¹ = I | Coincide |
| Determinante | (Solo si se usa) | Sarrus y cofactores (S3-24/08 pp. 10-27); propiedad de las operaciones de fila (p. 22) | `determinante` = (−1)^intercambios · Π pivotes | Procedimiento distinto, con el mismo valor y basado en la propiedad de la p. 22. Para 3×3 la docente usa Sarrus; nuestro `desarrollo_sarrus` lo aplica a T en el Módulo IV. **El enunciado no exige un método concreto para el determinante** |

## Módulo II — Condicionamiento

| Aspecto | Enunciado | PDF | Código | Conclusión |
|---|---|---|---|---|
| Definición | κ∞(A) = ‖A‖∞‖A⁻¹‖∞ con inversa propia | κ(A) = ‖A‖‖A⁻¹‖; ‖A‖∞ = máxima suma de fila (S7-21/09 p. 17, diap. 06); el ejemplo de la lámina usa la norma 1 | `numero_condicion_infinito`, `norma_infinito_matriz`, `inversa_gauss_jordan` | Coincide en la norma que exige el enunciado |
| Propiedades | — | κ ≥ 1; κ(A) = κ(A⁻¹); ortogonal ⇒ κ = 1 (S7-21/09 p. 17) | Probadas (κ(I) = 1 y ≥ 1 en la auditoría) | Coincide |
| Escala | < 10, < 100, ≥ 100 | 5 niveles: ≈1, ≤10, ≤10³, ≤10⁶, > 10⁶ (S7-21/09 p. 18, diap. 07) | `clasificar_kappa` con la escala del **enunciado** | **Diferencia justificada:** el enunciado fija su escala «para efectos del proyecto» |
| Cota | Explicar la sensibilidad | ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ (S7-21/09 p. 18) | `analizar_perturbacion`: cota, `cumple_cota`, amplificación | Coincide |
| Normas de los errores | ‖Δb‖∞/‖b‖∞ y ‖Δx‖∞/‖x‖∞ | Los manuscritos usan la norma 2 (S8-28/09 pp. 12-15) | Norma ∞ | **El enunciado manda la ∞**; un ejemplo de clase en norma 2 no coincidirá numéricamente |
| Perturbación | Absoluta o porcentual | No aparece la perturbación porcentual | Δbᵢ = p/100·bᵢ | Interpretación propia: ‖Δb‖/‖b‖ = p/100 (P-7) |

## Módulo III — Mínimos cuadrados

Procedimiento de la docente (S8-30/09 pp. 6-7, manuscrito, releído el 03-nov):

1. Comprobar que b no es combinación lineal de las columnas de A. En el ejemplo 3×2: det([A\|b]) por Sarrus = −11 ≠ 0, rango 3.
2. Plantear AᵀAx = Aᵀb, que da [[14, −13], [−13, 38]]x = (39, −59).
3. Resolver con la regla de Cramer: |A| = 363, |Aₓ| = 715, |A_y| = −319, x = (65/33, −29/33).

| Aspecto | Enunciado | PDF | Código | Conclusión |
|---|---|---|---|---|
| Detección | Detectar si es sobredeterminado | m > n; b ∉ Col(A) | `clasificar_forma`. Consistencia por rango (`resolver_gauss`). **Nuevo:** `det_aumentada` = det([A\|b]) si m = n + 1 | Coincide. El paso 1 de clase se muestra cuando aplica (m = n + 1) |
| Ecuaciones normales | AᵀAx = Aᵀb | Igual | `transpuesta`, `multiplicar_matrices` | Coincide; el ejemplo da exactamente las mismas matrices |
| Resolución | «Con un método directo ya implementado» | Cramer | `resolver_gauss` (la solución presentada). **Nuevo:** `cramer(AtA, Atb)` como verificación para n ≤ 3 | El enunciado obliga a usar el método propio, así que se usa Gauss. Cramer, el método de clase, se muestra y **coincide exactamente** (prueba `test_minimos_como_el_manuscrito`) |
| Residuo | r = b − Ax̂ y ‖r‖₂ | — | `residuo`, `norma_2_cuadrado_vector`; control Aᵀr = 0 | Coincide |
| Ajuste lineal | Ecuación y gráfica | Solo el planteamiento (S8-30/09 p. 8) | `ajuste_lineal` con la matriz [[xᵢ, 1]] | No hay un procedimiento resuelto en clase; la aplicación aplica el mismo esquema de ecuaciones normales |

## Módulo IV — Métodos iterativos

| Aspecto | Enunciado | PDF | Código | Conclusión |
|---|---|---|---|---|
| Jacobi | Desde cero | xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁾)/aᵢᵢ (S8-30/09 p. 15) | `paso_jacobi` | Coincide |
| Gauss-Seidel | Desde cero | Usa los valores actualizados (S8-30/09 p. 22) | `paso_gauss_seidel` | Coincide |
| SOR | Desde cero, con ω validado | xᵢ⁽ᵏ⁺¹⁾ = (1−ω)xᵢ⁽ᵏ⁾ + (ω/aᵢᵢ)(bᵢ − Σ_{j<i} aᵢⱼxⱼ⁽ᵏ⁺¹⁾ − Σ_{j>i} aᵢⱼxⱼ⁽ᵏ⁾), 0 < ω < 2 (S9-05/10 p. 16, diap. 12; S8-30/09 p. 28) | `paso_sor` | Coincide, término por término |
| Criterio de parada | «El error utilizado como criterio» | ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖∞ < ε (S8-30/09 pp. 13, 34, 39). Los manuscritos pp. 19-20 y 24 suman las diferencias | Criterio A (por defecto), con desigualdad estricta. B (residuo) y C (N fijo) son opcionales | Coincide con las láminas. **Diferencia con los manuscritos:** se usa el máximo (definición de la norma ∞); se explica en la defensa (IV-7: 1.8889 y no 2.402) |
| Error final | «Comparar … mediante número de iteraciones y error final» | Tabla «Error final (‖x⁽ᵏ⁾ − x‖∞)» (S9-05/10 p. 16 y p. 17, diap. 12-13) | `comparar_metodos.errores_finales` = ‖x⁽ᵏ⁾ − x*‖∞, con x* exacta de Gauss | **Coincide con la lámina.** Resuelve el pendiente P-4. La gráfica comparativa muestra ahora e_k como primera métrica |
| Dominancia | Criterio suficiente | Por filas, estricta (S8-30/09 p. 37). La docente **reordena las ecuaciones** para lograrla (Tarea II #2-3; S9-05/10 p. 32) | `dominancia_diagonal`. **Nuevo:** `reordenamiento_dominante` propone el orden de ecuaciones que logra la dominancia | Coincide; ahora también con el paso de reordenar (sin modificar los datos del usuario) |
| Matriz de iteración | Construir T | A = D + L + U; T_J = −D⁻¹(L+U), c = D⁻¹b; T_GS = −(D+L)⁻¹U (S8-30/09 p. 16; S9-07/10 pp. 4 y 6, releídas) | `descomponer`, `matriz_iteracion` | Coincide. La lámina S8-30/09 p. 36 escribe B_J = D⁻¹(L+U) y B_GS = (D−L)⁻¹U, que es la convención A = D − L − U; con A = D + L + U (la de sus manuscritos) lo correcto es lo del código |
| T de SOR | — | **No aparece en los PDF** | T_ω = (D + ωL)⁻¹[(1−ω)D − ωU] | **[Extensión]** Fórmula estándar (Burden & Faires), deducida de la fórmula por componentes de la lámina (guía, D.4) |
| ρ(T) | «Mediante los procedimientos estudiados en el curso» | det(T − λI) por Sarrus, luego las raíces y el máximo módulo (S9-05/10 pp. 32-34; S9-07/10 p. 4) | 3×3: el polinomio sale idéntico a Sarrus y **ahora se muestra el desarrollo de clase** (`desarrollo_sarrus`: tr, Σ menores, det). n > 3 o raíces: Faddeev-LeVerrier y Durand-Kerner | 3×3: coincide. **[Extensión]** para hallar raíces y para n > 3 (pendiente P-5). Nota: la hoja de S9-07/10 p. 4 omite el término 4/3 y concluye ρ = 0; la aplicación da 1.174 |

## Incentivo: precondicionador diagonal

Procedimiento de la docente (S9-05/10 pp. 21-23, diap. 17-19, releídas el 03-nov):

- M = D = diag(aᵢᵢ); sistema M⁻¹Ax = M⁻¹b; «se aplica el método iterativo (Jacobi, Gauss-Seidel, SOR, etc.) al sistema precondicionado».
- Un buen precondicionador busca ρ(B) < ρ(A) y κ(B) < κ(A), con los valores propios de B = D⁻¹A agrupados cerca de 1.
- Ejemplo: tridiagonal [−1, 4, −1], con M = 4I y M⁻¹A = A/4.

| Aspecto | Lámina | Código (`algebra/precondicionamiento.py`) | Conclusión |
|---|---|---|---|
| Construcción | M = D, M⁻¹A, M⁻¹b | `precondicionar_diagonal` (exacto) | Coincide; el ejemplo da A/4 y b/4 (prueba) |
| Comparación de κ | κ(B) frente a κ(A) | κ∞(A) y κ∞(D⁻¹A) con la inversa propia | Coincide |
| Valores propios | De A y de B = D⁻¹A | `analizar_matriz(A)` y `analizar_matriz(B)` | Coincide |
| Iteraciones | «Con precondicionamiento» Jacobi converge más rápido (diap. 19) | Jacobi, GS y SOR sobre los dos sistemas con la misma configuración, más una comparación **exacta** de T y c | **Diferencia demostrada:** T̃ = T y c̃ = c, así que las iteraciones son idénticas. La tabla de la diapositiva 19 no es reproducible: sin precondicionar, x⁽²⁾ = (0.25, 0.0625, 0.0625, 0.25), y la lámina pone 0.125 |
| Efecto real | — | Richardson, x ← x + (b − Ax), sobre ambos sistemas: ρ(I − A) frente a ρ(I − D⁻¹A) = ρ(T_J) | **[Extensión]** Cabe en el «etc.» de la lámina. Muestra un efecto real de M = D: en la tridiagonal, ρ pasa de 4.618 (diverge) a 0.405 (converge) |

## Decisiones derivadas de esta comparación (implementadas el 03-nov)

1. **Mínimos cuadrados:** se muestran det([A\|b]) y Cramer como verificación, siguiendo el procedimiento de clase.
2. **Radio espectral 3×3:** se muestra el desarrollo por Sarrus (tr, Σ menores, det) y se comprueba que coincide con Faddeev-LeVerrier.
3. **Dominancia:** se busca y se propone el reordenamiento de las ecuaciones, como en clase.
   - Defecto corregido: con un aᵢᵢ = 0 la pestaña no mostraba ni la dominancia ni el reordenamiento, porque fallaba al construir T. Ahora los muestra y explica por qué no hay T.
4. **Comparación:** e_k = ‖x⁽ᵏ⁾ − x*‖∞ («error final» de la lámina) pasa a ser la primera métrica de la gráfica comparativa.
5. **Precondicionamiento:** implementado con la comparación que propone la lámina y con la evidencia exacta de lo que cambia y lo que no.
