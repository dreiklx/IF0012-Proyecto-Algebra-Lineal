# Diseño visual e integración de la rúbrica en la interfaz

**Fecha:** 03-nov-2026. **Rama:** `feature/rediseño-visual`.

**Alcance:** solo la presentación. **No se modificó ningún archivo de `algebra/`** (núcleo matemático), de `tests/` ni de `auditoria/`.

- Los 25 resultados de los ejemplos precargados son idénticos byte a byte antes y después del rediseño (comparación automática de las salidas).
- Las 204 pruebas pasan y la auditoría independiente sigue en 0 fallos.

Las capturas de cada pantalla están en [`docs/capturas/`](capturas/).

## 1. Diagnóstico del diseño anterior

Revisado sobre capturas reales de la aplicación (`docs/capturas/antes_modulo_I.png`):

| Problema | Dónde | Efecto |
|---|---|---|
| Aspecto de la plantilla predeterminada de Streamlit (blanco y gris, sin identidad) | Toda la aplicación | Parecía un prototipo, no un software científico |
| Navegación como lista de botones de radio diminutos, sin indicar el módulo activo | Barra lateral | El módulo actual pasaba inadvertido |
| La portada era una tabla de texto; los incentivos no aparecían | Inicio | No se veía qué hace cada módulo ni dónde demostrar los incentivos |
| El resultado principal quedaba entre otras métricas del mismo tamaño | Los cuatro módulos | La solución y κ no destacaban |
| Formularios sin etapas (datos, método, resultado) | Los cuatro módulos | Costaba seguir el flujo |
| Gráficas con colores por defecto, leyendas sobre los datos y colores distintos para el mismo método en distintas gráficas | Módulos III y IV | Superposiciones y lectura difícil |
| El diagrama de autovalores y la figura 3D ocupaban todo el ancho | Módulos I y IV | Imágenes desproporcionadas |
| Incentivos sin ninguna señal en la interfaz | Módulo IV | No se distinguían durante la demostración |

## 2. Nueva identidad visual

- **Paleta** (`.streamlit/config.toml`, `interfaz/compartido/estilo.py`, `visualizacion/tema.py`):

  | Uso | Color |
  |---|---|
  | Fondo grafito azulado | `#0B1020` |
  | Paneles | `#141C30` |
  | Acento principal (azul eléctrico) | `#4F8CFF` |
  | Acento secundario (cian) | `#22D3EE` |
  | Incentivos (violeta) | `#A78BFA` |
  | Estado correcto | `#34D399` |
  | Advertencia | `#FBBF24` |
  | Error | `#F87171` |

- **Tipografía:** Segoe UI para el texto y Cascadia Code o Consolas para las matrices escritas; KaTeX para las fórmulas.
- **Componentes** (`interfaz/compartido/estilo.py`, solo presentación):
  - **Portada:** tarjetas de módulo y de incentivo, cada una con un botón que abre la funcionalidad real.
  - **Cabecera de módulo:** número, título, descripción y etiquetas.
  - **Rótulos de etapa numerados:** 1 Datos, 2 Método o parámetros, 3 Resultado.
  - **Tarjeta de resultado principal** (`tarjeta_resultado`): borde de acento, valor grande y etiquetas de estado.
  - **Etiquetas de estado:** solución única, inconsistente, converge, decisión exacta, Aᵀr = 0 verificado…
  - **Barra de la escala de κ** del proyecto (10 y 100). Solo visual: la clasificación la decide `clasificar_kappa`.
  - **Marcas de incentivo** junto a la funcionalidad que lo implementa.
  - **Métricas:** valores largos en varias líneas, nunca truncados con «…» (verificado a 1024 px).
- **Gráficas:**
  - fondo integrado;
  - un color y un marcador fijos por método (Jacobi azul, Gauss-Seidel rosa, SOR cian, Richardson ámbar);
  - leyendas **debajo** de los ejes, sin tapar datos;
  - círculo unidad sombreado en el diagrama de autovalores;
  - figuras acotadas a una columna, con su explicación al lado.

  **Los datos dibujados no cambian.**
- **Recomendaciones contextuales nuevas:**
  - sistema inconsistente → usar el Módulo III;
  - matriz singular → revisar dependencias;
  - AᵀA singular → eliminar columnas dependientes;
  - diagonal cero, máximo de iteraciones o desbordamiento → mirar «Convergencia» o reordenar.

  Son textos fijos según el código de resultado que ya devuelve el núcleo.

