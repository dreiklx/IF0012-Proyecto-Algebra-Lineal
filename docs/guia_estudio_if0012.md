# Guía de estudio del proyecto Ax — IF0012 Álgebra Lineal

**Versión:** 10-nov-2026.
**Grupo 01:** Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez.
**Fechas:** entrega el 11-nov-2026; defensa individual la semana del 16-nov-2026.
**Docente:** Prof. Imelda Sáenz Pineda.

**Para qué sirve esta guía:** es el material único para estudiar Ax y defenderlo. Resume y ordena los documentos del repositorio:

- `referencia_oficial_procedimientos.md`;
- `guia_defensa_equipo.md`;
- `guia_recorrido_codigo.md`;
- `investigacion_richardson.md`;
- `investigacion_mediapipe.md`;
- `arquitectura.md`;
- `auditoria_requisitos.md`;
- `auditoria_textos_profesora.md`.

Todo lo que dice esta guía corresponde al código real de `main`. Los ejemplos numéricos se volvieron a ejecutar el 10-nov.

**Cómo citar los PDF:**

- «S8-30/09 p. 20» es la página 20 del PDF de clase del 30-09 (semana 8).
- «OFICIAL p. 2» es el enunciado del proyecto.
- «PROG» es el programa del curso.

**Las cuatro categorías de procedencia (se ven en la aplicación como «Cat.»):**

| Cat. | Significa | Cómo decirlo en la defensa |
|---|---|---|
| **A** | Visto en clase (aparece en los PDF de la profesora) | «Lo vimos en clase: S… p. …» |
| **B** | Exigido por el enunciado del proyecto, aunque no se haya resuelto así en clase | «Lo pide el enunciado, OFICIAL p. …» |
| **C** | Extensión o incentivo: **no** se vio en clase | «Es una extensión, rotulada así en la aplicación; la usamos porque…» |
| **D** | Sin respaldo | No hay ninguna en Ax |

## Índice

- A. El proyecto
- B. Los cuatro módulos
- C. Procedimientos de la profesora: clase, proyecto y extensiones
- D. Arquitectura del código
- E. MediaPipe y control gestual
- F. Defensa: preguntas y respuestas
- G. Plan de estudio y hoja de repaso

---

## A. El proyecto

### A.1 Qué es Ax

Ax es una aplicación web **local**, hecha con Streamlit, que resuelve y analiza sistemas de ecuaciones lineales, como pide el proyecto final de IF0012 (OFICIAL pp. 1-5). Se abre en el navegador en `http://localhost:8501` y funciona sin internet una vez instalada.

### A.2 Qué problema resuelve

El enunciado pide una herramienta con **cuatro módulos** que implementen **desde cero** los métodos del curso.

**Está prohibido** usar bibliotecas que hagan directamente estos cálculos (OFICIAL p. 1):

- Gauss y Gauss-Jordan;
- determinantes e inversa;
- mínimos cuadrados;
- Jacobi, Gauss-Seidel y SOR;
- radio espectral.

**Ax cubre los cuatro módulos:**

| Módulo | Pregunta matemática |
|---|---|
| I · Sistemas lineales | ¿Ax = b tiene solución única, infinitas o ninguna? ¿Cuál es? |
| II · Condicionamiento | ¿Qué tan sensible es la solución a errores en b? (κ∞) |
| III · Mínimos cuadrados | Si hay más ecuaciones que incógnitas y no hay solución exacta, ¿cuál es la mejor aproximación? |
| IV · Métodos iterativos | ¿Cómo aproximar x con Jacobi, Gauss-Seidel y SOR? ¿Converge? ¿Cuál es más rápido? |

### A.3 Cómo está organizado (vista rápida)

```text
app.py            punto de entrada (barra superior con 5 páginas)
algebra/          NÚCLEO MATEMÁTICO: Python puro, sin bibliotecas externas
interfaz/         pantallas en Streamlit (no calcula)
visualizacion/    gráficas Plotly y Matplotlib (solo dibujan)
gestos/           control gestual de la gráfica 3D (MediaPipe; no toca el álgebra)
tests/            281 pruebas automáticas
auditoria/        comparación con miles de casos aleatorios
```

**Regla de oro:** la interfaz pide, el núcleo calcula y la visualización dibuja. Ninguna gráfica recalcula nada.

### A.4 Tecnologías

| Tecnología | Para qué | ¿Resuelve métodos del curso? |
|---|---|---|
| Python 3.11+ (probado en 3.13 y 3.14) | Todo el proyecto | — |
| `fractions`, `math`, `cmath`, `dataclasses` (estándar) | Núcleo matemático: aritmética exacta, raíces, resultados | No; son operaciones elementales |
| Streamlit 1.66.1 | Interfaz web local | No |
| Plotly 6.3.0 | Gráficas interactivas (rotar, zoom, valores al pasar el cursor) | No |
| Matplotlib 3.11.2 | Gráficas estáticas de respaldo | No |
| MediaPipe 1.2.2 + OpenCV (contrib) 5.0 | Control gestual opcional de la vista 3D | No |

**Dos tipos de aritmética:**

- **Fracciones exactas** (`Fraction`) en los Módulos I, II y III. Un pivote es 0 solo si es realmente 0, así que la clasificación no depende de redondeos.
- **Punto flotante** en el Módulo IV. Las iteraciones son aproximaciones que se detienen por tolerancia; con fracciones, los denominadores crecerían sin control.

**Ningún archivo del proyecto importa NumPy, SciPy ni SymPy.** NumPy solo lo usan Streamlit, Plotly, Matplotlib y MediaPipe por dentro.

---

## B. Los cuatro módulos

### B.1 Módulo I — Sistemas lineales y métodos directos

**Qué hace:**

- Resuelve Ax = b con **eliminación de Gauss** (forma escalonada más sustitución hacia atrás) o con **Gauss-Jordan** (forma escalonada reducida).
- Muestra cada operación elemental con la matriz resultante.
- Clasifica el sistema y dibuja las rectas o los planos.

**Procedimiento (como en clase, S6-14/09 p. 28 y S6-16/09 p. 29):**

1. Formar la matriz aumentada [A | b].
2. Recorrer las columnas de izquierda a derecha. Para cada una, buscar un pivote no nulo; si el elemento de la diagonal es 0, intercambiar filas (F₁ ↔ F₂).
3. Anular los elementos debajo del pivote con operaciones elementales, con la notación de la profesora: «−2F₁ + F₂» significa «a F₂ súmele −2 veces F₁».
4. Gauss-Jordan además normaliza el pivote («(−1/3)F₃») y anula también arriba.
5. Clasificar, y si la solución es única, hacer la sustitución hacia atrás.

**Fórmulas que hay que conocer:**

