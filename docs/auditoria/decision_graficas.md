# Decisión sobre gráficas por módulo (actualizada el 13-nov-2026)

Criterio: una gráfica se añade solo si la materia del curso la usa, si el enunciado la pide,
o si explica un concepto de clase que el procedimiento escrito no muestra con claridad.
Toda visualización no expresamente explicada en clase se identifica como **complementaria**.
No se añaden gráficas para igualar módulos.

Nota de verificación: las láminas citadas se han revisado visualmente (S7-21/09 pp. 18-19,
S8-30/09 p. 8, S2-19/08 p. 38), salvo los cuadrantes indicados en el inventario. El resto se
contrasta por OCR y no se considera revisado visualmente.

## Obligatorias (OFICIAL p. 2)

| Módulo | Exigencia literal | Implementación | Estado |
|---|---|---|---|
| III | «Generar una gráfica con los datos y la recta de mejor ajuste.» | `visualizacion/interactivas.py::ajuste`: puntos, recta y **segmentos verticales de residuo** rᵢ = yᵢ − ŷᵢ | Cumple. Verificada en la aplicación (captura `docs/auditoria/evidencias/capturas/modulo_III_ajuste.png`) |
| IV | «Mostrar una gráfica error vs. iteración para facilitar la comparación.» | `interactivas.convergencia` (d_k y r_k frente a k) y `interactivas.comparacion` | Cumple; sin cambios en esta etapa |

## Módulo I (sistemas lineales)

**Existente:** `interactivas.rectas_2d` (dos incógnitas: rectas, intersección o paralelas) y
`interactivas.planos_3d` (tres incógnitas: planos y solución), con control gestual 3D.

**Decisión:** sin cambios. Ambas gráficas ya muestran la clasificación de clase (S6-14/09 p. 26).
Una gráfica adicional de Gauss duplicaría `planos_3d` sin aportar.

## Módulo II (determinantes, inversa, normas, condicionamiento)

Se implementan **dos visualizaciones complementarias** (`visualizacion/geometria_modulo_II.py`),
con la matriz introducida por el usuario y los valores del núcleo. La interpretación del
determinante como factor de área **se retiró** (ver abajo):

| Visualización | Materia de clase relacionada | Tipo | Verificación |
|---|---|---|---|
| **Sumas absolutas por fila (norma ∞, máximo destacado) y por columna (norma 1, referencia)** | Norma ∞ = máxima suma de fila (S7-21/09 p. 19, pasos 2 y 4 de κ; la p. 17 solo por OCR) | Filas: procedimiento de clase. Columnas (norma 1): **complementaria** y no interviene en κ∞ | Las sumas coinciden con `sumas_absolutas_por_fila` (prueba); la barra destacada es la de la norma ∞ (prueba). Captura |
| **Perturbación frente a la cota κ∞·‖Δb‖/‖b‖** (tres barras) | Cota ‖Δx‖/‖x‖ ≤ κ·‖Δb‖/‖b‖ (S7-21/09 p. 18) | **Complementaria** (la cota es materia; el gráfico es apoyo) | Las barras coinciden con `analizar_perturbacion` (prueba). Captura |

**Retirado el 13-nov-2026: determinante como factor de área (2×2).** En S2-19/08 p. 38 (imagen
revisada) solo aparecen las propiedades del determinante (intercambio de filas, suma de múltiplos,
triangular, fila de ceros). La interpretación geométrica como área no aparece en los materiales.
Se elimina la visualización y su explicación. La captura se conserva en
`docs/auditoria/evidencias/capturas/retiradas/`.

**Qué no se implementa y por qué:**
- Extensión 3D (paralelepípedo para 3×3): no implementada. Requiere teoría de volumen que la
  materia del curso no desarrolla en las láminas revisadas; sería una extensión sin respaldo en clase.
- Gráfica de κ como clasificación de sensibilidad: no añadida. La escala 10/100 es un criterio
  operativo del enunciado (OFICIAL p. 2), no una magnitud que una figura aporte.

**Diferencia detectada en las láminas:** S7-21/09 p. 18 clasifica κ en 5 niveles (1, 10, 10³,
10⁶). El enunciado fija 3 niveles (10 y 100). Ax usa los 3 del enunciado (diferencia justificada).

## Módulo III · tabla de ajuste (complementaria)

Además de la gráfica exigida, se muestra una tabla con xᵢ, yᵢ observado, ŷᵢ = m·xᵢ + c estimado y
rᵢ = yᵢ − ŷᵢ (`interfaz/modulos/modulo_III_minimos.py::tabla_ajuste`). Usa los vectores exactos
del núcleo; no recalcula el ajuste. Prueba: Σ rᵢ = 0 con intercepto; los valores del ejemplo
(m = 3/4, c = 6/5, ŷ₁ = 39/20) coinciden con el cálculo a mano.

**Actualización de datos:** si el usuario cambia la tabla de puntos después de calcular, la
interfaz muestra un aviso y pide recalcular; los resultados anteriores no se presentan como actuales.
Lo mismo ocurre en el Módulo II al cambiar A, b o la perturbación.

## Resumen

| Módulo | Gráfica exigida | Gráficas en Ax | Acción en esta etapa |
|---|---|---|---|
| I | No | Rectas 2D y planos 3D | Ninguna |
| II | No | Normas ∞ (filas, con MediaPipe 2D) y norma 1 (columnas), sensibilidad (complementarias) | **Añadidas**; determinante geométrico **retirado** |
| III | Sí | Ajuste con residuos verticales; tabla de residuos (complementaria) | **Tabla añadida**; gráfica verificada sin duplicar |
| IV | Sí | Convergencia, comparación, autovalores, precondicionador | Ninguna |

## Actualización 13-nov-2026 (MediaPipe en el Módulo III)

La gráfica de mínimos cuadrados (obligatoria, OFICIAL p. 2) tiene control gestual 2D con
objetivo propio `2d_m3`. Solo cambia la vista de los ejes: datos, recta, estimados y residuos
no cambian (ver `docs/mediapipe_2d.md`, sección Módulo III).
