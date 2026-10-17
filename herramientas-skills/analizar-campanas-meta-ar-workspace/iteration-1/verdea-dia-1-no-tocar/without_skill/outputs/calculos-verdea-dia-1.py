import math
ads = [
 ("Lucía 1 · Esquejes podridos", 1402, 1690, 7402.18, 34, 0),
 ("Lucía 2 · Semanas sin raíz", 1215, 1448, 6950.40, 6, 0),
 ("Marta 1 · Golpe de trasplante", 1380, 1612, 7120.95, 27, 1),
 ("Marta 2 · Planta del vivero", 1290, 1530, 6890.02, 23, 0),
]
# calculadora preset verdea
costo, empaque, envio = 8000, 800, 7500
pct = (7+8+2+4+3)/100
packs = {1:58000, 2:81200, 3:113100}
cpa_eq = {}
for n,p in packs.items():
    env = envio if n >= 3 else 0
    costos = costo*n + empaque + env + p*pct
    m = p - costos
    cpa_eq[n] = m
    print(f"x{n}: precio {p} costos {costos:.0f} margen {m:.0f} ({m/p*100:.0f}%) ROAS eq {p/m:.2f}")
tot_sp = sum(a[3] for a in ads); tot_imp = sum(a[2] for a in ads); tot_cl = sum(a[4] for a in ads)
print("total gasto", round(tot_sp,2), "imp", tot_imp, "clics", tot_cl, "CTR", round(tot_cl/tot_imp*100,2), "CPC", round(tot_sp/tot_cl,2), "CPM", round(tot_sp/tot_imp*1000,0))
for name, reach, imp, sp, cl, pur in ads:
    print(f"{name}: CTR {cl/imp*100:.2f}% CPC {sp/cl:.0f} CPM {sp/imp*1000:.0f} freq {imp/reach:.2f} %CPAeq_x1 {sp/cpa_eq[1]*100:.0f}% %CPAeq_x2 {sp/cpa_eq[2]*100:.0f}%")
# Lucia 2 vs others
oth_cl = 34+27+23; oth_imp = 1690+1612+1530
r = oth_cl/oth_imp
lam = r*1448
p = sum(math.exp(-lam)*lam**k/math.factorial(k) for k in range(0,7))
print("CTR otros", round(r*100,2), "clics esperados L2", round(lam,1), "P(<=6)", p)
# CVR needed for CPA eq at each CPC
for name, reach, imp, sp, cl, pur in ads:
    cpc = sp/cl
    print(f"{name}: clics por venta para CPA eq x1 = {cpa_eq[1]/cpc:.0f} -> CVR minima {cpc/cpa_eq[1]*100:.2f}% | x2 {cpc/cpa_eq[2]*100:.2f}%")
# Days to reach CPA eq at ~7000/day
for k in (1,1.5):
    print(f"{k}x CPA eq x1 = {k*cpa_eq[1]:.0f} -> dias a ~7100/dia: {k*cpa_eq[1]/7100:.1f}")
print("gasto 4 dias aprox total", 4*tot_sp)
