#!/usr/bin/env python3
"""Diagnóstico de campañas de Meta Ads para un ecommerce en Argentina (pesos).

Lee el export del Administrador de anuncios (CSV o Excel, columnas en español o en inglés,
números con coma o punto decimal), suma por anuncio, calcula las métricas, compara contra el
CPA de equilibrio del producto, aplica las reglas de decisión e imprime tablas en markdown
(o JSON con --json).

Ejemplos:
  python metricas.py export.csv --cpa-equilibrio 13500
  python metricas.py export.xlsx --costo 12000 --packs 1:34900,2:59900,3:79900 --envio 8000 --envio-gratis-desde 3
  python metricas.py export.csv --precio 58000 --costo 9000 --shopify-ventas 7
  python metricas.py export.csv --cpa-equilibrio 20000 --recargo-anuncios 0.21   # IVA del gasto en anuncios
  python metricas.py captura.csv --cpa-equilibrio 35000 --dias 1                 # captura pasada a CSV

Los porcentajes van como fracción (0.07 = 7%). Los valores por defecto de comisiones son los
mismos de validar-producto-ar (verificarlos: cambian seguido).
"""
import argparse
import csv
import io
import json
import math
import re
import sys
import unicodedata
from datetime import datetime

# ---------------------------------------------------------------- referencias orientativas
REF = {
    "ctr_flojo": 0.008,      # CTR del enlace por debajo de 0,8% = el anuncio no engancha
    "ctr_muerto": 0.005,     # por debajo de 0,5% con 2.000+ impresiones = se puede cortar antes
    "ctr_bueno": 0.015,
    "gancho_flojo": 0.25,    # reproducciones de 3 s / impresiones
    "gancho_bueno": 0.35,
    "retencion_floja": 0.12, # ThruPlays / reproducciones de 3 s
    "llegada_floja": 0.70,   # visitas a la página / clics en el enlace
    "carrito_flojo": 0.04,   # carritos / visitas (o / clics si no hay visitas)
    "pago_flojo": 0.40,      # pagos iniciados / carritos
    "compra_floja": 0.40,    # compras / pagos iniciados
    "frecuencia_alta": 2.5,  # en 7 días, públicos fríos
}

# ---------------------------------------------------------------- columnas (español / inglés)
COLS = [
    ("fecha_inicio", [r"^inicio del informe", r"^reporting starts", r"^dia$", r"^day$", r"^fecha$", r"^date$"]),
    ("fecha_fin", [r"^fin del informe", r"^reporting ends"]),
    ("campana", [r"^nombre de la campana", r"^campaign name", r"^campana$", r"^campaign$"]),
    ("conjunto", [r"^nombre del conjunto de anuncios", r"^ad set name", r"^conjunto de anuncios$", r"^ad set$"]),
    ("anuncio", [r"^nombre del anuncio", r"^ad name", r"^anuncio$", r"^ad$"]),
    ("gasto", [r"^importe gastado", r"^amount spent", r"^gasto", r"^spend"]),
    ("impresiones", [r"^impresiones$", r"^impressions$"]),
    ("alcance", [r"^alcance$", r"^reach$"]),
    ("frecuencia", [r"^frecuencia$", r"^frequency$"]),
    ("clics", [r"^clics en el enlace$", r"^link clicks$", r"^clics en enlaces$"]),
    ("ctr_meta", [r"^ctr.*(enlace|link)"]),
    ("cpc_meta", [r"^cpc.*(enlace|link)"]),
    ("cpm_meta", [r"^cpm"]),
    ("rep3s", [r"reproducciones de video de 3 segundos", r"^3.second video plays", r"^reproducciones de 3 segundos"]),
    ("thruplays", [r"^thruplays?$"]),
    ("visitas", [r"^visitas a la pagina de destino", r"^(website )?landing page views$"]),
    ("carritos", [r"^(articulos )?agregados al carrito( en el sitio web)?$", r"^(website )?adds? to cart$"]),
    ("pagos", [r"^pagos iniciados( en el sitio web)?$", r"^(website )?checkouts initiated$"]),
    ("compras", [r"^compras( en el sitio web)?$", r"^(website )?purchases$"]),
    ("valor", [r"^valor de (la )?conversion de (las )?compras", r"^valor de (las )?compras",
               r"^(website )?purchases? conversion value"]),
]
SUMABLES = ["gasto", "impresiones", "alcance", "clics", "rep3s", "thruplays", "visitas", "carritos", "pagos", "compras", "valor"]


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\((ars|usd|\$|ars \$)\)", "", s)
    return re.sub(r"\s+", " ", s).strip()


def mapear_columnas(headers):
    mapa, usados = {}, set()
    for key, pats in COLS:
        for i, h in enumerate(headers):
            if i in usados:
                continue
            if any(re.search(p, norm(h)) for p in pats):
                mapa[key] = i
                usados.add(i)
                break
    return mapa


# ---------------------------------------------------------------- números
def detectar_formato(celdas):
    """'ar' (1.234,56) o 'us' (1,234.56) mirando cómo terminan los decimales."""
    ar = us = 0
    for c in celdas:
        if not isinstance(c, str):
            continue
        t = c.strip().replace("%", "").replace("$", "").strip()
        if re.fullmatch(r"-?[\d.]*\d,\d{1,2}", t):
            ar += 1
        elif re.fullmatch(r"-?[\d,]*\d\.\d{1,2}", t):
            us += 1
        elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", t):
            ar += 0.5
        elif re.fullmatch(r"-?\d{1,3}(,\d{3})+", t):
            us += 0.5
    return "ar" if ar > us else "us"


