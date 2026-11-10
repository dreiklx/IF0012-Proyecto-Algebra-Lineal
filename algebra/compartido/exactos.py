"""Aritmética exacta compartida.

Los módulos I, II y III (y la construcción de T en el IV) trabajan con
fractions.Fraction para que la clasificación y los resultados no dependan del
redondeo.  Esta función convierte lo que llega de la interfaz a una fracción.
"""

from fractions import Fraction


def a_fraccion(valor):
    """Convierte int/Fraction/float a Fraction exacta del decimal escrito."""
    if isinstance(valor, Fraction):
        return valor
    if isinstance(valor, int):
        return Fraction(valor)
    return Fraction(repr(valor))  # float: repr da el decimal más corto que lo representa
