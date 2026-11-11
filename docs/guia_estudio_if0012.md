# Guía de estudio del proyecto Ax — IF0012 Álgebra Lineal

**Versión:** 11-nov-2026.
**Grupo 01:** Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez.
**Fechas:** entrega 11-nov-2026; defensa individual la semana del 16-nov.
**Docente:** Prof. Imelda Sáenz Pineda.

Referencia compacta para repasar **todo** el proyecto antes de la defensa. Los cuatro integrantes deben conocer los cuatro módulos. Cada fórmula aparece una sola vez (en la parte B) y las demás partes remiten a ella. Todo corresponde al código de `main` y a los PDF de la profesora.

**Cómo citar:** «S8-30/09 p. 20» es la página 20 del PDF de clase del 30-09; «OFICIAL p. 2» es el enunciado del proyecto.

| Cat. | Significa | Frase para la defensa |
|---|---|---|
| **A** | Visto en clase | «Lo vimos en clase: S… p. …» |
| **B** | Exigido por el enunciado | «Lo pide el enunciado, OFICIAL p. …» |
| **C** | Extensión o incentivo, **no** visto en clase | «Es una extensión, rotulada así en la aplicación» |
| **D** | Sin respaldo | Ax no tiene ninguna |

## Índice

- A. Visión general
- B. Los cuatro módulos
- C. Extensiones
- D. Arquitectura
- E. MediaPipe
- F. Rúbrica e incentivos
- G. Defensa

---

## A. Visión general

**Qué es Ax:** una aplicación web **local** (Streamlit, `http://localhost:8501`) que resuelve y analiza sistemas lineales con los métodos del curso, **implementados desde cero**. El enunciado prohíbe bibliotecas que hagan Gauss, Gauss-Jordan, determinantes, inversa, mínimos cuadrados, Jacobi, Gauss-Seidel, SOR o radio espectral (OFICIAL p. 1).

| Módulo | Pregunta que responde | Aritmética |
|---|---|---|
| I · Sistemas lineales | ¿Ax = b tiene solución única, infinitas o ninguna? ¿Cuál es? | Fracciones exactas |
| II · Condicionamiento | ¿Qué tan sensible es x a errores en b? (κ∞) | Fracciones exactas |
| III · Mínimos cuadrados | Sin solución exacta, ¿cuál es la mejor aproximación? | Fracciones exactas |
| IV · Iterativos | ¿Cómo aproximar x con Jacobi, Gauss-Seidel y SOR? ¿Converge? ¿Cuál es más rápido? | Punto flotante |

**Por qué dos aritméticas:** con fracciones, un pivote es 0 solo si es realmente 0, así que la clasificación no depende de redondeos. Los iterativos son aproximaciones que paran por tolerancia; con fracciones los denominadores crecerían sin control.

**Cómo funciona:**

```text
el usuario escribe → interfaz/ valida → algebra/ calcula → interfaz/ muestra → visualizacion/ dibuja
```

La interfaz pide, el núcleo calcula y las gráficas dibujan. **Ninguna gráfica recalcula nada.**

| Tecnología | Uso | ¿Resuelve métodos del curso? |
|---|---|---|
| Python 3.11+ con `fractions`, `math`, `cmath` | Núcleo matemático | No: solo operaciones elementales |
| Streamlit 1.66 · Plotly 6.3 | Interfaz y gráficas interactivas | No |
| Matplotlib 3.11 | Solo en las pruebas, como figura de referencia | No |
| MediaPipe 1.2.2 + OpenCV 5.0 | Control gestual opcional de la gráfica 3D | No |

Ningún archivo del proyecto importa NumPy, SciPy ni SymPy.

---

## B. Los cuatro módulos

### B.1 Módulo I — Sistemas lineales (Gauss y Gauss-Jordan)

**Problema:** resolver Ax = b, mostrar cada operación elemental y clasificar el sistema.

**Procedimiento de clase** (S6-14/09 p. 28; S6-16/09 p. 29; S3-24/08 pp. 4-5):

1. Formar la matriz aumentada [A | b].
2. Para cada columna, buscar un pivote no nulo. Si es 0, intercambiar filas (F₁ ↔ F₂).
3. Anular debajo del pivote. La profesora escribe **«−2F₁ + F₂»**: a F₂ súmele −2 veces F₁.
4. **Gauss:** forma escalonada y sustitución hacia atrás. **Gauss-Jordan:** normaliza cada pivote («(−1/3)F₃») y anula también arriba, hasta la forma reducida.
5. Clasificar y escribir **Sol = {(…)}**.

**Fórmulas:**

- Multiplicador m = aᵢₖ/aₖₖ; la operación Fᵢ → Fᵢ − m·Fₖ se escribe «−m·Fₖ + Fᵢ».
- Clasificación («3 ecuaciones no nulas, 3 incógnitas → solución única»):

