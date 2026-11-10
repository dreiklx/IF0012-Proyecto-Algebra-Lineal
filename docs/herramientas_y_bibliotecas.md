# Herramientas y bibliotecas utilizadas

OFICIAL p. 1: «Si se utiliza una librería únicamente para visualización, interfaz o manejo de archivos, debe indicarse en la documentación».

## 1. Núcleo matemático (`algebra/`)

Solo se usa la **biblioteca estándar de Python 3.13**:

| Módulo estándar | Uso |
|---|---|
| `fractions.Fraction` | Representación exacta de números racionales: aritmética elemental |
| `math.sqrt`, `math.isfinite` | Raíz cuadrada de ‖r‖₂² y de discriminantes; comprobación de valores finitos |
| `cmath.sqrt` | Raíz cuadrada de discriminantes negativos (autovalores complejos) |
| `dataclasses` | Estructuras de datos para los resultados |

**No se usa** ninguna función que implemente Gauss, Gauss-Jordan, la inversa, determinantes, mínimos cuadrados, Jacobi, Gauss-Seidel, SOR, autovalores, raíces de polinomios ni el radio espectral. Todo eso está escrito en `algebra/`.

Se comprueba con:

```
grep -rn "^import\|^from" algebra/
```

Solo aparecen `fractions`, `math`, `cmath`, `dataclasses` y módulos propios.

Queda **[pendiente de confirmar con la docente]** si `math.sqrt` y `cmath.sqrt` se consideran «operaciones aritméticas elementales».

## 2. Interfaz, gráficas y archivos

| Biblioteca | Versión | Uso exclusivo |
|---|---|---|
| Streamlit | 1.66.1 | Interfaz web local (formularios, tablas, pestañas, descarga de CSV) |
| Plotly | 6.3.0 | **Gráficas interactivas de la interfaz** (desde el 03-nov-2026): rotar la figura 3D, acercar y alejar, zoom por región, desplazar, autoescala y restablecer, valores al pasar el cursor, ocultar y mostrar series. Solo dibuja datos calculados por `algebra/` (`visualizacion/interactivas.py`) |
| Matplotlib | 3.11.2 | Figuras estáticas equivalentes (`visualizacion/graficos.py`, `geometria_3d.py`): se conservan como respaldo y para las pruebas que comparan que ambas dibujan los mismos datos |
| `csv`, `io` (estándar) | — | Exportar la tabla de iteraciones |

**Por qué Plotly.** Altair, que ya instalaba Streamlit, no hace gráficas 3D; Plotly cubre la 3D y la 2D con una misma barra de herramientas. Es la única dependencia nueva y funciona sin internet, porque plotly.js viene dentro del paquete.

**Dependencias transitivas.** Streamlit, Matplotlib y Plotly instalan internamente NumPy 2.5.4, pandas 3.1.0, pyarrow y altair; la lista completa está en `requirements-bloqueado.txt`.

- **Nuestro código no importa NumPy ni pandas.**
- Estas bibliotecas las usan Streamlit y Matplotlib por dentro, para dibujar y para mostrar tablas.
- Conviene confirmarlo con la docente, porque la autorización de NumPy está pendiente.

## 3. Herramientas de desarrollo

| Herramienta | Uso |
|---|---|
| `unittest` (estándar) | Pruebas automáticas |
| `streamlit.testing.v1.AppTest` | Pruebas de integración de la interfaz sin navegador |
| Git + GitHub (repositorio privado `dreiklx/IF0012-Proyecto-Algebra-Lineal`) | Historial de cambios; ramas por funcionalidad, sin `push --force` |

## 4. Uso de herramientas de inteligencia artificial

En el desarrollo se usaron asistentes de IA:

- **Claude Code** (Anthropic): inspección de documentos, implementación del código, pruebas y documentación.
- **ChatGPT** (OpenAI): análisis académico y revisión.

**Marco aplicable:**

- El enunciado del proyecto no contiene disposiciones sobre la IA.
- El programa del curso (PROG p. 7, §6.2) sanciona el «uso indebido de herramientas de inteligencia artificial no autorizadas», como forma de copia o plagio.
- Ninguno de los dos exige un trámite de autorización previa.

En consecuencia:

1. Este uso **se declara aquí**, sin ocultarlo, y la declaración forma parte de la entrega.
2. **No se afirma** que la docente lo haya autorizado expresamente: no hay una respuesta suya al respecto.
3. Cada integrante debe comprender, explicar y reproducir cada algoritmo, porque la defensa es individual. Para eso están `docs/guia_defensa_equipo.md` y `docs/resumen_logica_por_modulo.md`.

El análisis completo está en `docs/pendientes_docente.md`, P-2.

## 5. PyVista (prototipo aislado; no integrado)

**Documentación consultada:** docs.pyvista.org (versión 0.49.1). La integración web ahora vive en el paquete independiente `trame-pyvista`; `Plotter.export_html` está deprecado en favor de `plotter.trame.export_html(...)`.

**Prototipo:** `prototipos/pyvista_planos.py`.

- Resuelve el sistema con **nuestro Gauss** y dibuja con PyVista un `pyvista.Plane` por ecuación y una esfera en la solución. PyVista no calcula nada.
- Se ejecutó en un **entorno virtual separado** (Python 3.13.0, fuera del proyecto): `pip install pyvista==0.49.1` instaló PyVista 0.49.1 y VTK 9.7.1.

| Estado | Resultado (27-oct-2026) |
|---|---|
| Implementado | Sí, como prototipo aislado (`prototipos/`) |
| Probado (render) | **Sí.** El render fuera de pantalla generó `prototipos/planos_pyvista.png` con los tres planos y la solución (1/3, 4, 5/3); la imagen se revisó |
| Probado (exportación web) | **Parcial.** `plotter.trame.export_html` falló primero con `ImportError: nest_asyncio2`. Tras instalar `nest_asyncio2` generó un HTML autónomo (vtk.js) de 1.08 MB, que cargó en Chrome con el título «VTK.js \| Example - OfflineLocalView». **El render en el navegador no se pudo confirmar visualmente**: la captura de pantalla agotó el tiempo |
| Integrado en la aplicación | **No.** Hay que añadir PyVista, VTK, `nest_asyncio2` y 10 paquetes `trame`, incluido `trame-pyvista`; la combinación no está en la documentación de Streamlit ni se probó dentro de la aplicación |

**Decisión:**

- La aplicación obligatoria no depende de PyVista. La interpretación geométrica se hace con Plotly (`visualizacion/interactivas.py`), con Matplotlib como respaldo (`visualizacion/geometria_3d.py`).
- Posible vía futura, experimental y no probada dentro de la aplicación: incrustar el HTML exportado con `streamlit.components.v1.html`.
- Antes de integrarlo habría que probar la estabilidad en el equipo de la defensa.

## 6. Evaluación de bibliotecas para reducir código (10-nov-2026)

**Regla:** no se reemplaza ningún método que la docente espera que implementemos: Gauss, Gauss-Jordan, determinante, inversa, mínimos cuadrados, Jacobi, Gauss-Seidel, SOR y radio espectral (OFICIAL p. 1). Solo se evaluó código auxiliar.

**Medición previa:** pylint `duplicate-code` (bloques de 6 o más líneas) se ejecutó sobre todo el código, de forma aislada con `uvx`, sin instalarlo en el proyecto. Encontró **un solo bloque repetido**, en la visualización, y se resolvió con una función propia (`serie_metrica`), sin dependencias nuevas. El resto del código repetitivo ya estaba centralizado: el editor, la lectura con mensajes y el estilo.

**Clasificación del código:**

| Tipo | Ejemplos | Decisión |
|---|---|---|
| A. Se puede simplificar con bibliotecas | Tablas (listas de diccionarios a `st.dataframe`), CSV (módulo `csv`) | Ya usan lo más simple; pandas no reduce líneas |
| B. Conviene compartir como funciones comunes | Lectura con errores, estilo, series de gráficas | Hecho: `interfaz/compartido/`, `algebra/compartido/`, `serie_metrica` |
| C. Matemática que debemos implementar y entender | `algebra/modulo_*` | **Propia, sin bibliotecas** |
| D. Necesario para mostrar el procedimiento | Pasos de Gauss, tabla de iteraciones, desarrollo de Sarrus | Propio; es lo que se evalúa |

