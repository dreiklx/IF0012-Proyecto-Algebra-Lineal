# Guía express del proyecto Ax — IF0012 Álgebra Lineal
**Versión:** 12-nov-2026.
**Grupo 01:** Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez.

Repaso breve para la defensa. La guía completa (`docs/guia_estudio_if0012.md`) tiene las explicaciones largas; esta trae lo necesario para responder. **Cat.** = A visto en clase · B exigido por el enunciado · C extensión · D sin respaldo. Citas: «S8-30/09 p. 20» = PDF de clase; «OFICIAL p. 2» = enunciado.

## Índice

- A. Proyecto
- B. Módulo I · Sistemas lineales
- C. Módulo II · Condicionamiento
- D. Módulo III · Mínimos cuadrados
- E. Módulo IV · Iterativos
- F. Arquitectura
- G. MediaPipe
- H. Rúbrica e incentivos
- I. Defensa

---

## A. Proyecto

**Ax** es una aplicación web local (Streamlit, `http://localhost:8501`) que resuelve y analiza sistemas lineales con los métodos del curso, implementados desde cero. El enunciado prohíbe bibliotecas que calculen Gauss, Gauss-Jordan, determinantes, inversas, mínimos cuadrados, Jacobi, Gauss-Seidel, SOR o radio espectral (OFICIAL p. 1).

| Módulo | Pregunta | Aritmética |
|---|---|---|
| I | ¿Ax = b tiene solución única, infinitas o ninguna? | Fracciones exactas |
| II | ¿Qué tan sensible es x a errores en b? (κ∞) | Fracciones exactas |
| III | Sin solución exacta, ¿cuál es la mejor aproximación? | Fracciones exactas |
| IV | ¿Cómo aproximar x iterando? ¿Converge? ¿Cuál es más rápido? | Punto flotante |

**Flujo:** el usuario escribe → `interfaz/` valida → `algebra/` calcula → `interfaz/` muestra → `visualizacion/` dibuja. **Ninguna gráfica recalcula nada.**

**Por qué dos aritméticas:** con fracciones, un pivote es 0 solo si es realmente 0. Los iterativos paran por tolerancia; con fracciones los denominadores crecerían sin control.

**Tecnologías:** Python con `fractions`, `math` y `cmath` (núcleo); Streamlit 1.66 y Plotly 6.3 (interfaz y gráficas); MediaPipe 1.2.2 y OpenCV (gestos); Matplotlib solo como referencia en pruebas. Ningún archivo importa NumPy, SciPy ni SymPy.

---

## B. Módulo I · Sistemas lineales (Cat. A y B)

**Procedimiento de clase** (S6-14/09 p. 28; S6-16/09 p. 29):

1. Formar la aumentada [A | b].
2. Por cada columna, buscar pivote no nulo; si es 0, intercambiar filas (F₁ ↔ F₂).
3. Anular debajo del pivote: **«−2F₁ + F₂»** (a F₂ súmele −2·F₁).
4. **Gauss:** escalonar y sustituir hacia atrás. **Gauss-Jordan:** normalizar pivotes («(−1/3)F₃») y anular también arriba.
5. Clasificar y escribir **Sol = {(…)}**.

**Clasificación:**

| Rangos | Tipo |
|---|---|
| rango(A) < rango([A \| b]) (fila «0 = c», c ≠ 0) | sin solución |
| rango(A) = rango([A \| b]) = n | solución única |
| rango(A) = rango([A \| b]) < n | infinitas: x = xₚ + t₁v₁ + …, con n − rango variables libres |

**Determinante:** det(A) = (−1)^intercambios × producto de pivotes (S2-19/08 p. 38).

**Código:** `algebra/modulo_I_sistemas/directos.py`
- `resolver_gauss`, `resolver_gauss_jordan`: entradas del módulo.
- `_escalonar`: pivotes, intercambios y eliminación; registra cada paso con la notación de clase.
- `_rango_aumentada`: detecta «0 = c».
- `_sustitucion_atras`: despeja desde la última ecuación.
- `inversa_gauss_jordan`, `determinante`, `solucion_unica`: los reutilizan II, III y IV.

**Ejemplo (S6-16/09 p. 29):** x + y + z = 6; 2x + y − z = 3; −x + y + 2z = 7 → **Sol = {(1/3, 4, 5/3)}**, det(A) = 3, b − Ax = 0.

**Debe explicar:** diferencia Gauss / Gauss-Jordan; qué hace con un pivote 0; cómo clasifica; por qué fracciones.

