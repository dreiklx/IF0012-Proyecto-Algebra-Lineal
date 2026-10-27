# Matriz de cumplimiento (rúbrica oficial) — revisión tras la auditoría final

- **Fuente:** `INTRUCCIONES-PROYECTO FINAL-ÁLGEBRA LINEAL-IIC2026.pdf` (OFICIAL). Los identificadores son los de la auditoría documental.
- **Fecha:** 27-oct-2026.

## Qué significa cada estado

| Estado | Significado |
|---|---|
| **Implementado** | Existe el código o el documento. No implica que esté probado |
| **Probado** | Hay pruebas automáticas que se ejecutaron y pasan |
| **Verificado** | Probado, y además el resultado se contrastó con oráculos independientes: la auditoría aleatoria de `auditoria/` y/o valores calculados a mano. En la interfaz, se revisó también visualmente |
| **Pendiente de revisión manual** | Necesita que una persona lo mire o lo use |
| **Bloqueado** | Depende de algo externo al código |

## Tipos de evidencia

| Evidencia | Qué es | Resultado (27-oct-2026) |
|---|---|---|
| **A. Pruebas automáticas** | `python -m unittest`: 184 pruebas en `tests/` (ver el desglose en estado_desarrollo.md) | 184 ejecutadas, 184 OK, 0 fallos, 0 omitidas |
| **B. Auditoría independiente** | `auditoria/*.py`. Compara el núcleo con oráculos escritos aparte: Leibniz, adjunta, Cramer, una implementación separada de las iteraciones y la fórmula de Gelfand ‖Tᵏ‖^(1/k) | 4500 sistemas, 400 inversas, 200 perturbaciones, 300 mínimos cuadrados, 600 ejecuciones iterativas y 300 análisis espectrales: **0 fallos** |
| **C. Revisión visual manual** | Capturas de Chrome sobre la aplicación real, o figuras guardadas como imagen | Ver la columna «Evidencia» de cada fila. Varias capturas fallaron por un problema de la herramienta (página en redibujado) y esas secciones **no** se dan por vistas |

## Requisitos generales

| ID | Requisito (pág.) | Archivo | Evidencia | Prueba | Estado | Pendiente |
|---|---|---|---|---|---|---|
| R-01 | Una sola aplicación con los 4 módulos (p. 2, 5) | `app.py` | A; C: los 4 módulos se abrieron desde la barra lateral en Chrome | test_app (navegación) | **Verificado** | — |
| R-02 | Algoritmos centrales desde cero (p. 1, 5) | `algebra/` | Los imports de `algebra/` son solo `fractions`, `math`, `cmath`, `dataclasses` y módulos propios | revisión de imports | **Verificado** | Confirmar con la docente que `math.sqrt` y `cmath.sqrt` cuentan como operaciones elementales |
| R-03 | Documentar las bibliotecas de interfaz y gráficas (p. 1) | `docs/herramientas_y_bibliotecas.md` | Documento | — | Implementado | NumPy entra como dependencia transitiva de Streamlit y Matplotlib: confirmar con la docente |

## Módulo I — Sistemas lineales (8 %)

| ID | Requisito | Archivo | Evidencia | Prueba | Estado | Pendiente |
|---|---|---|---|---|---|---|
| M1-01 | Entrada Ax = b | `modulo_directos.py`, `validacion.py` | A; C (texto editable, revisión de la fase VII) | test_validacion, test_app | **Verificado** | — |
| M1-02 | Gauss / Gauss-Jordan desde cero | `directos.py` | A; B (4500 casos, 3 variantes) | test_directos | **Verificado** | — |
| M1-03 | Procedimiento paso a paso | `directos.py` (`Paso`) | A; C (pasos vistos en Chrome) | test_pasos_registrados | **Verificado** | — |
| M1-04 | Clasificación única / infinitas / inconsistente | `directos.py` | B: rangos por menores (Leibniz) en 4500 casos | test_directos, test_app | **Verificado** | — |
| M1-05 | Dimensiones y pivotes nulos o problemáticos | `matriz.py`, `directos.py` | A | test_directos | Probado | El umbral de pivote pequeño (10⁻¹⁰) es técnico |
| — | Interpretación geométrica (extra) | `geometria_3d.py` | C: figuras de solución única e infinitas guardadas como PNG y revisadas (correctas) | test_app (genera la figura) | Probado | **Pendiente de revisión manual dentro del navegador**: la captura falló |

## Módulo II — Condicionamiento (8 %)

