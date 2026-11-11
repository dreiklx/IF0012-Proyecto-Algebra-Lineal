# Guía de recorrido del código (para Elmer, Samir, Daniel y Derek)

**Objetivo:** que cualquiera del grupo pueda abrir el proyecto y seguir cada procedimiento con este recorrido:

**ENTRADA DEL USUARIO → VALIDACIÓN → PROCEDIMIENTO MATEMÁTICO → RESULTADO → VISUALIZACIÓN**

Las referencias `archivo:línea` corresponden al estado del 10-nov-2026. Si cambian, la función conserva el mismo nombre: en VS Code, `Ctrl+P` y luego `@nombre` la encuentra.

## 1. Mapa visual

```text
                        ┌──────────────────────────── app.py ────────────────────────────┐
                        │  barra superior: Inicio · I · II · III · IV  (interfaz/navegacion.py) │
                        └──────┬───────────┬──────────────┬───────────────┬───────────────┘
                     paginas/sistemas  condicionamiento    minimos         iterativos
                               │           │              │               │
 ENTRADA          interfaz/modulos/modulo_I…  modulo_II…   modulo_III…     modulo_IV_iterativos/principal.py
 (editor)              └───────────┴──────┬───────┴───────────────┘   └─ pestana_ejecutar / comparar /
                                          │                               convergencia / precondicionamiento
                                          ▼
 VALIDACIÓN          interfaz/compartido/editor.py  (rejilla ↔ texto, aviso de dimensiones)
                     interfaz/compartido/componentes.py  leer_matriz_ui / leer_vector_ui
                     algebra/compartido/validacion.py    leer_numero → Fraction exacta o ErrorEntrada
                                          │
                                          ▼
 PROCEDIMIENTO       algebra/modulo_I_sistemas/directos.py ◄──────────── reutilizado por II, III y IV
                     algebra/modulo_II_condicionamiento/condicion.py
                     algebra/modulo_III_minimos/minimos.py
                     algebra/modulo_IV_iterativos/{metodos, ejecucion, convergencia, espectral, comparacion,
                                                   dispersas, precondicionamiento}.py
                     (todos usan algebra/compartido/matriz.py y exactos.py)
                                          │
                                          ▼
 RESULTADO           dataclasses: ResultadoSistema, ResultadoCondicion, ResultadoMinimos,
                     ResultadoIterativo, ResultadoComparacion, ResultadoEspectral, …
                     (se guardan en st.session_state para que no desaparezcan)
                                          │
                                          ▼
 VISUALIZACIÓN       interfaz/modulos/… (LaTeX, tablas, métricas)  +  visualizacion/interactivas.py (Plotly)
```

## 2. Qué hay en cada carpeta

| Carpeta | Contenido | ¿Calcula? |
|---|---|---|
| `algebra/compartido/` | Operaciones con matrices y normas (`matriz.py`), lectura y validación del texto (`validacion.py`), conversión a fracciones (`exactos.py`) | Utilidades, no métodos del curso |
| `algebra/modulo_I_sistemas/` | Gauss, Gauss-Jordan, clasificación, inversa, determinante | **Sí** |
| `algebra/modulo_II_condicionamiento/` | κ∞, perturbación, errores relativos | **Sí** |
| `algebra/modulo_III_minimos/` | Ecuaciones normales, residuo, ajuste lineal | **Sí** |
| `algebra/modulo_IV_iterativos/` | Jacobi, GS, SOR, convergencia, ρ(T), comparación, CSR, precondicionador | **Sí** |
| `interfaz/compartido/` | Estilo, editor, componentes, ejemplos | No |
| `interfaz/modulos/` | Una vista por módulo | No |
| `visualizacion/` | Gráficas | No |
| `gestos/` | Control gestual de la gráfica 3D: cámara, MediaPipe, reglas de gestos, cámara orbital, canal local. Leer en este orden: `mano.py` → `interpretacion.py` → `movimiento.py` → `control.py` | No (no toca el álgebra) |
| `tests/<módulo>/` | Pruebas de cada módulo | Verifica |
| `auditoria/` | Comparación con implementaciones independientes | Verifica |

## 3. Recorrido por módulo

### Módulo I — Sistemas lineales

