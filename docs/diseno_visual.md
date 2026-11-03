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

- **Paleta** (`.streamlit/config.toml`, `interfaz/estilo.py`, `visualizacion/tema.py`):

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
- **Componentes** (`interfaz/estilo.py`, solo presentación):
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
| Diseño del código | 5 % | Capas `algebra/`, `interfaz/`, `visualizacion/` | Estilo centralizado en `interfaz/estilo.py` y `visualizacion/tema.py`; los módulos no repiten CSS | `docs/arquitectura.md` | COMPLETADO |
| Validaciones y errores | 4 % | `validacion.py`, `validar_configuracion`, `ejecutar` sin excepciones | Errores en rojo con la celda exacta; recomendaciones | `test_validacion`, `test_modulo_I_entrada_invalida` | COMPLETADO |
| Interfaz y usabilidad | 5 % | — | Identidad visual propia; navegación con el módulo activo resaltado; etapas numeradas; portada con accesos directos; probado a 1440 y 1024 px | `capturas/0_inicio.png`, `9_modulo_IV_1024px.png` | COMPLETADO (juicio de la docente) |
| Manual de usuario | 3 % | `docs/manual_usuario.md` | Actualizado con la portada y los accesos | Probado en otra computadora (equipo, 03-nov) | COMPLETADO |
| Casos de prueba | 3 % | `casos_prueba/`, `tests/` | — | 204 pruebas | Casos propios: COMPLETADO. **Caso obligatorio: PENDIENTE (externo)** |

## 4. Incentivos (hasta 5 %): funcionalidad real y dónde se ve

| Incentivo | Máx. | Requisito (OFICIAL p. 5) | Funcionalidad y código | Dónde en la interfaz y cómo se usa | Evidencia | Estado |
|---|---:|---|---|---|---|---|
| Visualización avanzada | 1 % | «Gráficas comparativas adicionales, historial de convergencia o reportes exportables con utilidad real» | `grafica_comparacion`, `grafica_autovalores`, `grafica_convergencia`, `grafica_precondicionador`, barrido de ω, `csv_historial` | IV → «Comparar métodos» (gráfica e/d/r); «Ejecutar» → «Descargar tabla (CSV)»; «Convergencia» → autovalores | `test_csv_exportado_contiene_historial_completo`; `capturas/4b`, `4c` | COMPLETADO |
| Precondicionamiento | 1,5 % | «Implementación correcta de un precondicionador diagonal y comparación documentada de su efecto» | `algebra/precondicionamiento.py` (`precondicionar_diagonal`, `analizar_precondicionador`), `paso_richardson` | IV → pestaña «Precondicionamiento diagonal» → «Analizar el precondicionador M = D»; tarjeta con κ, T idénticas y efecto en Richardson | `test_precondicionamiento`, auditoría de 150 casos; `capturas/4d` | COMPLETADO |
| Matrices dispersas | 1 % | «Representación o tratamiento eficiente de matrices dispersas, con explicación de la estrategia» | `algebra/dispersas.py` (`a_csr`, `paso_*_csr`) | IV → «Ejecutar un método» → casilla «Usar almacenamiento disperso (CSR)»; informa nnz, densidad y memoria | `test_dispersas`, `test_modulo_IV_formato_csr` | COMPLETADO |
| Experiencia de usuario | 0,5 % | «Mejoras sustantivas de accesibilidad, ayuda contextual o interacción, no solo decoración» | Ejemplos precargados, ayudas en los campos, errores con la posición, recomendaciones, `reordenamiento_dominante`, interpretación geométrica, accesos desde la portada | Todos los módulos; I → «Interpretación geométrica»; IV → «Convergencia» (reordenamiento) | `test_app`, `test_modulo_IV_reordenamiento_y_sarrus` | COMPLETADO |
| Extensión matemática | 1 % | «Funcionalidad adicional pertinente, correctamente implementada y defendida» | `espectral.py`: Faddeev-LeVerrier, Durand-Kerner, Schur-Cohn, p(±1) = 0; T de SOR; Richardson | IV → «Convergencia: dominancia y radio espectral» | `test_espectral`; 300 casos de auditoría | COMPLETADO |

Las marcas violetas «Incentivo · …» aparecen **junto a la funcionalidad real** que lo implementa: son señales para la demostración y no sustituyen ninguna funcionalidad. Ningún incentivo se simula con elementos visuales: los cinco existían y estaban probados antes del rediseño.

## 4b. Editor interactivo de datos (03-nov-2026, rama `feature/editor-interactivo`)

**Componente:** `interfaz/editor.py`, función `editor(...)`, con tres tipos (MATRIZ, VECTOR y PUNTOS), reutilizado en los cuatro módulos.

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
- **Pruebas:** `tests/test_editor.py`, 13 pruebas con funciones puras e interacción real con AppTest: edición de celdas, botones, identidad, restaurar, pegado con comas, bloqueo por dimensiones, x⁽⁰⁾ y tabla de puntos (con la recta esperada calculada a mano).
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

**Nota de desarrollo:** el servidor de Streamlit no recarga `interfaz/estilo.py` al modificarlo; tras cambiar el estilo hay que reiniciar la aplicación.
