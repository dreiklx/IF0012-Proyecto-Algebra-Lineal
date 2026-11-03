# Estado del desarrollo

**Última actualización:** 03-nov-2026, comparación con los PDF de la docente y auditoría de las dos rúbricas. El historial completo está en `git log`.

## Datos del proyecto

| Dato | Valor |
|---|---|
| Curso | IF0012 Álgebra Lineal para Informática Empresarial, II Ciclo 2026 |
| Integrantes | Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias, Samir Sandoval Ramírez |
| Entrega | **11 de noviembre de 2026** |
| Defensa individual | Semana del **16 de noviembre de 2026** |
| Número de grupo | **01, confirmado por el equipo (03-nov-2026)**. Integrantes, exclusivamente los cuatro de arriba |

## Gráficas interactivas y reauditoría (03-nov-2026, rama `feature/graficas-interactivas`)

- **Gráficas:** Plotly 6.3.0 (única dependencia nueva) en `visualizacion/interactivas.py`. La 3D se puede rotar, ampliar y restablecer, y muestra valores al pasar el cursor; las 2D tienen zoom ＋/－ y por región, desplazamiento, autoescala, restablecer, valores y series activables. Los datos son exactamente los del núcleo (`tests/test_graficas_interactivas.py`, 8 pruebas).
- **Seguridad:** se restauraron `.env` y `.env.*` en `.gitignore` (el commit 59dd149 los había quitado) y una prueba lo vigila. No hay credenciales en los archivos rastreados ni en el historial (búsqueda de nombres y patrones; ningún valor se imprimió).
- **Reauditoría contra los PDF:** los archivos son los originales (huellas, tamaños y fechas); hay una sola versión de la rúbrica; los métodos que no están en los PDF siguen marcados como extensión. Detalle en `comparacion_procedimientos.md`. El editor no altera ningún ejemplo (prueba nueva).
- **Propuesta de navegación** (no implementada): `propuesta_navegacion.md`.
- **Pruebas:** 228 OK; la auditoría sigue con 0 fallos; los ejemplos precargados dan resultados idénticos; sin cambios en `algebra/` ni `auditoria/`.

## Editor interactivo de datos (03-nov-2026, rama `feature/editor-interactivo`)

- **Componente nuevo:** `interfaz/editor.py`, con tres tipos (MATRIZ, VECTOR y PUNTOS), integrado en los cuatro módulos.
  - Pestañas «Editor» (rejilla, ＋/－ filas y columnas, identidad, ceros, limpiar, restaurar) y «Pegar» (espacios, tabulaciones, «;» o «, », con vista previa).
  - Botón «⟲ Cargar ejemplo».
  - Tabla de puntos en el Módulo III y editor de x⁽⁰⁾ en el Módulo IV.
- **Validación previa visual:** faltan valores, formato inválido con su posición, y dimensiones incompatibles que bloquean el botón. Las validaciones del núcleo no se tocaron.
- **Sin cambios** en `algebra/` ni `auditoria/`; ninguna prueba existente se modificó.
- **Pruebas:** 217, todas OK (las 204 anteriores más las 13 de `tests/test_editor.py`). La auditoría sigue con 0 fallos y los ejemplos precargados dan resultados idénticos.

## Rediseño visual (03-nov-2026, rama `feature/rediseño-visual`)

- **Identidad propia:** tema oscuro de software científico, portada con tarjetas de los cuatro módulos y de los cinco incentivos (con accesos directos), etapas numeradas, tarjetas de resultado, etiquetas de estado, barra de la escala de κ, recomendaciones contextuales y gráficas con un tema común.
- **Archivos nuevos:** `interfaz/estilo.py` y `visualizacion/tema.py`. Archivos modificados: `app.py`, las cuatro pantallas de `interfaz/`, `visualizacion/graficos.py`, `visualizacion/geometria_3d.py` y `.streamlit/config.toml`.
- **Sin cambios** en `algebra/`, `tests/` ni `auditoria/`. Los resultados de los 25 ejemplos precargados son idénticos byte a byte; 204 pruebas OK y la auditoría con 0 fallos.
- **Documentación:** `docs/diseno_visual.md` (matrices de la rúbrica y de los incentivos con su presentación) y capturas en `docs/capturas/`.

## Actualización del 03-nov-2026 (tercera parte): organización del grupo

