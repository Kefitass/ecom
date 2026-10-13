---
name: validar-producto-ar
description: Valida un producto de ecommerce ANTES de gastar plata testeándolo con anuncios, con foco en el mercado argentino. Investiga demanda real (Mercado Libre, Google Trends AR, redes), competencia y anuncios activos (Biblioteca de Anuncios de Meta), calcula la economía unitaria en pesos (margen, costo de cuotas, comisiones, CPA y ROAS de equilibrio) y devuelve un puntaje de 0 a 100 con veredicto TESTEAR / AJUSTAR / DESCARTAR, precio sugerido y plan de test. Usá esta skill siempre que alguien pregunte si un producto "sirve", "vende", "es ganador", "vale la pena testearlo", si conviene venderlo en Argentina, cuánto cobrarlo, qué margen deja, o pase un link de AliExpress/proveedor, una foto o el nombre de un producto pensando en dropshipping, Shopify, Tiendanube o Meta Ads, aunque no diga la palabra "validar".
---

# Validar producto para Argentina

El objetivo es ahorrarle plata a quien vende: decidir con datos, antes de pautar, si un producto tiene chances en Argentina, y si las tiene, a qué precio y con qué oferta testearlo. Un test de Meta Ads mal elegido quema fácilmente $100.000–$300.000 ARS; esta validación tiene que ser lo bastante honesta como para decir "no lo testees" cuando corresponde.

Escribí siempre en español rioplatense, claro y directo, sin jerga innecesaria. Quien lo usa puede no saber qué es un CPA o un ROAS: la primera vez que aparezca un término, explicalo en media línea.

## Regla de oro: cada número con su fuente

El valor de esta skill depende de que los datos sean reales. Por eso:
- **Nunca inventes** cantidades vendidas, precios de la competencia, cantidad de anuncios ni tendencias.
- Cada dato del informe lleva su origen: **[ML]**, **[Meta Ad Library]**, **[Google Trends]**, **[Usuario]**, **[Web]** o **[Estimado]**.
- Si un dato no se pudo conseguir, decilo y bajá la confianza del puntaje, en vez de rellenar.
- Un número **[Estimado]** debe mostrar el rango y el supuesto ("entre X e Y, suponiendo Z").

## Qué necesitás del usuario

Pedí solo lo que falte, en un único mensaje corto:
1. **El producto**: nombre, link (AliExpress, proveedor local, Mercado Libre) o foto.
2. **Costo por unidad puesto en su casa/depósito** (en ARS o USD), si lo sabe. Si no lo sabe, estimalo con el precio del proveedor + envío/importación y marcalo [Estimado].
3. **Dónde vende**: Shopify, Tiendanube, Mercado Libre o redes. Si no lo dice, asumí tienda propia + Meta Ads.

Si el usuario solo da el nombre, arrancá igual con la investigación y pedí el costo al final.

## Proceso

### Paso 1 · Entender el producto (2-3 líneas)
Qué es, qué problema resuelve o qué deseo cumple, a quién le sirve y en qué categoría compite en Argentina. Esto define dónde buscar y qué comparar.

### Paso 2 · Demanda en Argentina
Buscá evidencia de que **la gente ya compra esto en Argentina**. Las fuentes, cómo consultarlas y qué hacer si están bloqueadas están en `references/fuentes-ar.md`; leelo antes de buscar.

Lo mínimo a relevar:
- **Mercado Libre Argentina**: cuántas publicaciones hay, los 5-10 más vendidos (título, precio, "+X vendidos", reputación, si son Full / envío gratis / cuotas), rango de precios, y las preguntas frecuentes de las publicaciones top (muestran dudas y objeciones reales).
- **Estacionalidad** (Google Trends AR, últimos 12 meses): ¿crece, cae, tiene temporada? Recordá que en Argentina las estaciones están invertidas respecto al hemisferio norte (jardinería y pileta suben en primavera-verano: sep–feb; calefacción en may–ago).
- **Redes**: si hay videos/creadores argentinos mostrándolo (TikTok/Instagram) y cómo reacciona la gente.

Si una fuente no responde (bloqueo, login, captcha), no la saltees en silencio: pedile al usuario una captura concreta con instrucciones exactas (están en `references/fuentes-ar.md`) y seguí con lo demás mientras tanto.

### Paso 3 · Competencia y anuncios
- **Biblioteca de Anuncios de Meta** (país Argentina, palabra clave del producto): cuántos anunciantes, y sobre todo **cuáles anuncios llevan más de 30 días activos** (si alguien paga un anuncio un mes entero, casi seguro le está dando ganancia). Anotá sus ángulos, ofertas (2x1, packs, cuotas) y precios.
- **Tiendas propias** que lo venden en Argentina (Shopify/Tiendanube): precio, oferta, calidad de la página.
- Concluí: ¿hay un mercado probado y todavía espacio, o está saturado con todos vendiendo lo mismo al mismo precio?

### Paso 4 · Economía unitaria (en pesos)
Es el paso que más productos descarta, así que hacelo con cuidado. Usá `scripts/economia.py` si podés ejecutar código (es determinístico y evita errores de cuentas); si no, seguí las fórmulas de `references/costos-ar.md` paso a paso y mostrá el cálculo.

