# Gráficas de exploración: propuesta e implementación

**Fecha:** 10-nov-2026.
**Rama:** `feature/graficas-exploracion`.

**Objetivo:** que las gráficas 2D de Ax permitan **explorar** los resultados:

- ampliarlas;
- seleccionar puntos y zonas;
- ver los valores de una iteración;
- distinguir los hitos reales.

**Regla:** todo lo que se marca sale de los datos que calculó el núcleo: el historial, el código de terminación y los autovalores. No se recalcula nada y no se declara convergencia si el método no la alcanzó.

**Fuera de alcance:** la gráfica 3D de planos y su control gestual quedan **exactamente** como estaban. No se tocaron `planos_3d` ni `gestos/`.

## 1. Diagnóstico (antes)

Capturas en Brave a 1440×900:

- Todas las gráficas 2D medían 440 px de alto.
- Tenían zoom, desplazamiento, autoescala, restablecer y leyenda interactiva.
- **No había forma de fijar o seleccionar un punto.** El valor de x⁽ᵏ⁾ solo estaba en la tabla, no en la gráfica.
- No se distinguía en qué iteración se cumplió el criterio, ni si el método se detuvo por k_max.
- Streamlit 1.66 ya ofrece **pantalla completa nativa** (ícono ⛶ arriba a la derecha de cada gráfica): la gráfica pasa a 1416×842 y conserva la barra y la leyenda. Funcionaba, pero **nadie la mencionaba**.
- Había una línea vertical en k = 0 (la línea del cero del eje x) que no aporta nada en un eje de iteraciones.

## 2. Propuesta por gráfica

| Gráfica | Finalidad matemática | Mejoras propuestas | Beneficio | Descartado (y por qué) |
|---|---|---|---|---|
| **Convergencia** (IV · Ejecutar). **Prioridad** | Ver cómo bajan d_k y r_k hasta ε | Hitos reales: primera iteración, última, «ε alcanzado en k» solo si el código es `TOLERANCIA_*`; aviso de k_max o de valores no finitos; tramos donde d_k crece (sombreados, rotulados «d_k aumenta», **no** «diverge»); x⁽ᵏ⁾ al pasar el cursor; **clic en un punto o deslizador de iteración**, que marca la iteración en la gráfica y muestra un panel con k, x⁽ᵏ⁾, d_k, r_k y el método; **selección de zona**, que muestra la tabla de esas iteraciones; ε solo con los criterios A o B | Explicar la convergencia iteración por iteración durante la defensa | Animación de la curva: distrae y no aporta dato |
| **Comparación** (IV · Comparar) | Comparar Jacobi, GS y SOR en las mismas condiciones | «Destacar método» (atenúa los demás); el deslizador de iteración marca k y muestra una tabla con el valor de cada método en esa k («ya terminó» si el método paró antes); la última iteración de cada método se resalta y rotula; ε solo si la métrica coincide con el criterio real (d con A, r con B) | Comparar en la misma región sin leer tres tablas | Ejes separados por método: se perdería la comparación |
| **Autovalores** (IV · Convergencia) | ρ(T) frente al círculo unidad | Resaltar los autovalores dominantes (\|λ\| = ρ) | Se ve qué autovalor decide la convergencia | Etiquetar todos los λ: satura con n grande (el cursor ya los muestra) |
| **Precondicionador** (IV) | Original frente a M = D | Sin línea del cero; el resto se conserva (leyenda por método, vista acotada con autoescala) | — | Más controles: ya tiene leyenda agrupada y el aviso de la vista acotada |
| **Ajuste lineal** (III) | Recta y residuos | Resaltar el dato con mayor \|rᵢ\| | Muestra dónde el ajuste falla más | Banda de confianza: no es materia del curso |
| **Rectas 2D** (I) | Intersección de rectas | Sin cambios | Ya muestra la solución y las ecuaciones | — |
| **Planos 3D** (I) | Intersección de planos + gestos | **Sin cambios** (requisito) | — | — |
| **Todas las 2D** | — | Pantalla completa visible y explicada; la vista (zoom) se conserva entre interacciones (`uirevision`); herramienta «Seleccionar zona» en las gráficas que la usan | Ampliar, acercar, seleccionar y restablecer sin perder el estado | Más altura fija: la pantalla completa ya da todo el espacio |

## 3. Cómo se implementó (sin bibliotecas nuevas ni JavaScript)

- **Plotly** (ya instalado):
  - los hitos son estilos sobre las mismas trazas (tamaño, borde y símbolo de cada marcador) más anotaciones;
  - **no se agregan trazas con datos nuevos**, así que las pruebas que comparan los datos dibujados con el núcleo siguen pasando sin cambios.
- **Streamlit:**
  - `st.plotly_chart(on_select="rerun", selection_mode=("points", "box"))` devuelve los puntos elegidos con un clic o un recuadro;
  - el panel de detalle y el deslizador son widgets de Python;
  - la pantalla completa es la del propio Streamlit.

## 4. Verificación (10-nov)

| Comprobación | Resultado |
|---|---|
| Suite completa | **281 pruebas OK**: 269 anteriores + 12 nuevas en `tests/interfaz/test_graficas_exploracion.py` |
| Datos de las gráficas | Las 8 pruebas de `test_graficas_interactivas.py` pasan **sin cambios**: mismas trazas, mismos x e y que el historial y que Matplotlib |
| Honestidad de los hitos | Con k_max (`MAXIMO_ITERACIONES`) no aparece «ε alcanzado» ni «cumplido». El sombreado coincide exactamente con los k en que d_k creció. Con el criterio C no hay línea ε |
| Gráfica 3D | `planos_3d` produce **el mismo JSON byte a byte** que en `main`. Su contenedor queda fuera de la regla CSS nueva. `gestos/` no se tocó |
| Núcleo | Auditoría con 0 fallos; volcado de 273 resultados idéntico |
| Brave, 1440 / 1366 / 1024 px | Un clic real en el punto k = 3 mueve el deslizador y actualiza el panel (d₃ = 0,094; r₃ = 0,238413, igual que la tabla). «Destacar» atenúa los demás métodos. La pantalla completa da 1416×842 px con barra y leyenda |
| Detalle corregido | Con la selección activa aparecía una barra de desplazamiento interna (contenido de 477 px en 470): se corrigió con CSS solo para las gráficas 2D |

**Capturas** (`docs/capturas/`):

- `graficas_antes_convergencia.png`: antes;
- `graficas_1440_convergencia_clic.png`: iteración elegida con un clic;
- `graficas_1440_pantalla_completa.png`;
- `graficas_1366_comparacion.png`: Gauss-Seidel destacado y la tabla por iteración;
- `graficas_no_converge_figura.png`: S9-07/10, Jacobi, k_max sin cumplir y tramos crecientes;
- `graficas_1440_autovalores.png`: λ dominante;
- `graficas_1366_ajuste.png`: mayor |rᵢ|;
- `graficas_1024_convergencia_clic.png`.