## 3. Rúbrica normal (65 %): lógica y presentación

| Criterio | Puntaje | Implementación lógica | Presentación visual | Evidencia | Estado |
|---|---:|---|---|---|---|
| Módulo I: sistemas lineales | 8 % | `directos._escalonar`, `_resolver`, `inversa_gauss_jordan` | Tarjeta con la clasificación, la solución en LaTeX y el rango y det; pasos desplegados; figura 2D o 3D | `test_directos`, `test_app`; 4500 casos de auditoría; `capturas/1_modulo_I.png`, `1b_geometria.png` | COMPLETADO |
| Módulo II: condicionamiento | 8 % | `numero_condicion_infinito`, `construir_delta_b`, `analizar_perturbacion` | κ grande con la barra de la escala; ‖A‖ y ‖A⁻¹‖; tarjeta de perturbación con la cota y la amplificación | `test_condicion`, `test_app`; `capturas/2_modulo_II.png` | COMPLETADO |
| Módulo III: mínimos cuadrados | 8 % | `minimos_cuadrados`, `ajuste_lineal`, `cramer` | Ecuación de la recta destacada junto a la gráfica; x̂ y ‖r‖₂ en una tarjeta; etiquetas b ∉ Col(A) y Aᵀr = 0; verificación de clase | `test_minimos`, `test_app`; `capturas/3_modulo_III_ajuste.png` | COMPLETADO |
| Módulo IV: métodos iterativos | 8 % | `paso_*`, `_ejecutar`, `comparar_metodos`, `radio_espectral` | Aproximación final destacada; tabla con la columna de parada rotulada; comparación con error final; tarjeta de ρ con su estado | P1–P21, `test_espectral`, `test_app`; `capturas/4*` | COMPLETADO |
| Procedimiento matemático | 7 % | `Paso`, `mostrar_pasos`, D/L/U/T, `desarrollo_sarrus`, `cramer` | Pasos numerados con las matrices en LaTeX; desplegables con el procedimiento | `test_app` (pasos, Cramer, Sarrus) | COMPLETADO |
| Análisis e interpretación | 6 % | `_interpretar`, mensajes del núcleo | Mensajes por color; recomendaciones nuevas; «cómo leer el diagrama» | `test_app` | COMPLETADO (juicio de la docente) |
| Diseño del código | 5 % | Capas `algebra/`, `interfaz/`, `visualizacion/` | Estilo centralizado en `interfaz/compartido/estilo.py` y `visualizacion/tema.py`; los módulos no repiten CSS | `docs/arquitectura.md` | COMPLETADO |
| Validaciones y errores | 4 % | `validacion.py`, `validar_configuracion`, `ejecutar` sin excepciones | Errores en rojo con la celda exacta; recomendaciones | `test_validacion`, `test_modulo_I_entrada_invalida` | COMPLETADO |
| Interfaz y usabilidad | 5 % | — | Identidad visual propia; navegación con el módulo activo resaltado; etapas numeradas; portada con accesos directos; probado a 1440 y 1024 px | `capturas/0_inicio.png`, `9_modulo_IV_1024px.png` | COMPLETADO (juicio de la docente) |
| Manual de usuario | 3 % | `docs/manual_usuario.md` | Actualizado con la portada y los accesos | Probado en otra computadora (equipo, 03-nov) | COMPLETADO |
| Casos de prueba | 3 % | `casos_prueba/`, `tests/` | — | 204 pruebas | Casos propios: COMPLETADO. **Caso obligatorio: PENDIENTE (externo)** |

## 4. Incentivos (hasta 5 %): funcionalidad real y dónde se ve

