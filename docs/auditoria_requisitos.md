# Matriz de cumplimiento — revisión del 03-nov-2026

**Fuente:** `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` (OFICIAL). Se releyeron las pp. 1-5 en texto el 03-nov-2026:

- rúbrica del proyecto: p. 4;
- rúbrica de la defensa: p. 4;
- incentivos y lista de verificación final: p. 5.

**Documentos relacionados:**

- [comparacion_procedimientos.md](comparacion_procedimientos.md): procedimientos de clase frente al código;
- [pendientes_docente.md](pendientes_docente.md): lo que depende de la docente.

> **03-nov-2026, rediseño visual:** la presentación de cada criterio y de los cinco incentivos en la interfaz se documenta en [diseno_visual.md](diseno_visual.md), con capturas. La lógica y los estados de esta matriz no cambiaron.

## Estados

| Estado | Significado |
|---|---|
| **COMPLETADO** | Implementado **en la aplicación** y con evidencia ejecutada (pruebas que pasan; en el núcleo, también oráculos independientes) |
| **INCOMPLETO** | Falta una parte que el grupo **sí** puede hacer |
| **NO IMPLEMENTADO** | No existe en la aplicación |
| **PENDIENTE DE CONFIRMACIÓN** | Depende de un dato o de una respuesta de la docente, o de una confirmación del grupo |
| **NO VERIFICABLE** | Solo lo puede evaluar la docente, por ejemplo la defensa o el puntaje que asigne |

## Evidencia general (03-nov-2026)

| Evidencia | Resultado |
|---|---|
| `.venv\Scripts\python -m unittest` | **204 pruebas, 204 OK** (las 202 del 03-nov más 2 del empaquetado) |
| Auditoría independiente (`auditoria/*.py`) | **0 fallos** en todas: 4500 sistemas; 400 inversas, determinantes y κ; 200 perturbaciones; 300 mínimos cuadrados; 600 ejecuciones iterativas; 300 análisis espectrales; **150 análisis del precondicionador (nuevo)**; los casos difíciles se comportan como se espera |
| Imports de `algebra/` | Solo `fractions`, `math`, `cmath`, `dataclasses` y módulos propios. Ningún `.py` del proyecto importa NumPy, SciPy ni SymPy |

---

## 1. Rúbrica del proyecto (65 %, OFICIAL p. 4)

