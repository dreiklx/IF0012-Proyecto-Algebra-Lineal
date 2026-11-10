# Casos de prueba — Módulo II: condicionamiento y sensibilidad

κ∞(A) = ‖A‖∞·‖A⁻¹‖∞. Los oráculos se obtuvieron a mano: con la fórmula de la inversa 2×2, A⁻¹ = (1/det)[[d, −b], [−c, a]], o con la estructura A = I + 10J, cuya inversa es (I + 10J)⁻¹ = I − (10/31)J.

- **Resultado obtenido:** ejecución de `algebra/modulo_II_condicionamiento/condicion.py` el 27-oct-2026.
- **Pruebas automáticas:** `tests/modulo_II/test_condicion.py`.

| ID | Entrada | Salida esperada (oráculo) | Resultado obtenido | ¿Coincide? |
|---|---|---|---|---|
| II-1 | A = `4 1 / 1 3`, b = (1, 2), Δb = (0.01, −0.01) (S7-21/09 p. 20) | ‖A‖ = 5, ‖A⁻¹‖ = 5/11, κ = 25/11 (baja). x = (1/11, 7/11); x̃ = (26/275, 139/220) ≈ (0.0945, 0.6318). ‖Δb‖/‖b‖ = 1/200; ‖Δx‖/‖x‖ = 1/140 ≤ κ/200. **La lámina da 0.6309 (error aritmético)** | κ = 25/11 BAJA; x̃ = (26/275, 139/220); 1/200; 1/140; amplificación 10/7; la cota se cumple | Sí |
| II-2 | A = I + 10J (3×3), b = (31, 31, 31), Δb = (1, −1, 1) (S8-28/09 p. 13) | κ∞ = 31·41/31 = **41** (moderada; κ₂ = 31 en clase). x = (1, 1, 1); x̃ = (52/31, −10/31, 52/31). La amplificación es 41 = κ: es el caso peor | κ = 41 MODERADA; x̃ = (52/31, −10/31, 52/31); amplificación 41; la cota se cumple | Sí |
| II-3 | A = `1 1 / 1 1.0001`, b = (2, 2.0001), Δb = (0, 0.0001) (S7-21/09 p. 15) | κ = 2.0001 · 20001 = 40004.0001 (alta). x = (1, 1); x̃ = (0, 2) | κ = 400040001/10000 ALTA; x̃ = (0, 2); amplificación 20001 ≤ κ | Sí |
| II-4 | A = `1 2 / 2 4` | Singular: no existe A⁻¹ y κ no está definido. Debe distinguirse de «κ grande» | SINGULAR, mensaje «A es singular (det(A) = 0)…» | Sí |
| II-5 | b = (31, 31, 31) con perturbación del 10 % | Δb = (3.1, 3.1, 3.1) y x̃ = 1.1·x = (1.1, 1.1, 1.1): el error relativo de x es 10 % | x̃ = (11/10, 11/10, 11/10); amplificación 1 | Sí |