| Incentivo | Máx. | Requisito (OFICIAL p. 5) | Funcionalidad y código | Dónde en la interfaz y cómo se usa | Evidencia | Estado |
|---|---:|---|---|---|---|---|
| Visualización avanzada | 1 % | «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» | `interactivas.comparacion`, `interactivas.autovalores`, `interactivas.convergencia`, `interactivas.precondicionador`, barrido de ω, `csv_historial` | IV → «Comparar métodos» (gráfica e/d/r); «Ejecutar» → «Descargar tabla (CSV)»; «Convergencia» → autovalores | `test_csv_exportado_contiene_historial_completo`; `capturas/4b`, `4c` | COMPLETADO |
| Precondicionamiento | 1,5 % | «Implementación correcta de un precondicionador diagonal y comparación documentada de su efecto» | `algebra/modulo_IV_iterativos/precondicionamiento.py` (`precondicionar_diagonal`, `analizar_precondicionador`), `paso_richardson` | IV → pestaña «Precondicionamiento diagonal» → «Analizar el precondicionador M = D»; tarjeta con κ, T idénticas y efecto en Richardson | `test_precondicionamiento`, auditoría de 150 casos; `capturas/4d` | COMPLETADO |
| Matrices dispersas | 1 % | «Representación o tratamiento eficiente de matrices dispersas, con explicación de la estrategia» | `algebra/modulo_IV_iterativos/dispersas.py` (`a_csr`, `paso_*_csr`) | IV → «Ejecutar un método» → casilla «Usar almacenamiento disperso (CSR)»; informa nnz, densidad y memoria | `test_dispersas`, `test_modulo_IV_formato_csr` | COMPLETADO |
| Experiencia de usuario | 0,5 % | «Mejoras sustantivas de accesibilidad, ayuda contextual o interacción, no solo decoración» | Ejemplos precargados, ayudas en los campos, errores con la posición, recomendaciones, `reordenamiento_dominante`, interpretación geométrica, accesos desde la portada | Todos los módulos; I → «Interpretación geométrica»; IV → «Convergencia» (reordenamiento) | `test_app`, `test_modulo_IV_reordenamiento_y_sarrus` | COMPLETADO |
| Extensión matemática | 1 % | «Funcionalidad adicional pertinente, correctamente implementada y defendida» | `polinomio_raices.py`: Faddeev-LeVerrier, Durand-Kerner, Schur-Cohn, p(±1) = 0; T de SOR; Richardson | IV → «Convergencia: dominancia y radio espectral» | `test_espectral`; 300 casos de auditoría | COMPLETADO |

Las marcas violetas «Incentivo · …» aparecen **junto a la funcionalidad real** que lo implementa: son señales para la demostración y no sustituyen ninguna funcionalidad. Ningún incentivo se simula con elementos visuales: los cinco existían y estaban probados antes del rediseño.

## 4b. Editor interactivo de datos (03-nov-2026, rama `feature/editor-interactivo`)

**Componente:** `interfaz/compartido/editor.py`, función `editor(...)`, con tres tipos (MATRIZ, VECTOR y PUNTOS), reutilizado en los cuatro módulos.

- **Fuente de verdad:** el texto de siempre, con las mismas claves. Por eso las funciones del núcleo reciben exactamente el mismo formato y los mismos valores. La rejilla de celdas está sincronizada con ese texto en los dos sentidos.
- **Formas de entrada:**
  - pestaña «Editor»: celdas, «＋/－ Fila/Columna», selectores de dimensión y, en «⋯ Más», Identidad, Ceros, Limpiar y Restaurar;
  - pestaña «Pegar»: separadores espacio, tabulación, «;» y «, », con la vista previa de lo interpretado;
  - botón «⟲ Cargar ejemplo» junto al selector de ejemplos del curso.
- **Por módulo:**
  - I: A rectangular y b;
  - II: A (debe ser cuadrada) y b;
  - III: A rectangular y b, más la **tabla editable de puntos (x, y)**;
  - IV: A (cuadrada), b y un **editor de x⁽⁰⁾** cuando es personalizado. Se conservan todos los parámetros.
- **Validación previa** (solo interfaz):
  - etiqueta de estado por editor: lista, faltan valores en (i, j), o formato inválido con la posición que da `leer_matriz`/`leer_vector`;
  - bloqueo del botón de cálculo con un mensaje cuando las dimensiones son incompatibles (`problema_dimensiones`): b con otra longitud, A no cuadrada donde el método lo exige o x⁽⁰⁾ con otra dimensión.
  - Las matrices rectangulares se aceptan donde el procedimiento lo permite (Módulos I y III). Las validaciones existentes del núcleo no se reemplazan.
- **Pruebas:** `tests/interfaz/test_editor.py`, 13 pruebas con funciones puras e interacción real con AppTest: edición de celdas, botones, identidad, restaurar, pegado con comas, bloqueo por dimensiones, x⁽⁰⁾ y tabla de puntos (con la recta esperada calculada a mano).
- **Capturas:** `capturas/editor_*.png`.

