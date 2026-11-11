# `interfaz/`: lo que ve el usuario (Streamlit)

Aquí no se calcula nada. Cada vista lee los datos, llama al núcleo (`algebra/`) y muestra el resultado.

## Una vista por módulo: `modulos/`

| Archivo | Función de entrada | Qué muestra |
|---|---|---|
| `modulo_I_sistemas.py` | `mostrar()` | editor de A y b, método y pivote, pasos con notación de clase, Sol = {…}, rectas o planos |
| `modulo_II_condicionamiento.py` | `mostrar()` | κ∞, escala, los 5 pasos de clase, inversa paso a paso, perturbación |
| `modulo_III_minimos.py` | `mostrar()` | pestañas «Sistema» y «Ajuste»: ecuaciones normales, residuos, Cramer, gráfica |
| `modulo_IV_iterativos/principal.py` | `mostrar()` | datos y parámetros comunes; cuatro pestañas, cada una en su archivo |
| `modulo_IV_iterativos/pestana_ejecutar.py` | `ejecutar_un_metodo()` | despejes, tabla de iteraciones, CSV, gráfica de convergencia explorable |
| `modulo_IV_iterativos/pestana_comparar.py` | `comparar()` | los 3 métodos, error final, gráfica comparativa, barrido de ω |
| `modulo_IV_iterativos/pestana_convergencia.py` | `convergencia()` | dominancia, pasos ①-⑤ (T_J, C_J), polinomio, autovalores, ρ(T) |
| `modulo_IV_iterativos/pestana_precondicionamiento.py` | `precondicionamiento()` | M = D, κ antes y después, Richardson (extensión) |

`portada.py` es la página de inicio y `navegacion.py` la lista de páginas que usa `app.py`. Los archivos de `paginas/` solo llaman a `mostrar()`: Streamlit necesita un archivo por página.

## Piezas comunes: `compartido/`

| Archivo | Para qué |
|---|---|
| `editor.py` | editor de celdas de matrices, vectores y puntos; avisa de dimensiones incompatibles antes de calcular |
| `componentes.py` | `leer_matriz_ui` y `leer_vector_ui` (leen y muestran el error exacto); `mostrar_pasos`; `mostrar_interactiva` (barra de herramientas y selección de puntos) |
| `formulas.py` | todo el LaTeX: `latex_matriz`, `latex_numero` (fracciones apiladas), `latex_polinomio`, `latex_despejes` |
| `estilo.py` | componentes HTML: encabezado de módulo, chips, procedencia Cat. A/B/C/D, escala de κ |
| `ejemplos.py` | ejemplos precargados del curso |
| `control_gestual.py` y `puente_camara.js` | panel del control con la mano para la gráfica 3D (usa `gestos/`) |

`recursos/` contiene el logo (`marca.svg`) y la hoja de estilos (`estilo.css`).

**Notación.** Los textos que vienen del núcleo pasan por `visualizacion/notacion.md()`, para que «a_11» o «d_7» se vean como a₁₁ y d₇. Ver [docs/notacion_matematica.md](../docs/notacion_matematica.md).