| Rangos | Tipo | Geometría (S6-14/09 p. 26) |
|---|---|---|
| rango(A) < rango([A \| b]): aparece «0 = c» con c ≠ 0 | sin solución | los planos no tienen punto común |
| rango(A) = rango([A \| b]) = n | única | se cortan en un punto |
| rango(A) = rango([A \| b]) < n | infinitas: x = xₚ + t₁v₁ + …, con n − rango variables libres | comparten una recta o un plano |

- det(A) = (−1)<sup>intercambios</sup> × (producto de los pivotes) (S2-19/08 p. 38).

**Código:** `algebra/modulo_I_sistemas/directos.py`

| Función | Qué hace |
|---|---|
| `resolver_gauss`, `resolver_gauss_jordan` | Entrada del módulo |
| `_escalonar` | El corazón: pivotes, intercambios, eliminación; registra cada `Paso` con su notación de clase |
| `_buscar_pivote` | «Primer no nulo» (como en clase) o pivoteo parcial (opción, Cat. C). Avisa si un pivote es «numéricamente problemático»: \|pivote\| < 10⁻¹⁰·máx\|aᵢⱼ\| (umbral propio para un requisito B) |
| `_rango_aumentada` | Detecta la fila 0 = c |
| `_sustitucion_atras` | Despeja desde la última ecuación |
| `inversa_gauss_jordan`, `determinante`, `solucion_unica` | Los reutilizan los módulos II, III y IV |

**Ejemplo** (S6-16/09 p. 29, precargado): x + y + z = 6, 2x + y − z = 3, −x + y + 2z = 7.

- −2F₁ + F₂ y F₁ + F₃; −F₂; −2F₂ + F₃; (−1/3)F₃.
- z = 5/3; y + 3(5/3) = 9 ⇒ y = 4; x = 6 − 4 − 5/3 = 1/3.
- **Sol = {(1/3, 4, 5/3)}**, det(A) = 3, verificación b − Ax = (0, 0, 0).

**Debe saber explicar:** la diferencia entre Gauss y Gauss-Jordan; qué hace con un pivote 0; cómo clasifica; por qué usa fracciones.

### B.2 Módulo II — Condicionamiento y sensibilidad

**Problema:** medir con κ∞(A) cuánto puede amplificarse un error en b, y comprobarlo perturbando b.

**Procedimiento de clase en 5 pasos** (S7-21/09 p. 19); Ax los muestra así:

1. Elegir la norma: **∞** (OFICIAL p. 2), la suma de valores absolutos por **fila**.
2. ‖A‖∞: «Fila 1: |1| + |2| = 3; Fila 2: |3| + |1| = 4» ⇒ ‖A‖∞ = máx{3, 4} = 4.
3. A⁻¹ por Gauss-Jordan [A | I] → [I | A⁻¹], verificando A·A⁻¹ = I.
4. ‖A⁻¹‖∞, en la misma norma.
5. κ∞(A) = ‖A‖∞ · ‖A⁻¹‖∞.

**Fórmulas:**

- Escala del enunciado (Cat. B): κ < 10 baja; 10 ≤ κ < 100 moderada; κ ≥ 100 alta. La lámina tiene 5 niveles, pero el enunciado fija estos 3.
- Cota (S7-21/09 p. 18): ‖Δx‖∞/‖x‖∞ ≤ κ∞(A) · ‖Δb‖∞/‖b‖∞.
- Perturbación porcentual (interpretación propia de un requisito B): Δbᵢ = (p/100)·bᵢ.

**Código:** `algebra/modulo_II_condicionamiento/condicion.py`: `numero_condicion_infinito`, `clasificar_kappa`, `construir_delta_b`, `analizar_perturbacion`. Las sumas por fila salen de `matriz.sumas_absolutas_por_fila`.

**Ejemplo** (S7-21/09 p. 19): B = [[1, 2], [3, 1]], ‖B‖∞ = 4, B⁻¹ = [[−1/5, 2/5], [3/5, −1/5]], ‖B⁻¹‖∞ = 4/5, **κ∞ = 16/5 ≈ 3,2**: sensibilidad baja.

**Debe saber explicar:** «con κ = 3,2, un error del 1 % en b produce como mucho un 3,2 % en x»; por qué se usa la norma ∞; por qué la inversa es nuestra.

### B.3 Módulo III — Mínimos cuadrados y ajuste lineal

**Problema:** si m > n y b ∉ Col(A) no hay solución exacta. Se busca el x̂ que minimiza ‖Ax − b‖₂.

**Procedimiento de clase** (S8-30/09 pp. 5-7):

1. Comprobar que b es **linealmente independiente** de las columnas de A: si m = n + 1, det[A | b] ≠ 0 (por Sarrus).
2. Plantear el sistema normal asociado **AᵀAx = Aᵀb**.
3. Resolverlo. La profesora usa **Cramer**: D = det(AᵀA), Dᵢ = det(Aᵢ), x̂ᵢ = Dᵢ/D (S8-30/09 p. 4).

El enunciado exige resolverlo «con un método directo ya implementado» (Cat. B). **Ax lo resuelve con Gauss** y muestra Cramer como verificación (Cat. A).

**Fórmulas:**