---

## C. Módulo II · Condicionamiento (Cat. A y B)

**Procedimiento de 5 pasos** (S7-21/09 p. 19):

1. Norma **∞** (OFICIAL p. 2): suma de valores absolutos por **fila**, máximo.
2. ‖A‖∞.
3. A⁻¹ por Gauss-Jordan [A | I] → [I | A⁻¹]; verificar A·A⁻¹ = I.
4. ‖A⁻¹‖∞.
5. **κ∞(A) = ‖A‖∞ · ‖A⁻¹‖∞.**

**Fórmulas:**
- Escala del enunciado (Cat. B): κ < 10 baja; 10 ≤ κ < 100 moderada; κ ≥ 100 alta.
- Cota: ‖Δx‖∞/‖x‖∞ ≤ κ∞(A) · ‖Δb‖∞/‖b‖∞.
- Perturbación porcentual (interpretación propia, Cat. B): Δbᵢ = (p/100)·bᵢ.

**Código:** `algebra/modulo_II_condicionamiento/condicion.py`: `numero_condicion_infinito`, `clasificar_kappa`, `construir_delta_b`, `analizar_perturbacion`. Sumas por fila: `algebra/compartido/matriz.py`.

**Ejemplo (S7-21/09 p. 19):** B = [[1, 2], [3, 1]]; ‖B‖∞ = 4; B⁻¹ = [[−1/5, 2/5], [3/5, −1/5]]; ‖B⁻¹‖∞ = 4/5; **κ∞ = 16/5 ≈ 3,2**: sensibilidad baja.

**Debe explicar:** «con κ = 3,2, un error del 1 % en b da como máximo 3,2 % en x»; por qué norma ∞.

---

## D. Módulo III · Mínimos cuadrados (Cat. A y B)

**Problema:** si m > n y b ∉ Col(A), no hay solución exacta. Se busca x̂ que minimiza ‖Ax − b‖₂.

**Procedimiento** (S8-30/09 pp. 5-7):
1. Comprobar que b es independiente de las columnas: si m = n + 1, det[A | b] ≠ 0 (Sarrus).
2. Plantear **AᵀAx̂ = Aᵀb** (ecuaciones normales).
3. Resolver. La profesora usa **Cramer**: D = det(AᵀA), x̂ᵢ = Dᵢ/D (S8-30/09 p. 4).

El enunciado pide un método directo ya implementado (B). **Ax resuelve con Gauss** y muestra Cramer como verificación (A).

**Fórmulas:**
- r = b − Ax̂; ‖r‖₂ = √(Σrᵢ²).
- Aᵀr = 0: el residuo es ortogonal a Col(A). De ahí salen las ecuaciones normales.
- Recta y = mx + c: matriz de diseño con filas [xᵢ, 1].

**Código:** `algebra/modulo_III_minimos/minimos.py`: `clasificar_forma`, `minimos_cuadrados`, `cramer`, `ajuste_lineal`. **Gráfica obligatoria:** `visualizacion/interactivas.py::ajuste`.

**Ejemplo (S8-30/09 pp. 6-7):** x + 3y = −1; 3x − 2y = 8; −2x + 5y = −8.
- det[A | b] = −11 ≠ 0.
- AᵀA = [[14, −13], [−13, 38]]; Aᵀb = (39, −59).
- D = 363, D₁ = 715, D₂ = −319 → **x̂ = (65/33, −29/33)**, igual por Gauss y Cramer.

**Debe explicar:** por qué no hay solución exacta; qué mide el residuo; por qué Gauss y no Cramer.

---

## E. Módulo IV · Iterativos (Cat. A, B y C)

Con A = D + L + U (L y U estrictamente triangulares):

| Método | Fórmula por componentes |
|---|---|
| Jacobi | xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ_{j≠i} aᵢⱼxⱼ⁽ᵏ⁾)/aᵢᵢ |
| Gauss-Seidel | igual, pero usa xⱼ⁽ᵏ⁺¹⁾ para j < i en cuanto están calculados |
| SOR | xᵢ⁽ᵏ⁺¹⁾ = (1 − ω)xᵢ⁽ᵏ⁾ + ω·xᵢ^GS. ω = 1 → Gauss-Seidel; 0 < ω < 1 subrelajación; 1 < ω < 2 sobrerrelajación |
| Richardson (**C**) | x⁽ᵏ⁺¹⁾ = x⁽ᵏ⁾ + (b − Ax⁽ᵏ⁾) |

