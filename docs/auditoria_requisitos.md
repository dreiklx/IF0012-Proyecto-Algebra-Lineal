# Matriz de cumplimiento — revisión del 02-nov-2026

- **Fuente de los requisitos:** `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` (OFICIAL), páginas 1 a 5, leído de nuevo el 02-nov-2026. Los identificadores (R-, M1-…, V-, E-, C-, I-) son los de la auditoría documental.
- **Formato:** REQUISITO → IMPLEMENTACIÓN → ARCHIVO O FUNCIÓN → PRUEBA → ESTADO.
- **Pendientes con la docente:** el detalle de cada uno está en [pendientes_docente.md](pendientes_docente.md).

## Estados

| Estado | Significado |
|---|---|
| **COMPLETADO** | Existe la implementación y hay evidencia ejecutada: pruebas automáticas que pasan y, en el núcleo, contraste con oráculos independientes (`auditoria/`, cálculos a mano o teoremas) |
| **INCOMPLETO** | Falta una parte que el grupo **sí** puede hacer, por ejemplo una prueba con una persona ajena |
| **FALLIDO** | Implementado, pero con resultados incorrectos. **Ningún requisito está en este estado** |
| **PENDIENTE DE CONFIRMACIÓN EXTERNA** | Depende de una respuesta de la docente o de un dato que el grupo debe confirmar |

## Evidencia general (02-nov-2026)

| Evidencia | Resultado |
|---|---|
| Pruebas automáticas: `.venv\Scripts\python -m unittest` | **185 pruebas, 185 OK.** Son las 184 anteriores más una nueva (IV-22) |
| Auditoría independiente: `auditoria/*.py` | **0 fallos** en 4500 sistemas, 400 inversas, determinantes y κ, 200 perturbaciones, 300 mínimos cuadrados, 600 ejecuciones iterativas y 300 análisis espectrales (0 indeterminados y 0 no fiables entre los aleatorios) |
| Ejemplos precargados de la interfaz recalculados con oráculos nuevos (02-nov) | Cramer y Leibniz (Módulo I), adjunta (κ), fórmula cerrada de la recta (Módulo III) y fórmula de Gelfand ‖T¹²⁸‖^(1/128) (ρ). **Todos coinciden** |
| Imports de `algebra/` | Solo `fractions`, `math`, `cmath`, `dataclasses` y módulos propios. **Ningún** `.py` del proyecto importa NumPy, SciPy ni SymPy |

## Restricciones generales (OFICIAL p. 1)

| ID | Requisito | Implementación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|---|
| R-01 | Una sola aplicación con los 4 módulos | Navegación lateral de Streamlit | `app.py` (`PAGINAS`) | `test_app` (abre los 4 módulos) | COMPLETADO |
| R-02 | Algoritmos centrales desde cero, sin bibliotecas que los implementen | Python puro con listas y `Fraction` | `algebra/` | Revisión de imports (arriba) y auditoría | COMPLETADO |
| R-03 | Documentar las bibliotecas de interfaz y gráficas | Streamlit y Matplotlib, con versiones fijadas | `docs/herramientas_y_bibliotecas.md`, `requirements.txt` | — | COMPLETADO (ver P-6 en pendientes: NumPy entra como dependencia interna) |
| R-04 | Todas las entradas validadas | Lectura de texto a `Fraction` y validación de dimensiones y parámetros | `algebra/validacion.py`, `algebra/matriz.py` (`validar_*`), `validar_configuracion` | `test_validacion`, `test_matriz`, P20, `test_app` | COMPLETADO |
| R-05 | Interfaz intuitiva, clara y funcional | Ejemplos cargables, ayudas, mensajes por color | `interfaz/` | `test_app` (solo funcionamiento) | INCOMPLETO: falta que la use una persona ajena al desarrollo. La calidad la juzga la docente |

## Módulo I — Sistemas lineales (8 %)

| ID | Requisito | Implementación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|---|
| M1-01 | Ingreso de Ax = b en forma matricial | Áreas de texto, una fila por línea | `modulo_directos.mostrar`, `leer_matriz`, `leer_vector` | `test_validacion`, `test_app` | COMPLETADO |
| M1-02 | Gauss o Gauss-Jordan desde cero | Eliminación exacta con fracciones; los dos métodos | `directos._escalonar`, `resolver_gauss`, `resolver_gauss_jordan` | `test_directos`; auditoría: 4500 casos | COMPLETADO |
| M1-03 | Procedimiento paso a paso | Cada operación elemental guarda un `Paso` (texto y matriz) | `directos.Paso`, `_escalonar`, `componentes.mostrar_pasos` | `test_pasos_registrados` | COMPLETADO |
| M1-04 | Clasificación automática: única, infinitas o inconsistente | Rangos de A y [A\|b] (Rouché-Frobenius); forma paramétrica | `_resolver`, `_rango_aumentada`, `_sustitucion_atras` | `test_directos`; auditoría: rangos por menores (Leibniz) | COMPLETADO |
| M1-05 | Validar dimensiones y detectar pivotes nulos o numéricamente problemáticos | Intercambio de filas con su motivo; aviso si \|pivote\| < 10⁻¹⁰·máx\|aᵢⱼ\| | `validar_sistema`, `_buscar_pivote`, `UMBRAL_PIVOTE_PEQUENO` | `test_directos` | COMPLETADO |
| — | Extra: interpretación geométrica 2D y 3D | Rectas y planos dibujados con el resultado del núcleo | `visualizacion/geometria_3d.py` | `test_app` (genera la figura); PNG revisados el 27-oct | COMPLETADO (no se vio dentro del navegador) |

