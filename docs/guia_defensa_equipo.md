# Guía de defensa del equipo — Proyecto final IF0012

**Para:** Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez.
**Defensa:** semana del 16-nov-2026, individual, de 6 a 8 minutos por persona.
**Versión:** 10-nov-2026. Rutas actualizadas a la nueva organización por módulos y revisada contra las 457 páginas de los PDF de la docente (`docs/referencia_oficial_procedimientos.md`). Explica el código **real** del repositorio. Todos los números de los ejemplos se obtuvieron ejecutando la aplicación y se contrastaron con un cálculo independiente.

> **Cómo usar esta guía.** La docente elige **al menos dos módulos** y puede pedir un caso no preparado (OFICIAL p. 3). Por eso **cada integrante debe dominar los cuatro**. Primero lean las partes A y B, luego el módulo de la parte C junto con su teoría en la parte D, y al final practiquen las preguntas de la parte E con la aplicación abierta (parte F).
> Para repasar rápido está [resumen_logica_por_modulo.md](resumen_logica_por_modulo.md).
> Para encontrar cada función en el código: [guia_recorrido_codigo.md](guia_recorrido_codigo.md). Para Richardson: [investigacion_richardson.md](investigacion_richardson.md).

---

## Índice

- A. Visión general del proyecto
- B. Arquitectura del código
- C. Los cuatro módulos, función por función
- D. Explicación matemática, con ejemplos pequeños
- E. Preguntas de defensa, con respuestas
- F. Cómo ejecutar y demostrar el proyecto
- G. Limitaciones y decisiones técnicas

---

## A. Visión general del proyecto

### Qué hace la aplicación

Es **una sola aplicación web local**, hecha con Streamlit, que integra los cuatro módulos que pide el enunciado:

| Módulo | Problema | Métodos |
|---|---|---|
| I · Sistemas lineales | Resolver Ax = b y decir si tiene solución única, infinitas o ninguna | Gauss y Gauss-Jordan con pasos visibles; inversa y determinante |
| II · Condicionamiento | Medir cuánto cambia la solución si cambian los datos | κ∞(A) = ‖A‖∞‖A⁻¹‖∞ con nuestra inversa; perturbación de b |
| III · Mínimos cuadrados | «Resolver» un sistema con más ecuaciones que incógnitas, que en general no tiene solución | Ecuaciones normales AᵀA x̂ = Aᵀb con nuestro Gauss; ajuste de una recta |
| IV · Métodos iterativos | Aproximar la solución de Ax = b paso a paso y saber si el proceso converge | Jacobi, Gauss-Seidel, SOR; dominancia diagonal; matriz de iteración y radio espectral |

### Principio de diseño

**Toda la matemática está en la carpeta `algebra/`**, escrita desde cero en Python, solo con la biblioteca estándar.

- Lo único que se importa en el núcleo es `fractions`, `math`, `cmath` y `dataclasses`.
- La interfaz (`interfaz/`) solo lee lo que escribe el usuario y muestra resultados.
- Las gráficas (`visualizacion/`) solo dibujan resultados ya calculados.

Ningún archivo del proyecto importa NumPy, SciPy ni SymPy.

### Dos tipos de aritmética (decisión clave)

| Dónde | Aritmética | Por qué |
|---|---|---|
| Módulos I, II y III y la matriz T del Módulo IV | **Exacta**, con `fractions.Fraction` | 1/3 se guarda como 1/3. Un pivote es cero solo si es exactamente 0, así que la clasificación (única, infinitas o inconsistente) y la detección de singularidad no dependen de redondeos |
| Iteraciones de Jacobi, GS y SOR; raíces del polinomio característico | **Punto flotante** (`float`) | Las iteraciones son aproximaciones que se cortan por tolerancia; con fracciones los denominadores crecerían sin control. Las raíces de un polinomio de grado ≥ 3 en general no son racionales |

---

## B. Arquitectura del código

### Carpetas

```
proyecto-algebra/
├── app.py                         ← punto de entrada: navegación entre los 4 módulos
├── algebra/                       ← NÚCLEO MATEMÁTICO (Python puro)
│   ├── compartido/                ← matriz.py (operaciones, normas), validacion.py (texto → Fraction), exactos.py
│   ├── modulo_I_sistemas/         ← directos.py: Gauss, Gauss-Jordan, inversa, determinante
│   ├── modulo_II_condicionamiento/← condicion.py: κ∞, perturbación, errores relativos
│   ├── modulo_III_minimos/        ← minimos.py: ecuaciones normales, residuo, recta
│   └── modulo_IV_iterativos/
│       ├── metodos.py             ← fórmulas de Jacobi, GS y SOR (un paso cada uno)
│       ├── ejecucion.py           ← bucle común, criterios A/B/C, motivo de parada
│       ├── convergencia.py        ← dominancia diagonal y reordenamiento
│       ├── matriz_iteracion.py    ← D, L, U, D⁻¹, T y c (clase)
│       ├── polinomio_raices.py    ← polinomio y raíces (extensiones Cat. C)
│       ├── espectral.py           ← autovalores, ρ(T) y conclusión
│       ├── comparacion.py         ← comparación de los 3 métodos, error final
│       ├── dispersas.py           ← Incentivo: formato CSR
│       └── precondicionamiento.py ← Incentivo: precondicionador diagonal M = D
├── paginas/                       ← una página por módulo (barra superior); cada una llama a mostrar()
├── interfaz/                      ← Streamlit: no calcula nada
│   ├── navegacion.py, portada.py
│   ├── compartido/                ← estilo.py, componentes.py, editor.py, ejemplos.py
│   └── modulos/                   ← modulo_I_sistemas.py, modulo_II_condicionamiento.py,
│                                    modulo_III_minimos.py, modulo_IV_iterativos/ (una vista por pestaña)
├── visualizacion/                 ← Plotly (interactivas.py); Matplotlib solo como oráculo de las pruebas
├── tests/                         ← 295 pruebas, una carpeta por módulo
├── auditoria/                     ← comparación aleatoria contra oráculos independientes
├── casos_prueba/                  ← casos documentados por módulo (entrada, esperado, obtenido)
└── docs/                          ← manual, guías, referencia oficial, matriz de cumplimiento
```

### Reglas de dependencia

- `interfaz/` puede usar `algebra/` y `visualizacion/`.
- `visualizacion/` solo recibe resultados.
- `algebra/` **no** importa nada de la interfaz.

Por eso el núcleo se puede probar sin abrir la aplicación, y eso es exactamente lo que hacen `tests/` y `auditoria/`.

### Representación de los datos

- **Matriz:** lista de filas. Por ejemplo, `[[1, 2], [3, 4]]`.
- **Vector:** lista plana, por ejemplo `[1, 2, 3]`.
- **Resultados:** se devuelven como `dataclass`, con todos los datos que la interfaz necesita mostrar:
  - `ResultadoSistema` e `ResultadoInversa` (`directos.py`);
  - `ResultadoCondicion` y `ResultadoPerturbacion` (`condicion.py`);
  - `ResultadoMinimos` y `ResultadoAjuste` (`minimos.py`);
  - `ResultadoIterativo` (`ejecucion.py`) y `ResultadoComparacion` (`comparacion.py`);
  - `ResultadoEspectral` (`espectral.py`).
- **Errores:** son excepciones propias.
  - `ErrorMatriz` y su subclase `ErrorDimension`, en `matriz.py`;
  - `ErrorEntrada`, en `validacion.py`;
  - `ErrorSistema`, en `directos.py`, cuando un módulo exige solución única y no la hay;
  - `ErrorAjuste`, en `minimos.py`.

### Flujo de la información (igual en los cuatro módulos)

```
Usuario escribe texto
   │   p. ej. "1 1 1\n2 1 -1\n-1 1 2"
   ▼
interfaz/modulos/…    ──►  componentes.leer_matriz_ui / leer_vector_ui  (interfaz/compartido/)
   │                         └─► validacion.leer_matriz → leer_numero (Fraction exacta)
   │                             si hay error: st.error("… elemento (2, 2) …") y se detiene
   ▼
algebra/modulo_X/…    ──►  función principal (p. ej. resolver_gauss)
   │                         valida dimensiones (matriz.validar_*), calcula y
   │                         devuelve un dataclass Resultado…
   ▼
st.session_state       ──►  el resultado se guarda para que no desaparezca al interactuar
   ▼
interfaz/modulos/… (mostrar_resultado) ──► st.latex / st.table / st.metric
   └─► visualizacion/interactivas.py (figura Plotly) ──► componentes.mostrar_interactiva
```

`interfaz/navegacion.py` contiene la lista `PAGINAS` (archivo, título y dirección de cada página). `app.py` la convierte en páginas `st.Page` y la muestra como barra superior con `st.navigation(..., position="top")`. Cada archivo de `paginas/` solo llama al `mostrar()` de su módulo de interfaz. La portada está en `interfaz/portada.py`.

### Índice de funciones importantes (archivo:línea)

