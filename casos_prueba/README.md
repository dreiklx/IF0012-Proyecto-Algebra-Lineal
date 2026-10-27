# Casos de prueba

| Archivo | Módulo |
|---|---|
| [modulo_I.md](modulo_I.md) | Sistemas lineales y métodos directos |
| [modulo_II.md](modulo_II.md) | Condicionamiento y sensibilidad |
| [modulo_III.md](modulo_III.md) | Mínimos cuadrados y ajuste lineal |
| [modulo_IV.md](modulo_IV.md) | Métodos iterativos y radio espectral |

Cada caso tiene una entrada, una salida esperada calculada de forma independiente y el resultado que obtuvo la aplicación. Las mismas comprobaciones se ejecutan automáticamente con `python -m unittest`.

## Caso de validación obligatorio de la docente

**Pendiente.** OFICIAL p. 3 indica que la docente proporcionará al menos un caso obligatorio antes de la entrega. Cuando llegue:

1. Añadirlo aquí, en `caso_obligatorio.md`, con la entrada exacta recibida.
2. Ejecutarlo en la aplicación y registrar el resultado obtenido.
3. Calcular la salida esperada de forma independiente.
4. Agregar una prueba automática en el archivo `tests/test_*.py` del módulo correspondiente.
