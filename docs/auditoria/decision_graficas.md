# Decisión sobre gráficas por módulo (12-nov-2026)

Nota de verificación: las páginas citadas (S6-14/09 p. 26, S7-21/09 pp. 18-19) se consultaron por OCR
y por la auditoría anterior; **no se han revisado visualmente en esta etapa**. La decisión no depende
de su contenido gráfico exacto, pero debe confirmarse al revisar esas páginas.

Criterio: una gráfica se añade solo si la materia del curso la usa, si el enunciado la pide,
o si explica un concepto de clase que el procedimiento escrito no muestra con claridad.
No se añaden gráficas para igualar módulos. Las extensiones no vistas en clase no se
presentan como materia de la profesora.

## Obligatorias (OFICIAL p. 2)

| Módulo | Exigencia literal | Implementación | Estado |
|---|---|---|---|
| III | «Generar una gráfica con los datos y la recta de mejor ajuste.» | `visualizacion/interactivas.py::ajuste` (datos, recta, residuos) | Cumple; sin cambios |
| IV | «Mostrar una gráfica error vs. iteración para facilitar la comparación.» | `interactivas.convergencia` (d_k y r_k frente a k) y `interactivas.comparacion` (error final por método) | Cumple; sin cambios |

## Módulo I (sistemas lineales)

**Existente:** `interactivas.rectas_2d` (dos incógnitas: rectas, punto de intersección o rectas paralelas)
y `interactivas.planos_3d` (tres incógnitas: planos y la solución). Ambas muestran exactamente la
clasificación de clase (S6-14/09 p. 26): planos que se cortan en un punto, en una recta o no tienen
punto común.

**Evaluación de una gráfica adicional:** no se añade. El paso a paso de Gauss (la lámina
S6-14/09 p. 26 y el procedimiento «−2F₁ + F₂») no necesita una figura para verificarse, y las
dos gráficas existentes ya cubren la interpretación geométrica. Otra vista duplicaría
`planos_3d` sin aportar.

**Decisión:** sin cambios.

## Módulo II (determinantes, inversa, normas, condicionamiento)

**Evaluación:** κ∞ es un número (producto de dos normas). Las láminas de la profesora (S7-21/09 p. 18-19)
calculan ‖A‖∞, ‖A⁻¹‖∞ y κ con sumas por filas y no usan ninguna figura. Una gráfica del
efecto de la perturbación o de la transformación lineal de A sería teoría que no aparece en
los documentos; presentarla como visto en clase sería incorrecto. Una visualización de la
amplificación del error (‖Δx‖/‖x‖ frente a ‖Δb‖/‖b‖) sería una extensión (Cat. C): no aporta
nada que el informe numérico no diga ya.

**Decisión:** no añadir gráfica. Justificación para la defensa: el módulo es numérico y su
resultado (κ y su escala de tres niveles) cabe en una tabla.

## Resumen

| Módulo | Gráfica exigida | Gráfica en Ax | Acción |
|---|---|---|---|
| I | No | Rectas 2D y planos 3D (existentes) | Ninguna |
| II | No | Ninguna | Ninguna (decisión justificada) |
| III | Sí | Ajuste | Ninguna |
| IV | Sí | Convergencia, comparación, autovalores, precondicionador | Ninguna |
