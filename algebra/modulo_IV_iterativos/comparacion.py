"""Módulo IV — Comparación de Jacobi, Gauss-Seidel y SOR (OFICIAL p. 2).

Ejecuta las configuraciones sobre el mismo A x = b, comprueba que sean
comparables (mismo criterio, ε, k_max, N y x(0)) y calcula el «error final»
e = ||x(k) - x*||∞ con la x* exacta del Módulo I, como en la tabla de la
lámina S9-05/10 p. 17.
"""

from dataclasses import dataclass

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import ErrorMatriz
from algebra.compartido.validacion import ErrorEntrada
from algebra.modulo_IV_iterativos.ejecucion import (
    CRITERIO_CAMBIO,
    CRITERIO_ITERACIONES,
    ConfiguracionIterativa,
    ejecutar,
    norma_inf,
)
from algebra.modulo_IV_iterativos.metodos import METODOS
from algebra.modulo_I_sistemas.directos import ErrorSistema, solucion_unica


CAMPOS_HOMOGENEOS = ("criterio", "tolerancia", "k_max", "n_iteraciones", "x0")


@dataclass
class ResultadoComparacion:
    resultados: list
    homogeneo: bool
    diferencias: list
    referencia: list = None          # solución del método directo, si existe
    errores_finales: list = None     # ||x_final - x*||∞ por método (o None)
    errores_historial: list = None   # lista por método de e_k
    nota: str = ("El número de iteraciones solo es comparable entre métodos que "
                 "terminaron por el mismo motivo.")


def _valor_campo(config, campo):
    valor = getattr(config, campo)
    if campo == "x0" and valor is not None:
        return tuple(float(a_fraccion(v)) for v in valor)
    if campo in ("tolerancia",):
        return float(a_fraccion(valor))
    return valor


def comparar_metodos(A, b, configuraciones):
    """Ejecuta varias configuraciones sobre el mismo A x = b y las compara.

    Se considera homogéneo si coinciden criterio, tolerancia, k_max, N y x(0)
    (los que corresponden al criterio).  ω solo afecta a SOR y no se compara.
    """
    resultados = [ejecutar(A, b, c) for c in configuraciones]
    diferencias = []
    base = configuraciones[0]
    campos = list(CAMPOS_HOMOGENEOS)
    if base.criterio == CRITERIO_ITERACIONES:
        campos.remove("tolerancia")
        campos.remove("k_max")
    else:
        campos.remove("n_iteraciones")
    for campo in campos:
        try:
            valores = {_valor_campo(c, campo) for c in configuraciones}
        except Exception:
            valores = {None, "?"}
        if len(valores) > 1:
            diferencias.append(campo)

    referencia = None
    try:
        referencia = [float(v) for v in solucion_unica(
            [[a_fraccion(v) for v in fila] for fila in A], [a_fraccion(v) for v in b])]
    except (ErrorSistema, ErrorMatriz, ErrorEntrada, OverflowError, ValueError):
        referencia = None

    errores_finales = []
    errores_historial = []
    for r in resultados:
        if referencia is None or not r.historial:
            errores_finales.append(None)
            errores_historial.append(None)
            continue
        historia = [norma_inf([fila.x[i] - referencia[i] for i in range(len(referencia))])
                    for fila in r.historial]
        errores_historial.append(historia)
        errores_finales.append(historia[-1])
    return ResultadoComparacion(
        resultados=resultados, homogeneo=not diferencias, diferencias=diferencias,
        referencia=referencia, errores_finales=errores_finales,
        errores_historial=errores_historial)


def configuraciones_homogeneas(criterio=CRITERIO_CAMBIO, tolerancia=1e-3, k_max=50,
                               n_iteraciones=5, x0=None, omega=1.2):
    """Devuelve las tres configuraciones (Jacobi, Gauss-Seidel, SOR) con los mismos
    parámetros; SOR usa además su propio ω."""
    return [ConfiguracionIterativa(metodo=m, criterio=criterio, tolerancia=tolerancia,
                                   k_max=k_max, n_iteraciones=n_iteraciones,
                                   x0=list(x0) if x0 is not None else None, omega=omega)
            for m in METODOS]
