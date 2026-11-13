# Matriz de trazabilidad: enunciado, rúbrica e incentivos

Fuente oficial: `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` («OFICIAL»), 5 páginas.
Estado de la evidencia: **Demostrado** = existe prueba automatizada o auditoría que se ejecutó;
**Implementado** = existe en el código y en la interfaz, sin prueba específica citada;
**Pendiente** = depende de la docente o de una prueba física del equipo.

Categorías de procedencia: **A** visto en clase · **B** exigido por el enunciado ·
**C** extensión o incentivo no visto en clase · **D** sin respaldo suficiente.

## 1. Requisitos obligatorios (OFICIAL pp. 2-3)

| Requisito | Fuente | Cat. | Implementación | Archivo y función | Prueba o evidencia | Estado |
|---|---|---|---|---|---|---|
| M-I: ingreso Ax = b | OFICIAL p. 2 | B | Editor de matriz y vector | `interfaz/compartido/editor.py`; `algebra/modulo_I_sistemas/directos.py` | `tests/modulo_I/test_directos.py`; `tests/interfaz/test_editor.py` | Demostrado |
| M-I: Gauss o Gauss-Jordan, paso a paso | OFICIAL p. 2 | A/B | `_escalonar`, `resolver_gauss`, `resolver_gauss_jordan` | `directos.py` | `test_directos.py`; auditoría `auditoria_directos.py` (4500 sistemas, 0 fallos) | Demostrado |
| M-I: clasificación única, infinitas, inconsistente | OFICIAL p. 2 | A/B | `_rango_aumentada`, `clasificar` | `directos.py` | `test_directos.py` | Demostrado |
| M-I: validaciones y pivotes nulos o problemáticos | OFICIAL p. 2 | B | `_buscar_pivote`, avisos de pivote | `directos.py`, `validacion.py` | `tests/compartido/test_validacion.py` | Demostrado |
| M-II: κ∞ = ‖A‖∞ ‖A⁻¹‖∞ con inversa propia | OFICIAL p. 2 | A/B | `numero_condicion_infinito`; inversa por Gauss-Jordan | `algebra/modulo_II_condicionamiento/condicion.py`; `directos.py::inversa_gauss_jordan` | `tests/modulo_II/test_condicion.py`; `auditoria_directos.py` (400 casos) | Demostrado |
| M-II: escala 10 / 100 | OFICIAL p. 2 | B | `clasificar_kappa` | `condicion.py` | `test_condicion.py` | Demostrado |
| M-II: perturbación en b (valor absoluto o porcentaje) | OFICIAL p. 2 | B | `construir_delta_b`, `analizar_perturbacion` | `condicion.py` | `test_condicion.py`; auditoría 200 perturbaciones | Demostrado |
| M-II: reportar ‖Δx‖/‖x‖ y ‖Δb‖/‖b‖ | OFICIAL p. 2 | B | `analizar_perturbacion` | `condicion.py` | `test_condicion.py` | Demostrado |
| M-III: detectar sobredeterminado | OFICIAL p. 2 | B | `clasificar_forma` | `algebra/modulo_III_minimos/minimos.py` | `tests/modulo_III/test_minimos.py` | Demostrado |
| M-III: ecuaciones normales AᵀAx = Aᵀb | OFICIAL p. 2 | A/B | `minimos_cuadrados` | `minimos.py` | `test_minimos.py`; auditoría 300 casos | Demostrado |
| M-III: resolver con método directo implementado | OFICIAL p. 2 | B | Gauss (`solucion_unica`) y Cramer como verificación | `minimos.py`, `cramer` | `test_minimos.py` | Demostrado |
| M-III: residual r = b − Ax y medida de error | OFICIAL p. 2 | B | `ajuste_lineal`, `residuo` | `minimos.py` | `test_minimos.py` | Demostrado |
| M-III: ajuste lineal y ecuación de la recta | OFICIAL p. 2 | B | `ajuste_lineal` | `minimos.py` | `test_minimos.py` | Demostrado |
| **M-III: gráfica con datos y recta** | OFICIAL p. 2 | B | `visualizacion/interactivas.py::ajuste`; pestaña «Ajuste» | `interactivas.py`; `interfaz/modulos/modulo_III_minimos.py` | `tests/interfaz/test_graficas_interactivas.py` | Demostrado |
| M-IV: Jacobi, Gauss-Seidel, SOR | OFICIAL p. 2 | A/B | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor` | `algebra/modulo_IV_iterativos/metodos.py` | `tests/modulo_IV/test_iterativos.py`; auditoría 600 iteraciones | Demostrado |
| M-IV: x⁽⁰⁾, tolerancia, k_max configurables; ω validado | OFICIAL p. 2-3 | B | `validar_configuracion` | `ejecucion.py` | `test_iterativos.py` (validación) | Demostrado |
| M-IV: tabla k, x, error de parada | OFICIAL p. 2 | B | `filas_tabla`; `FilaIteracion` | `interfaz/modulos/modulo_IV_iterativos/pestana_ejecutar.py`; `ejecucion.py` | `tests/interfaz/test_app.py` | Demostrado |
| M-IV: dominancia diagonal | OFICIAL p. 2 | A/B | `dominancia_diagonal` | `algebra/modulo_IV_iterativos/convergencia.py` | `test_iterativos.py` | Demostrado |
| M-IV: matriz de iteración y radio espectral | OFICIAL p. 2 | A/B | `matriz_iteracion`, `radio_espectral` | `matriz_iteracion.py`, `espectral.py` | `test_espectral.py`; auditoría 300 espectrales | Demostrado |
| M-IV: motivo de finalización | OFICIAL p. 2 | B | Códigos de terminación | `ejecucion.py` | `test_iterativos.py` | Demostrado |
| M-IV: comparar Jacobi, GS, SOR | OFICIAL p. 2 | B | `comparar_metodos` y pestaña «Comparar» | `comparacion.py`; `pestana_comparar.py` | `tests/interfaz/test_graficas_exploracion.py` | Demostrado |
| **M-IV: gráfica error vs. iteración** | OFICIAL p. 2 | B | `interactivas.convergencia` y `interactivas.comparacion` | `visualizacion/interactivas.py` | `tests/interfaz/test_graficas_interactivas.py` | Demostrado |
| Validaciones: vacíos, formatos, dimensiones, singularidad, división por cero, tolerancia > 0, k_max entero > 0, 0 < ω < 2 | OFICIAL p. 3 | B | `validar_configuracion`, `analizar`, editor | `ejecucion.py`; `interfaz/compartido/editor.py` | `test_iterativos.py`; `test_editor.py` | Demostrado |
| Casos de prueba documentados por módulo | OFICIAL p. 3 | B | `casos_prueba/modulo_I.md` … `modulo_IV.md` | `casos_prueba/` | Revisión documental | Implementado |
| Caso obligatorio de validación de la docente | OFICIAL p. 3 | B | Estructura lista en `casos_prueba/` (sin contenido) | — | — | **Pendiente**: no ha llegado el caso |
| Manual de usuario | OFICIAL p. 3 | B | `docs/manual_usuario.md` | — | Revisión documental | Implementado |
| Instrucciones de ejecución y dependencias | OFICIAL p. 1 | B | `README.md`, `requirements*.txt`, `ejecutar.bat` | — | Instalación limpia (ver `docs/instalacion_limpia.md`) | Implementado |
| Declaración de herramientas de IA | Programa §6.2 | — | `docs/herramientas_y_bibliotecas.md` §4 | — | — | Implementado; **Pendiente** de confirmación de la docente |
| Interfaz intuitiva y resultados interpretables | OFICIAL p. 3 | B | Navegación superior, interpretación en cada módulo | `interfaz/`, `visualizacion/` | `tests/interfaz/` | Implementado |

**Gráficas exigidas (solo estas dos):** M-III (datos y recta) y M-IV (error frente a iteración). Módulos I y II no exigen gráfica; no se añadieron gráficas decorativas a esos módulos.

## 2. Incentivos (OFICIAL p. 5, hasta 5 % adicional)

El puntaje lo decide la docente. Esta tabla solo indica lo implementado y cómo se demuestra.

| Incentivo | Máximo | Implementación | Archivo y función | Cómo se demuestra | Estado |
|---|---|---|---|---|---|
| Visualización avanzada: gráficas comparativas adicionales, historial de convergencia o reportes exportables | 1 % | Comparación superpuesta (e_k, d_k o r_k); historial explorable (clic y deslizador); tabla y CSV con precisión completa; autovalores con círculo unidad | `interactivas.comparacion`, `interactivas.autovalores`, `pestana_ejecutar.py::csv_historial`, `explorar_convergencia` | `tests/interfaz/test_graficas_exploracion.py`; `test_graficas_interactivas.py`; botón «Descargar CSV» | Implementado y probado en interfaz |
| Precondicionamiento: precondicionador diagonal y comparación documentada de su efecto | 1,5 % | M = D; B = D⁻¹A; κ(A) frente a κ(B); T y c **idénticas** en Jacobi, GS y SOR (demostrado); Richardson con ρ 4,618 → 0,405 | `algebra/modulo_IV_iterativos/precondicionamiento.py::precondicionar_diagonal`, `analizar_precondicionador` | `tests/modulo_IV/test_precondicionamiento.py`; `auditoria_precondicionamiento.py` (150 casos, 0 fallos) | Demostrado |
| Matrices dispersas: tratamiento eficiente con explicación de la estrategia | 1 % | CSR propio (valores, columnas, inicio); pasos Jacobi, GS, SOR y Richardson sobre CSR; mismas iteraciones que el formato denso | `algebra/modulo_IV_iterativos/dispersas.py::MatrizCSR`, `a_csr`, `paso_*_csr` | `tests/modulo_IV/test_dispersas.py`; formato CSR en `ejecutar` | Demostrado |
| Experiencia de usuario: accesibilidad, ayuda contextual o interacción (no decoración) | 0,5 % | Editor de rejilla con validación previa; distintivos de procedencia A/B/C/D; avisos de «Extensión no vista en clase»; control gestual 3D y 2D; ayuda contextual en cada pestaña | `interfaz/compartido/editor.py`, `estilo.py::procedencia`, `control_gestual.py`, `gestos/vista2d.py` | `tests/interfaz/test_editor.py`; `tests/interfaz/test_control_gestual.py`; `tests/gestos/test_vista2d.py` | Implementado; el gesto 2D **no está validado con mano real** |
| Extensión matemática pertinente, implementada y defendida | 1 % | ρ(T) con autovalores complejos (n ≤ 8): Faddeev-LeVerrier y Durand-Kerner; decisiones exactas (λ = ±1); matriz de iteración de SOR; Richardson | `algebra/modulo_IV_iterativos/polinomio_raices.py`, `espectral.py::concluir`, `matriz_iteracion.py` | `tests/modulo_IV/test_espectral.py`; `auditoria_iterativos.py` (300 espectrales, 0 fallos); `auditoria/casos_dificiles.py` | Demostrado; **Cat. C** |

**Limitaciones que deben decirse en la defensa:** Durand-Kerner no garantiza convergencia global
(Ax avisa cuando no alcanza la precisión); ρ se declara «no fiable» con raíces casi repetidas
(`casos_dificiles.py`).

## 3. Correcciones matemáticas y procedencia (diapositivas frente a Ax)

| Documento y página | Diferencia | Comprobación | Tratamiento en Ax |
|---|---|---|---|
| S9-07/10 p. 4 | Sale ρ(T_J) = 0 | Polinomio correcto −λ³ − (4/9)λ + 4/3; ρ ≈ 1,174 > 1: no converge | Ax muestra 1,174 y explica la omisión del término 4/3 |
| S9-05/10 p. 23 | «Jacobi con M = D converge más rápido» | Con M = D, D⁻¹A tiene diagonal 1 y T_J es la misma: iteraciones idénticas | Ax documenta que no acelera Jacobi; el efecto aparece en κ y en Richardson |
| S8-30/09 pp. 32-33 | SOR presentado por componentes | La forma matricial T_ω = (D + ωL)⁻¹[(1 − ω)D − ωU] no aparece en las láminas | Ax la calcula y la rotula Cat. C |
| S8-28/09 p. 6 | Criterio con norma relativa ‖x⁽ᵏ⁺¹⁾ − x⁽ᵏ⁾‖/‖x⁽ᵏ⁾‖ | Medido: Jacobi k = 7 (absoluta) frente a k = 8 (relativa) en la tridiagonal de la guía | Ax usa la absoluta; la interfaz lo indica (ver `docs/auditoria_procedimientos_pdf.md` §2.2) |
| Richardson, Faddeev-LeVerrier, Durand-Kerner | No aparecen en ninguna lámina (OCR de las 15 láminas: 0 coincidencias) | Búsqueda sobre el texto de las 457 páginas | **Cat. C**, rotulados como extensiones en la interfaz |
| Erratas S2-19/08, S3-26/08, S6-14/09, S7-21/09, S8-30/09 p. 20, S9-07/10 p. 7 | Varias (ver `docs/referencia_oficial_procedimientos.md`) | Recalculadas | Ax muestra el valor correcto |

## 4. Estado global

- Requisitos obligatorios: **implementados y demostrados** salvo el caso de validación de la docente (pendiente externo).
- Incentivos: **implementados**; el puntaje lo decide la docente. Ninguno está marcado como garantizado.
- Gráficas: exactamente las exigidas (M-III y M-IV).
- Pendientes externos: caso obligatorio de validación (P-3); confirmación sobre el uso de IA (P-2, programa §6.2).
