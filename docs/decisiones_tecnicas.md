# Decisiones técnicas

Cada decisión indica su fundamento y las alternativas descartadas. Las que dependen de la docente están marcadas **[Pendiente de confirmar]**.

| # | Decisión | Fundamento | Alternativas descartadas |
|---|---|---|---|
| 1 | Núcleo matemático en **Python puro** (listas y `fractions.Fraction`) | OFICIAL p. 1 prohíbe delegar los métodos en bibliotecas. Además, el uso de NumPy está pendiente de confirmar, y sin él la duda no afecta al núcleo | NumPy como contenedor (pendiente de autorización) |
| 2 | **Aritmética exacta** en Gauss, la inversa, κ, los mínimos cuadrados y T | La clasificación por rangos y la detección de singularidad son exactas; los resultados coinciden con el cálculo a mano | `float` con tolerancias, que podría clasificar mal un sistema casi singular |
| 3 | **Punto flotante** en Jacobi, GS y SOR | Son aproximaciones que se cortan por tolerancia. Con fracciones, los denominadores crecerían sin control | Fracciones en las iteraciones |
| 4 | Los datos se leen como **texto y se convierten a Fraction** | `Fraction("0.1")` es exactamente 1/10; `float` no lo es | `float(texto)` |
| 5 | **Pivote por defecto: primer elemento no nulo**; pivoteo parcial opcional | Reproduce el procedimiento de clase; el pivoteo parcial queda disponible y documentado | Solo pivoteo parcial |
| 6 | Umbral técnico **10⁻¹⁰** para el aviso de pivote pequeño | OFICIAL p. 2 pide detectar pivotes «numéricamente problemáticos»; con aritmética exacta solo se advierte, no se altera el resultado | Rechazar el sistema |
| 7 | Clasificación de κ con la **escala oficial** (10/100) | OFICIAL p. 2 | La escala de 5 niveles de las láminas |
| 8 | **Perturbación porcentual por componente**: Δbᵢ = p/100·bᵢ | Interpretación natural de «perturbación en b por porcentaje» **[Pendiente de confirmar]** | Porcentaje de ‖b‖ |
| 9 | Las ecuaciones normales se resuelven con **nuestro Gauss** | OFICIAL p. 2 exige «un método directo ya implementado». Cramer (usado en clase) se menciona como verificación | Cramer como método principal |
| 10 | **Criterios de parada configurables A, B y C**, con A como predeterminado y norma ∞ | Aclaración de la docente (criterios elegibles por el usuario). El criterio A es el más frecuente en los PDF | Un único criterio fijo |
| 11 | **Desigualdad estricta** (<) | Láminas S8-30/09 pp. 18, 23, 39 | ≤ |
| 12 | Paso de cada método **separado** del bucle común | Evita triplicar la lógica de parada; facilita explicar y probar | Tres funciones completas |
| 13 | `ejecutar` **nunca lanza excepciones** | OFICIAL p. 3: no debe haber cierres inesperados | Excepciones atrapadas en la interfaz |
| 14 | No se afirma divergencia al alcanzar k_max ni al aparecer valores no finitos | Corrección conceptual: alcanzar el máximo no demuestra divergencia | Mensaje «el método diverge» |
| 15 | Comparación con **condiciones homogéneas** por defecto y aviso si no lo son | Comparación justa (OFICIAL p. 2) | — |
| 16 | **e_k** se calcula solo respecto a la solución exacta del método directo | No se confunde con d_k ni con r_k | Usar d_k como «error» |
| 17 | ρ(T) por **polinomio característico exacto (Faddeev-LeVerrier) y Durand-Kerner** | Procedimiento del curso (det(T − λI) = 0) generalizado a n > 3 y a raíces complejas. Son algoritmos propios, documentados como extensión **[Pendiente de confirmar el alcance]** | Método de la potencia, que falla con pares complejos y ±μ; `numpy.roots` está prohibido |
| 18 | Decisión exacta de ρ < 1 para grado ≤ 2 (Schur-Cohn) y de ρ ≥ 1 si p(±1) = 0; banda de indeterminación de 10⁻⁹ (10⁻⁶ con raíces casi repetidas); tolerancia de Durand-Kerner 10⁻¹² (corregida en la auditoría) | Evita conclusiones falsas cuando ρ ≈ 1 | Comparar siempre ρ con 1 en `float` |
| 19 | Límite de **n ≤ 8** para el cálculo de ρ | Prioriza la fiabilidad sobre el tamaño (OFICIAL: «cuando el procedimiento estudiado lo permita») | Sin límite |
| 20 | No hay reordenamiento automático de filas | No está pedido; puede cambiar el procedimiento esperado **[Pendiente de confirmar]**. El usuario puede reordenar a mano | Reordenar en silencio |
| 21 | **Streamlit** como interfaz web local | Formularios, tablas y gráficas con poco código. Se probó con AppTest y con el servidor real | Tkinter; Trame |
| 22 | Planos 3D con **Matplotlib** (`Poly3DCollection`) | Sin dependencias nuevas; funciona dentro de Streamlit | PyVista (ver herramientas_y_bibliotecas.md) |
| 23 | Configuración de Streamlit: `localhost`, `gatherUsageStats = false`, `headless = true` | Privacidad y no exposición en la red. Sin `headless`, el primer arranque se queda esperando un correo y bloquearía `ejecutar.bat` (comprobado) | Configuración por defecto |
| 24 | Las figuras se dibujan **sin NumPy en nuestro código** | `plot_surface` exige arreglos de NumPy (error comprobado en Matplotlib 3.11); se usaron polígonos con listas | Importar NumPy en la visualización |
| 25 | **Precondicionador diagonal implementado** (03-nov) con la comparación de la lámina S9-05/10 p. 21: κ(B) frente a κ(A), autovalores, y las iteraciones de Jacobi, GS, SOR y Richardson en ambos sistemas, con comparación exacta de T | Con M = D, Jacobi, GS y SOR no cambian (demostración en guia_matematica.md §10). Se documenta el efecto real (κ, residuo, Richardson) en lugar de presentar una aceleración inexistente | Copiar la tabla de la lámina (no es reproducible); no implementarlo |
| 27 | Formato **CSR propio** como opción, con iteraciones idénticas a las densas | Incentivo de matrices dispersas (OFICIAL p. 5); base en S9-05/10 pp. 8-15 | `scipy.sparse` (prohibido delegar) |
| 26 | Nombre del ZIP: `Grupo01-…` o `Grupo02-…` | Interpretación de «Grupo(01-02)-IF0012-Proyecto-IIC.zip». **El número de grupo está pendiente de confirmar por el grupo**; las fechas (entrega 11-nov, defensa en la semana del 16-nov) ya están confirmadas | — |
| 28 | En mínimos cuadrados se muestran **det([A\|b]) y Cramer como verificación** | Es el procedimiento de clase (S8-30/09 pp. 6-7). La solución sigue saliendo de Gauss, como exige el enunciado | Usar Cramer como método principal |
| 29 | **Desarrollo de Sarrus** visible para T 3×3 | Es el procedimiento de clase para det(T − λI); se comprueba contra Faddeev-LeVerrier | Mostrar solo el polinomio final |
| 30 | **Reordenamiento** de las ecuaciones para lograr la dominancia: se **sugiere**, no se aplica | Lo hace la docente (Tarea II #2-3). Aplicarlo en silencio cambiaría el sistema del usuario | Reordenar automáticamente |
| 31 | «Error final» = ‖x⁽ᵏ⁾ − x*‖∞, primera métrica de la gráfica comparativa | Definición de la lámina S9-05/10 p. 17 | Usar d_k |
