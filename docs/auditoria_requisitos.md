# Matriz de cumplimiento (rúbrica oficial)

- **Fuente:** `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` (OFICIAL). Los identificadores son los de la auditoría documental.
- **Fecha de esta revisión:** 27-oct-2026.

**Estados:**

| Estado | Significado |
|---|---|
| No iniciado | — |
| En desarrollo | — |
| Implementado | Existe el código o el documento |
| Probado | Hay pruebas automáticas que se ejecutaron y pasan |
| Verificado | Además se comparó el comportamiento real con el criterio oficial usando referencias independientes |
| Bloqueado | Depende de algo externo |
| No aplicable | Con su justificación |

Última ejecución de pruebas: `python -m unittest` → **176 pruebas, 0 fallos**.

## Requisitos generales

| ID | Requisito | Fuente | Implementación | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|---|
| R-01 | Una sola aplicación integrada con 4 módulos | p. 2, 3, 5 | `app.py` | `tests/test_app.py` | Verificado | Navegación por los 4 módulos ejecutada con AppTest y con el servidor real (localhost:8501) |
| R-02 | Algoritmos centrales desde cero | p. 1, 5 | `algebra/` | revisión de imports | Verificado | `algebra/` solo importa `fractions`, `math`, `cmath`, `dataclasses` y módulos propios |
| R-03 | Documentar las bibliotecas de interfaz y gráficas | p. 1 | `docs/herramientas_y_bibliotecas.md` | — | Implementado | Documento |

## Módulo I (8 %)

| ID | Requisito | Implementación | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|
| M1-01 | Entrada Ax = b | `interfaz/modulo_directos.py`, `validacion.leer_matriz` | test_validacion, test_app | Probado | — |
| M1-02 | Gauss / Gauss-Jordan desde cero | `algebra/directos.py` | test_directos (21) | Verificado | Soluciones comprobadas por sustitución (casos I-1 a I-6) |
| M1-03 | Procedimiento paso a paso | `Paso`, `mostrar_pasos` | test_directos.test_pasos_registrados | Probado | Pasos visibles en la interfaz (verificado en el navegador) |
| M1-04 | Clasificación única / infinitas / inconsistente | `_resolver` (rangos) | test_directos, test_app | Verificado | Casos I-1, I-4 e I-5 |
| M1-05 | Dimensiones y pivotes nulos o problemáticos | `validar_sistema`, `_buscar_pivote`, `UMBRAL_PIVOTE_PEQUENO` | test_directos | Probado | Intercambio registrado con motivo; aviso de pivote pequeño |

## Módulo II (8 %)

| ID | Requisito | Implementación | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|
| M2-01 | κ∞ con inversa propia | `numero_condicion_infinito` + `inversa_gauss_jordan` | test_condicion | Verificado | κ = 3, 16/5, 41 y 40004.0001 derivados a mano |
| M2-02 | Interpretación con la escala 10/100 | `clasificar_kappa` | test_umbrales | Verificado | Límites exactos 10 y 100 |
| M2-03 | Perturbación absoluta o porcentual | `construir_delta_b` | test_condicion | Probado | La interpretación del porcentaje está pendiente de confirmar |
| M2-04 | Comparar la solución original con la perturbada | `analizar_perturbacion`, tabla | test_condicion | Verificado | Caso II-1 |
| M2-05 | ‖Δb‖/‖b‖ y ‖Δx‖/‖x‖ con denominador ≠ 0 | `analizar_perturbacion` | test_denominador_cero | Probado | — |
| M2-06 | Explicación de la sensibilidad | `_interpretar`, `_TEXTO_SENSIBILIDAD` | test_app.test_modulo_II | Probado | — |

## Módulo III (8 %)

| ID | Requisito | Implementación | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|
| M3-01 | Detección de sistema sobredeterminado | `clasificar_forma` | test_minimos | Probado | — |
| M3-02 | AᵀA x = Aᵀb | `minimos_cuadrados` | test_minimos | Verificado | Casos III-1 y III-2 |
| M3-03 | Resolución con un método directo propio | `resolver_gauss` | test_minimos | Verificado | — |
| M3-04 | r = b − Ax̂ y ‖r‖₂ | `minimos_cuadrados` | test_minimos | Verificado | Aᵀr = 0 |
| M3-05 | Ajuste lineal y ecuación de la recta | `ajuste_lineal` | test_minimos, test_app | Verificado | Fórmula cerrada m = 3/4, c = 6/5 |
| M3-06 | Gráfica de datos y recta | `grafica_ajuste` | test_app.test_modulo_III | Probado | La figura se genera sin errores; no hay prueba automática del contenido visual |

## Módulo IV (8 %)

