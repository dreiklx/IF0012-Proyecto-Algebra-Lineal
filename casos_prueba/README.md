# Casos de prueba

| Archivo | Módulo |
|---|---|
| [modulo_I.md](modulo_I.md) | Sistemas lineales y métodos directos |
| [modulo_II.md](modulo_II.md) | Condicionamiento y sensibilidad |
| [modulo_III.md](modulo_III.md) | Mínimos cuadrados y ajuste lineal |
| [modulo_IV.md](modulo_IV.md) | Métodos iterativos y radio espectral |

Cada caso tiene una entrada, una salida esperada calculada de forma independiente y el resultado que obtuvo la aplicación. Las mismas comprobaciones se ejecutan automáticamente con `python -m unittest`.

## Caso de validación obligatorio de la docente

**Pendiente: no se ha recibido** (búsqueda hecha el 03-nov-2026 en el texto de todos los PDF del curso).

- **Requisito:** OFICIAL p. 3, «La docente proporcionará al menos un caso de validación obligatorio antes de la entrega».
- **Dónde va:** OFICIAL p. 1, «Carpeta de casos de prueba, incluyendo los casos obligatorios indicados por la docente».
- **Qué acredita:** el criterio «Casos de prueba» de la rúbrica (3 %): «aplicación supera el caso obligatorio».

Detalle y pregunta para la docente: `docs/pendientes_docente.md`, P-3.

**Cuando llegue:**

1. Crear aquí `caso_obligatorio.md` con la entrada exacta recibida, la fecha y el medio.
2. Anotar la salida esperada que dé la docente. Si no la da, calcularla de forma independiente.
3. Ejecutarlo en la aplicación y registrar el resultado obtenido: entrada, esperado, obtenido y si coincide.
4. Crear `tests/test_caso_obligatorio.py` con esos datos exactos.
5. Ejecutar todas las pruebas y la auditoría, regenerar el ZIP y subir a GitHub.
