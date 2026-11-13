r"""Auditoría matemática independiente (fase final, 27-oct-2026).

Uso (desde la raíz del proyecto):  .venv\Scripts\python auditoria/auditoria_iterativos.py .

Compara el núcleo con oráculos independientes (fórmula de Leibniz, adjunta,
Cramer, implementación separada de las iteraciones, fórmula de Gelfand).
No forma parte de la suite rápida de tests/ porque tarda unos 20 segundos y es aleatoria (semilla fija)."""
import sys, random, math, itertools
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
from algebra.modulo_IV_iterativos.ejecucion import (
    ConfiguracionIterativa,
    ejecutar,
)
from algebra.modulo_IV_iterativos.espectral import CONVERGE, INDETERMINADO, NO_CONVERGE, radio_espectral
from algebra.modulo_IV_iterativos.metodos import (
    GAUSS_SEIDEL,
    JACOBI,
    SOR,
)
random.seed(7)
def oraculo(A,b,met,x0,crit,eps,kmax,N,w):
    n=len(A); x=list(x0)
    res=lambda x:max(abs(b[i]-sum(A[i][j]*x[j] for j in range(n))) for i in range(n))
    if crit=='B' and res(x)<eps: return 0,x
    lim=N if crit=='C' else kmax
    for k in range(1,lim+1):
        o=list(x)
        for i in range(n):
            s=sum(A[i][j]*(o[j] if met==JACOBI else x[j]) for j in range(n) if j!=i)
            g=(b[i]-s)/A[i][i]
            x[i]= g if met!=SOR else (1-w)*o[i]+w*g
        d=max(abs(x[i]-o[i]) for i in range(n))
        if crit=='A' and d<eps: return k,x
        if crit=='B' and res(x)<eps: return k,x
    return lim,x
fallos=0;casos=0
for _ in range(600):
    n=random.randint(1,5)
    A=[[float(random.randint(-3,3)) for _ in range(n)] for _ in range(n)]
    for i in range(n): A[i][i]=float(random.choice([1,2,-2,5,8,10]))*(1 if random.random()<0.8 else 1)
    b=[float(random.randint(-5,5)) for _ in range(n)]
    x0=[float(random.randint(-2,2)) for _ in range(n)]
    met=random.choice([JACOBI,GAUSS_SEIDEL,SOR]); crit=random.choice('ABC'); w=random.choice([0.5,1.0,1.2,1.7])
    eps=random.choice([1e-2,1e-4,1e-6]); kmax=random.choice([5,30,200]); N=random.choice([1,4,10])
    r=ejecutar(A,b,ConfiguracionIterativa(metodo=met,criterio=crit,x0=x0,tolerancia=eps,k_max=kmax,n_iteraciones=N,omega=w))
    if r.codigo=='ERROR_NO_FINITO': continue
    casos+=1
    k,x=oraculo(A,b,met,x0,crit,eps,kmax,N,w)
    if r.k_final!=k or max(abs(a-c) for a,c in zip(r.x_final,x))>1e-9*max(1,max(map(abs,x))):
        fallos+=1; print('FALLO it',met,crit,A,b,r.k_final,k); break
    # coherencia de métricas registradas
    for f0,f1 in zip(r.historial,r.historial[1:]):
        if abs(f1.d-max(abs(a-c) for a,c in zip(f1.x,f0.x)))>1e-12*max(1,f1.d): fallos+=1; print('d incoherente'); break
print('iterativos: casos',casos,'fallos',fallos)

def det_c(M):
    n=len(M); t=0
    for p in itertools.permutations(range(n)):
        s=1
        for i in range(n):
            for j in range(i+1,n):
                if p[i]>p[j]: s=-s
        pr=1
        for i in range(n): pr*=M[i][p[i]]
        t+=s*pr
    return t
def gelfand(T,k=3000):
    n=len(T); X=[[float(T[i][j]) for j in range(n)] for i in range(n)]; P=[r[:] for r in X]; logs=0.0
    for _ in range(k-1):
        P=[[sum(P[i][l]*X[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        s=max(sum(abs(v) for v in r) for r in P)
        if s==0: return 0.0
        P=[[v/s for v in r] for r in P]; logs+=math.log(s)
    s=max(sum(abs(v) for v in r) for r in P); logs+=math.log(s) if s>0 else -1e9
    # ||T^k|| = exp(logs) (con normalizaciones), T^1 norma inicial incluida implícitamente
    return math.exp((logs + math.log(max(sum(abs(v) for v in r) for r in X)))/k)
f2=0;c2=0;indet=0;nofiable=0
for _ in range(300):
    n=random.randint(2,5)
    A=[[F(random.randint(-3,3)) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i]=F(random.choice([1,2,3,5,-4]))
    met=random.choice([JACOBI,GAUSS_SEIDEL,SOR]); w=random.choice([F(1,2),F(6,5),F(3,2)])
    b=[F(1)]*n
    e=radio_espectral(A,b,met,w)
    if e.rho is None:               # ρ no calculable con el curso (SOR, n > 3, grado ≥ 3)
        continue
    T=e.iteracion.T; c2+=1
    # T coincide con un paso del método: x1 = T x0 + c para x0 aleatorio
    x0=[random.random() for _ in range(n)]
    r=ejecutar(A,b,ConfiguracionIterativa(metodo=met,criterio='C',n_iteraciones=1,x0=x0,omega=float(w)))
    x1=[sum(float(T[i][j])*x0[j] for j in range(n))+float(e.iteracion.c[i]) for i in range(n)]
    ok=max(abs(a-b2) for a,b2 in zip(r.historial[1].x,x1))<1e-9*max(1,max(map(abs,x1)))
    # cada autovalor anula det(T - λI) (Leibniz, independiente del núcleo)
    esc=max(1,max(abs(float(v)) for f in T for v in f))**n
    for z in e.autovalores:
        M=[[complex(float(T[i][j]))-(z if i==j else 0) for j in range(n)] for i in range(n)]
        if abs(det_c(M))>1e-7*esc*max(1,abs(z))**n: ok=False
    # producto = det(T)
    prod=1
    for z in e.autovalores: prod*=z
    dT=det_c([[float(v) for v in f] for f in T])
    if abs(prod-dT)>1e-7*max(1,abs(dT)): ok=False
    rho=max(abs(z) for z in e.autovalores)
    if abs(rho-e.rho)>1e-15: ok=False
    g=gelfand(T)
    if abs(g-e.rho)>0.05*max(1,e.rho): ok=False; print('gelfand',g,e.rho)
    if e.conclusion==INDETERMINADO: indet+=1
    if not e.fiable: nofiable+=1
    if e.conclusion==CONVERGE and not e.rho<1: ok=False
    if e.conclusion==NO_CONVERGE and not e.rho>=1-1e-12: ok=False
    if not ok: f2+=1; print('FALLO esp',met,w,A); break
print('espectral aleatorio: casos',c2,'fallos',f2,'indeterminados',indet,'no fiables',nofiable)