- **Grupo 01 confirmado:** Derek, Elmer, Samir y Daniel.
- **Manual:** la prueba en otra computadora quedó completada (confirmada por el equipo).
- **Repositorio:** GitHub creado y sincronizado.
- **Invitaciones:** enviadas a `samir24cr`, `NaygellArias` y `ELMER100102`, con permiso de escritura. Estaban **pendientes de aceptación** al momento de registrarlas.
- **IA:** el pendiente se reevaluó. No hay requisito de autorización previa y se mantiene la declaración. Detalle en `pendientes_docente.md`.
- **Sin cambios** en la lógica ni en la interfaz.

## Revisión del 03-nov-2026 (segunda parte): grupo, GitHub y separación de archivos

1. **Grupo 01 confirmado por el equipo.** Integrantes, exclusivamente: Elmer López Hernández, Derek Farley Noguera, Daniel Córdoba Arias y Samir Sandoval Ramírez. Se actualizaron los pendientes, la matriz de cumplimiento, las decisiones técnicas y el README. Los números de carné **no** se incluyen en el repositorio, porque son datos personales que ningún requisito del enunciado pide.
2. **Caso obligatorio (P-3).** Se releyó el enunciado y se revisó el texto de todos los PDF del curso. El caso **no está en ningún documento**. Se detalló qué dice cada página, qué acredita (rúbrica «Casos de prueba», 3 %), cómo incorporarlo y la pregunta exacta para la docente (`pendientes_docente.md`, P-3; `casos_prueba/README.md`).
3. **Archivos internos de IA y credenciales fuera de la entrega y del repositorio:**
   - `.gitignore` excluye `CLAUDE.md`, `CLAUDE.local.md`, `.claude/`, `.mcp.json`, `.env*`, claves y archivos temporales.
   - `empaquetar.py` los excluye y, además, se niega a crear el ZIP si encontrara alguno (prueba `tests/test_empaquetado.py`).
   - Se comprobó que **ninguno** existe en el proyecto ni en el historial de Git.
   - La declaración del uso de IA (`docs/herramientas_y_bibliotecas.md` §4) **se conserva** y se entrega.
   - Se quitó de dos documentos la ruta local que contenía el nombre de usuario del equipo.
4. **Generador del HTML en el repositorio:** `herramientas/generar_guia_html.py` (solo de desarrollo, fuera del ZIP; requiere `requirements-desarrollo.txt`). Reproduce byte a byte el HTML ya compartido. Ahora escribe a la vez `dist/Guia_Defensa_IF0012.html` y la copia del escritorio, y toma de la guía la versión y el número de pruebas.
5. **Pruebas:** 204 (las 202 anteriores más 2 del empaquetado), todas OK. Auditorías: 0 fallos.
6. **ZIP regenerado:** 64 archivos, verificado en una copia extraída (pruebas OK y auditorías con 0 fallos). El anterior quedó en `dist/anteriores/`.
7. **Repositorio central en GitHub (privado):** `https://github.com/dreiklx/IF0012-Proyecto-Algebra-Lineal`, rama `main`. Reglas de trabajo en el README.
   - Se versiona: el código, las pruebas, la auditoría, la documentación y la entrega estable de `dist/` (ZIP, SHA256.txt y la guía HTML).
   - No se versiona: `.venv`, las cachés, `dist/anteriores/` ni las copias de documentos de `dist/`.

## Revisión del 03-nov-2026: comparación con los PDF y rúbricas

1. **Inventario y lectura de los PDF.** Se usó el inventario de la auditoría documental (19 archivos). Se releyeron en imagen las páginas clave:
   - mínimos cuadrados: S8-30/09 pp. 6-7;
   - condicionamiento: S7-21/09 pp. 17-18;
   - comparación y SOR: S9-05/10 pp. 16-17;
   - precondicionamiento: S9-05/10 pp. 21-24;
   - matrices de iteración y ρ: S9-07/10 pp. 4 y 6.

   También se releyeron el enunciado oficial completo (texto) y PROG p. 9. **No inspeccionados visualmente:** las semanas 1, 2 y 4 y el Quiz (Tema 1, sin procedimientos del proyecto). Resultado en [comparacion_procedimientos.md](comparacion_procedimientos.md).
