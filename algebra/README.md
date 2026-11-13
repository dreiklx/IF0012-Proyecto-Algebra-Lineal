# `algebra/`: núcleo matemático

Todos los cálculos de Ax están aquí, implementados desde cero en Python puro. No se usan NumPy, SciPy ni ninguna biblioteca de álgebra; solo `fractions`, `math` y `cmath` de la biblioteca estándar. Nada en esta carpeta importa Streamlit ni las gráficas, así que todo se puede probar por separado.

| Carpeta | Archivo | Qué hace | Categoría |
|---|---|---|---|
| `compartido/` | `matriz.py` | validar dimensiones; suma, producto, transpuesta; normas ∞ y 2 (`sumas_absolutas_por_fila` da las sumas de clase); residuo b − Ax | base |
| | `validacion.py` | convertir el texto del usuario en números (`leer_matriz`, `leer_tolerancia`, `leer_omega`…) con mensajes claros (`ErrorEntrada`); `formatear_numero` | base |
| | `exactos.py` | `a_fraccion`: trabajar con fracciones exactas | base |
| `modulo_I_sistemas/` | `directos.py` | Gauss, Gauss-Jordan, pivoteo, clasificación por rangos, inversa [A \| I] → [I \| A⁻¹], determinante | A |
| `modulo_II_condicionamiento/` | `condicion.py` | κ∞(A) = ‖A‖∞‖A⁻¹‖∞, escala 10/100 del enunciado, perturbación de b | A y B |
| `modulo_III_minimos/` | `minimos.py` | ecuaciones normales AᵀAx̂ = Aᵀb resueltas con Gauss, residuo, ‖r‖₂, Cramer de verificación, recta y = mx + c | A y B |
| `modulo_IV_iterativos/` | `metodos.py` | **una** iteración de Jacobi, Gauss-Seidel y SOR | A |
| | `ejecucion.py` | el bucle común: criterios A, B y C, tabla k, x⁽ᵏ⁾, dₖ, rₖ y motivo de parada | A y B |
| | `convergencia.py` | dominancia diagonal estricta y reordenamiento de ecuaciones | A |
| | `matriz_iteracion.py` | A = D + L + U, D⁻¹ o (D+L)⁻¹, T y c; desarrollo por Sarrus | A (T de SOR: C) |
| | `polinomio_raices.py` | det(λI − T) por Faddeev-LeVerrier y raíces por Durand-Kerner | **C, extensión** |
| | `espectral.py` | ρ(T) = máx\|λ\| y la conclusión «converge si y solo si ρ(T) < 1» | A |
| | `comparacion.py` | los tres métodos con la misma configuración; error final ‖x⁽ᵏ⁾ − x*‖∞ | B |
| | `dispersas.py` | formato CSR y pasos que recorren solo los no nulos | incentivo |
| | `precondicionamiento.py` | M = D, comparación de κ, autovalores e iteraciones | incentivo |

Categorías: **A** = visto en clase; **B** = exigido por el enunciado; **C** = extensión no vista en clase.

**Dependencias.** `compartido/` no depende de nada. Los módulos II, III y IV reutilizan el Módulo I, como pide el enunciado: la inversa del Módulo II, las ecuaciones normales del III y la solución de referencia del IV.

**Resultados.** Cada función principal devuelve una `dataclass` (`ResultadoSistema`, `ResultadoCondicion`, `ResultadoMinimos`, `ResultadoIterativo`, `ResultadoEspectral`…) con los valores y los mensajes. La interfaz solo los muestra.

Recorrido completo de cada módulo: [docs/mapa_completo_del_codigo.md](../docs/mapa_completo_del_codigo.md).