**Despejes:** cada método se muestra despejando cada incógnita (S8-30/09 p. 19: x₁⁽ᵏ⁺¹⁾ = (22 − 2x₂⁽ᵏ⁾ − x₃⁽ᵏ⁾)/6).

**Inicio x⁽⁰⁾:** cero, xᵢ⁽⁰⁾ = bᵢ/aᵢᵢ (convención de la profesora) o personalizado.

**Criterios de parada:**

| Criterio | Condición | Nombre en Ax |
|---|---|---|
| A (S8-28/09 p. 6) | Ax: ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε (absoluta). La lámina escribe la **relativa** ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖/‖x⁽ᵏ⁾‖ | dₖ (cambio entre iteraciones) |
| B | ‖b − Ax⁽ᵏ⁾‖∞ < ε | rₖ (residuo) |
| C | N iteraciones fijas | **no demuestra convergencia** |

Siempre hay un máximo k_max. El motivo de parada sale del código de terminación real («Criterio A cumplido», «Máximo de iteraciones sin cumplir el criterio», «Elemento diagonal nulo»…).

**Convergencia:**
- **Dominancia diagonal estricta por filas:** |aᵢᵢ| > Σ_{j≠i}|aᵢⱼ|. Es **suficiente, no necesaria**. Si falla, reordenar (S9-05/10 pp. 32-33).
- **Pasos de clase (S9-07/10 pp. 3-7):**
  1. A = D + L + U.
  2. D⁻¹ o (D + L)⁻¹.
  3. T_J = −D⁻¹(L + U); T_GS = −(D + L)⁻¹U.
  4. C_J = D⁻¹b; C_GS = (D + L)⁻¹b.
  5. det(T − λI) = 0 por Sarrus; ρ(T) = máx|λ|.
- **Teorema:** x⁽ᵏ⁺¹⁾ = Tx⁽ᵏ⁾ + C converge para todo x⁽⁰⁾ **si y solo si ρ(T) < 1**. Menor ρ → más rápido.
- **Comparación:** mismos datos para los tres métodos; error final ‖x⁽ᵏ⁾ − x*‖∞ en escala logarítmica (S9-05/10 p. 17).

**Código:** `algebra/modulo_IV_iterativos/`
- `metodos.py`: `paso_jacobi`, `paso_gauss_seidel`, `paso_sor`, `paso_richardson`.
- `ejecucion.py`: `ConfiguracionIterativa`, `ejecutar` (bucle común, criterios; no lanza excepciones).
- `convergencia.py`: `dominancia_diagonal`, `reordenamiento_dominante`.
- `matriz_iteracion.py`: `descomponer`, `matriz_iteracion`, `desarrollo_sarrus`.
- `polinomio_raices.py`: Faddeev-LeVerrier y Durand-Kerner (C).
- `espectral.py`: `radio_espectral`, `concluir`.
- `comparacion.py`: `comparar_metodos`. `dispersas.py` (CSR) y `precondicionamiento.py`: incentivos.

**Gráficas obligatorias:** `interactivas.convergencia` (dₖ y rₖ frente a k, con ε) e `interactivas.comparacion`.

**Ejemplos:**
- Tridiagonal [−1, 4, −1] 4×4, b = (1, 0, 0, 1), ε = 10⁻³, x⁽⁰⁾ = 0, ω = 1,2: Jacobi 7 iteraciones, Gauss-Seidel 5, SOR 7 (criterio A absoluto de Ax; con la relativa de la lámina serían 8 y 6). Solución (1/3, 1/15, 1/15, 1/3) (S9-05/10 p. 14).
- S9-07/10, Jacobi con A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]]: det(T − λI) = −λ³ − (4/9)λ + 4/3; **ρ ≈ 1,174 > 1: no converge.** La hoja dice ρ = 0 (errata: omite el 4/3).

**Debe explicar:** por qué Gauss-Seidel suele ser más rápido; qué es dₖ y qué es rₖ; por qué la dominancia no basta para decidir no convergencia; qué es ρ(T).

**Erratas de las láminas (Ax muestra el valor correcto):**

