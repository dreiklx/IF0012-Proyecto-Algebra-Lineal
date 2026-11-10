"""Módulo II — Condicionamiento y sensibilidad (OFICIAL p. 2).

Número de condición en norma infinito:

    κ∞(A) = ||A||∞ · ||A⁻¹||∞

donde ||A||∞ es la mayor suma de valores absolutos por fila (S7-21/09 p. 17)
y A⁻¹ se calcula con nuestro Gauss-Jordan (OFICIAL p. 2: "la inversa deberá
obtenerse con un algoritmo implementado por el grupo").

Clasificación orientativa del proyecto (OFICIAL p. 2), que es un criterio
operativo y no una frontera matemática universal:
    κ < 10          sensibilidad baja
    10 <= κ < 100   sensibilidad moderada
    κ >= 100        sensibilidad alta

Perturbación de b: se resuelve A x = b y A x̃ = b + Δb, y se comparan
    error relativo de b:  ||Δb||∞ / ||b||∞
    error relativo de x:  ||Δx||∞ / ||x||∞,   Δx = x̃ - x
Teoría (S7-21/09 p. 18):  ||Δx|| / ||x||  <=  κ(A) · ||Δb|| / ||b||.

Una matriz singular no tiene número de condición finito; se informa por
separado y nunca se confunde con "κ grande".
"""

from dataclasses import dataclass, field
from fractions import Fraction

from algebra.compartido.exactos import a_fraccion
from algebra.compartido.matriz import (
    ErrorDimension,
    norma_infinito_matriz,
    norma_infinito_vector,
    restar_vectores,
    validar_cuadrada,
    validar_vector,
)
from algebra.compartido.validacion import formatear_numero
from algebra.modulo_I_sistemas.directos import inversa_gauss_jordan, solucion_unica

SENSIBILIDAD_BAJA = "BAJA"
SENSIBILIDAD_MODERADA = "MODERADA"
SENSIBILIDAD_ALTA = "ALTA"
MATRIZ_SINGULAR = "SINGULAR"

PERTURBACION_ABSOLUTA = "absoluta"
PERTURBACION_PORCENTAJE = "porcentaje"


@dataclass
class ResultadoCondicion:
    clasificacion: str
    interpretacion: str
    norma_A: Fraction
    inversa: list = None
    norma_inversa: Fraction = None
    kappa: Fraction = None          # None si A es singular (κ no está definido / es infinito)
    resultado_inversa: object = None


@dataclass
class ResultadoPerturbacion:
    x: list
    x_perturbada: list
    b: list
    b_perturbado: list
    delta_b: list
    delta_x: list
    norma_delta_b: Fraction
    norma_b: Fraction
    norma_delta_x: Fraction
    norma_x: Fraction
    error_relativo_b: Fraction = None   # None si ||b|| = 0
    error_relativo_x: Fraction = None   # None si ||x|| = 0
    amplificacion: Fraction = None      # error_rel_x / error_rel_b, si ambos existen
    cota: Fraction = None               # κ · error_rel_b
    cumple_cota: bool = None
    condicion: ResultadoCondicion = None
    interpretacion: str = ""
    avisos: list = field(default_factory=list)


def clasificar_kappa(kappa):
    """Devuelve la sensibilidad según la escala operativa del proyecto."""
    if kappa < 10:
        return SENSIBILIDAD_BAJA
    if kappa < 100:
        return SENSIBILIDAD_MODERADA
    return SENSIBILIDAD_ALTA


_TEXTO_SENSIBILIDAD = {
    SENSIBILIDAD_BAJA: (
        "Sensibilidad baja: pequeñas perturbaciones en los datos producen cambios "
        "relativos pequeños en la solución."),
    SENSIBILIDAD_MODERADA: (
        "Sensibilidad moderada: un error relativo en b puede amplificarse hasta "
        "κ veces en la solución; conviene vigilar la precisión de los datos."),
    SENSIBILIDAD_ALTA: (
        "Sensibilidad alta: errores relativos pequeños en los datos pueden "
        "producir errores relativos grandes en la solución (sistema mal condicionado)."),
}


def numero_condicion_infinito(A):
    """Calcula κ∞(A) = ||A||∞ ||A⁻¹||∞ y su interpretación."""
    validar_cuadrada(A, "matriz A")
    A_exacta = [[a_fraccion(v) for v in fila] for fila in A]
    norma_A = norma_infinito_matriz(A_exacta)
    inv = inversa_gauss_jordan(A_exacta)
    if not inv.invertible:
        return ResultadoCondicion(
            clasificacion=MATRIZ_SINGULAR,
            interpretacion=(
                "A es singular (det(A) = 0): no existe A⁻¹ y el número de condición no "
                "está definido (se considera infinito). El sistema no tiene solución "
                "única; esto es distinto de una matriz invertible con κ grande."),
            norma_A=norma_A, resultado_inversa=inv)
    norma_inv = norma_infinito_matriz(inv.inversa)
    kappa = norma_A * norma_inv
    clase = clasificar_kappa(kappa)
    texto = (f"κ∞(A) = ||A||∞ · ||A⁻¹||∞ = {formatear_numero(norma_A)} · "
             f"{formatear_numero(norma_inv)} = {formatear_numero(kappa)}. "
             + _TEXTO_SENSIBILIDAD[clase]
             + " (Clasificación operativa del proyecto: κ < 10 baja, 10 ≤ κ < 100 "
               "moderada, κ ≥ 100 alta; debe interpretarse según la escala y la "
               "precisión del problema.)")
    return ResultadoCondicion(
        clasificacion=clase, interpretacion=texto, norma_A=norma_A,
        inversa=inv.inversa, norma_inversa=norma_inv, kappa=kappa,
        resultado_inversa=inv)