| ID | Requisito | Archivo | Evidencia | Prueba | Estado | Pendiente |
|---|---|---|---|---|---|---|
| M2-01 | κ∞ con inversa propia | `condicion.py`, `directos.py` | B: inversa por adjunta y κ en 400 casos | test_condicion | **Verificado** | — |
| M2-02 | Interpretación con la escala 10/100 | `condicion.py` | A (límites exactos 10 y 100); C (mensaje visto) | test_umbrales | **Verificado** | — |
| M2-03 | Perturbación absoluta o porcentual | `condicion.py`, `modulo_condicionamiento.py` | A | test_condicion | Probado | El porcentaje se interpreta como Δbᵢ = p/100·bᵢ (una componente bᵢ = 0 no se perturba). **Confirmar la interpretación** |
| M2-04 | Comparar las soluciones original y perturbada | `condicion.py` | B: x̃ por Cramer en 200 casos; C: tabla vista en Chrome | test_condicion | **Verificado** | — |
| M2-05 | ‖Δb‖/‖b‖ y ‖Δx‖/‖x‖ con denominador ≠ 0 | `condicion.py` | B; A (denominador cero) | test_denominador_cero | **Verificado** | — |
| M2-06 | Explicación de la sensibilidad | `condicion.py` | C: el texto distingue el error observado de la cota teórica | test_app | **Verificado** | — |

## Módulo III — Mínimos cuadrados (8 %)

| ID | Requisito | Archivo | Evidencia | Prueba | Estado | Pendiente |
|---|---|---|---|---|---|---|
| M3-01 | Detectar un sistema sobredeterminado | `minimos.py` | A; C (mensaje visto) | test_minimos | **Verificado** | — |
| M3-02 | AᵀA x = Aᵀb | `minimos.py` | B: 300 casos por Cramer; C (matrices vistas) | test_minimos | **Verificado** | — |
| M3-03 | Resolver con el método directo propio | `minimos.py` → `resolver_gauss` | Código; B | test_minimos | **Verificado** | — |
| M3-04 | r = b − Ax̂ y ‖r‖₂ | `minimos.py` | B: Aᵀr = 0 exacto en todos los casos; C (tabla de residuos vista) | test_minimos | **Verificado** | — |
| M3-05 | Ajuste lineal y ecuación de la recta | `minimos.py` | A (fórmula cerrada); C («y = 3/4 x + 6/5» visto) | test_minimos, test_app | **Verificado** | — |
| M3-06 | Gráfica de datos y recta | `graficos.py` | C: gráfica vista en Chrome, con puntos, recta y residuos | test_app (genera la figura) | **Verificado** | — |
| — | AᵀA singular / ajuste imposible | `minimos.py` | A | test_columnas_dependientes, test_datos_invalidos | Probado | — |

## Módulo IV — Métodos iterativos (8 %)

| ID | Requisito | Archivo | Evidencia | Prueba | Estado | Pendiente |
|---|---|---|---|---|---|---|
| M4-01 | Jacobi, GS y SOR desde cero | `iterativos.py` | B: 600 ejecuciones aleatorias idénticas a la implementación independiente (k final y x) | test_iterativos (P1–P21) | **Verificado** | — |
| M4-02 | x⁽⁰⁾, ε, k_max y ω validados | `iterativos.py`, `validacion.py` | A, incluidos ε que se anulan en float y ε enormes | P20, test_tolerancias_extremas | Probado | — |
| M4-03 | Tabla k, x⁽ᵏ⁾ y error de parada | `modulo_iterativos.py` | C: tabla con la columna «(criterio de parada)» vista; A | test_app | **Verificado** | — |
| M4-04 | Dominancia diagonal | `iterativos.py` | A; C (tabla vista) | TestDominancia | **Verificado** | — |
| M4-05 | Matriz de iteración y ρ(T) sin bibliotecas | `espectral.py` | B: 300 casos (Leibniz, producto = det, Gelfand); casos difíciles; C (pestaña vista; polinomio comprobado a mano) | test_espectral (24) | **Verificado, con limitación** | Con autovalores **múltiples** la conclusión es «indeterminado» (ver Limitaciones). **Alcance pendiente de confirmar** con la docente |
| M4-06 | Motivo de finalización | `iterativos.py` | A; C | P8–P14, P16 | **Verificado** | — |
| M4-07 | Comparación por iteraciones y error final | `iterativos.py` | C: tabla homogénea con d, r, e y ρ vista; ρ contrastado con Gelfand | P18, P19 | **Verificado** | **«Error final» oficial pendiente de confirmar**: se muestran d, r y e |
| M4-08 | Gráfica de error frente a iteración | `graficos.py` | C: gráfica comparativa vista (parte superior) | test_app | Probado | **La gráfica de una sola ejecución no se capturó** en el navegador |

## Criterios transversales

| ID | Criterio (peso) | Evidencia | Estado | Pendiente |
|---|---|---|---|---|
| C-01 | Procedimiento matemático visible (7 %) | C: pasos de Gauss, ecuaciones normales, D/L/U/T/polinomio | **Verificado** | — |
| C-02 | Análisis e interpretación (6 %) | C: textos de los módulos II, III y IV | Implementado | La calidad la juzga la docente |
| C-03 | Código modular y comentado (5 %) | `docs/arquitectura.md` | Implementado | — |
| C-04 | Validaciones sin cierres inesperados (4 %) | A: entradas inválidas en el núcleo y en la interfaz; `ejecutar` nunca lanza excepciones | Probado | — |
| C-05 | Interfaz intuitiva (5 %) | C: revisión parcial; se corrigió el espaciado de fracciones apiladas | **Pendiente de revisión manual** | La corrección del espaciado no se confirmó visualmente (la captura falló); falta que lo pruebe un usuario |
| C-06 | Manual de usuario (3 %) | `docs/manual_usuario.md` | Implementado | **Pendiente**: que una persona ajena siga el manual en otro equipo |
| C-07 | Casos de prueba y caso obligatorio (3 %) | `casos_prueba/` | **Bloqueado (parcial)** | El caso obligatorio de la docente no se ha recibido |

