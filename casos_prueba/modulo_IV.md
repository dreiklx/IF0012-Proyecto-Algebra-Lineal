# Casos de prueba — Módulo IV: métodos iterativos y convergencia

Los oráculos de las iteraciones se obtuvieron el 27-oct-2026 con un programa independiente, escrito aparte de `algebra/modulo_IV_iterativos/`. Se contrastaron así:

- La solución exacta de S es (217/208, 59/26, −225/208), comprobada por sustitución.
- Las iteraciones 1–3 de SOR coinciden con el manuscrito S8-30/09 pp. 32-33.
- La Tarea II #2 coincide con la solución estudiantil del ZIP, que usa la norma ∞.

Los radios espectrales se verificaron con oráculos independientes:

- coeficientes del polinomio calculados a mano por traza, menores principales y determinante;
- fórmulas cerradas de la ecuación cuadrática;
- bisección y relaciones de Vieta.

**Los valores impresos en las láminas de S8 para el sistema S son incorrectos:** dan tres «soluciones» distintas según el método. No se usan.

- **Sistema S:** 10x − y + 2z = 6, −x + 11y − z = 25, 2x − y + 10z = −11. Es estrictamente diagonalmente dominante.
- **Configuración:** x⁽⁰⁾ = 0, ε = 10⁻³, k_max = 50, norma ∞ y desigualdad estricta.
- **Pruebas automáticas:** `tests/modulo_IV/test_iterativos.py` (P1–P21) y `tests/modulo_IV/test_espectral.py`.

## Métodos y criterios de parada

| ID | Caso | Salida esperada | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| IV-1 | S, Jacobi, criterio A | k = 7; x = (1.043187, 2.269277, −1.081786); d = 3.78139e-4; r = 9.76218e-4 | TOLERANCIA_CAMBIO, k = 7, mismos x, d y r | Sí |
| IV-2 | S, Gauss-Seidel, criterio A | k = 4; x = (1.043297, 2.269235, −1.081736) | TOLERANCIA_CAMBIO, k = 4 | Sí |
| IV-3 | S, SOR ω = 1.2, criterio A | k = 6; x = (1.043010, 2.269367, −1.081809); d = 8.62517e-4 | TOLERANCIA_CAMBIO, k = 6 | Sí |
| IV-4 | S, SOR ω = 1.2, criterio B (residuo) | k = 7; r = 8.78688e-4 (con el criterio A eran 6 iteraciones) | TOLERANCIA_RESIDUO, k = 7 | Sí |
| IV-5 | S, Jacobi, criterio C con N = 5 | 5 iteraciones; mensaje de que no demuestra convergencia; d₅ = 5.85917e-3 | N_COMPLETADAS, k = 5 | Sí |
| IV-6 | 10x+2y+z = 9, 2x+10y+2z = 13, x+2y+10z = 14; SOR ω = 1.2 (manuscrito S8-30/09 p. 32) | x⁽¹⁾ = (1.08, 1.3008, 1.2382); x⁽²⁾ = (0.4032, 0.9059, 1.1666); termina en k = 7 | Igual | Sí |
| IV-7 | 6x₁+2x₂+x₃ = 22, …; x⁽⁰⁾ = bᵢ/aᵢᵢ; Jacobi (S8-30/09 p. 19) | d₁ = ‖x⁽¹⁾ − x⁽⁰⁾‖∞ = 1.8889. **El manuscrito suma las diferencias (2.402) y lo rotula ∞** | d₁ = 1.8889 | Sí |
| IV-8 | 3x+3y+3z = 9, 3x+3y+2z = 9, −3x−2y+3z = −2; Jacobi, k_max = 30 (S9-07/10) | Se alcanza el máximo sin cumplir el criterio; **no se afirma divergencia** | MAXIMO_ITERACIONES, k = 30 | Sí |
| IV-9 | A = [[1, 1e200], [1e200, 1]], Jacobi | Error numérico por valores no finitos, sin cerrar la aplicación | ERROR_NO_FINITO en k = 2 | Sí |
| IV-10 | A = [[0, 1], [1, 0]] | Diagonal cero: no se itera | DIAGONAL_CERO | Sí |
| IV-11 | M₃ con x⁽⁰⁾ = (2, 3, 4) (la solución), criterio B | Se detiene en k = 0 y explica que el vector inicial ya cumple | TOLERANCIA_RESIDUO, k = 0 | Sí |
| IV-12 | Entradas inválidas: ε = 0, k_max = 2.5, ω = 2 | Mensaje claro, sin excepción | ENTRADA_INVALIDA con mensaje | Sí |

## Radio espectral