| Criterio | Puntaje | Qué solicita la profesora («Excelente») | Dónde está implementado | Evidencia | Estado |
|---|---:|---|---|---|---|
| Módulo I: sistemas lineales | 8 % | «Implementación correcta, clasificación de soluciones, validaciones y procedimiento completo» | `algebra/directos.py` (`_escalonar`, `_resolver`, `_rango_aumentada`, `_sustitucion_atras`); `interfaz/modulo_directos.py` | `test_directos` (26); auditoría de 4500 sistemas contra rangos por menores y Cramer; `test_app` con los 3 tipos; pasos visibles | COMPLETADO |
| Módulo II: condicionamiento | 8 % | «κ correcto, perturbación, errores relativos e interpretación coherente» | `algebra/condicion.py` (`numero_condicion_infinito`, `construir_delta_b`, `analizar_perturbacion`, `_interpretar`) | `test_condicion` (13); 400 κ por adjunta; 200 perturbaciones por Cramer; mensajes vistos | COMPLETADO |
| Módulo III: mínimos cuadrados | 8 % | «Ecuaciones normales, residual, error, ajuste y gráfica correctos» | `algebra/minimos.py` (`minimos_cuadrados`, `ajuste_lineal`, `cramer`); `graficos.grafica_ajuste` | `test_minimos`; 300 casos con Aᵀr = 0; verificación de clase (det([A\|b]) y Cramer) idéntica al manuscrito S8-30/09 pp. 6-7 (`test_minimos_como_el_manuscrito`) | COMPLETADO |
| Módulo IV: métodos iterativos | 8 % | «Jacobi, Gauss-Seidel y SOR correctos; convergencia, error y comparación bien presentados» | `algebra/iterativos.py`, `algebra/espectral.py`; 4 pestañas en `interfaz/modulo_iterativos.py` | P1–P21; 600 ejecuciones frente a una implementación independiente; `test_espectral` (25); «error final» igual a la definición de la lámina S9-05/10 p. 17 | COMPLETADO |
| Procedimiento matemático | 7 % | «Desarrollo claro, completo y justificable en los módulos» | Pasos de Gauss; [A\|I] → [I\|A⁻¹]; AᵀA y Aᵀb; det([A\|b]) y Cramer; D, L, U, T, c, polinomio y desarrollo de Sarrus en 3×3; tabla de iteraciones | `test_app` (pasos y verificación de Cramer y Sarrus); [comparacion_procedimientos.md](comparacion_procedimientos.md) | COMPLETADO |
| Análisis e interpretación | 6 % | «Interpreta estabilidad, sensibilidad, residual, error y convergencia correctamente» | Textos automáticos: sensibilidad (`_interpretar`), b ∈ Col(A), residuo, motivos de parada (sin afirmar divergencia), dominancia como condición suficiente, ρ, precondicionador | `test_app`; los textos dependen de los resultados calculados | COMPLETADO (la calidad la juzga la docente) |
| Diseño del código | 5 % | «Código modular, legible, reutilizable y comentado» | 3 capas (`algebra/`, `interfaz/`, `visualizacion/`); un paso por método y un bucle común; `analizar_matriz` reutilizado; docstrings con fórmulas y referencias | `docs/arquitectura.md` | COMPLETADO |
| Validaciones y errores | 4 % | «Validaciones completas y mensajes claros; no se producen cierres inesperados» | `validacion.py`, `matriz.validar_*`, `validar_configuracion`; `ejecutar` nunca lanza excepciones | V-01 a V-07 (abajo); `test_validacion`, P20, `test_tolerancias_extremas`, `test_app` | COMPLETADO |
| Interfaz y usabilidad | 5 % | «Interfaz intuitiva, consistente y resultados fáciles de interpretar» | Ejemplos cargables, ayudas, errores con la posición, colores por tipo de resultado | `test_app` (15 pruebas de funcionamiento); revisión visual parcial | COMPLETADO. Falta una prueba con un usuario ajeno, que es recomendable |
| Manual de usuario | 3 % | «Manual claro, completo, reproducible y coherente con la aplicación» | `docs/manual_usuario.md`: formato de entradas, instalación, un ejemplo por módulo, funciones principales, dependencias. Actualizado el 03-nov con las funciones nuevas | Instalación desde el ZIP en una carpeta limpia; **el equipo confirmó (03-nov) que funciona en otra computadora** siguiendo el manual | COMPLETADO |
| Casos de prueba | 3 % | «Casos documentados y aplicación supera el caso obligatorio» | `casos_prueba/modulo_I..IV.md` (entrada, esperado, obtenido) | Las mismas comprobaciones automatizadas | Casos propios: COMPLETADO. **Caso obligatorio: PENDIENTE DE CONFIRMACIÓN** (no recibido) |

## 2. Rúbrica de la defensa oral (35 %, OFICIAL p. 4)

| Criterio | Puntaje | Qué solicita | Preparación disponible | Estado |
|---|---:|---|---|---|
| Dominio conceptual | 10 % | «Explica con claridad y seguridad los métodos y conceptos» | `guia_defensa_equipo.md` (partes C y D) y su versión HTML | NO VERIFICABLE (depende de cada integrante) |
| Explicación matemática | 10 % | «Justifica correctamente los procedimientos y decisiones numéricas» | Guía D y G; comparacion_procedimientos.md | NO VERIFICABLE |
| Uso del programa | 5 % | «Demuestra la aplicación funcionando y responde a un caso solicitado» | Guion de demostración (guía F) con los resultados esperados | NO VERIFICABLE; requiere instalar en cada computadora |
| Claridad y organización | 5 % | «Exposición ordenada, pertinente y dentro del tiempo» (6-8 min) | Guion por módulo | NO VERIFICABLE |
| Comunicación | 5 % | «Expresión clara, vocabulario matemático adecuado» | Preguntas con respuesta (guía E) | NO VERIFICABLE |

## 3. Incentivos por innovación (hasta 5 % sobre la nota del proyecto, OFICIAL p. 5)

**El puntaje lo asigna la docente.** «Estado» indica si hay una implementación con evidencia, no cuántos puntos se obtendrán.

