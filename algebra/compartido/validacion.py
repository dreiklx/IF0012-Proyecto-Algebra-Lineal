"""Lectura y validación de los datos que escribe el usuario.

La interfaz entrega texto; este módulo lo convierte en números exactos
(fractions.Fraction) o lanza ErrorEntrada con un mensaje comprensible que
indica dónde está el problema.  Así ninguna entrada inválida llega a los
algoritmos ni provoca un cierre inesperado (OFICIAL p. 3, validaciones).

Formatos de número aceptados (una celda):
    entero          3   -12
    decimal         2.5   -0.25   2,5   (coma decimal permitida)
    fracción        1/3   -7/4
    notación cient. 1e-3   2.5E2

Formato de matriz: una fila por línea, números separados por espacios
(o tabuladores).  Formato de vector: números separados por espacios o saltos
de línea.
"""

from fractions import Fraction


class ErrorEntrada(ValueError):
    """El texto introducido por el usuario no es válido."""


def leer_numero(texto, nombre="valor"):
    """Convierte un texto en un Fraction exacto.

    Se usa Fraction(texto) y no float(texto) para que "0.1" valga exactamente
    1/10 (con float valdría 0.1000000000000000055...).
    """
    if texto is None:
        raise ErrorEntrada(f"El {nombre} está vacío.")
    limpio = str(texto).strip()
    if limpio == "":
        raise ErrorEntrada(f"El {nombre} está vacío.")
    limpio = limpio.replace("−", "-")  # signo menos tipográfico "−"
    if "_" in limpio:
        raise ErrorEntrada(f"El {nombre} «{limpio}» no es un número válido.")
    # Coma decimal: "2,5" -> "2.5" (solo si hay una coma y ningún punto).
    if limpio.count(",") == 1 and "." not in limpio:
        limpio = limpio.replace(",", ".")
    try:
        valor = Fraction(limpio)
    except ZeroDivisionError:
        raise ErrorEntrada(f"El {nombre} «{texto}» tiene denominador cero.") from None
    except ValueError:
        raise ErrorEntrada(
            f"El {nombre} «{texto}» no es un número válido "
            f"(use, por ejemplo, 3, -2.5, 2,5 o 1/3)."
        ) from None
    return valor


def leer_matriz(texto, nombre="matriz"):
    """Convierte un texto (una fila por línea) en una matriz de Fraction.

    Se ignoran las líneas en blanco.  Todas las filas deben tener la misma
    cantidad de números.
    """
    if texto is None or str(texto).strip() == "":
        raise ErrorEntrada(f"La {nombre} está vacía.")
    filas = []
    for linea in str(texto).splitlines():
        if linea.strip() == "":
            continue
        numero_fila = len(filas) + 1
        celdas = linea.split()
        fila = []
        for j, celda in enumerate(celdas, start=1):
            fila.append(leer_numero(celda, f"elemento ({numero_fila}, {j}) de la {nombre}"))
        if filas and len(fila) != len(filas[0]):
            raise ErrorEntrada(
                f"La fila {numero_fila} de la {nombre} tiene {len(fila)} números; "
                f"la fila 1 tiene {len(filas[0])}. Todas deben tener la misma cantidad."
            )
        filas.append(fila)
    return filas


def leer_vector(texto, nombre="vector"):
    """Convierte un texto con números separados por espacios o líneas en una lista."""
    if texto is None or str(texto).strip() == "":
        raise ErrorEntrada(f"El {nombre} está vacío.")
    celdas = str(texto).split()
    return [leer_numero(c, f"componente {i} del {nombre}") for i, c in enumerate(celdas, start=1)]


def leer_tolerancia(texto, nombre="tolerancia ε"):
    """Lee ε y exige ε > 0 (OFICIAL p. 3).  Devuelve un Fraction."""
    valor = leer_numero(texto, nombre)
    if valor <= 0:
        raise ErrorEntrada(f"La {nombre} debe ser un número mayor que 0.")
    return valor


def leer_entero_positivo(texto, nombre, maximo):
    """Lee un entero n con 1 <= n <= maximo (k_max, N).  Rechaza 2.5, 0, -3."""
    valor = leer_numero(texto, nombre)
    if valor.denominator != 1:
        raise ErrorEntrada(f"El {nombre} debe ser un número entero (se recibió {texto}).")
    entero = int(valor)
    if entero < 1 or entero > maximo:
        raise ErrorEntrada(f"El {nombre} debe ser un entero entre 1 y {maximo}.")
    return entero


def leer_omega(texto):
    """Lee el factor de relajación de SOR y exige 0 < ω < 2 (OFICIAL p. 3).

    Este rango es el de trabajo del proyecto: no garantiza la convergencia.
    """
    valor = leer_numero(texto, "factor de relajación ω")
    if not (0 < valor < 2):
        raise ErrorEntrada(
            "El factor de relajación debe cumplir 0 < ω < 2. "
            "Este rango no garantiza por sí solo la convergencia."
        )
    return valor


def formatear_numero(valor, cifras=6):
    """Representa un número para mostrarlo: fracciones exactas cortas tal cual,
    el resto en decimal con `cifras` cifras significativas."""
    if isinstance(valor, Fraction):
        if valor.denominator == 1:
            return str(valor.numerator)
        if len(str(valor)) <= 12:
            return str(valor)
        valor = float(valor)
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, complex):
        return f"{formatear_numero(valor.real, cifras)} {'+' if valor.imag >= 0 else '−'} {formatear_numero(abs(valor.imag), cifras)}i"
    return f"{valor:.{cifras}g}"
