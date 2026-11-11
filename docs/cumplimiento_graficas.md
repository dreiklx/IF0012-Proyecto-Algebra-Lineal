# ¿Exige el proyecto gráficas en todos los módulos?

**Revisión del 11-nov-2026.** Se volvió a extraer el texto del enunciado (`INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf`, 5 páginas, «OFICIAL») página por página y se buscaron todos los requisitos visuales.

## Respuesta corta

**No.** El enunciado pide **dos** gráficas: una en el Módulo III y una en el Módulo IV. Los módulos I y II no tienen ningún requisito de gráfica. Ax cumple ambas y no agrega gráficas decorativas a los módulos I y II.

## 1. Requisitos visuales, textuales

| Documento | Pág. | Texto exacto | Interpretación |
|---|---|---|---|
| OFICIAL | 1 | Objetivo específico 7: «Presentar resultados de forma clara, justificada y visual, con rigor matemático y computacional» | Objetivo general de presentación. **No** exige una gráfica por módulo |
| OFICIAL | 1 | «Se permiten estructuras de datos, entrada/salida, interfaz gráfica, gráficos y operaciones aritméticas elementales» | Autoriza bibliotecas de gráficos (no calcular con ellas) |
| OFICIAL | 2 | Módulo I: ingreso Ax = b, Gauss o Gauss-Jordan, «Presentación del procedimiento paso a paso», clasificación, validación | **Ninguna gráfica.** Lo visual es el paso a paso |
| OFICIAL | 2 | Módulo II: κ∞, interpretación, perturbación, «Comparar la solución original y la perturbada», reportar errores relativos, explicar | **Ninguna gráfica.** La comparación puede ser numérica (tabla) |
| OFICIAL | 2 | Módulo III: «Generar una gráfica con los datos y la recta de mejor ajuste.» | **Gráfica obligatoria** |
| OFICIAL | 2 | Módulo IV: «Mostrar una gráfica error vs. iteración para facilitar la comparación.» | **Gráfica obligatoria**: error frente a k, que sirva para comparar los métodos |
| OFICIAL | 4 | Rúbrica Módulo III, Excelente: «Ecuaciones normales, residual, error, ajuste y gráfica correctos.» Aceptable: «… interpretación o visualización limitada» | La gráfica del III se evalúa |
| OFICIAL | 4 | Rúbrica Módulo IV, Excelente: «… convergencia, error y comparación bien presentados» | La presentación del error y de la comparación se evalúa |
| OFICIAL | 4 | Rúbrica Interfaz: «resultados fáciles de interpretar» | General |
| OFICIAL | 5 | Incentivo «Visualización avanzada»: «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» (hasta 1 %) | Gráficas **adicionales** = opcionales |
| OFICIAL | 5 | Lista de cotejo: «Los procedimientos matemáticos pueden visualizarse o verificarse» | Se refiere a ver el procedimiento (pasos), no a graficar |

**Modelo de la profesora para el Módulo IV** (S9-05/10 pp. 16-17, diapositivas 12-13): «Evolución del error: se muestra el error relativo ‖x⁽ᵏ⁾ − x‖∞ en función del número de iteraciones, con tolerancia ε = 10⁻⁴», en escala logarítmica y con los tres métodos superpuestos.

## 2. Matriz de cumplimiento gráfico