| Función | Qué hace |
|---|---|
| `algebra/compartido/validacion.py:26` `leer_numero` | Texto → `Fraction`. Acepta `3`, `-2.5`, `2,5`, `1/3` y `1e-3` |
| `algebra/compartido/validacion.py:55` `leer_matriz` | Una fila por línea; exige que todas las filas tengan la misma longitud |
| `algebra/compartido/validacion.py:89` `leer_tolerancia` / `:97` `leer_entero_positivo` / `:108` `leer_omega` | ε > 0; k_max y N enteros; 0 < ω < 2 |
| `algebra/compartido/matriz.py:69` `validar_matriz` / `:122` `validar_sistema` | Comprueba la forma rectangular, los números válidos y que b tenga m componentes |
| `algebra/compartido/matriz.py:240` `norma_infinito_vector` / `:255` `norma_infinito_matriz` | máx\|vᵢ\| y máxima suma de fila |
| `algebra/compartido/matriz.py:335` `residuo` | r = b − Ax |
| `algebra/modulo_I_sistemas/directos.py:144` `_escalonar` | **Corazón del Módulo I**: pivotes, intercambios, eliminación, determinante |
| `algebra/modulo_I_sistemas/directos.py:236` `_resolver` | Clasificación por rangos y solución (única o paramétrica) |
| `algebra/modulo_I_sistemas/directos.py:323` `inversa_gauss_jordan` | [A \| I] → [I \| A⁻¹] y verificación A·A⁻¹ = I |
| `algebra/modulo_I_sistemas/directos.py:355` `determinante` | (−1)^intercambios · Π pivotes |
| `algebra/modulo_II_condicionamiento/condicion.py:105` `numero_condicion_infinito` | κ∞ e interpretación |
| `algebra/modulo_II_condicionamiento/condicion.py:134` `construir_delta_b` / `:158` `analizar_perturbacion` | Δb absoluta o porcentual; x frente a x̃ |
| `algebra/modulo_III_minimos/minimos.py:111` `minimos_cuadrados` / `:182` `ajuste_lineal` | Ecuaciones normales, residuo, recta; det([A\|b]) si m = n + 1 |
| `algebra/modulo_III_minimos/minimos.py:168` `cramer` | Regla de Cramer (procedimiento de clase), usada como verificación |
| `algebra/modulo_IV_iterativos/metodos.py:35` `paso_jacobi` / `:48` `paso_gauss_seidel` / `:61` `paso_sor` | Una iteración de cada método |
| `algebra/modulo_IV_iterativos/metodos.py:75` `paso_richardson` | Richardson x ← x + (b − Ax): solo para el análisis del precondicionador |
| `algebra/modulo_IV_iterativos/ejecucion.py:205` `validar_configuracion` | Valida A, b, x⁽⁰⁾, ε, k_max, N y ω |
| `algebra/modulo_IV_iterativos/ejecucion.py:259` `ejecutar` / `:274` `_ejecutar` | Bucle común, métricas d_k y r_k, criterios A, B y C, motivos de parada |
| `algebra/modulo_IV_iterativos/convergencia.py:25` `dominancia_diagonal` | \|aᵢᵢ\| > Σ_{j≠i}\|aᵢⱼ\| fila por fila |
| `algebra/modulo_IV_iterativos/convergencia.py:50` `reordenamiento_dominante` | Orden de las ecuaciones que logra la dominancia (como en la Tarea II) |
| `algebra/modulo_IV_iterativos/comparacion.py:49` `comparar_metodos` | Los 3 métodos con las mismas condiciones; error final e = ‖x⁽ᵏ⁾ − x*‖∞ |
| `algebra/modulo_IV_iterativos/matriz_iteracion.py` `matriz_iteracion` | T y c exactas para Jacobi, GS y SOR |
| `algebra/modulo_IV_iterativos/polinomio_raices.py` `polinomio_caracteristico` | Faddeev-LeVerrier (exacto) |
| `algebra/modulo_IV_iterativos/matriz_iteracion.py` `desarrollo_sarrus` | Procedimiento de clase en 3×3: tr(T), Σ menores, det(T) por Sarrus |
| `algebra/modulo_IV_iterativos/polinomio_raices.py` `durand_kerner` / `raices` | Raíces: λ = 0 exactas, grado ≤ 2 por fórmula, grado ≥ 3 por Durand-Kerner |
| `algebra/modulo_IV_iterativos/espectral.py` `analizar_matriz` | Autovalores, ρ, verificaciones y p(±1) = 0 de cualquier matriz |
| `algebra/modulo_IV_iterativos/espectral.py` `concluir` / `radio_espectral` | ρ(T), verificaciones y conclusión |
| `algebra/modulo_IV_iterativos/dispersas.py:61` `a_csr` | Densa → CSR (`valores`, `columnas`, `inicio`) |
| `algebra/modulo_IV_iterativos/precondicionamiento.py:85` `precondicionar_diagonal` / `:128` `analizar_precondicionador` | M = D, B = D⁻¹A, b̃; comparación original frente a precondicionado |

---

## C. Los cuatro módulos, función por función

### Módulo I — Sistemas lineales y métodos directos

**Archivos:** `algebra/modulo_I_sistemas/directos.py` (núcleo) e `interfaz/modulos/modulo_I_sistemas.py` (pantalla).