2. **Hallazgos:**
   - **«Error final» = ‖x⁽ᵏ⁾ − x‖∞** según la lámina S9-05/10 p. 17. Coincide con nuestro e. P-4 resuelto.
   - **Grupo 01:** el horario coincide con el programa; después lo confirmó el equipo (P-1 resuelto).
   - **Precondicionamiento:** la lámina indica qué comparar (κ y ρ de A frente a B = D⁻¹A).
   - **Procedimientos de clase no visibles en la aplicación:** det([A|b]) y Cramer en mínimos cuadrados; Sarrus en det(T − λI); reordenamiento de ecuaciones para lograr la dominancia.
3. **Implementado:**
   - `algebra/precondicionamiento.py`, con la pestaña «Precondicionamiento diagonal», y `paso_richardson`;
   - `minimos.cramer` y `det_aumentada`, con el desplegable de verificación del procedimiento de clase;
   - `espectral.desarrollo_sarrus`, mostrado para T 3×3;
   - `espectral.analizar_matriz`, una refactorización sin cambio de resultados: los 300 casos aleatorios y los ejemplos precargados dan lo mismo que el 02-nov;
   - `iterativos.reordenamiento_dominante`, mostrado en «Convergencia»;
   - e_k como primera métrica de la gráfica comparativa;
   - la gráfica del precondicionador recorta las curvas divergentes.
4. **Defecto corregido:** con un aᵢᵢ = 0, la pestaña «Convergencia» no mostraba ni la dominancia ni el reordenamiento, porque fallaba al construir T. Ahora los muestra junto con el error (prueba `test_modulo_IV_reordenamiento_y_sarrus`).
5. **Pruebas nuevas (17):**
   - `tests/test_precondicionamiento.py` (14), con oráculos de la lámina, a mano y de la teoría de la tridiagonal;
   - 3 pruebas de interfaz.
   - Auditoría nueva: `auditoria/auditoria_precondicionamiento.py`, 150 casos y 0 fallos.
6. **Revisión visual (Chrome, 03-nov):**
   - pestaña «Precondicionamiento diagonal» de la aplicación real con el ejemplo S: matrices, κ, autovalores, tabla y gráfica;
   - HTML de la guía: portada, índice, tablas, fórmulas y listas, sin restos de Markdown. Se corrigieron una tabla duplicada y asteriscos y guiones bajos mal interpretados.
7. **Documentación actualizada:**
   - matriz de cumplimiento con las dos rúbricas (`auditoria_requisitos.md`);
   - manual;
   - guía de defensa (34 preguntas) y resumen;
   - guía matemática §10;
   - decisiones técnicas #25 y #28-31;
   - casos III-6 e IV-23 a IV-26;
   - pendientes con la docente.
8. **HTML para compartir:** `%USERPROFILE%\Desktop\Guia_Defensa_IF0012.html` (copia versionada en `dist/Guia_Defensa_IF0012.html`), un solo archivo sin dependencias externas. Contiene la guía completa y el resumen.

## Revisión del 02-nov-2026: qué se hizo

1. **Requisitos.** Se releyó el enunciado oficial (pp. 1-5) y se rehízo la matriz de cumplimiento con los estados COMPLETADO, INCOMPLETO, FALLIDO y PENDIENTE DE CONFIRMACIÓN EXTERNA. Ver [auditoria_requisitos.md](auditoria_requisitos.md). **Ningún requisito queda FALLIDO.**
2. **Revisión matemática de los cuatro módulos.** Se leyeron completos `matriz`, `validacion`, `directos`, `condicion`, `minimos`, `iterativos`, `espectral` y `dispersas`, y las interfaces.
   - Se comprobaron:
     - las fórmulas: Gauss, Gauss-Jordan, determinante, κ∞, ecuaciones normales, los tres pasos iterativos, T_J, T_GS, T_ω, Faddeev-LeVerrier, Schur-Cohn y Durand-Kerner;
     - el tratamiento de los casos especiales;
     - la coherencia entre lo que se calcula y lo que se muestra.
   - **No se encontró ningún error matemático, así que no se modificó el código del núcleo ni de la interfaz.**
   - Pruebas adicionales ejecutadas en esta revisión:
     - casos límite: matriz cero (infinitas o inconsistente), sistemas 1×1, 3×2 consistente e inconsistente, 1×3 y 2×3, inversa 1×1, κ(I) = 1, mínimos cuadrados cuadrado y subdeterminado, iterativos con n = 1, SOR con ω = 1 igual a GS, y radio espectral en 2×2 con raíces complejas o λ = ±1;
     - tiempos: ρ para n = 8 en 0.03 s; comparación con n = 50 en 0.07 s;
     - **todos los ejemplos precargados** recalculados con oráculos escritos aparte: Cramer con determinantes de Leibniz (I), inversa por adjunta (κ), fórmula cerrada de la recta (III) y fórmula de Gelfand ‖T¹²⁸‖^(1/128) (ρ). Todos coinciden.
