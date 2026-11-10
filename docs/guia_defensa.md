# Guía de estudio para la defensa individual

> **Versión ampliada (02-nov-2026):** [guia_defensa_equipo.md](guia_defensa_equipo.md) explica el código real función por función, incluye 35 preguntas con respuesta y el guion de demostración. Para repasar rápido: [resumen_logica_por_modulo.md](resumen_logica_por_modulo.md). Esta guía se conserva por la tabla de errores de las láminas (§6).

## Formato de la defensa (OFICIAL p. 3-4)

Integrantes: Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez. La defensa es en la semana del 16 de noviembre de 2026.


- **Duración:** 6 a 8 minutos por integrante.
- **Contenido:**
  - demostrar que la aplicación funciona;
  - explicar **al menos dos módulos elegidos por la docente**;
  - justificar la lógica matemática;
  - responder preguntas;
  - ejecutar un caso **no preparado**.
- **Rúbrica de la defensa (35 %):** dominio conceptual 10 %, explicación matemática 10 %, uso del programa 5 %, claridad 5 %, comunicación 5 %.

**Consecuencia:** cada integrante debe dominar **los cuatro módulos**. Esta guía está organizada para eso.

---

## 0. Ideas que hay que saber explicar en cualquier módulo

1. **Por qué fracciones exactas.** En Gauss, la inversa, κ y los mínimos cuadrados los resultados son exactos: 1/3 se guarda como 1/3, no como 0.333… Así un pivote es cero solo si es realmente cero, y la clasificación no depende de redondeos.
2. **Por qué `float` en los iterativos.** Son aproximaciones que se detienen por tolerancia. Con fracciones, los denominadores crecerían en cada iteración.
3. **Núcleo e interfaz.** `algebra/` contiene todos los cálculos, en Python puro. `interfaz/` solo lee los datos y muestra los resultados. `visualizacion/` solo dibuja.
4. **Cómo se verifica.** Hay 232 pruebas automáticas (`python -m unittest`) y una auditoría independiente en `auditoria/`, que compara el núcleo con oráculos escritos aparte (Leibniz, adjunta, Cramer, Gelfand). Los valores esperados se calcularon de forma independiente: a mano, con Cramer, con fórmulas cerradas o con teoremas. No se copiaron de las láminas.
5. **Errores de las láminas.** Algunos ejemplos impresos están mal (tabla de la sección 6). Si en la defensa la aplicación «no coincide» con una lámina, hay que poder mostrar por qué: sustituir la solución en el sistema y ver el residuo.

---

## Módulo I — Gauss y Gauss-Jordan (`algebra/modulo_I_sistemas/directos.py`)

**Saber explicar:**

- Las 3 operaciones elementales: Fi ↔ Fj, Fi → kFi y Fi → Fi + kFj. Ninguna cambia el conjunto de soluciones.
- El papel del pivote, y por qué se intercambian filas cuando el pivote es 0 (función `_buscar_pivote`).
- La diferencia entre la forma escalonada (Gauss, seguida de sustitución hacia atrás) y la forma escalonada reducida (Gauss-Jordan).
- La clasificación por rangos:

  | Condición | Tipo |
  |---|---|
  | rango(A) < rango([A\|b]) | inconsistente: fila 0 = c |
  | rango(A) = rango([A\|b]) = n | solución única |
  | rango(A) = rango([A\|b]) < n | infinitas soluciones |

- La forma paramétrica: las variables libres son las columnas sin pivote; x = xₚ + t·v, con A·v = 0.
- La geometría (3 incógnitas): planos que se cortan en un punto, que comparten una recta o un plano, o que no tienen un punto común.
- El determinante como (−1)^(intercambios) · Π pivotes.

**Preguntas probables:**

- *¿Qué pasa si un pivote es cero?* Se busca una fila más abajo con elemento no nulo y se intercambian. Si no la hay, esa columna no tiene pivote y su variable es libre.
- *¿Qué es el pivoteo parcial?* Elegir el mayor |elemento| de la columna. En punto flotante reduce los errores de redondeo; con fracciones el resultado es el mismo.
- *¿Por qué la aplicación dice que el ejemplo de la lámina S6-14/09 p. 29 tiene otra solución?* Porque la lámina se equivoca en el último paso: (1/2, −1, −1) no cumple la 2.ª ecuación. Se puede verificar sustituyendo.