Calculá:
- **Costo total por pedido**: producto + envío al cliente (si lo absorbés) + empaque + comisión de la pasarela + costo de ofrecer cuotas sin interés + comisión de la plataforma + impuestos aplicables (configurables).
- **Margen de contribución** por pedido (antes de publicidad).
- **CPA de equilibrio** (cuánto podés pagar en anuncios por venta sin perder plata) y **ROAS de equilibrio** (cuánto tiene que facturar cada $1 de anuncios).
- **Precio sugerido**: en Argentina, para pautar en Meta con margen, apuntá a que el precio sea **al menos 3 veces el costo del producto puesto**; por debajo de 2,5x casi siempre se pierde plata con publicidad. Contrastalo con los precios de Mercado Libre: si para que cierren los números tenés que cobrar bastante más que en ML, necesitás una oferta o diferenciación que lo justifique (packs, regalo, garantía, marca).
- **Oferta recomendada**: packs (x2, x3) que suban el ticket promedio, regalo, envío gratis desde cierto monto.

Los porcentajes de comisiones y costos financieros en Argentina cambian seguido. En `references/costos-ar.md` hay valores por defecto con la indicación de verificarlos; si el usuario te da sus porcentajes reales, usá esos.

### Paso 5 · Puntaje y veredicto
Puntuá con la grilla de abajo. Justificá cada criterio en una línea con el dato que lo respalda.

| Criterio | Puntos | Qué mirar |
|---|---|---|
| Problema o deseo fuerte | 15 | ¿Resuelve un dolor concreto o cumple un deseo claro? ¿Se entiende en 3 segundos? |
| Demostrable en video | 15 | ¿Tiene efecto "wow", antes/después, o se ve funcionar en un Reel? |
| Margen | 20 | Precio ≥ 3x costo puesto = completo; 2,5–3x = parcial; < 2,5x = 0–5 |
| Demanda probada en AR | 15 | Ventas en ML, búsquedas, anuncios activos hace más de 30 días |
| Nivel de competencia | 10 | Hay demanda pero no está saturado de vendedores idénticos y baratos |
| Diferenciación posible | 10 | ¿Podés venderlo con otro ángulo, oferta, pack o marca? |
| Logística y riesgo | 10 | Peso, fragilidad, líquidos, talles, devoluciones, importación |
| Recompra / ticket | 5 | ¿Se consume y se vuelve a comprar? ¿Permite packs o upsells? |

**Veredicto:**
- **70–100 → TESTEAR**: tiene chances; pasá el plan de test.
- **50–69 → AJUSTAR**: puede funcionar si se corrige algo concreto (precio, oferta, proveedor, ángulo); decí exactamente qué.
- **0–49 → DESCARTAR**: explicá por qué, sin rodeos.

**Alertas que bajan el veredicto aunque el puntaje dé alto** (ver detalle en `references/costos-ar.md`):
- Requiere registro o habilitación (ANMAT para cosméticos, suplementos, productos médicos; SENASA para agroquímicos y fertilizantes con ciertas formulaciones; homologación ENACOM para electrónica con radio/Bluetooth/WiFi; normas de seguridad eléctrica). Si probablemente aplica, avisá y recomendá verificarlo antes de vender.
- Réplicas o productos con marcas registradas de terceros.
- Promesas de salud o resultados que no se pueden demostrar (riesgo legal y de rechazo de anuncios en Meta).
- Si la confianza en los datos es baja (pocas fuentes conseguidas), decilo junto al veredicto.

### Paso 6 · Plan de test (solo si el veredicto es TESTEAR o AJUSTAR)
- **Precio y oferta** con los que salir.
- **3 ángulos de venta** distintos (dolor, deseo, demostración) con un gancho de ejemplo para cada uno.
- **Presupuesto de test**: 3 a 5 anuncios, durante 3 a 5 días, con un monto diario que permita gastar al menos **2 veces el CPA de equilibrio por anuncio** antes de juzgarlo.
- **Criterios para cortar o escalar**: cortar un anuncio que gastó 1,5–2x el CPA de equilibrio sin ventas; escalar el que vende por debajo del CPA de equilibrio.

## Formato de la respuesta

Usá esta estructura, en este orden:

```
# [Producto] · Validación para Argentina

## Veredicto: [TESTEAR / AJUSTAR / DESCARTAR] · [puntaje]/100
[2-3 líneas: por qué, y la acción concreta que sigue]
Confianza en los datos: [alta / media / baja] — [qué faltó, si algo]

## Números clave
| | |
|---|---|
| Costo puesto por unidad | $... [fuente] |
| Precio sugerido | $... (x2: $..., x3: $...) |
| Precio de mercado en ML | $... a $... [ML] |
| Margen antes de anuncios | $... (..%) |
| CPA de equilibrio | $... |
| ROAS de equilibrio | ... |

## Demanda en Argentina
[hallazgos con fuente]

## Competencia y anuncios
[hallazgos con fuente]

## Puntaje por criterio
[tabla con puntos y justificación de una línea cada uno]

## Alertas
[regulatorias, logísticas o de datos; "ninguna" si no hay]

## Plan de test
[solo si TESTEAR / AJUSTAR]

## Datos que me faltaron
[qué capturas o números mejorarían la validación, con instrucciones exactas para conseguirlos]
```

Si el usuario después te pasa datos que faltaban (capturas, su costo real, sus comisiones), recalculá y mostrá qué cambió en el puntaje y el veredicto.
