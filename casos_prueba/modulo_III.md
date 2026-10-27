# Casos de prueba — Módulo III: mínimos cuadrados y ajuste lineal

Los oráculos se calcularon a mano. Las ecuaciones normales 2×2 se resolvieron por la regla de Cramer, que es un método distinto del Gauss que usa la aplicación. La recta se obtuvo con la fórmula cerrada m = (nΣxy − ΣxΣy)/(nΣx² − (Σx)²).

También se verifica una propiedad independiente: **Aᵀr = 0**.

- **Resultado obtenido:** ejecución de `algebra/minimos.py` el 27-oct-2026.
- **Pruebas automáticas:** `tests/test_minimos.py`.

| ID | Entrada | Salida esperada (oráculo) | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| III-1 | x+3y = −1, 3x−2y = 8, −2x+5y = −8 (S8-30/09 pp. 6-7) | AᵀA = [[14, −13], [−13, 38]], Aᵀb = (39, −59); Cramer: x̂ = (65/33, −29/33); r = (−1/3, 1/3, 1/3); ‖r‖₂² = 1/3 | Sobredeterminado; x̂ = (65/33, −29/33); r = (−1/3, 1/3, 1/3); ‖r‖₂ = 0.5773502692; Aᵀr = (0, 0) | Sí |
| III-2 | x+y = 2, 2x+y = 2, x+2y = 3 (Tarea II #1) | AᵀA = [[6, 5], [5, 6]], Aᵀb = (9, 10); x̂ = (4/11, 15/11) (igual que la solución del ZIP); r = (3/11, −1/11, −1/11); ‖r‖₂² = 1/11 | x̂ = (4/11, 15/11); r = (3/11, −1/11, −1/11); ‖r‖₂ = 0.3015113446; Aᵀr = (0, 0) | Sí |
| III-3 | Puntos (1, 2), (2, 2.5), (3, 3.7), (4, 4.1) (S8-30/09 p. 8) | Σx = 10, Σx² = 30, Σy = 12.3, Σxy = 34.5 → m = 15/20 = 3/4, c = 4.8/4 = 6/5. Residuos (0.05, −0.2, 0.25, −0.1); ‖r‖₂² = 0.115 | y = 3/4 x + 6/5; r = (1/20, −1/5, 1/4, −1/10); ‖r‖₂² = 23/200 | Sí |
| III-4 | A = `1 2 / 2 4 / 3 6`, b = (1, 2, 4) | Columnas dependientes → AᵀA singular → no hay x̂ único; debe advertirse | No devuelve x̂; mensaje «AᵀA es singular: las columnas de A son linealmente dependientes…» | Sí |
| III-5 | Puntos con todos los x iguales, (2, 1), (2, 2), (2, 3) | No existe una recta y = mx + c; mensaje de error claro | ErrorAjuste: «Todos los valores de x son iguales…» | Sí |