## 5. Verificación visual

Capturas reales de la aplicación en ejecución (Edge sin interfaz controlado por CDP, a 1440×900 y 1024×768).

| Pantalla | Captura |
|---|---|
| Inicio | `capturas/0_inicio.png` |
| I · resultado y pasos | `capturas/1_modulo_I.png` |
| I · figura 3D | `capturas/1b_geometria.png` |
| II | `capturas/2_modulo_II.png` |
| III · ajuste | `capturas/3_modulo_III_ajuste.png` |
| IV · las cuatro pestañas | `capturas/4_modulo_IV_ejecutar.png` … `4d_modulo_IV_precondicionamiento.png` |
| IV a 1024 px | `capturas/9_modulo_IV_1024px.png` |

**Defectos encontrados y corregidos durante la revisión:**

- Los rótulos en mayúsculas convertían ‖r‖₂ en «‖R‖₂» y κ en «K», lo que alteraba la notación.
- A 1024 px las métricas se truncaban («0.00037…»).
- El diagrama de autovalores y la figura 3D quedaban desproporcionados.
- La navegación lateral tenía anchos desiguales.

**No capturado:** el mensaje de error por una entrada no numérica. La escritura simulada no llega al área de texto en el modo sin interfaz. Su aparición, con la posición de la celda, la comprueba la prueba automática `test_modulo_I_entrada_invalida`.

**Nota de desarrollo:** el servidor de Streamlit no recarga `interfaz/compartido/estilo.py` al modificarlo; tras cambiar el estilo hay que reiniciar la aplicación.

## 7. Gráficas interactivas y matrices vigentes (03-nov-2026, rama `feature/graficas-interactivas`)

**Tecnología:** Plotly 6.3.0 (`visualizacion/interactivas.py`); es la única dependencia nueva, porque Altair, que ya traía Streamlit, no hace 3D. Las figuras se muestran con `interfaz/compartido/componentes.py::mostrar_interactiva`:

- barra de herramientas vertical, siempre visible, con los colores de Ax;
- zoom con la rueda;
- doble clic para restablecer;
- exportación a PNG.

**Las interacciones solo cambian la vista.** Los datos se toman de los mismos resultados del núcleo, y `tests/interfaz/test_graficas_interactivas.py` (8 pruebas) comprueba que coinciden exactamente con los historiales, los autovalores y la solución, y con las líneas de las figuras de Matplotlib.

| Gráfica | Controles |
|---|---|
| Planos 3D (Módulo I) | Rotar arrastrando (órbita o giro), rueda para el zoom, desplazar, **restablecer vista** y vista guardada; valor de x, y, z y la ecuación al pasar sobre un plano; coordenadas de la solución; ocultar planos desde la leyenda. Escala cúbica y los mismos rangos de ejes que la figura estática |
| Rectas 2D, ajuste, convergencia, comparación, autovalores, precondicionador | Zoom ＋/－, **zoom por región** (arrastrar), desplazar, **autoescala** y **restablecer**; valor de cada punto al pasar el cursor (en la comparación, los tres métodos a la vez); activar y desactivar series en la leyenda; un color y un marcador fijos por método en todas las gráficas |

**Revisado con eventos de ratón reales** (Chromium sin interfaz, el mismo motor que Brave; capturas en `capturas/graf_*.png`):

- la 3D rota al arrastrar;
- el cursor sobre la solución muestra (0.333333, 4, 1.66667);
- en la comparación, el cursor en k = 3 muestra los tres e_k;
- arrastrar sobre una región la amplía;
- a 1024 px la barra vertical no tapa los títulos (se corrigió una superposición).

### 7.1 Rúbrica normal (65 %): versión vigente

