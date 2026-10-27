# Proyecto IF0012 — Álgebra Lineal

Aplicación integrada para el proyecto final de IF0012 (II Ciclo 2026). Está en desarrollo.

## Estructura actual

| Ruta | Contenido |
|---|---|
| `algebra/` | Núcleo matemático, escrito en Python puro con la biblioteca estándar y sin NumPy. |
| `algebra/matriz.py` | Validación de matrices y vectores, transpuesta, suma, resta, producto, matriz por vector, norma infinito y residuo. |
| `tests/` | Pruebas automáticas con `unittest`. |

Las carpetas `casos_prueba/` y `docs/` y el archivo `app.py` (la interfaz) se crearán en las fases siguientes.

## Requisitos

Python 3.11 o superior. Se probó con 3.13.0 y 3.14.1. No hay dependencias externas.

## Ejecutar las pruebas

Desde esta carpeta:

```
python -m unittest -v
```

## Convenciones del núcleo

- Una matriz es una lista de filas (`[[1, 2], [3, 4]]`). Un vector es una lista plana (`[1, 2]`).
- Se aceptan números `int`, `float` y `fractions.Fraction`. Con enteros y fracciones los resultados son exactos.
- Las funciones nunca modifican sus argumentos.
- Los errores de entrada lanzan `ErrorMatriz`. Los de tamaño lanzan `ErrorDimension`, que es una subclase de `ErrorMatriz`. Ambos llevan un mensaje en español.