1. **Problema.** Resolver Ax = b con A de m×n (no tiene que ser cuadrada) y clasificar el sistema.
2. **Entrada.** A y b como texto. En la pantalla también se eligen el método («Gauss» o «Gauss-Jordan») y la estrategia de pivote («primer no nulo», como en clase, o «pivoteo parcial»).
3. **Operaciones.** Solo las operaciones elementales de fila: Fᵢ ↔ Fⱼ, Fᵢ → Fᵢ/p y Fᵢ → Fᵢ − m·Fᵣ.
4. **Fórmulas.** El multiplicador es m = aᵢc / a_rc. La sustitución hacia atrás es x_c = (b'_r − Σ_{j>c} u_rj x_j) / u_rc. El determinante es det A = (−1)^(intercambios) · Π pivotes.
5. **Algoritmo.** `resolver_gauss` y `resolver_gauss_jordan` llaman a `_resolver(A, b, metodo, estrategia)`.
6. **Paso a paso:**
   1. `validar_sistema(A, b)` devuelve (m, n) o lanza `ErrorDimension`.
   2. Todo se convierte a `Fraction` con `a_fraccion`. Un `float` 0.1 pasa a 1/10 mediante `repr`.
   3. Se arma la matriz aumentada `M = [A | b]` y se registra el primer `Paso`.
   4. `_escalonar(M, n, estrategia, reducida, pasos, advertencias, referencia)` recorre las columnas c = 0…n−1 con un puntero `fila`:
      - `_buscar_pivote` busca, desde `fila` hacia abajo, la primera fila con elemento ≠ 0 (o la de mayor |elemento| con pivoteo parcial).
      - Si no hay ninguna, **la columna no tiene pivote**: su variable será libre y se pasa a la siguiente columna (`continue`).
      - Si el pivote está en otra fila, se **intercambian filas**: el paso se registra con su motivo («el elemento (1, 1) es 0») y `signo = −signo`.
      - `producto *= pivote` acumula el producto de pivotes para el determinante.
      - Si |pivote| < 10⁻¹⁰ · máx|aᵢⱼ| (`UMBRAL_PIVOTE_PEQUENO`), se agrega un aviso de «pivote numéricamente problemático».
      - En **Gauss-Jordan** (`reducida=True`), la fila se divide entre el pivote y se anulan los elementos de **todas** las demás filas. En **Gauss**, solo los de abajo.
      - Cada operación guarda un `Paso(descripcion, copia de la matriz)`.
   5. `rango_A = len(pivotes)`. `_rango_aumentada` busca una fila [0 … 0 | c] con c ≠ 0; si la hay, rango([A|b]) = rango(A) + 1.
   6. Clasificación:
      - rango(A) < rango([A|b]) → **INCONSISTENTE**;
      - no hay variables libres → **UNICA**;
      - hay libres → **INFINITAS**.
   7. `_sustitucion_atras` despeja de abajo hacia arriba.
      - Con las libres iguales a 0 se obtiene la solución única o la **solución particular** xₚ.
      - Cada **dirección** vⱼ se obtiene resolviendo el sistema homogéneo con la libre j igual a 1 y las demás iguales a 0.
      - La solución general es x = xₚ + t₁v₁ + ….
7. **Resultados (`ResultadoSistema`):** `clasificacion`, `mensaje`, `rango_A`, `rango_aumentada`, `solucion` o `solucion_particular` con `direcciones`, `variables_libres`, `pasos`, `sustitucion`, `advertencias`, `matriz_final` y `determinante` (solo si A es cuadrada).
   - La pantalla además verifica b − Ax con `matriz.residuo` (debe dar 0) y dibuja rectas o planos si n = 2 o 3 (`visualizacion/interactivas.py` `rectas_2d` / `planos_3d`).
8. **Validaciones:**
   - texto vacío o no numérico, con la posición exacta;
   - filas de distinta longitud;
   - b con un número de componentes distinto de m;
   - pivote nulo, que se resuelve con un intercambio;
   - pivote pequeño, que genera un aviso.
9. **Errores posibles:** `ErrorEntrada` (texto) y `ErrorMatriz`/`ErrorDimension` (forma). La interfaz los muestra en rojo y no se cierra.
10. **Funciones relacionadas:**
    - `inversa_gauss_jordan(A)` aplica `_escalonar` sobre [A | I]. Si faltan pivotes, A es singular y devuelve `invertible=False` con det = 0. Si no, toma la parte derecha y comprueba `multiplicar_matrices(A, inversa) == I` (`verificacion_identidad`).
    - `determinante(A)` calcula (−1)^intercambios · Π pivotes.
    - `solucion_unica(A, b)` es la puerta de entrada que usan los Módulos II, III y IV: devuelve x o lanza `ErrorSistema`.

### Módulo II — Condicionamiento y sensibilidad

**Archivos:** `algebra/modulo_II_condicionamiento/condicion.py` e `interfaz/modulos/modulo_II_condicionamiento.py`.

1. **Problema.** ¿Cuánto puede cambiar la solución x si los datos b cambian un poco?
2. **Entrada.** A cuadrada, b y una perturbación: absoluta (un número o un vector Δb) o porcentual (un p o un vector de pᵢ).
3. **Operaciones.** Norma ∞ de matriz y de vector, inversa por Gauss-Jordan y dos resoluciones por Gauss.
4. **Fórmulas:**
   - κ∞(A) = ‖A‖∞·‖A⁻¹‖∞;
   - errores relativos ‖Δb‖∞/‖b‖∞ y ‖Δx‖∞/‖x‖∞;
   - cota ‖Δx‖/‖x‖ ≤ κ·‖Δb‖/‖b‖;
   - en modo porcentual, Δbᵢ = (pᵢ/100)·bᵢ.
5. **Algoritmo:**
   - `numero_condicion_infinito(A)`:
     1. calcula `norma_infinito_matriz(A)`;
     2. calcula `inversa_gauss_jordan(A)`. Si A no es invertible, devuelve `MATRIZ_SINGULAR` y κ no está definido;
     3. calcula `norma_infinito_matriz(A⁻¹)` y κ = producto;
     4. asigna la sensibilidad con `clasificar_kappa`: κ < 10 baja, 10 ≤ κ < 100 moderada, κ ≥ 100 alta.
   - `construir_delta_b(b, modo, valor)` construye Δb.
   - `analizar_perturbacion(A, b, Δb)`:
     1. x = `solucion_unica(A, b)` y x̃ = `solucion_unica(A, b + Δb)`, ambas con Gauss exacto;
     2. Δx = x̃ − x y las cuatro normas;
     3. los errores relativos, o `None` y un aviso si el denominador es 0;
     4. la cota κ·rel_b, `cumple_cota` y la amplificación rel_x/rel_b;
     5. el texto de `_interpretar`.
6. **Resultados:** `ResultadoCondicion` (`norma_A`, `inversa`, `norma_inversa`, `kappa`, `clasificacion`, `interpretacion`) y `ResultadoPerturbacion` (x, x̃, Δb, Δx, normas, errores relativos, cota, `cumple_cota`, amplificación e interpretación).
7. **Validaciones:**
   - A cuadrada;
   - b y Δb con n componentes;
   - singularidad, que se informa **aparte** y nunca como «κ grande»;
   - denominadores cero.
8. **Errores posibles:** `ErrorDimension`, `ErrorEntrada` (texto de la perturbación) y `ErrorSistema` (se atrapan en la interfaz).

### Módulo III — Mínimos cuadrados y ajuste lineal

**Archivos:** `algebra/modulo_III_minimos/minimos.py` e `interfaz/modulos/modulo_III_minimos.py`.

1. **Problema.** Si A es m×n con m > n, Ax = b en general no tiene solución. Se busca x̂ que haga ‖b − Ax‖₂ lo más pequeño posible.
2. **Entrada.** A y b (pestaña «Sistema sobredeterminado»), o listas de puntos xᵢ, yᵢ (pestaña «Ajuste lineal»).
3. **Operaciones.** Transpuesta, productos AᵀA y Aᵀb y Gauss sobre las ecuaciones normales.
4. **Fórmulas:** AᵀA x̂ = Aᵀb; r = b − Ax̂; ‖r‖₂ = √(Σ rᵢ²). Como control, Aᵀr = 0.
5. **Algoritmo** (`minimos_cuadrados(A, b)`):
   1. `validar_sistema` y conversión a `Fraction`.
   2. `clasificar_forma(m, n)` → SOBREDETERMINADO, CUADRADO o SUBDETERMINADO.
   3. Comprueba si b pertenece a Col(A): `resolver_gauss(A, b)` no debe dar INCONSISTENTE.
   4. `transpuesta`, `multiplicar_matrices(Aᵀ, A)` y `multiplicar_matriz_vector(Aᵀ, b)`.
   5. `resolver_gauss(AᵀA, Aᵀb)`, el método directo del Módulo I. Si no da solución única, AᵀA es singular (columnas dependientes): se informa y no se presenta x̂.
   6. Calcula A x̂, r = b − A x̂, ‖r‖₂² **exacta**, ‖r‖₂ con `math.sqrt` (lo único inexacto), ‖r‖∞ y Aᵀr.
   7. **Procedimiento de clase como verificación** (S8-30/09 pp. 6-7):
      - si m = n + 1, `det_aumentada` = det([A | b]): si es ≠ 0, b ∉ Col(A);
      - si n ≤ 3, `cramer(AtA, Atb)` resuelve con la regla de Cramer, x_j = det(M_j)/det(AᵀA).
      - La pantalla muestra los tres pasos de la docente en «Verificación con el procedimiento de clase», y Cramer **coincide exactamente** con Gauss.
      - Ejemplo del manuscrito: det([A|b]) = −11, |AᵀA| = 363, |Aₓ| = 715, |A_y| = −319, x̂ = (65/33, −29/33).
   - `ajuste_lineal(xs, ys)`:
     1. exige listas de la misma longitud, al menos 2 puntos y que no todos los x sean iguales;
     2. arma la matriz de diseño `[[xᵢ, 1]]` y llama a `minimos_cuadrados`;
     3. de x̂ = (m, c) sale la ecuación «y = m x + c».
6. **Resultados:** `ResultadoMinimos` (`tipo`, `AtA`, `Atb`, `solucion`, `estimados`, `residuo`, `norma_residuo_2`, `norma_residuo_2_cuadrado`, `norma_residuo_inf`, `ortogonalidad` = Aᵀr y `mensaje`) y `ResultadoAjuste` (pendiente, intercepto, ecuación). `visualizacion/interactivas.py::ajuste` dibuja los puntos, la recta y los residuos.
7. **Validaciones y errores:**
   - dimensiones;
   - AᵀA singular;
   - menos de 2 puntos;
   - x todos iguales (recta vertical, `ErrorAjuste`);
   - número distinto de x y de y.

### Módulo IV — Métodos iterativos y convergencia

**Archivos:** `algebra/modulo_IV_iterativos/`, `algebra/modulo_IV_iterativos/matriz_iteracion.py`, `polinomio_raices.py`, `espectral.py`, `algebra/modulo_IV_iterativos/dispersas.py`, `algebra/modulo_IV_iterativos/precondicionamiento.py` e `interfaz/modulos/modulo_IV_iterativos/`. La pantalla tiene cuatro pestañas: «Ejecutar un método», «Comparar métodos», «Convergencia» y «Precondicionamiento diagonal».

1. **Problema.** Aproximar la solución de Ax = b (A n×n) con iteraciones x⁽ᵏ⁾, y saber si convergen.
2. **Entrada:**
   - A y b;
   - el criterio de parada: A (cambio), B (residuo) o C (N fijas);
   - ε y k_max (criterios A y B) o N (criterio C);
   - ω (solo SOR);
   - x⁽⁰⁾: cero, bᵢ/aᵢᵢ (`vector_diagonal`) o personalizado;
   - la opción de almacenamiento CSR.
3. **Fórmulas por componentes** (i = 1…n):
   - **Jacobi** (`paso_jacobi`): xᵢ⁽ᵏ⁾ = (bᵢ − Σ_{j≠i} aᵢⱼ xⱼ⁽ᵏ⁻¹⁾) / aᵢᵢ. Usa solo el vector anterior y crea un vector nuevo.
   - **Gauss-Seidel** (`paso_gauss_seidel`): igual, pero actualiza **sobre la misma lista** `x`. Así, para j < i ya usa xⱼ⁽ᵏ⁾.
   - **SOR** (`paso_sor`): xᵢ⁽ᵏ⁾ = (1 − ω)xᵢ⁽ᵏ⁻¹⁾ + ω·[valor de Gauss-Seidel]. Con ω = 1 es Gauss-Seidel (prueba P15).
4. **Métricas en cada iteración** (`FilaIteracion`):
   - d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ (no existe para k = 0);
   - r_k = ‖b − Ax⁽ᵏ⁾‖∞, con la A y la b **originales**;
   - en la comparación, además, e_k = ‖x⁽ᵏ⁾ − x*‖∞, con x* la solución exacta de Gauss.
5. **Algoritmo común** (`ejecutar` → `_ejecutar`):
   1. `validar_configuracion` comprueba el método, el criterio, A cuadrada, las longitudes, ε > 0 (y que no se anule en `float`), k_max o N entero en [1, 100 000] y 0 < ω < 2. Convierte todo a `float`.
   2. Si algún aᵢᵢ = 0 → `DIAGONAL_CERO`: no se itera.
   3. Elige el paso del método (`PASOS` o `PASOS_CSR`) y calcula r₀. Con el criterio B, si r₀ < ε se detiene en k = 0.
   4. Para k = 1…límite:
      - calcula `x_nuevo = paso(...)`;
      - si hay inf o nan → `ERROR_NO_FINITO`;
      - calcula d y r y guarda la fila;
      - criterio A: si d < ε → `TOLERANCIA_CAMBIO`. Criterio B: si r < ε → `TOLERANCIA_RESIDUO`. La desigualdad es **estricta**.
   5. Al acabar el bucle: con el criterio C → `N_COMPLETADAS` («no demuestra convergencia»); si no → `MAXIMO_ITERACIONES` («sin satisfacer el criterio», **sin** afirmar divergencia).
   - `ejecutar` **nunca lanza excepciones**: una entrada inválida da `ENTRADA_INVALIDA` y un fallo inesperado da `ERROR_INTERNO`.
6. **Comparación** (`comparar_metodos`):
   - Ejecuta las configuraciones de `configuraciones_homogeneas`: mismo criterio, ε, k_max, N y x⁽⁰⁾; SOR usa además su ω.
   - Comprueba la homogeneidad campo por campo (`CAMPOS_HOMOGENEOS`).
   - Calcula x* con `solucion_unica` y el error e_k de cada iteración. El **error final** e = ‖x⁽ᵏ⁾ − x*‖∞ es la misma columna «Error final (‖x⁽ᵏ⁾ − x‖∞)» de la tabla de la lámina S9-05/10 p. 17. Por eso e_k es la primera métrica de la gráfica comparativa.
   - La pantalla agrega ρ(T) de cada método.
7. **Convergencia:**
   - `dominancia_diagonal(A)` comprueba fila por fila |aᵢᵢ| > Σ_{j≠i}|aᵢⱼ|.
   - `reordenamiento_dominante(A, b)` busca el orden de las ecuaciones que hace la matriz dominante, como hace la docente en la Tarea II #2-3.
     - Idea: si la fila i es dominante con su elemento de la columna j, entonces 2|aᵢⱼ| > Σₖ|aᵢₖ|, y solo una columna puede cumplirlo. Se asigna cada fila a esa columna y se comprueba que sea una permutación.
     - La pantalla lo **sugiere** (no cambia los datos), aunque algún aᵢᵢ sea 0.
   - `radio_espectral(A, b, método, ω)`:
     1. `matriz_iteracion` construye D, L, U, T y c **exactas**.
     2. Si n > 8 → `NO_CALCULADO`.
     3. `polinomio_caracteristico(T)` aplica Faddeev-LeVerrier y da [1, c₁, …, cₙ] de det(λI − T). Si T es 3×3, la pantalla muestra además el **desarrollo de clase por Sarrus** (`desarrollo_sarrus`: tr(T), Σ menores 2×2, det(T)) y comprueba que da el mismo polinomio.
     4. `raices` obtiene los autovalores, si son fiables y, si es posible, una decisión exacta.
     5. ρ = máx|λ|.
     6. Verificaciones: |p(λ)| relativo < 10⁻⁸ y Σλ = traza(T).
     7. Comprobación exacta de p(1) = 0 o p(−1) = 0.
     8. `concluir` → CONVERGE, NO_CONVERGE o INDETERMINADO.
8. **Resultados:**
   - `ResultadoIterativo`: `codigo`, `mensaje`, `criterio_cumplido`, `historial`, `advertencias`, `k_final`, `x_final`, `d_final` y `r_final`.
   - La tabla (`filas_tabla`) rotula la columna que actúa como criterio. Hay gráfica (`interactivas.convergencia`) y CSV (`csv_historial`).
   - `ResultadoComparacion` y `ResultadoEspectral` (T, polinomio, autovalores, ρ, `fiable`, `decision_exacta`, verificaciones y avisos).
9. **Códigos de terminación:**

   | Código | Significado |
   |---|---|
   | `TOLERANCIA_CAMBIO` | d_k < ε |
   | `TOLERANCIA_RESIDUO` | r_k < ε |
   | `N_COMPLETADAS` | Se hicieron las N iteraciones pedidas |
   | `MAXIMO_ITERACIONES` | Se llegó a k_max sin cumplir el criterio |
   | `ERROR_NO_FINITO` | Desbordamiento numérico |
   | `DIAGONAL_CERO` | Algún aᵢᵢ = 0 |
   | `ENTRADA_INVALIDA` | Dato inválido |
   | `ERROR_INTERNO` | Fallo inesperado |

10. **CSR** (`dispersas.py`):
    - `a_csr` guarda solo los no nulos en `valores`, `columnas` e `inicio`.
    - `paso_*_csr` recorre solo esos elementos, de modo que cada iteración cuesta O(nnz) en lugar de O(n²).
    - Las iteraciones son **idénticas** a las densas: se suman los mismos productos en el mismo orden.
11. **Precondicionamiento diagonal** (`algebra/modulo_IV_iterativos/precondicionamiento.py`, pestaña «Precondicionamiento diagonal»):
    - `precondicionar_diagonal(A, b)` construye M = D, M⁻¹, B = D⁻¹A y b̃ = D⁻¹b, de forma exacta. Exige que no haya ningún aᵢᵢ = 0.
    - `analizar_precondicionador(A, b, config, ω)` calcula:
      - κ∞(A) y κ∞(B), con `numero_condicion_infinito`;
      - los autovalores de A y de B, con `analizar_matriz`;
      - la ejecución de Jacobi, GS, SOR y **Richardson** (`paso_richardson`) sobre los dos sistemas, con la misma configuración;
      - ρ de cada matriz de iteración;
      - la comparación **exacta** de T y c (`T_identicas`) y si las iteraciones coinciden (`mismas_iteraciones`).
    - Devuelve `ResultadoPrecondicionamiento` con la lista `comparaciones` (de tipo `ComparacionMetodo`) y las `conclusiones` en texto. La gráfica es `interactivas.precondicionador`.

---

## D. Explicación matemática, con ejemplos pequeños

### D.1 Gauss: por qué funciona y cómo clasifica

**Por qué funciona.** Las operaciones elementales de fila se pueden deshacer y no cambian el conjunto de soluciones. Si [A|b] se transforma en [U|b'] escalonada, los dos sistemas tienen exactamente las mismas soluciones, y el escalonado se resuelve de abajo hacia arriba.

**Ejemplo real de la aplicación** («2 incógnitas: 2x + y = 5, x − y = 1»):

```
[ 2   1 | 5 ]   F2 → F2 − (1/2)·F1   [ 2    1   |  5   ]
[ 1  −1 | 1 ]  ───────────────────►  [ 0  −3/2  | −3/2 ]
x2 = (−3/2 − 0) / (−3/2) = 1;     x1 = (5 − 1·1) / 2 = 2
det = (+1)·2·(−3/2) = −3     (0 intercambios; pivotes 2 y −3/2)
```

Son exactamente los pasos que imprime `_escalonar` y los textos que genera `_sustitucion_atras`.

**Clasificación (Rouché-Frobenius).** El rango es el número de pivotes.

- Si queda una fila [0 0 … 0 | c] con c ≠ 0, esa fila dice «0 = c»: es imposible, y el sistema es inconsistente.
- Si no queda ninguna, el sistema es consistente:
  - cada columna con pivote fija una variable;
  - las columnas sin pivote son variables libres (n − rango de ellas).
  - Con 0 libres la solución es única; con ≥ 1, hay infinitas.

**Forma paramétrica** (ejemplo precargado «Infinitas soluciones»: x + y + z = 1, 2x + 2y + 2z = 2, x − y = 0).

- El rango es 2 y z es libre.
- La aplicación da x = (1/2, 1/2, 0) + t·(−1/2, −1/2, 1).
- Comprobación: A·(−1/2, −1/2, 1) = 0, porque v resuelve el sistema homogéneo.

**Por qué se intercambian filas.** Si el pivote es 0, dividir entre él es imposible. Se busca abajo un elemento ≠ 0. Intercambiar filas solo reordena ecuaciones, pero **cambia el signo del determinante**; por eso `signo = −signo`.

**Pivoteo parcial.** Elegir el mayor |aᵢc| hace que |m| ≤ 1 y reduce la propagación del redondeo **en punto flotante**. Con fracciones exactas no cambia la solución; se ofrece porque es la práctica numérica estándar.

**Inversa.**

- Aplicar Gauss-Jordan a [A | I] equivale a multiplicar por la izquierda por un producto E de matrices elementales tal que EA = I. Entonces E = A⁻¹, y la parte derecha (EI) es A⁻¹.
- Si alguna columna no tiene pivote, rango(A) < n y A no es invertible.
- Ejemplo: [[2, 1], [1, 1]]⁻¹ = [[1, −1], [−1, 2]].

### D.2 Condicionamiento: de dónde sale la cota

**Demostración** (en 3 líneas, que conviene saber):

1. Ax = b y A(x + Δx) = b + Δb, de modo que AΔx = Δb y Δx = A⁻¹Δb. Por eso ‖Δx‖ ≤ ‖A⁻¹‖‖Δb‖.
2. b = Ax, de modo que ‖b‖ ≤ ‖A‖‖x‖, es decir, 1/‖x‖ ≤ ‖A‖/‖b‖.
3. Multiplicando: ‖Δx‖/‖x‖ ≤ ‖A‖‖A⁻¹‖ · ‖Δb‖/‖b‖ = κ(A)·‖Δb‖/‖b‖.

**Qué significa:** κ es el **factor máximo** de amplificación del error relativo. Es un peor caso; la amplificación observada puede ser menor (depende de la dirección de Δb). También se cumple κ ≥ 1, porque 1 = ‖I‖ = ‖AA⁻¹‖ ≤ ‖A‖‖A⁻¹‖.

**Ejemplo pequeño** (precargado «κ∞ = 16/5»): A = [[1, 2], [3, 1]].

- ‖A‖∞ = máx(1 + 2, 3 + 1) = 4.
- det = 1 − 6 = −5, de modo que A⁻¹ = (1/−5)[[1, −2], [−3, 1]] = [[−1/5, 2/5], [3/5, −1/5]].
- ‖A⁻¹‖∞ = máx(3/5, 4/5) = 4/5.
- κ∞ = 4 · 4/5 = 16/5 = 3.2, sensibilidad **baja**.
- Con b = (3, 4) y Δb = (0.1, 0.1): x = (1, 1) y x̃ = (51/50, 26/25).
  - ‖Δb‖/‖b‖ = 0.1/4 = 0.025 y ‖Δx‖/‖x‖ = 0.04.
  - Cota: 3.2 · 0.025 = 0.08 ≥ 0.04 ✓.

**Matriz mal condicionada** («S7-21/09 p. 15»): A = [[1, 1], [1, 1.0001]].

- κ∞ = 400040001/10000 ≈ 40004.
- Un cambio de 0.0001 en b₂ (error relativo ≈ 5·10⁻⁵) lleva x de (1, 1) a (0, 2): error relativo del **100 %**.

**Singular no es lo mismo que mal condicionada:**

- Si A es singular, no existe A⁻¹, κ no está definido (se toma como infinito) y no hay solución única.
- Si A es invertible con κ grande, la solución existe y es única, pero es muy sensible a los datos.

La aplicación los distingue (`MATRIZ_SINGULAR`).

**Por qué funciona la perturbación porcentual.** Si Δb = (p/100)·b, entonces ‖Δb‖∞/‖b‖∞ = |p|/100 exactamente.

### D.3 Mínimos cuadrados: por qué las ecuaciones normales

**Planteamiento.** Se busca minimizar f(x) = ‖b − Ax‖₂² = (b − Ax)ᵀ(b − Ax).

**Por cálculo.** ∇f = −2Aᵀ(b − Ax). Igualarlo a 0 da **AᵀA x = Aᵀb**.

**Por geometría.**

- Ax recorre el espacio columna Col(A).
- El punto de Col(A) más cercano a b es la proyección ortogonal de b.
- En ese punto el residuo r = b − Ax̂ es perpendicular a cada columna de A, es decir, **Aᵀr = 0**.
- Esa es la comprobación que muestra la aplicación.

**Unicidad.** Si las columnas de A son independientes, AᵀA es invertible: si AᵀAx = 0, entonces xᵀAᵀAx = ‖Ax‖² = 0, de modo que Ax = 0 y x = 0. Si las columnas son dependientes, hay infinitos x̂ y la aplicación no presenta ninguno (ejemplo «Columnas dependientes», donde la columna 2 es el doble de la 1).

**Ejemplo real** («y = 0.75x + 1.2»): puntos (1, 2), (2, 2.5), (3, 3.7), (4, 4.1).

- A = [[1, 1], [2, 1], [3, 1], [4, 1]].
- AᵀA = [[Σx², Σx], [Σx, k]] = [[30, 10], [10, 4]].
- Aᵀb = [Σxy, Σy] = [34.5, 12.3].
- Resolviendo: 30m + 10c = 34.5 y 10m + 4c = 12.3. Restando a la segunda, multiplicada por 3, la primera: 2c = 2.4, así que **c = 6/5** y **m = 3/4**. La aplicación muestra «y = 3/4 x + 6/5».
- ‖r‖₂ ≈ 0.339116.

**Sistema** («S8-30/09 pp. 6-7»): A = [[1, 3], [3, −2], [−2, 5]] y b = (−1, 8, −8).

- x̂ = (65/33, −29/33) y r = (−1/3, 1/3, 1/3).
- ‖r‖₂ = √(1/3) ≈ 0.57735.
- Aᵀr = (0, 0).

### D.4 Métodos iterativos: de dónde salen las fórmulas

**Descomposición.** Se escribe A = D + L + U, con D diagonal y L y U estrictamente inferior y superior, **con los signos de A** (`descomponer`).

**Jacobi.**

- Ax = b ⇔ Dx = b − (L + U)x ⇔ x = −D⁻¹(L + U)x + D⁻¹b.
- La iteración es x⁽ᵏ⁾ = T_J x⁽ᵏ⁻¹⁾ + c, con **T_J = −D⁻¹(L + U)** y c = D⁻¹b.
- Por componentes, es la fórmula de `paso_jacobi`.

**Gauss-Seidel.**

- (D + L)x = b − Ux, de modo que **T_GS = −(D + L)⁻¹U** y c = (D + L)⁻¹b.
- Por componentes: al calcular xᵢ ya se conocen x₁⁽ᵏ⁾…xᵢ₋₁⁽ᵏ⁾, y se usan.

**SOR.**

- Se parte de la fórmula por componentes, xᵢ_nuevo = (1 − ω)xᵢ_viejo + (ω/aᵢᵢ)(bᵢ − Σ_{j<i} aᵢⱼxⱼ_nuevo − Σ_{j>i} aᵢⱼxⱼ_viejo).
- Se multiplica por aᵢᵢ y se pasan los términos nuevos a la izquierda: (D + ωL)x_nuevo = [(1 − ω)D − ωU]x_viejo + ωb.
- Por tanto, **T_ω = (D + ωL)⁻¹[(1 − ω)D − ωU]** y c = ω(D + ωL)⁻¹b.
- Con ω = 1 se obtiene T_GS. Es la fórmula estándar (Burden & Faires); no está en los PDF del curso.

**Ejemplo real: primeras iteraciones del sistema S** (10x − y + 2z = 6, −x + 11y − z = 25, 2x − y + 10z = −11), con x⁽⁰⁾ = 0:

| Método | x⁽¹⁾ | d₁ |
|---|---|---|
| Jacobi | (6/10, 25/11, −11/10) = (0.6, 2.272727, −1.1) | 2.272727 |
| Gauss-Seidel | x = 0.6; y = (25 + 0.6)/11 = 2.327273; z = (−11 − 2·0.6 + 2.327273)/10 = −0.987273 | 2.327273 |
| SOR (ω = 1.2) | x = 1.2·0.6 = 0.72; y = 1.2·(25 + 0.72)/11 = 2.805818; z = 1.2·(−11 − 1.44 + 2.805818)/10 = −1.156102 | 2.805818 |

Son los mismos valores que muestra la tabla de la aplicación. Con ε = 10⁻³ (criterio A):

| Método | Iteraciones | ρ(T) |
|---|---|---|
| Jacobi | 7 | 0.2679 |
| Gauss-Seidel | 4 | 0.0426 |
| SOR (ω = 1.2) | 6 | 0.2165 |

La solución exacta es x* = (217/208, 59/26, −225/208) ≈ (1.043269, 2.269231, −1.081731).

**Teorema de convergencia.**

- Sea e⁽ᵏ⁾ = x⁽ᵏ⁾ − x*. Como x* = Tx* + c, se cumple e⁽ᵏ⁾ = Te⁽ᵏ⁻¹⁾ = Tᵏe⁽⁰⁾.
- El error tiende a 0 **para todo** x⁽⁰⁾ si y solo si Tᵏ → 0, y eso ocurre si y solo si **ρ(T) = máx|λᵢ| < 1**.
- Cuanto menor es ρ, más rápido converge: el error se multiplica aproximadamente por ρ en cada iteración.
  - Gauss-Seidel en S: ρ ≈ 0.043, 4 iteraciones.
  - Jacobi en S: ρ ≈ 0.268, 7 iteraciones.

**Dominancia diagonal** (`dominancia_diagonal`).

- Si |aᵢᵢ| > Σ_{j≠i}|aᵢⱼ| en todas las filas, entonces ‖T_J‖∞ = máxᵢ Σ_{j≠i}|aᵢⱼ|/|aᵢᵢ| < 1.
- Como ρ(T) ≤ ‖T‖ para cualquier norma inducida, ρ(T_J) < 1 y Jacobi converge. Gauss-Seidel también, por un teorema del curso.
- Es una condición **suficiente, no necesaria**: Gauss-Seidel en S9-07/10 converge (ρ ≈ 0.935) sin dominancia.
- En S, las filas dan 10 > 3, 11 > 2 y 10 > 3: S es dominante.

**Las tres métricas no son lo mismo.**

- d_k pequeño no garantiza un error pequeño. Si ‖T‖ < 1, ‖x* − x⁽ᵏ⁾‖ ≤ ‖T‖/(1 − ‖T‖)·d_k, y con ‖T‖ cercano a 1 ese factor es enorme.
- r_k pequeño tampoco: ‖e‖/‖x*‖ ≤ κ(A)·‖r‖/‖b‖.
- Por eso la aplicación las muestra por separado y calcula e_k solo cuando hay una solución exacta de referencia.

### D.5 Radio espectral: el procedimiento implementado

**Paso 1: T exacta** (`matriz_iteracion`). Las inversas de D + L y D + ωL se calculan con **nuestro** Gauss-Jordan, con fracciones.

**Paso 2: polinomio característico** con Faddeev-LeVerrier (`polinomio_caracteristico`). Se calcula p(λ) = det(λI − T) = λⁿ + c₁λⁿ⁻¹ + … + cₙ con:

- M₀ = 0;
- para k = 1…n: Mₖ = T·Mₖ₋₁ + cₖ₋₁·I y cₖ = −tr(T·Mₖ)/k.

Usa solo productos, sumas y trazas, y con fracciones es **exacto**.

*Ejemplo 2×2 real:* A = [[4, 1], [2, 5]] con Jacobi.

- T_J = [[0, −1/4], [−2/5, 0]].
- k = 1: M₁ = I y c₁ = −tr(T) = 0.
- k = 2: M₂ = T·I + 0·I = T. Como T² = [[1/10, 0], [0, 1/10]], c₂ = −tr(T²)/2 = −1/10.
- Por tanto, p(λ) = λ² − 1/10 y ρ = √(1/10) ≈ 0.3162. Es lo que muestra la aplicación: «det(T − λI) = λ² − 1/10».

*Relación con la clase:* en 3×3 da lo mismo que Sarrus, det(T − λI) = −λ³ + tr(T)λ² − (Σ menores 2×2)λ + det(T). Lo verifica `test_faddeev_coincide_con_sarrus_3x3`. La pantalla escribe el polinomio con el signo de clase (`texto_polinomio_curso`), por ejemplo «−λ³ + 1/6λ + 1/40» para la Tarea II #4.

**Paso 3: raíces** (`raices`):

- Las **λ = 0** se extraen de forma exacta. Si cₙ = 0, λ divide a p.
- **Grado 1 o 2:** fórmula directa, con discriminante exacto (las raíces complejas aparecen si es negativo). Además, la decisión «todas |λ| < 1» se toma **exactamente** con Schur-Cohn: |c₂| < 1 y |c₁| < 1 + c₂.
  - En el ejemplo 2×2: |−1/10| < 1 y |0| < 9/10, así que converge con decisión exacta.
- **Grado ≥ 3:** Durand-Kerner (`durand_kerner`), que aproxima **todas** las raíces complejas a la vez:
  - zᵢ ← zᵢ − p(zᵢ) / Π_{j≠i}(zᵢ − zⱼ);
  - empieza en puntos distintos dentro del círculo |z| ≤ 1 + máx|cᵢ|, donde están todas las raíces;
  - se detiene cuando la corrección es < 10⁻¹² (relativa).
  - Es como Newton aplicado a cada raíz, «separándola» de las demás.

**Paso 4: verificaciones.**

- |p(λ)| debe ser ≈ 0 (relativo < 10⁻⁸).
- Σλ debe ser igual a la traza de T: el coeficiente c₁ = −Σλ.
- Se avisa si hay raíces casi repetidas o si Durand-Kerner no convergió.

**Paso 5: conclusión** (`concluir`):

- Si p(1) = 0 o p(−1) = 0 **exactamente**, ρ ≥ 1 y la respuesta es «no converge», con decisión exacta.
- Si hay una decisión exacta de Schur-Cohn, se usa esa.
- Si el cálculo no es fiable o |ρ − 1| < 10⁻⁹ (10⁻⁶ con raíces casi repetidas) → INDETERMINADO.
- En otro caso, se compara ρ con 1.

**Ejemplo real con raíces complejas** (S9-07/10, Jacobi): A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]].