- r = b − Ax̂; ‖r‖₂ = √(Σrᵢ²).
- Aᵀr = 0: el residuo es ortogonal a las columnas de A. De ahí salen las ecuaciones normales: Aᵀ(b − Ax̂) = 0.
- Recta y = mx + c: matriz de diseño con filas [xᵢ, 1].

**Código:** `algebra/modulo_III_minimos/minimos.py`: `clasificar_forma`, `minimos_cuadrados`, `cramer`, `ajuste_lineal`. **Gráfica obligatoria:** `visualizacion/interactivas.py::ajuste` (datos, recta y residuos).

**Ejemplo** (S8-30/09 pp. 6-7): x + 3y = −1, 3x − 2y = 8, −2x + 5y = −8.

- det[A | b] = −11 ≠ 0.
- AᵀA = [[14, −13], [−13, 38]], Aᵀb = (39, −59).
- D = 363, D₁ = 715, D₂ = −319, así que **x̂ = (65/33, −29/33)**, igual por Gauss y por Cramer.

**Debe saber explicar:** por qué la solución no es exacta; qué mide el residuo; por qué Gauss y no Cramer.

### B.4 Módulo IV — Métodos iterativos y convergencia

**Problema:** aproximar x iterando, decidir cuándo parar, comparar los métodos y saber si convergen.

**Procedimiento de clase** (S8-30/09 pp. 15-33). Con A = D + L + U (L y U **estrictamente** triangulares):

1. **Despejar cada incógnita.** Ejemplo de S8-30/09 p. 19: x₁⁽ᵏ⁺¹⁾ = (22 − 2x₂⁽ᵏ⁾ − x₃⁽ᵏ⁾)/6. Ax muestra los despejes en «Ejecutar».
2. Elegir x⁽⁰⁾: cero, **xᵢ⁽⁰⁾ = bᵢ/aᵢᵢ** (convención de la profesora) o personalizado.
3. Iterar y verificar el criterio de parada.

| Método | Fórmula por componentes |
|---|---|
| Jacobi | xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ<sub>j≠i</sub> aᵢⱼxⱼ⁽ᵏ⁾)/aᵢᵢ |
| Gauss-Seidel | xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ<sub>j&lt;i</sub> aᵢⱼxⱼ⁽ᵏ⁺¹⁾ − Σ<sub>j&gt;i</sub> aᵢⱼxⱼ⁽ᵏ⁾)/aᵢᵢ: usa los valores nuevos en cuanto los calcula |
| SOR (S8-30/09 pp. 32-33) | primero xᵢ<sup>GS</sup> y después xᵢ⁽ᵏ⁺¹⁾ = (1 − ω)xᵢ⁽ᵏ⁾ + ω·xᵢ<sup>GS</sup>. Con ω = 1 es Gauss-Seidel; 0 < ω < 1 subrelajación; 1 < ω < 2 sobrerrelajación |

| Criterio | Condición | Nombre en Ax |
|---|---|---|
| A (S8-28/09 p. 6) | ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε | dₖ (en los manuscritos, la «tolerancia» T₁, T₂, …) |
| B | ‖b − Ax⁽ᵏ⁾‖∞ < ε | rₖ (residuo) |
| C | N iteraciones fijas | **no demuestra convergencia** |

Siempre hay un máximo de iteraciones k<sub>max</sub>. El motivo de parada sale del código de terminación: «Criterio A cumplido», «Máximo de iteraciones sin cumplir el criterio», «Elemento diagonal nulo»…

**Convergencia** (S8-30/09 p. 37; S9-07/10 pp. 3-7):

- **Dominancia diagonal estricta por filas:** |aᵢᵢ| > Σ<sub>j≠i</sub>|aᵢⱼ|. Es **suficiente**, no necesaria. Si no se cumple, reordenar las ecuaciones (S9-05/10 pp. 32-33).
- **Pasos de clase:**
  1. A = D + L + U;
  2. D⁻¹ (o (D + L)⁻¹);
  3. **T<sub>J</sub> = −D⁻¹(L + U)** o **T<sub>GS</sub> = −(D + L)⁻¹U**;
  4. **C<sub>J</sub> = D⁻¹b** o C<sub>GS</sub> = (D + L)⁻¹b;
  5. det(T − λI) = 0 por Sarrus y ρ(T) = máx{|λ|}.
- **Teorema:** x⁽ᵏ⁺¹⁾ = Tx⁽ᵏ⁾ + C converge para todo x⁽⁰⁾ **si y solo si ρ(T) < 1**. Cuanto menor es ρ, más rápido.
- **Comparación:** los tres métodos con la misma configuración; «error final» ‖x⁽ᵏ⁾ − x*‖∞ y gráfica logarítmica (S9-05/10 p. 17).

**Código:** `algebra/modulo_IV_iterativos/`