- Multiplicador: m = aᵢₖ / aₖₖ. La operación es Fᵢ → Fᵢ − m·Fₖ, que la profesora escribe «−m·Fₖ + Fᵢ».
- **Clasificación**, en palabras de clase («3 ecuaciones no nulas, 3 incógnitas → única solución») y en rangos:
  - rango(A) < rango([A|b]) → **sin solución**. Aparece una fila [0 … 0 | c] con c ≠ 0, es decir, «0 = c».
  - rango(A) = rango([A|b]) = n → **solución única**.
  - rango(A) = rango([A|b]) < n → **infinitas soluciones**, con n − rango variables libres: x = xₚ + t₁v₁ + …
- det(A) = (−1)^(número de intercambios) × (producto de los pivotes). Es la propiedad de las operaciones de fila (S2-19/08 p. 38).

**Funciones del código** (`algebra/modulo_I_sistemas/directos.py`):

| Función | Qué hace |
|---|---|
| `resolver_gauss(A, b, pivoteo)` / `resolver_gauss_jordan(A, b, pivoteo)` | Puntos de entrada del módulo |
| `_resolver` | Arma [A\|b], escalona, clasifica y sustituye |
| `_escalonar` | El corazón: busca pivotes, intercambia, anula y registra cada `Paso` (con `descripcion` y `notacion` de clase) |
| `_buscar_pivote` | «Primer no nulo» (como en clase) o pivoteo parcial (opción) |
| `_rango_aumentada` | Detecta la fila 0 = c |
| `_sustitucion_atras` | Despeja desde la última ecuación |
| `inversa_gauss_jordan`, `determinante`, `solucion_unica` | Los reutilizan los Módulos II, III y IV |

**Ejemplo para la defensa** (manuscrito de S6-16/09 p. 29, ejemplo precargado). El sistema es x + y + z = 6, 2x + y − z = 3, −x + y + 2z = 7:

- −2F₁ + F₂ y F₁ + F₃ → −F₂ → −2F₂ + F₃ → (−1/3)F₃;
- z = 5/3, y + 3(5/3) = 9 ⇒ y = 4, x = 6 − 4 − 5/3 = 1/3;
- **Sol = {(1/3, 4, 5/3)}** y det(A) = 3.

**Cómo explicar el resultado:**

- «Hay 3 ecuaciones no nulas y 3 incógnitas, así que la solución es única».
- «Geométricamente, los tres planos se cortan en un punto».
- «La verificación b − Ax = (0, 0, 0) confirma la solución exacta».

### B.2 Módulo II — Condicionamiento y sensibilidad

**Qué hace:**

- Calcula κ∞(A) con la inversa obtenida por **nuestro** Gauss-Jordan [A | I] → [I | A⁻¹].
- Clasifica la sensibilidad.
- Compara la solución de Ax = b con la del sistema perturbado Ax̃ = b + Δb.

**Procedimiento:** los 5 pasos de clase (S7-21/09 p. 19), con la norma que exige el enunciado.

1. Elegir la norma: ∞, por OFICIAL p. 2.
2. Calcular ‖A‖∞, la máxima suma de valores absolutos por **fila**.
3. Calcular A⁻¹, verificando que sea invertible y que A·A⁻¹ = I.
4. Calcular ‖A⁻¹‖∞.
5. Multiplicar: κ∞(A) = ‖A‖∞ · ‖A⁻¹‖∞.

**Fórmulas:**

- **Escala del proyecto (OFICIAL p. 2, Cat. B):** κ < 10 baja; 10 ≤ κ < 100 moderada; κ ≥ 100 alta. La lámina S7-21/09 p. 18 usa 5 niveles, pero el enunciado fija esta escala.
- **Cota (S7-21/09 p. 18):** ‖Δx‖/‖x‖ ≤ κ(A) · ‖Δb‖/‖b‖.
- **Perturbación porcentual** (interpretación propia de un requisito B): Δbᵢ = (p/100)·bᵢ.

**Funciones** (`algebra/modulo_II_condicionamiento/condicion.py`):

- `numero_condicion_infinito`;
- `clasificar_kappa`;
- `construir_delta_b` (absoluta o porcentual);
- `analizar_perturbacion`, que da los errores relativos, verifica la cota y calcula la amplificación.

**Ejemplo** (lámina S7-21/09 p. 19): B = [[1, 2], [3, 1]].

- ‖B‖∞ = 4 y B⁻¹ = [[−1/5, 2/5], [3/5, −1/5]], así que ‖B⁻¹‖∞ = 4/5.
- **κ∞ = 16/5 ≈ 3,2**: sensibilidad baja.

**Cómo explicar el resultado:**

- «κ dice cuánto puede amplificarse, como máximo, un error relativo en b».
- «Con κ = 3,2, un error del 1 % en b produce como mucho un 3,2 % en x».

### B.3 Módulo III — Mínimos cuadrados y ajuste lineal

**Qué hace:**

- Detecta si el sistema es sobredeterminado (m > n).
- Resuelve las **ecuaciones normales** AᵀA x̂ = Aᵀb con nuestro Gauss.
- Calcula el residuo r = b − A x̂ y ‖r‖₂.
- Hace el ajuste de una recta y = mx + c a datos (xᵢ, yᵢ), con su gráfica.

**Procedimiento:**

- Ax muestra **los tres pasos del manuscrito de la profesora** (S8-30/09 pp. 5-7):
  1. Comprobar que b **no** es combinación lineal de las columnas de A: si m = n + 1, det([A | b]) ≠ 0. La profesora lo calcula por Sarrus.
  2. Plantear el sistema normal asociado AᵀAx = Aᵀb.
  3. Resolverlo. La profesora usa la **regla de Cramer**.
- El enunciado exige resolverlo «con un método directo ya implementado» (Cat. B), así que Ax lo resuelve con **Gauss** y muestra Cramer como **verificación** (Cat. A).

**Fórmulas:**

- Ecuaciones normales: AᵀA x̂ = Aᵀb.
- Residuo: r = b − A x̂; ‖r‖₂ = √(Σ rᵢ²).
- Propiedad que se verifica: Aᵀr = 0, es decir, el residuo es ortogonal a las columnas de A.
- Cramer: xⱼ = det((AᵀA)ⱼ) / det(AᵀA), donde la columna j se reemplaza por Aᵀb.
- Recta: matriz de diseño con filas [xᵢ, 1] e incógnitas (m, c).

**Funciones** (`algebra/modulo_III_minimos/minimos.py`):

- `clasificar_forma`;
- `minimos_cuadrados`, que calcula det_aumentada, AᵀA, Aᵀb, la solución con `solucion_unica`, el residuo y Cramer;
- `cramer`;
- `ajuste_lineal`.

