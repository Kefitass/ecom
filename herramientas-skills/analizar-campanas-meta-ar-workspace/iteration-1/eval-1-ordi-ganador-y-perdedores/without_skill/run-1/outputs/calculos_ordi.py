"""Calculos auxiliares para el analisis de la campana ORDI (4 dias).
Uso: python3 -I calculos_ordi.py <ruta_csv>
Margenes con la formula de herramientas/calculadora-rentabilidad.html (preset ORDI).
"""
import csv, sys, itertools, json

PRECIO = {1: 34900, 2: 59900, 3: 79900}
PCT = (7 + 8 + 2 + 4 + 3) / 100  # pasarela, cuotas, plataforma, impuestos, devoluciones
EMPAQUE, ENVIO_GRATIS, GRATIS_DESDE = 1000, 8000, 3

def margen(n, costo):
    envio = ENVIO_GRATIS if n >= GRATIS_DESDE else 0
    return PRECIO[n] - (costo * n + EMPAQUE + envio + PRECIO[n] * PCT)

def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0

def mezcla(valor, compras):
    """Combinaciones de packs (x1, x2, x3) que suman el valor de conversion."""
    sols = []
    for a in range(compras + 1):
        for b in range(compras + 1 - a):
            c = compras - a - b
            if a * PRECIO[1] + b * PRECIO[2] + c * PRECIO[3] == round(valor):
                sols.append((a, b, c))
    return sols

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
K = {k: k for k in rows[0].keys()}
col = lambda name: next(k for k in rows[0].keys() if k.startswith(name))
c_gasto, c_imp, c_alc = col("Importe gastado"), col("Impresiones"), col("Alcance")
c_clics, c_3s, c_thru = col("Clics en el enlace"), col("Reproducciones de video de 3"), col("ThruPlays")
c_lpv, c_atc, c_ic = col("Visitas a la p"), col("Artículos agregados"), col("Pagos iniciados")
c_comp, c_valor = col("Compras"), col("Valor de conversión")

print("Margen por pedido (costo $12.000):", {n: round(margen(n, 12000)) for n in (1, 2, 3)})
tot = {}
res = []
for r in rows:
    g, imp, cl = f(r[c_gasto]), f(r[c_imp]), f(r[c_clics])
    s3, th, lpv, atc, ic = f(r[c_3s]), f(r[c_thru]), f(r[c_lpv]), f(r[c_atc]), f(r[c_ic])
    comp, val = int(f(r[c_comp])), f(r[c_valor])
    mix = mezcla(val, comp) if comp else [(0, 0, 0)]
    a, b, c = mix[0]
    out = {
        "anuncio": r["Nombre del anuncio"], "conjunto": r["Nombre del conjunto de anuncios"],
        "gasto": g, "compras": comp, "valor": val,
        "cpa": round(g / comp) if comp else None, "roas": round(val / g, 2) if g else None,
        "ticket": round(val / comp) if comp else None, "mezcla_x1_x2_x3": mix,
        "ctr_%": round(cl / imp * 100, 2), "cpc": round(g / cl), "cpm": round(g / imp * 1000),
        "hook_3s_%": round(s3 / imp * 100, 1), "thruplay/3s_%": round(th / s3 * 100, 1),
        "lpv/clic_%": round(lpv / cl * 100, 1), "costo_lpv": round(g / lpv),
        "atc/lpv_%": round(atc / lpv * 100, 1), "ic/atc_%": round(ic / atc * 100, 1) if atc else None,
        "compra/lpv_%": round(comp / lpv * 100, 2), "costo_atc": round(g / atc) if atc else None,
    }
    for costo in (10000, 12000, 13000, 15000):
        m = a * margen(1, costo) + b * margen(2, costo) + c * margen(3, costo)
        out[f"ganancia_costo_{costo}"] = round(m - g)
    # costo por set con el que el anuncio queda en cero
    if comp:
        lo, hi = 0, 40000
        for _ in range(60):
            mid = (lo + hi) / 2
            m = a * margen(1, mid) + b * margen(2, mid) + c * margen(3, mid)
            lo, hi = (mid, hi) if m - g > 0 else (lo, mid)
        out["costo_set_equilibrio"] = round(lo)
        m12 = a * margen(1, 12000) + b * margen(2, 12000) + c * margen(3, 12000)
        out["cpa_equilibrio_mezcla_12000"] = round(m12 / comp)
        out["roas_equilibrio_mezcla_12000"] = round(val / m12, 2)
    res.append(out)
    for k in ("gasto", "compras", "valor"):
        tot[k] = tot.get(k, 0) + out[k]
    for k in ("ganancia_costo_10000", "ganancia_costo_12000", "ganancia_costo_13000", "ganancia_costo_15000"):
        tot[k] = tot.get(k, 0) + out[k]
    for k, v in (("lpv", lpv), ("atc", atc), ("ic", ic), ("clics", cl), ("imp", imp)):
        tot[k] = tot.get(k, 0) + v

for o in res:
    print(json.dumps(o, ensure_ascii=False))
tot["cpa"] = round(tot["gasto"] / tot["compras"])
tot["roas"] = round(tot["valor"] / tot["gasto"], 2)
tot["ticket"] = round(tot["valor"] / tot["compras"])
print("TOTAL", json.dumps(tot, ensure_ascii=False))

# por conjunto
conj = {}
for o in res:
    d = conj.setdefault(o["conjunto"], {"gasto": 0, "compras": 0, "valor": 0})
    d["gasto"] += o["gasto"]; d["compras"] += o["compras"]; d["valor"] += o["valor"]
for k, d in conj.items():
    d["cpa"] = round(d["gasto"] / d["compras"]) if d["compras"] else None
    d["roas"] = round(d["valor"] / d["gasto"], 2)
    print("CONJUNTO", k, json.dumps(d, ensure_ascii=False))

# equilibrio de la campana segun costo por set (mezcla real de packs)
win = [o for o in res if o["compras"]]
def gan_total(costo):
    s = -sum(o["gasto"] for o in res)
    for o in win:
        a, b, c = o["mezcla_x1_x2_x3"][0]
        s += a * margen(1, costo) + b * margen(2, costo) + c * margen(3, costo)
    return s
lo, hi = 0, 40000
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if gan_total(mid) > 0 else (lo, mid)
print("Costo por set de equilibrio de toda la campana:", round(lo))
# margen promedio por pedido con la mezcla real
m_tot = sum(o["gasto"] + o["ganancia_costo_12000"] for o in win)
print("Margen total (costo 12000):", round(m_tot), "| CPA equilibrio mezcla:", round(m_tot / tot["compras"]),
      "| ROAS equilibrio mezcla:", round(tot["valor"] / m_tot, 2))
# solo los dos que quedan
g2 = sum(o["gasto"] for o in win); print("Ganadores: gasto", g2, "ganancia (12000)", sum(o["ganancia_costo_12000"] for o in win))