| Archivo | Contenido |
|---|---|
| `metodos.py` | `paso_jacobi`, `paso_gauss_seidel`, `paso_sor` (y `paso_richardson`, Cat. C) |
| `ejecucion.py` | `ConfiguracionIterativa`, `ejecutar`: bucle común, criterios, tabla y motivo; nunca lanza excepciones |
| `convergencia.py` | `dominancia_diagonal`, `reordenamiento_dominante` |
| `matriz_iteracion.py` | `descomponer`, `matriz_iteracion` (T, c y la inversa del paso 2), `desarrollo_sarrus` |
| `polinomio_raices.py` | Faddeev-LeVerrier y Durand-Kerner (Cat. C) |
| `espectral.py` | `radio_espectral`, `concluir` |
| `comparacion.py` | `comparar_metodos` |
| `dispersas.py`, `precondicionamiento.py` | Incentivos |

**Gráficas obligatorias:** `interactivas.convergencia` (dₖ y rₖ frente a k, con ε) y `interactivas.comparacion` (los tres métodos).

**Ejemplos:**

- Tridiagonal [−1, 4, −1] de 4×4, b = (1, 0, 0, 1), ε = 10⁻³, x⁽⁰⁾ = 0, ω = 1,2: Jacobi 7 iteraciones, Gauss-Seidel 5 y SOR 7. Solución (1/3, 1/15, 1/15, 1/3) (S9-05/10 p. 14).
- S9-07/10, A = [[3, 3, 3], [3, 3, 2], [−3, −2, 3]] con Jacobi: det(T − λI) = −λ³ − (4/9)λ + 4/3; **ρ(T<sub>J</sub>) ≈ 1,174 > 1: no converge**. La hoja dice ρ = 0 porque omite el término 4/3 (errata).

**Debe saber explicar:** por qué Gauss-Seidel suele ser más rápido; qué es dₖ y qué es rₖ; por qué la dominancia no basta para concluir que no converge; qué significa ρ(T).

### B.5 Erratas de las láminas (Ax muestra el valor correcto)

| Fuente | Dice | Correcto |
|---|---|---|
| S2-19/08 pp. 42-43 | det = 42 | 15 |
| S3-26/08 p. 26 | ‖x‖₂ ≤ ‖x‖∞ ≤ ‖x‖₁ | ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ |
| S6-14/09 p. 29 | (1/2, −1, −1) | (19/20, −5/4, −7/20) |
| S7-21/09 p. 14 | (100, −97) | (100/101, 203/101) |
| S8-30/09 p. 20 | T₁ = 2,402 «‖·‖∞» | esa suma es la norma 1; la ‖·‖∞ es 1,889 |
| S9-05/10 p. 23 | Jacobi con M = D converge más rápido | las iteraciones son **idénticas** |
| S9-07/10 p. 4 | ρ(T<sub>J</sub>) = 0 | ≈ 1,174: no converge |
| S9-07/10 p. 7 | C<sub>GS</sub> = −(D + L)⁻¹b | C<sub>GS</sub> = (D + L)⁻¹b |

Ninguna salida de una lámina se usó como resultado esperado sin recalcularla.

### B.6 Diferencias de presentación con la profesora (documentadas)

- **Gauss:** Ax sigue la lámina S6-14/09 (multiplicadores sin normalizar). El manuscrito S6-16/09 normaliza los pivotes; el resultado es el mismo.
- **Gauss-Jordan:** Ax anula arriba y abajo en cada columna. El manuscrito S3-24/08 primero baja y luego sube; el resultado es el mismo.
- **κ:** Ax usa la norma ∞ y la escala 10/100 porque lo exige el enunciado; la lámina usa las normas 1 o 2 y 5 niveles.
- **Notación de los manuscritos que conviene reconocer:** ρ(T) aparece como «P(T)»; la tolerancia como «T = 0,01» y el cambio entre iteraciones como T₁, T₂; el determinante como |A|; el sistema normal como «AᵀAx = AᵀB».

---

## C. Extensiones (Cat. C): no se vieron en clase

| Extensión | Qué es | Por qué está | Dónde |
|---|---|---|---|
| **Richardson** | x⁽ᵏ⁺¹⁾ = x⁽ᵏ⁾ + (b − Ax⁽ᵏ⁾); matriz de iteración I − A | Para **demostrar** el precondicionador: con M = D, Jacobi, Gauss-Seidel y SOR no cambian, y Richardson sí. Precondicionado con M = D es exactamente Jacobi | `metodos.paso_richardson`; pestaña «Precondicionamiento» con el aviso «Extensión no vista en clase» |
| **Faddeev-LeVerrier** | Coeficientes de det(λI − T) con productos y trazas: M₀ = 0; Mₖ = T·Mₖ₋₁ + cₖ₋₁I; cₖ = −tr(T·Mₖ)/k. Exacto con fracciones | Sarrus solo sirve para 3×3 y el enunciado pide ρ(T). En 3×3 da **el mismo** polinomio que Sarrus (prueba `test_faddeev_coincide_con_sarrus_3x3`) | `polinomio_raices.polinomio_caracteristico` |
| **Durand-Kerner** | Aproxima a la vez **todas** las raíces, también las complejas: zᵢ ← zᵢ − p(zᵢ)/Π<sub>j≠i</sub>(zᵢ − zⱼ) | Un polinomio de grado ≥ 3 en general no tiene fórmula sencilla, y ρ depende de las raíces complejas | `polinomio_raices.durand_kerner`, `raices` |
| Matriz de iteración de SOR | T<sub>ω</sub> = (D + ωL)⁻¹[(1 − ω)D − ωU] | Para dar ρ(T) también de SOR | `matriz_iteracion.matriz_iteracion` |
| Pivoteo parcial | Elegir el mayor \|aᵢₖ\| como pivote | Opción; la lámina solo menciona PA = LU | Módulo I |