def num(v, formato="us", pct=False):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        if isinstance(v, float) and math.isnan(v):
            return None
        return float(v)
    t = str(v).strip().replace("\xa0", "").replace(" ", "")
    es_pct = t.endswith("%")
    t = re.sub(r"(ARS|US\$|USD|\$|%)", "", t, flags=re.I)
    if t in ("", "-", "—", "–", "n/a", "N/A", "None"):
        return None
    if formato == "ar":
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "")
    try:
        x = float(t)
    except ValueError:
        return None
    return x / 100 if (es_pct or pct) else x


# ---------------------------------------------------------------- lectura
def leer_tabla(ruta):
    if ruta.lower().endswith((".xlsx", ".xlsm")):
        try:
            import openpyxl
        except ImportError:
            sys.exit("Para leer Excel hace falta openpyxl (pip install openpyxl) o exportá en CSV.")
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        filas = [list(r) for r in wb.worksheets[0].iter_rows(values_only=True)]
    else:
        raw = open(ruta, "rb").read()
        if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
            texto = raw.decode("utf-16")
        else:
            for enc in ("utf-8-sig", "latin-1"):
                try:
                    texto = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
        muestra = texto[:4096]
        delim = max([",", ";", "\t"], key=lambda d: muestra.split("\n")[0].count(d))
        filas = list(csv.reader(io.StringIO(texto), delimiter=delim))
    # la fila de encabezados es la primera que tenga al menos 3 columnas conocidas
    for i, fila in enumerate(filas[:15]):
        if len(mapear_columnas([str(c or "") for c in fila])) >= 3:
            return [str(c or "") for c in fila], filas[i + 1:]
    sys.exit("No encontré los encabezados del export de Meta (nombre del anuncio, importe gastado, impresiones…).")


def a_fecha(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if hasattr(v, "isoformat") and not isinstance(v, str):
        return v
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(v).strip()[:10], f).date()
        except ValueError:
            continue
    return None


def tendencia(por_dia):
    """Primera mitad de los días contra la segunda: (cpm1, cpm2, ctr1, ctr2), o None con menos de 3 días."""
    fechas = sorted(por_dia)
    if len(fechas) < 3:
        return None
    mitad = len(fechas) // 2
    a = [sum(por_dia[f][i] for f in fechas[:mitad]) for i in range(3)]
    b = [sum(por_dia[f][i] for f in fechas[-mitad:]) for i in range(3)]
    if not (a[1] and b[1]):
        return None
    return a[0] * 1000 / a[1], b[0] * 1000 / b[1], a[2] / a[1], b[2] / b[1]


def cargar(ruta, nivel):
    headers, filas = leer_tabla(ruta)
    mapa = mapear_columnas(headers)
    avisos = []
    if "gasto" not in mapa:
        sys.exit("No encontré la columna de gasto (Importe gastado / Amount spent).")
    if "compras" not in mapa:
        for i, h in enumerate(headers):
            if re.search(r"^(resultados|results)$", norm(h)) and i not in mapa.values():
                mapa["compras"] = i
                avisos.append("No hay columna de compras: usé 'Resultados'. Verificá que el objetivo de la campaña sea Ventas (compras).")
                break
    faltan = [k for k in ("gasto", "impresiones", "clics", "carritos", "compras", "valor") if k not in mapa]
    moneda = "USD" if re.search(r"usd|us\$|u\$s", headers[mapa["gasto"]].lower()) else "ARS"
    celdas = [c for f in filas for c in f]
    formato = detectar_formato(celdas)
    clave_nivel = nivel
    if clave_nivel not in mapa:
        for alt in ("anuncio", "conjunto", "campana"):
            if alt in mapa:
                clave_nivel = alt
                break
    grupos, orden, filas_por_grupo, por_dia = {}, [], {}, {}
    fechas = []
    for f in filas:
        if not any(str(c or "").strip() for c in f):
            continue
        g = lambda k: f[mapa[k]] if k in mapa and mapa[k] < len(f) else None
        nombre = str(g(clave_nivel) or "").strip()
        n = norm(nombre)
        if not nombre or n.startswith(("total", "resultados de", "results from", "results of")):
            continue
        key = nombre
        if clave_nivel == "anuncio" and "conjunto" in mapa and str(g("conjunto") or "").strip():
            key = str(g("conjunto")).strip() + " › " + nombre
        if key not in grupos:
            grupos[key] = {k: 0.0 for k in SUMABLES}
            grupos[key].update(nombre=nombre, conjunto=str(g("conjunto") or "").strip(),
                               campana=str(g("campana") or "").strip(), frecuencia=None, tendencia=None)
            orden.append(key)
            filas_por_grupo[key] = 0
        filas_por_grupo[key] += 1
        for k in SUMABLES:
            x = num(g(k), formato)
            if x is not None:
                grupos[key][k] += x
        fr = num(g("frecuencia"), formato)
        if fr is not None:
            grupos[key]["frecuencia"] = fr
        d0 = a_fecha(g("fecha_inicio"))
        for d in (d0, a_fecha(g("fecha_fin"))):
            if d:
                fechas.append(d)
        if d0:
            dia = por_dia.setdefault(key, {}).setdefault(d0, [0.0, 0.0, 0.0])
            dia[0] += num(g("gasto"), formato) or 0
            dia[1] += num(g("impresiones"), formato) or 0
            dia[2] += num(g("clics"), formato) or 0
    desglosado = any(v > 1 for v in filas_por_grupo.values())
    total_dia = {}
    for key in orden:
        r = grupos[key]
        if desglosado or r["frecuencia"] is None:
            r["frecuencia"] = (r["impresiones"] / r["alcance"]) if r["alcance"] else None
        if desglosado and key in por_dia:
            r["tendencia"] = tendencia(por_dia[key])
            for d, v in por_dia[key].items():
                t = total_dia.setdefault(d, [0.0, 0.0, 0.0])
                for i in range(3):
                    t[i] += v[i]
    info = {
        "columnas_encontradas": sorted(mapa.keys()),
        "columnas_faltantes": faltan,
        "formato_numeros": "1.234,56" if formato == "ar" else "1,234.56",
        "moneda": moneda,
        "desglose_por_dia": desglosado,
        "nivel": clave_nivel,
        "desde": min(fechas).isoformat() if fechas else None,
        "hasta": max(fechas).isoformat() if fechas else None,
        "dias": ((max(fechas) - min(fechas)).days + 1) if fechas else None,
        "tiene_video": "rep3s" in mapa,
        "tiene_visitas": "visitas" in mapa,
        "tendencia_total": tendencia(total_dia) if desglosado else None,
        "avisos": avisos,
    }
    return [grupos[k] for k in orden], info, set(mapa)


