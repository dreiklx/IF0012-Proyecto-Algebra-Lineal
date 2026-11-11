# `visualizacion/`: gráficas y notación

Estas funciones solo **dibujan** resultados que ya calculó `algebra/`: no resuelven, no iteran y no ajustan nada. Las pruebas (`tests/interfaz/test_graficas_*.py`) comprueban que cada gráfica dibuja exactamente los datos del núcleo.

| Archivo | Contenido |
|---|---|
| `interactivas.py` | todas las gráficas Plotly de la aplicación (tabla abajo) |
| `datos_graficas.py` | los datos que se dibujan, sin ninguna biblioteca: valores positivos para la escala logarítmica, serie de cada métrica, región y esquinas de los planos |
| `notacion.py` | cada símbolo en tres formas (LaTeX, HTML para Plotly, Unicode para tablas) y la conversión de los textos del núcleo |
| `tema.py` | colores |
| `referencia_matplotlib.py` | figura estática de la convergencia; **no se muestra**: las pruebas la usan como oráculo independiente |

| Gráfica (`interactivas.py`) | Módulo | ¿La exige el enunciado? |
|---|---|---|
| `ajuste` | III | **Sí**: «gráfica con los datos y la recta de mejor ajuste» |
| `convergencia` | IV | **Sí**: «gráfica error vs. iteración» |
| `comparacion` | IV | **Sí**: «… para facilitar la comparación» |
| `rectas_2d`, `planos_3d` | I | No: interpretación geométrica, incentivo de experiencia de usuario |
| `autovalores` | IV | No: extensión matemática (ρ(T) en el plano complejo) |
| `precondicionador` | IV | No: incentivo de precondicionamiento |

Detalle de la matriz de cumplimiento: [docs/cumplimiento_graficas.md](../docs/cumplimiento_graficas.md).