**Limitaciones que conviene decir:** Durand-Kerner no tiene garantía de convergencia global. Ax verifica cada raíz (|p(λ)| y Σλ = tr(T)), avisa cuando hay raíces casi repetidas y declara «indeterminado» si ρ está muy cerca de 1. ρ(T) se calcula hasta n = 8.

**Frase:** «Richardson, Faddeev-LeVerrier y Durand-Kerner no los vimos en clase. Son extensiones y la aplicación las rotula así. Las usamos porque Sarrus solo cubre 3×3 y porque, con M = D, Jacobi no cambia».

---

## D. Arquitectura

```text
app.py → paginas/ → interfaz/modulos/<módulo>.mostrar()
                         │           │            │
                         ▼           ▼            ▼
             interfaz/compartido/  algebra/     visualizacion/
             (editor, LaTeX,       (calcula)    (dibuja con Plotly)
              estilo, gestos)        │
                                     ▼
                            algebra/compartido/ (matriz, validacion, exactos)
```

| Carpeta | Contenido | Archivos clave |
|---|---|---|
| `algebra/` | Núcleo: una carpeta por módulo + `compartido/` | `directos.py`, `condicion.py`, `minimos.py`, `metodos.py`, `ejecucion.py`, `matriz_iteracion.py`, `espectral.py` |
| `interfaz/` | Pantallas; no calcula | `modulos/` (una vista por módulo), `compartido/editor.py`, `formulas.py` (LaTeX), `componentes.py` |
| `visualizacion/` | Gráficas y notación | `interactivas.py`, `notacion.py`, `datos_graficas.py` |
| `gestos/` | Control gestual | ver la parte E |
| `tests/`, `auditoria/` | Pruebas y verificación independiente | una carpeta de pruebas por módulo |

**Reglas:**

- `algebra/` no importa la interfaz ni bibliotecas externas.
- `gestos/` no importa `algebra/`.
- No hay ciclos de importación (Graphify y análisis AST).
- **El Módulo I es la base:** II (inversa), III (Gauss) y IV (solución de referencia) lo reutilizan, como pide el enunciado.

**Funciones más conectadas** (Graphify): `ejecutar`, `formatear_numero`, `ConfiguracionIterativa`, `ErrorEntrada`, `ErrorMatriz`, `radio_espectral`, `a_fraccion`.

**Recorrido común:**

```text
entrada → validación → función principal → auxiliares → Resultado (dataclass) → vista y gráfica
```

Detalle por módulo en `docs/mapa_completo_del_codigo.md`.

**«Muéstreme el código»:** las tablas «Código» de cada módulo en la parte B dicen archivo y función; `visualizacion/notacion.py` y `interfaz/compartido/formulas.py` escriben las fórmulas.

**Verificación:**

- **295 pruebas.**
- **Auditoría aleatoria con 0 fallos:** 4500 sistemas; 400 inversas, determinantes y κ; 200 perturbaciones; 300 mínimos cuadrados; 600 iteraciones; 300 análisis espectrales; 150 precondicionadores.
- **Volcado de los 273 resultados** de los ejemplos: idéntico tras cada cambio.
- **Autoverificación en pantalla:** b − Ax = 0, A·A⁻¹ = I, Aᵀr = 0, Σλ = tr(T).

---

## E. MediaPipe: control gestual de la gráfica 3D

Es un incentivo de experiencia de usuario (Cat. C). Gira y acerca la **gráfica 3D de planos del Módulo I** con la mano. **No calcula nada del álgebra.**

**Bibliotecas:** MediaPipe 1.2.2 (Hand Landmarker, API Tasks) y OpenCV 5.0 (cámara). El modelo `hand_landmarker.task` (Apache-2.0) va dentro del proyecto, así que funciona sin internet.

```text
cámara ─► captura.py ─► deteccion.py ─► interpretacion.py ─► movimiento.py ─► servidor.py ─► puente JS ─► Plotly
(OpenCV)   fotograma      21 puntos       gesto estable        cámara θ, φ, r   127.0.0.1, SSE   relayout
```

**Cómo detecta las manos:** el fotograma en espejo pasa por el Hand Landmarker (modo VIDEO, hasta 2 manos), que devuelve **21 puntos** por mano (0 = muñeca, 4 = punta del pulgar, 8 = punta del índice). Todas las distancias se dividen por el **tamaño de la palma**, así que funciona igual cerca o lejos de la cámara.