- T_J = [[0, −1, −1], [−1, 0, −2/3], [1, 2/3, 0]].
- det(T − λI) = −λ³ − (4/9)λ + 4/3.
- Raíces: 0.9668 y −0.4834 ± 1.0703i. El par complejo tiene módulo 1.1744.
- ρ ≈ 1.174 > 1: **no converge**. La hoja de clase concluye ρ = 0 porque omite el término 4/3.
- El método de la potencia fallaría aquí, porque el autovalor dominante es un par complejo.

**Ejemplo con decisión exacta** (S9-07/10, SOR con ω = 6/5, el ω por defecto).

- Polinomio: λ³ + (11/125)λ² − (113/125)λ + 1/125. Se comprueba que p(−1) = −1 + 11/125 + 113/125 + 1/125 = 0.
- Por tanto λ = −1 es autovalor, ρ ≥ 1 y el método no converge.
- La aplicación lo informa: «λ = -1 es autovalor exacto de T: ρ(T) ≥ 1».

### D.5b Lo que enseña la docente y cómo lo seguimos en el radio espectral

En S9-07/10 p. 4 la docente calcula det(T − λI) por Sarrus para T_J = [[0, −1, −1], [−1, 0, −2/3], [1, 2/3, 0]]. Nuestro `desarrollo_sarrus` hace el mismo desarrollo:

- tr(T) = 0;
- Σ menores 2×2 = (0 − 1) + (0 + 1) + (0 + 4/9) = 4/9;
- det(T) por Sarrus = 4/3.

Por tanto, det(T − λI) = −λ³ + 0·λ² − (4/9)λ + 4/3.

La hoja de clase escribe −λ³ − (4/9)λ: **omite el término 4/3**, porque los productos +2/3 y +2/3 de la regla de Sarrus se tacharon como si se cancelaran. Así concluye ρ = 0. La aplicación muestra el desarrollo completo, y ρ ≈ 1.174 > 1.

Si la docente pregunta, se enseñan en la pantalla los tres números (tr, Σ menores, det), que se pueden comprobar a mano.

### D.6 CSR (incentivo de matrices dispersas)

La tridiagonal 3×3 [[4, −1, 0], [−1, 4, −1], [0, −1, 4]] se guarda así:

- `valores = [4, −1, −1, 4, −1, −1, 4]`;
- `columnas = [0, 1, 0, 1, 2, 1, 2]`;
- `inicio = [0, 2, 5, 7]`: la fila i ocupa las posiciones inicio[i]…inicio[i+1]−1.

La memoria es 2·nnz + n + 1 números en lugar de n², y cada iteración cuesta O(nnz) en lugar de O(n²).

---

### D.7 Precondicionamiento diagonal: qué cambia y qué no

**Lo que dice la lámina** (S9-05/10 pp. 21-22, diapositivas 17-18):

- M = D = diag(aᵢᵢ) y se resuelve M⁻¹Ax = M⁻¹b, que tiene la misma solución;
- un buen precondicionador busca κ(B) < κ(A) y ρ(B) < ρ(A).

**Demostración de que Jacobi no cambia.**

- En B = D⁻¹A la diagonal es 1 y la parte fuera de la diagonal es D⁻¹(L + U).
- Entonces T̃_J = −I⁻¹·D⁻¹(L + U) = T_J y c̃ = I⁻¹·D⁻¹b = D⁻¹b = c.
- Para GS: (I + D⁻¹L)⁻¹ = (D⁻¹(D + L))⁻¹ = (D + L)⁻¹D, así que T̃_GS = −(D + L)⁻¹D·D⁻¹U = −(D + L)⁻¹U = T_GS.
- SOR es análogo.
- Intuición: Jacobi, GS y SOR ya dividen cada ecuación entre su aᵢᵢ, así que dividirla antes no cambia nada.

**Ejemplo real de la aplicación** (tridiagonal [−1, 4, −1] de la lámina):

| | Original | Con M = D |
|---|---|---|
| κ∞ | 30/11 | 30/11 (B = A/4) |
| Jacobi | 7 iteraciones | 7 (idénticas) |
| GS | 5 | 5 |
| SOR (ω = 1.2) | 7 | 7 |
| Richardson | no converge (ρ(I − A) ≈ 4.618) | converge (ρ = ρ(T_J) ≈ 0.405) |

(Iteraciones con ε = 10⁻³ y x⁽⁰⁾ = 0.)

**Dónde sí hay efecto:**

- κ cuando la diagonal no es uniforme. Por ejemplo, [[100, 1], [1, 1/50]] pasa de κ∞ = 10201 a 5202.
- El residuo r̃ = D⁻¹r.
- **Richardson**, x ← x + (b − Ax): precondicionado se convierte en x ← x + D⁻¹(b − Ax), que es exactamente Jacobi.

**Valores propios.** μ(B) = 1 − λ(T_J), así que «agrupados cerca de 1» significa ρ(T_J) pequeño.

**Discrepancia con la lámina.** La diapositiva 19 muestra que Jacobi mejora con M = D. Eso no puede pasar: la aplicación lo demuestra en vivo con la columna «¿T y c idénticas? Sí (exacto)».

### D.8 Qué es de clase y qué es extensión (Cat. A/B/C/D)

En la cabecera de cada módulo hay distintivos «Cat.»; al pasar el cursor se ve la página del PDF. La tabla completa está en `docs/auditoria_textos_profesora.md`.

| Cat. | Significado | Ejemplos |
|---|---|---|
| **A** | Visto en clase | OEF, Gauss, Gauss-Jordan, inversa [A\|I], κ en 5 pasos, sistema normal, Cramer, Jacobi, GS, SOR, x⁽⁰⁾ = bᵢ/aᵢᵢ, dominancia, T_J, T_GS, det(T − λI) por Sarrus |
| **B** | Exigido por el enunciado | Norma ∞ y escala 10/100; resolver el sistema normal con nuestro Gauss; ‖r‖₂; tabla, motivo, comparación y gráfica del Módulo IV; detección de pivotes problemáticos |
| **C** | Extensión o incentivo (no visto en clase) | Pivoteo parcial; T de SOR; **Faddeev-LeVerrier**; **Durand-Kerner**; **Richardson**; CSR; M = D; CSV; gráfica 3D y control gestual |
| **D** | Sin respaldo | Ninguno |

**Si preguntan «¿esto lo vimos en clase?»:**

- Si el distintivo es Cat. A, citar la página del PDF.
- Si es Cat. C, decir que es una extensión, rotulada así en la aplicación, y explicar por qué hace falta. Por ejemplo, Sarrus solo sirve para 3×3 y Faddeev-LeVerrier da el mismo polinomio para cualquier n.

**Notación de la profesora:** los pasos de Gauss muestran primero «−2F₁ + F₂», «(−1/3)F₃» y «F₁ ↔ F₂», y el resultado cierra con «Sol = {(1/3, 4, 5/3)}» y «3 ecuaciones no nulas, 3 incógnitas → solución única», igual que su manuscrito de S6-16/09 p. 29.

### D.9 Control gestual de la gráfica 3D (MediaPipe, en Python)