## Módulo II — Condicionamiento (8 %)

| ID | Requisito | Implementación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|---|
| M2-01 | κ∞(A) = ‖A‖∞·‖A⁻¹‖∞ con inversa propia | Inversa por Gauss-Jordan [A\|I] → [I\|A⁻¹], verificada con A·A⁻¹ = I | `numero_condicion_infinito`, `inversa_gauss_jordan`, `norma_infinito_matriz` | `test_condicion`; auditoría: adjunta en 400 casos | COMPLETADO |
| M2-02 | Valor de κ e interpretación con la escala 10/100 | Escala oficial con los límites exactos | `clasificar_kappa`, `_TEXTO_SENSIBILIDAD` | `test_umbrales` | COMPLETADO |
| M2-03 | Perturbación de b por valor absoluto o porcentaje | Absoluta: Δb dado. Porcentual: Δbᵢ = p/100·bᵢ | `construir_delta_b` | `test_condicion` | COMPLETADO. Con un único p ambas lecturas del porcentaje dan el mismo ‖Δb‖∞/‖b‖∞ = \|p\|/100 (ver P-7); confirmarlo con la docente es opcional |
| M2-04 | Comparar las soluciones original y perturbada | Se resuelven Ax = b y Ax̃ = b + Δb con el Gauss propio | `analizar_perturbacion` | `test_condicion`; auditoría: Cramer en 200 casos | COMPLETADO |
| M2-05 | ‖Δb‖∞/‖b‖∞ y ‖Δx‖∞/‖x‖∞ cuando los denominadores no son cero | `None` y aviso si el denominador es 0 | `analizar_perturbacion` | `test_denominador_cero` | COMPLETADO |
| M2-06 | Explicar qué indica sobre la sensibilidad | Texto automático: amplificación observada frente a la cota κ·‖Δb‖/‖b‖ | `_interpretar` | `test_app` | COMPLETADO |
| V-03 | Matriz singular distinta de «κ grande» | Clasificación `MATRIZ_SINGULAR` aparte | `numero_condicion_infinito` | `test_modulo_II_singular` | COMPLETADO |

## Módulo III — Mínimos cuadrados (8 %)

| ID | Requisito | Implementación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|---|
| M3-01 | Detectar si el sistema es sobredeterminado | Compara m y n | `clasificar_forma` | `test_minimos` | COMPLETADO |
| M3-02 | Construir AᵀA x = Aᵀb | Transpuesta y productos propios | `minimos_cuadrados` (`transpuesta`, `multiplicar_matrices`) | `test_minimos`; auditoría: 300 casos | COMPLETADO |
| M3-03 | Resolverlas con un método directo ya implementado | `resolver_gauss` del Módulo I | `minimos_cuadrados` | `test_minimos` | COMPLETADO |
| M3-04 | r = b − Ax̂ y ‖r‖₂ | ‖r‖₂² exacta y raíz en float; se comprueba Aᵀr = 0 | `minimos_cuadrados` (`norma_2_cuadrado_vector`) | `test_minimos`; auditoría: Aᵀr = 0 exacto | COMPLETADO |
| M3-05 | Ajuste lineal y ecuación de la recta | Matriz de diseño [[xᵢ, 1]] | `ajuste_lineal` | `test_minimos` (fórmula cerrada), `test_app` | COMPLETADO |
| M3-06 | Gráfica de los datos y la recta | Puntos, recta y residuos | `graficos.grafica_ajuste` | `test_app`; vista en Chrome el 27-oct | COMPLETADO |
| — | AᵀA singular o datos insuficientes | Mensaje; no se presenta ningún x̂ | `minimos_cuadrados`, `ErrorAjuste` | `test_columnas_dependientes`, `test_datos_invalidos` | COMPLETADO |

## Módulo IV — Métodos iterativos (8 %)

