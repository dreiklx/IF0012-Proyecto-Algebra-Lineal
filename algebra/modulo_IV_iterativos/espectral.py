"""Módulo IV (convergencia) — Radio espectral ρ(T) con procedimientos de clase.

  matriz_iteracion.py  → T y c de cada método (procedimiento de clase);
  polinomio_raices.py  → det(T − λI) por Sarrus y sus raíces por factor λ y fórmula cuadrática.

ρ(T) = máx |λ| y el teorema del curso: el método converge para todo x(0) si y solo si ρ(T) < 1
(S9-07/10 pp. 3-7).  Si el procedimiento de clase no permite obtener los autovalores, ρ no se
calcula (OFICIAL p. 2: «cuando el procedimiento estudiado lo permita»).
La matriz de iteración de SOR no aparece en los materiales del curso (solo su forma por
componentes, S8-30/09 pp. 32-33): ρ no se calcula para SOR.
"""

from dataclasses import dataclass, field

from algebra.compartido.matriz import validar_cuadrada
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_IV_iterativos.matriz_iteracion import MatrizIteracion, matriz_iteracion
from algebra.modulo_IV_iterativos.metodos import SOR
from algebra.modulo_IV_iterativos.polinomio_raices import (
    ErrorNoCalculable,
    N_MAX_CARACTERISTICO,
    evaluar,
    polinomio_caracteristico,
    raices,
    texto_polinomio_curso,
)

UMBRAL_RHO_UNO = 1e-9          # banda alrededor de 1 donde la conclusión es indeterminada

CONVERGE = "CONVERGE"
NO_CONVERGE = "NO_CONVERGE"
INDETERMINADO = "INDETERMINADO"
NO_CALCULADO = "NO_CALCULADO"


@dataclass
class ResultadoEspectral:
    iteracion: MatrizIteracion
    conclusion: str
    mensaje: str
    coeficientes: list = None      # [1, c1, ..., cn] de det(λI − T), exactos
    polinomio_curso: str = ""      # det(T − λI) escrito como en clase
    autovalores: list = None       # complejos; None si no se pueden obtener con el curso
    multiplicidad_cero: int = 0
    rho: float = None
    fiable: bool = False
    verificaciones: dict = field(default_factory=dict)
    advertencias: list = field(default_factory=list)


def concluir(rho, fiable):
    """Conclusión de convergencia a partir de ρ; INDETERMINADO si ρ está pegado a 1."""
    if not fiable or abs(rho - 1) < UMBRAL_RHO_UNO:
        return INDETERMINADO
    return CONVERGE if rho < 1 else NO_CONVERGE


@dataclass
class AnalisisMatriz:
    coeficientes: list
    autovalores: list          # None si no se pueden obtener
    multiplicidad_cero: int
    rho: float                 # None si no se pueden obtener
    fiable: bool
    verificaciones: dict
    advertencias: list


def analizar_matriz(T):
    """Polinomio característico, autovalores y ρ de una matriz T (n ≤ 3).

    Lanza ErrorNoCalculable si el procedimiento del curso no alcanza."""
    validar_cuadrada(T, "matriz T")
    coeficientes = polinomio_caracteristico(T)
    autovalores, ceros = raices(coeficientes)
    advertencias = []
    if autovalores is None:
        return AnalisisMatriz(coeficientes=coeficientes, autovalores=None, multiplicidad_cero=ceros,
                              rho=None, fiable=False, verificaciones={}, advertencias=[
            "El polinomio tiene grado ≥ 3 después de extraer λ = 0 y no se factoriza con los "
            "procedimientos del curso: ρ(T) no se calcula."])
    rho = max(abs(z) for z in autovalores)
    # Verificación: cada autovalor anula el polinomio y la suma es la traza de T.
    escala = max(1.0, max(abs(float(c)) for c in coeficientes))
    residuos = [abs(evaluar([float(c) for c in coeficientes], z)) / escala for z in autovalores]
    traza = sum(float(T[i][i]) for i in range(len(T)))
    suma = sum(autovalores)
    verificaciones = {"max |p(λ)| relativo": max(residuos) if residuos else 0.0,
                      "suma de autovalores": suma, "traza de T": traza}
    fiable = max(residuos or [0.0]) < 1e-8 and abs(suma - traza) < 1e-8 * max(1.0, abs(traza))
    if not fiable:
        advertencias.append("La verificación de los autovalores no cumple la precisión esperada.")
    return AnalisisMatriz(coeficientes=coeficientes, autovalores=autovalores, multiplicidad_cero=ceros,
                          rho=rho, fiable=fiable, verificaciones=verificaciones,
                          advertencias=advertencias)


def radio_espectral(A, b, metodo, omega=None):
    """Construye T, su polinomio característico, sus autovalores y ρ(T), si el curso lo permite."""
    n = validar_cuadrada(A, "matriz A")
    iteracion = matriz_iteracion(A, b, metodo, omega) if metodo != SOR else None
    if metodo == SOR:
        return ResultadoEspectral(
            iteracion=None, conclusion=NO_CALCULADO,
            mensaje=("No se calcula ρ(T) para SOR: su matriz de iteración no aparece en los "
                     "materiales del curso (solo su forma por componentes)."))
    if n > N_MAX_CARACTERISTICO:
        return ResultadoEspectral(
            iteracion=iteracion, conclusion=NO_CALCULADO,
            mensaje=(f"No se calcula ρ(T) para n > {N_MAX_CARACTERISTICO}: el desarrollo de "
                     f"det(T − λI) por Sarrus solo cubre 2×2 y 3×3 (procedimiento del curso)."))
    try:
        analisis = analizar_matriz(iteracion.T)
    except ErrorNoCalculable as error:
        return ResultadoEspectral(iteracion=iteracion, conclusion=NO_CALCULADO, mensaje=str(error))
    if analisis.rho is None:
        return ResultadoEspectral(
            iteracion=iteracion, conclusion=NO_CALCULADO, coeficientes=analisis.coeficientes,
            polinomio_curso=texto_polinomio_curso(analisis.coeficientes),
            mensaje=("No se calcula ρ(T): " + analisis.advertencias[0] + " "
                     + texto_polinomio_curso(analisis.coeficientes) + "."))
    resultado = ResultadoEspectral(
        iteracion=iteracion, conclusion="", mensaje="", coeficientes=analisis.coeficientes,
        polinomio_curso=texto_polinomio_curso(analisis.coeficientes),
        autovalores=analisis.autovalores, multiplicidad_cero=analisis.multiplicidad_cero,
        rho=analisis.rho, fiable=analisis.fiable, verificaciones=analisis.verificaciones,
        advertencias=analisis.advertencias)
    resultado.conclusion = concluir(analisis.rho, analisis.fiable)
    rho_txt = formatear_numero(analisis.rho)
    if resultado.conclusion == CONVERGE:
        resultado.mensaje = f"ρ(T) = {rho_txt} < 1: el método {metodo} converge para cualquier vector inicial."
    elif resultado.conclusion == NO_CONVERGE:
        resultado.mensaje = (f"ρ(T) = {rho_txt} ≥ 1: el método {metodo} no converge para todo vector "
                             f"inicial (la convergencia no está garantizada).")
    else:
        resultado.mensaje = (f"ρ(T) ≈ {rho_txt}: no es posible decidir con fiabilidad si ρ(T) < 1.")
    return resultado
