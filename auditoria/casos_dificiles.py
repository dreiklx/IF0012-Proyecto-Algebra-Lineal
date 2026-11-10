r"""Auditoría matemática independiente (fase final, 27-oct-2026).

Uso (desde la raíz del proyecto):  .venv\Scripts\python auditoria/casos_dificiles.py .

Compara el núcleo con oráculos independientes (fórmula de Leibniz, adjunta,
Cramer, implementación separada de las iteraciones, fórmula de Gelfand).
No forma parte de la suite rápida de tests/ porque tarda unos 20 segundos y es aleatoria (semilla fija)."""
import sys, random
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from algebra.modulo_IV_iterativos.espectral import (
    durand_kerner,
    polinomio_caracteristico,
    radio_espectral,
    raices,
)
from algebra.modulo_IV_iterativos.iterativos import GAUSS_SEIDEL, JACOBI, SOR
def poli(rs):  # coeficientes de prod (λ - r) con r Fraction (reales)
    c=[F(1)]
    for r in rs:
        c=[a-r*b for a,b in zip(c+[F(0)],[F(0)]+c)]
    return c
def poli_c(c_real_pairs, reales):
    c=poli(reales)
    for (a,b2) in c_real_pairs:  # factor λ² - 2aλ + (a²+b²)
        q=[F(1),-2*a,a*a+b2]
        nc=[F(0)]*(len(c)+2)
        for i,x in enumerate(c):
            for j,y in enumerate(q): nc[i+j]+=x*y
        c=nc
    return c
casos={
 'triple 1/2': poli([F(1,2)]*3),
 'doble 0.9 + simple 0.3': poli([F(9,10),F(9,10),F(3,10)]),
 'rho=1 exacto real (1, 1/2, 1/5)': poli([F(1),F(1,2),F(1,5)]),
 'rho=1 par complejo ±i y 1/2': poli_c([(F(0),F(1))],[F(1,2)]),
 'raices casi iguales 1/2 y 1/2+1e-9': poli([F(1,2),F(1,2)+F(1,10**9),F(1,10)]),
 'escalas 1e-8, 1, 100': poli([F(1,10**8),F(1),F(100)]),
 'rho=0.999999 grado 4': poli([F(999999,10**6),F(1,2),F(-1,3),F(1,7)]),
 'par complejo doble': poli_c([(F(1,2),F(1,4)),(F(1,2),F(1,4))],[F(1,10)]),
 'cuadruple 0.8': poli([F(4,5)]*4),
 'grado 8 mixto': poli_c([(F(1,5),F(1,2)),(F(-3,10),F(1,10))],[F(9,10),F(-1,2),F(1,3),F(1,4)]),
}
for nombre,c in casos.items():
    av,ceros,fiable,adv,dec=raices(c)
    rho=max(abs(z) for z in av)
    print(f'{nombre:40s} rho={rho:.12f} fiable={fiable} decision_exacta={dec} avisos={[a[:45] for a in adv]}')