3. **Nuevo caso verificado (IV-22).** En S9-07/10 con SOR y ω = 6/5 (el ω por defecto), λ = −1 es autovalor exacto: det((2 − ω)D + ωL − ωU) = 0, comprobado a mano. Se añadió la prueba `test_sor_s9_omega_6_5_autovalor_menos_uno_exacto`, de modo que ahora hay **185 pruebas**.
4. **Revisión visual pendiente.** La gráfica de convergencia de una ejecución individual (criterios A y B, sistema S) se generó como imagen y se revisó: d₇ = 3.78·10⁻⁴ < ε y r₇ = 8.79·10⁻⁴ < ε, como en IV-1 e IV-4. **Siguen sin verse dentro del navegador** la figura 3D y el espaciado de las fracciones.
5. **Correcciones de documentación.**
   - La precisión con raíces múltiples ahora es exacta: ≈10⁻⁸ en una raíz doble, que suele decidirse con la banda de 10⁻⁶, y ≈10⁻⁵ en una triple, que queda «indeterminado».
   - Se añadieron `dispersas.py` y `auditoria/` al árbol de `arquitectura.md`.
6. **Documentos nuevos:**
   - [guia_defensa_equipo.md](guia_defensa_equipo.md): guía completa para el equipo;
   - [resumen_logica_por_modulo.md](resumen_logica_por_modulo.md): resumen de estudio;
   - [pendientes_docente.md](pendientes_docente.md): pendientes con la docente, con su interpretación provisional y la pregunta exacta.

## Pruebas: resultados reales (03-nov-2026)

```
.venv\Scripts\python -m unittest
Ran 228 tests ... OK            (0 fallos, 0 omitidas; 03-nov-2026)
```

| Archivo | Pruebas | Qué cubre | Tipo de oráculo |
|---|---:|---|---|
| test_matriz | 47 | Validación, operaciones, normas, residuo | Valores calculados a mano y ejemplos del curso |
| test_validacion | 13 | Lectura de texto, parámetros, formato | Casos construidos a mano |
| test_directos | 26 | Gauss, Gauss-Jordan, clasificación, inversa, determinante | Sustitución a mano; inversa por adjunta |
| test_condicion | 13 | κ∞, escala, perturbaciones | Inversa 2×2 por fórmula; estructura I + 10J |
| test_minimos | 10 | Ecuaciones normales, residuo, ajuste | Cramer; fórmula cerrada de la recta; Aᵀr = 0 |
| test_iterativos | 31 | Jacobi, GS y SOR, criterios A/B/C, motivos, comparación | Programa independiente, manuscritos y el ZIP de la Tarea II |
| test_espectral | 25 | T, polinomio, autovalores, ρ, regresiones | Sarrus a mano, formas cerradas, bisección, teoría tridiagonal, determinante a mano (IV-22) |
| test_dispersas | 8 | Formato CSR | Construcción a mano; igualdad con la versión densa |
| test_precondicionamiento | 14 | Precondicionador M = D, Richardson, reordenamiento, Sarrus, Cramer | Lámina S9-05/10 diap. 18; inversas 2×2 a mano; autovalores teóricos de la tridiagonal; manuscrito S8-30/09 |
| test_empaquetado | 2 | El ZIP excluye los archivos internos de IA, las credenciales y las cachés; una sola carpeta raíz | Proyecto temporal con archivos trampa |
| test_editor | 13 | Editor interactivo: separadores, celdas, botones, pegado, bloqueo por dimensiones, x⁽⁰⁾, tabla de puntos | Construcción a mano; recta de 3 puntos calculada a mano |
| test_graficas_interactivas | 8 | Datos de las gráficas Plotly = núcleo = Matplotlib; planos en su ecuación; vista acotada sin perder datos | Resultados del núcleo y líneas de Matplotlib |
| test_app | 15 | La interfaz con AppTest (sin navegador) y el CSV | **Superficiales:** comprueban que no hay excepciones y que aparecen los mensajes, **no** el contenido visual de las gráficas |