| ID | Caso | Salida esperada (oráculo independiente) | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| IV-13 | Tarea II #4, Jacobi | Polinomio −λ³ + (1/6)λ + 1/40; ρ = raíz positiva de λ³ − λ/6 − 1/40 ≈ 0.4690 (bisección; coincide con el ZIP) | ρ = 0.46901, converge | Sí |
| IV-14 | Tarea II #5, Gauss-Seidel | ρ = (11 + √241)/120 = 0.221035 (fórmula cuadrática) | ρ = 0.221035, converge | Sí |
| IV-15 | S9-07/10, Jacobi | Polinomio −λ³ − (4/9)λ + 4/3. ρ = 1.174364, por un par complejo: \|λ\|² = (4/3)/λ_real por Vieta. **La hoja concluye ρ = 0 (error)** | ρ = 1.174364, NO converge, 2 autovalores complejos | Sí |
| IV-16 | S9-07/10, Gauss-Seidel | Polinomio −λ³ + (2/9)λ² + (2/3)λ, igual al manuscrito; ρ = (2 + √220)/18 = 0.935133 | ρ = 0.935133, converge | Sí |
| IV-17 | Tridiagonal [−1, 4, −1], n = 4 | Por teoría: ρ_J = cos(π/5)/2 = 0.404508; ρ_GS = ρ_J² = 0.163627; ρ_SOR(ω = 1.25) = ω − 1 = 0.25 | Coinciden con 10, 10 y 6 decimales | Sí |

## Casos añadidos en la auditoría final (27-oct-2026)

| ID | Caso | Salida esperada | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| IV-18 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | A = [[−4, −1, 3, −1], [2, 5, 1, 0], [1, −3, 5, 0], [2, 2, 2, 5]], SOR ω = 1/2 | Autovalores simples; ρ ≈ 0.5951 < 1; conclusión «converge» y resultado fiable (antes salía «indeterminado» por un defecto). Comprobación independiente: las iteraciones de SOR alcanzan ε = 10⁻¹⁰ | ρ = 0.5950974, CONVERGE, fiable; la ejecución termina por tolerancia | Sí |
| IV-19 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | A = [[2, 1, 1], [1, 2, 1], [3, 3, 2]] (singular), SOR ω = 1/2 | λ = 1 es autovalor exacto de T, luego ρ ≥ 1: «no converge», con decisión exacta | NO_CONVERGE, decisión exacta | Sí |
| IV-20 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | T con el autovalor 1/2 triple (bloque de Jordan) | ρ = 1/2, pero con raíz múltiple Durand-Kerner es impreciso: debe declararse «no fiable», no presentarse como garantizado | No fiable, aviso de autovalor múltiple, \|λ\| ≈ 0.500 | Sí |
| IV-21 | ε = 10⁻⁴⁰⁰ (se anula en float) y ε = 10⁴⁰⁰ | Mensajes claros y específicos | «…en punto flotante vale 0…» / «…demasiado grande…» | Sí |

## Caso añadido en la revisión del 02-nov-2026

| ID | Caso | Salida esperada | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| IV-22 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | S9-07/10 (A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]]) con SOR, ω = 6/5 (el ω por defecto de la interfaz) | λ = −1 es autovalor de T_ω si y solo si det((2 − ω)D + ωL − ωU) = 0. Con ω = 6/5 esa matriz es (6/5)·[[2, −3, −3], [3, 2, −2], [−3, −2, 2]], cuya fila 3 es la fila 2 con el signo cambiado: es singular. Por tanto ρ ≥ 1 y el método **no converge**, con decisión exacta (oráculo a mano) | Polinomio λ³ + (11/125)λ² − (113/125)λ + 1/125; aviso «λ = −1 es autovalor exacto de T»; NO_CONVERGE, decisión exacta. En la comparación, SOR llega a k_max = 50 | Sí |

## Casos añadidos en la revisión del 03-nov-2026 (precondicionamiento, reordenamiento, Sarrus)

| ID | Caso | Salida esperada (oráculo) | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| IV-23 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | Tridiagonal [−1, 4, −1] 4×4, b = (1, 0, 0, 1), precondicionador M = D | Lámina S9-05/10 diap. 18: M = 4I, M⁻¹A = A/4. Teoría: κ(A/4) = κ(A); T_J, T_GS y T_ω no cambian. Richardson: ρ(I − A) = 3 + 2cos(π/5) ≈ 4.618 (no converge); con M = D, ρ = cos(π/5)/2 ≈ 0.405 | B = A/4; κ∞ = 30/11 en ambos; T y c idénticas (exacto); Richardson: máximo o desbordamiento sin precondicionar, y converge con M = D en las mismas iteraciones que Jacobi | Sí |
| IV-24 | A = [[100, 1], [1, 1/50]], M = D | Inversas 2×2 a mano: κ∞(A) = 101·101 = 10201; κ∞(D⁻¹A) = 51·102 = 5202 | 10201 y 5202; conclusión «mejora» | Sí |
| IV-25 | Ecuaciones de la Tarea II #3 desordenadas: [[−1, 4, −1], [0, −1, 3], [4, −1, 0]], b = (10, 10, 15) | El orden (E3, E1, E2) da [[4, −1, 0], [−1, 4, −1], [0, −1, 3]], b = (15, 10, 10), que es estrictamente dominante | Mismo orden y matriz. La pestaña «Convergencia» lo sugiere aunque a₃₃ = 0 | Sí |
| IV-26 (RETIRADO: procedimiento de extensión, ver matriz de fidelidad) | T_J de S9-07/10, desarrollo de Sarrus | tr = 0, Σ menores = 4/9, det = 4/3 (a mano) → −λ³ − (4/9)λ + 4/3 | (0, 4/9, 4/3); coincide con Faddeev-LeVerrier | Sí |
