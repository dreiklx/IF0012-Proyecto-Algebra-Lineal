# Arquitectura

**Versión:** reorganización del 09/10-nov-2026 (rama `refactor/arquitectura-modular`).
**Regla de oro:** la reorganización **solo movió código**. No cambió ninguna fórmula ni ningún resultado.

- **Pruebas:** después de cada etapa pasaron las 232 pruebas.
- **Volcado de comparación:** se volcaron 273 resultados de los ejemplos precargados (todas las variantes de método, criterio, formato y pivoteo) y salieron idénticos byte a byte a los anteriores.

Para un recorrido de estudio, ver [guia_recorrido_codigo.md](guia_recorrido_codigo.md).

## 1. Estructura actual

```text
proyecto-algebra/
├── app.py                          Punto de entrada: barra superior (st.navigation) con 5 páginas
├── paginas/                        Una página por módulo; cada archivo llama a mostrar()
│
├── algebra/                        NÚCLEO MATEMÁTICO — Python puro, sin bibliotecas externas
│   ├── compartido/                 Lo que usan los cuatro módulos (no implementa métodos del curso)
│   │   ├── matriz.py               validación de forma, producto, transpuesta, normas ∞ y 2, residuo
│   │   ├── validacion.py           texto del usuario → Fraction; ε, k_max, ω; mensajes de error
│   │   └── exactos.py              a_fraccion: int/float/Fraction → Fraction exacta
│   ├── modulo_I_sistemas/
│   │   └── directos.py             Gauss, Gauss-Jordan, clasificación, inversa [A|I], determinante
│   ├── modulo_II_condicionamiento/
│   │   └── condicion.py            κ∞, clasificación del enunciado, perturbación, errores relativos
│   ├── modulo_III_minimos/
│   │   └── minimos.py              ecuaciones normales, residuo ‖r‖₂, Cramer de verificación, recta
│   └── modulo_IV_iterativos/
│       ├── metodos.py              fórmulas: un paso de Jacobi, Gauss-Seidel, SOR (y Richardson)
│       ├── ejecucion.py            bucle común: validación, criterios A/B/C, tabla, motivo de parada
│       ├── convergencia.py         dominancia diagonal y reordenamiento de ecuaciones
│       ├── espectral.py            A = D + L + U, T y c, polinomio característico, ρ(T)
│       ├── comparacion.py          los tres métodos con la misma configuración; error final
│       ├── dispersas.py            incentivo: formato CSR y pasos O(nnz)
│       └── precondicionamiento.py  incentivo: M = D y comparación de su efecto
│
├── interfaz/                       PRESENTACIÓN — Streamlit; no hace cálculos
│   ├── navegacion.py               lista de páginas (archivo, título, URL)
│   ├── portada.py                  portada: módulos, incentivos, figura [A|b] → [I|x]
│   ├── recursos/marca.svg          marca «Ax»
│   ├── compartido/
│   │   ├── estilo.py               sistema de diseño: tokens, tipografía, componentes, animaciones
│   │   ├── componentes.py          lectura con mensajes de error, LaTeX, gráficas Plotly
│   │   ├── editor.py               editor interactivo de matrices, vectores y puntos
│   │   └── ejemplos.py             ejemplos precargados del curso
│   └── modulos/
│       ├── modulo_I_sistemas.py
│       ├── modulo_II_condicionamiento.py
│       ├── modulo_III_minimos.py
│       └── modulo_IV_iterativos/   una vista por pestaña
│           ├── principal.py        mostrar(): sistema, parámetros comunes, pestañas
│           ├── pestana_ejecutar.py
│           ├── pestana_comparar.py
│           ├── pestana_convergencia.py
│           └── pestana_precondicionamiento.py
│
├── visualizacion/                  GRÁFICAS — solo dibujan resultados ya calculados
│   ├── tema.py                     colores y estilo común
│   ├── interactivas.py             gráficas Plotly que muestra la interfaz (2D y 3D)
│   ├── graficos.py                 versión Matplotlib (respaldo y pruebas)
│   └── geometria_3d.py             geometría de rectas y planos para dibujar el Módulo I
│
├── gestos/                         CONTROL GESTUAL de la gráfica 3D (10-nov; no es parte del núcleo)
│   ├── mano.py                     21 puntos de MediaPipe, conexiones, tamaño de la palma
│   ├── interpretacion.py           reglas de gestos, antirrebote, histéresis, calibración
│   ├── movimiento.py               suavizado y cámara orbital (θ, φ, r) con límites
│   ├── captura.py                  cámara web con OpenCV (DirectShow), en memoria
│   ├── deteccion.py                MediaPipe Tasks Hand Landmarker (modo VIDEO)
│   ├── control.py                  hilo de visión, estado con candado, perro guardián
│   ├── servidor.py                 canal 127.0.0.1 (SSE) que lleva la cámara a la gráfica
│   └── modelos/hand_landmarker.task  modelo de MediaPipe (Apache-2.0)
│
├── tests/                          269 pruebas (unittest), una carpeta por módulo
│   ├── compartido/  modulo_I/  modulo_II/  modulo_III/  modulo_IV/
│   ├── interfaz/                   la aplicación completa con streamlit.testing (AppTest)
│   ├── entrega/                    el ZIP no filtra archivos internos; .gitignore protege credenciales
│   └── rutas.py                    raíz del proyecto para las pruebas
├── auditoria/                      oráculos independientes y casos difíciles
├── casos_prueba/                   casos documentados: entrada, esperado, obtenido
├── docs/                           documentación
├── herramientas/                   solo desarrollo (generar la guía HTML)
├── dist/                           entrega estable: ZIP, SHA256.txt y guía HTML
├── requirements.txt / ejecutar.bat / ejecutar_pruebas.bat / empaquetar.py
```