**Qué es:** un complemento de experiencia de usuario (Cat. C). No calcula nada del álgebra; solo cambia desde dónde se mira la gráfica de planos del Módulo I.

**Cadena:**

1. `cv2.VideoCapture` lee un fotograma en memoria.
2. MediaPipe Hand Landmarker devuelve 21 puntos por mano.
3. Las reglas de `gestos/interpretacion.py` deciden el gesto.
4. `gestos/movimiento.py` convierte el movimiento en una cámara orbital: eye = r(cos φ cos θ, cos φ sin θ, sin φ).
5. Un canal local (127.0.0.1) lleva esos números a la gráfica.

**Preguntas probables:**

- **¿Se graba o se envía la imagen?** No. El fotograma se procesa y se descarta (`del fotograma`). Al navegador solo llegan 9 números. El servidor solo escucha en 127.0.0.1 y pide un token.
- **¿Por qué no se confunde un puño con una pinza?** Todo se mide en «unidades de palma». En la pinza, la punta del índice queda fuera de la palma; en el puño, no.
- **¿Por qué no tiembla?** Por cuatro mecanismos:
  - suavizado exponencial (α = 0,35);
  - zona muerta acumulada;
  - antirrebote: tiempo mínimo para cada gesto;
  - histéresis: la pinza entra con un umbral y sale con otro 1,5 veces mayor.
- **¿Qué pasa si se cambia de módulo?** El panel envía un latido cada 0,5 s. Sin latido durante 4 s, el hilo libera la cámara.
- **¿Por qué hay JavaScript?** Se midió que, sin él, Streamlit actualiza la gráfica 1-3 veces por segundo y vuelve a montarla. Con el puente de unas 50 líneas llega a ~30 veces por segundo sin trabarse. Todo lo demás es Python (ver `portabilidad_java_python.md`).
- **Rendimiento medido:**
  - ~32 fotogramas/s;
  - detección de ~18-28 ms;
  - CPU de alrededor de 1 núcleo de 12 hilos;
  - memoria estable durante 3 min.

**Antes de la defensa:** probar con la mano real en el equipo y con la luz del aula. Si algo falla, se usa el ratón: la gráfica funciona igual.

## E. Preguntas de defensa, con respuestas

Cada respuesta se puede comprobar en el código (se indica dónde) o con la aplicación.

**Generales y de diseño**

1. **¿Qué bibliotecas usaron y para qué? ¿Usaron alguna que resuelva los métodos?**
   - El núcleo (`algebra/`) solo usa la biblioteca estándar: `fractions`, `math`, `cmath` y `dataclasses`.
   - Streamlit sirve para la interfaz, y Plotly y Matplotlib para las gráficas, como lo permite OFICIAL p. 1, y están documentadas en `docs/herramientas_y_bibliotecas.md`.
   - Ningún archivo importa NumPy, SciPy ni SymPy. NumPy solo se instala porque lo necesitan internamente Streamlit, Plotly y Matplotlib.

2. **¿Por qué usaron fracciones en unos módulos y `float` en otros?**
   - Con `Fraction`, Gauss, la inversa, κ y los mínimos cuadrados son exactos. Un pivote es 0 solo si es realmente 0, así que la clasificación y la detección de singularidad no dependen de redondeos.
   - Los iterativos son aproximaciones que se detienen por tolerancia. Con fracciones, los denominadores crecerían en cada iteración. Las raíces de un polinomio de grado ≥ 3 en general no son racionales.
   - La lectura usa `Fraction(texto)`, de modo que «0.1» es exactamente 1/10 (`leer_numero`).

3. **¿Cómo está organizado el código y por qué así?**
   - Hay tres capas: `algebra/` (cálculos), `interfaz/` (pantallas) y `visualizacion/` (dibujos).
   - El núcleo no depende de la interfaz. Por eso se prueba solo (295 pruebas) y la interfaz no repite cálculos.
   - En los iterativos, cada método es una función `paso_*` y el bucle de parada es uno solo (`_ejecutar`), para no triplicar la lógica.

4. **¿Cómo saben que los resultados son correctos?**
   - Hay 295 pruebas con valores esperados calculados aparte: a mano, con Cramer, con la adjunta, con fórmulas cerradas o con teoremas.
   - La auditoría aleatoria (`auditoria/`) compara miles de casos con oráculos escritos aparte (Leibniz, adjunta, Cramer, una implementación separada de las iteraciones, Gelfand) y da 0 fallos.
   - La aplicación además se autoverifica:
     - b − Ax = 0 en el Módulo I;
     - A·A⁻¹ = I en el Módulo II;
     - Aᵀr = 0 en el Módulo III;
     - Σλ = traza(T) en el radio espectral.
   - **No** se usaron los resultados de las láminas como referencia, porque varios son incorrectos.

5. **¿Qué pasa si el usuario escribe algo inválido?**
   - `leer_numero` lanza `ErrorEntrada` con la posición, por ejemplo «el elemento (2, 2) de la matriz A "x" no es un número válido».
   - La interfaz lo muestra con `st.error`.
   - En el Módulo IV, `ejecutar` nunca lanza excepciones: devuelve `ENTRADA_INVALIDA` con su mensaje.
   - La aplicación no se cierra en ningún caso (validaciones de OFICIAL p. 3).

**Módulo I**

6. **¿Cómo decide el programa si hay solución única, infinitas o ninguna?**
   - Por rangos. `rango_A` es el número de pivotes encontrados por `_escalonar`. `_rango_aumentada` suma 1 si existe una fila [0 … 0 | c] con c ≠ 0.
   - rango(A) < rango([A|b]) → inconsistente.
   - Iguales y = n → única.
   - Iguales y < n → infinitas, con n − rango variables libres.

7. **¿Qué hace el programa cuando un pivote es cero?**
   - `_buscar_pivote` busca debajo una fila con elemento ≠ 0 y la intercambia. El paso queda registrado con el motivo, y el signo del determinante cambia.
   - Si toda la columna (desde la fila actual) es 0, esa columna no tiene pivote y su variable es libre.
   - Ejemplo precargado: «Pivote nulo», con F1 ↔ F2.

8. **¿Qué es un pivote «numéricamente problemático» si usan fracciones exactas?**
   - Es un aviso técnico: |pivote| < 10⁻¹⁰·máx|aᵢⱼ| (`UMBRAL_PIVOTE_PEQUENO`).
   - Con fracciones el resultado sigue siendo exacto, pero en punto flotante ese pivote amplificaría los errores de redondeo.
   - Se avisa porque el enunciado pide detectar esos pivotes, y no se altera el resultado.

9. **¿Cómo se obtiene la solución general cuando hay infinitas soluciones?**
   - La solución particular xₚ se obtiene con `_sustitucion_atras`, dando el valor 0 a las variables libres.
   - Para cada libre j se resuelve el sistema **homogéneo** (lado derecho 0) con esa libre igual a 1 y las demás iguales a 0. Esa es la dirección vⱼ.
   - Entonces x = xₚ + Σ tⱼvⱼ. Funciona porque A(xₚ + Σtⱼvⱼ) = b + 0.

10. **¿Cómo calculan el determinante y por qué es correcto?**
    - det = (−1)^(número de intercambios) · Π pivotes.
    - Sumar a una fila un múltiplo de otra no cambia el determinante; cada intercambio lo cambia de signo; y el determinante de una triangular es el producto de su diagonal.
    - En Gauss-Jordan el pivote se guarda **antes** de normalizar la fila.
    - Si falta un pivote, det = 0.

**Módulo II**

11. **¿Qué es κ∞(A) y qué indica?**
    - κ∞ = ‖A‖∞‖A⁻¹‖∞, donde ‖A‖∞ es la mayor suma de valores absolutos por fila.
    - Es el factor máximo por el que se puede amplificar el error relativo de b en la solución: ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖ (demostración en D.2).
    - La escala del proyecto (< 10, < 100, ≥ 100) es la orientativa del enunciado, no una frontera universal.

12. **En un ejemplo la amplificación observada fue menor que κ. ¿Está mal?**
    - No: κ es el **peor caso** sobre todas las direcciones de Δb.
    - En «S7-21/09 p. 19» la amplificación es 0.04/0.025 = 1.6, menor que κ = 3.2.
    - En «A = I + 10J» con Δb = (1, −1, 1) se alcanza exactamente κ = 41, porque esa Δb es la dirección más desfavorable.

13. **¿Qué diferencia hay entre una matriz singular y una mal condicionada?**
    - Una singular (det = 0) no tiene inversa: κ no está definido y el sistema no tiene solución única. La aplicación devuelve `MATRIZ_SINGULAR`.
    - Una mal condicionada es invertible, con solución única, pero muy sensible. Ejemplo: [[1, 1], [1, 1.0001]], con κ ≈ 40004.

14. **¿Cómo interpretan la perturbación porcentual?**
    - Δbᵢ = (p/100)·bᵢ en cada componente (`construir_delta_b`). Con un solo p, ‖Δb‖∞/‖b‖∞ = |p|/100 exactamente.
    - Límite: una componente bᵢ = 0 no se perturba. Para eso está el modo absoluto.

**Módulo III**

15. **¿Por qué se resuelven las ecuaciones normales y no Ax = b directamente?**
    - Con m > n, Ax = b en general es inconsistente.
    - Minimizar ‖b − Ax‖² lleva a AᵀAx = Aᵀb (gradiente igual a 0) o, geométricamente, a r ⟂ Col(A).
    - AᵀA es n×n y se resuelve con **nuestro** `resolver_gauss`, como pide el enunciado.

16. **¿Qué significa la comprobación Aᵀr = 0?**
    - Que el residuo es perpendicular a todas las columnas de A, de modo que Ax̂ es la proyección ortogonal de b sobre Col(A).
    - Es la propiedad que **caracteriza** a la solución de mínimos cuadrados.
    - Como el cálculo es exacto, sale (0, 0) exactamente.

17. **¿Cuándo falla el ajuste y qué hace la aplicación?**
    - Si las columnas de A son dependientes, AᵀA es singular y x̂ no es único: se informa y no se presenta ninguno.
    - En el ajuste de una recta: con menos de 2 puntos, con todos los x iguales (recta vertical) o con un número distinto de x y de y, se lanza `ErrorAjuste` con su mensaje.

**Módulo IV**

18. **¿Cuál es la diferencia entre Jacobi, Gauss-Seidel y SOR en el código?**
    - `paso_jacobi` escribe en un vector nuevo y usa solo x⁽ᵏ⁻¹⁾.
    - `paso_gauss_seidel` escribe sobre la misma lista, así que para j < i ya usa los valores nuevos.
    - `paso_sor` calcula el valor de Gauss-Seidel y lo mezcla: (1 − ω)·anterior + ω·GS. Con ω = 1 es idéntico a Gauss-Seidel (prueba P15).

19. **¿Qué criterio de parada usan y qué error muestra la tabla?**
    - El usuario elige:
      - A: d_k = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε (por defecto, el que más usa la docente);
      - B: r_k = ‖b − Ax⁽ᵏ⁾‖∞ < ε;
      - C: N iteraciones fijas.
    - La desigualdad es estricta. La tabla muestra d_k y r_k y rotula cuál es el «(criterio de parada)».
    - La norma ∞ es el **máximo**. Algunos manuscritos suman las diferencias (eso es la norma 1).

