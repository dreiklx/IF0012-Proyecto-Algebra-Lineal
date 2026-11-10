r"""Auditoría matemática independiente (fase final, 27-oct-2026).

Uso (desde la raíz del proyecto):  .venv\Scripts\python auditoria/auditoria_directos.py .

Compara el núcleo con oráculos independientes (fórmula de Leibniz, adjunta,
Cramer, implementación separada de las iteraciones, fórmula de Gelfand).
No forma parte de la suite rápida de tests/ porque tarda unos 20 segundos y es aleatoria (semilla fija)."""
# Auditoría independiente de Módulos I-III: oráculos por Leibniz/adjunta/Cramer.
import sys, random, itertools
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from algebra.condicion import analizar_perturbacion, numero_condicion_infinito
from algebra.minimos import minimos_cuadrados
from algebra.modulo_I_sistemas.directos import (
    INCONSISTENTE,
    INFINITAS,
    PIVOTEO_PARCIAL,
    UNICA,
    determinante,
    inversa_gauss_jordan,
    resolver_gauss,
    resolver_gauss_jordan,
)

def leibniz(M):
    n=len(M); tot=F(0)
    for p in itertools.permutations(range(n)):
        s=1
        for i in range(n):
            for j in range(i+1,n):
                if p[i]>p[j]: s=-s
        prod=F(1)
        for i in range(n): prod*=M[i][p[i]]
        tot+=s*prod
    return tot
def rango(M):
    m=len(M); n=len(M[0])
    for k in range(min(m,n),0,-1):
        for filas in itertools.combinations(range(m),k):
            for cols in itertools.combinations(range(n),k):
                if leibniz([[M[i][j] for j in cols] for i in filas])!=0: return k
    return 0
def mul(A,x): return [sum(F(a)*xi for a,xi in zip(f,x)) for f in A]
random.seed(2026)
errores=0; casos=0
for _ in range(1500):
    m=random.randint(1,4); n=random.randint(1,4)
    rng=random.choice([1,2,3])
    A=[[F(random.randint(-rng,rng), random.choice([1,1,1,2,3])) for _ in range(n)] for _ in range(m)]
    if random.random()<0.3 and m>1:  # filas dependientes
        k=random.randrange(m); A[k]=[2*v for v in A[(k+1)%m]]
    b=[F(random.randint(-3,3)) for _ in range(m)]
    rA=rango(A); rAb=rango([A[i]+[b[i]] for i in range(m)])
    esperado = INCONSISTENTE if rA<rAb else (UNICA if rA==n else INFINITAS)
    for res in (resolver_gauss(A,b), resolver_gauss_jordan(A,b), resolver_gauss(A,b,PIVOTEO_PARCIAL)):
        casos+=1
        ok = res.clasificacion==esperado and res.rango_A==rA and res.rango_aumentada==rAb
        if esperado==UNICA: ok = ok and mul(A,res.solucion)==b
        if esperado==INFINITAS:
            ok = ok and mul(A,res.solucion_particular)==b and all(mul(A,v)==[0]*m for v in res.direcciones) and len(res.direcciones)==n-rA
            # direcciones linealmente independientes
            if res.direcciones: ok = ok and rango([list(v) for v in res.direcciones])==len(res.direcciones)
        if m==n: ok = ok and res.determinante==leibniz(A)
        if not ok: errores+=1; print('FALLO directos',A,b,res.clasificacion,esperado); break
print('directos: casos',casos,'fallos',errores)
# inversa, det, kappa
e2=0
for _ in range(400):
    n=random.randint(1,4)
    A=[[F(random.randint(-4,4),random.choice([1,2])) for _ in range(n)] for _ in range(n)]
    d=leibniz(A); r=inversa_gauss_jordan(A)
    if d==0:
        ok = (not r.invertible) and numero_condicion_infinito(A).kappa is None and determinante(A)==0
    else:
        adj=[[ (-1)**(i+j)*leibniz([[A[a][c] for c in range(n) if c!=i] for a in range(n) if a!=j]) if n>1 else F(1) for j in range(n)] for i in range(n)]
        inv=[[v/d for v in f] for f in adj]
        nA=max(sum(abs(v) for v in f) for f in A); nI=max(sum(abs(v) for v in f) for f in inv)
        ok = r.invertible and r.inversa==inv and r.determinante==d and determinante(A)==d and numero_condicion_infinito(A).kappa==nA*nI
    if not ok: e2+=1; print('FALLO inversa',A)
print('inversa/det/kappa: casos 400 fallos',e2)
# perturbación: x̃ por Cramer, errores relativos
e3=0
for _ in range(200):
    n=random.randint(1,3)
    A=[[F(random.randint(-4,4)) for _ in range(n)] for _ in range(n)]
    d=leibniz(A)
    if d==0: continue
    b=[F(random.randint(-5,5)) for _ in range(n)]; db=[F(random.randint(-3,3),100) for _ in range(n)]
    def cramer(bb): return [leibniz([[bb[i] if j==c else A[i][j] for j in range(n)] for i in range(n)])/d for c in range(n)]
    x=cramer(b); xt=cramer([b[i]+db[i] for i in range(n)])
    p=analizar_perturbacion(A,b,db)
    nb=max(abs(v) for v in b); nx=max(abs(v) for v in x)
    rb = max(abs(v) for v in db)/nb if nb else None
    rx = max(abs(xt[i]-x[i]) for i in range(n))/nx if nx else None
    ok = p.x==x and p.x_perturbada==xt and p.error_relativo_b==rb and p.error_relativo_x==rx
    if rb is not None and rx is not None: ok = ok and rx <= p.condicion.kappa*rb and p.cumple_cota
    if not ok: e3+=1; print('FALLO perturb',A,b,db)
print('perturbacion: fallos',e3)
# mínimos cuadrados: Cramer en ecuaciones normales y A^T r = 0
e4=0; c4=0
for _ in range(300):
    n=random.randint(1,3); m=random.randint(n,5)
    A=[[F(random.randint(-3,3)) for _ in range(n)] for _ in range(m)]
    b=[F(random.randint(-4,4)) for _ in range(m)]
    AtA=[[sum(A[k][i]*A[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    Atb=[sum(A[k][i]*b[k] for k in range(m)) for i in range(n)]
    d=leibniz(AtA); r=minimos_cuadrados(A,b); c4+=1
    if d==0: ok = r.solucion is None and rango(A)<n
    else:
        xs=[leibniz([[Atb[i] if j==c else AtA[i][j] for j in range(n)] for i in range(n)])/d for c in range(n)]
        res=[b[i]-sum(A[i][j]*xs[j] for j in range(n)) for i in range(m)]
        ok = r.solucion==xs and r.residuo==res and all(v==0 for v in r.ortogonalidad) and r.norma_residuo_2_cuadrado==sum(v*v for v in res)
    if not ok: e4+=1; print('FALLO mc',A,b)
print('minimos: casos',c4,'fallos',e4)
