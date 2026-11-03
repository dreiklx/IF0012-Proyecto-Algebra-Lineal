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
| Matplotlib | 3.11.2 | Gráficas: datos y recta de ajuste; d_k y r_k; comparación; autovalores; rectas y planos |
| `csv`, `io` (estándar) | — | Exportar la tabla de iteraciones |

**Dependencias transitivas.** Streamlit y Matplotlib instalan internamente NumPy 2.5.4, pandas 3.1.0, pyarrow y altair; la lista completa está en `requirements-bloqueado.txt`.

- **Nuestro código no importa NumPy ni pandas.**
- Estas bibliotecas las usan Streamlit y Matplotlib por dentro, para dibujar y para mostrar tablas.
- Conviene confirmarlo con la docente, porque la autorización de NumPy está pendiente.

## 3. Herramientas de desarrollo

| Herramienta | Uso |
|---|---|
| `unittest` (estándar) | Pruebas automáticas |
| `streamlit.testing.v1.AppTest` | Pruebas de integración de la interfaz sin navegador |
| Git (local, sin repositorio remoto) | Historial de cambios |

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

- La aplicación obligatoria no depende de PyVista. La interpretación geométrica se hace con Matplotlib (`visualizacion/geometria_3d.py`).
- Posible vía futura, experimental y no probada dentro de la aplicación: incrustar el HTML exportado con `streamlit.components.v1.html`.
- Antes de integrarlo habría que probar la estabilidad en el equipo de la defensa.