# ---------------------------------------------------------------- economía
def margen_pack(n, precio, a):
    pct_total = a.pasarela + a.cuotas + a.plataforma + a.impuestos + a.devoluciones
    envio = a.envio if (a.envio_gratis_desde is not None and n >= a.envio_gratis_desde) else 0
    return precio - (a.costo * n + envio + a.empaque + precio * pct_total)


def puntos_equilibrio(a):
    packs = []
    if a.packs:
        for p in a.packs.split(","):
            n, pr = p.split(":")
            packs.append((int(n), float(pr)))
    elif a.precio:
        packs.append((1, a.precio))
    return [(pr, margen_pack(n, pr, a), n) for n, pr in sorted(packs, key=lambda x: x[1])]


def cpa_eq_para(ticket, puntos):
    """Interpola el margen (= CPA de equilibrio) según el ticket promedio real."""
    if not puntos:
        return None
    if ticket is None:
        return min(m for _, m, _ in puntos)  # sin ventas: el pack con menos margen (conservador)
    if ticket <= puntos[0][0]:
        return puntos[0][1]
    if ticket >= puntos[-1][0]:
        return puntos[-1][1]
    for (p1, m1, _), (p2, m2, _) in zip(puntos, puntos[1:]):
        if p1 <= ticket <= p2:
            return m1 + (ticket - p1) / (p2 - p1) * (m2 - m1)


# ---------------------------------------------------------------- métricas y reglas
def div(a, b):
    return (a / b) if (a is not None and b) else None


def metricas(r, recargo, cols):
    gasto = r["gasto"] * (1 + recargo)
    m = dict(r)
    m["gasto_real"] = gasto
    m["cpm"] = div(gasto * 1000, r["impresiones"])
    m["ctr"] = div(r["clics"], r["impresiones"]) if "clics" in cols else None
    m["cpc"] = div(gasto, r["clics"]) if "clics" in cols else None
    m["gancho"] = div(r["rep3s"], r["impresiones"]) if r["rep3s"] else None
    m["retencion"] = div(r["thruplays"], r["rep3s"]) if r["rep3s"] and "thruplays" in cols else None
    m["llegada"] = div(r["visitas"], r["clics"]) if r["visitas"] else None
    base_carrito = r["visitas"] or r["clics"]
    m["tasa_carrito"] = div(r["carritos"], base_carrito) if "carritos" in cols else None
    m["tasa_pago"] = div(r["pagos"], r["carritos"]) if {"pagos", "carritos"} <= cols else None
    m["tasa_compra"] = div(r["compras"], r["pagos"]) if ("pagos" in cols and r["pagos"]) else None
    m["cpa"] = div(gasto, r["compras"])
    m["roas"] = div(r["valor"], gasto) if "valor" in cols else None
    m["ticket"] = div(r["valor"], r["compras"]) if "valor" in cols else None
    return m