| ID | Requisito | Implementación | Prueba | Estado | Evidencia |
|---|---|---|---|---|---|
| M4-01 | Jacobi, GS y SOR desde cero | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor` | test_iterativos | Verificado | P1–P3, P5, P15 |
| M4-02 | x⁽⁰⁾, ε, k_max y ω validados | `validar_configuracion`, `leer_*` | P20 | Probado | — |
| M4-03 | Tabla k, x⁽ᵏ⁾ y error de parada | `ResultadoIterativo.historial`, `filas_tabla` | test_iterativos, test_app | Probado | La columna del criterio activo está marcada |
| M4-04 | Dominancia diagonal | `dominancia_diagonal` | TestDominancia | Probado | — |
| M4-05 | Matriz de iteración y ρ(T) sin bibliotecas | `algebra/espectral.py` | test_espectral (19) | Verificado | Oráculos: Sarrus a mano, formas cerradas, bisección, teoría tridiagonal. **El alcance está pendiente de confirmar** (n > 3, métodos extra) |
| M4-06 | Motivo de finalización | Códigos y mensajes de `iterativos.py` | P8–P14, P16 | Verificado | Nunca afirma divergencia por k_max |
| M4-07 | Comparación por iteraciones y error final | `comparar_metodos` | P18, P19 | Probado | La definición oficial de «error final» está pendiente; se muestran d, r y e |
| M4-08 | Gráfica de error frente a iteración | `grafica_convergencia`, `grafica_comparacion` | test_app | Probado | — |

## Criterios transversales

| ID | Criterio | Peso | Estado | Evidencia o comentario |
|---|---|---|---|---|
| C-01 | Procedimiento matemático visible | 7 % | Implementado | Pasos (I), Gauss-Jordan de la inversa (II), ecuaciones normales (III), D, L, U, T y polinomio (IV) |
| C-02 | Análisis e interpretación | 6 % | Implementado | Textos de interpretación en los 4 módulos |
| C-03 | Código modular y comentado | 5 % | Implementado | `docs/arquitectura.md` |
| C-04 | Validaciones sin cierres inesperados | 4 % | Probado | test_validacion, P20, test_app (entradas inválidas) |
| C-05 | Interfaz intuitiva | 5 % | Implementado | Revisado en el navegador; la usabilidad no se probó con usuarios |
| C-06 | Manual de usuario | 3 % | Implementado | `docs/manual_usuario.md`; **no se probó con una persona ajena al equipo** |
| C-07 | Casos de prueba y caso obligatorio | 3 % | Bloqueado (parcial) | `casos_prueba/` completos; el caso obligatorio de la docente **no se ha recibido** |

## Validaciones obligatorias (OFICIAL p. 3)

| ID | Validación | Estado | Prueba |
|---|---|---|---|
| V-01 | Campos vacíos y formatos no numéricos | Probado | test_validacion, test_app |
| V-02 | Dimensiones incompatibles | Probado | test_matriz, test_directos, P20 |
| V-03 | Matriz singular o casi singular | Probado | Singular: test_directos y test_condicion. Casi singular: aviso de pivote pequeño y κ alto |
| V-04 | Divisiones entre cero y pivotes nulos | Probado | test_directos, P14 |
| V-05 | ε > 0 y k_max entero positivo | Probado | P20 |
| V-06 | 0 < ω < 2 con aviso | Probado | P20 |
| V-07 | Sin cierres; mensajes comprensibles | Probado | `ejecutar` no lanza excepciones; test_app |

## Entregables (OFICIAL p. 1)

| ID | Entregable | Estado | Comentario |
|---|---|---|---|
| E-01 | ZIP `Grupo(01-02)-IF0012-Proyecto-IIC.zip` | Implementado | `empaquetar.py 01` o `02`; falta confirmar el número de grupo |
| E-02 | Mecanismo de ejecución | Probado | `ejecutar.bat`; instalación probada en un entorno virtual limpio (ver estado_desarrollo.md), no en otro equipo |
| E-03 | Manual de usuario | Implementado | `docs/manual_usuario.md` |
| E-04 | Instrucciones de ejecución | Implementado | README y manual §1 |
| E-05 | Código fuente comentado | Implementado | — |
| E-06 | Carpeta de casos de prueba | Implementado | Falta el caso obligatorio |
| E-07 | Bibliotecas documentadas | Implementado | — |
| E-08 | Citar el código externo | No aplicable | No se copió código externo. El uso de IA se declara en herramientas_y_bibliotecas.md §4 |

## Defensa (35 %)

| ID | Criterio | Estado |
|---|---|---|
| D-01 a D-05 | Dominio, explicación, uso, claridad, comunicación | No iniciado: preparación del grupo con `docs/guia_defensa.md` |

## Incentivos por innovación (hasta 5 %, OFICIAL p. 5)

| ID | Incentivo | Estado | Evidencia que se presentaría |
|---|---|---|---|
| I-01 | Visualización avanzada (hasta 1 %) | Implementado | Comparación superpuesta de los 3 métodos (d, r, e); autovalores en el plano complejo con el círculo unidad; barrido de ω; CSV exportable de iteraciones |
| I-02 | Precondicionamiento (hasta 1.5 %) | Bloqueado | Con M = D no hay efecto en Jacobi, GS ni SOR (demostrado); falta la aclaración de la docente |
| I-03 | Matrices dispersas (hasta 1 %) | Probado | Formato CSR propio (`algebra/dispersas.py`), con pasos de Jacobi, GS y SOR que recorren solo los no nulos: O(nnz) por iteración frente a O(n²). Iteraciones idénticas a las densas (prueba); el paso CSR es 52 veces más rápido en una tridiagonal de 400×400 (medido); casilla «almacenamiento disperso» en el Módulo IV |
| I-04 | Experiencia de usuario (hasta 0.5 %) | Implementado | Ejemplos del curso cargables, ayudas contextuales, mensajes con la posición del error, interpretación geométrica 2D y 3D |
| I-05 | Extensión matemática (hasta 1 %) | Implementado | ρ(T) para n ≤ 8 con autovalores complejos (Faddeev-LeVerrier + Durand-Kerner, verificados); forma paramétrica de las infinitas soluciones; determinante; decisión exacta de Schur-Cohn |

La concesión de los incentivos depende de la evaluación de la docente. Aquí solo se indica qué evidencia existe.
