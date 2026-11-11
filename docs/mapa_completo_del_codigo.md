# Mapa completo del código de Ax

**Versión:** 11-nov-2026 (rama `feature/notacion-y-organizacion`).

Este documento es el punto de partida para estudiar el código. Responde a tres preguntas:

1. **Dónde está cada cosa:** árbol y tabla por carpeta.
2. **Cómo se conectan las piezas:** capas y dependencias.
3. **Cómo seguir un procedimiento de principio a fin:** un recorrido por módulo, con los archivos y funciones reales.

La explicación de **por qué** se organizó así está en [arquitectura.md](arquitectura.md).

---

## 1. Árbol del proyecto

```text
proyecto-algebra/
├── app.py                      ENTRADA: st.navigation con 5 páginas
├── paginas/                    1 archivo por página (Streamlit exige archivos): llaman a mostrar()
│
├── algebra/                    NÚCLEO MATEMÁTICO: Python puro, sin bibliotecas externas
│   ├── compartido/             usado por los 4 módulos
│   │   ├── matriz.py           validar formas, producto, transpuesta, normas ∞ y 2, residuo
│   │   ├── validacion.py       texto del usuario → números; ε, k_max, ω; mensajes de error
│   │   └── exactos.py          a_fraccion: cualquier número → Fraction exacta
│   ├── modulo_I_sistemas/directos.py               Gauss, Gauss-Jordan, inversa, determinante
│   ├── modulo_II_condicionamiento/condicion.py     κ∞, escala del enunciado, perturbación
│   ├── modulo_III_minimos/minimos.py               ecuaciones normales, residuo, Cramer, recta
│   └── modulo_IV_iterativos/
│       ├── metodos.py          UN paso de Jacobi, Gauss-Seidel, SOR (y Richardson)
│       ├── ejecucion.py        el bucle común: criterios A/B/C, tabla, motivo de parada
│       ├── convergencia.py     dominancia diagonal y reordenamiento
│       ├── matriz_iteracion.py A = D + L + U, D⁻¹, T y c (procedimiento de clase)
│       ├── polinomio_raices.py Faddeev-LeVerrier y Durand-Kerner (extensiones, Cat. C)
│       ├── espectral.py        ρ(T) y conclusión de convergencia
│       ├── comparacion.py      los 3 métodos en las mismas condiciones; error final
│       ├── dispersas.py        incentivo: formato CSR
│       └── precondicionamiento.py  incentivo: M = D (y Richardson, Cat. C)
│
├── interfaz/                   PRESENTACIÓN (Streamlit): no calcula nada
│   ├── navegacion.py           lista de páginas
│   ├── portada.py              página de inicio
│   ├── recursos/               marca.svg y estilo.css
│   ├── compartido/             piezas comunes a los 4 módulos
│   │   ├── editor.py           editor de matrices, vectores y puntos (con validación previa)
│   │   ├── componentes.py      leer_*_ui, mostrar_pasos, mostrar_interactiva
│   │   ├── formulas.py         LaTeX: matrices, fracciones, polinomio, despejes
│   │   ├── estilo.py           encabezados, chips, procedencia (Cat. A/B/C/D), escala de κ
│   │   ├── ejemplos.py         ejemplos precargados del curso
│   │   └── control_gestual.py  panel «Control con gestos» (usa gestos/)
│   └── modulos/                UNA VISTA POR MÓDULO
│       ├── modulo_I_sistemas.py
│       ├── modulo_II_condicionamiento.py
│       ├── modulo_III_minimos.py
│       └── modulo_IV_iterativos/
│           ├── principal.py               datos, parámetros comunes y pestañas
│           ├── pestana_ejecutar.py        un método: despejes, tabla, CSV, gráfica
│           ├── pestana_comparar.py        los 3 métodos, gráfica comparativa, barrido de ω
│           ├── pestana_convergencia.py    dominancia, pasos ①-⑤, ρ(T), autovalores
│           └── pestana_precondicionamiento.py
│
├── visualizacion/              GRÁFICAS: solo dibujan lo que calculó el núcleo
│   ├── interactivas.py         todas las gráficas Plotly de la aplicación
│   ├── datos_graficas.py       los datos que se dibujan, sin bibliotecas
│   ├── notacion.py             cada símbolo en LaTeX, HTML o Unicode
│   ├── tema.py                 colores
│   └── referencia_matplotlib.py  figura estática: oráculo de las pruebas
│
├── gestos/                     MediaPipe: control con la mano de la gráfica 3D
│   ├── captura.py  deteccion.py  mano.py  interpretacion.py
│   ├── movimiento.py  control.py  servidor.py
│   └── modelos/hand_landmarker.task
│
├── tests/                      pruebas unittest: una carpeta por módulo
├── auditoria/                  oráculos independientes (miles de casos aleatorios)
├── casos_prueba/               casos documentados: entrada, esperado, obtenido
├── docs/                       documentación (índice en docs/README.md)
├── herramientas/               solo desarrollo: generan las guías HTML (no van en el ZIP)
├── prototipos/                 prototipo PyVista descartado (decisiones_tecnicas.md)
└── empaquetar.py · ejecutar.bat · ejecutar_pruebas.bat · requirements*.txt
```

