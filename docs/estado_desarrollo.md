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
| VIII · Visualización 3D | Matplotlib: hecho e integrado. PyVista: prototipo aislado probado (render fuera de pantalla), exportación HTML parcial, no integrado | `visualizacion/geometria_3d.py`; `docs/herramientas_y_bibliotecas.md` §5 |
| IX · Pruebas integrales | Hecho | 176 pruebas, 0 fallos |
| X · Documentación | Hecho | `docs/`, `casos_prueba/`, `README.md` |
| XI · Matriz de cumplimiento | Hecho | `docs/auditoria_requisitos.md` |
| Incentivo I-03 · Matrices dispersas (CSR) | Probado | `algebra/dispersas.py`, `tests/test_dispersas.py` |
| XII · Empaquetado | Hecho | `empaquetar.py`, `ejecutar.bat`; ver la prueba de instalación abajo |

## Últimas pruebas

```
.venv\Scripts\python -m unittest
Ran 176 tests ... OK
```

## Prueba de instalación aislada (27-oct-2026)

**Procedimiento:**

1. Se generó el ZIP con `empaquetar.py 01`.
2. Se extrajo en una carpeta temporal nueva, sin `.venv`.
3. Se ejecutó el propio `ejecutar.bat` de esa copia, con `IF0012_SIN_NAVEGADOR=1` para no abrir el navegador.

**Resultado:**

- `ejecutar.bat` creó `.venv` con `py -3` (que en este equipo es **Python 3.14.1**) e instaló `requirements.txt` desde internet: «Successfully installed … matplotlib-3.11.2 … streamlit-1.66.1».
- Arrancó el servidor, que respondió `ok` en `/_stcore/health` a los 62 s.
- En esa copia, `python -m unittest` dio **167 pruebas OK**. El ZIP de esa prueba se generó antes de añadir el formato CSR; el ZIP final se volvió a probar:
- **ZIP final** (53 archivos, con CSR): extraído en otra carpeta nueva, venv creado desde cero con Python 3.13.0 y `pip install -r requirements.txt` → `python -m unittest` dio **176 pruebas OK**.

**Limitación honesta:** se probó en un entorno virtual nuevo **en este mismo equipo**, no en otro computador ni en un Windows sin Python previo.

**Lecciones aplicadas:**

- Sin `headless = true`, Streamlit pide un correo en el primer arranque y la consola se queda esperando. Por eso está en `.streamlit/config.toml`.
- `ejecutar.bat` abre el navegador unos segundos después de arrancar el servidor.

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
2. PyVista: decidir si vale la pena incrustar el HTML exportado (ver herramientas_y_bibliotecas.md §5).