**Ejemplo** (manuscrito S8-30/09 pp. 6-7): x + 3y = −1, 3x − 2y = 8, −2x + 5y = −8.

- det[A|b] = −11 ≠ 0, así que b no está en Col(A).
- AᵀA = [[14, −13], [−13, 38]] y Aᵀb = (39, −59).
- **x̂ = (65/33, −29/33)**, igual en Ax por Gauss y por Cramer.

**Cómo explicar el resultado:**

- «No existe solución exacta, así que buscamos el x̂ que hace ‖Ax − b‖₂ lo más pequeño posible».
- «El residuo mide cuánto falta para cumplir las ecuaciones».

### B.4 Módulo IV — Métodos iterativos y convergencia

**Qué hace:**

- Ejecuta Jacobi, Gauss-Seidel y SOR con:
  - vector inicial: cero, xᵢ⁽⁰⁾ = bᵢ/aᵢᵢ (convención de la profesora) o personalizado;
  - tolerancia ε, máximo de iteraciones y ω.
- Muestra la tabla k, x⁽ᵏ⁾ y error, el motivo de parada y la gráfica del error frente a la iteración.
- Compara los tres métodos.
- Analiza la convergencia: dominancia diagonal y radio espectral.

**Procedimiento y fórmulas (S8-30/09 pp. 15-33; A = D + L + U, con L y U estrictas):**

- **Jacobi:** xᵢ⁽ᵏ⁺¹⁾ = (1/aᵢᵢ)·(bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁾).
- **Gauss-Seidel:** xᵢ⁽ᵏ⁺¹⁾ = (1/aᵢᵢ)·(bᵢ − Σ_{j<i} aᵢⱼxⱼ⁽ᵏ⁺¹⁾ − Σ_{j>i} aᵢⱼxⱼ⁽ᵏ⁾). Usa los valores ya actualizados.
- **SOR**, como lo calcula la profesora (S8-30/09 pp. 32-33): primero x^GS y luego xᵢ⁽ᵏ⁺¹⁾ = (1 − ω)xᵢ⁽ᵏ⁾ + ω·xᵢ^GS.
  - ω = 1 es Gauss-Seidel;
  - 0 < ω < 1 es subrelajación;
  - 1 < ω < 2 es sobrerrelajación.
- **Criterios de parada:**
  - A: ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε, el que más usa la profesora;
  - B: ‖b − Ax⁽ᵏ⁾‖∞ < ε (S8-28/09 p. 6);
  - C: un número fijo de iteraciones N.
- **Dominancia diagonal estricta por filas:** |aᵢᵢ| > Σ_{j≠i}|aᵢⱼ| es una condición **suficiente** de convergencia (S8-30/09 p. 37). Si no se cumple, se pueden reordenar las ecuaciones (S9-05/10 pp. 32-33).
- **Forma matricial (S9-07/10 pp. 3-7):**
  - T_J = −D⁻¹(L + U), C_J = D⁻¹b;
  - T_GS = −(D + L)⁻¹U, C_GS = (D + L)⁻¹b;
  - x⁽ᵏ⁺¹⁾ = T x⁽ᵏ⁾ + C.
- **Radio espectral:** ρ(T) = máx{|λ|}, donde det(T − λI) = 0. El método converge para todo x⁽⁰⁾ si y solo si ρ(T) < 1. En 3×3 la profesora usa Sarrus.

**Funciones** (`algebra/modulo_IV_iterativos/`):

