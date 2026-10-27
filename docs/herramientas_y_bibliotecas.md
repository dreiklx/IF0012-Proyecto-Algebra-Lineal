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

**La autorización de la docente para este uso todavía no está confirmada.** El programa del curso (PROG p. 7, §6.2) sanciona el «uso indebido de herramientas de inteligencia artificial no autorizadas». Antes de entregar, el grupo debe:

1. Consultar a la docente si el uso está autorizado y en qué condiciones.
2. Declarar el uso según lo que ella indique.
3. Asegurarse de que cada integrante comprende y puede explicar y reproducir cada algoritmo. Para eso está `docs/guia_defensa.md`.

## 5. PyVista (evaluado, no incluido)

- **Qué es:** PyVista 0.49.1 (docs.pyvista.org) es una biblioteca de visualización 3D basada en VTK.
- **Integración web:** según su documentación, ahora requiere el paquete independiente `trame-pyvista` (0.2.3 en PyPI, publicado el 24-oct-2026). El componente de Streamlit `stpyvista` es de terceros y arrastra Panel y Bokeh.
- **Decisión:** no se incluyó. No cubre ningún requisito obligatorio, y la misma visualización de planos se resolvió con Matplotlib dentro de Streamlit. Integrarlo añadiría dependencias pesadas y un componente experimental a la aplicación obligatoria.
- **Estado:** no implementado, no probado y no integrado.