## Validaciones obligatorias (OFICIAL p. 3)

| ID | Validación | Prueba | Estado |
|---|---|---|---|
| V-01 | Campos vacíos o no numéricos | test_validacion, test_app (celda (2, 2)) | **Verificado** (mensaje visto) |
| V-02 | Dimensiones incompatibles | test_matriz, test_directos, P20 | Probado |
| V-03 | Matriz singular o casi singular | test_directos, test_condicion; aviso de pivote pequeño y de κ alto | Probado |
| V-04 | Divisiones entre cero y pivotes nulos | test_directos, P14 | Probado |
| V-05 | ε > 0 y k_max entero positivo | P20, test_tolerancias_extremas | Probado |
| V-06 | 0 < ω < 2 con aviso | P20 | Probado |
| V-07 | Sin cierres; mensajes comprensibles | test_app; `ejecutar` devuelve códigos | Probado |

## Entregables (OFICIAL p. 1)

| ID | Entregable | Estado | Pendiente |
|---|---|---|---|
| E-01 | ZIP `Grupo(01-02)-IF0012-Proyecto-IIC.zip` | Implementado (`empaquetar.py 01|02`) | **Número de grupo sin confirmar** |
| E-02 | Mecanismo de ejecución | Probado (`ejecutar.bat` en una copia limpia) | No se probó en otro equipo |
| E-03 | Manual de usuario | Implementado | Prueba con un tercero |
| E-04 | Instrucciones de ejecución | Implementado (README y manual §1) | — |
| E-05 | Código fuente comentado | Implementado | — |
| E-06 | Carpeta de casos de prueba | Implementado | Falta el caso obligatorio |
| E-07 | Bibliotecas documentadas | Implementado | — |
| E-08 | Código externo citado | No aplicable: no se copió código externo | El uso de IA está declarado; **la autorización está pendiente** |

## Defensa (35 %)

| ID | Criterio | Estado |
|---|---|---|
| D-01 a D-05 | Dominio, explicación, uso, claridad, comunicación | **No iniciado**: preparación del grupo (Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez) con `docs/guia_defensa.md`. Defensa en la semana del 16-nov-2026 |

## Incentivos por innovación (OFICIAL p. 5)

**No se afirma ningún punto adicional:** la evaluación corresponde a la docente. Se indica la evidencia concreta que existe.

| ID | Incentivo (máx.) | Criterio oficial | Evidencia concreta | Estado |
|---|---|---|---|---|
| I-01 | Visualización avanzada (1 %) | «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» | Comparación superpuesta de los 3 métodos (vista); autovalores con el círculo unidad; barrido de ω; **CSV del historial con precisión completa** (contenido probado) | Probado; parcialmente visto |
| I-02 | Precondicionamiento (1.5 %) | «Implementación correcta de un precondicionador diagonal y comparación documentada de su efecto» | Demostración de que con M = D, Jacobi, GS y SOR no cambian (guia_matematica §10) | **Bloqueado**: falta la aclaración de la docente. No implementado |
| I-03 | Matrices dispersas (1 %) | «Representación o tratamiento eficiente… con explicación de la estrategia» | CSR propio; iteraciones idénticas a las densas (prueba); paso unas 52 veces más rápido en una tridiagonal de 400×400 (medido); explicación en guia_matematica §9 | Probado |
| I-04 | Experiencia de usuario (0.5 %) | «Mejoras sustantivas de accesibilidad, ayuda contextual o interacción» | Ejemplos cargables, ayudas, errores con la posición, interpretación geométrica | Implementado; pendiente de revisión manual |
| I-05 | Extensión matemática (1 %) | «Funcionalidad adicional pertinente, correctamente implementada y defendida» | ρ(T) con autovalores complejos (verificado, con la limitación de raíces múltiples); solución paramétrica; determinante | Verificado; **defenderlo requiere dominar Faddeev-LeVerrier y Durand-Kerner** |

## Limitaciones conocidas que afectan a requisitos

1. **Radio espectral con autovalores múltiples** (M4-05).
   - Durand-Kerner pierde precisión con raíces repetidas, del orden de 10⁻⁴ en una raíz triple.
   - La aplicación marca el resultado como no fiable y concluye «indeterminado», aunque ρ esté lejos de 1 (por ejemplo, la triple de 1/2).
   - **No da conclusiones falsas**, pero en esos casos no decide.
   - Las raíces λ = 0, el grado ≤ 2 y λ = ±1 se deciden de forma exacta.
2. **ρ cerca de 1.** Dentro de una banda de 10⁻⁹, o de 10⁻⁶ si hay raíces casi repetidas, la conclusión es «indeterminado».
3. **Revisión visual incompleta.** No se capturaron: la gráfica de una ejecución individual del Módulo IV, la figura 3D dentro del navegador y el espaciado corregido de las fracciones.