**Auditoría independiente** (`auditoria/`, semilla fija) — **0 fallos**:

- 4500 sistemas;
- 400 inversas, determinantes y κ;
- 200 perturbaciones;
- 300 mínimos cuadrados;
- 600 ejecuciones iterativas;
- 300 análisis espectrales aleatorios (0 indeterminados, 0 no fiables);
- casos difíciles: con raíces casi iguales, escalas muy distintas o ρ = 0.999999 el resultado es fiable; con el par complejo doble y la raíz cuádruple se marca «no fiable», como corresponde.

## Limitaciones conocidas (no resueltas)

1. **Autovalores múltiples.** Con raíces triples o de mayor multiplicidad ρ suele quedar «indeterminado». Con raíces dobles se decide con la banda de 10⁻⁶ y un aviso.
2. Las gráficas no tienen pruebas automáticas de su contenido visual.
3. La instalación se probó en entornos virtuales nuevos **en este equipo**, no en otro computador.
4. Streamlit y Matplotlib instalan NumPy como dependencia interna. Ningún archivo del proyecto lo importa.

## Empaquetado

Ver la sección «Verificación del ZIP», al final de este archivo.

## Pendientes

Los que dependen de la docente están detallados en [pendientes_docente.md](pendientes_docente.md), con la pregunta exacta para cada uno.

| # | Pendiente | Impacto | Quién |
|---|---|---|---|
| P-1 | ~~Número de grupo~~ | **Resuelto:** grupo 01, confirmado por el equipo | — |
| P-2 | Uso de IA | **Declarado.** No hay requisito de autorización previa (PROG §6.2 y OFICIAL revisados); no bloquea | — |
| P-3 | **Caso de validación obligatorio** | C-07 (3 %) | Docente |
| P-4 | Significado de «error final» | **Resuelto** con la lámina S9-05/10 p. 17 | — |
| P-5 | Alcance del radio espectral (métodos que no se vieron en clase) | M4-05 | Docente |
| P-6 | NumPy como dependencia interna | Resuelto por el enunciado; confirmación opcional | — |
| P-7 | Perturbación porcentual | Resuelto: ‖Δb‖/‖b‖ = p/100 en ambas lecturas; confirmación opcional | — |
| P-8 | Precondicionamiento | **Implementado** con la comparación de la lámina; confirmación opcional | — |
| G-1 | ~~Manual en otra computadora~~ | **Completado:** confirmado por el equipo el 03-nov | — |
| G-4 | Aceptar las invitaciones a GitHub (`samir24cr`, `NaygellArias`, `ELMER100102`) | Acceso al repositorio central | Cada compañero |
| G-2 | Cada integrante instala, ensaya la demostración y estudia la guía | Defensa (35 %) | Los 4 integrantes |
| G-3 | Mirar dentro del navegador la figura 3D y las fracciones | C-05 (estético) | Grupo |

## Verificación del ZIP

ZIP generado el 03-nov-2026 con `python empaquetar.py 01`: `dist/Grupo01-IF0012-Proyecto-IIC.zip`. Grupo 01, confirmado por el equipo.

- **Contenido:** 64 archivos (regenerado tras la segunda parte del 03-nov), una sola carpeta raíz (`Grupo01-IF0012-Proyecto-IIC/`) y `testzip` sin errores. Incluye `algebra/precondicionamiento.py`, `tests/test_precondicionamiento.py`, `auditoria/auditoria_precondicionamiento.py` y `docs/comparacion_procedimientos.md`.
- **Exclusiones:** sin `.venv`, `__pycache__`, `.pyc`, `.git`, `dist`, imágenes ni `secrets.toml`.
- **Prueba en una copia limpia** (03-nov):
  - el ZIP se extrajo en una carpeta nueva;
  - `ejecutar.bat` creó `.venv` (Python 3.14.1) e instaló las dependencias;
  - el servidor respondió `ok` a los ~58 s (puerto 8502);
  - en esa copia: **202 pruebas OK** y las 3 auditorías con **0 fallos**.
- **Candidatos anteriores** (27-oct y 02-nov): se conservaron, sin sobrescribirlos, en `dist/anteriores/`.
- **Después de la verificación** solo se modificó esta sección y se regeneró el ZIP. El SHA-256 final está en `dist/SHA256.txt`.