| Biblioteca | Problema que resolvería | Código que reduciría | Impacto | Licencia | Decisión |
|---|---|---|---|---|---|
| NumPy | Operaciones con matrices | `algebra/compartido/matriz.py` (~350 líneas) | **Negativo:** oculta los procedimientos, trabaja en punto flotante (rompe la clasificación exacta) y su `linalg` está prohibido | BSD | **Rechazada** para nuestro código (ya llega como dependencia interna de Streamlit) |
| SciPy / SymPy | Métodos iterativos, autovalores, fracciones simbólicas | Núcleo completo | Sustituiría lo que se evalúa | BSD | **Rechazada** |
| pandas | Tablas y CSV | ~15 líneas | Ninguno real: `st.dataframe` acepta listas de diccionarios | BSD | **Rechazada** (no se importa; llega por Streamlit) |
| pydantic | Validación de entradas | `validacion.py` (~130 líneas) | Mensajes en inglés y menos control de la posición del error; dependencia nueva | MIT | **Rechazada** |
| streamlit-aggrid / data_editor de terceros | Editor de matrices | `editor.py` (~320 líneas) | Cambiaría la validación por celda ya probada; JS adicional | MIT | **Rechazada** |
| attrs | Dataclasses | — | `dataclasses` (estándar) ya cubre el uso | MIT | **Rechazada** |
| ruff / pylint | Calidad del código (no se entregan) | — | Solo desarrollo | MIT / GPL-2.0 | **Usados como herramienta externa** (`uvx`), sin añadir dependencias |

**Resultado:** no se añadió **ninguna** dependencia a `requirements.txt`. Siguen siendo tres (Streamlit, Plotly y Matplotlib), todas de interfaz o gráficas, como lo permite OFICIAL p. 1.

## 7. Herramientas de desarrollo con IA (no forman parte de la entrega)

Están instaladas **a nivel de usuario**, fuera del proyecto. No aparecen en `requirements*.txt` ni en el ZIP, y sus archivos (`graphify-out/`, `.graphifyignore`, `.claude/`, `CLAUDE.md`) están excluidos por `.gitignore` y por `empaquetar.py`.

| Herramienta | Versión y licencia | Instalación | Para qué se usó | Riesgos revisados |
|---|---|---|---|---|
| **uv** | 0.13.7, MIT/Apache-2.0 | `pip install --user uv` (paquete oficial de Astral) | Instalar herramientas aisladas (`uv tool`) | No modifica el proyecto |
| **Graphify** (`graphifyy`) | 0.9.102, Apache-2.0 | `uv tool install graphifyy`; skill de Claude Code en `~/.claude/skills/graphify` | Grafo del código: dependencias, funciones centrales, comunidades, ciclos (ninguno), impacto de cada etapa de la reorganización | Se ejecutó **solo con extracción AST local** (`graphify update .`): sin LLM, sin enviar datos y sin procesar los PDF de la docente (`.graphifyignore`) |
| **Caveman** | 4.0.1, Apache-2.0 | Plugin de usuario de Claude Code (ya instalado el 04-nov) | Respuestas breves en el modo moderado (`caveman`) para los informes de avance | Sus propias reglas excluyen código, documentación, commits y advertencias de seguridad; se activa con un hook al iniciar la sesión |

**Inventario de skills y plugins disponibles en Claude Code (10-nov-2026):**

| Skill o plugin | ¿Útil aquí? | Decisión |
|---|---|---|
| graphify | Sí: arquitectura | Usado |
| caveman | Sí: informes | Instalado; modo moderado |
| code-review, security-review, simplify (integrados) | Sí: revisión antes de entregar | Disponibles sin instalar nada |
| pdf / docx / xlsx / pptx (document-skills) | Parcial: los PDF se revisaron directamente con PyMuPDF en un entorno aparte, con referencias de página | No necesario |
| ui-ux-pro-max | Sí: revisión visual | Disponible (plugin de usuario) |
| vercel, claude-seo, instagram-agent, youtube-agent | No: el proyecto es una aplicación local, no un sitio web | No aplicables |

No se instaló ningún plugin nuevo. Los disponibles cubren Python, pruebas, revisión, seguridad, documentación y diagramas, y cada instalación nueva ejecuta código de terceros y añade instrucciones al asistente sin un beneficio claro.