| Paso | Dónde | Qué mirar |
|---|---|---|
| Entrada | `interfaz/modulos/modulo_I_sistemas.py:46` `mostrar` | Selector de ejemplo, editor de A y b, método (Gauss o Gauss-Jordan) y pivoteo |
| Validación | `algebra/compartido/matriz.py:122` `validar_sistema`; `validacion.leer_matriz` | Dimensiones y números válidos |
| **Inicio del procedimiento** | `algebra/modulo_I_sistemas/directos.py:297` `resolver_gauss` / `:302` `resolver_gauss_jordan` | Las dos llaman a `_resolver` |
| Corazón | `directos.py:144` `_escalonar` | Pivote (`_buscar_pivote`, :119), intercambio Fᵢ ↔ Fⱼ, multiplicador m = aᵢc/a_rc, Fᵢ → Fᵢ − m·Fᵣ; en Gauss-Jordan además normaliza y anula arriba |
| Clasificación | `directos.py:236` `_resolver`, `:200` `_rango_aumentada` | rango(A) frente a rango([A\|b]) |
| Solución | `directos.py:208` `_sustitucion_atras` | Sustitución hacia atrás; variables libres si hay infinitas soluciones |
| Resultado | `ResultadoSistema` (`directos.py:61`) | `pasos`, `clasificacion`, `solucion` o `solucion_particular` + `direcciones` |
| Visualización | `modulo_I_sistemas.py:102` `mostrar_resultado`; `visualizacion/interactivas.py` (rectas y planos) | Matriz en cada paso; interpretación geométrica |
| Pruebas | `tests/modulo_I/test_directos.py` | |

**Herramientas que reutilizan otros módulos:** `inversa_gauss_jordan` (`directos.py:323`), `solucion_unica` (`:307`) y `determinante` (`:355`).

### Módulo II — Condicionamiento

| Paso | Dónde | Qué mirar |
|---|---|---|
| Entrada | `interfaz/modulos/modulo_II_condicionamiento.py:48` `mostrar` | A, b y la perturbación (absoluta o %) |
| **Inicio** | `algebra/modulo_II_condicionamiento/condicion.py:105` `numero_condicion_infinito` | ‖A‖∞ (`matriz.norma_infinito_matriz`) · ‖A⁻¹‖∞, con A⁻¹ de `inversa_gauss_jordan` (Módulo I) |
| Clasificación | `condicion.py:83` `clasificar_kappa` | Escala del enunciado: < 10, < 100, ≥ 100 |
| Perturbación | `condicion.py:134` `construir_delta_b` → `:158` `analizar_perturbacion` | x y x̃ con el Gauss del Módulo I; ‖Δb‖∞/‖b‖∞, ‖Δx‖∞/‖x‖∞ y la cota κ·‖Δb‖/‖b‖ |
| Interpretación | `condicion.py:210` `_interpretar` | Texto automático |
| Visualización | `modulo_II_condicionamiento.py:107` `mostrar_resultado` | |
| Pruebas | `tests/modulo_II/test_condicion.py` | |

### Módulo III — Mínimos cuadrados

| Paso | Dónde | Qué mirar |
|---|---|---|
| Entrada | `interfaz/modulos/modulo_III_minimos.py:57` `sistema` y `:159` `ajuste` | Sistema A x = b o puntos (x, y) |
| **Inicio** | `algebra/modulo_III_minimos/minimos.py:111` `minimos_cuadrados` | `clasificar_forma` (m > n), AᵀA y Aᵀb, Gauss del Módulo I, r = b − Ax̂, ‖r‖₂ y Aᵀr = 0 |
| Verificación de clase | `minimos.py:168` `cramer` | Cramer sobre AᵀA y det([A\|b]), como en S8-30/09 pp. 6-7 |
| Ajuste | `minimos.py:182` `ajuste_lineal` | A = [[xᵢ, 1]] y la misma función |
| Visualización | `modulo_III_minimos.py:87` `mostrar_minimos`; `visualizacion/interactivas.py` (`ajuste`) | Recta y residuos |
| Pruebas | `tests/modulo_III/test_minimos.py` | |

### Módulo IV — Métodos iterativos

| Paso | Dónde | Qué mirar |
|---|---|---|
| Entrada | `interfaz/modulos/modulo_IV_iterativos/principal.py` `mostrar` | A, b, criterio, ε, k_max, N, ω, x⁽⁰⁾; `leer_todo` valida |
| **Fórmulas** | `algebra/modulo_IV_iterativos/metodos.py:35` `paso_jacobi` / `:48` `paso_gauss_seidel` / `:61` `paso_sor` | **Aquí está cada método**, una iteración por función |
| Validación | `ejecucion.py:205` `validar_configuracion` | ε > 0, k_max y N enteros, 0 < ω < 2, aᵢᵢ ≠ 0 |
| **Bucle común** | `ejecucion.py:259` `ejecutar` → `:274` `_ejecutar` | d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞, r_k, criterios A, B y C, motivo de parada |
| Convergencia | `convergencia.py:25` `dominancia_diagonal`, `:50` `reordenamiento_dominante` | Condición suficiente; reordenar como en clase |
| Radio espectral | `matriz_iteracion.py` `matriz_iteracion` → `polinomio_raices.py` `polinomio_caracteristico` y `raices` → `espectral.py` `radio_espectral` | T_J = −D⁻¹(L+U), T_GS = −(D+L)⁻¹U; Sarrus en 3×3 (`matriz_iteracion.py` `desarrollo_sarrus`) |
| Comparación | `comparacion.py:49` `comparar_metodos` | Los 3 métodos con la misma configuración; error final ‖x⁽ᵏ⁾ − x*‖∞ |
| Incentivo CSR | `dispersas.py:61` `a_csr` y `paso_*_csr` | Recorre solo los no nulos |
| Incentivo precondicionador | `precondicionamiento.py:85` `precondicionar_diagonal`, `:128` `analizar_precondicionador` | M = D; T y c idénticas; Richardson como extensión |
| Visualización | `pestana_ejecutar.py`, `pestana_comparar.py`, `pestana_convergencia.py`, `pestana_precondicionamiento.py` | Tabla, CSV, gráficas |
| Pruebas | `tests/modulo_IV/` | `test_iterativos` (P1-P21), `test_espectral`, `test_dispersas`, `test_precondicionamiento` |