| ID | Requisito | Implementación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|---|
| M4-01 | Jacobi, Gauss-Seidel y SOR desde cero | Un paso por método y un bucle común | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor`, `_ejecutar` | P1–P21; auditoría: 600 ejecuciones | COMPLETADO |
| M4-02 | Ingresar x⁽⁰⁾, ε y k_max; ω validado para SOR | Vector cero, bᵢ/aᵢᵢ o personalizado; 0 < ω < 2 | `validar_configuracion`, `leer_tolerancia`, `leer_omega`, `vector_diagonal` | P20, `test_tolerancias_extremas` | COMPLETADO |
| M4-03 | Tabla con k, x⁽ᵏ⁾ y el error usado como criterio de parada | Columnas d_k y r_k, rotuladas «(criterio de parada)» o «(informativo)» | `modulo_iterativos.filas_tabla` | `test_app` | COMPLETADO |
| M4-04 | Dominancia diagonal como criterio suficiente | Fila por fila: \|aᵢᵢ\| > Σ\|aᵢⱼ\| | `dominancia_diagonal` | `TestDominancia` | COMPLETADO |
| M4-05a | Matriz de iteración y ρ(T) sin funciones de biblioteca | T exacta, Faddeev-LeVerrier, raíces y decisiones exactas | `espectral.matriz_iteracion`, `polinomio_caracteristico`, `raices`, `radio_espectral` | `test_espectral` (25); auditoría: 300 casos | COMPLETADO para n ≤ 8. Con autovalores triples o de mayor multiplicidad suele dar «indeterminado» (ver Limitaciones) |
| M4-05b | ρ(T) «mediante los procedimientos estudiados en el curso» | Para n ≤ 3 el polinomio coincide con Sarrus; para las raíces y para n > 3 se usan métodos que no se vieron en clase | ídem | `test_faddeev_coincide_con_sarrus_3x3` | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-5) |
| M4-06 | Motivo de finalización | Ocho códigos con mensaje | `ejecutar`, `_ejecutar` | P8–P14, P16 | COMPLETADO |
| M4-07a | Comparar los 3 métodos por iteraciones y error final | Experimento homogéneo; tabla con k, motivo, d, r, e = ‖x⁽ᵏ⁾ − x*‖∞ y ρ | `comparar_metodos`, `configuraciones_homogeneas`, `modulo_iterativos.comparar` | P18, P19, `test_app` | COMPLETADO |
| M4-07b | Significado oficial de «error final» | Se muestran las tres medidas (d, r, e) | ídem | — | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-4). Riesgo bajo: cualquiera de las tres lecturas está en la tabla |
| M4-08 | Gráfica de error frente a iteración | Una ejecución (d_k y r_k con la línea ε) y comparación (d, r o e) | `grafica_convergencia`, `grafica_comparacion` | `test_app`. 02-nov: la gráfica individual (criterios A y B) se revisó como imagen y coincide con IV-1 e IV-4 | COMPLETADO |

## Validaciones obligatorias (OFICIAL p. 3)

| ID | Validación | Archivo o función | Prueba | Estado |
|---|---|---|---|---|
| V-01 | Campos vacíos y no numéricos | `leer_numero`, `leer_matriz` (indica la posición) | `test_validacion`, `test_modulo_I_entrada_invalida` | COMPLETADO |
| V-02 | Dimensiones incompatibles entre A y b | `validar_sistema`, `validar_configuracion` | `test_matriz`, `test_directos`, P20 | COMPLETADO |
| V-03 | Matriz singular o casi singular cuando el método exige que no lo sea | `inversa_gauss_jordan`, `solucion_unica` (`ErrorSistema`), aviso de pivote pequeño, κ alto | `test_directos`, `test_condicion` | COMPLETADO |
| V-04 | Divisiones entre cero y pivotes nulos | Intercambio de filas; `DIAGONAL_CERO` en los iterativos | `test_directos`, P14 | COMPLETADO |
| V-05 | ε > 0 y k_max entero positivo | `leer_tolerancia`, `leer_entero_positivo`, `validar_configuracion` | P20, `test_tolerancias_extremas` | COMPLETADO |
| V-06 | 0 < ω < 2, aclarando que no garantiza la convergencia | `leer_omega`, `validar_configuracion` | P20 | COMPLETADO |
| V-07 | Sin cierres inesperados y con mensajes comprensibles | `ejecutar` nunca lanza excepciones; la interfaz atrapa `ErrorEntrada` y `ErrorMatriz` | `test_app` | COMPLETADO |

## Casos de prueba, manual y entregables (OFICIAL pp. 1, 3, 5)

| ID | Requisito | Implementación | Archivo | Prueba | Estado |
|---|---|---|---|---|---|
| C-07a | Al menos un caso documentado por módulo (entrada, salida esperada, resultado) | Tablas con oráculos independientes | `casos_prueba/modulo_I.md` … `modulo_IV.md` | Las mismas comprobaciones están automatizadas | COMPLETADO |
| C-07b | Superar el caso obligatorio de la docente | Procedimiento preparado | `casos_prueba/README.md` | — | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-3): **no se ha recibido** |
| C-06 | Manual: formato de entradas, pasos de ejecución, un ejemplo por módulo, funciones principales y dependencias | Los cinco apartados existen (§1, §2, §4–7, §8) | `docs/manual_usuario.md` | — | INCOMPLETO: falta que alguien ajeno lo siga en **otro** equipo (lista de verificación, p. 5) |
| E-01 | ZIP `Grupo(01-02)-IF0012-Proyecto-IIC.zip` | `empaquetar.py 01\|02`, una sola carpeta raíz | `dist/` | Verificación del ZIP (estado_desarrollo.md) | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-1): el número 01 es provisional |
| E-02 | Ejecutable o mecanismo de ejecución documentado | `ejecutar.bat` (crea `.venv`, instala y abre el navegador) | `ejecutar.bat`, README, manual §1 | Copia limpia del ZIP en este equipo | COMPLETADO en este equipo. Probarlo en otro equipo forma parte de C-06 |
| E-03/E-04 | Manual e instrucciones de ejecución | — | `docs/manual_usuario.md`, `README.md` | — | COMPLETADO (ver C-06) |
| E-05 | Código fuente completo, legible y comentado | Docstrings con fórmulas y referencias | todo el proyecto | — | COMPLETADO |
| E-08 | Código externo citado | No se copió código externo; el uso de IA está declarado | `docs/herramientas_y_bibliotecas.md` §4 | — | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-2): **autorización del uso de IA** |

## Defensa (35 %)

| ID | Criterio | Implementación | Estado |
|---|---|---|---|
| D-01 a D-05 | Dominio, explicación matemática, uso del programa, claridad y comunicación | Material: `docs/guia_defensa_equipo.md` (guía completa) y `docs/resumen_logica_por_modulo.md` (estudio rápido) | INCOMPLETO: falta que **cada integrante** estudie y ensaye. Defensa en la semana del 16-nov-2026 |

## Incentivos por innovación (OFICIAL p. 5)

**No se afirma ningún punto adicional**: la evaluación corresponde a la docente.

| ID | Incentivo (máx.) | Evidencia | Archivo | Estado |
|---|---|---|---|---|
| I-01 | Visualización avanzada (1 %) | Comparación superpuesta de los 3 métodos (d, r, e); autovalores con el círculo unidad; barrido de ω; CSV del historial con precisión completa | `graficos.py`, `csv_historial` | COMPLETADO (`test_csv_exportado_contiene_historial_completo`) |
| I-02 | Precondicionamiento diagonal (1.5 %) | Se demostró que con M = D Jacobi, GS y SOR no cambian | `guia_matematica.md` §10 | PENDIENTE DE CONFIRMACIÓN EXTERNA (P-8). No implementado |
| I-03 | Matrices dispersas (1 %) | CSR propio con iteraciones idénticas a las densas | `algebra/dispersas.py` | COMPLETADO (`test_dispersas`, `test_modulo_IV_formato_csr`) |
| I-04 | Experiencia de usuario (0.5 %) | Ejemplos cargables, ayudas contextuales, errores con la posición | `interfaz/` | COMPLETADO (juicio de la docente) |
| I-05 | Extensión matemática (1 %) | ρ con autovalores complejos; decisiones exactas (Schur-Cohn, p(±1) = 0); solución paramétrica; determinante | `espectral.py`, `directos.py` | COMPLETADO. Defenderlo exige dominar Faddeev-LeVerrier y Durand-Kerner |

## Limitaciones reales (no son fallos, pero hay que saber defenderlas)

1. **Autovalores múltiples:** Durand-Kerner pierde precisión (≈10⁻⁸ en una raíz doble y ≈10⁻⁵ en una triple).
   - Con raíces dobles suele converger: se avisa y se decide con la banda ampliada de 10⁻⁶.
   - Con raíces triples o de mayor multiplicidad suele no converger: el resultado se marca no fiable y la conclusión es «indeterminado». **Nunca da una conclusión falsa**, pero en esos casos no decide.
2. **ρ muy cerca de 1:** dentro de una banda de 10⁻⁹ (10⁻⁶ si hay raíces casi repetidas) la conclusión es «indeterminado», salvo que una decisión exacta la resuelva.
3. **n > 8:** no se calcula ρ. Se informa y se remite a la dominancia diagonal y a las iteraciones.
4. **Iterativos en punto flotante:** los resultados son aproximaciones. Las diferencias en los últimos decimales se justifican por la tolerancia ε (OFICIAL p. 3), no por redondeos arbitrarios.
5. **Sin pruebas automáticas del contenido visual** de las gráficas. Se revisaron manualmente como imagen.
