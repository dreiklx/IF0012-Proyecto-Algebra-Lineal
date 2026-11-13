# Instalación limpia y verificación de la entrega

Verificado el 12-nov-2026 con el commit de `main` 223d259 (rama de origen `feature/mediapipe-2d`).

## Procedimiento seguido

1. Clon temporal del repositorio, separado del entorno de trabajo:
   `git clone --branch <rama> <repo> <temporal>\repo`
2. Entorno virtual nuevo con Python 3.13 (`laragon\bin\python\python-3.13`).
3. Instalación de las dependencias fijadas:
   `python -m pip install -r requirements-bloqueado.txt`
4. Ejecución de la suite completa desde el clon: `python -m unittest`.
5. Extracción del ZIP de entrega en otra carpeta temporal y suite desde allí, con el mismo entorno.

## Resultados

| Verificación | Resultado |
|---|---|
| Instalación desde `requirements-bloqueado.txt` | Correcta (streamlit, mediapipe, opencv y plotly importan) |
| Suite en el clon de `main`/rama | 314 pruebas, 314 aprobadas |
| Suite desde el ZIP extraído | 314 pruebas, 314 aprobadas |

## Lo que esta verificación NO cubre

- No prueba gestos con una mano real: solo pruebas sintéticas (ver `docs/mediapipe_2d.md`).
- No prueba un equipo distinto con otra webcam ni otros navegadores fuera de Brave.
- El caso obligatorio de la docente no está incluido (pendiente externo).

## Uso del entorno de trabajo

El entorno del desarrollo (`.venv`) no se toca en esta verificación. Los paquetes de desarrollo
(p. ej. `markdown`, de `requirements-desarrollo.txt`) no están en la entrega.