| Criterio | Puntaje | Implementación | Presentación | Evidencia | Estado |
|---|---:|---|---|---|---|
| Módulo I: sistemas lineales | 8 % | `directos._escalonar`, `_resolver`, `inversa_gauss_jordan` | Editor de A y b; tarjeta con la clasificación, la solución, el rango y det; pasos; **3D y 2D interactivas** | `test_directos`, `test_app`, `test_editor`, `test_graficas_interactivas`; auditoría (4500 casos) | COMPLETADO |
| Módulo II: condicionamiento | 8 % | `numero_condicion_infinito`, `construir_delta_b`, `analizar_perturbacion` | Editor (A cuadrada); κ con la barra de la escala; tarjeta de perturbación | `test_condicion`, `test_app`; auditoría (400 + 200 casos) | COMPLETADO |
| Módulo III: mínimos cuadrados | 8 % | `minimos_cuadrados`, `ajuste_lineal`, `cramer` | Editor de A rectangular; **tabla editable de puntos**; ecuación destacada; **gráfica interactiva** con el residuo de cada dato al pasar el cursor | `test_minimos`, `test_editor`, `test_graficas_interactivas`; auditoría (300 casos) | COMPLETADO |
| Módulo IV: métodos iterativos | 8 % | `paso_*`, `_ejecutar`, `comparar_metodos`, `radio_espectral` | Editor de A, b y x⁽⁰⁾; tabla de iteraciones; **convergencia y comparación interactivas** (error frente a iteración, con zoom y valores) | P1–P21, `test_espectral`, `test_app`, `test_graficas_interactivas`; auditoría (600 + 300 casos) | COMPLETADO |
| Procedimiento matemático | 7 % | `Paso`, D/L/U/T, `desarrollo_sarrus`, `cramer` | Pasos numerados en LaTeX | `test_app` | COMPLETADO |
| Análisis e interpretación | 6 % | `_interpretar`, mensajes del núcleo | Mensajes por color, recomendaciones, «cómo leer el diagrama» | `test_app` | COMPLETADO (juicio de la docente) |
| Diseño del código | 5 % | Capas `algebra/`, `interfaz/` y `visualizacion/`; el editor y las gráficas, en módulos propios | — | `docs/arquitectura.md` | COMPLETADO |
| Validaciones y errores | 4 % | `validacion.py`, `validar_configuracion` | Validación previa en el editor y bloqueo por dimensiones incompatibles | `test_validacion`, `test_editor` | COMPLETADO |
| Interfaz y usabilidad | 5 % | — | Identidad Ax, **navegación superior** con el módulo activo marcado, editor interactivo, **gráficas interactivas**, probado a 1440, 1366 y 1024 px | Capturas en `docs/capturas/`; `TestNavegacion` | COMPLETADO (juicio de la docente) |
| Manual de usuario | 3 % | `docs/manual_usuario.md` (editor y gráficas documentados) | — | Probado en otra computadora (equipo) | COMPLETADO |
| Casos de prueba | 3 % | `casos_prueba/`, 232 pruebas | — | — | Propios: COMPLETADO. **Caso obligatorio: PENDIENTE (externo, no recibido)** |

### 7.2 Incentivos (hasta 5 %): versión vigente

| Incentivo | Valor | Qué exige (OFICIAL p. 5) | Implementación y funciones | En la interfaz y cómo se demuestra | Pruebas | ¿Cumple? |
|---|---:|---|---|---|---|---|
| Visualización avanzada | 1 % | «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» | `interactivas.comparacion`, `convergencia`, `autovalores`, `precondicionador`; `csv_historial`; barrido de ω | IV → «Comparar métodos»: e/d/r de los 3 métodos superpuestos, cursor con los 3 valores, zoom por región y series activables. «Ejecutar» → historial y descarga CSV | `test_graficas_interactivas`, `test_csv_exportado_contiene_historial_completo` | **Sí:** cubre las tres evidencias citadas. La interactividad **refuerza** la «utilidad real» (comparar iteraciones concretas, ampliar la zona final), pero no es por sí sola el criterio; lo es el contenido comparativo y exportable |
| Precondicionamiento | 1,5 % | «Implementación correcta de un precondicionador diagonal y comparación documentada de su efecto» | `precondicionamiento.py` | IV → pestaña «Precondicionamiento diagonal» → «Analizar»: κ(A) frente a κ(D⁻¹A), T idénticas (exacto), Richardson; gráfica interactiva | `test_precondicionamiento`, auditoría (150 casos) | **Sí.** Riesgo: la docente esperaba quizá ver acelerar a Jacobi, lo que es matemáticamente imposible con M = D (se demuestra en vivo) |
| Matrices dispersas | 1 % | «Representación o tratamiento eficiente… con explicación de la estrategia» | `dispersas.py` (`a_csr`, `paso_*_csr`) | IV → casilla CSR: nnz, densidad y memoria; mismas iteraciones | `test_dispersas`, `test_modulo_IV_formato_csr` | **Sí** |
| Experiencia de usuario | 0,5 % | «Mejoras sustantivas de accesibilidad, ayuda contextual o interacción, no solo decoración» | `editor.py`, recomendaciones, `reordenamiento_dominante`, gráficas interactivas | Editor de matrices con validación previa; 3D manipulable; ayudas en cada campo | `test_editor` (15), `test_app` | **Sí:** la interacción es funcional, no decorativa |
| Extensión matemática | 1 % | «Funcionalidad adicional pertinente, correctamente implementada y defendida» | `polinomio_raices.py` (Faddeev-LeVerrier, Durand-Kerner, Schur-Cohn) y `espectral.py` (p(±1)), T de SOR, Richardson | IV → «Convergencia» | `test_espectral`, auditoría (300 casos) | **Sí**, siempre que la defensa la justifique: no está en los PDF |

