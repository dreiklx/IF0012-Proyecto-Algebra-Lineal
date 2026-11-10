# Proyecto IF0012 — Álgebra Lineal Numérica

Proyecto final de **IF0012 Álgebra Lineal para Informática Empresarial**, Universidad de Costa Rica, Sede del Caribe (Aula de Siquirres), II Ciclo 2026.

**Grupo 01.** Integrantes:

- Elmer López Hernández
- Derek Farley Noguera
- Daniel Córdoba Arias
- Samir Sandoval Ramírez

**Entrega:** 11 de noviembre de 2026, con el archivo `Grupo01-IF0012-Proyecto-IIC.zip`. **Defensa individual:** semana del 16 de noviembre de 2026.

## Qué es

Una aplicación web local e integrada (Streamlit) para modelar, resolver y analizar problemas de álgebra lineal y análisis numérico.

- **Algoritmos centrales:** todos están implementados **desde cero** en Python (carpeta `algebra/`), solo con la biblioteca estándar. Ningún archivo del proyecto importa NumPy, SciPy ni SymPy.
- **Aritmética:** los métodos directos usan fracciones exactas; los iterativos, punto flotante.
- **Bibliotecas externas:** Streamlit (interfaz), Plotly y Matplotlib (gráficas), MediaPipe y OpenCV (control gestual opcional de la gráfica 3D); ninguna resuelve los métodos del curso.

## Funcionalidades

| Módulo | Contenido |
|---|---|
| **I · Sistemas lineales** | Gauss y Gauss-Jordan paso a paso; clasificación por rangos (única, infinitas o inconsistente); solución paramétrica; determinante; interpretación geométrica en 2D y 3D; control opcional de la vista 3D con gestos de la mano (MediaPipe, en este equipo) |
| **II · Condicionamiento** | Inversa por Gauss-Jordan (verificando A·A⁻¹ = I); κ∞(A) con la escala del proyecto; perturbación absoluta o porcentual de b; errores relativos y cota teórica |
| **III · Mínimos cuadrados** | Detección de sistema sobredeterminado; ecuaciones normales AᵀAx̂ = Aᵀb resueltas con Gauss; residuo y ‖r‖₂; verificación con el procedimiento de clase (det([A\|b]) y Cramer); ajuste lineal con gráfica |
| **IV · Métodos iterativos** | Jacobi, Gauss-Seidel y SOR con criterios de parada A, B y C; tabla, gráficas y exportación CSV; comparación homogénea con error final ‖x⁽ᵏ⁾ − x*‖∞; dominancia diagonal con sugerencia de reordenamiento; matriz de iteración, polinomio característico (con Sarrus en 3×3), autovalores y radio espectral; almacenamiento disperso CSR; precondicionador diagonal M = D |

## Instalación y ejecución (Windows)

Requisito: **Python 3.11 o superior** (python.org, marcando «Add python.exe to PATH»).

- **Forma rápida:** doble clic en **`ejecutar.bat`**. La primera vez crea `.venv` e instala `requirements.txt`, para lo que necesita internet. Luego abre `http://localhost:8501`.
- **Forma manual:**

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

## Pruebas y auditoría

```
.venv\Scripts\python -m unittest
```

También se puede usar `ejecutar_pruebas.bat`. Son **269 pruebas**: el núcleo matemático, la validación, la interfaz (con `streamlit.testing`) y el empaquetado.

Auditoría matemática independiente: compara el núcleo con oráculos escritos aparte, con semilla fija, y tarda unos 20 s. Debe decir «fallos 0».

```
.venv\Scripts\python auditoria\auditoria_directos.py .
.venv\Scripts\python auditoria\auditoria_iterativos.py .
.venv\Scripts\python auditoria\auditoria_precondicionamiento.py .
```

## Organización del código

```
app.py              punto de entrada: navegación entre los 4 módulos
algebra/            núcleo matemático (Python puro)
  compartido/         matriz, validacion, exactos (lo que usan los 4 módulos)
  modulo_I_sistemas/  directos.py            (Gauss, Gauss-Jordan, inversa, determinante)
  modulo_II_condicionamiento/  condicion.py  (κ∞, perturbación)
  modulo_III_minimos/ minimos.py             (ecuaciones normales, residuo, recta)
  modulo_IV_iterativos/  metodos, ejecucion, convergencia, espectral, comparacion,
                      dispersas (CSR), precondicionamiento (M = D)
interfaz/           Streamlit: compartido/ (estilo, editor, componentes, ejemplos) y
                    modulos/ (una vista por módulo); no hace cálculos
visualizacion/      gráficas Plotly y Matplotlib; solo dibujan resultados ya calculados
gestos/             control gestual de la gráfica 3D (cámara, MediaPipe, gestos, cámara orbital);
                    separado del núcleo matemático
tests/              pruebas automáticas (unittest), una carpeta por módulo
auditoria/          comparación aleatoria con oráculos independientes
casos_prueba/       casos documentados por módulo (entrada, esperado, obtenido)
docs/               manual, guías, decisiones, matriz de cumplimiento
dist/               entrega estable: ZIP, su SHA-256 y la guía en HTML
empaquetar.py       genera el ZIP de entrega
```

