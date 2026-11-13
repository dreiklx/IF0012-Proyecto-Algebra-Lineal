# Pruebas basadas en los ejemplos resueltos de la profesora

Archivo de pruebas: `tests/referencia_profesora/test_ejemplos_verificados.py`
(ejecutar con `python -m unittest tests.referencia_profesora.test_ejemplos_verificados`).

**Regla:** solo aparecen aquí ejemplos cuyas páginas se han leído en imagen (revisión visual).
Los ejercicios sintéticos de otros archivos de `tests/` no pertenecen a este grupo. Las
erratas de las láminas se fijan con el valor correcto y se indican.

Leyenda de valores: **T** = transcrito de la imagen de la lámina; **D** = derivado, recalculado
siguiendo exactamente las operaciones escritas por la profesora.

## Resumen

| Ejemplos encontrados (con imagen revisada en esta etapa) | Convertidos en prueba | Aprobados | Fallidos |
|---|---|---|---|
| 5 bloques de páginas (S6-16/09 p. 29; S7-21/09 p. 19; S9-07/10 pp. 3-7) | 13 pruebas | 13 | 0 |

**Pendientes de revisión visual** (aparecen en los índices de las láminas, pero no se han leído en imagen y por tanto no hay prueba):

| Ejemplo | Lámina | Motivo |
|---|---|---|
| Gauss con pivote nulo / resolución de S6-14/09 p. 29 (la lámina da un resultado erróneo) | S6-14/09 p. 29 | Pendiente: `interfaz/compartido/ejemplos.py` lo cita, no se ha leído en imagen |
| Factorización LU de S6-16/09 p. 35 | S6-16/09 p. 35 | Pendiente |
| κ∞ de S7-21/09 pp. 15 y 20; de S8-28/09 p. 13 | S7-21, S8-28 | Pendiente |
| Mínimos cuadrados completos de S8-30/09 pp. 6-9 (x̂ = (65/33, −29/33); recta y = 0,75x + 1,2) | S8-30/09 | Solo se ha leído la tabla de datos (p. 8); el resultado está en las páginas siguientes |
| Criterio de parada x⁽⁸⁾ − x⁽⁷⁾ = 0,002 < 0,01 | S8-28/09 p. 6 | Pendiente; la norma del ejemplo es ambigua (ver `decision_graficas.md`) |
| Jacobi, Gauss-Seidel y SOR de S8-30/09 pp. 19, 32 | S8-30/09 | Pendiente |
| Tridiagonal de S9-05/10 p. 14 | S9-05/10 | Pendiente |
| Dominancia de S8-30/09 p. 37 | S8-30/09 | Pendiente |

Ningún ejemplo pendiente se ha dado por validado. El proyecto **no** puede declararse validado
al 100 % mientras queden estos ejemplos sin revisar.

## Índice de pruebas

### 1. S6-16/09 p. 29 — Gauss (ejemplo precargado «S6-16/09 p. 29 — solución única»)

Imagen: `docs/auditoria/evidencias/modulo_I/S6-16_p29.jpg`.

| Elemento | Valor | Tipo | Ax | Estado |
|---|---|---|---|---|
| Entrada | x + y + z = 6; 2x + y − z = 3; −x + y + 2z = 7 | T | misma | — |
| Paso 1 | −2F₁ + F₂ → fila 2 = (0, −1, −3 | −9) | T | notación «−2F₁ + F₂» y matriz (D) | Coincide |
| Paso 2 | F₁ + F₃ → fila 3 = (0, 2, 3 | 13) | T | notación «F₁ + F₃» y matriz | Coincide |
| Paso 3 | Lámina: −F₂, luego −2F₂ + F₃ → fila 3 = (0, 0, −3 | −5) | T (parcial) | Ax: «2F₂ + F₃», sin el paso −F₂ | **Simplificación equivalente**: Ax no normaliza la fila pivote; el resultado es el mismo |
| Paso 4 | (−1/3)F₃ → z = 5/3 | T | Ax lo obtiene por sustitución hacia atrás | Coincide en el valor |
| Solución | Sol = {(1/3, 4, 5/3)} | T | `solucion` = (1/3, 4, 5/3) | Coincide |

Prueba: `TestS616Gauss` (3 pruebas).

### 2. S6-16/09 p. 29 — sustitución hacia atrás (segundo ejemplo de la misma página)

Sistema x₁ − x₂ + x₃ = 4; x₂ + x₃ = 3; x₃ = 1 ⇒ Sol = {(5, 2, 1)}. Valores **T** (lectura en imagen).