def decidir(m, E, ctx):
    """Devuelve (decisión, motivo, notas). ctx: cols, medicion_rota, fuga_grave, prom (toda la cuenta), n, dias."""
    notas = []
    cols, prom = ctx["cols"], ctx["prom"]
    ctr, imp, gasto, compras = m["ctr"], m["impresiones"], m["gasto_real"], m["compras"]
    prom_ctr = ("; promedio de la cuenta %s" % pct(prom["ctr"], 2)) if ctx["n"] > 1 and prom["ctr"] else ""
    # señales del anuncio, del embudo y del público
    if m["gancho"] is not None and m["gancho"] < REF["gancho_flojo"]:
        notas.append("gancho flojo (%s): cambiar los primeros 3 s" % pct(m["gancho"]))
    if ctr is not None and imp >= 1000:
        if ctr < REF["ctr_flojo"]:
            notas.append("CTR flojo (%s%s)" % (pct(ctr, 2), prom_ctr))
        elif ctx["n"] > 1 and prom["ctr"] and ctr < 0.7 * prom["ctr"]:
            notas.append("CTR por debajo del resto de la cuenta (%s%s)" % (pct(ctr, 2), prom_ctr))
    if m["retencion"] is not None and m["retencion"] < REF["retencion_floja"] and (m["gancho"] or 0) >= REF["gancho_flojo"]:
        notas.append("engancha pero no retiene (retención %s): el medio del video aburre" % pct(m["retencion"]))
    if (not ctx["fuga_grave"] and ctr is not None and ctr >= REF["ctr_flojo"] and m["clics"] >= 80
            and m["tasa_carrito"] is not None and m["tasa_carrito"] < REF["carrito_flojo"]):
        notas.append("muchos clics y pocos carritos (%s): revisar página u oferta" % pct(m["tasa_carrito"]))
    if not ctx["medicion_rota"] and "carritos" in cols and m["carritos"] >= 5 and compras / m["carritos"] < 0.2:
        notas.append("carritos sin compra: precio final, envío o checkout")
    if m["llegada"] is not None and m["llegada"] < REF["llegada_floja"] and m["clics"] >= 50:
        notas.append("solo llega el %s de los clics: página lenta o clics sin querer" % pct(m["llegada"]))
    if m["frecuencia"] and m["frecuencia"] > REF["frecuencia_alta"]:
        notas.append("frecuencia alta (%s): público cansado" % dec(m["frecuencia"], 1))
    t = m.get("tendencia")
    if t and (t[3] < 0.7 * t[2] or (t[1] > 1.3 * t[0] and t[3] < 0.85 * t[2])):
        notas.append("se está cansando: CPM %s → %s y CTR %s → %s del principio al final" % (pesos(t[0]), pesos(t[1]), pct(t[2], 2), pct(t[3], 2)))

    if "compras" not in cols:
        return "FALTAN DATOS", "el export no trae la columna de compras", notas
    if E is None:
        if imp >= 2000 and ctr is not None and ctr < REF["ctr_muerto"]:
            return "CORTAR", "CTR de %s con %s impresiones: el anuncio no engancha" % (pct(ctr, 2), miles(imp)), notas
        return "FALTAN DATOS", "falta el costo y el precio para saber cuánto podés pagar por venta", notas
    if E <= 0:
        return "SIN MARGEN", "con estos precios y costos cada venta pierde plata antes de pagar anuncios", notas
    if ctx["medicion_rota"]:
        return "NO DECIDIR", "Meta no está midiendo las compras: no se puede juzgar por ventas", notas
    x = gasto / E
    if ctx["fuga_grave"] and compras < 3 and ctr is not None and ctr >= REF["ctr_flojo"]:
        return "PAUSAR", "trae clics (CTR %s, CPC %s) pero la página no convierte: pausarlo, arreglar la página y reactivarlo" % (pct(ctr, 2), pesos(m["cpc"])), notas
    debil = any(n.startswith(("gancho flojo", "CTR flojo")) for n in notas)
    if compras == 0:
        if x < 1:
            if imp >= 2000 and ctr is not None and ctr < REF["ctr_muerto"]:
                return "CORTAR", "CTR de %s con %s impresiones: el anuncio no engancha" % (pct(ctr, 2), miles(imp)), notas
            if ctr is not None and ctr < REF["ctr_muerto"] and imp >= 500:
                notas.append("vigilarlo: si al pasar las 2.000 impresiones sigue con CTR menor a 0,5%, cortarlo")
            return "NO TOCAR", "gastó %s CPA de equilibrio: todavía no alcanza para decidir" % dec(x, 1), notas
        no_engancha = ctr is not None and ctr < REF["ctr_flojo"] and (m["gancho"] is None or m["gancho"] < REF["gancho_flojo"])
        if no_engancha:
            return "CORTAR", "sin ventas con %s CPA de equilibrio gastados y el anuncio no engancha (CTR %s)" % (dec(x, 1), pct(ctr, 2)), notas
        if x < 1.5:
            if debil:
                return "ITERAR", "sin ventas con %s CPA de equilibrio gastados y una parte floja: hacer una variante que cambie solo eso" % dec(x, 1), notas
            return "MANTENER", "sin ventas con %s CPA de equilibrio gastados: se decide al llegar a 1,5–2" % dec(x, 1), notas
        if x < 2 and m["pagos"] >= 2:
            return "MANTENER", "%s CPA sin ventas pero con %d pagos iniciados: darle hasta 2 CPA" % (dec(x, 1), m["pagos"]), notas
        buen_gancho = (ctr is not None and ctr >= REF["ctr_bueno"]) or (m["gancho"] is not None and m["gancho"] >= REF["gancho_bueno"])
        if buen_gancho:
            return "ITERAR", "engancha (CTR %s) pero no vende con %s CPA gastados: apagar esta versión y probar el mismo gancho con otra promesa o demostración" % (pct(ctr, 2), dec(x, 1)), notas
        return "CORTAR", "gastó %s veces el CPA de equilibrio sin ventas" % dec(x, 1), notas
    cpa = m["cpa"]
    r = cpa / E
    if compras < 3 and x < 1:
        return "NO TOCAR", "%d venta(s) con %s CPA de equilibrio gastados: prometedor, pero todavía no alcanza para decidir (no subir presupuesto)" % (compras, dec(x, 1)), notas
    if compras >= 3:
        if r <= 1:
            if ctx["dias"] is not None and ctx["dias"] < 3:
                return "MANTENER", "%d ventas con CPA %s: muy bien, pero con %s de datos conviene esperar al día 3 para escalar" % (compras, pesos(cpa), "1 día" if ctx["dias"] == 1 else "2 días"), notas
            return "ESCALAR", "%d ventas con CPA %s (%.0f%% del de equilibrio): subir 20%% por día" % (compras, pesos(cpa), r * 100), notas
        if r > 1.5:
            return "CORTAR", "%d ventas pero CPA %s, %s veces el de equilibrio" % (compras, pesos(cpa), dec(r, 1)), notas
        if debil:
            return "ITERAR", "vende pero caro (CPA %s) y el gancho es flojo: probar otros primeros 3 s con el mismo resto" % pesos(cpa), notas
        if r <= 1.2:
            return "MANTENER", "CPA %s, apenas arriba del equilibrio: no subir, mejorar" % pesos(cpa), notas
        return "ITERAR", "CPA %s (%s veces el de equilibrio): probar otro gancho u oferta" % (pesos(cpa), dec(r, 1)), notas
    if r <= 1:
        return "MANTENER", "%d venta(s) con CPA %s: prometedor, falta llegar a 3 ventas para escalar" % (compras, pesos(cpa)), notas
    if x >= 3:
        return "CORTAR", "%d venta(s) con %s CPA de equilibrio gastados" % (compras, dec(x, 1)), notas
    return "MANTENER", "vende pero caro (CPA %s): vigilar" % pesos(cpa), notas


# ---------------------------------------------------------------- formato
def pesos(x):
    return "—" if x is None else "$" + f"{x:,.0f}".replace(",", ".")


