# Registro de correcciones (12-nov-2026)

## Cambios en Ax desde esta auditoría

| Commit | Archivo | Cambio | Motivo |
|---|---|---|---|
| f1bcf21 | `interfaz/modulos/modulo_IV_iterativos/principal.py` | Nota bajo el selector de criterio A y procedencia corregida | Diferencia D4 |
| (este registro) | `docs/auditoria/*` | Inventario, comparaciones y discrepancias | Auditoría visual parcial |

## Cambios de código por la auditoría visual de S9-07/10

**Ninguno.** Las comparaciones de S9-07/10 (Jacobi, Gauss-Seidel, radio espectral, T_GS, c_GS) coinciden con Ax, excepto en las erratas de la lámina (D1, D2, D3), que Ax no reproduce.

## Pruebas ejecutadas

- Suite completa: 314 pruebas (ver el informe de la sesión).
- Auditorías matemáticas: `auditoria/auditoria_directos.py`, `auditoria_iterativos.py`, `auditoria_precondicionamiento.py`, `casos_dificiles.py`: 0 fallos.