El detalle está en [docs/arquitectura.md](docs/arquitectura.md); el recorrido de estudio, en [docs/guia_recorrido_codigo.md](docs/guia_recorrido_codigo.md).

## Guía de defensa y documentación

| Documento | Contenido |
|---|---|
| [docs/guia_defensa_equipo.md](docs/guia_defensa_equipo.md) | **Guía de defensa del equipo**: el código real función por función, la matemática, 35 preguntas con respuesta y el guion de demostración |
| [dist/Guia_Defensa_IF0012.html](dist/Guia_Defensa_IF0012.html) | La misma guía, más el resumen, en un HTML autónomo que funciona sin internet. Descárguelo y ábralo en el navegador |
| [docs/resumen_logica_por_modulo.md](docs/resumen_logica_por_modulo.md) | Resumen de estudio rápido por módulo |
| [docs/propuesta_navegacion.md](docs/propuesta_navegacion.md) | Navegación superior y animaciones (implementada) |
| [docs/diseno_visual.md](docs/diseno_visual.md) | Rediseño visual, rúbrica e incentivos en la interfaz, con capturas en `docs/capturas/` |
| [docs/manual_usuario.md](docs/manual_usuario.md) | Manual de usuario: entradas, pasos y un ejemplo por módulo |
| [docs/guia_matematica.md](docs/guia_matematica.md) | Fórmulas, procedimientos y ejemplos verificados |
| [docs/referencia_oficial_procedimientos.md](docs/referencia_oficial_procedimientos.md) | Lo que enseñan los 18 PDF de la docente (457 páginas revisadas), con páginas y erratas |
| [docs/investigacion_richardson.md](docs/investigacion_richardson.md) | Qué es Richardson, por qué está y la clasificación A/B/C/D de todos los procedimientos |
| [docs/guia_recorrido_codigo.md](docs/guia_recorrido_codigo.md) | Recorrido del código para los cuatro integrantes |
| [docs/investigacion_mediapipe.md](docs/investigacion_mediapipe.md) | Investigación (sin implementar) de control gestual de la gráfica 3D |
| [docs/comparacion_procedimientos.md](docs/comparacion_procedimientos.md) | Procedimientos del enunciado, de los PDF de clase y del código, comparados |
| [docs/auditoria_requisitos.md](docs/auditoria_requisitos.md) | Matriz de cumplimiento de la rúbrica normal y de los incentivos |
| [docs/pendientes_docente.md](docs/pendientes_docente.md) | Lo que depende de la docente, con la pregunta exacta para cada caso |
| [docs/decisiones_tecnicas.md](docs/decisiones_tecnicas.md) | Decisiones técnicas y alternativas descartadas |
| [docs/herramientas_y_bibliotecas.md](docs/herramientas_y_bibliotecas.md) | Dependencias y **declaración del uso de herramientas de IA** |
| [docs/estado_desarrollo.md](docs/estado_desarrollo.md) | Estado actual del proyecto |
| [docs/guia_defensa.md](docs/guia_defensa.md) | Guía anterior; incluye la tabla de errores de las láminas |
| [casos_prueba/](casos_prueba/README.md) | Casos de prueba documentados |

## Trabajar con el repositorio (integrantes)

**Repositorio privado:** solo pueden verlo quienes hayan sido invitados.

**Primera vez:**

```
git clone https://github.com/dreiklx/IF0012-Proyecto-Algebra-Lineal.git
cd IF0012-Proyecto-Algebra-Lineal
ejecutar.bat
```

`ejecutar.bat` crea el entorno virtual e instala todo la primera vez. El entorno `.venv` no se sube a GitHub, así que cada persona crea el suyo.

**Para actualizar su copia:** `git pull`.

**Reglas del repositorio:**

- **`main` es la versión estable.** Solo se sube a `main` lo que pasa todas las pruebas y la auditoría.
- **Cambios en curso o no probados:** en una rama aparte, por ejemplo `git switch -c revision-modulo-II`. Se integran a `main` cuando están completos y probados.
- **Antes de subir:** ejecutar `.venv\Scripts\python -m unittest` y la auditoría.
- **Nunca** usar `git push --force` ni reescribir el historial: así se puede recuperar cualquier versión anterior.
- **No subir:**
  - contraseñas, tokens ni archivos `.env`;
  - el entorno `.venv`;
  - archivos personales;
  - archivos internos de asistentes de IA (`CLAUDE.md`, `.claude/`).

  `.gitignore` y `empaquetar.py` ya los excluyen.
- **Si se modifica la guía Markdown:** regenerar también `dist/Guia_Defensa_IF0012.html`, para que tengan el mismo contenido.

## Archivo de entrega

```
.venv\Scripts\python empaquetar.py 01
```

Genera `dist/Grupo01-IF0012-Proyecto-IIC.zip`, con una sola carpeta raíz. Deja fuera los entornos, las cachés, `.git`, las credenciales y los archivos internos de IA, e incluye la declaración de herramientas.