**Demostración sugerida:** cargar «Pivote nulo» y mostrar el paso F1 ↔ F2. Después cargar «Infinitas» y luego «Inconsistente», y abrir la interpretación geométrica.

---

## Módulo II — Condicionamiento (`algebra/modulo_II_condicionamiento/condicion.py`)

**Saber explicar:**

- ‖A‖∞ es la mayor suma de fila, y κ∞ = ‖A‖∞‖A⁻¹‖∞.
- A⁻¹ se calcula con nuestro Gauss-Jordan [A | I] → [I | A⁻¹], y se verifica A·A⁻¹ = I.
- La cota ‖Δx‖/‖x‖ ≤ κ·‖Δb‖/‖b‖: κ dice **cuánto puede amplificarse**, en el peor caso, un error relativo de los datos.
- Singular no es lo mismo que mal condicionada. Una matriz singular no tiene inversa (κ no está definido). Una invertible con κ grande tiene solución única pero muy sensible.
- La escala del proyecto: κ < 10 baja, < 100 moderada, ≥ 100 alta. Es un criterio operativo.

**Preguntas probables:**

- *¿Por qué κ ≥ 1?* Porque 1 = ‖I‖ = ‖AA⁻¹‖ ≤ ‖A‖‖A⁻¹‖.
- *¿Por qué la amplificación observada puede ser menor que κ?* κ es el peor caso sobre todas las direcciones de Δb. En el ejemplo I + 10J con Δb = (1, −1, 1) se alcanza exactamente κ = 41.
- *¿Qué pasa si b = 0?* El error relativo de b no está definido y la aplicación lo indica.

**Demostración sugerida:** comparar el ejemplo «bien condicionada» (κ ≈ 2.27) con «mal condicionada» (κ ≈ 40004): un cambio de 0.0001 en b cambia x de (1, 1) a (0, 2).

---

## Módulo III — Mínimos cuadrados (`algebra/modulo_III_minimos/minimos.py`)

**Saber explicar:**

- Si m > n, el sistema es sobredeterminado y, en general, b ∉ Col(A), así que no hay solución exacta.
- x̂ minimiza ‖b − Ax‖₂ y cumple AᵀA x̂ = Aᵀb.
- Se resuelve con nuestro Gauss, porque el enunciado lo exige.
- r = b − Ax̂ y ‖r‖₂ = √Σrᵢ². La comprobación Aᵀr = 0 indica que el residuo es perpendicular a las columnas de A.
- Para el ajuste lineal, A = [[xᵢ, 1]] y b = (yᵢ), y la solución da m y c.
- Si las columnas de A son dependientes, AᵀA es singular y x̂ no es único.

**Preguntas probables:**

- *¿Por qué las ecuaciones normales?* Porque el gradiente de ‖b − Ax‖² es −2Aᵀ(b − Ax). Igualarlo a 0 da AᵀAx = Aᵀb.
- *¿Qué significa ‖r‖₂ pequeño?* Que los datos están cerca de la recta. ‖r‖₂ = 0 solo si hay solución exacta.

**Demostración sugerida:** el ejemplo S8-30/09 p. 8 (la recta y = 0.75x + 1.2), mostrando la gráfica con los residuos.

---

## Módulo IV — Métodos iterativos (`algebra/modulo_IV_iterativos/`, `algebra/modulo_IV_iterativos/espectral.py`)

**Saber explicar:**

- **Las tres fórmulas.**
  - Jacobi usa solo x⁽ᵏ⁻¹⁾.
  - Gauss-Seidel usa los valores nuevos en cuanto están disponibles.
  - SOR mezcla el valor anterior y el de Gauss-Seidel: (1 − ω)·anterior + ω·GS. Con ω = 1 es Gauss-Seidel.