## 2. Estructura anterior y qué cambió

| Antes | Ahora | Motivo |
|---|---|---|
| `algebra/matriz.py`, `algebra/validacion.py` | `algebra/compartido/` | Las usan los cuatro módulos y la interfaz |
| `a_fraccion` dentro de `directos.py` | `algebra/compartido/exactos.py` | La usan los módulos I, II, III y IV; no es parte de Gauss |
| `algebra/directos.py`, `condicion.py`, `minimos.py` | `algebra/modulo_I_sistemas/`, `modulo_II_condicionamiento/`, `modulo_III_minimos/` | Una carpeta por módulo del enunciado |
| `algebra/iterativos.py` (566 líneas, 5 responsabilidades) | `metodos.py`, `ejecucion.py`, `convergencia.py`, `comparacion.py` | Cada procedimiento tiene un archivo reconocible: fórmulas, bucle, criterio de convergencia, comparación |
| `paso_richardson_csr` en `iterativos.py` | `dispersas.py` | Junto a los demás pasos CSR |
| `algebra/espectral.py`, `dispersas.py`, `precondicionamiento.py` | `algebra/modulo_IV_iterativos/` | Son del Módulo IV y de sus incentivos |
| `interfaz/estilo.py`, `componentes.py`, `editor.py`, `ejemplos.py` | `interfaz/compartido/` | Piezas comunes a las cuatro vistas |
| `interfaz/modulo_*.py` | `interfaz/modulos/` | Una vista por módulo |
| `interfaz/modulo_iterativos.py` (577 líneas, 4 pestañas) | `interfaz/modulos/modulo_IV_iterativos/` | Una vista por pestaña; la pestaña 1 pasó de código dentro de `mostrar()` a `ejecutar_un_metodo()` |
| `tests/test_*.py` (13 archivos juntos) | `tests/<módulo>/` | Se encuentra la prueba de cada procedimiento junto a su módulo |

**Detalles de la reorganización:**

- **Sin capas de compatibilidad:** no se dejaron «adaptadores» con rutas viejas. Todas las importaciones se reescribieron con una herramienta basada en el AST de Python, para que no quedaran dos caminos al mismo código.
- **Único cambio de nombre:** `_norma_inf` pasó a llamarse `norma_inf`, con el mismo cuerpo, porque ahora la usan dos archivos.

### Lo que no se movió, y por qué