| Archivo | Funciones |
|---|---|
| `metodos.py` | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor` (y `paso_richardson`, extensión) |
| `ejecucion.py` | `ConfiguracionIterativa`, `ejecutar` (bucle común, criterios A/B/C, tabla, motivo; nunca lanza excepciones) |
| `convergencia.py` | `dominancia_diagonal`, `reordenamiento_dominante` |
| `espectral.py` | `descomponer` (D, L, U), `matriz_iteracion` (T y c), `polinomio_caracteristico`, `desarrollo_sarrus`, `raices`, `durand_kerner`, `concluir`, `radio_espectral` |
| `comparacion.py` | `comparar_metodos` (misma configuración; error final ‖x⁽ᵏ⁾ − x*‖∞, S9-05/10 p. 17) |
| `dispersas.py` | CSR: `a_csr`, `producto_csr_vector`, pasos `*_csr` (incentivo) |
| `precondicionamiento.py` | `precondicionar_diagonal`, `analizar_precondicionador` (incentivo) |

**Ejemplos:**

- **Tridiagonal [−1, 4, −1] de 4×4, b = (1, 0, 0, 1)**, con ε = 10⁻³, x⁽⁰⁾ = 0 y ω = 1,2:
  - Jacobi para en 7 iteraciones, Gauss-Seidel en 5 y SOR en 7, todos por tolerancia (criterio A);
  - la solución es (1/3, 1/15, 1/15, 1/3) (S9-05/10 p. 14).
- **S9-07/10 (Jacobi), A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]]:**
  - det(T − λI) = −λ³ − (4/9)λ + 4/3;
  - **ρ(T_J) ≈ 1,174 > 1: no converge**;
  - la hoja de clase concluye ρ = 0 porque omite el término 4/3 (errata verificada).

**Cómo explicar el resultado:**

- «Paró por tolerancia: el cambio entre iteraciones fue menor que ε en la iteración k».
- «Gauss-Seidel suele necesitar menos iteraciones, porque usa los valores nuevos en cuanto los calcula».
- «ρ(T) < 1 garantiza la convergencia; la dominancia diagonal es solo una condición suficiente».

---

## C. Procedimientos de la profesora: clase, proyecto y extensiones

### C.1 Notación de sus PDF (la que usa Ax)

| Concepto | Notación de la profesora | Fuente |
|---|---|---|
| Operaciones elementales | Fᵢ ↔ Fⱼ; kFᵢ; «−5F₁ + F₂» (múltiplo de la fila pivote más la fila destino); normaliza el pivote: «½F₁», «−F₂» | S2-19/08 p. 27; S3-24/08 pp. 4-5 |
| Sistema | Ax = b; [A \| b] | S6-14/09 pp. 22-25 |
| Solución | «Sol = {(1/3, 4, 5/3)}» | S6-16/09 p. 29 |
| Clasificación | «3 ecuaciones no nulas, 3 incógnitas → única solución» | S6-16/09 p. 29 |
| Determinante | \|A\|, det(A); Sarrus en 3×3 | S2-19/08 pp. 29-38 |
| Iterativos | A = D + L + U; T_J, C_J; x⁽ᵏ⁺¹⁾ = Tx⁽ᵏ⁾ + C | S8-28/09 p. 7; S9-07/10 |
| Radio espectral | ρ(T) = máx{\|λ\|}; en los manuscritos aparece como «P(T)» | S9-05/10 p. 34 |
| Tolerancia | ε, o «T = 0,01» en los manuscritos («Cálculo de la tolerancia T₁ = ‖x⁽¹⁾ − x⁽⁰⁾‖∞») | S8-30/09 pp. 19-20 |
| Precondicionador | M, M⁻¹Ax = M⁻¹b, M = D | S9-05/10 pp. 19-22 |

### C.2 Lo que se vio en clase (Cat. A)

| Procedimiento | Fuente | Dónde en Ax |
|---|---|---|
| [A \| b] y operaciones elementales | S2-19/08 p. 27; S6-14/09 pp. 25-27 | Módulo I, pasos |
| Gauss y sustitución hacia atrás | S6-14/09 pp. 28-32; S6-16/09 p. 29 | `_escalonar`, `_sustitucion_atras` |
| Gauss-Jordan e inversa [A \| I] → [I \| A⁻¹] | S3-24/08 pp. 4-8; S6-14/09 p. 30 | `inversa_gauss_jordan` |
| Tipos de solución y su interpretación geométrica | S6-14/09 p. 26 | Clasificación y gráfica |
| κ(A) = ‖A‖‖A⁻¹‖ en 5 pasos; la cota | S7-21/09 pp. 17-19 | Módulo II |
| det[A\|b], sistema normal, Cramer | S8-30/09 pp. 4-7 | Módulo III |
| Jacobi, Gauss-Seidel, SOR; x⁽⁰⁾ = bᵢ/aᵢᵢ; criterio ‖Δx‖ < ε | S8-30/09 pp. 15-33 | Módulo IV |
| Dominancia diagonal y reordenamiento | S8-30/09 p. 37; S9-05/10 pp. 32-33 | Pestaña «Convergencia» |
| T_J, T_GS, det(T − λI) por Sarrus, ρ(T) | S9-07/10 pp. 3-7 | `desarrollo_sarrus`, `matriz_iteracion` |
| Error final ‖x⁽ᵏ⁾ − x‖∞ | S9-05/10 p. 17 | `comparar_metodos` |

### C.3 Lo que exige el proyecto (Cat. B)

- **Norma ∞ y escala 10 / 100** para κ (OFICIAL p. 2). La lámina usa la norma 1 o 2 y 5 niveles.
- **Resolver las ecuaciones normales con un método directo propio**, que en Ax es Gauss.
- **‖r‖₂** del residuo, y la recta de ajuste con su gráfica.
- **Detectar pivotes nulos o «numéricamente problemáticos».** El umbral 10⁻¹⁰·máx|aᵢⱼ| es una decisión técnica propia.
- **Perturbación absoluta o porcentual** de b.
- **Módulo IV:**
  - tabla k, x⁽ᵏ⁾ y error;
  - motivo de parada;
  - comparación de los tres métodos;
  - gráfica del error frente a la iteración;
  - máximo de iteraciones.
- **Validaciones** (OFICIAL p. 3): vacíos, dimensiones, singularidad, ε > 0, k_max entero > 0, 0 < ω < 2 y ningún cierre inesperado.

### C.4 Extensiones (Cat. C): **no** se vieron en clase

| Extensión | Qué es | Por qué está en Ax | Dónde |
|---|---|---|---|
| **Richardson** | x⁽ᵏ⁺¹⁾ = x⁽ᵏ⁾ + (b − Ax⁽ᵏ⁾); su matriz de iteración es I − A | Para **demostrar** el efecto del precondicionador: con M = D, Jacobi, GS y SOR **no cambian**, y Richardson sí. Precondicionado con M = D, Richardson es exactamente Jacobi | `metodos.paso_richardson`; pestaña «Precondicionamiento», con el aviso «Extensión no vista en clase» |
| **Faddeev-LeVerrier** | Calcula los coeficientes de det(λI − T) con productos y trazas: M₀ = 0; Mₖ = T·Mₖ₋₁ + cₖ₋₁I; cₖ = −tr(T·Mₖ)/k. Es exacto con fracciones | Sarrus solo sirve para 3×3; el enunciado pide ρ(T) para cualquier n. En 3×3 da **el mismo** polinomio que Sarrus (prueba `test_faddeev_coincide_con_sarrus_3x3`) | `espectral.polinomio_caracteristico` |
| **Durand-Kerner** | Aproxima **todas** las raíces (también las complejas) a la vez: zᵢ ← zᵢ − p(zᵢ)/Π_{j≠i}(zᵢ − zⱼ) | Las raíces de un polinomio de grado ≥ 3 en general no tienen fórmula sencilla, y ρ depende de las complejas (ejemplo de S9-07/10) | `espectral.durand_kerner`, `raices` |
| Matriz de iteración de SOR | T_ω = (D + ωL)⁻¹[(1 − ω)D − ωU] | Para dar ρ(T) también de SOR | `matriz_iteracion` |
| Pivoteo parcial | Elegir el mayor \|aᵢₖ\| como pivote | Opción; la lámina solo menciona PA = LU | Módulo I |
| CSR, precondicionador M = D, CSV, gráficas, control gestual | Incentivos (OFICIAL p. 5) | Ver F.6 | Módulos I y IV |

**Frase para la defensa:** «Richardson, Faddeev-LeVerrier y Durand-Kerner no los vimos en clase. Son extensiones y la aplicación las rotula así. Las usamos porque el procedimiento de clase (Sarrus) solo cubre 3×3 y porque, con M = D, Jacobi no cambia».

### C.5 Erratas de las láminas (verificadas con fracciones; Ax muestra el valor correcto)

| Fuente | Dice | Valor correcto |
|---|---|---|
| S2-19/08 pp. 42-43 | det = 42 | 15 |
| S3-26/08 p. 26 | ‖x‖₂ ≤ ‖x‖∞ ≤ ‖x‖₁ | ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ |
| S6-14/09 p. 29 | (1/2, −1, −1) | (19/20, −5/4, −7/20) |
| S7-21/09 p. 14 | (100, −97) | (100/101, 203/101) |
| S8-30/09 p. 20 | T₁ = 2,402 «‖·‖∞» | Esa suma es la norma 1; la norma ∞ da 1,889 (Ax usa el máximo) |
| S9-05/10 p. 23 | Jacobi con M = D converge más rápido | Las iteraciones son **idénticas** |
| S9-07/10 p. 4 | ρ(T_J) = 0 | ≈ 1,174: no converge |
| S9-07/10 p. 7 | C_GS = −(D + L)⁻¹b | C_GS = (D + L)⁻¹b |

**Regla:** ninguna salida de una lámina se usó como «resultado esperado» sin recalcularla.

---

## D. Arquitectura del código

### D.1 Carpetas y archivos

```text
proyecto-algebra/
├── app.py                         st.navigation con 5 páginas (barra superior)
├── paginas/                       inicio, sistemas, condicionamiento, minimos, iterativos
├── algebra/                       NÚCLEO (solo biblioteca estándar)
│   ├── compartido/
│   │   ├── matriz.py              validar, producto, transpuesta, normas ∞ y 2, residuo
│   │   ├── validacion.py          texto → Fraction; ε, k_max, ω; ErrorEntrada; formatear_numero
│   │   └── exactos.py             a_fraccion
│   ├── modulo_I_sistemas/directos.py
│   ├── modulo_II_condicionamiento/condicion.py
│   ├── modulo_III_minimos/minimos.py
│   └── modulo_IV_iterativos/      metodos, ejecucion, convergencia, espectral,
│                                  comparacion, dispersas, precondicionamiento
├── interfaz/                      PRESENTACIÓN (no calcula)
│   ├── portada.py, navegacion.py
│   ├── compartido/                estilo (diseño y distintivos Cat.), componentes, editor de
│   │                              matrices, ejemplos, control_gestual.py, puente_camara.js
│   └── modulos/                   modulo_I_sistemas.py, modulo_II_…, modulo_III_…,
│                                  modulo_IV_iterativos/ (una vista por pestaña)
├── visualizacion/                 interactivas.py (Plotly), graficos.py y geometria_3d.py
│                                  (Matplotlib), tema.py
├── gestos/                        control gestual (ver la parte E)
├── tests/                         compartido, modulo_I…IV, interfaz, entrega, gestos
├── auditoria/                     oráculos independientes y casos difíciles
├── casos_prueba/                  casos documentados: entrada, esperado, obtenido
└── docs/                          documentación
```

### D.2 Reglas de dependencia

```text
paginas → interfaz/modulos → interfaz/compartido → visualizacion
                     │                   └──────→ gestos
                     ▼