20. **Si se alcanza el máximo de iteraciones, ¿el método diverge?**
    - No necesariamente: solo significa que no se cumplió el criterio en k_max iteraciones. Puede converger lentamente.
    - Ejemplo: Gauss-Seidel en S9-07/10 tiene ρ ≈ 0.935 < 1 (converge), pero no llega a ε = 10⁻³ en 50 iteraciones.
    - Por eso el mensaje es «máximo de iteraciones sin satisfacer el criterio».
    - Tampoco un desbordamiento (`ERROR_NO_FINITO`) se presenta como demostración de divergencia.
    - La convergencia se decide con ρ(T).

21. **¿Por qué el criterio C «no demuestra convergencia»?**
    - Porque hacer N iteraciones no dice nada de si x⁽ᴺ⁾ está cerca de la solución.
    - La aplicación las hace, registra d y r y lo advierte (`N_COMPLETADAS`).

22. **¿La dominancia diagonal garantiza convergencia? ¿Y si no se cumple?**
    - Si A es estrictamente dominante por filas, ‖T_J‖∞ < 1, de modo que ρ < 1 y Jacobi converge. Gauss-Seidel también.
    - Es suficiente, no necesaria. Si no se cumple, no se concluye nada y hay que mirar ρ(T): por ejemplo, Gauss-Seidel en S9-07/10 converge sin dominancia.
    - Como la docente en la Tarea II, se puede **reordenar las ecuaciones**. La aplicación busca ese orden (`reordenamiento_dominante`) y lo sugiere, pero no lo aplica sola: cambiaría el sistema que dio el usuario.

23. **¿Cómo calculan el radio espectral sin bibliotecas?**
    1. T exacta con nuestro Gauss-Jordan.
    2. Polinomio det(λI − T) con Faddeev-LeVerrier (Mₖ = TMₖ₋₁ + cₖ₋₁I, cₖ = −tr(TMₖ)/k), que es exacto y coincide con Sarrus en 3×3.
    3. Raíces: λ = 0 exactas, fórmula cuadrática para grado ≤ 2 y Durand-Kerner para grado ≥ 3.
    4. ρ = máx|λ|, verificado con |p(λ)| ≈ 0 y Σλ = traza.
    - Archivo: `algebra/modulo_IV_iterativos/espectral.py`.

24. **¿Por qué no usaron el método de la potencia?**
    - Porque falla cuando el autovalor de mayor módulo es un par complejo, o hay dos de igual módulo y signo opuesto (±μ).
    - Eso ocurre en los ejemplos del curso. En S9-07/10 Jacobi, ρ = 1.174 viene de un par complejo.
    - Durand-Kerner encuentra todas las raíces, también las complejas.

25. **¿Qué pasa si ρ está muy cerca de 1 o hay autovalores repetidos?**
    - Con raíces múltiples, Durand-Kerner pierde precisión (≈10⁻⁸ en una doble, ≈10⁻⁵ en una triple).
      - Si aun así converge (lo habitual con una doble), la aplicación avisa y amplía la banda de duda a 10⁻⁶.
      - Si no converge (lo habitual con una triple), marca el resultado como no fiable y concluye «indeterminado».
    - Si |ρ − 1| < 10⁻⁹ (10⁻⁶ con raíces casi repetidas), también da «indeterminado».
    - Nunca da una conclusión falsa. Cuando puede decidir de forma exacta, decide: grado ≤ 2 con Schur-Cohn, o p(±1) = 0.

26. **¿Por qué A singular implica que ningún método converge?**
    - T = I − M⁻¹A, con M = D (Jacobi), D + L (GS) o (D + ωL)/ω (SOR).
    - Si Av = 0 con v ≠ 0, entonces Tv = v: λ = 1 es autovalor y ρ ≥ 1.
    - La aplicación lo detecta exactamente con p(1) = 0 (`radio_espectral`).

27. **¿Qué es la comparación «homogénea»?**
    - Que los tres métodos usan el mismo sistema, el mismo x⁽⁰⁾, el mismo criterio, la misma ε y el mismo k_max (o N). Solo cambia el método, y SOR añade su ω.
    - `comparar_metodos` lo comprueba campo por campo y avisa si algo difiere.
    - El número de iteraciones solo es comparable entre métodos que terminaron por el mismo motivo.

28. **¿Qué es «e final» en la tabla de comparación?**
    - e = ‖x⁽ᵏ⁾ − x*‖∞, donde x* es la solución **exacta** obtenida con nuestro Gauss.
    - Es el error verdadero; no es d ni r.
    - Es exactamente la definición de la lámina S9-05/10 p. 17: columna «Error final (‖x⁽ᵏ⁾ − x‖∞)». La tabla muestra además d y r.

29. **¿Qué ventaja tiene el formato CSR y cómo saben que da lo mismo?**
    - Guarda solo los nnz no nulos (`valores`, `columnas`, `inicio`). Memoria O(nnz), y cada iteración O(nnz) en lugar de O(n²).
    - Los pasos CSR recorren los no nulos en el mismo orden de columnas que los densos. Sumar productos por cero no cambia nada en punto flotante, así que las iteraciones son idénticas bit a bit (prueba en `test_dispersas`).

30. **¿Qué es el precondicionamiento diagonal y qué efecto tiene en su aplicación?**
    - Se resuelve D⁻¹Ax = D⁻¹b, con M = D, como en la lámina. Archivo: `algebra/modulo_IV_iterativos/precondicionamiento.py`.
    - Para Jacobi, GS y SOR **no cambia nada**: T̃ = T y c̃ = c (demostración en D.7). La aplicación lo comprueba con fracciones y lo muestra en la tabla.
    - Sí cambia κ (si la diagonal no es uniforme), el residuo y Richardson, que precondicionado se convierte en Jacobi.
    - Si la docente pregunta por qué no coincide con la diapositiva 19, se muestra la demostración y la tabla en vivo.

31. **En mínimos cuadrados, la docente usó Cramer. ¿Por qué ustedes usan Gauss?**
    - El enunciado exige resolver las ecuaciones normales «con un método directo ya implementado», que es nuestro `resolver_gauss`.
    - Aun así, la aplicación muestra el procedimiento de clase completo: det([A|b]) ≠ 0 y Cramer (`cramer`), y comprueba que da exactamente lo mismo.
    - Ejemplo del manuscrito: 715/363 = 65/33 y −319/363 = −29/33.

32. **¿Cómo comprueban que b no está en el espacio columna de A?**
    - En general, con el rango: `resolver_gauss(A, b)` da INCONSISTENTE.
    - Si m = n + 1, también como en clase: det([A|b]) ≠ 0 implica que [A|b] tiene rango n + 1, así que b no es combinación lineal de las columnas.

33. **¿Su polinomio característico es el mismo que el de Sarrus?**
    - Sí, en 3×3 son idénticos.
    - La aplicación muestra tr(T), la suma de los menores principales 2×2 y det(T) (Sarrus), arma −λ³ + tr·λ² − Σmen·λ + det y comprueba que coincide con Faddeev-LeVerrier.
    - Faddeev-LeVerrier se usa porque también vale para n > 3.

34. **¿Qué es Richardson y por qué aparece en la pestaña de precondicionamiento?**
    - Es la iteración x⁽ᵏ⁾ = x⁽ᵏ⁻¹⁾ + (b − Ax⁽ᵏ⁻¹⁾), con T_R = I − A.
    - No es uno de los métodos del enunciado ni se vio en clase. Se incluye porque es el método más simple sobre el que M = D tiene efecto: con M = D se convierte en Jacobi.
    - Así se documenta un efecto real del precondicionador, en vez de inventar uno.
    - **Si la profesora pregunta «¿eso lo vimos?»:** «No, profesora. Es una extensión, y la aplicación la rotula como "Extensión no vista en clase". La usamos solo para mostrar el efecto de M = D, porque en Jacobi, Gauss-Seidel y SOR la matriz de iteración no cambia.»
    - Demostración en una línea: T̃_R = I − D⁻¹A = I − D⁻¹(D + L + U) = −D⁻¹(L + U) = T_J.

35. **¿Cómo está organizado el código? Muéstreme dónde está Jacobi.**
    - `algebra/` es el núcleo y tiene una carpeta por módulo: `modulo_I_sistemas/` … `modulo_IV_iterativos/`. Lo común está en `algebra/compartido/`.
    - Jacobi: `algebra/modulo_IV_iterativos/metodos.py`, función `paso_jacobi`. El bucle y la parada están en `ejecucion.py` (`ejecutar`).
    - La interfaz (`interfaz/modulos/…`) solo lee los datos, llama al núcleo y muestra el resultado; las gráficas (`visualizacion/`) solo dibujan.

---

## F. Cómo ejecutar y demostrar el proyecto

### Instalación (Windows)

1. Instalar **Python 3.11 o superior** desde python.org, marcando «Add python.exe to PATH».
2. Descomprimir el ZIP. Contiene una sola carpeta, `Grupo01-IF0012-Proyecto-IIC`.
3. Doble clic en **`ejecutar.bat`**.
   - La primera vez crea `.venv` e instala Streamlit 1.66.1 y Matplotlib 3.11.2 (requiere internet y tarda unos minutos).
   - Después abre `http://localhost:8501`.
   - Para cerrar: cerrar la ventana negra.
4. Alternativa desde la terminal:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

5. Pruebas: `ejecutar_pruebas.bat` o `.venv\Scripts\python -m unittest`. Deben salir **295 pruebas OK**.
6. Auditoría (opcional, unos 20 s): `.venv\Scripts\python auditoria\auditoria_directos.py .` y `.venv\Scripts\python auditoria\auditoria_iterativos.py .` (y `auditoria_precondicionamiento.py`). Deben dar «fallos 0».

> **Antes de la defensa:** cada integrante debe hacer la instalación **en su propia computadora** al menos una vez. La primera instalación necesita internet; no la dejen para el aula.

### Formato de entrada

Cada matriz y cada vector tiene un **editor interactivo** con dos pestañas:

- **Editor:** rejilla de celdas con «＋/－ Fila» y «＋/－ Columna», selectores de dimensión y, en «⋯ Más», las opciones Identidad, Ceros, Limpiar y Restaurar el ejemplo.
- **Pegar:** se escribe o pega el texto; se aceptan espacios, tabulaciones, «;» o «, » como separadores.

Debajo de cada editor una etiqueta indica si los datos están listos, si faltan valores o en qué celda hay un error. Si las dimensiones no son compatibles (por ejemplo, b con otra longitud o una A no cuadrada en el Módulo IV), el botón de cálculo queda bloqueado y se explica por qué.


- Una fila por línea, con los números separados por espacios.
- Se aceptan `3`, `-2.5`, `2,5`, `1/3` y `1e-3`.
- Cada módulo tiene «Cargar un ejemplo».

### Guion de demostración (con los resultados que deben aparecer)

Los parámetros por defecto del Módulo IV son: x⁽⁰⁾ = vector cero, criterio A, ε = 1e-3, k_max = 50 y ω = 1.2.

**Módulo I** (unos 2 minutos)

1. Ejemplo «Pivote nulo: requiere intercambio de filas», método Gauss → **Solución única** x = (1, 1, 1), det = −1.
   - En «Procedimiento paso a paso» se ve F1 ↔ F2 con el motivo «el elemento (1, 1) es 0».
   - La verificación b − Ax es (0, 0, 0).
