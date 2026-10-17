#!/usr/bin/env python3
"""Economía unitaria de un producto para vender en Argentina con anuncios.

Uso mínimo:
    python economia.py --costo 9000 --precio 29900

Con packs y porcentajes propios:
    python economia.py --costo 9000 --precio 29900 --pack 2:49900 --pack 3:64900 \
        --envio 7500 --pasarela 0.07 --cuotas 0.08 --plataforma 0.02 --impuestos 0.04

Todos los porcentajes van como fracción (0.07 = 7%). Los valores por defecto son
referencias a verificar (ver references/costos-ar.md).
"""
import argparse


def fmt(x):
    return "$" + f"{x:,.0f}".replace(",", ".")


def calcular(precio, unidades, a):
    pct = a.pasarela + a.cuotas + a.plataforma + a.impuestos + a.devoluciones
    variables = a.costo * unidades + a.envio + a.empaque + precio * pct
    margen = precio - variables
    return {
        "precio": precio,
        "unidades": unidades,
        "costos": variables,
        "margen": margen,
        "margen_pct": margen / precio if precio else 0,
        "cpa": margen,
        "roas": (precio / margen) if margen > 0 else float("inf"),
        "multiplo": precio / (a.costo * unidades) if a.costo else 0,
    }


def precio_para_margen(a, objetivo, unidades=1):
    pct = a.pasarela + a.cuotas + a.plataforma + a.impuestos + a.devoluciones
    denom = 1 - pct - objetivo
    if denom <= 0:
        return None
    return (a.costo * unidades + a.envio + a.empaque) / denom


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--costo", type=float, required=True, help="Costo por unidad puesto (ARS)")
    p.add_argument("--precio", type=float, help="Precio de venta de 1 unidad (ARS)")
    p.add_argument("--pack", action="append", default=[], help="Pack como unidades:precio, ej 2:49900")
    p.add_argument("--envio", type=float, default=7500, help="Envío absorbido por pedido (0 si lo paga el cliente)")
    p.add_argument("--empaque", type=float, default=1000)
    p.add_argument("--pasarela", type=float, default=0.07)
    p.add_argument("--cuotas", type=float, default=0.08)
    p.add_argument("--plataforma", type=float, default=0.02)
    p.add_argument("--impuestos", type=float, default=0.04)
    p.add_argument("--devoluciones", type=float, default=0.03)
    a = p.parse_args()

    filas = []
    if a.precio:
        filas.append(calcular(a.precio, 1, a))
    for pk in a.pack:
        u, pr = pk.split(":")
        filas.append(calcular(float(pr), int(u), a))

    pct_total = a.pasarela + a.cuotas + a.plataforma + a.impuestos + a.devoluciones
    print(f"Supuestos: envío {fmt(a.envio)} · empaque {fmt(a.empaque)} · "
          f"porcentajes sobre el precio {pct_total*100:.1f}% "
          f"(pasarela {a.pasarela*100:.0f}%, cuotas {a.cuotas*100:.0f}%, plataforma {a.plataforma*100:.0f}%, "
          f"impuestos {a.impuestos*100:.0f}%, devoluciones {a.devoluciones*100:.0f}%)\n")

    if filas:
        print("| Oferta | Precio | Costos variables | Margen (antes de anuncios) | CPA equilibrio | ROAS equilibrio | Precio / costo producto |")
        print("|---|---|---|---|---|---|---|")
        for f in filas:
            roas = "no cierra" if f["margen"] <= 0 else f"{f['roas']:.2f}"
            print(f"| x{f['unidades']} | {fmt(f['precio'])} | {fmt(f['costos'])} | {fmt(f['margen'])} ({f['margen_pct']*100:.0f}%) "
                  f"| {fmt(max(f['cpa'], 0))} | {roas} | {f['multiplo']:.1f}x |")
        print()

    print("Precio sugerido para 1 unidad según margen objetivo (antes de anuncios):")
    for obj in (0.30, 0.35, 0.40, 0.45):
        pr = precio_para_margen(a, obj)
        print(f"  {int(obj*100)}% → {fmt(pr) if pr else 'imposible con estos porcentajes'}")
    print(f"\nReferencia: 3x el costo del producto = {fmt(a.costo*3)} · 2,5x = {fmt(a.costo*2.5)}")


if __name__ == "__main__":
    main()
