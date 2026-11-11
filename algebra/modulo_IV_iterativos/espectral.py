"""Módulo IV (convergencia) — Radio espectral ρ(T) y conclusión de convergencia.

Une los dos pasos anteriores:
  matriz_iteracion.py  → T y c de cada método (procedimiento de clase, Cat. A);
  polinomio_raices.py  → det(λI - T) y sus raíces (Faddeev-LeVerrier y Durand-Kerner, Cat. C).
Aquí se toma ρ(T) = máx |λ| y se concluye con el teorema del curso: el método
converge para todo x(0) si y solo si ρ(T) < 1.

Si ρ está muy cerca de 1, o el cálculo numérico no es fiable, la conclusión se
informa como indeterminada.  Si λ = 1 o λ = -1 anulan el polinomio exacto, ρ(T) ≥ 1
con certeza.
"""

from dataclasses import dataclass, field
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import validar_cuadrada
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_IV_iterativos.matriz_iteracion import MatrizIteracion, matriz_iteracion
from algebra.modulo_IV_iterativos.polinomio_raices import (
    AVISO_CASI_REPETIDOS,
    evaluar,
    polinomio_caracteristico,
    raices,
    texto_polinomio_curso,
)

N_MAX_ESPECTRAL = 8            # tamaño máximo para el que se calcula ρ
UMBRAL_RHO_UNO = 1e-9          # banda alrededor de 1 donde la conclusión es indeterminada
# Con raíces (casi) múltiples el error de ρ puede ser ~1e-8: se amplía la banda.
UMBRAL_RHO_UNO_MULTIPLE = 1e-6

CONVERGE = "CONVERGE"
NO_CONVERGE = "NO_CONVERGE"
INDETERMINADO = "INDETERMINADO"
NO_CALCULADO = "NO_CALCULADO"


@dataclass
class ResultadoEspectral:
    iteracion: MatrizIteracion
    conclusion: str
    mensaje: str
    coeficientes: list = None      # [1, c1, ..., cn] de det(λI - T)
    polinomio_curso: str = ""      # det(T - λI) escrito como en clase
    autovalores: list = None       # complejos
    multiplicidad_cero: int = 0
    rho: float = None
    fiable: bool = False
    decision_exacta: bool = False
    verificaciones: dict = field(default_factory=dict)
    advertencias: list = field(default_factory=list)

def concluir(rho, fiable, decision_exacta=None, casi_repetidas=False):
    """Conclusión de convergencia a partir de ρ.

    decision_exacta (True/False) tiene prioridad: viene de un criterio exacto.
    Si el cálculo numérico no es fiable, o ρ está dentro de la banda de
    incertidumbre alrededor de 1, la conclusión es INDETERMINADO.
    """
    if decision_exacta is not None:
        return CONVERGE if decision_exacta else NO_CONVERGE
    banda = UMBRAL_RHO_UNO_MULTIPLE if casi_repetidas else UMBRAL_RHO_UNO
    if not fiable or abs(rho - 1) < banda:
        return INDETERMINADO
    return CONVERGE if rho < 1 else NO_CONVERGE

@dataclass
class AnalisisMatriz:
    """Autovalores y radio espectral de una matriz cuadrada cualquiera (n <= 8)."""
    coeficientes: list
    autovalores: list
    multiplicidad_cero: int
    rho: float
    fiable: bool
    decision: object              # True/False (todas |λ| < 1) si es exacta; None si no
    verificaciones: dict
    advertencias: list