def miles(x):
    return "—" if x is None else f"{x:,.0f}".replace(",", ".")


def pct(x, d=1):
    return "—" if x is None else (f"{x * 100:.{d}f}%").replace(".", ",")


def dec(x, d=2):
    return "—" if x is None or x == float("inf") else f"{x:.{d}f}".replace(".", ",")


def lectura(etapa, T, medicion_rota):
    if medicion_rota and etapa == "Compras":
        return "la gente compra (lo dice Shopify) pero Meta no lo ve: es un problema de medición, no de los anuncios ni de la página."
    if etapa == "Clics en el enlace":
        return "el problema está en los anuncios: casi nadie hace clic. Cambiar ganchos y primeros 3 s antes de tocar la página."
    buenos = T["ctr"] is not None and T["ctr"] >= REF["ctr_flojo"]
    base = "los anuncios traen clics de sobra (CTR %s): " % pct(T["ctr"], 2) if buenos else ""
    if etapa == "Visitas a la página":
        return base + "muchos clics no llegan a ver la página: revisar velocidad y que el link funcione."
    if etapa == "Agregados al carrito":
        return base + "la gente entra y no agrega al carrito. El problema está en la página o la oferta (precio, primera pantalla, packs, confianza); cortar anuncios no lo arregla."
    if etapa == "Pagos iniciados":
        return base + "agregan al carrito pero no avanzan: algo del carrito los frena (envío, precio final, cuotas, descuento que no aparece)."
    return base + "inician el pago y no terminan: revisar medios de pago, cuotas, confianza y que el evento de compra se mida."


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("archivo", help="Export del Administrador de anuncios (.csv o .xlsx)")
    p.add_argument("--nivel", choices=["anuncio", "conjunto", "campana"], default="anuncio")
    p.add_argument("--cpa-equilibrio", type=float, help="CPA de equilibrio ya calculado (pesos)")
    p.add_argument("--costo", type=float, help="Costo por unidad puesto")
    p.add_argument("--precio", type=float, help="Precio de 1 unidad")
    p.add_argument("--packs", help="Packs como unidades:precio separados por coma, ej 1:34900,2:59900,3:79900")
    p.add_argument("--envio", type=float, default=0, help="Lo que te cuesta el envío cuando lo absorbés")
    p.add_argument("--envio-gratis-desde", type=int, default=None, help="Unidades desde las que el envío es gratis para el cliente (1 = siempre; sin este dato, lo paga el cliente)")
    p.add_argument("--empaque", type=float, default=1000)
    p.add_argument("--pasarela", type=float, default=0.07)
    p.add_argument("--cuotas", type=float, default=0.08)
    p.add_argument("--plataforma", type=float, default=0.02)
    p.add_argument("--impuestos", type=float, default=0.04)
    p.add_argument("--devoluciones", type=float, default=0.03)
    p.add_argument("--recargo-anuncios", type=float, default=0.0, help="Impuestos sobre el gasto de Meta que no recuperás (ej. 0.21 de IVA si sos monotributista)")
    p.add_argument("--tipo-cambio", type=float, help="Pesos por dólar, si la cuenta publicitaria está en USD")
    p.add_argument("--shopify-ventas", type=int, help="Pedidos en Shopify en las mismas fechas (para controlar el píxel)")
    p.add_argument("--dias", type=int, help="Días que cubre el export, si no trae fechas")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    filas, info, cols = cargar(a.archivo, a.nivel)
    dias = info["dias"] or a.dias
    alertas = list(info["avisos"])
    moneda_ok = True
    if info["moneda"] == "USD":
        if a.tipo_cambio:
            tc = a.tipo_cambio
            for r in filas:
                r["gasto"] *= tc
                r["valor"] *= tc
                if r["tendencia"]:
                    r["tendencia"] = (r["tendencia"][0] * tc, r["tendencia"][1] * tc) + r["tendencia"][2:]
            if info["tendencia_total"]:
                t = info["tendencia_total"]
                info["tendencia_total"] = (t[0] * tc, t[1] * tc) + t[2:]
            alertas.append("La cuenta está en dólares: pasé gasto y facturación a pesos a $%s por dólar [Usuario]." % miles(a.tipo_cambio))
        else:
            moneda_ok = False
            alertas.append("MONEDA: el gasto está en dólares. Pasá --tipo-cambio (pesos por dólar de tu tarjeta) para compararlo con el CPA de equilibrio en pesos.")
    ms = [metricas(r, a.recargo_anuncios, cols) for r in filas]
    tot = {k: sum(m[k] for m in ms) for k in SUMABLES}
    tot.update(nombre="TOTAL", conjunto="", campana="", frecuencia=None, tendencia=info["tendencia_total"])
    T = metricas(tot, a.recargo_anuncios, cols)
    if tot["alcance"]:
        T["frecuencia"] = tot["impresiones"] / tot["alcance"]

    # CPA de equilibrio
    puntos = []
    if a.cpa_equilibrio:
        E, fuente_E = a.cpa_equilibrio, "[Usuario]"
    elif a.costo and (a.precio or a.packs):
        puntos = puntos_equilibrio(a)
        E = cpa_eq_para(T["ticket"], puntos)
        fuente_E = "[Calculado]" + (" con el ticket promedio real" if T["ticket"] else " con el pack de menor margen (todavía no hay ventas con valor)")
    else:
        E, fuente_E = None, "falta"
    if not moneda_ok:
        E, fuente_E = None, "falta el tipo de cambio"
    roas_eq = None
    if E and E > 0:
        roas_eq = div(T["ticket"], E) if T["ticket"] else (div(puntos[0][0], puntos[0][1]) if puntos and puntos[0][1] > 0 else None)

    # control de medición
    medicion_rota = False
    if a.shopify_ventas is not None:
        sv, mv = a.shopify_ventas, tot["compras"]
        if sv > 0 and mv == 0:
            medicion_rota = True
            alertas.append("MEDICIÓN: Shopify registró %d ventas y Meta 0 compras. El píxel o la API de conversiones no está mandando el evento de compra. Arreglarlo antes de juzgar anuncios por ventas." % sv)
        elif sv > 0 and mv < 0.5 * sv:
            alertas.append("MEDICIÓN: Meta ve %d compras de %d ventas en Shopify (menos de la mitad). Revisar la API de conversiones." % (mv, sv))
        elif sv > 0 and mv > 1.3 * sv:
            alertas.append("MEDICIÓN: Meta cuenta %d compras y Shopify tiene %d ventas: posible píxel duplicado." % (mv, sv))
    elif tot["pagos"] >= 5 and tot["compras"] == 0:
        alertas.append("MEDICIÓN: hay %d pagos iniciados y 0 compras. Puede ser el checkout o el evento de compra: comparar con las ventas de Shopify." % tot["pagos"])
    if tot["compras"] > 0 and "valor" in cols and not tot["valor"]:
        alertas.append("MEDICIÓN: hay compras sin valor: el evento de compra no manda el monto.")
    if "carritos" in cols and tot["clics"] >= 200 and tot["carritos"] == 0:
        alertas.append("MEDICIÓN: %d clics y 0 carritos: revisar que el evento de agregar al carrito dispare (o la página no funciona)." % tot["clics"])
    if info["columnas_faltantes"]:
        nombres = {"gasto": "importe gastado", "impresiones": "impresiones", "clics": "clics en el enlace", "carritos": "agregados al carrito",
                   "compras": "compras", "valor": "valor de conversión de compras"}
        alertas.append("FALTAN COLUMNAS: " + ", ".join(nombres[k] for k in info["columnas_faltantes"]) + ". Ver references/exportar-informe-meta.md.")
    if info["desglose_por_dia"]:
        alertas.append("El export viene desglosado por día: sumé por anuncio (la frecuencia es aproximada).")
    if dias is not None and dias <= 2:
        alertas.append("Solo %s de datos: Meta todavía está aprendiendo y los primeros días son ruidosos. No cambies presupuestos ni apagues anuncios, salvo CTR muy bajo." % ("1 día" if dias == 1 else "%d días" % dias))
    tt = info["tendencia_total"]
    if tt and (tt[3] < 0.7 * tt[2] or (tt[1] > 1.3 * tt[0] and tt[3] < 0.85 * tt[2])):
        alertas.append("PÚBLICO: el CPM pasó de %s a %s y el CTR de %s a %s del principio al final: el público se está cansando de los anuncios." % (pesos(tt[0]), pesos(tt[1]), pct(tt[2], 2), pct(tt[3], 2)))

    # fuga en la página: los anuncios traen clics pero casi nadie agrega al carrito, y no es rentable
    fuga_pagina = (not medicion_rota and E is not None and E > 0 and tot["clics"] >= 200
                   and T["ctr"] is not None and T["ctr"] >= REF["ctr_flojo"]
                   and T["tasa_carrito"] is not None and T["tasa_carrito"] < REF["carrito_flojo"]
                   and (tot["compras"] < 3 or T["cpa"] > E))
    fuga_grave = fuga_pagina and T["gasto_real"] >= 2 * E

    n = len(ms)
    ctx = {"cols": cols, "medicion_rota": medicion_rota, "fuga_grave": fuga_grave, "prom": T, "n": n, "dias": dias}
    filas_dec = [(m,) + decidir(m, E, ctx) for m in ms]

    # CPA real con ventas de Shopify (todas las ventas atribuidas a los anuncios: es un piso)
    cpa_real_shopify = div(T["gasto_real"], a.shopify_ventas) if a.shopify_ventas else None

    # semáforo
    gasto_tot = T["gasto_real"]
    if medicion_rota:
        semaforo = "AMARILLO" if (E and E > 0 and cpa_real_shopify and cpa_real_shopify <= E) else "ROJO"
        porque = "Meta no mide las compras: primero arreglar el píxel (con las ventas de Shopify el CPA real es %s)" % pesos(cpa_real_shopify)
    elif "compras" not in cols:
        semaforo, porque = "AMARILLO", "el export no trae compras: no se puede juzgar por ventas"
    elif E is None:
        semaforo, porque = "AMARILLO", "falta el costo o el precio para saber cuánto podés pagar por venta"
    elif E <= 0:
        semaforo, porque = "ROJO", "con estos precios y costos cada venta pierde plata antes de pagar anuncios: revisar precio o costo"
    elif fuga_grave:
        semaforo, porque = "ROJO", "los anuncios traen clics (CTR %s) pero la página no convierte (solo el %s agrega al carrito): frenar y arreglar la página antes de seguir gastando" % (pct(T["ctr"], 2), pct(T["tasa_carrito"]))
    elif tot["compras"] < 3 and gasto_tot < n * E:
        semaforo, porque = "AMARILLO", "todavía no alcanza para decidir: el gasto no llega a 1 CPA de equilibrio por anuncio"
    elif tot["compras"] >= 3 and T["cpa"] <= E:
        semaforo, porque = "VERDE", "el CPA total (%s) está por debajo del de equilibrio (%s)" % (pesos(T["cpa"]), pesos(E))
    elif tot["compras"] == 0 and gasto_tot >= 3 * E:
        semaforo, porque = "ROJO", "%s gastados (%s CPA de equilibrio) sin ventas" % (pesos(gasto_tot), dec(gasto_tot / E, 1))
    elif tot["compras"] >= 1 and T["cpa"] > 1.5 * E and gasto_tot >= 3 * E:
        semaforo, porque = "ROJO", "el CPA total (%s) es %s veces el de equilibrio" % (pesos(T["cpa"]), dec(T["cpa"] / E, 1))
    else:
        semaforo, porque = "AMARILLO", "hay señales mezcladas: ajustar antes de subir presupuesto"

    # embudo
    etapas = [
        ("Impresiones", tot["impresiones"], None, None, None),
        ("Clics en el enlace", tot["clics"], T["ctr"], REF["ctr_flojo"], "anuncio (gancho, primeros 3 s, texto)"),
    ]
    if tot["visitas"]:
        etapas.append(("Visitas a la página", tot["visitas"], T["llegada"], REF["llegada_floja"], "página lenta o clics accidentales"))
    if "carritos" in cols:
        etapas.append(("Agregados al carrito", tot["carritos"], T["tasa_carrito"], REF["carrito_flojo"], "página u oferta (primera pantalla, precio, packs, confianza)"))
    if "pagos" in cols:
        etapas.append(("Pagos iniciados", tot["pagos"], T["tasa_pago"], REF["pago_flojo"], "sorpresa en el carrito (envío, precio final, cuotas)"))
    if "compras" in cols:
        etapas.append(("Compras", tot["compras"], T["tasa_compra"], REF["compra_floja"], "checkout, medios de pago o medición del evento de compra"))
    peor, peor_ratio = None, 1.0
    for nombre, cant, tasa, ref, causa in etapas[1:]:
        if tasa is not None and ref:
            ratio = tasa / ref
            if ratio < peor_ratio:
                peor, peor_ratio = (nombre, causa), ratio

    # presupuesto sugerido, agrupado por conjunto (es donde se carga con ABO) y sin el recargo de impuestos
    presupuesto = {}
    if dias and not fuga_grave:
        for m, d, motivo, notas in filas_dec:
            diario = m["gasto"] / dias
            g = presupuesto.setdefault(m["conjunto"] or m["nombre"], {"hoy": 0.0, "prox": [0.0] * 4, "quedan": []})
            g["hoy"] += diario
            if d in ("CORTAR", "PAUSAR", "SIN MARGEN"):
                continue
            factores = [1.2 ** k for k in range(1, 5)] if d == "ESCALAR" else [1] * 4
            for i in range(4):
                g["prox"][i] += diario * factores[i]
            g["quedan"].append((m["nombre"], "variante" if d == "ITERAR" else d.lower()))
    hay_cambios = any(d in ("ESCALAR", "CORTAR", "ITERAR") for _, d, _, _ in filas_dec)
    nuevo_por_anuncio = (E / 2) if (E and E > 0 and hay_cambios and not fuga_grave) else None
    diario_actual = (sum(m["gasto"] for m in ms) / dias) if dias else None

    if a.json:
        print(json.dumps({
            "info": info, "cpa_equilibrio": E, "fuente_cpa_equilibrio": fuente_E, "roas_equilibrio": roas_eq,
            "margen_por_pack": [{"unidades": nn, "precio": pr, "margen": mg} for pr, mg, nn in puntos],
            "semaforo": semaforo, "porque": porque, "alertas": alertas, "cpa_real_shopify": cpa_real_shopify,
            "fuga_en_la_pagina": fuga_pagina,
            "total": {k: T[k] for k in ("gasto_real", "impresiones", "clics", "carritos", "pagos", "compras", "valor", "ctr", "cpc", "cpm", "cpa", "roas", "ticket", "frecuencia")},
            "anuncios": [dict(nombre=m["nombre"], conjunto=m["conjunto"], gasto=m["gasto_real"], ctr=m["ctr"], gancho=m["gancho"],
                              retencion=m["retencion"], cpc=m["cpc"], cpm=m["cpm"], tasa_carrito=m["tasa_carrito"], carritos=m["carritos"],
                              compras=m["compras"], cpa=m["cpa"], roas=m["roas"], ticket=m["ticket"], frecuencia=m["frecuencia"],
                              decision=d, motivo=motivo, notas=notas) for m, d, motivo, notas in filas_dec],
            "embudo_donde_se_cae": peor, "lectura": lectura(peor[0], T, medicion_rota) if peor else None,
            "presupuesto_por_conjunto": presupuesto, "presupuesto_por_anuncio_nuevo_diario": nuevo_por_anuncio,
            "gasto_diario_actual": diario_actual,
        }, ensure_ascii=False, indent=1, default=str))
        return

    o = []
    o.append("## Datos leídos [Meta]")
    o.append("- Período: %s a %s (%s) · nivel: %s · números en formato %s · moneda %s" % (
        info["desde"] or "?", info["hasta"] or "?", ("1 día" if dias == 1 else "%s días" % (dias or "?")), info["nivel"], info["formato_numeros"], info["moneda"]))
    o.append("- Columnas encontradas: " + ", ".join(info["columnas_encontradas"]))
    if a.recargo_anuncios:
        o.append("- Gasto con %s de impuestos sobre los anuncios incluido [Usuario]" % pct(a.recargo_anuncios, 0))
    o.append("")
    o.append("## Resumen [Calculado]")
    o.append("| | |\n|---|---|")
    o.append("| Gasto | %s |" % pesos(T["gasto_real"]))
    o.append("| Compras (Meta) | %s |" % (miles(tot["compras"]) if "compras" in cols else "—"))
    if a.shopify_ventas is not None:
        o.append("| Ventas en Shopify [Usuario] | %d |" % a.shopify_ventas)
        if cpa_real_shopify:
            o.append("| CPA con ventas de Shopify | %s |" % pesos(cpa_real_shopify))
    o.append("| CPA (costo por venta) | %s |" % pesos(T["cpa"]))
    o.append("| ROAS (facturación / gasto) | %s |" % dec(T["roas"]))
    o.append("| Ticket promedio | %s |" % pesos(T["ticket"]))
    o.append("| CPA de equilibrio %s | %s |" % (fuente_E, pesos(E)))
    o.append("| ROAS de equilibrio | %s |" % dec(roas_eq))
    o.append("| CTR del enlace · CPC · CPM | %s · %s · %s |" % (pct(T["ctr"], 2), pesos(T["cpc"]), pesos(T["cpm"])))
    o.append("| Frecuencia | %s |" % dec(T["frecuencia"], 1))
    o.append("")
    if puntos:
        o.append("Margen por pack (= CPA de equilibrio de cada uno): " + " · ".join("x%d %s → %s" % (nn, pesos(pr), pesos(mg)) for pr, mg, nn in puntos))
        o.append("")
    o.append("**Semáforo sugerido: %s** · %s" % (semaforo, porque))
    o.append("")
    o.append("## Resultados por anuncio")
    o.append("| Anuncio | Gasto | CTR | Gancho | CPC | Carritos | Compras | CPA | ROAS | Decisión |")
    o.append("|---|---|---|---|---|---|---|---|---|---|")
    car = lambda v: miles(v) if "carritos" in cols else "—"
    com = lambda v: miles(v) if "compras" in cols else "—"
    for m, d, motivo, notas in sorted(filas_dec, key=lambda t: -t[0]["gasto"]):
        nombre = m["nombre"] + (" (%s)" % m["conjunto"] if m["conjunto"] else "")
        o.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** |" % (nombre, pesos(m["gasto_real"]), pct(m["ctr"], 2), pct(m["gancho"]), pesos(m["cpc"]),
                 car(m["carritos"]), com(m["compras"]), pesos(m["cpa"]), dec(m["roas"]), d))
    o.append("| **Total cuenta** | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (pesos(T["gasto_real"]), pct(T["ctr"], 2), pct(T["gancho"]), pesos(T["cpc"]),
             car(tot["carritos"]), com(tot["compras"]), pesos(T["cpa"]), dec(T["roas"]), semaforo))
    o.append("")
    o.append("### Por qué")
    for m, d, motivo, notas in filas_dec:
        o.append("- **%s → %s**: %s%s" % (m["nombre"], d, motivo, ("; " + "; ".join(notas)) if notas else ""))
    o.append("")
    o.append("## Embudo total")
    o.append("| Etapa | Cantidad | Tasa | Referencia (orientativa) |")
    o.append("|---|---|---|---|")
    for nombre, cant, tasa, ref, causa in etapas:
        marca = " ⚠️" if (peor and peor[0] == nombre) else ""
        o.append("| %s%s | %s | %s | %s |" % (nombre, marca, miles(cant), pct(tasa, 1) if tasa is not None else "—", ("flojo si < " + pct(ref, 1)) if ref else ""))
    if peor:
        o.append("")
        o.append("Donde más se cae: **%s** (%.0f%% de la referencia) → %s" % (peor[0], peor_ratio * 100, peor[1]))
        o.append("")
        o.append("Lectura: " + lectura(peor[0], T, medicion_rota))
    if alertas:
        o.append("")
        o.append("## Alertas")
        for al in alertas:
            o.append("- " + al)
    o.append("")
    o.append("## Presupuesto sugerido (próximos 4 días)")
    if fuga_grave:
        o.append("- Pausar la campaña mientras se arregla la página: seguir pagando clics que no compran no lo arregla.")
        if diario_actual:
            o.append("- Con la página lista, reactivar los mismos anuncios con lo que gastaban (~%s por día en total) y volver a juzgar al llegar a 2 CPA de equilibrio por anuncio." % pesos(diario_actual))
    elif presupuesto:
        con_conjuntos = any(m["conjunto"] for m in ms)
        o.append("| %s | %s | Hoy por día | Día 1 | Día 2 | Día 3 | Día 4 |" % (("Conjunto", "Quedan") if con_conjuntos else ("Anuncio", "Decisión")))
        o.append("|---|---|---|---|---|---|---|")
        for nombre, g in presupuesto.items():
            quedan = ", ".join(("%s (%s)" % q) if con_conjuntos else q[1] for q in g["quedan"]) or "apagar"
            o.append("| %s | %s | %s | %s |" % (nombre, quedan, pesos(g["hoy"]), " | ".join(pesos(x) for x in g["prox"])))
        tot_prox = [sum(g["prox"][i] for g in presupuesto.values()) for i in range(4)]
        o.append("| **Total** | | %s | %s |" % (pesos(sum(g["hoy"] for g in presupuesto.values())), " | ".join(pesos(x) for x in tot_prox)))
        if con_conjuntos:
            o.append("- Con presupuesto por conjunto (ABO), cargá esa cifra en cada conjunto: es la suma de los anuncios que quedan, así que baja cuando apagás un perdedor aunque el ganador suba 20%. Con presupuesto de campaña (Advantage+), usá el total.")
    elif not dias:
        o.append("- Sin fechas en el export: pasá --dias para calcular el gasto diario.")
    if nuevo_por_anuncio:
        o.append("- Anuncios nuevos: en un conjunto aparte (para no reiniciar el aprendizaje del ganador), ~%s por día cada uno: llegan a 2 CPA de equilibrio en 4 días. Con 3 nuevos son %s por día; hoy gastás %s por día en total." % (
            pesos(nuevo_por_anuncio), pesos(3 * nuevo_por_anuncio), pesos(diario_actual)))
    elif medicion_rota:
        o.append("- No cambies presupuestos ni sumes anuncios hasta que Meta vuelva a ver las compras: sin eso no hay con qué decidir y el algoritmo optimiza a ciegas.")
    elif not fuga_grave and E and E > 0:
        o.append("- No sumes anuncios nuevos todavía: primero que los actuales lleguen a 1–2 CPA de equilibrio cada uno.")
    o.append("- Subir como máximo 20% por día; cambiar una cosa por vez para no reiniciar el aprendizaje de Meta.")
    print("\n".join(o))


if __name__ == "__main__":
    main()
