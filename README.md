# Proyecto IF0012 — Álgebra Lineal Numérica

Aplicación web local e integrada para el proyecto final de **IF0012 Álgebra Lineal para Informática Empresarial** (Universidad de Costa Rica, II Ciclo 2026). Sirve para modelar, resolver y analizar problemas de álgebra lineal y análisis numérico. Todos los algoritmos centrales se implementaron **desde cero** en Python.

## Funcionalidades

| Módulo | Contenido |
|---|---|
| **I · Sistemas lineales** | Gauss y Gauss-Jordan con el procedimiento paso a paso; clasificación (única, infinitas o inconsistente) por rangos; solución paramétrica; determinante; interpretación geométrica en 2D y 3D |
| **II · Condicionamiento** | Inversa por Gauss-Jordan (verificando A·A⁻¹ = I); κ∞(A) con la escala del proyecto; perturbación de b por valor absoluto o porcentaje; errores relativos; cota teórica |
| **III · Mínimos cuadrados** | Detección de sistema sobredeterminado; ecuaciones normales AᵀAx̂ = Aᵀb; residuo; ‖r‖₂; ajuste lineal y = mx + c con gráfica |
| **IV · Métodos iterativos** | Jacobi, Gauss-Seidel y SOR con criterio de parada configurable (A: cambio entre iteraciones, B: residuo, C: N fijas); tabla y gráficas; exportación a CSV; comparación homogénea; dominancia diagonal; matrices de iteración, polinomio característico, autovalores y radio espectral |

El núcleo matemático (`algebra/`) usa solo la biblioteca estándar de Python y trabaja con fracciones exactas en los métodos directos. Streamlit y Matplotlib se usan solo para la interfaz y las gráficas.

## Instalación y ejecución (Windows)

Requisito: **Python 3.11 o superior**.

1. Haga doble clic en **`ejecutar.bat`**. La primera vez crea `.venv` e instala `requirements.txt`, para lo que necesita internet.
2. Se abre `http://localhost:8501` en el navegador.

Instalación manual:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

## Pruebas

```
.venv\Scripts\python -m unittest -v
```

También puede usar `ejecutar_pruebas.bat`. Hay 167 pruebas: el núcleo matemático, la validación y la interfaz (esta última con `streamlit.testing`).

## Documentación

| Documento | Contenido |
|---|---|
| [docs/manual_usuario.md](docs/manual_usuario.md) | Manual de usuario: entradas, pasos y un ejemplo por módulo |
| [docs/guia_matematica.md](docs/guia_matematica.md) | Fórmulas, procedimientos, casos especiales y ejemplos verificados |
| [docs/guia_defensa.md](docs/guia_defensa.md) | Guía de estudio para la defensa individual |
| [docs/arquitectura.md](docs/arquitectura.md) | Estructura del código |
| [docs/decisiones_tecnicas.md](docs/decisiones_tecnicas.md) | Decisiones y alternativas descartadas |
| [docs/herramientas_y_bibliotecas.md](docs/herramientas_y_bibliotecas.md) | Dependencias y declaración de uso de IA |
| [docs/auditoria_requisitos.md](docs/auditoria_requisitos.md) | Matriz de cumplimiento de la rúbrica |
| [docs/estado_desarrollo.md](docs/estado_desarrollo.md) | Estado actual, pendientes y bloqueos |
| [casos_prueba/](casos_prueba/README.md) | Casos documentados por módulo |

## Archivo de entrega

```
.venv\Scripts\python empaquetar.py 01
```

Genera `dist/Grupo01-IF0012-Proyecto-IIC.zip`; use `02` si corresponde a ese grupo.