| Gesto | Acción |
|---|---|
| ✋ Palma abierta (½ s) | Activa y **calibra** la pinza |
| 🤏 Pinza pulgar-índice | Agarrar y **girar**. Mano a la derecha: gira a la derecha. **Vertical invertido:** mano arriba baja la vista y mano abajo la sube |
| 🤏🤏 Pinza con las dos manos | **Zoom**: separarlas acerca |
| ✊ Puño (½ s) | **Pausa** (se reanuda con la palma) |
| ✌️ Victoria (≈ 1 s) | **Restablece** la vista |

**Estabilidad:**

- antirrebote (0,35 s; victoria 0,8 s);
- histéresis: la pinza sale con un umbral 1,5 veces el de entrada;
- calibración: umbral entre 0,18 y 0,25;
- suavizado s ← s + 0,35(x − s);
- zona muerta acumulada.

**Cámara:** orbital, eye = r(cos φ cos θ, cos φ sin θ, sin φ), con φ ∈ [−80°, 85°] y r ∈ [0,9; 5].

**Conexión con Plotly:** un servidor mínimo (`servidor.py`, solo en 127.0.0.1 y con un token) envía la cámara unas 30 veces por segundo. Un puente de unas 50 líneas (`puente_camara.js`) la aplica con `Plotly.relayout`, sin redibujar. Sin el puente, Streamlit solo lograba 1-3 actualizaciones por segundo (medido). El ratón funciona siempre y `uirevision` conserva la vista.

**Privacidad y apagado:**

- La cámara **solo se enciende con el botón** «Activar cámara y gestos». Mientras está encendida se ve «● Cámara activa».
- El fotograma se procesa en memoria y se descarta: no se graba ni se envía. Al navegador solo llegan 9 números.
- Se apaga con el botón «⏹ Detener», al cambiar de módulo o cerrar la pestaña (perro guardián: 4 s sin latido) o ante cualquier error, con un mensaje.
- El hilo de visión nunca llama a Streamlit.

**Medido** (10-nov, Brave): ~32 fotogramas por segundo; detección en 18-28 ms; ~1 núcleo de CPU; +54 MB de memoria, liberados al detener.

---

## F. Rúbrica e incentivos (OFICIAL pp. 4-5)

### F.1 Requisitos obligatorios y dónde se ven

| Criterio (peso) | Qué se evalúa | Dónde demostrarlo en Ax |
|---|---|---|
| Módulo I (8 %) | Implementación, clasificación, validaciones, procedimiento completo | I: ejemplo S6-16/09, pasos «−2F₁ + F₂», Sol = {…}; ejemplos «infinitas» e «inconsistente» |
| Módulo II (8 %) | κ∞, perturbación, errores relativos, interpretación | II: ejemplo S7-21/09 p. 19, los 5 pasos, tabla de la perturbación, cota |
| Módulo III (8 %) | Ecuaciones normales, residual, error, ajuste y **gráfica** | III: S8-30/09 (Cramer igual), pestaña «Ajuste» con gráfica |
| Módulo IV (8 %) | Métodos; convergencia, error y comparación | IV: despejes, tabla, motivo, **gráfica de error**, «Comparar», «Convergencia» |
| Procedimiento (7 %) | Desarrollo claro y completo | Paso a paso en I, II, III y IV, con la notación de la profesora |
| Análisis (6 %) | Estabilidad, sensibilidad, residual, error, convergencia | Mensajes de interpretación en cada módulo |
| Código (5 %) | Modular, legible, comentado | Parte D; `mapa_completo_del_codigo.md` |
| Validaciones (4 %) | Vacíos y no numéricos, dimensiones, singularidad, división entre 0 y pivotes nulos, ε > 0, máximo de iteraciones entero > 0, 0 < ω < 2, sin cierres (OFICIAL p. 3) | Editor con validación previa; errores con la celda exacta; diagonal nula; matriz singular en II |
| Interfaz (5 %) | Intuitiva y fácil de interpretar | Navegación superior, ejemplos precargados, ayudas |
| Manual (3 %) y casos de prueba (3 %) | Manual reproducible; caso obligatorio | `docs/manual_usuario.md`, `casos_prueba/` |

**Gráficas:** el enunciado exige solo la de III (datos y recta) y la de IV (error frente a iteración). Las de I (rectas y planos), los autovalores y el precondicionador son opcionales (`docs/cumplimiento_graficas.md`).

### F.2 Los cinco incentivos (el puntaje lo decide la docente)

