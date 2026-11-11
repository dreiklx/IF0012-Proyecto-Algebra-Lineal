# `auditoria/`: verificación independiente

Guiones que comparan el núcleo con **oráculos calculados de otra forma** sobre miles de casos aleatorios. No forman parte de la suite rápida porque tardan entre 20 s y 1 min. Se ejecutan desde la raíz del proyecto:

| Guion | Qué audita | Casos |
|---|---|---|
| `auditoria_directos.py .` | Gauss y Gauss-Jordan (contra Cramer y la sustitución); inversa, determinante (fórmula de Leibniz) y κ; perturbación; mínimos cuadrados (Aᵀr = 0) | 4500 + 400 + 200 + 300 |
| `auditoria_iterativos.py .` | iteraciones contra una implementación separada; ρ(T) contra la fórmula de Gelfand | 600 + 300 |
| `auditoria_precondicionamiento.py .` | M = D: T y c idénticas, κ y autovalores | 150 |
| `casos_dificiles.py .` | raíces múltiples, ρ muy cerca de 1 y grado 8 | casos fijos |

Resultado esperado: **0 fallos** en todas las baterías (último registro: 11-nov-2026).