Prueba: `TestS616SustitucionHaciaAtras`.

### 3. S7-21/09 p. 19 — número de condición con la norma ∞ (B = [[1, 2], [3, 1]])

Imagen: `docs/auditoria/evidencias/modulo_II/S7-21_p19.jpg`.

| Paso de la profesora | Valor | Tipo | Ax | Estado |
|---|---|---|---|---|
| 1 Norma ∞ (suma de valores absolutos por fila) | — | T | `sumas_absolutas_por_fila` | Coincide |
| 2 Fila 1: 1 + 2 = 3; Fila 2: 3 + 1 = 4; ‖B‖∞ = 4 | 3, 4, 4 | T | 3, 4, 4 | Coincide |
| 3 B⁻¹ = [[−1/5, 2/5], [3/5, −1/5]] | exacta | T | misma | Coincide |
| 4 Fila 1: |−1/5| + |2/5| = 3/5; Fila 2: |3/5| + |−1/5| = 4/5; ‖B⁻¹‖∞ = 4/5 | 3/5, 4/5 | T | 3/5, 4/5 | Coincide |
| 5 κ∞ = 4 · 4/5 = 16/5 ≈ 3,2 | 16/5 | T | 16/5 | Coincide |

Prueba: `TestS721Condicionamiento`.

### 4. S9-07/10 pp. 3-5 — Jacobi para A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]], b = (9, 9, −2)

Imagen: `docs/auditoria/evidencias/modulo_IV/S9-07_p4.jpg` y `S9-07_p5.jpg`.

| Elemento | Valor | Tipo | Ax | Estado |
|---|---|---|---|---|
| Descomposición A = D + L + U | D = diag(3, 3, 3) | T | `descomponer` | Coincide |
| T_J = −D⁻¹(L + U) | [[0, −1, −1], [−1, 0, −2/3], [1, 2/3, 0]] | T | misma | Coincide (exacto) |
| c_J = D⁻¹b | (3, 3, −2/3) | T | misma | Coincide |
| x⁽¹⁾ desde x⁽⁰⁾ = 0 | (3, 3, −2/3) | T | misma | Coincide |
| x⁽²⁾ primeras componentes | (2/3, 4/9, …) | T | (2/3, 4/9, 13/3) | Coincide en las dos primeras; la tercera **no se lee con certeza** en la imagen: no se usa como referencia |
| det(T − λI) | −λ³ − (4/9)λ **+ 4/3** | D | λ³ + (4/9)λ − 4/3 (equivalente) | Lámina p. 5: omite +4/3 → **errata** |
| ρ(T_J) | ≈ 1,1744 | D | 1,17436 | Coincide; la lámina dice ρ = 0 (errata) |

Pruebas: `TestS907Jacobi` (4 pruebas).

### 5. S9-07/10 pp. 6-7 — Gauss-Seidel para el mismo sistema

Imagen: `docs/auditoria/evidencias/modulo_IV/S9-07_p6.jpg` y `S9-07_p7.jpg`.

| Elemento | Valor | Tipo | Ax | Estado |
|---|---|---|---|---|
| T_GS = −(D + L)⁻¹U | [[0, −1, −1], [0, 1, 1/3], [0, −1/3, −7/9]] | T | misma | Coincide (exacto) |
| c_GS | (D + L)⁻¹b = (3, 0, 7/3) | D | (3, 0, 7/3) | **La lámina (p. 7) escribe −(D+L)⁻¹b y calcula T_GS·b = (−7, 25/3, −13/9): errata** |
| x⁽¹⁾ | (3, 0, 7/3) | D | (3, 0, 7/3) | La lámina propaga el error (−7, 25/3, −13/9) |
| ρ(T_GS) | ≈ 0,9351 (λ₁ = 0,9351; λ₂ = −0,7129; λ₃ = 0) | T | 0,93513 | Coincide |

Pruebas: `TestS907GaussSeidel` (4 pruebas).

## Relación con las erratas de las láminas

Ver `docs/auditoria/discrepancias.md` (D1 a D6). Las pruebas fijan el valor correcto; no copian
el de la lámina.

## Estado global

- Pruebas de ejemplos de la profesora: 13 (13 aprobadas; 0 fallidas) con las páginas revisadas en imagen.
- Ejemplos con página sin revisar visualmente: ver la tabla de pendientes.
- Procedimientos sin prueba posible por falta de datos en la lámina: la tercera componente de x⁽²⁾ de Jacobi (ver D5).
