# Estado del desarrollo

**Última actualización:** 27-oct-2026. El historial completo está en `git log`.

## Resumen

| Etapa | Estado | Evidencia |
|---|---|---|
| Entorno (venv con Python 3.13.0, git local, `.gitignore`) | Hecho | `.venv/`, repositorio git sin remoto |
| I · Operaciones matriciales y validación | Probado | `tests/test_matriz.py`, `tests/test_validacion.py` |
| II · Métodos directos (Gauss, Gauss-Jordan, inversa, det) | Verificado | `tests/test_directos.py`, `casos_prueba/modulo_I.md` |
| III · Condicionamiento y perturbaciones | Verificado | `tests/test_condicion.py`, `casos_prueba/modulo_II.md` |
| IV · Mínimos cuadrados y ajuste | Verificado | `tests/test_minimos.py`, `casos_prueba/modulo_III.md` |
| V · Iterativos con criterios A/B/C | Verificado | `tests/test_iterativos.py` (P1–P21), `casos_prueba/modulo_IV.md` |
| VI · Radio espectral | Verificado | `tests/test_espectral.py` |
| VII · Interfaz web Streamlit | Probado | `tests/test_app.py` (AppTest); servidor real en localhost:8501; revisión visual de los módulos I y IV en Chrome |
| VIII · Visualización 3D | Matplotlib: hecho. PyVista: evaluado, no incluido | `visualizacion/geometria_3d.py`; `docs/herramientas_y_bibliotecas.md` §5 |
| IX · Pruebas integrales | Hecho | 167 pruebas, 0 fallos |
| X · Documentación | Hecho | `docs/`, `casos_prueba/`, `README.md` |
| XI · Matriz de cumplimiento | Hecho | `docs/auditoria_requisitos.md` |
| XII · Empaquetado | Hecho | `empaquetar.py`, `ejecutar.bat`; ver la prueba de instalación abajo |

## Últimas pruebas

```
.venv\Scripts\python -m unittest
Ran 167 tests ... OK
```

## Prueba de instalación aislada

Ver la sección «Resultado de la instalación aislada» más abajo.

## Bloqueos y pendientes que no dependen del código

| # | Pendiente | Impacto | Quién |
|---|---|---|---|
| 1 | **Autorización del uso de IA** (PROG p. 7 §6.2) | Integridad académica | Grupo → docente |
| 2 | Fecha de entrega y defensa: el 11-nov (OFICIAL) o la semana 15 (programa) | Planificación | Grupo → docente |
| 3 | Número de grupo (01 o 02) para el nombre del ZIP | Entregable | Grupo |
| 4 | Caso de validación obligatorio de la docente | C-07 (3 %) | Docente |
| 5 | Si se permite NumPy como dependencia transitiva de Streamlit y Matplotlib | Restricción | Docente |
| 6 | Alcance de ρ(T) (n > 3, autovalores complejos, métodos extra) | M4-05 | Docente |
| 7 | Qué es el «error final» en la comparación | M4-07 | Docente |
| 8 | Qué comparación espera en el precondicionamiento diagonal | I-02 (1.5 %) | Docente |
| 9 | Si se acepta el reordenamiento automático de filas | — | Docente |
| 10 | Probar el manual con una persona ajena al equipo | C-06 | Grupo |
| 11 | Preparar la defensa individual (4 integrantes) | 35 % | Grupo |

## Siguiente paso técnico sugerido

1. Añadir el caso obligatorio cuando llegue (`casos_prueba/README.md`).
2. Incentivo I-03, matrices dispersas: formato CSR propio para Jacobi y GS.
3. PyVista como prototipo aislado, solo si queda tiempo después de lo anterior.