| Elemento | Decisión |
|---|---|
| `visualizacion/` | Se mantiene plana. Son 4 archivos con una responsabilidad clara cada uno. Separarlos en `graficas_2d/` y `graficas_3d/` partiría `interactivas.py`, que dibuja ambas, sin ganar claridad |
| `auditoria/` | Plana. Son 4 guiones independientes que se ejecutan por separado |
| `directos.py` | No se dividió. Gauss, Gauss-Jordan, la inversa y el determinante comparten `_escalonar`. Dividirlo obligaría a importar funciones privadas entre archivos |
| `espectral.py` (440 líneas) | No se dividió. Todo su contenido sirve a ρ(T): T, polinomio, raíces y conclusión |
| `interfaz/compartido/editor.py`, función `identidad` | No duplica a `algebra/compartido/matriz.identidad`: es una plantilla de texto ("1"/"0") para el editor |

## 3. Reglas de dependencia

```text
            paginas/
               │
               ▼
   interfaz/modulos/ ──► interfaz/compartido/
          │      │
          │      └──────────► visualizacion/   (recibe resultados ya calculados)
          ▼
   algebra/modulo_IV ──► algebra/modulo_I (inversa, Gauss, x* exacta)
   algebra/modulo_III ─► algebra/modulo_I (Gauss para las ecuaciones normales)
   algebra/modulo_II ──► algebra/modulo_I (inversa por Gauss-Jordan)
          │
          ▼
   algebra/compartido/   (matriz, validacion, exactos)
```

- `algebra/` no importa nada de `interfaz/` ni de `visualizacion/`, ni bibliotecas externas.
- `gestos/` no importa `algebra/` ni `interfaz/`. Solo `interfaz/compartido/control_gestual.py` lo usa. El hilo de visión nunca llama a `st.*`. Detalle: `investigacion_mediapipe.md` y `portabilidad_java_python.md`.
- **El Módulo I es la base:** los módulos II, III y IV reutilizan su Gauss-Jordan y su Gauss, como pide el enunciado: «la inversa … con un algoritmo implementado por el grupo» y las ecuaciones normales «con un método directo ya implementado».
- **No hay ciclos de importación.** Lo verificaron Graphify y un análisis AST propio.

## 4. Flujo de datos (igual en los cuatro módulos)

```text
ENTRADA (editor, texto)  →  VALIDACIÓN  →  PROCEDIMIENTO  →  RESULTADO (dataclass)  →  VISUALIZACIÓN
interfaz/compartido/       algebra/          algebra/           ResultadoSistema,         interfaz/modulos/…
editor.py                  compartido/       modulo_X/…         ResultadoIterativo, …     visualizacion/
                           validacion.py
```

Ejemplo del Módulo IV, pestaña «Ejecutar un método»:

1. `principal.mostrar()` dibuja el editor. `leer_todo()` convierte el texto con `validacion.leer_*`, o muestra el error exacto.
2. `pestana_ejecutar.ejecutar_un_metodo()` arma una `ConfiguracionIterativa` y llama a `ejecucion.ejecutar(A, b, config)`.
3. `ejecutar` valida y repite `metodos.paso_<método>` hasta cumplir el criterio. Devuelve un `ResultadoIterativo` y **nunca lanza excepciones**: los problemas vuelven como códigos de terminación.
4. `mostrar_ejecucion` muestra la tabla y el motivo, ofrece el CSV y pasa el historial a `visualizacion.interactivas.convergencia`.

## 5. Herramienta de mapa del código: Graphify

`graphify update .` construye un grafo del código en `graphify-out/`:

- extracción AST local, sin LLM y sin costo;
- `.graphifyignore` excluye documentación, PDF e imágenes;
- se usó para ubicar funciones centrales («nodos dios»: `ejecutar`, `ErrorEntrada`, `formatear_numero`, `ConfiguracionIterativa`, `a_fraccion`), comunidades y ciclos (ninguno), y para analizar el impacto de cada etapa;
- `graphify-out/` y `.graphifyignore` son locales: están en `.gitignore` y no entran al ZIP.
