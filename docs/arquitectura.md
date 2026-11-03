# Arquitectura

```text
proyecto-algebra/
├── app.py                  Punto de entrada Streamlit: navegación entre los 4 módulos
├── algebra/                NÚCLEO MATEMÁTICO: Python puro, sin dependencias externas
│   ├── matriz.py           Validación, transpuesta, suma, producto, normas, residuo
│   ├── validacion.py       Texto del usuario → Fraction exacta; mensajes de error
│   ├── directos.py         Gauss, Gauss-Jordan, clasificación, inversa, determinante
│   ├── condicion.py        κ∞, perturbación de b, errores relativos
│   ├── minimos.py          Ecuaciones normales, residuo, ajuste lineal
│   ├── iterativos.py       Jacobi, GS, SOR, criterios A/B/C, comparación, dominancia
│   ├── espectral.py        Matrices de iteración, polinomio característico, ρ(T)
│   ├── dispersas.py        Formato CSR propio (incentivo de matrices dispersas)
│   └── precondicionamiento.py  Precondicionador diagonal M = D (incentivo)
├── interfaz/               PRESENTACIÓN: Streamlit; no contiene cálculos
│   ├── componentes.py      LaTeX, tablas, lectura con mensajes de error
│   ├── estilo.py           Identidad visual: hoja de estilos y componentes (tarjetas, etiquetas)
│   ├── ejemplos.py         Ejemplos del curso (resultados verificados)
│   └── modulo_*.py         Una página por módulo
├── visualizacion/          GRÁFICAS: Matplotlib; solo dibujan resultados del núcleo
│   ├── tema.py             Tema común de las gráficas (colores por método, leyendas)
│   ├── graficos.py         Ajuste, convergencia, comparación, autovalores
│   └── geometria_3d.py     Rectas (2D) y planos (3D) de un sistema
├── tests/                  Pruebas unittest del núcleo y de la interfaz (AppTest)
├── auditoria/              Comparación aleatoria del núcleo con oráculos independientes
├── casos_prueba/           Casos documentados: entrada, esperado, obtenido
├── docs/                   Documentación
├── herramientas/           Solo desarrollo: generar_guia_html.py (no se entrega en el ZIP)
├── dist/                   Entrega estable: ZIP, SHA256.txt y la guía en HTML
├── .streamlit/config.toml  Solo localhost, sin telemetría, sin preguntas al arrancar
├── requirements.txt        Dependencias directas fijadas
├── ejecutar.bat            Instala la primera vez y ejecuta (Windows)
└── empaquetar.py           Genera el ZIP de entrega
```

## Reglas de dependencia

```text
interfaz  ──►  algebra  ◄──  tests
   │
   └──────►  visualizacion  (recibe resultados ya calculados)
```

- `algebra` no importa nada de `interfaz` ni de `visualizacion`, ni ninguna biblioteca externa. Por eso se puede probar y defender por separado.
- La interfaz solo lee los datos, llama al núcleo y muestra lo que este devuelve.
- Los resultados son objetos de datos (`dataclass`) con todo lo necesario para mostrar el procedimiento: pasos, historial, motivos de terminación y advertencias.

## Flujo típico (Módulo IV)

1. `modulo_iterativos.py` lee el texto con `validacion.leer_*` y obtiene números exactos o un mensaje de error.
2. Construye una `ConfiguracionIterativa` y llama a `iterativos.ejecutar(A, b, config)`.
3. `ejecutar` valida la configuración, comprueba la diagonal y repite `paso_<método>` hasta que se cumpla el criterio. Devuelve un `ResultadoIterativo` y **nunca lanza excepciones**: los errores son códigos de terminación.
4. La interfaz muestra la tabla y el motivo, y pasa el historial a `graficos.grafica_convergencia`.