**Nada queda pendiente de implementar en los incentivos.** El puntaje lo asigna la docente; el riesgo principal es la defensa de las extensiones.


## 8. Navegación superior y rediseño integral (03-nov-2026, rama `feature/navegacion-superior`)

Es la implementación de la Opción A de `propuesta_navegacion.md`. **No se modificó** `algebra/`, `visualizacion/` ni `auditoria/`, ni ninguna fórmula, algoritmo, validación o dato de las gráficas. Los 23 ejemplos precargados dan resultados idénticos a los de antes, comparados con el oráculo independiente.

### 8.1 Navegación

- **Barra superior nativa** (`st.navigation(..., position="top")`): Inicio, I · Sistemas lineales, II · Condicionamiento, III · Mínimos cuadrados y IV · Métodos iterativos.
- **Una dirección por módulo:** `/sistemas`, `/condicionamiento`, `/minimos` y `/iterativos`. Funcionan los botones «atrás» y «adelante» del navegador.
- **Registro único** en `interfaz/navegacion.py`. Lo usan `app.py`, la portada y las pruebas. Cada archivo de `paginas/` solo llama al `mostrar()` de su módulo, y las claves de los widgets no cambiaron.
- **Módulo activo:** texto blanco y un subrayado cian de 2 px que se desliza en 200 ms al cambiar de página. Las demás opciones van en gris y se aclaran al pasar el cursor.
- **Barra lateral eliminada.** Tenía la marca y dos notas. La marca pasó a la barra superior (`st.logo`, `interfaz/recursos/marca.svg`), la ayuda de entrada ya estaba en cada editor y en la portada, y la información de la UCR va en el pie de la portada.

### 8.2 Identidad

- **Sistema de diseño único** (`interfaz/compartido/estilo.py`, 10 secciones). Los colores, las tipografías, los radios y las duraciones son variables en `:root`; ningún estilo está repetido en los módulos.
- **Menos efectos.** Se quitaron los halos de fondo, los degradados de la portada, las cabeceras y los botones, el texto con degradado y las sombras grandes.
- **Una sola tarjeta por resultado:** el resultado principal, con un borde cian a la izquierda. Las métricas dejaron de ser tarjetas: ahora son columnas separadas por reglas finas.
- **Uso del color:** el cian marca lo activo o el resultado, y el violeta, los incentivos.
- **Tipografía**, toda local, sin fuentes externas ni internet:
  - títulos en **Bahnschrift**, que viene con Windows 10/11 (si falta, Segoe UI);
  - texto en Segoe UI;
  - matrices, celdas del editor, números de sección y rótulos técnicos en **Cascadia Code / Consolas**;
  - cifras tabulares en las métricas y las tablas.

### 8.3 Portada

- Composición editorial, sin rejilla de tarjetas:
  - a la izquierda, el título, el propósito y tres datos clave (núcleo, directos, iterativos);
  - a la derecha, una figura matemática sobre papel cuadriculado tenue.
- **La figura no es decorativa.** Es la eliminación de Gauss-Jordan [A | b] ∼ [I | x] del primer ejemplo del Módulo I, que el núcleo calcula al abrir la página: x = (1/3, 4, 5/3), rango 3 y det(A) = 3. Una prueba lo comprueba.
- **Cuatro módulos en columnas**, cada uno con su número romano, título, una frase y el enlace «Abrir el módulo».
- **Los cinco incentivos en una lista de filas** (nombre, valor máximo, descripción, «Dónde verlo» y el enlace «Ver →»), sin insignias.