| Incentivo (máx.) | Qué tiene Ax | Cómo demostrarlo |
|---|---|---|
| Visualización avanzada (1 %) | Comparación superpuesta (e, d o r), historial explorable (clic en un punto, deslizador), **CSV** con precisión completa, autovalores, planos 3D | IV → «Comparar»; «Ejecutar» → botón CSV |
| Precondicionamiento (1,5 %) | M = D, B = D⁻¹A; κ(A) frente a κ(B); T y c **idénticas** en Jacobi, Gauss-Seidel y SOR (demostrado exactamente); Richardson: ρ 4,618 → 0,405 | IV → «Precondicionamiento» con la tridiagonal |
| Matrices dispersas (1 %) | CSR propio (`valores`, `columnas`, `inicio`); memoria 2·nnz + n + 1; costo O(nnz) por iteración; mismas iteraciones que el formato denso | IV → casilla «CSR» con el ejemplo tridiagonal |
| Experiencia de usuario (0,5 %) | Editor de rejilla con validación previa; sugerencia de reordenamiento; distintivos Cat.; **control gestual** | I → panel de gestos; IV → «Convergencia» con un sistema no dominante |
| Extensión matemática (1 %) | ρ(T) para n ≤ 8 con autovalores complejos; decisiones exactas (λ = ±1); T de SOR | IV → «Convergencia» con el ejemplo de S9-07/10 |

---

## G. Defensa

### G.1 Preguntas y respuestas

| # | Pregunta | Respuesta técnica |
|---|---|---|
| 1 | ¿Cómo clasifica un sistema? | Cuenta las ecuaciones no nulas de la forma escalonada (el rango) y las compara con n; «0 = c» significa sin solución. Código: `_escalonar` y `_rango_aumentada` |
| 2 | ¿Y si un pivote es 0? | Busca debajo una fila no nula e intercambia (F₁ ↔ F₂), con el motivo registrado. Si no hay ninguna, la variable es libre |
| 3 | ¿Gauss o Gauss-Jordan? | Gauss: forma escalonada y sustitución hacia atrás. Gauss-Jordan: forma reducida, donde la solución se lee directamente |
| 4 | ¿Por qué norma ∞ y no 1 como en la lámina? | La exige el enunciado (OFICIAL p. 2); los 5 pasos son los de S7-21/09 p. 19 |
| 5 | ¿Qué significa κ = 16/5? | Un error relativo en b se amplifica como mucho 3,2 veces en x; es < 10, sensibilidad baja |
| 6 | ¿Por qué las ecuaciones normales dan la mejor aproximación? | En el mínimo de ‖Ax − b‖₂ el residuo es ortogonal a Col(A): Aᵀr = 0 ⇒ AᵀAx̂ = Aᵀb. Ax lo verifica |
| 7 | La profesora usó Cramer, ¿por qué Gauss? | El enunciado pide «un método directo ya implementado». Cramer se muestra como verificación y da lo mismo |
| 8 | ¿Por qué Gauss-Seidel es más rápido? | Usa cada componente nueva en cuanto la calcula (tridiagonal: 5 iteraciones frente a 7) |
| 9 | ¿Qué garantiza la convergencia? | ρ(T) < 1 es necesaria y suficiente; la dominancia diagonal es solo suficiente |
| 10 | ¿Cómo calculan ρ(T)? | Los pasos ①-⑤ de S9-07/10; en 3×3 se muestra Sarrus. Para cualquier n: Faddeev-LeVerrier y Durand-Kerner (Cat. C) |
| 11 | ¿Por qué Ax da 1,174 si la hoja dice ρ = 0? | La hoja omitió det(T) = 4/3. El polinomio correcto, −λ³ − (4/9)λ + 4/3, tiene raíces complejas de módulo 1,174 |
| 12 | ¿Qué hace ω en SOR? | Mezcla (1 − ω)x⁽ᵏ⁾ + ω·x<sup>GS</sup>. ω = 1 es Gauss-Seidel; Ax exige 0 < ω < 2, que por sí solo no garantiza la convergencia |
| 13 | ¿Fracciones o float? | Exactas en I-III (la clasificación no depende de redondeos); float en IV (aproximación por tolerancia) |
| 14 | ¿Usaron bibliotecas de álgebra? | No. El núcleo solo usa la biblioteca estándar; Streamlit, Plotly y MediaPipe solo para la interfaz, las gráficas y la cámara |
| 15 | ¿Cómo saben que es correcto? | 295 pruebas con valores calculados aparte; auditoría con oráculos independientes (Leibniz, adjunta, Cramer, Gelfand), 0 fallos; autoverificaciones |
| 16 | ¿Y una entrada inválida? | Mensaje con la celda exacta y botón bloqueado si las dimensiones no cuadran. El Módulo IV devuelve códigos en vez de excepciones; la aplicación nunca se cierra |
| 17 | ¿Por qué el máximo y no la suma (S8-30/09 p. 20)? | La norma ∞ es el máximo; la suma es la norma 1 |
| 18 | ¿Cómo está organizado el código? | `algebra/` (calcula), `interfaz/` (muestra), `visualizacion/` (dibuja), `gestos/`. El núcleo no depende de la interfaz |
| 19 | ¿Dónde está Jacobi? | `metodos.py` → `paso_jacobi`; el bucle y los criterios en `ejecucion.py` → `ejecutar` |
| 20 | ¿Por qué el Módulo II usa el Gauss-Jordan del I? | El enunciado pide la inversa «con un algoritmo implementado por el grupo»; no se duplicó código |
| 21 | ¿Las gráficas calculan algo? | No. Dibujan los datos del núcleo y una prueba lo compara |
| 22 | ¿Qué gráficas son obligatorias? | Solo la de III (datos y recta) y la de IV (error frente a iteración). I y II no exigen gráfica |
| 23 | ¿Cómo se explora la gráfica de convergencia? | ⛶ pantalla completa; clic en un punto o deslizador para ver k, x⁽ᵏ⁾, dₖ y rₖ; recuadro para varias iteraciones; «Destacar método». El estado final sale del motivo real: nunca marca una convergencia que no ocurrió |
| 24 | ¿Se graba la imagen? | No: se procesa en memoria y se descarta; solo 9 números van a la gráfica, por 127.0.0.1 |
| 25 | ¿Puño o pinza? | En la pinza la punta del índice está fuera de la palma; todo se mide en unidades de palma |
| 26 | ¿Por qué no tiembla? | Suavizado, zona muerta acumulada, antirrebote e histéresis |
| 27 | ¿Y si cambio de módulo con la cámara encendida? | A los 4 s sin latido se apaga y libera la cámara |
| 28 | ¿Por qué hay JavaScript? | Sin el puente, la gráfica se actualiza 1-3 veces por segundo. Las 50 líneas solo aplican la cámara; la visión es Python |
| 29 | ¿Por qué M = D no acelera Jacobi? | D⁻¹A tiene diagonal 1, así que T̃<sub>J</sub> = T<sub>J</sub>: iteraciones idénticas. El efecto real se ve en κ y en Richardson |
| 30 | ¿Richardson se vio en clase? | No, profesora. Es una extensión rotulada así; con M = D se convierte en Jacobi |
| 31 | ¿Qué es CSR? | Guarda solo los no nulos (valores, columna, inicio de fila; S9-05/10 p. 9); cada iteración cuesta O(nnz) en vez de O(n²) |
| 32 | ¿Faddeev-LeVerrier en una frase? | Los coeficientes de det(λI − T) con productos y trazas, cₖ = −tr(T·Mₖ)/k; en 3×3 coincide con Sarrus |
| 33 | ¿Durand-Kerner en una frase? | Corrige todas las raíces a la vez, como Newton pero separándolas: zᵢ ← zᵢ − p(zᵢ)/Π(zᵢ − zⱼ) |