- **Las tres métricas.** d_k es el cambio entre iteraciones; r_k, el residuo; e_k, el error respecto a la solución exacta. **No son lo mismo.**
- **Los tres criterios.**
  - A: d_k < ε.
  - B: r_k < ε.
  - C: N iteraciones fijas, que **no** demuestran convergencia.
  - Se usa la desigualdad estricta, y A es el predeterminado porque es el que más usa la docente.
- **Norma ∞ = máximo.** Los manuscritos de clase suman las diferencias (eso es la norma 1).
- **Motivos de parada.** Alcanzar k_max **no** demuestra divergencia. Los valores no finitos son un error numérico, no una demostración.
- **Dominancia diagonal.** Es condición suficiente, no necesaria.
- **Radio espectral.** T_J = −D⁻¹(L + U) y T_GS = −(D + L)⁻¹U; ρ(T) = máx|λ|; el método converge para todo x⁽⁰⁾ si y solo si ρ < 1.
- **Cómo se calcula ρ.**
  1. T exacta.
  2. det(λI − T) con Faddeev-LeVerrier, que en 3×3 da lo mismo que Sarrus.
  3. Raíces: las λ = 0 exactas, la fórmula cuadrática o Durand-Kerner.
  4. Verificación con |p(λ)| y con traza = Σλ.

**Preguntas probables:**

- *¿Por qué Gauss-Seidel suele converger antes que Jacobi?* Porque usa información más reciente. En S: 4 iteraciones frente a 7.
- *¿Qué hace ω?* Con ω < 1 se sub-relaja y con ω > 1 se sobre-relaja. El barrido de ω muestra cómo cambia ρ(T_ω).
- *¿Por qué no basta con 0 < ω < 2?* Es necesario para la convergencia, pero no suficiente en general.
- *¿Por qué la hoja de S9-07/10 dice ρ = 0 y la aplicación dice 1.174?* Porque en el desarrollo de Sarrus los términos constantes +2/3 + 2/3 no se cancelan: el polinomio correcto es −λ³ − (4/9)λ + 4/3. Además, las raíces de −λ² − 4/9 serían complejas de módulo 2/3, no 0. La aplicación muestra el par complejo −0.483 ± 1.070i, de módulo 1.174 > 1.
- *¿Qué son Faddeev-LeVerrier y Durand-Kerner?*
  - Faddeev-LeVerrier: una forma de obtener los coeficientes de det(λI − T) para cualquier n usando solo productos y trazas, porque Sarrus solo vale para 3×3.
  - Durand-Kerner: un método iterativo que aproxima todas las raíces complejas a la vez.
  - Ninguno se vio en clase; se usaron porque los autovalores pueden ser complejos y n puede ser mayor que 3. La aplicación verifica cada resultado.

**Demostración sugerida:** el sistema S con los criterios A y luego B, y la comparación homogénea. Después, «S9-07/10» en la pestaña de convergencia (ρ > 1), y ejecutar Jacobi para ver que se alcanza k_max sin afirmar divergencia.

---

## 5. Estructuras de datos y validaciones

- **Matriz:** lista de filas; **vector:** lista. Los resultados son `dataclass`, por ejemplo `ResultadoSistema` o `ResultadoIterativo`.
- **Validaciones** (OFICIAL p. 3), en `algebra/compartido/validacion.py` y `algebra/compartido/matriz.py`:
  - campos vacíos o no numéricos, indicando la posición;
  - dimensiones;
  - singularidad;
  - pivote nulo o aᵢᵢ = 0;
  - ε > 0;
  - k_max y N enteros positivos;
  - 0 < ω < 2.
  - Ninguna entrada provoca el cierre de la aplicación (`ejecutar` nunca lanza excepciones; la interfaz muestra los errores en rojo).

## 6. Errores de los materiales detectados y corregidos