| Incentivo | Puntaje adicional | Requisito (literal) | Implementación actual | Evidencia | Estado |
|---|---:|---|---|---|---|
| Visualización avanzada | hasta 1 % | «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» | Comparación superpuesta de los 3 métodos (e, d o r); autovalores con el círculo unidad; barrido de ω; **CSV** del historial con precisión completa; gráfica del efecto del precondicionador; planos 2D y 3D del Módulo I | `test_csv_exportado_contiene_historial_completo`, `test_app` | COMPLETADO |
| Precondicionamiento | hasta 1.5 % | «Implementación correcta de un precondicionador diagonal y comparación documentada de su efecto» | `algebra/precondicionamiento.py` y la pestaña «Precondicionamiento diagonal»: M = D, B = D⁻¹A, b̃; κ∞(A) frente a κ∞(B); autovalores de A y de B; Jacobi, GS, SOR y Richardson en ambos sistemas; comparación **exacta** de T y c; conclusiones y gráfica | `TestPrecondicionadorDiagonal` (5) y `TestRichardson` (2) en `test_precondicionamiento.py`; `test_modulo_IV_precondicionamiento`; auditoría de 150 casos aleatorios sin fallos; documentación en guia_matematica §10 y comparacion_procedimientos.md | COMPLETADO (nuevo, 03-nov). La comparación muestra lo que la teoría exige: sin efecto en Jacobi, GS y SOR, y efecto real en κ y en Richardson |
| Matrices dispersas | hasta 1 % | «Representación o tratamiento eficiente de matrices dispersas, con explicación de la estrategia» | CSR propio (`algebra/dispersas.py`); casilla «Usar almacenamiento disperso»; nnz, densidad y memoria | `test_dispersas` (iteraciones idénticas a las densas), `test_modulo_IV_formato_csr`; explicación en guia_matematica §9 | COMPLETADO |
| Experiencia de usuario | hasta 0.5 % | «Mejoras sustantivas de accesibilidad, ayuda contextual o interacción, no solo decoración» | Ejemplos cargables; ayudas contextuales; errores con la celda exacta; resultados persistentes; **sugerencia de reordenamiento para lograr dominancia** (nuevo); interpretación geométrica | `test_app`, `test_modulo_IV_reordenamiento_y_sarrus` | COMPLETADO (el juicio es de la docente) |
| Extensión matemática | hasta 1 % | «Funcionalidad adicional pertinente, correctamente implementada y defendida» | ρ con autovalores complejos para n ≤ 8 (Faddeev-LeVerrier y Durand-Kerner); decisiones exactas (Schur-Cohn, p(±1) = 0); T de SOR; solución paramétrica; determinante; Richardson | `test_espectral` (25); 300 análisis espectrales aleatorios contra Leibniz y Gelfand | COMPLETADO. Defenderlo exige dominar los dos algoritmos (guía, D.5) |

**Total implementado:** los 5 incentivos, que suman un máximo posible de **5 %**. Los puntos que se otorguen: NO VERIFICABLE.

## 4. Requisitos detallados del enunciado (OFICIAL pp. 1-3)

### Restricciones generales

| ID | Requisito | Dónde | Evidencia | Estado |
|---|---|---|---|---|
| R-01 | Una sola aplicación con los 4 módulos | `app.py` (`PAGINAS`) | `test_app` | COMPLETADO |
| R-02 | Algoritmos centrales desde cero | `algebra/` | Revisión de imports; auditoría | COMPLETADO |
| R-03 | Documentar las bibliotecas de interfaz y gráficas | `docs/herramientas_y_bibliotecas.md`, `requirements.txt` | — | COMPLETADO |
| R-04 | Todas las entradas con validación | `validacion.py`, `validar_configuracion`, `precondicionar_diagonal` | Pruebas V-01 a V-07 | COMPLETADO |
| R-05 | Código externo citado | No se copió código externo. El uso de IA está declarado en `herramientas_y_bibliotecas.md` §4 | — | COMPLETADO: uso de IA **declarado**. Ningún documento exige autorización previa (P-2) |

### Módulo I