def analizar_matriz(T):
    """Polinomio característico exacto, autovalores, ρ y verificaciones de la matriz T.

    Es el núcleo común de radio_espectral y del análisis del precondicionador."""
    n = validar_cuadrada(T, "matriz T")
    coeficientes = polinomio_caracteristico(T)
    autovalores, ceros, fiable, advertencias, decision = raices(coeficientes)
    rho = max(abs(z) for z in autovalores) if autovalores else 0.0

    # Verificaciones independientes de las raíces
    escala = max(1.0, max(abs(float(c)) for c in coeficientes))
    residuos = [abs(evaluar([float(c) for c in coeficientes], z)) / escala for z in autovalores]
    suma = sum(autovalores)
    traza = sum(a_fraccion(T[i][i]) for i in range(n))
    verificaciones = {
        "max |p(λ)| relativo": max(residuos) if residuos else 0.0,
        "suma de autovalores": suma,
        "traza de T": float(traza),
    }
    if abs(suma - float(traza)) > 1e-8 * max(1.0, abs(float(traza)), rho * n):
        fiable = False
        advertencias.append("La suma de los autovalores no coincide con la traza de T.")
    if residuos and max(residuos) > 1e-8:
        fiable = False
        advertencias.append("Algún autovalor no anula el polinomio con la precisión esperada.")

    # Comprobación exacta (fracciones): si λ = 1 o λ = -1 anulan p(λ), entonces
    # ρ(T) >= 1 con certeza (λ = 1 aparece, por ejemplo, cuando A es singular).
    if all(isinstance(c, Fraction) for c in coeficientes):
        for candidato in (1, -1):
            if evaluar(coeficientes, Fraction(candidato)) == 0:
                decision = False
                advertencias.append(f"λ = {candidato} es autovalor exacto de T: ρ(T) ≥ 1.")
                break
    return AnalisisMatriz(coeficientes=coeficientes, autovalores=autovalores,
                          multiplicidad_cero=ceros, rho=rho, fiable=fiable, decision=decision,
                          verificaciones=verificaciones, advertencias=advertencias)

def radio_espectral(A, b, metodo, omega=None):
    """Construye T, su polinomio característico, sus autovalores y ρ(T)."""
    n = validar_cuadrada(A, "matriz A")
    iteracion = matriz_iteracion(A, b, metodo, omega)
    if n > N_MAX_ESPECTRAL:
        return ResultadoEspectral(
            iteracion=iteracion, conclusion=NO_CALCULADO,
            mensaje=(f"No se calcula ρ(T) para n > {N_MAX_ESPECTRAL}: el procedimiento "
                     f"por polinomio característico pierde fiabilidad. Use la dominancia "
                     f"diagonal y el comportamiento observado de las iteraciones."))
    analisis = analizar_matriz(iteracion.T)
    rho, advertencias = analisis.rho, analisis.advertencias
    resultado = ResultadoEspectral(
        iteracion=iteracion, conclusion="", mensaje="", coeficientes=analisis.coeficientes,
        polinomio_curso=texto_polinomio_curso(analisis.coeficientes),
        autovalores=analisis.autovalores, multiplicidad_cero=analisis.multiplicidad_cero,
        rho=rho, fiable=analisis.fiable, verificaciones=analisis.verificaciones,
        advertencias=advertencias)
    resultado.decision_exacta = analisis.decision is not None
    resultado.conclusion = concluir(rho, analisis.fiable, analisis.decision,
                                    AVISO_CASI_REPETIDOS in advertencias)

    rho_txt = formatear_numero(rho)
    if resultado.conclusion == CONVERGE:
        resultado.mensaje = (f"ρ(T) = {rho_txt} < 1: el método {metodo} converge para "
                             f"cualquier vector inicial.")
    elif resultado.conclusion == NO_CONVERGE:
        resultado.mensaje = (f"ρ(T) = {rho_txt} ≥ 1: el método {metodo} no converge para "
                             f"todo vector inicial (la convergencia no está garantizada y, "
                             f"en general, los errores no disminuyen).")
    else:
        resultado.mensaje = (f"ρ(T) ≈ {rho_txt}: no es posible decidir con fiabilidad si "
                             f"ρ(T) < 1 (valor muy cercano a 1 o cálculo numérico poco fiable).")
    if resultado.decision_exacta:
        resultado.mensaje += " (Decisión verificada de forma exacta.)"
    return resultado