Cada carpeta importante tiene su propio `README.md`, con el detalle de sus archivos.

## 2. Qué buscar y dónde

| Busco… | Archivo | Función o clase principal |
|---|---|---|
| Gauss y Gauss-Jordan | `algebra/modulo_I_sistemas/directos.py` | `resolver_gauss`, `resolver_gauss_jordan` → `_resolver` → `_escalonar` |
| Elección del pivote | `directos.py` | `_buscar_pivote` (primer no nulo o pivoteo parcial) |
| Clasificación del sistema | `directos.py` | `_rango_aumentada` y el final de `_resolver` |
| Sustitución hacia atrás | `directos.py` | `_sustitucion_atras` |
| Inversa y determinante | `directos.py` | `inversa_gauss_jordan` ([A \| I] → [I \| A⁻¹]), `determinante` |
| Número de condición | `algebra/modulo_II_condicionamiento/condicion.py` | `numero_condicion_infinito`, `clasificar_kappa` |
| Perturbación de b | `condicion.py` | `construir_delta_b`, `analizar_perturbacion` |
| Normas ∞ y 2 | `algebra/compartido/matriz.py` | `norma_infinito_matriz`, `sumas_absolutas_por_fila`, `norma_infinito_vector`, `norma_2_vector` |
| Ecuaciones normales | `algebra/modulo_III_minimos/minimos.py` | `minimos_cuadrados` |
| Cramer (verificación) | `minimos.py` | `cramer` |
| Recta de mejor ajuste | `minimos.py` | `ajuste_lineal` |
| Fórmula de cada método iterativo | `algebra/modulo_IV_iterativos/metodos.py` | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor`, `paso_richardson` |
| Criterios de parada A/B/C | `algebra/modulo_IV_iterativos/ejecucion.py` | `ejecutar` → `_ejecutar`; códigos `TOLERANCIA_CAMBIO`, `MAXIMO_ITERACIONES`… |
| Dominancia diagonal | `algebra/modulo_IV_iterativos/convergencia.py` | `dominancia_diagonal`, `reordenamiento_dominante` |
| T_J, T_GS, T_ω | `algebra/modulo_IV_iterativos/matriz_iteracion.py` | `descomponer`, `matriz_iteracion`, `desarrollo_sarrus` |
| Polinomio característico y raíces | `algebra/modulo_IV_iterativos/polinomio_raices.py` | `polinomio_caracteristico`, `raices`, `durand_kerner` |
| ρ(T) y conclusión | `algebra/modulo_IV_iterativos/espectral.py` | `radio_espectral`, `analizar_matriz`, `concluir` |
| Comparación de métodos | `algebra/modulo_IV_iterativos/comparacion.py` | `comparar_metodos`, `configuraciones_homogeneas` |
| Matrices dispersas | `algebra/modulo_IV_iterativos/dispersas.py` | `a_csr`, `paso_*_csr` |
| Precondicionador | `algebra/modulo_IV_iterativos/precondicionamiento.py` | `analizar_precondicionador` |
| Leer lo que escribe el usuario | `algebra/compartido/validacion.py` | `leer_matriz`, `leer_vector`, `leer_tolerancia`, `leer_omega` |
| Editor de matrices | `interfaz/compartido/editor.py` | `editor`, `analizar`, `problema_dimensiones` |
| Una fórmula en LaTeX | `interfaz/compartido/formulas.py` | `latex_matriz`, `latex_polinomio`, `latex_despejes` |
| Un símbolo bien escrito | `visualizacion/notacion.py` | `D_K`, `K_MAX`…, `md`, `unicode` |
| Una gráfica | `visualizacion/interactivas.py` | `rectas_2d`, `planos_3d`, `ajuste`, `convergencia`, `comparacion`, `autovalores`, `precondicionador` |
| Gestos de la mano | `gestos/interpretacion.py` | `InterpreteGestos` |

## 3. Piezas compartidas

| Pieza | Quién la usa | Para qué |
|---|---|---|
| `algebra/compartido/matriz.py` | los 4 módulos | validar dimensiones (`validar_sistema`, `validar_cuadrada`), operar y medir (normas, `residuo`) |
| `algebra/compartido/validacion.py` | interfaz y núcleo | convertir texto en números y dar mensajes claros (`ErrorEntrada`); `formatear_numero` |
| `algebra/compartido/exactos.py` | módulos I a IV | `a_fraccion`: trabajar con fracciones exactas |
| `directos.py` (Módulo I) | módulos II, III y IV | el enunciado exige reutilizar «un método directo ya implementado»: inversa (II), Gauss (III), solución de referencia x* (IV) |
| `interfaz/compartido/*` | las 4 vistas | editor, lectura con errores, paso a paso, LaTeX, estilo |
| `visualizacion/notacion.py` | interfaz y gráficas | notación consistente en toda la aplicación |

**Funciones más conectadas** (Graphify, 11-nov): `ejecutar` (61 conexiones), `formatear_numero` (49), `ConfiguracionIterativa` (41), `ErrorEntrada` (38), `ErrorMatriz` (36), `radio_espectral` (32), `a_fraccion` (32). Son las que más conviene conocer.

## 4. Cómo se conectan las capas

```text
app.py ─► paginas/*.py ─► interfaz/modulos/<módulo>.mostrar()
                                │            │             │
                                ▼            ▼             ▼
              interfaz/compartido/   algebra/modulo_X/   visualizacion/
              (editor, LaTeX, estilo)  (calcula)          (dibuja)
                                             │
                                             ▼
                                    algebra/compartido/
```

- `algebra/` no importa nada de la interfaz ni bibliotecas externas: se puede probar solo.
- `visualizacion/` recibe resultados ya calculados y no importa `interfaz/`.
- `gestos/` es independiente: solo lo usa `interfaz/compartido/control_gestual.py`.
- No hay ciclos de importación (Graphify y análisis AST).

## 5. Recorrido de cada módulo

Todos siguen el mismo camino:

```text
ENTRADA DEL USUARIO → VALIDACIÓN → FUNCIÓN PRINCIPAL → FUNCIONES AUXILIARES → RESULTADO → VISUALIZACIÓN
```

### Módulo I — Sistemas lineales

```text
ENTRADA       paginas/sistemas.py → interfaz/modulos/modulo_I_sistemas.py::mostrar()
              editor.editor("Matriz A"), editor.editor("Vector b"); ejemplos.DIRECTOS
   ↓
VALIDACIÓN    editor.analizar + editor.problema_dimensiones   (avisa antes de resolver)
              componentes.leer_matriz_ui → validacion.leer_matriz   (texto → Fraction)
   ↓
PRINCIPAL     directos.resolver_gauss(A, b, pivoteo)  o  resolver_gauss_jordan
   ↓
AUXILIARES    _resolver: matriz.validar_sistema → _escalonar (_buscar_pivote, operaciones
              de fila con su notación de clase «−2F₁ + F₂») → _rango_aumentada →
              _sustitucion_atras (solo Gauss) o lectura directa (Gauss-Jordan)
   ↓
RESULTADO     ResultadoSistema: clasificacion, solucion o forma paramétrica, pasos, rangos, det
   ↓
VISUALIZACIÓN modulo_I_sistemas.mostrar_resultado: mensaje, Sol = {…}, componentes.mostrar_pasos,
              verificación b − Ax; interactivas.rectas_2d (2 incógnitas) o planos_3d (3) +
              control_gestual.panel
```

### Módulo II — Condicionamiento

```text
ENTRADA       interfaz/modulos/modulo_II_condicionamiento.py::mostrar(): A, b y la perturbación
              (absoluta o porcentual)
   ↓
VALIDACIÓN    problema_dimensiones(cuadrada=True); leer_matriz_ui, leer_vector_ui, leer_vector(Δb)
   ↓
PRINCIPAL     condicion.numero_condicion_infinito(A)
   ↓
AUXILIARES    matriz.norma_infinito_matriz(A) → directos.inversa_gauss_jordan(A) →
              norma_infinito_matriz(A⁻¹) → κ = producto → clasificar_kappa (10 / 100)
              condicion.construir_delta_b → analizar_perturbacion (solucion_unica dos veces,
              errores relativos en norma ∞, cota κ·‖Δb‖/‖b‖)
   ↓
RESULTADO     ResultadoCondicion (kappa, normas, inversa, interpretación); ResultadoPerturbacion
   ↓
VISUALIZACIÓN mostrar_resultado: κ∞ destacado, escala, procedimiento_de_clase (los 5 pasos de
              S7-21/09 p. 19 con matriz.sumas_absolutas_por_fila), pasos de la inversa,
              tabla de la perturbación
```

### Módulo III — Mínimos cuadrados

```text
ENTRADA       interfaz/modulos/modulo_III_minimos.py: pestaña «Sistema» (A, b) o «Ajuste» (puntos)
   ↓
VALIDACIÓN    problema_dimensiones; leer_matriz_ui; minimos.clasificar_forma (¿m > n?)
   ↓
PRINCIPAL     minimos.minimos_cuadrados(A, b)   ·   minimos.ajuste_lineal(xs, ys)
   ↓
AUXILIARES    matriz.transpuesta, multiplicar_matrices → AᵀA, Aᵀb → directos.resolver_gauss
              (ecuaciones normales) → matriz.residuo, normas → directos.determinante([A | b])
              → minimos.cramer (verificación de clase)
   ↓
RESULTADO     ResultadoMinimos (AᵀA, Aᵀb, x̂, r, ‖r‖₂, Aᵀr); ResultadoAjuste (m, c, ecuación)
   ↓
VISUALIZACIÓN mostrar_minimos: ecuaciones normales en LaTeX, x̂, tabla de residuos, procedimiento
              de clase (det[A | b], D y Dᵢ de Cramer); interactivas.ajuste (gráfica obligatoria)
```

### Módulo IV — Métodos iterativos

```text
ENTRADA       interfaz/modulos/modulo_IV_iterativos/principal.py::mostrar(): A, b, criterio,
              ε, k_max o N, ω, x⁽⁰⁾
   ↓
VALIDACIÓN    principal.leer_todo: validacion.leer_tolerancia, leer_entero_positivo, leer_omega;
              en el núcleo, ejecucion.validar_configuracion (diagonal no nula, dimensiones)
   ↓
PRINCIPAL     Ejecutar:      ejecucion.ejecutar(A, b, ConfiguracionIterativa)
              Comparar:      comparacion.comparar_metodos
              Convergencia:  convergencia.dominancia_diagonal + espectral.radio_espectral
              Precondicionar: precondicionamiento.analizar_precondicionador
   ↓
AUXILIARES    _ejecutar repite metodos.paso_<método> (o dispersas.paso_*_csr) y calcula
              dₖ = ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ y rₖ = ‖b − Ax⁽ᵏ⁾‖∞ hasta el criterio o k_max.
              radio_espectral: matriz_iteracion (① A = D + L + U, ② D⁻¹, ③ T, ④ c) →
              polinomio_raices (⑤ det(λI − T) y raíces) → concluir
   ↓
RESULTADO     ResultadoIterativo (historial de FilaIteracion, codigo, mensaje);
              ResultadoComparacion; ResultadoEspectral; ResultadoPrecondicionamiento
   ↓
VISUALIZACIÓN pestana_ejecutar: despejes (formulas.latex_despejes), tabla, CSV,
              interactivas.convergencia; pestana_comparar: interactivas.comparacion;
              pestana_convergencia: pasos ①-⑤, interactivas.autovalores;
              pestana_precondicionamiento: interactivas.precondicionador
```

### Control gestual (gráfica 3D del Módulo I)

```text
botón «Activar cámara»  →  control_gestual.control()  →  gestos.control.ControlGestual (hilo propio)
   captura.Camara (OpenCV) → deteccion.DetectorManos (MediaPipe) → mano.Mano (21 puntos)
   → interpretacion.InterpreteGestos (gesto estable) → movimiento.CamaraOrbital (θ, φ, r)
   → servidor.ServidorCamara (127.0.0.1, SSE) → interfaz/compartido/puente_camara.js
   → Plotly.relayout en el navegador
```

## 6. Pruebas de cada parte

| Carpeta de `tests/` | Prueba |
|---|---|
| `compartido/` | `matriz.py` y `validacion.py` |
| `modulo_I/` | Gauss, Gauss-Jordan, pivoteo, clasificación, inversa, notación de clase |
| `modulo_II/` | κ∞, escala, perturbación |
| `modulo_III/` | ecuaciones normales, Cramer, ajuste |
| `modulo_IV/` | métodos, criterios, ρ(T), dispersas, precondicionamiento |
| `gestos/` | gestos con manos sintéticas, cámara orbital, hilo y perro guardián |
| `interfaz/` | la aplicación completa con AppTest, editor, gráficas (mismos datos que el núcleo), notación |
| `entrega/` | el ZIP no incluye archivos internos ni credenciales |

Ejecutar todas: `ejecutar_pruebas.bat`, o `python -m unittest discover -s tests -t .`.
Auditoría independiente: `python auditoria/auditoria_directos.py .` (y los demás guiones de `auditoria/`).

## 7. Por dónde empezar a leer

1. `algebra/modulo_I_sistemas/directos.py`: es la base que reutilizan los otros tres módulos.
2. `algebra/modulo_IV_iterativos/metodos.py` y `ejecucion.py`: las fórmulas y el bucle.
3. La vista de un módulo (`interfaz/modulos/…`), para ver cómo se muestra un resultado.
4. `visualizacion/interactivas.py`, para las gráficas.
