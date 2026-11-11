# `tests/`: pruebas automáticas

Ejecutar todas, desde la raíz del proyecto:

```text
ejecutar_pruebas.bat
python -m unittest discover -s tests -t .
```

| Carpeta | Qué comprueba | Oráculo (de dónde sale el valor esperado) |
|---|---|---|
| `compartido/` | `matriz.py`, `validacion.py` | valores calculados a mano y ejemplos de las láminas |
| `modulo_I/` | Gauss, Gauss-Jordan, pivoteo, clasificación, inversa, notación «−2F₁ + F₂» | soluciones de los manuscritos, verificadas con fracciones |
| `modulo_II/` | κ∞, escala, perturbación, cota | ejemplos de S7-21/09 (κ∞ = 16/5) |
| `modulo_III/` | ecuaciones normales, Cramer, ajuste, Aᵀr = 0 | manuscrito S8-30/09 pp. 6-7: x̂ = (65/33, −29/33) |
| `modulo_IV/` | métodos, criterios, T y c, ρ(T), dispersas, precondicionador | manuscritos S9-07/10, Tarea II, iteraciones independientes |
| `gestos/` | gestos, cámara orbital, hilo y perro guardián | manos sintéticas (sin cámara) |
| `interfaz/` | la aplicación completa con AppTest; editor; gráficas con los datos del núcleo; notación | el núcleo y una figura independiente de Matplotlib |
| `entrega/` | el ZIP no incluye archivos internos ni credenciales | lista de exclusiones |

Regla del proyecto: **nunca se cambia un valor esperado para que una prueba pase.** Las erratas de las láminas no se usan como resultado esperado (ver `docs/referencia_oficial_procedimientos.md` §9).

La auditoría con miles de casos aleatorios está aparte, en `auditoria/`, porque tarda más.
