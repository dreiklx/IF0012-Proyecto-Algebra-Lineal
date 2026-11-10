"""Ejemplos precargados.  Todos provienen de los materiales del curso; los
resultados esperados están verificados de forma independiente (ver
casos_prueba/).  Cuando la lámina original tiene un error, se indica."""

DIRECTOS = {
    "S6-16/09 p. 29 — solución única (1/3, 4, 5/3)": ("1 1 1\n2 1 -1\n-1 1 2", "6 3 7"),
    "S6-14/09 p. 29 — Gauss (la lámina da un resultado erróneo)": ("2 1 -1\n1 -3 2\n3 2 1", "1 4 0"),
    "Pivote nulo: requiere intercambio de filas": ("0 1 1\n1 1 1\n1 2 3", "2 3 6"),
    "Infinitas soluciones (una variable libre)": ("1 1 1\n2 2 2\n1 -1 0", "1 2 0"),
    "Sistema inconsistente (planos sin punto común)": ("1 1 1\n1 1 1\n1 -1 2", "1 2 0"),
    "LU de clase S6-16/09 p. 35 — solución (1, 1, 2)": ("2 1 1\n4 -6 0\n-2 7 2", "5 -2 9"),
    "2 incógnitas: 2x + y = 5, x − y = 1": ("2 1\n1 -1", "5 1"),
}

CONDICION = {
    "S7-21/09 p. 20 — bien condicionada (corregida)": ("4 1\n1 3", "1 2", "0.01 -0.01"),
    "S7-21/09 p. 15 — mal condicionada": ("1 1\n1 1.0001", "2 2.0001", "0 0.0001"),
    "S8-28/09 p. 13 — A = I + 10J (κ∞ = 41)": ("11 10 10\n10 11 10\n10 10 11", "31 31 31", "1 -1 1"),
    "S7-21/09 p. 19 — κ∞ = 16/5": ("1 2\n3 1", "3 4", "0.1 0.1"),
}

MINIMOS = {
    "S8-30/09 pp. 6-7 — x̂ = (65/33, −29/33)": ("1 3\n3 -2\n-2 5", "-1 8 -8"),
    "Tarea II #1 — x̂ = (4/11, 15/11)": ("1 1\n2 1\n1 2", "2 2 3"),
    "Columnas dependientes (AᵀA singular)": ("1 2\n2 4\n3 6", "1 2 4"),
}

AJUSTE = {
    "S8-30/09 p. 8 — y = 0.75x + 1.2": ("1 2 3 4", "2 2.5 3.7 4.1"),
    "Puntos alineados — y = 2x + 1": ("0 1 2 3", "1 3 5 7"),
}

ITERATIVOS = {
    "S8-30/09 — 10x−y+2z=6 (dominante)": ("10 -1 2\n-1 11 -1\n2 -1 10", "6 25 -11"),
    "S8-30/09 p. 32 — SOR del manuscrito": ("10 2 1\n2 10 2\n1 2 10", "9 13 14"),
    "S8-30/09 p. 19 — solución (2, 3, 4)": ("6 2 1\n-1 8 2\n1 -1 6", "22 30 23"),
    "Tarea II #4/#5": ("4 -1 1\n-2 6 1\n1 1 5", "7 9 -6"),
    "S9-07/10 — Jacobi no converge (ρ ≈ 1.174)": ("3 3 3\n3 3 2\n-3 -2 3", "9 9 -2"),
    "Tarea II #3 reordenada — SOR ω = 1.04": ("4 -1 0\n-1 4 -1\n0 -1 3", "15 10 10"),
    "Tridiagonal dispersa [−1, 4, −1]": ("4 -1 0 0\n-1 4 -1 0\n0 -1 4 -1\n0 0 -1 4", "1 0 0 1"),
}