| ID | Requisito | Dónde | Evidencia | Estado |
|---|---|---|---|---|
| M1-01 | Entrada Ax = b | `modulo_directos`, `leer_matriz` | `test_validacion`, `test_app` | COMPLETADO |
| M1-02 | Gauss o Gauss-Jordan desde cero | `_escalonar` | 4500 casos | COMPLETADO |
| M1-03 | Paso a paso | `Paso`, `mostrar_pasos` | `test_pasos_registrados` | COMPLETADO |
| M1-04 | Clasificación automática | `_resolver` | Rangos por menores | COMPLETADO |
| M1-05 | Dimensiones y pivotes nulos o problemáticos | `validar_sistema`, `_buscar_pivote`, `UMBRAL_PIVOTE_PEQUENO` | `test_directos` | COMPLETADO |

### Módulo II

| ID | Requisito | Dónde | Evidencia | Estado |
|---|---|---|---|---|
| M2-01 | κ∞ con inversa propia | `numero_condicion_infinito` | 400 casos por adjunta | COMPLETADO |
| M2-02 | Valor e interpretación (escala 10/100) | `clasificar_kappa` | `test_umbrales` | COMPLETADO |
| M2-03 | Perturbación absoluta o porcentual | `construir_delta_b` | `test_condicion` | COMPLETADO (interpretación porcentual documentada, P-7) |
| M2-04 | Comparar las soluciones original y perturbada | `analizar_perturbacion` | 200 casos por Cramer | COMPLETADO |
| M2-05 | Errores relativos con denominador ≠ 0 | ídem | `test_denominador_cero` | COMPLETADO |
| M2-06 | Explicación de la sensibilidad | `_interpretar` | `test_app` | COMPLETADO |

### Módulo III

| ID | Requisito | Dónde | Evidencia | Estado |
|---|---|---|---|---|
| M3-01 | Detectar sobredeterminado | `clasificar_forma` | `test_minimos` | COMPLETADO |
| M3-02 | AᵀAx = Aᵀb | `minimos_cuadrados` | 300 casos | COMPLETADO |
| M3-03 | Resolver con el método directo propio | `resolver_gauss` | `test_minimos` | COMPLETADO |
| M3-04 | r y ‖r‖₂ | ídem | Aᵀr = 0 exacto | COMPLETADO |
| M3-05 | Ajuste lineal y ecuación | `ajuste_lineal` | Fórmula cerrada | COMPLETADO |
| M3-06 | Gráfica de datos y recta | `grafica_ajuste` | `test_app`; vista el 27-oct | COMPLETADO |

### Módulo IV

| ID | Requisito | Dónde | Evidencia | Estado |
|---|---|---|---|---|
| M4-01 | Jacobi, GS y SOR desde cero | `paso_*`, `_ejecutar` | P1–P21; 600 casos | COMPLETADO |
| M4-02 | x⁽⁰⁾, ε, k_max y ω validado | `validar_configuracion` | P20 | COMPLETADO |
| M4-03 | Tabla con k, x⁽ᵏ⁾ y el error del criterio | `filas_tabla` | `test_app` | COMPLETADO |
| M4-04 | Dominancia diagonal | `dominancia_diagonal`, `reordenamiento_dominante` | `TestDominancia`, `TestReordenamientoDominante` | COMPLETADO |
| M4-05 | T y ρ(T) sin bibliotecas | `matriz_iteracion`, `analizar_matriz`, `desarrollo_sarrus` | `test_espectral`; 300 casos | COMPLETADO para n ≤ 8. **Alcance de los métodos que no se vieron en clase: PENDIENTE DE CONFIRMACIÓN (P-5)** |
| M4-06 | Motivo de finalización | Códigos de `ejecutar` | P8–P16 | COMPLETADO |
| M4-07 | Comparación por iteraciones y error final | `comparar_metodos` (e = ‖x⁽ᵏ⁾ − x*‖∞) | P18, P19; coincide con la definición de la lámina S9-05/10 p. 17 | COMPLETADO (**P-4 resuelto por la lámina**) |
| M4-08 | Gráfica de error frente a iteración | `grafica_convergencia`, `grafica_comparacion` | `test_app`; gráfica individual revisada como imagen el 02-nov | COMPLETADO |

### Validaciones obligatorias (OFICIAL p. 3)