| Módulo | Qué exige el enunciado | Gráfica necesaria | Gráfica actual en Ax | Estado |
|---|---|---|---|---|
| I | Paso a paso y clasificación (p. 2) | **Ninguna** | `interactivas.rectas_2d` y `planos_3d` (interpretación geométrica, con control gestual) | Opcional. Cuenta para el incentivo de experiencia de usuario; respaldo de clase en S6-14/09 p. 26 («la solución de un sistema lineal tiene un significado geométrico») |
| II | Comparar soluciones y reportar errores relativos (p. 2) | **Ninguna** | Ninguna: tabla original/perturbada, cota y escala de κ | Cumple sin gráfica. No se agrega una gráfica decorativa |
| III | «Gráfica con los datos y la recta de mejor ajuste» (p. 2) | **Datos y recta** | `interactivas.ajuste`: puntos (xᵢ, yᵢ), recta y = mx + c, residuos verticales, mayor \|rᵢ\| | ✅ Cumple |
| IV | «Gráfica error vs. iteración para facilitar la comparación» (p. 2) | **Error frente a k, comparando métodos** | `interactivas.convergencia` (dₖ y rₖ de un método, ε, motivo de parada); `interactivas.comparacion` (eₖ = ‖x⁽ᵏ⁾ − x*‖∞, dₖ o rₖ de los 3 métodos, escala log.) | ✅ Cumple, con la misma forma que la lámina S9-05/10 p. 17 |
| IV (extra) | — | — | `autovalores` (λ y círculo unidad), `precondicionador` (efecto de M = D), barrido de ω | Opcionales: incentivos de extensión matemática y precondicionamiento |

**Gráficas obligatorias:** `ajuste` (III), y `convergencia` y `comparacion` (IV).
**Gráficas opcionales:** `rectas_2d`, `planos_3d`, `autovalores`, `precondicionador`.

## 3. ¿Son académicamente correctas?

| Gráfica | Necesidad real | Datos | Coherencia con la profesora | Etiquetas |
|---|---|---|---|---|
| `ajuste` | La exige el enunciado | Los puntos son los datos; la recta usa m y c de `minimos.ajuste_lineal` (ecuaciones normales resueltas con Gauss); los residuos son b − Ax̂ del núcleo. Prueba: `test_graficas_interactivas.test_ajuste` | Ajuste lineal como caso de mínimos cuadrados (S8-30/09 p. 8) | y = mx + c, r<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub> ✅ |
| `convergencia` | La exige el enunciado (error vs. iteración) | dₖ y rₖ salen del historial de `ejecucion.ejecutar`, sin recalcular. El estado final sale del **código de terminación**: con k_max nunca dice «ε alcanzado». Pruebas: `test_graficas_exploracion` | Criterio de parada ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖ < ε o residuo (S8-28/09 p. 6), escala logarítmica | d<sub>k</sub>, r<sub>k</sub>, k<sub>max</sub>, ε ✅ |
| `comparacion` | La exige el enunciado («para facilitar la comparación») | Las mismas iteraciones de los 3 métodos con la misma configuración (`comparacion.comparar_metodos`). eₖ contra x* exacta de Gauss. La línea ε aparece solo si la métrica es la del criterio | Igual que S9-05/10 p. 17: ‖x⁽ᵏ⁾ − x‖∞ en escala log. | e<sub>k</sub>, d<sub>k</sub>, r<sub>k</sub> ✅ |
| `rectas_2d` / `planos_3d` | Interpretación geométrica (opcional) | Ecuaciones de A y b; la solución o la recta de soluciones es la de `directos`. Prueba: cada esquina dibujada cumple su ecuación | S6-14/09 p. 26: punto, recta o sin punto común | Ecuaciones con signos correctos (11-nov) ✅ |
| `autovalores` | Ver por qué ρ(T) decide la convergencia | Autovalores de `espectral.radio_espectral` | ρ(T) = máx\|λ\| (S9-07/10 p. 4) | \|λ\| = ρ(T), círculo \|λ\| = 1 ✅ |
| `precondicionador` | Mostrar el efecto de M = D (incentivo) | dₖ de cada método con y sin M = D, del núcleo | S9-05/10 pp. 19-23; la lámina 19 no es reproducible (documentado en `investigacion_richardson.md`) | d<sub>k</sub> ✅ |

**Conclusión:** no falta ninguna gráfica obligatoria y no se propone agregar ninguna. Las opcionales tienen una función matemática concreta y dibujan solo datos del núcleo, verificados por pruebas.