| Fuente | Dice | Correcto |
|---|---|---|
| S2-19/08 pp. 42-43 | det = 42 | 15 |
| S3-26/08 p. 26 | ‖x‖₂ ≤ ‖x‖∞ ≤ ‖x‖₁ | ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ |
| S6-14/09 p. 29 | (1/2, −1, −1) | (19/20, −5/4, −7/20) |
| S7-21/09 p. 14 | (100, −97) | (100/101, 203/101) |
| S8-30/09 p. 20 | T₁ = 2,402 «‖·‖∞» | es la norma 1; la ‖·‖∞ es 1,889 |
| S9-05/10 p. 23 | M = D converge más rápido en Jacobi | iteraciones **idénticas** |
| S9-07/10 p. 4 | ρ(T_J) = 0 | ≈ 1,174 |
| S9-07/10 p. 7 | C_GS = −(D + L)⁻¹b | C_GS = (D + L)⁻¹b |

---

## F. Arquitectura

```text
app.py → paginas/ → interfaz/modulos/<módulo>.mostrar()
                        │            │             │
                        ▼            ▼             ▼
             interfaz/compartido/  algebra/     visualizacion/
             (editor, LaTeX,       (calcula)    (dibuja con Plotly)
              estilo, gestos)        │
                                     ▼
                       algebra/compartido/ (matriz, validacion, exactos)
```

| Carpeta | Contenido |
|---|---|
| `algebra/` | Núcleo matemático: una carpeta por módulo + `compartido/`. No importa interfaz ni bibliotecas externas |
| `interfaz/` | Pantallas. No calcula. `modulos/`, `compartido/` (editor, `formulas.py`, `componentes.py`), `navegacion.py` |
| `visualizacion/` | Gráficas Plotly (`interactivas.py`), notación (`notacion.py`), datos (`datos_graficas.py`) |
| `gestos/` | Control gestual con cámara. No importa `algebra/` |
| `tests/` | 295 pruebas, una carpeta por módulo |
| `auditoria/` | Verificación aleatoria independiente |
| `docs/` | Documentación, guías y auditorías |
| `herramientas/` | Generadores de HTML. Solo desarrollo; no entran en el ZIP |

**Reglas:** `algebra/` no importa interfaz; `gestos/` no importa `algebra/`; no hay ciclos de importación. El Módulo I es la base de II, III y IV.

**Verificación:** 295 pruebas; auditoría aleatoria con 0 fallos (4500 sistemas, 400 inversas/determinantes/κ, 200 perturbaciones, 300 mínimos cuadrados, 600 iteraciones, 300 espectrales, 150 precondicionadores).

---

## G. MediaPipe (Cat. C, incentivo de experiencia de usuario)

Gira y acerca la **gráfica 3D de planos del Módulo I**. **No calcula nada del álgebra.**

**Bibliotecas:** MediaPipe 1.2.2 (Hand Landmarker, API Tasks) y OpenCV (cámara). El modelo `hand_landmarker.task` va dentro del proyecto; funciona sin internet.

```text
cámara ─► captura.py ─► deteccion.py ─► interpretacion.py ─► movimiento.py ─► servidor.py ─► puente JS ─► Plotly
(OpenCV)   fotograma     21 puntos        gesto estable        cámara θ, φ, r   127.0.0.1, SSE   relayout
```

**Detección:** 21 puntos por mano (0 = muñeca, 4 = punta del pulgar, 8 = punta del índice). Las distancias se dividen por el tamaño de la palma, así que funciona a cualquier distancia.

| Gesto | Acción |
|---|---|
| ✋ Palma abierta (½ s) | Activa y **calibra** la pinza |
| 🤏 Pinza pulgar-índice | Agarrar y girar. Vertical invertido: mano arriba baja la vista |
| 🤏🤏 Pinza con dos manos | **Zoom**: separarlas acerca |
| ✊ Puño (½ s) | **Pausa** (se reanuda con la palma) |
| ✌️ Victoria (≈ 1 s) | **Restablece** la vista |

**Módulo IV (2D):** los mismos gestos mueven el rango visible de la gráfica de convergencia (una pinza desplaza, dos pinzas acercan o alejan, puño pausa, victoria restablece). No cambian datos, criterios ni iteraciones. Un solo objetivo activo a la vez. Documento: `docs/mediapipe_2d.md`. **Probado solo con datos sintéticos**; la validación con mano real la hace el equipo.

**Estabilidad:** antirrebote (0,35 s; victoria 0,8 s); histéresis (la pinza sale con 1,5× el umbral de entrada); calibración del umbral entre 0,18 y 0,25; suavizado s ← s + 0,35(x − s); zona muerta acumulada.

**Conexión con Plotly:** `servidor.py` (solo 127.0.0.1, con token) envía la cámara ~30 veces por segundo; `puente_camara.js` (~50 líneas) la aplica con `Plotly.relayout`. Sin el puente, Streamlit daba 1-3 actualizaciones por segundo. El ratón funciona siempre.

