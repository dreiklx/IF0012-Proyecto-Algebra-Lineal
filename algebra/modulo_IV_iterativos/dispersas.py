"""Incentivo «Matrices dispersas» (OFICIAL p. 5): almacenamiento CSR propio.

Una matriz es dispersa cuando casi todos sus elementos son cero
(nnz << n², S9-05/10 p. 8).  El formato CSR ("Compressed Sparse Row",
S9-05/10 p. 9) guarda solo los no nulos, fila por fila, en tres listas:

    valores     a_ij no nulos, recorriendo las filas en orden
    columnas    la columna j de cada valor
    inicio      inicio[i] .. inicio[i+1]-1 son las posiciones de la fila i
                (len(inicio) = n + 1; inicio[n] = nnz)

Ejemplo (tridiagonal 3x3):
    [[ 4, -1,  0],        valores  = [4, -1, -1, 4, -1, -1, 4]
     [-1,  4, -1],   ->   columnas = [0,  1,  0, 1,  2,  1, 2]
     [ 0, -1,  4]]        inicio   = [0, 2, 5, 7]

Estrategia: Jacobi, Gauss-Seidel y SOR solo necesitan, para cada fila i,
recorrer sus elementos no nulos.  Con CSR cada iteración cuesta O(nnz) en
lugar de O(n²) y la memoria es O(nnz).  Los pasos recorren los no nulos en
el mismo orden de columnas que la versión densa, por lo que producen
EXACTAMENTE las mismas iteraciones (sumar productos por cero no cambia el
resultado en punto flotante).
"""

from dataclasses import dataclass

from algebra.compartido.matriz import validar_cuadrada


@dataclass
class MatrizCSR:
    n: int
    valores: list
    columnas: list
    inicio: list

    @property
    def nnz(self):
        """Número de elementos no nulos."""
        return len(self.valores)

    @property
    def densidad(self):
        """Fracción de elementos no nulos: nnz / n²."""
        return self.nnz / (self.n * self.n)

    def memoria(self):
        """Cantidad de números almacenados: CSR (2·nnz + n + 1) frente a denso (n²)."""
        return {"csr": 2 * self.nnz + self.n + 1, "densa": self.n * self.n}

    def diagonal(self):
        """Devuelve a_ii de cada fila (0 si no está almacenado)."""
        d = [0.0] * self.n
        for i in range(self.n):
            for p in range(self.inicio[i], self.inicio[i + 1]):
                if self.columnas[p] == i:
                    d[i] = self.valores[p]
        return d


def a_csr(A):
    """Convierte una matriz densa (lista de filas) al formato CSR."""
    n = validar_cuadrada(A, "matriz A")
    valores, columnas, inicio = [], [], [0]
    for i in range(n):
        for j in range(n):
            if A[i][j] != 0:
                valores.append(float(A[i][j]))
                columnas.append(j)
        inicio.append(len(valores))
    return MatrizCSR(n=n, valores=valores, columnas=columnas, inicio=inicio)


def a_densa(M):
    """Reconstruye la matriz densa (para comprobar la conversión)."""
    A = [[0.0] * M.n for _ in range(M.n)]
    for i in range(M.n):
        for p in range(M.inicio[i], M.inicio[i + 1]):
            A[i][M.columnas[p]] = M.valores[p]
    return A


def producto_csr_vector(M, x):
    """y = A x recorriendo solo los no nulos: O(nnz)."""
    y = [0.0] * M.n
    for i in range(M.n):
        suma = 0.0
        for p in range(M.inicio[i], M.inicio[i + 1]):
            suma += M.valores[p] * x[M.columnas[p]]
        y[i] = suma
    return y


def _suma_fuera_diagonal(M, i, x):
    suma = 0.0
    diagonal = 0.0
    for p in range(M.inicio[i], M.inicio[i + 1]):
        j = M.columnas[p]
        if j == i:
            diagonal = M.valores[p]
        else:
            suma += M.valores[p] * x[j]
    return suma, diagonal


def paso_jacobi_csr(M, b, x_anterior, omega=None):
    x_nuevo = [0.0] * M.n
    for i in range(M.n):
        suma, a_ii = _suma_fuera_diagonal(M, i, x_anterior)
        x_nuevo[i] = (b[i] - suma) / a_ii
    return x_nuevo


def paso_gauss_seidel_csr(M, b, x_anterior, omega=None):
    x = list(x_anterior)
    for i in range(M.n):
        suma, a_ii = _suma_fuera_diagonal(M, i, x)
        x[i] = (b[i] - suma) / a_ii
    return x


def paso_sor_csr(M, b, x_anterior, omega):
    x = list(x_anterior)
    for i in range(M.n):
        suma, a_ii = _suma_fuera_diagonal(M, i, x)
        valor_gs = (b[i] - suma) / a_ii
        x[i] = (1 - omega) * x_anterior[i] + omega * valor_gs
    return x


def paso_richardson_csr(M, b, x_anterior, omega=None):
    """Richardson en CSR (extensión; ver metodos.paso_richardson)."""
    ax = producto_csr_vector(M, x_anterior)
    return [x_anterior[i] + (b[i] - ax[i]) for i in range(M.n)]


def residuo_inf_csr(M, b, x):
    """||b - A x||∞ con el producto disperso."""
    ax = producto_csr_vector(M, x)
    mayor = 0.0
    for i in range(M.n):
        valor = abs(b[i] - ax[i])
        if valor > mayor or valor != valor:   # valor != valor detecta NaN
            mayor = valor
    return mayor


def tridiagonal(n, diagonal=4.0, fuera=-1.0):
    """Matriz tridiagonal n x n densa (ejemplo típico de S9-05/10 pp. 8-14)."""
    return [[diagonal if i == j else (fuera if abs(i - j) == 1 else 0.0) for j in range(n)]
            for i in range(n)]
