"""Pruebas de algebra/compartido/validacion.py (lectura de texto escrito por el usuario)."""

import unittest
from fractions import Fraction

from algebra.compartido.validacion import (
    ErrorEntrada,
    formatear_numero,
    leer_entero_positivo,
    leer_matriz,
    leer_numero,
    leer_omega,
    leer_tolerancia,
    leer_vector,
)


class TestLeerNumero(unittest.TestCase):

    def test_formatos_validos(self):
        casos = {
            "3": Fraction(3), "-12": Fraction(-12), "2.5": Fraction(5, 2),
            "2,5": Fraction(5, 2), "-0.25": Fraction(-1, 4), "1/3": Fraction(1, 3),
            "-7/4": Fraction(-7, 4), "1e-3": Fraction(1, 1000), " 4 ": Fraction(4),
            "−3": Fraction(-3), "0.1": Fraction(1, 10),
        }
        for texto, esperado in casos.items():
            self.assertEqual(leer_numero(texto), esperado, texto)

    def test_decimal_es_exacto(self):
        # 0.1 se guarda como 1/10 exacto, no como el float 0.1000000000000000055...
        self.assertEqual(leer_numero("0.1") * 3, Fraction(3, 10))

    def test_invalidos(self):
        for texto in ("", "   ", None, "abc", "1/0", "nan", "inf", "1,000.5", "2..3",
                      "1_000", "3x", "1/2/3"):
            with self.assertRaises(ErrorEntrada, msg=repr(texto)):
                leer_numero(texto)

    def test_mensaje_indica_nombre(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            leer_numero("abc", "elemento (2, 3) de la matriz A")
        self.assertIn("(2, 3)", str(ctx.exception))


class TestLeerMatrizVector(unittest.TestCase):

    def test_matriz(self):
        A = leer_matriz("2 1 -1\n1 -3 2\n\n3 2 1\n")
        self.assertEqual(A, [[2, 1, -1], [1, -3, 2], [3, 2, 1]])
        self.assertIsInstance(A[0][0], Fraction)

    def test_matriz_con_fracciones_y_decimales(self):
        self.assertEqual(leer_matriz("1/2 0,5\n-1 1e1"),
                         [[Fraction(1, 2), Fraction(1, 2)], [-1, 10]])

    def test_matriz_filas_desiguales(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            leer_matriz("1 2 3\n4 5")
        self.assertIn("fila 2", str(ctx.exception))

    def test_matriz_vacia_o_invalida(self):
        for texto in ("", "  \n  ", None):
            with self.assertRaises(ErrorEntrada):
                leer_matriz(texto)
        with self.assertRaises(ErrorEntrada) as ctx:
            leer_matriz("1 2\n3 x")
        self.assertIn("(2, 2)", str(ctx.exception))

    def test_vector(self):
        self.assertEqual(leer_vector("1 2\n3"), [1, 2, 3])
        with self.assertRaises(ErrorEntrada):
            leer_vector("")
        with self.assertRaises(ErrorEntrada) as ctx:
            leer_vector("1 a 3")
        self.assertIn("componente 2", str(ctx.exception))


class TestParametros(unittest.TestCase):

    def test_tolerancia(self):
        self.assertEqual(leer_tolerancia("1e-3"), Fraction(1, 1000))
        for texto in ("0", "-1", "abc", ""):
            with self.assertRaises(ErrorEntrada):
                leer_tolerancia(texto)

    def test_entero_positivo(self):
        self.assertEqual(leer_entero_positivo("50", "máximo", 100000), 50)
        self.assertEqual(leer_entero_positivo("100000", "máximo", 100000), 100000)
        for texto in ("0", "-3", "2.5", "2,5", "100001", "x", ""):
            with self.assertRaises(ErrorEntrada, msg=texto):
                leer_entero_positivo(texto, "máximo", 100000)

    def test_omega(self):
        self.assertEqual(leer_omega("1.2"), Fraction(6, 5))
        self.assertEqual(leer_omega("1,04"), Fraction(26, 25))
        for texto in ("0", "2", "2.5", "-1", ""):
            with self.assertRaises(ErrorEntrada, msg=texto):
                leer_omega(texto)


class TestFormato(unittest.TestCase):

    def test_formatos(self):
        self.assertEqual(formatear_numero(Fraction(4)), "4")
        self.assertEqual(formatear_numero(Fraction(-29, 33)), "-29/33")
        self.assertEqual(formatear_numero(0.000378139123), "0.000378139")
        self.assertEqual(formatear_numero(complex(0.5, -1.25)), "0.5 − 1.25i")


if __name__ == "__main__":
    unittest.main()