**Privacidad:**
- La cámara solo se enciende con el botón «Activar cámara y gestos».
- El fotograma se procesa en memoria y se descarta. No se graba ni se envía. Al navegador llegan 9 números.
- Se apaga con «⏹ Detener», al cambiar de módulo, al cerrar la pestaña (4 s sin latido) o ante un error.

**Medido (10-nov, Brave):** ~32 fotogramas/s; detección 18-28 ms; ~1 núcleo de CPU; +54 MB de memoria, liberados al detener.

---

## H. Rúbrica e incentivos (OFICIAL pp. 4-5)

**Requisitos obligatorios:**

| Criterio (peso) | Dónde se demuestra |
|---|---|
| Módulo I (8 %) | Ejemplo S6-16/09, pasos «−2F₁ + F₂», Sol = {…}; casos «infinitas» e «inconsistente» |
| Módulo II (8 %) | Ejemplo S7-21/09 p. 19, 5 pasos, perturbación, cota |
| Módulo III (8 %) | S8-30/09 con Cramer igual; pestaña «Ajuste» con gráfica |
| Módulo IV (8 %) | Despejes, tabla, motivo, gráfica de error, «Comparar», «Convergencia» |
| Procedimiento (7 %) | Paso a paso en I-IV con la notación de la profesora |
| Análisis (6 %) | Mensajes de interpretación en cada módulo |
| Código (5 %) | Parte F; `docs/mapa_completo_del_codigo.md` |
| Validaciones (4 %) | Editor con validación previa; errores con la celda exacta; diagonal nula; singularidad |
| Interfaz (5 %) | Navegación superior, ejemplos precargados, ayudas |
| Manual (3 %) y casos (3 %) | `docs/manual_usuario.md`, `casos_prueba/` |

**Gráficas:** el enunciado exige solo la de III (datos y recta) y la de IV (error frente a iteración). Las de I, los autovalores y el precondicionador son opcionales (`docs/cumplimiento_graficas.md`).

**Cinco incentivos** (el puntaje lo decide la docente):

| Incentivo (máx.) | Qué tiene Ax | Cómo demostrarlo |
|---|---|---|
| Visualización avanzada (1 %) | Comparación superpuesta, historial explorable, CSV, autovalores, planos 3D | IV → «Comparar»; «Ejecutar» → CSV |
| Precondicionamiento (1,5 %) | M = D; κ(A) frente a κ(B); T y c **idénticas** en Jacobi, GS y SOR; Richardson ρ 4,618 → 0,405 | IV → «Precondicionamiento» |
| Matrices dispersas (1 %) | CSR propio; memoria 2·nnz + n + 1; O(nnz) por iteración | IV → casilla «CSR» |
| Experiencia de usuario (0,5 %) | Editor de rejilla; sugerencia de reordenamiento; distintivos Cat.; control gestual | I → panel de gestos; IV → «Convergencia» |
| Extensión matemática (1 %) | ρ(T) para n ≤ 8 con complejas; decisiones exactas; T de SOR | IV → «Convergencia» con S9-07/10 |

---

## I. Defensa