## 4. Funciones compartidas (las que se ven en todos lados)

| Función | Archivo | Para qué |
|---|---|---|
| `leer_matriz`, `leer_vector`, `leer_numero` | `algebra/compartido/validacion.py` | Texto → números exactos o mensaje con la posición del error |
| `formatear_numero` | `algebra/compartido/validacion.py` | Mostrar fracciones y decimales de forma legible |
| `ErrorEntrada`, `ErrorMatriz`, `ErrorDimension` | `validacion.py`, `matriz.py` | Errores con mensaje para el usuario (nunca cierran la aplicación) |
| `a_fraccion` | `algebra/compartido/exactos.py` | Convertir a `Fraction` exacta (0.1 → 1/10) |
| `validar_cuadrada`, `validar_sistema`, `multiplicar_matrices`, `transpuesta`, normas | `algebra/compartido/matriz.py` | Operaciones elementales permitidas por el enunciado |
| `editor`, `analizar`, `aviso_dimensiones` | `interfaz/compartido/editor.py` | Editor de matrices y validación previa |
| `encabezado_modulo`, `seccion`, `tarjeta_resultado`, `insignias` | `interfaz/compartido/estilo.py` | Apariencia común |

## 5. Cómo ejecutar las pruebas

```bat
ejecutar_pruebas.bat
rem o bien
.venv\Scripts\python -m unittest -v
rem solo un módulo:
.venv\Scripts\python -m unittest discover -s tests\modulo_IV -t .
rem auditoría independiente (unos 20 s):
.venv\Scripts\python auditoria\auditoria_directos.py .
.venv\Scripts\python auditoria\auditoria_iterativos.py .
.venv\Scripts\python auditoria\auditoria_precondicionamiento.py .
```

## 6. Recorrido de estudio recomendado (unas 3 horas por persona)

La docente elige al menos dos módulos por integrante, así que **todos deben conocer los cuatro**.

1. **(20 min) Mapa general.** Esta guía, secciones 1 y 2, y [arquitectura.md](arquitectura.md). Abrir la aplicación y probar un ejemplo de cada módulo.
2. **(40 min) Módulo I.** Leer `_escalonar` línea por línea con el ejemplo S6-16/09 p. 29 (1/3, 4, 5/3), comparando con la pestaña de pasos de la aplicación. Es la base de los otros tres módulos.
3. **(25 min) Módulo II.** `numero_condicion_infinito` y `analizar_perturbacion`. Saber por qué se usa κ∞ y la escala de 3 niveles del enunciado y no la de la lámina ([referencia_oficial_procedimientos.md](referencia_oficial_procedimientos.md) §5).
4. **(25 min) Módulo III.** `minimos_cuadrados`: AᵀA, Aᵀb, Gauss, residuo. Repetir a mano el ejemplo del manuscrito (65/33, −29/33).
5. **(50 min) Módulo IV.**
   - `metodos.py` completo (son 87 líneas).
   - Después `_ejecutar`: cómo se calcula d_k y cuándo se detiene.
   - Después `matriz_iteracion` y `radio_espectral`.
6. **(20 min) Incentivos.** `dispersas.py` y [investigacion_richardson.md](investigacion_richardson.md). Saber decir en 30 segundos por qué M = D no cambia Jacobi.
7. **(Resto) Preguntas.** [guia_defensa_equipo.md](guia_defensa_equipo.md), partes D y E.

**Ejercicio de autocomprobación:** sin mirar esta guía, encontrar desde la carpeta raíz dónde se calcula el multiplicador de Gauss, dónde se decide que SOR terminó por tolerancia y dónde se arma T de Gauss-Seidel.