| Material | Dice | Correcto | Cómo comprobarlo |
|---|---|---|---|
| S6-14/09 p. 29 (Gauss) | (1/2, −1, −1) | (19/20, −5/4, −7/20) | Sustituir en x − 3y + 2z = 4 |
| S3-24/08 p. 3 (OEF) | (2, 1, −1) | (16/5, 1, −3/5) | A·(2, 1, −1) = (6, −1, 7) ≠ (8, 1, 11) |
| S3-24/08 p. 8 (inversa) | 1.ª columna (9/8, −5/8, 3/8) | (1/8, −1/8, 3/8) | A·A⁻¹ = I |
| S3-24/08 pp. 25-27 (adjunta) | det = 42 | det = 15 | Desarrollo por la fila 1 |
| S7-21/09 p. 20 | x̃₂ = 0.6309 | 0.6318 | (−1.01 + 4·1.99)/11 |
| S8-30/09 pp. 17-31 (sistema S) | Soluciones 1.27…, 0.4667… | (1.0433, 2.2692, −1.0817) | Residuo de las láminas ≠ 0 |
| S8-30/09 pp. 19-20, 24 (manuscritos) | Suma de \|diferencias\| rotulada ∞ | Máximo | Definición de ‖·‖∞ |
| S8-30/09 p. 36 | B_J = D⁻¹(L+U), B_GS = (D−L)⁻¹U con A = D+L+U | −D⁻¹(L+U), −(D+L)⁻¹U | Lámina p. 16 |
| S8-30/09 p. 38 | ρ ≈ 0.52; caso C 3.32 | 0.580; 3.10 | Pestaña de convergencia |
| S9-05/10 pp. 14-16 | «Solución exacta» (1/3, 1/15, …); ω = 1.8 no converge | (3/11, 1/11, 1/11, 3/11); converge (A simétrica definida positiva) | Residuo; teorema de Ostrowski-Reich |
| S9-07/10 p. 4 | ρ(T_J) = 0 | 1.174 (no converge) | Pestaña de convergencia |
| S9-07/10 p. 7 | c_GS = (−7, 25/3, −13/9) | (3, 0, 7/3) | c = (D+L)⁻¹b |

## 7. Errores propios corregidos durante el desarrollo

- `plot_surface` de Matplotlib 3.11 no acepta listas; los planos se dibujan con polígonos (`Poly3DCollection`). Lo detectó la prueba `test_app`.
- Una constante de prueba mal redondeada (0.5798 en lugar de 0.57985). La implementación era correcta: lo confirmó la comprobación por bisección.
- Streamlit se quedaba esperando un correo electrónico en el primer arranque. Se configuró `headless = true` para que `ejecutar.bat` no se bloquee.

## 7b. Defectos encontrados en la auditoría final (27-oct-2026)

- **Durand-Kerner tenía una tolerancia de parada inalcanzable (10⁻¹⁵).** Con raíces simples, a veces declaraba «no fiable» y la aplicación concluía «indeterminado» aunque el método convergía (por ejemplo, ρ = 0.595). Se cambió a 10⁻¹²; la verificación posterior (|p(λ)|, traza) se mantiene.
- **λ = ±1 se comprueba ahora de forma exacta.** Si p(1) = 0 o p(−1) = 0 con fracciones, ρ ≥ 1 con certeza. Esto ocurre, por ejemplo, si A es singular, porque T = I − M⁻¹A tiene entonces el autovalor 1.
- **Limitación que hay que saber explicar.** Con autovalores **múltiples** (raíz doble o triple) Durand-Kerner pierde precisión, y la aplicación responde «indeterminado» en lugar de dar un número dudoso.
- **Fracciones en LaTeX:** se añadió espacio entre filas para que las fracciones no se monten.

## 8. Cómo comprobar un resultado en vivo

1. **Métodos directos:** la aplicación muestra b − Ax, que debe ser (0, …, 0).
2. **Inversa:** se comprueba «A·A⁻¹ = I».
3. **Mínimos cuadrados:** se comprueba Aᵀr = (0, 0).
4. **Iterativos:** el valor de r_k de la tabla. En la comparación, e final usa la solución exacta de Gauss.
5. **Radio espectral:** la verificación «suma de autovalores = traza(T)».