**Preguntas probables:**

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Cómo clasifica? | Cuenta ecuaciones no nulas de la forma escalonada (rango) y compara con n; «0 = c» → sin solución |
| 2 | ¿Pivote 0? | Busca abajo una fila no nula e intercambia; si no hay, la variable es libre |
| 3 | ¿Gauss o Gauss-Jordan? | Gauss: escalonada + sustitución. Gauss-Jordan: forma reducida, se lee la solución |
| 4 | ¿Por qué norma ∞? | La exige el enunciado (OFICIAL p. 2) |
| 5 | ¿Qué significa κ = 16/5? | Error relativo en b se amplifica como mucho 3,2 veces en x; sensibilidad baja |
| 6 | ¿Por qué ecuaciones normales? | En el mínimo, el residuo es ortogonal a Col(A): Aᵀr = 0 ⇒ AᵀAx̂ = Aᵀb |
| 7 | La profesora usó Cramer, ¿por qué Gauss? | El enunciado pide un método directo implementado; Cramer se muestra como verificación |
| 8 | ¿Por qué GS es más rápido? | Usa cada componente nueva en cuanto la calcula (tridiagonal: 5 frente a 7 iteraciones) |
| 9 | ¿Qué garantiza convergencia? | ρ(T) < 1 es necesario y suficiente; dominancia diagonal solo suficiente |
| 10 | ¿Cómo se calcula ρ? | Pasos ①-⑤ de S9-07/10; 3×3 con Sarrus; cualquier n con Faddeev-LeVerrier y Durand-Kerner (C) |
| 11 | ¿Por qué 1,174 si la hoja dice 0? | La hoja omitió el término 4/3 del polinomio |
| 12 | ¿Qué hace ω? | Mezcla (1 − ω)x⁽ᵏ⁾ + ω·x^GS. 0 < ω < 2 no garantiza convergencia por sí solo |
| 13 | ¿Fracciones o float? | Exactas en I-III; float en IV (aproximación por tolerancia) |
| 14 | ¿Bibliotecas de álgebra? | No. Núcleo solo con la biblioteca estándar |
| 15 | ¿Cómo sabemos que es correcto? | 295 pruebas con valores calculados aparte; auditoría aleatoria con 0 fallos |
| 16 | ¿Entrada inválida? | Mensaje con la celda exacta; el Módulo IV devuelve códigos, no excepciones |
| 17 | ¿Por qué el máximo y no la suma (S8-30/09 p. 20)? | La norma ∞ es el máximo; la suma es la norma 1 |
| 18 | ¿Organización? | `algebra/` calcula, `interfaz/` muestra, `visualizacion/` dibuja, `gestos/` controla con cámara |
| 19 | ¿Dónde está Jacobi? | `metodos.py` → `paso_jacobi`; bucle y criterios en `ejecucion.py` → `ejecutar` |
| 20 | ¿Por qué II usa el Gauss-Jordan de I? | El enunciado pide un algoritmo del grupo; no se duplicó código |
| 21 | ¿Las gráficas calculan? | No. Dibujan datos del núcleo |
| 22 | ¿Qué gráficas son obligatorias? | Solo III y IV |
| 23 | ¿Cómo se explora la gráfica de convergencia? | Pantalla completa, clic en punto o deslizador, «Destacar método» |
| 24 | ¿Se graba la imagen? | No. Se procesa en memoria y se descarta |
| 25 | ¿Por qué M = D no acelera Jacobi? | D⁻¹A tiene diagonal 1: T̃_J = T_J, iteraciones idénticas |
| 26 | ¿Richardson se vio en clase? | No. Es extensión (C), rotulada así; con M = D se convierte en Jacobi |
| 27 | ¿Qué es CSR? | Guarda solo no nulos (valores, columnas, inicio de fila); O(nnz) por iteración |

**Errores que evitar:**
- Decir que Richardson, Faddeev-LeVerrier o Durand-Kerner se vieron en clase.
- Decir que la dominancia diagonal es **necesaria**.
- Decir que completar N iteraciones (criterio C) demuestra convergencia.
- Confundir dₖ, rₖ y el error real eₖ.
- Decir que 0 < ω < 2 garantiza convergencia de SOR.
- Usar como correcto un resultado de una lámina con errata.
- Decir que todos los módulos exigen gráfica: solo III y IV.
- Si la cámara falla: usar el ratón.

**Diferencias clase / extensión:**

| Clase (A) | Extensión (C) |
|---|---|
| Gauss, Gauss-Jordan, det, Sarrus, κ∞, ecuaciones normales, Jacobi, GS, SOR, criterios A-C, ρ(T) con 3×3, dominancia | Richardson, Faddeev-LeVerrier, Durand-Kerner, ρ para n ≤ 8, pivoteo parcial, CSR, precondicionador, MediaPipe, gráficas 2D de exploración |

**Repaso final:**
- **Clasificación:** rango(A) frente a rango([A | b]) frente a n; Sol = {(…)}.
- **κ∞:** ‖A‖∞ · ‖A⁻¹‖∞ (5 pasos); escala < 10 / < 100 / ≥ 100.
- **Mínimos cuadrados:** AᵀAx̂ = Aᵀb; r = b − Ax̂; Aᵀr = 0; Cramer x̂ᵢ = Dᵢ/D.
- **Iterativos:** T_J = −D⁻¹(L + U); T_GS = −(D + L)⁻¹U; ρ(T) < 1 ⇔ converge; criterio A ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε.
- **Gestos:** palma activa, pinza gira, dos pinzas zoom, puño pausa, victoria restablece.

**Antes de la defensa:** `ejecutar.bat`; `ejecutar_pruebas.bat` (295 OK); practicar cada módulo con los ejemplos precargados.