2. Ejemplo «Infinitas soluciones» → rango(A) = rango([A|b]) = 2 < 3. x = (1/2, 1/2, 0) + t₁(−1/2, −1/2, 1).
3. Ejemplo «Sistema inconsistente» → la fila queda como [0 0 0 | c], con rango(A) = 2 < rango([A|b]) = 3.
4. Abrir «Interpretación geométrica»: planos que se cortan en un punto, en una recta o sin punto común. **Rotar la figura con el ratón** y pasar el cursor sobre la solución para ver sus coordenadas.
5. Otros resultados esperados:

   | Ejemplo | Resultado |
   |---|---|
   | S6-16/09 p. 29 | (1/3, 4, 5/3), det = 3 |
   | S6-14/09 p. 29 | (19/20, −5/4, −7/20), det = −20. La lámina da (1/2, −1, −1), que no cumple la 2.ª ecuación |
   | LU de clase S6-16/09 p. 35 | (1, 1, 2), det = −16 |
   | 2 incógnitas | (2, 1), det = −3 |

**Módulo II** (unos 2 minutos)

1. «S7-21/09 p. 20 — bien condicionada» → κ∞ = 25/11 ≈ 2.27, sensibilidad **baja**. Con Δb = (0.01, −0.01): x = (1/11, 7/11) y x̃ = (26/275, 139/220).
   - ‖Δb‖/‖b‖ = 0.005, ‖Δx‖/‖x‖ ≈ 0.00714 y cota ≈ 0.01136: la cota se cumple.
2. «S7-21/09 p. 15 — mal condicionada» → κ∞ ≈ 40004, sensibilidad **alta**. x = (1, 1) pasa a x̃ = (0, 2): error relativo del 100 % con un cambio de 5·10⁻⁵ en b.
3. «A = I + 10J» → κ∞ = 41, sensibilidad **moderada**. La amplificación es exactamente 41, el peor caso.
4. Matriz singular: escribir `1 2` / `2 4` → mensaje de A singular, sin κ.

**Módulo III** (unos 2 minutos)

1. Pestaña «Sistema sobredeterminado», «S8-30/09 pp. 6-7» → sistema sobredeterminado 3×2.
   - x̂ = (65/33, −29/33), r = (−1/3, 1/3, 1/3), ‖r‖₂ ≈ 0.57735 y Aᵀr = (0, 0).
   - Abrir «Verificación con el procedimiento de clase»: det([A|b]) = −11, Cramer 363, 715 y −319, que coincide exactamente. Son los mismos números del manuscrito de la docente.
2. Pestaña «Ajuste lineal», «y = 0.75x + 1.2» → **y = 3/4 x + 6/5**, ‖r‖₂ ≈ 0.339. La gráfica muestra los puntos, la recta y los residuos.
3. «Columnas dependientes» → AᵀA singular; no se presenta ningún x̂.

**Módulo IV** (unos 3 minutos)

1. Ejemplo «10x−y+2z=6», pestaña «Ejecutar un método», Jacobi → «Criterio satisfecho: d_7 = 0.000378139 < ε = 0.001».
   - x ≈ (1.043187, 2.269277, −1.081786).
   - Cambiar al criterio B con SOR → termina en k = 7 con r_7 ≈ 8.79·10⁻⁴.
2. Pestaña «Comparar métodos» → «Experimento homogéneo».
   - Jacobi: 7 iteraciones; Gauss-Seidel: 4; SOR (ω = 1.2): 6. ρ = 0.268, 0.043 y 0.217.
   - Mostrar la gráfica: por defecto e_k, el «error final» de la lámina. Pasar el cursor por una iteración para ver los tres valores a la vez, arrastrar para ampliar una zona y doble clic para volver.
3. Pestaña «Convergencia» con el mismo ejemplo → la matriz es dominante (10 > 3, 11 > 2, 10 > 3). Se ven T, el polinomio con su desarrollo por Sarrus y ρ_J ≈ 0.2679 < 1.
4. Ejemplo «S9-07/10 — Jacobi no converge»:
   - Convergencia con Jacobi → polinomio −λ³ − 4/9λ + 4/3, par complejo y ρ ≈ 1.174 > 1: **no converge**.
   - Ejecutar Jacobi → «máximo de iteraciones sin satisfacer el criterio».
   - Gauss-Seidel en el mismo ejemplo → ρ ≈ 0.935 < 1: converge, pero lentamente (no llega en 50 iteraciones).
5. Pestaña «Precondicionamiento diagonal» con el ejemplo «Tridiagonal dispersa» → B = A/4, κ igual, Jacobi, GS y SOR «Sí (exacto)» e iteraciones idénticas; Richardson no converge sin precondicionar y converge con M = D.
6. Reordenamiento: escribir A = `-1 4 -1` / `0 -1 3` / `4 -1 0` y b = `10 10 15`, y pulsar «Analizar convergencia». La aplicación avisa del a₃₃ = 0 y propone el orden E3, E1, E2, que es dominante.
7. Otros radios esperados (Jacobi / GS / SOR ω = 1.2):

   | Ejemplo | ρ_J | ρ_GS | ρ_SOR |
   |---|---|---|---|
   | Tarea II #4/#5 | 0.4690 | 0.2210 | 0.2316 |
   | Tridiagonal | 0.4045 | 0.1636 | 0.2000 |
   | S8-30/09 p. 19 | 0.3025 | 0.1179 | 0.3437 |

### Caso no preparado: cómo actuar

1. Escribir los datos tal como los dicte la docente. Si hay un error de formato, la aplicación indica la celda.
2. Elegir el módulo según la pregunta: ¿resolver o clasificar?, ¿sensibilidad?, ¿más ecuaciones que incógnitas?, ¿iterar?
3. **Verificar en voz alta** con lo que muestra la aplicación:
   - b − Ax = 0 (I);
   - A·A⁻¹ = I (II);
   - Aᵀr = 0 (III);
   - en el IV, r_k pequeño y la verificación Σλ = traza.
4. En el Módulo IV, mirar primero la pestaña «Convergencia».
   - Si ρ ≥ 1 o hay un aᵢᵢ = 0, explicar por qué no conviene iterar (o reordenar las filas a mano).
   - Si la matriz no es dominante, recordar que eso no implica divergencia.
5. Si un resultado no coincide con el que espera la docente: la diferencia en los últimos decimales de los iterativos se explica por la tolerancia ε, no por redondeos. En los Módulos I a III los resultados son exactos y se pueden comprobar sustituyendo.

### Propuesta de reparto para profundizar

Esta propuesta la debe decidir el grupo. Cada uno **igual debe dominar los cuatro módulos**: la docente elige. El reparto es solo para que alguien prepare cada parte a fondo y se la explique a los demás.

| Integrante | Profundiza en | Lo mínimo que debe enseñar al resto |
|---|---|---|
| Elmer López Hernández | Módulo I | `_escalonar`, rangos, forma paramétrica, determinante e inversa |
| Derek Farley Noguera | Módulo II y la arquitectura | Demostración de la cota de κ, singular frente a mal condicionada, flujo de datos y validaciones |
| Daniel Córdoba Arias | Módulo III | Deducción de las ecuaciones normales, Aᵀr = 0, matriz de diseño, ajuste |
| Samir Sandoval Ramírez | Módulo IV | Los tres pasos, criterios y códigos, deducción de T, teorema de ρ, Faddeev-LeVerrier, Durand-Kerner y el precondicionador M = D |

---

## G. Limitaciones y decisiones técnicas

| Limitación o decisión | Qué pasa | Cómo defenderla |
|---|---|---|
| Autovalores **múltiples** | Durand-Kerner pierde precisión: ≈10⁻⁸ en una raíz doble (medido: 5·10⁻⁹ en 0.9 doble) y ≈10⁻⁵ en una triple (medido: 4·10⁻⁶ en 1/2 triple). **Raíz doble:** suele converger; la aplicación avisa «autovalores casi repetidos» y decide con una banda ampliada de 10⁻⁶. **Raíz triple o mayor:** normalmente no alcanza la precisión; se marca «no fiable» y la conclusión es **indeterminado**, aunque ρ esté lejos de 1 (por ejemplo, el 1/2 triple) | Es preferible no decidir a dar una conclusión falsa. Con raíces múltiples, hallar las raíces es un problema mal condicionado (error ≈ ε_máquina^(1/m)) |
| ρ muy cerca de 1 | Con \|ρ − 1\| < 10⁻⁹ (10⁻⁶ con raíces casi repetidas) → indeterminado | El error de redondeo de ρ es de ese orden; comparar ρ con 1 en `float` podría invertir la conclusión. Si hay decisión exacta (grado ≤ 2, p(±1) = 0), se usa |
| n > 8 en el radio espectral | No se calcula ρ (`N_MAX_ESPECTRAL`) | OFICIAL p. 2: «cuando el procedimiento estudiado lo permita». Para n grande quedan la dominancia y las iteraciones |
| Durand-Kerner y Faddeev-LeVerrier **no se vieron en clase** | Son una extensión | El polinomio coincide con Sarrus en 3×3, y las raíces se verifican con \|p(λ)\| y la traza. El alcance está pendiente con la docente (P-5) |
| Iterativos en `float` | Aproximaciones | Se detienen por tolerancia; las diferencias se justifican por ε (OFICIAL p. 3) |
| Criterio A predeterminado y norma ∞ | Distinto de algunos manuscritos que suman las diferencias | La norma ∞ es el máximo por definición; con la suma se calcula la norma 1 |
| No hay reordenamiento automático de filas | Una matriz no dominante se informa tal cual | Reordenar cambiaría el sistema que dio el usuario; se puede reordenar a mano |
| Perturbación porcentual por componente | bᵢ = 0 no se perturba | Con un único p, ‖Δb‖/‖b‖ = p/100 exactamente. Para bᵢ = 0 está el modo absoluto |
| Aviso de pivote pequeño (10⁻¹⁰) | Solo advierte | Es un umbral técnico: con fracciones el resultado es exacto |
| Precondicionador M = D sin efecto en Jacobi, GS y SOR | Es un hecho matemático, no un fallo; contradice la diapositiva 19 de S9-05/10 | Demostración en D.7; la aplicación compara T de forma exacta y muestra el efecto real (κ y Richardson) |
| Richardson y la sugerencia de reordenamiento | Son extras | Richardson solo se usa en la pestaña del precondicionador. El reordenamiento se sugiere y no se aplica |
| Gráficas sin pruebas automáticas de su contenido | Se revisaron como imagen | Las pruebas comprueban que se generan sin errores; el contenido se revisó manualmente |
| Instalación probada solo en un equipo | — | Cada integrante debe probarla en el suyo antes de la defensa |

**Errores de las láminas que la aplicación corrige** (detalle en `docs/guia_defensa.md` §6). Si la docente pregunta por qué la aplicación no coincide con una lámina, sustituyan la solución en el sistema y muestren el residuo. Por ejemplo, en S6-14/09 p. 29 la lámina da (1/2, −1, −1), y la 2.ª ecuación da 0.5 + 3 − 2 = 1.5 ≠ 4.

**Uso de IA:** está declarado en `docs/herramientas_y_bibliotecas.md` §4. Ni el enunciado ni el programa exigen una autorización previa: lo que se exige es declararlo y poder defender el trabajo. Si la docente pregunta, digan con honestidad para qué se usó y demuestren que entienden el código. No afirmen que ella lo autorizó expresamente.