def construir_delta_b(b, modo, valor):
    """Construye el vector Δb a partir de la perturbación pedida por el usuario.

    modo "absoluta":   valor es un número (se suma a cada componente) o un
                       vector Δb de la misma longitud que b.
    modo "porcentaje": valor es un porcentaje p (número) o un vector de
                       porcentajes; Δb_i = (p_i / 100) · b_i.
    """
    n = validar_vector(b, "vector b")
    if isinstance(valor, list):
        if len(valor) != n:
            raise ErrorDimension(
                f"La perturbación tiene {len(valor)} componentes y b tiene {n}.")
        valores = [a_fraccion(v) for v in valor]
    else:
        valores = [a_fraccion(valor)] * n
    b_exacto = [a_fraccion(v) for v in b]
    if modo == PERTURBACION_ABSOLUTA:
        return valores
    if modo == PERTURBACION_PORCENTAJE:
        return [valores[i] / 100 * b_exacto[i] for i in range(n)]
    raise ValueError(f"Modo de perturbación desconocido: {modo}")


def analizar_perturbacion(A, b, delta_b):
    """Compara la solución de A x = b con la de A x̃ = b + Δb.

    Requiere A cuadrada e invertible (si no, lanza ErrorSistema desde
    solucion_unica, con la clasificación del sistema).
    """
    n = validar_cuadrada(A, "matriz A")
    if validar_vector(b, "vector b") != n or validar_vector(delta_b, "vector Δb") != n:
        raise ErrorDimension("A, b y Δb deben tener dimensiones compatibles.")
    A_exacta = [[a_fraccion(v) for v in fila] for fila in A]
    b_exacto = [a_fraccion(v) for v in b]
    delta = [a_fraccion(v) for v in delta_b]
    b_pert = [b_exacto[i] + delta[i] for i in range(n)]

    condicion = numero_condicion_infinito(A_exacta)
    x = solucion_unica(A_exacta, b_exacto)
    x_pert = solucion_unica(A_exacta, b_pert)
    delta_x = restar_vectores(x_pert, x)

    norma_db = norma_infinito_vector(delta)
    norma_b = norma_infinito_vector(b_exacto)
    norma_dx = norma_infinito_vector(delta_x)
    norma_x = norma_infinito_vector(x)
    avisos = []
    rel_b = norma_db / norma_b if norma_b != 0 else None
    rel_x = norma_dx / norma_x if norma_x != 0 else None
    if rel_b is None:
        avisos.append("||b||∞ = 0: el error relativo de b no está definido (denominador cero).")
    if rel_x is None:
        avisos.append("||x||∞ = 0: el error relativo de x no está definido (denominador cero).")

    resultado = ResultadoPerturbacion(
        x=x, x_perturbada=x_pert, b=b_exacto, b_perturbado=b_pert, delta_b=delta,
        delta_x=delta_x, norma_delta_b=norma_db, norma_b=norma_b,
        norma_delta_x=norma_dx, norma_x=norma_x, error_relativo_b=rel_b,
        error_relativo_x=rel_x, condicion=condicion, avisos=avisos)

    if rel_b is not None and condicion.kappa is not None:
        resultado.cota = condicion.kappa * rel_b
        if rel_x is not None:
            resultado.cumple_cota = rel_x <= resultado.cota
    if rel_b is not None and rel_x is not None and rel_b != 0:
        resultado.amplificacion = rel_x / rel_b

    resultado.interpretacion = _interpretar(resultado)
    return resultado


def _porcentaje(valor):
    return f"{float(valor) * 100:.4g} %"


def _interpretar(r):
    if r.error_relativo_b is None or r.error_relativo_x is None:
        return "No se puede comparar errores relativos porque algún denominador es cero."
    if r.error_relativo_b == 0:
        return "No se aplicó ninguna perturbación (Δb = 0): las soluciones coinciden."
    partes = [
        f"Un cambio relativo de {_porcentaje(r.error_relativo_b)} en b produjo un "
        f"cambio relativo de {_porcentaje(r.error_relativo_x)} en x "
        f"(factor de amplificación {formatear_numero(r.amplificacion)})."
    ]
    if r.cota is not None:
        partes.append(
            f"La teoría garantiza que el cambio relativo en x no supera "
            f"κ∞ · ||Δb||/||b|| = {_porcentaje(r.cota)}; "
            + ("la cota se cumple." if r.cumple_cota else "LA COTA NO SE CUMPLE (revisar).")
        )
        partes.append(
            "El número de condición es el peor caso posible: según la dirección de la "
            "perturbación, la amplificación observada puede ser menor que κ.")
    return " ".join(partes)