algebra/modulo_IV → modulo_I (Gauss-Jordan, Gauss)   modulo_III → modulo_I   modulo_II → modulo_I
                     ▼
              algebra/compartido
```

- `algebra/` no importa nada de la interfaz ni bibliotecas externas.
- `gestos/` no importa `algebra/`.
- No hay ciclos de importación (verificado con Graphify y con un análisis AST).
- **El Módulo I es la base.** Los Módulos II, III y IV reutilizan su Gauss-Jordan y su Gauss, como pide el enunciado: «inversa con un algoritmo implementado por el grupo» y «un método directo ya implementado».

### D.3 Flujo de un cálculo (igual en los cuatro módulos)

```text
editor (texto) → validacion.leer_* → función del núcleo → Resultado (dataclass) → interfaz y gráficas
```

Ejemplo, Módulo IV «Ejecutar»:

1. `principal.mostrar()` lee A, b y los parámetros.
2. `pestana_ejecutar` arma una `ConfiguracionIterativa`.
3. `ejecucion.ejecutar(A, b, config)` repite `metodos.paso_*` hasta cumplir el criterio y devuelve un `ResultadoIterativo`.
4. La pestaña muestra la tabla, el motivo, el CSV y la gráfica.

### D.4 Dónde encontrar cada cosa (para «muéstreme el código»)

| Pregunta | Archivo → función |
|---|---|
| Gauss | `algebra/modulo_I_sistemas/directos.py` → `_escalonar` |
| Inversa | `directos.py` → `inversa_gauss_jordan` |
| κ∞ | `algebra/modulo_II_condicionamiento/condicion.py` → `numero_condicion_infinito` |
| Ecuaciones normales | `algebra/modulo_III_minimos/minimos.py` → `minimos_cuadrados` |
| Jacobi | `algebra/modulo_IV_iterativos/metodos.py` → `paso_jacobi` |
| Criterio de parada | `ejecucion.py` → `ejecutar` |
| ρ(T) | `espectral.py` → `radio_espectral` |
| CSR | `dispersas.py` → `MatrizCSR`, `a_csr` |
| Precondicionador | `precondicionamiento.py` → `analizar_precondicionador` |
| Notación «−2F₁ + F₂» | `directos.py` → `_notacion_combinacion` |
| Distintivos Cat. | `interfaz/compartido/estilo.py` → `procedencia` |

### D.5 Cómo se verificó

- **281 pruebas** (`python -m unittest`).
- **Auditoría aleatoria con 0 fallos:**
  - 4500 sistemas;
  - 400 inversas, determinantes y κ;
  - 200 perturbaciones;
  - 300 mínimos cuadrados;
  - 600 ejecuciones iterativas;
  - 300 análisis espectrales;
  - 150 precondicionadores.
- **Volcado de los 273 resultados de los ejemplos:** idéntico tras cada cambio.
- **Autoverificaciones en pantalla:** b − Ax = 0; A·A⁻¹ = I; Aᵀr = 0; Σλ = tr(T).

---

## E. MediaPipe y control gestual

**Qué es:** un complemento de experiencia de usuario (Cat. C) para girar y acercar la **gráfica 3D de planos del Módulo I** con la mano durante la exposición. **No calcula nada del álgebra**: solo cambia desde dónde se mira la gráfica.

### E.1 Cómo se activa la cámara

1. Módulo I → resolver un sistema de 3 incógnitas → abrir «Interpretación geométrica».
2. Debajo de la gráfica, pulsar **«📷 Activar cámara y gestos»**.
3. **La cámara solo se enciende con ese botón**, nunca al cargar la página.
4. Mientras está encendida se ven la insignia **«● Cámara activa»**, el estado, el gesto detectado, los fotogramas por segundo y la latencia.

### E.2 Cómo se detectan las manos

```text
cámara web ─► captura.py ─► deteccion.py ─► interpretacion.py ─► movimiento.py ─► servidor.py ─► gráfica
(OpenCV)      fotograma      21 puntos       gesto y acción      cámara 3D         9 números      Plotly
              en memoria     por mano                            (θ, φ, r)         127.0.0.1
