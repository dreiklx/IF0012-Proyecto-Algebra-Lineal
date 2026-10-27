# Casos de prueba — Módulo I: sistemas lineales y métodos directos

Requisito: «cada módulo debe incluir al menos un caso de prueba documentado con entrada, salida esperada y resultado obtenido» (OFICIAL p. 3).

- **Salida esperada:** calculada de forma independiente, a mano, por sustitución en las ecuaciones originales.
- **Resultado obtenido:** lo que devolvió la aplicación (`algebra/directos.py`) al ejecutarse el 27-oct-2026.
- **Pruebas automáticas equivalentes:** `tests/test_directos.py`.

| ID | Entrada (A ; b) | Salida esperada (oráculo independiente) | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| I-1 | `1 1 1 / 2 1 -1 / -1 1 2` ; `6 3 7` (S6-16/09 p. 29) | Única: (1/3, 4, 5/3). Comprobación: 1/3+4+5/3 = 6; 2/3+4−5/3 = 3; −1/3+4+10/3 = 7. det = 3 | ÚNICA, rango 3/3, det 3, x = (1/3, 4, 5/3) | Sí |
| I-2 | `2 1 -1 / 1 -3 2 / 3 2 1` ; `1 4 0` (S6-14/09 p. 29) | Única: (19/20, −5/4, −7/20); det = −20. **La lámina da (1/2, −1, −1), que no satisface la 2.ª ecuación** | ÚNICA, det −20, x = (19/20, −5/4, −7/20) | Sí |
| I-3 | `0 1 1 / 1 1 1 / 1 2 3` ; `2 3 6` (pivote nulo) | Única: (1, 1, 1) (2, 3, 6 ✓); det = −1; requiere F1 ↔ F2 | ÚNICA, det −1, x = (1, 1, 1); paso «F1 ↔ F2 (el elemento (1, 1) es 0)» | Sí |
| I-4 | `1 1 1 / 2 2 2 / 1 -1 0` ; `1 2 0` | Infinitas: la ecuación 2 es el doble de la 1; rango 2 < 3; una variable libre | INFINITAS, rango(A) = rango([A\|b]) = 2; x = (1/2, 1/2, 0) + t(−1/2, −1/2, 1). Comprobado: A·xₚ = b y A·v = 0 | Sí |
| I-5 | `1 1 1 / 1 1 1 / 1 -1 2` ; `1 2 0` | Inconsistente: mismas incógnitas igualadas a 1 y a 2 (0 = 1) | INCONSISTENTE, rango(A) = 2 < rango([A\|b]) = 3 | Sí |
| I-6 | Inversa de `1 2 3 / 2 -1 -1 / 3 0 -1` (S3-24/08 p. 8) | [[1/8, 1/4, 1/8], [−1/8, −5/4, 7/8], [3/8, 3/4, −5/8]], con A·A⁻¹ = I. det = 8. **El manuscrito tiene un error en la 1.ª columna** | Misma matriz; verificación A·A⁻¹ = I exacta; det 8 | Sí |
| I-7 | Entrada `1 2 / 3 x` | Mensaje de error que indique la celda (2, 2), sin cerrar la aplicación | «El elemento (2, 2) de la matriz A "x" no es un número válido…» (prueba `test_app.test_modulo_I_entrada_invalida`) | Sí |

En la aplicación, los casos I-1 a I-5 están precargados en el selector «Cargar un ejemplo» del Módulo I.