| ID | Validación | Dónde | Prueba | Estado |
|---|---|---|---|---|
| V-01 | Campos vacíos y no numéricos | `leer_numero`, `leer_matriz` | `test_validacion`, `test_modulo_I_entrada_invalida` | COMPLETADO |
| V-02 | Dimensiones incompatibles | `validar_sistema`, `validar_configuracion` | `test_matriz`, P20 | COMPLETADO |
| V-03 | Matriz singular o casi singular | `inversa_gauss_jordan`, `solucion_unica`, aviso de pivote pequeño | `test_directos`, `test_modulo_II_singular` | COMPLETADO |
| V-04 | Divisiones entre cero y pivotes nulos | Intercambio de filas; `DIAGONAL_CERO`; `precondicionar_diagonal` | P14, `test_diagonal_cero` | COMPLETADO |
| V-05 | ε > 0 y k_max entero positivo | `leer_tolerancia`, `leer_entero_positivo` | P20, `test_tolerancias_extremas` | COMPLETADO |
| V-06 | 0 < ω < 2 con aviso | `leer_omega` | P20 | COMPLETADO |
| V-07 | Sin cierres y con mensajes comprensibles | `ejecutar`; la interfaz atrapa los errores | `test_app` | COMPLETADO |

### Entregables (OFICIAL p. 1)

| ID | Entregable | Dónde | Estado |
|---|---|---|---|
| E-01 | ZIP `Grupo(01-02)-IF0012-Proyecto-IIC.zip` | `empaquetar.py`, `dist/` | COMPLETADO: grupo 01, confirmado por el equipo el 03-nov-2026 (`Grupo01-IF0012-Proyecto-IIC.zip`) |
| E-02 | Mecanismo de ejecución | `ejecutar.bat` | COMPLETADO (probado desde una copia limpia del ZIP en este equipo) |
| E-03/E-04 | Manual e instrucciones | `docs/manual_usuario.md`, `README.md` | COMPLETADO (probado en otra computadora, confirmado por el equipo) |
| E-05 | Código fuente comentado | Todo el proyecto | COMPLETADO |
| E-06 | Carpeta de casos de prueba con los obligatorios | `casos_prueba/` | PENDIENTE DE CONFIRMACIÓN (caso obligatorio, P-3) |

## 5. Lista de verificación final (OFICIAL p. 5)

| Punto | Estado |
|---|---|
| Integra los cuatro módulos en una sola solución | COMPLETADO |
| Todos los algoritmos obligatorios implementados desde cero | COMPLETADO |
| Los procedimientos matemáticos pueden visualizarse o verificarse | COMPLETADO |
| Las entradas inválidas generan mensajes claros y no cierran la aplicación | COMPLETADO |
| Hay casos de prueba y se verificó el caso obligatorio | Casos: COMPLETADO. Caso obligatorio: PENDIENTE DE CONFIRMACIÓN |
| El manual permite instalar, ejecutar y usar el programa sin ayuda del equipo | COMPLETADO (confirmado por el equipo en otra computadora, 03-nov) |
| El ZIP tiene el nombre solicitado y todos los elementos | COMPLETADO (grupo 01 confirmado; contenido verificado). El caso obligatorio se añadirá cuando llegue |
| Cada integrante está preparado para defender el trabajo | NO VERIFICABLE (material listo: guía, HTML y resumen) |

## Limitaciones reales (no son fallos, pero hay que saber defenderlas)

1. **Autovalores múltiples:** con raíces dobles se avisa y se decide con la banda de 10⁻⁶; con raíces triples o de mayor multiplicidad suele quedar «indeterminado». **Nunca da una conclusión falsa.**
2. **ρ muy cerca de 1:** el resultado es «indeterminado» dentro de la banda, salvo que haya una decisión exacta.
3. **n > 8:** no se calcula ρ.
4. **Iterativos en punto flotante:** las diferencias se justifican por ε (OFICIAL p. 3).
5. **Precondicionador M = D:** no acelera Jacobi, GS ni SOR. Es un hecho matemático demostrado y verificado, no una limitación de la implementación, y contradice la tabla de la lámina S9-05/10 p. 23.
6. **Gráficas:** no hay pruebas automáticas de su contenido visual.