### 8.4 Pantallas de los módulos

- **Cabecera editorial:** rótulo «MÓDULO I» en mono cian, título de 1,75 a 2,25 rem y descripción. Ya no va en una caja.
- **Etapas numeradas** (01, 02, 03) con una regla fina.
- **Editor de matrices:** aprovecha el ancho que liberó la barra lateral. Las celdas conservan su tamaño mínimo (2,45 rem de alto, fuente de 1,02 rem).
- **Gráficas:** ganan ancho, mantienen su altura y toda la interactividad. La 3D del Módulo I pasó a ocupar 5/7 del expansor, con 859 px de ancho a 1440 px y 560 px de alto, igual que antes. Se comprobó con un arrastre real del ratón que la cámara rota.
- **Fórmulas:** más espacio vertical en `katex-display`.

### 8.5 Animaciones (solo `opacity` y `transform`, de 140 a 220 ms)

| Microinteracción | Duración | Comprobado con eventos `animationstart` reales |
|---|---|---|
| Aparición del resultado principal | 220 ms | Se reproduce **una vez** al pulsar «Resolver»; en reruns posteriores (cambiar el método o el pivoteo), **0 eventos** |
| Cambio de página (cabecera) | 200 ms | Una vez por cambio de módulo |
| Indicador de la barra superior | 200 ms | Transición del subrayado |
| Cambio de pestaña (panel e indicador) | 200 ms | Un fundido por cambio; 0 en reruns |
| «Cargar ejemplo» | 220 ms | Destello del borde de los dos editores **solo** en esa ejecución, más el aviso «Ejemplo cargado · …»; en el rerun siguiente, 0 eventos y la marca desaparece |
| Hover y pulsación de botones, enlaces y pestañas; color de los campos | 140 ms | Transiciones de color y 1 px de elevación |

- **Movimiento reducido:** con `prefers-reduced-motion: reduce` (emulado), todas las duraciones quedan en 0 s.
- **Descartado:** partículas, paralaje, números que cuentan y animaciones infinitas.
- **Corrección detectada al medir:** en Streamlit 1.66 las pestañas usan react-aria (`data-testid="stTab"`), no baseweb. Los selectores antiguos de pestañas no tenían efecto y se reemplazaron.

### 8.6 Responsive

Las 9 pantallas (portada, I, II, III, ajuste y las 4 pestañas de IV) se revisaron con Chromium sin interfaz, el mismo motor que Brave, a **1440×900, 1366×768 y 1024×768**:

- **sin desbordamiento horizontal** en ninguna de las 27 (`scrollWidth` = ancho de la ventana);
- la barra superior cabe completa;
- el módulo activo siempre se identifica.

La aplicación se abrió también en Brave.

**Capturas:**

- `capturas/0_inicio.png`, `1_modulo_I.png`, `1b_geometria.png`, `2_modulo_II.png`, `3_modulo_III*.png` y `4*_modulo_IV_*.png` (1440 px);
- `nav_1366_*.png` y `nav_1024_*.png`;
- `antes_navegacion_inicio.png`: la portada anterior.

### 8.7 Pruebas

- **Adaptación:** las pruebas de interfaz pasaron de `at.sidebar.radio(key="navegacion")` a `at.switch_page(nav.SISTEMAS)`, etc. Lo que verifican no cambió.
- **4 pruebas nuevas** (`TestNavegacion`):
  - registro de páginas;
  - cada página abre su módulo y la barra lateral queda vacía;
  - la portada enlaza los 4 módulos y los 5 incentivos;
  - la figura de la portada es el resultado del núcleo.
- **Empaquetado:** `paginas/` y la marca se entregan en el ZIP, y `test_empaquetado` lo comprueba.
- **Total:** 232 pruebas OK; la auditoría sigue con 0 fallos.

## 9. Gráficas de exploración (10-nov-2026, rama `feature/graficas-exploracion`)

Las gráficas 2D pasan de mostrar resultados a permitir explorarlos:

- iteración elegida con un clic o con el deslizador, y un panel de detalle;
- selección de zonas;
- hitos tomados del código de terminación real;
- método destacado;
- pantalla completa señalada en la ayuda.

La gráfica 3D y su control gestual no cambiaron. Propuesta, decisiones, verificación y capturas en [propuesta_graficas.md](propuesta_graficas.md).