```

- `gestos/captura.py`: `cv2.VideoCapture(0, cv2.CAP_DSHOW)`. Voltea la imagen en espejo para que el movimiento resulte natural.
- `gestos/deteccion.py`: **MediaPipe Hand Landmarker** (API Tasks, modo VIDEO, hasta 2 manos). Devuelve **21 puntos** por mano: 0 = muñeca, 4 = punta del pulgar, 8 = punta del índice…
- `gestos/control.py`: un **hilo** («gestos-vision») repite captura → detección → interpretación → cámara. **Nunca llama a funciones de Streamlit**; deja el estado en un objeto protegido con un candado.
- El modelo `hand_landmarker.task` (7,8 MB, Apache-2.0) va dentro del proyecto, así que funciona sin internet.
- **Privacidad:**
  - el fotograma se procesa y se descarta (`del fotograma`); no se guarda, no se graba y no se envía;
  - al navegador solo llegan 9 números de la cámara 3D.

### E.3 Qué hace cada gesto

Todas las distancias se dividen por el **tamaño de la palma** (muñeca → nudillo del dedo medio). Así los gestos funcionan igual con la mano cerca o lejos de la cámara.

| Gesto | Acción | Cómo lo reconoce el código (`interpretacion.py`) |
|---|---|---|
| ✋ Palma abierta (½ s) | Activa el control y **calibra** la pinza con su mano | Los 4 dedos extendidos (punta más lejos de la muñeca que su articulación) |
| 🤏 Pinza pulgar-índice | Agarrar y **girar** la vista | Punta del pulgar cerca de la punta del índice (razón < umbral), con el índice fuera de la palma |
| 🤏🤏 Pinza con las dos manos | **Zoom**: separarlas acerca, juntarlas aleja | Cociente de la distancia entre los dos puntos de agarre |
| ✊ Puño (½ s) | **Pausa**: la vista deja de seguir la mano. Se reanuda con la palma | Ningún dedo extendido |
| ✌️ Victoria (≈ 1 s) | **Restablece** la vista inicial (una vez por gesto) | Índice y medio extendidos; anular y meñique doblados |

### E.4 Cómo funciona la pinza (estabilidad)

- **Antirrebote:** los gestos discretos deben mantenerse un tiempo mínimo (0,35 s; victoria 0,8 s).
- **Histéresis:** la pinza **entra** cuando la razón pulgar-índice baja del umbral y **sale** solo cuando supera un umbral 1,5 veces mayor. Así no parpadea en el borde.
- **Calibración (umbral adaptativo):** al activar con la palma se mide su separación natural pulgar-índice, y el umbral se ajusta dentro de [0,18; 0,25].
- **Suavizado exponencial** del punto de agarre: s ← s + α(x − s), con α = 0,35.
- **Zona muerta acumulada** (0,004 del ancho de la imagen): el temblor, que va y viene, se cancela; el movimiento lento y sostenido sí llega.
- **Sin saltos:** el primer fotograma de la pinza solo fija la referencia.
- Si se pierde la mano durante 0,5 s, se suelta.

### E.5 Cómo se controla la perspectiva 3D

La cámara de Plotly es una **cámara orbital en coordenadas esféricas** alrededor del centro (`gestos/movimiento.py`, `CamaraOrbital`):

**eye = r · (cos φ · cos θ, cos φ · sin θ, sin φ)**, con up = (0, 0, 1) fijo.

| Movimiento con la pinza | Efecto | Código |
|---|---|---|
| Mano a la derecha (dx > 0) | θ disminuye: la escena gira hacia la derecha, como al arrastrar con el ratón | `theta -= dx · sensibilidad` |
| **Mano hacia arriba** (dy < 0 en la imagen) | **φ disminuye: la vista baja** (se mira más desde abajo) | `phi + dy · sensibilidad` |
| **Mano hacia abajo** (dy > 0) | **φ aumenta: la vista sube** (se mira más desde arriba) | ídem |
| Dos manos que se separan | r disminuye: acerca | `zoom`: r ← r / factor |

- **Cambio reciente (10-nov):** a pedido del equipo **se invirtió solo el eje vertical** de la pinza con una mano. En `CamaraOrbital.girar` (`gestos/movimiento.py`), `phi - dy·s` pasó a `phi + dy·s`.
- No cambiaron el giro horizontal, el zoom, la detección, la calibración, el suavizado, los límites, la pausa ni el restablecimiento. La prueba `test_eje_vertical_invertido` lo comprueba.
- **Límites:** elevación φ ∈ [−80°, 85°]; distancia r ∈ [0,9; 5]. La vista nunca se voltea.
- **Sensibilidad:** cruzar la imagen de lado a lado equivale a media vuelta (π radianes).

**Cómo llega la cámara a la gráfica:**

- Un servidor mínimo de Python (`gestos/servidor.py`) escucha **solo en 127.0.0.1**, con un token aleatorio, y envía la cámara por «Server-Sent Events».
- Un puente de unas 50 líneas de JavaScript (`interfaz/compartido/puente_camara.js`) la aplica con `Plotly.relayout` sobre la gráfica que ya existe, sin redibujarla.
- **Por qué hace falta el puente** (se midió el 10-nov en Brave):
  - con los reruns de Streamlit la gráfica se actualiza 1-3 veces por segundo y se traba;
  - con el canal llega a unas 30 veces por segundo, con el navegador a 60 fps.
  - El equipo aprobó este único JS.

### E.6 Cómo se detiene

- Botón **«⏹ Detener y apagar cámara»**: libera la cámara (`cap.release()`), cierra el modelo y el canal.
- **Al cambiar de módulo o cerrar la pestaña**, se detiene solo. El panel envía un «latido» cada 0,5 s; con **4 s sin latido**, el hilo libera la cámara (perro guardián).
- **Ante cualquier error** (no hay cámara, está ocupada o Windows no da permiso) se apaga y se muestra un mensaje con la solución.

### E.7 Cómo se conserva el ratón

- El puente no bloquea la gráfica: **el ratón funciona siempre** (rotar, zoom, desplazar, «Restablecer vista», ver valores).
- Cuando el ratón mueve la vista, el puente la envía a Python (`POST /raton`). La siguiente pinza continúa desde ahí, sin saltos.
- La figura tiene `uirevision` fija, así que un rerun de Streamlit no devuelve la gráfica a la vista inicial.
- **Si algo falla en la defensa**, se usa el ratón: la gráfica funciona igual.

### E.8 Rendimiento medido (10-nov, cámara real, Brave)

| Métrica | Valor |
|---|---|
| Fotogramas procesados | ~32 por segundo (22-34) |
| Detección | 18-28 ms por fotograma, en CPU |
| CPU del proceso | ~1 núcleo, de 12 hilos |
| Memoria | +54 MB con la cámara activa; estable durante 3 min; se libera al detener |
| Canal hacia la gráfica | ~30 cambios/s, navegador a 60 fps |

---

## F. Defensa: preguntas y respuestas

Las respuestas corresponden al código de `main` y a los PDF de la profesora.

### F.1 Métodos matemáticos

1. **¿Cómo clasifica Ax un sistema?**
   - Igual que en clase: cuenta las ecuaciones no nulas de la forma escalonada (el rango) y las compara con el número de incógnitas. Una fila [0 … 0 | c] con c ≠ 0 significa que no hay solución.
   - En el código: `_escalonar` cuenta los pivotes y `_rango_aumentada` detecta la fila 0 = c.

2. **¿Qué hace el programa si un pivote es cero?**
   - Como en clase, busca debajo una fila con elemento no nulo y la intercambia (F₁ ↔ F₂). Queda registrado el motivo.
   - Si no hay ninguna, esa variable es libre.

3. **¿Qué diferencia hay entre Gauss y Gauss-Jordan?**
   - Gauss deja la matriz escalonada (triangular superior) y despeja con sustitución hacia atrás.
   - Gauss-Jordan normaliza cada pivote a 1 y anula arriba y abajo, hasta llegar a la forma reducida, donde la solución se lee directamente.

4. **¿Por qué κ usa la norma ∞ y no la 1, como en la lámina?**
   - El enunciado exige κ∞ y su escala 10/100 (OFICIAL p. 2).
   - El procedimiento es el mismo de los 5 pasos de S7-21/09 p. 19.

5. **¿Qué significa κ = 16/5?**
   - Que un error relativo en b puede amplificarse hasta 3,2 veces en x.
   - Es menor que 10, así que la sensibilidad es baja.

6. **¿Por qué las ecuaciones normales dan la mejor aproximación?**
   - x̂ minimiza ‖Ax − b‖₂. En el mínimo, el residuo es ortogonal a las columnas de A: Aᵀ(b − Ax̂) = 0, y de ahí AᵀAx̂ = Aᵀb.
   - Ax lo comprueba: Aᵀr = 0.

7. **La profesora resolvió el sistema normal con Cramer. ¿Por qué ustedes con Gauss?**
   - El enunciado pide resolverlo «con un método directo ya implementado».
   - Ax muestra además Cramer, como en S8-30/09 p. 7, y da lo mismo: (65/33, −29/33).

8. **¿Por qué Gauss-Seidel suele converger más rápido que Jacobi?**
   - Porque usa cada componente nueva en cuanto la calcula.
   - En la tridiagonal [−1, 4, −1]: Jacobi necesita 7 iteraciones y Gauss-Seidel 5, con ε = 10⁻³.

9. **¿Qué garantiza la convergencia?**
   - ρ(T) < 1 es la condición necesaria y suficiente para que converja con cualquier x⁽⁰⁾.
   - La dominancia diagonal estricta es solo **suficiente**: si falla, el método aún puede converger.

10. **¿Cómo calculan ρ(T)?**
    - Como en S9-07/10: T = −D⁻¹(L + U) (o −(D + L)⁻¹U), det(T − λI) = 0 y ρ = máx|λ|.
    - En 3×3 se muestra el desarrollo de Sarrus.
    - Para cualquier n y para las raíces se usan dos extensiones: Faddeev-LeVerrier y Durand-Kerner.

11. **En la hoja de S9-07/10 sale ρ = 0. ¿Por qué Ax da 1,174?**
    - Porque el desarrollo de Sarrus tiene el término det(T) = 4/3, que en la hoja se tachó.
    - El polinomio correcto es −λ³ − (4/9)λ + 4/3. Tiene raíces complejas de módulo 1,174, así que **no converge**.

12. **¿Qué es SOR y qué hace ω?**
    - Mezcla el valor anterior con el de Gauss-Seidel: (1 − ω)x⁽ᵏ⁾ + ω·x^GS, como en el manuscrito de S8-30/09.
    - ω = 1 es Gauss-Seidel; ω > 1 acelera (sobrerrelajación). Ax exige 0 < ω < 2.

### F.2 Decisiones de implementación

13. **¿Por qué fracciones en unos módulos y float en otros?**
    - Con fracciones, Gauss, la inversa, κ y los mínimos cuadrados son **exactos**, y la clasificación no depende de redondeos.
    - Los iterativos son aproximaciones y con fracciones los números crecerían sin límite.

14. **¿Usaron bibliotecas que resuelvan los métodos?**
    - No. El núcleo solo usa la biblioteca estándar. Streamlit, Plotly, Matplotlib y MediaPipe solo sirven para la interfaz, las gráficas y la cámara.
    - Ningún archivo importa NumPy, SciPy ni SymPy.

15. **¿Cómo saben que los resultados son correctos?**
    - Hay 281 pruebas, con valores esperados calculados aparte.
    - La auditoría aleatoria, con oráculos independientes (Leibniz, adjunta, Cramer, Gelfand), da 0 fallos.
    - La aplicación se autoverifica. No usamos los resultados de las láminas como referencia, porque varios tienen errores.

16. **¿Qué pasa con una entrada inválida?**
    - Aparece un mensaje con la celda exacta (`ErrorEntrada`) y el botón queda bloqueado si las dimensiones no cuadran.
    - El Módulo IV nunca lanza excepciones: devuelve un código, por ejemplo `DIAGONAL_CERO`.
    - La aplicación nunca se cierra.

17. **¿Por qué el error del criterio es el máximo y no la suma, como en el manuscrito?**
    - Porque la norma ∞ es el máximo. La suma que aparece en S8-30/09 p. 20 es la norma 1.
    - Ax sigue la definición (S8-30/09 p. 6).

### F.3 Arquitectura

18. **¿Cómo está organizado el código?**
    - Hay tres capas, más `gestos/`:
      - `algebra/` (una carpeta por módulo y `compartido/`);
      - `interfaz/` (pantallas);
      - `visualizacion/` (gráficas).
    - El núcleo no depende de la interfaz.

19. **Muéstreme dónde está Jacobi.**
    - `algebra/modulo_IV_iterativos/metodos.py` → `paso_jacobi`.
    - El bucle y los criterios están en `ejecucion.py` → `ejecutar`.

20. **¿Por qué el Módulo II usa el Gauss-Jordan del Módulo I?**
    - El enunciado pide la inversa «con un algoritmo implementado por el grupo».
    - No se duplicó código: II, III y IV reutilizan el Módulo I.

### F.4 Gráficas

21. **¿Las gráficas calculan algo?**
    - No. `visualizacion/` solo dibuja los resultados que entrega `algebra/`.
    - Hay una prueba que compara los datos dibujados con los del núcleo.

22. **¿Qué muestra la gráfica 3D?**
    - Cada ecuación es un plano y la solución es su intersección: un punto, una recta o nada (S6-14/09 p. 26).
    - Se puede rotar, acercar y ver las coordenadas al pasar el cursor.

23. **¿Qué gráficas hay en el Módulo IV y cómo se exploran?**
    - El error frente a la iteración (lo exige el enunciado).
    - La comparación superpuesta de los tres métodos.
    - Los autovalores con el círculo unidad.
    - El efecto del precondicionador.
    - Se exploran así:
      - ⛶ las amplía a pantalla completa;
      - un **clic en un punto** o el deslizador «Iteración a explorar» muestran k, x⁽ᵏ⁾, d_k y r_k;
      - un recuadro lista varias iteraciones;
      - «Destacar método» sigue una sola curva en la comparación.
    - Los rótulos salen del motivo real de parada: «Criterio A cumplido en k = 7» o «Se alcanzó k_max sin cumplir el criterio». Nunca se marca convergencia que no ocurrió.

### F.5 MediaPipe

24. **¿Se graba o se envía su imagen a internet?**
    - No. Cada fotograma se procesa en memoria y se descarta.
    - El modelo corre en este equipo. Solo 9 números van del servidor local (127.0.0.1) a la gráfica.

25. **¿Cómo distingue un puño de una pinza?**
    - En ambos el pulgar queda cerca del índice, pero en la pinza la punta del índice está fuera de la palma.
    - Todo se mide en unidades de palma.

26. **¿Por qué no tiembla la gráfica?**
    - Por el suavizado exponencial, la zona muerta acumulada, el antirrebote y la histéresis.

27. **¿Qué pasa si cambio de módulo con la cámara encendida?**
    - Sin el latido de la página, a los 4 s se apaga y se libera la cámara.

28. **¿Por qué hay JavaScript si el proyecto es en Python?**
    - Medimos que, sin él, la gráfica se actualiza 1-3 veces por segundo.
    - El puente de unas 50 líneas solo aplica la cámara; toda la visión y los gestos son Python.

29. **¿Hacia dónde se mueve la vista con la pinza?**
    - Horizontal: la escena gira hacia donde va la mano.
    - Vertical (invertido a pedido del equipo): mano arriba baja la vista y mano abajo la sube.

### F.6 Los cinco incentivos (OFICIAL p. 5; el puntaje lo decide la docente)

| Incentivo (máx.) | Qué pide | Qué tiene Ax | Cómo demostrarlo |
|---|---|---|---|
| Visualización avanzada (1 %) | Gráficas comparativas, historial o reportes exportables | Comparación superpuesta de los 3 métodos (e, d o r); historial d_k/r_k; **CSV** con precisión completa; autovalores; planos 3D | IV → «Comparar» y botón CSV |
| Precondicionamiento (1,5 %) | Precondicionador diagonal + comparación documentada | M = D, B = D⁻¹A; κ(A) frente a κ(B); T y c **idénticas** en Jacobi, GS y SOR (demostrado exactamente); Richardson (Cat. C): ρ 4,618 → 0,405 | IV → «Precondicionamiento diagonal» con la tridiagonal |
| Matrices dispersas (1 %) | Tratamiento eficiente + explicación de la estrategia | CSR propio: `valores`, `columnas`, `inicio`; memoria 2·nnz + n + 1; costo O(nnz) por iteración | IV → casilla CSR (muestra las tres listas) |
| Experiencia de usuario (0,5 %) | Accesibilidad, ayuda contextual o interacción sustantiva | Editor de rejilla con validación previa; errores con la celda exacta; sugerencia de reordenamiento; distintivos Cat.; **control gestual** | I → panel de gestos; IV → reordenamiento |
| Extensión matemática (1 %) | Funcionalidad pertinente, correcta y defendida | ρ(T) para n ≤ 8 con autovalores complejos (Faddeev-LeVerrier + Durand-Kerner); decisiones exactas (λ = ±1); T de SOR | IV → «Convergencia» con el ejemplo de S9-07/10 |

30. **¿Por qué el precondicionador no acelera Jacobi, si la lámina dice que sí?**
    - Con M = D, la diagonal de D⁻¹A es 1, así que T̃_J = −D⁻¹(L + U) = T_J: las iteraciones son idénticas.
    - Jacobi, GS y SOR ya dividen entre aᵢᵢ.
    - Por eso mostramos el efecto real en κ y en Richardson, que sí cambia.

31. **¿Richardson lo vimos en clase?**
    - No, profesora. Es una extensión, rotulada así en la aplicación.
    - Precondicionado con M = D se convierte exactamente en Jacobi.

32. **¿Qué es CSR y por qué ahorra?**
    - Guarda solo los no nulos: los valores, su columna y dónde empieza cada fila (S9-05/10 p. 9).
    - Cada iteración recorre nnz elementos en lugar de n².

33. **Explique Faddeev-LeVerrier en una frase.**
    - Obtiene los coeficientes de det(λI − T) solo con productos de matrices y trazas: cₖ = −tr(T·Mₖ)/k.
    - En 3×3 da el mismo polinomio que Sarrus.

34. **Explique Durand-Kerner en una frase.**
    - Aproxima todas las raíces a la vez, corrigiendo cada una como en Newton pero «separándola» de las demás: zᵢ ← zᵢ − p(zᵢ)/Π(zᵢ − zⱼ).

---

## G. Plan de estudio y hoja de repaso

**Reparto sugerido (unas 3 horas por persona):**

| Integrante | Profundizar en | Leer en el código |
|---|---|---|
| Elmer | Módulo I y la parte C (notación de clase) | `directos.py` |
| Samir | Módulos II y III | `condicion.py`, `minimos.py` |
| Daniel | Módulo IV: métodos, criterios y convergencia | `metodos.py`, `ejecucion.py`, `espectral.py` |
| Derek | Incentivos, arquitectura y MediaPipe | `precondicionamiento.py`, `dispersas.py`, `gestos/` |

**Todos deben saber explicar:**

- las fórmulas de la parte B;
- las extensiones de C.4;
- las preguntas 1, 9, 13, 14, 30 y 31.

**Hoja de repaso (memorizar):**

- Clasificación: rango(A) vs rango([A|b]) vs n. **Sol = {(…)}**.
- κ∞ = ‖A‖∞‖A⁻¹‖∞; escala < 10 / < 100 / ≥ 100; ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖.
- AᵀAx̂ = Aᵀb; r = b − Ax̂; Aᵀr = 0; ‖r‖₂.
- Jacobi, GS, SOR por componentes; T_J = −D⁻¹(L + U); T_GS = −(D + L)⁻¹U; ρ(T) < 1 ⇔ converge.
- Criterio A: ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε.
- Extensiones (Cat. C): Richardson, Faddeev-LeVerrier, Durand-Kerner, T de SOR, pivoteo parcial.
- Gestos: palma activa, pinza gira (vertical invertido), dos pinzas hacen zoom, puño pausa, victoria restablece; botón «Detener»; ratón siempre disponible.

**Antes de la defensa:**

- Instalar en su propia computadora: `ejecutar.bat`, o `pip install -r requirements.txt`.
- Correr las pruebas: 281 OK.
- Practicar la demostración de cada módulo con los ejemplos precargados.
- Probar los gestos con la mano y la luz del aula.