### G.2 Errores que debemos evitar

- **Decir que Richardson, Faddeev-LeVerrier o Durand-Kerner se vieron en clase.** Son extensiones (Cat. C).
- Decir que la dominancia diagonal es **necesaria**: es solo suficiente.
- Decir que «completar N iteraciones» (criterio C) demuestra la convergencia.
- Confundir dₖ (cambio entre iteraciones), rₖ (residuo) y eₖ (error respecto a x*): ninguno de los dos primeros es el error real.
- Decir que 0 < ω < 2 garantiza la convergencia de SOR.
- Usar como correcto un resultado de una lámina con errata (B.5).
- Decir que «el programa usó una biblioteca para…»: solo la interfaz y las gráficas usan bibliotecas.
- Decir que todos los módulos exigen gráfica: solo III y IV.
- Si la cámara falla en la defensa: usar el ratón, que funciona igual.

### G.3 Profundización por integrante (todos estudian todo)

| Integrante | Profundizar en | Código para leer |
|---|---|---|
| Elmer | Módulo I y notación de clase (B.1, B.6) | `directos.py`, `componentes.mostrar_pasos` |
| Samir | Módulos II y III (B.2, B.3) | `condicion.py`, `minimos.py`, `modulo_II_condicionamiento.py` |
| Daniel | Módulo IV y convergencia (B.4, C) | `metodos.py`, `ejecucion.py`, `matriz_iteracion.py`, `espectral.py` |
| Derek | Incentivos, arquitectura y MediaPipe (D, E, F.2) | `precondicionamiento.py`, `dispersas.py`, `gestos/` |

**Todos:** las fórmulas de la parte B, las extensiones (C) y las preguntas 1, 9, 13, 14, 22, 29 y 30.

### G.4 Hoja de repaso

- **Clasificación:** rango(A) frente a rango([A | b]) frente a n. Se escribe Sol = {(…)}.
- **Condicionamiento:** κ∞ = ‖A‖∞‖A⁻¹‖∞ (5 pasos); escala < 10 / < 100 / ≥ 100; ‖Δx‖/‖x‖ ≤ κ‖Δb‖/‖b‖.
- **Mínimos cuadrados:** AᵀAx̂ = Aᵀb; r = b − Ax̂; Aᵀr = 0; ‖r‖₂; Cramer x̂ᵢ = Dᵢ/D.
- **Iterativos:** despejes; T<sub>J</sub> = −D⁻¹(L + U), T<sub>GS</sub> = −(D + L)⁻¹U; ρ(T) < 1 ⇔ converge; criterio A ‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞ < ε; k<sub>max</sub>.
- **Gestos:** palma activa, pinza gira, dos pinzas zoom, puño pausa, victoria restablece.

**Antes de la defensa:** instalar con `ejecutar.bat`; correr las pruebas (295 OK); practicar cada módulo con los ejemplos precargados; probar los gestos con la luz del aula.
