---
name: analizar-campanas-meta-ar
description: Diagnostica campañas de Meta Ads (Facebook e Instagram) de un ecommerce en Argentina, en pesos, y dice en lenguaje simple qué anuncios cortar, mantener, escalar o cambiar y qué probar después. Lee el export del Administrador de anuncios (CSV o Excel, en español o inglés) o capturas, calcula CPM, CTR, CPC, gancho, retención, tasa de carrito, CPA, ROAS y ticket promedio, los compara con el CPA de equilibrio del producto, controla que el píxel mida bien contra las ventas de Shopify y devuelve un semáforo VERDE/AMARILLO/ROJO, la decisión por anuncio, dónde se cae la venta y 3 anuncios nuevos para probar. Usá esta skill siempre que alguien pegue o suba resultados de Meta Ads, mande capturas de sus campañas o pregunte cómo va su campaña, si corta o apaga un anuncio, si escala o le sube el presupuesto, por qué no le compran, diga que gastó tanto y no vende o que tiene clics pero no ventas, o mencione CPA, ROAS, CTR, CPM, CPC, frecuencia o el píxel, aunque no diga la palabra analizar.
---

# Analizar campañas de Meta Ads (Argentina)

El objetivo es que quien vende no queme plata: mirar los números reales de sus anuncios y decirle, en criollo, qué apagar, qué dejar, qué escalar y qué probar mañana. Leer mal un día de campaña sale caro para los dos lados: apagar un anuncio que iba a vender, o seguir pagando uno que nunca va a vender. Por eso el diagnóstico tiene que ser honesto: si hay que frenar todo, se dice; si todavía no hay datos para decidir, también.

Escribí en español rioplatense, simple y directo, como para leer en el celular a la noche y actuar a la mañana. Quien lo lee puede no saber qué es un CPA: la primera vez que aparece cada término, explicalo en media línea (glosario abajo).

## Regla de oro: cada número con su origen

Las decisiones valen lo que valen los datos. Por eso:
- Cada número lleva su origen: **[Meta]** (export o captura), **[Shopify]** (lo que el usuario sacó de su tienda), **[Usuario]** (lo que dijo en el mensaje), **[Calculado]** (cuenta tuya o del script con datos de arriba) o **[Estimado]** (un supuesto: mostrá el rango y en qué se basa).
- **Nunca inventes** un dato que falta (compras, carritos, costo, ventas de Shopify). Si no está, va "—" y se pide en "Datos que me faltaron".
- Con pocos datos, la respuesta correcta es **"todavía no alcanza para decidir"**, no una adivinanza. Un anuncio que gastó menos de 1 CPA de equilibrio y no vendió no dice nada: es lo esperable aunque sea bueno.
- Las referencias generales (CTR, gancho, frecuencia, tasas del embudo) son **orientativas**: cambian según el producto, el precio y la cuenta. Decilo cuando las uses y dale más peso a la comparación con el CPA de equilibrio y con el promedio de la propia cuenta.

## Glosario (media línea, la primera vez que uses cada término)
- **CPM**: lo que cuesta que el anuncio se muestre 1.000 veces.
- **CTR del enlace**: de cada 100 personas que ven el anuncio, cuántas hacen clic para ir a la página.
- **CPC**: lo que pagás por cada clic que llega a la página.
- **Gancho**: de cada 100 que ven el video, cuántas lo miran al menos 3 segundos (lo deciden los primeros 3 s).
- **Retención**: de los que miraron 3 s, cuántos lo ven completo o 15 s (ThruPlay).
- **Tasa de carrito**: de cada 100 que llegan a la página, cuántos agregan al carrito.
- **CPA**: lo que pagaste en anuncios por cada venta.
- **CPA de equilibrio**: lo máximo que podés pagar en anuncios por venta sin perder plata (lo que te queda de cada venta antes de pagar anuncios).
- **ROAS**: cuántos pesos facturaste por cada $1 de anuncios; **ROAS de equilibrio**: el mínimo para no perder.
- **Ticket promedio**: cuánto paga en promedio cada cliente (con los packs de Kaching sube cuando eligen x2 o x3).
- **Frecuencia**: cuántas veces vio el anuncio cada persona, en promedio.
- **Fase de aprendizaje**: los primeros días (o después de un cambio grande) en que Meta prueba a quién mostrarle el anuncio; los resultados saltan mucho.

## Qué necesitás

No pidas nada antes de arrancar: con el export o la captura alcanza para empezar. Lo que falte, pedilo una sola vez, al final, en "Datos que me faltaron".

1. **Los resultados de Meta**, idealmente el export del Administrador de anuncios **a nivel anuncio** (CSV o Excel, en español o inglés). Si solo hay capturas, leelas (Paso 1). Cómo exportarlo bien, paso a paso: `references/exportar-informe-meta.md`.
2. **Los números del producto** para el CPA de equilibrio, en este orden:
   - Lo que diga el usuario (precio de cada pack, costo) → [Usuario].
   - Si existe la carpeta de la marca en el repo: `<MARCA>/validacion/` (tabla "Números clave": CPA de equilibrio por pack, costo y supuestos de envío y comisiones). Usá esos datos y aclará si el costo figuraba como [Estimado]. Los precios de los packs también están en `<MARCA>/landing/info.txt`.
   - Si no hay nada: precios de la landing o la tienda si se pueden ver, y el costo como [Estimado] con el supuesto a la vista. Las comisiones por defecto son las de validar-producto-ar (pasarela 7%, cuotas sin interés 8%, plataforma 2%, impuestos 4%, devoluciones 3%, empaque $1.000): mencioná que conviene verificarlas.
3. **Las ventas de Shopify del mismo período** (pedidos pagos). Es opcional pero clave: es la única forma de saber si el píxel mide bien. Si no las pasó, pedilas al final sin frenar el análisis.

Si la carpeta de la marca tiene `CLAUDE.md` (por ejemplo `VERDEA-huerta/CLAUDE.md`) o `creativos/buyer-personas*`, leelos antes de proponer anuncios: ahí están las buyer personas habilitadas, el tono, el formato de video y qué está prohibido.

## Proceso

### Paso 1 · Ordenar los datos
Corré `scripts/metricas.py`: lee el archivo tal como lo baja Meta (CSV con coma o punto y coma, Excel, columnas en español o en inglés, números 1.234,56 o 1,234.56), suma por anuncio si viene desglosado por día, calcula todo y avisa qué columnas faltan.

```bash
python scripts/metricas.py export.csv --costo 12000 --packs 1:34900,2:59900,3:79900 --envio 8000 --envio-gratis-desde 3 --shopify-ventas 7
```

- `--cpa-equilibrio 13524` si ya está calculado; o `--costo` con `--precio` o `--packs unidades:precio,...` para que lo calcule (misma fórmula que `economia.py` de validar-producto-ar). Con packs, el script deduce qué packs se vendieron a partir del valor de las compras de cada anuncio y usa el margen de esa mezcla (si no cierra, porque el valor incluye envío o descuentos, se ajusta al ticket promedio); sin ventas usa el pack que menos deja, que es lo prudente.
- `--envio` (lo que te cuesta el envío cuando lo regalás) y `--envio-gratis-desde N` (desde cuántas unidades es gratis). Sin `--envio-gratis-desde`, asume que el envío lo paga el cliente.
- `--shopify-ventas N` para controlar la medición; `--dias N` si el archivo no trae fechas; `--tipo-cambio` si la cuenta publicitaria está en dólares; `--recargo-anuncios 0.21` si los impuestos que Meta cobra arriba del gasto son costo para el usuario (ver `references/metricas-y-reglas.md`); `--json` para leer el resultado como datos.
- Si no podés ejecutar código, hacé las cuentas con las fórmulas de `references/metricas-y-reglas.md` y mostralas.

**Si llegan capturas**: leé de la imagen el período, y por anuncio el importe gastado, impresiones, alcance, clics en el enlace y resultados (compras). Pasalo a un CSV en tu carpeta de trabajo con encabezados como los de Meta (`Inicio del informe,Fin del informe,Nombre del anuncio,Importe gastado (ARS),Impresiones,Alcance,Clics en el enlace,Compras`) y corré el script con esas fechas o con `--dias`. Esos números van como [Meta · captura]. Si un número no se lee bien, no lo adivines: decilo. Las capturas casi nunca traen carritos, pagos ni reproducciones de 3 s, así que el diagnóstico del embudo queda incompleto: eso va en "Datos que me faltaron".

Anotá: período (fechas y cantidad de días), cuántos anuncios y cómo están agrupados (campaña → conjunto → anuncio), y qué falta.

### Paso 2 · Controlar la medición antes de opinar
Antes de juzgar un anuncio por sus ventas, fijate que Meta las esté viendo. Si el píxel no mide, cortar "los que no venden" es cortar a ciegas, y además Meta optimiza a ciegas.
- **Shopify tiene ventas y Meta muestra 0 compras** → la medición está rota. No decidas por ventas (decisión NO DECIDIR, no se apaga nada por "no vender"), calculá el CPA real con las ventas de Shopify (gasto ÷ ventas; es un piso, porque alguna venta pudo venir de otro lado) y poné el arreglo del píxel como primer punto de "Qué hacer mañana".
- **Meta ve menos de la mitad de las ventas de Shopify** → medición parcial (API de conversiones apagada, pagos con Mercado Pago que no vuelven a la página de gracias).
- **Meta cuenta bastante más compras que Shopify** → píxel duplicado (en el tema y en la app a la vez).
- Sin datos de Shopify, sospechá si hay pagos iniciados y 0 compras, compras sin valor, o muchos clics y 0 carritos; pedí las ventas de Shopify.

Una diferencia chica entre Meta y Shopify es normal (Meta atribuye por ventanas de 7 días después del clic y 1 día después de ver el anuncio; Shopify cuenta todas las ventas). Cómo revisar y arreglar la medición: `references/diagnostico-embudo.md`, sección "Medición".

### Paso 3 · Calcular las métricas por anuncio
El script calcula, por anuncio y para toda la cuenta: CPM, CTR del enlace, CPC, gancho, retención, llegada a la página, tasa de carrito, de pago y de compra, CPA, ROAS y ticket promedio. Usá sus números ([Calculado]) en vez de rehacerlos a mano. Fórmulas: `references/metricas-y-reglas.md`.

### Paso 4 · Comparar con el equilibrio y con la propia cuenta
- **Contra el CPA de equilibrio**, que es la vara principal: con CPA por debajo, el anuncio gana plata; por encima, pierde.
- **Contra el promedio de la cuenta**: un anuncio con la mitad del CTR que el resto está flojo aunque pase la referencia general.
- **Contra las referencias orientativas**, aclarando que lo son: CTR del enlace menor a 0,8% = gancho flojo; gancho menor a 25%; frecuencia mayor a 2,5 en 7 días = público cansado; tasa de carrito menor a 4%. Detalle y porqué en `references/metricas-y-reglas.md`.

### Paso 5 · Encontrar dónde se cae la venta
Recorré el embudo (impresiones → clics → visitas → carrito → pago → compra) y buscá la etapa que más se aleja de lo normal; el script la marca con ⚠️ y da una lectura. Los cuatro lugares típicos:
- **En el anuncio**: CTR bajo o gancho flojo, la gente no frena ni hace clic. Se arregla con ganchos nuevos, no tocando la página.
- **En la página**: muchos clics y pocos carritos. La promesa del anuncio no aparece en la página, el precio asusta, la primera pantalla no convence, falta confianza o algo anda mal en el celular. **Cortar anuncios no lo arregla**: si los anuncios traen clics baratos, el problema está después del clic.
- **En la oferta o el precio**: carritos sin pago o pagos sin compra. Sorpresas al final: envío, precio final, cuotas, descuento del pack que no aparece, medio de pago.
- **En el público**: frecuencia alta, CPM que sube y CTR que baja con los días. El público se cansó: hacen falta creativos nuevos o un público más amplio.

Causas, cómo confirmarlas y qué cambiar en cada caso: `references/diagnostico-embudo.md`.

### Paso 6 · Decidir por anuncio
Partí de la decisión del script y explicá cada una en una línea, con el número que la respalda. Las reglas:

| Decisión | Cuándo | Qué hacer |
|---|---|---|
| **NO TOCAR** | Gastó menos de 1 CPA de equilibrio, con o sin 1-2 ventas. Excepción: CTR menor a 0,5% con más de 2.000 impresiones → CORTAR. | Nada: ni presupuesto, ni texto, ni público. |
| **CORTAR** | 1,5–2 CPA de equilibrio gastados sin ventas; o 3+ ventas con CPA mayor a 1,5 veces el de equilibrio; o 1-2 ventas con 3+ CPA gastados; o no engancha (CTR menor a 0,8% y gancho menor a 25%) con 1 CPA gastado sin ventas. | Apagarlo. Si el ángulo era bueno, se reusa con otro gancho. |
| **ESCALAR** | 3 o más ventas con CPA menor o igual al de equilibrio, y al menos 3 días de datos. | Subir el presupuesto **20% por día como máximo**. |
| **ITERAR** | Engancha pero no vende, vende pero el gancho es flojo, o vende apenas caro. | Hacer una variante que cambie **una sola cosa** (la que falla) y subirla como anuncio nuevo. Decí exactamente qué cambiar. |
| **MANTENER** | Zona gris: vende cerca del equilibrio, 1-2 ventas prometedoras, o sin ventas pero con pagos iniciados y menos de 2 CPA gastados. | Dejarlo igual y mirarlo de nuevo en 1-2 días. |
| **PAUSAR** | Toda la cuenta trae clics (CTR de 0,8% o más) pero la página no convierte (tasa de carrito menor a 4%), no es rentable y ya gastó 2+ CPA de equilibrio. | Pausar mientras se arregla la página y reactivar los mismos anuncios después. |
| **NO DECIDIR** | Meta no ve las compras que sí registra Shopify. | Arreglar la medición primero. |

Por qué estos números: un anuncio que vende justo en equilibrio hace, en promedio, 1 venta por cada CPA de equilibrio gastado. Con menos gasto, 0 ventas es normal (pasa 1 de cada 3 veces aunque el anuncio sea bueno); con 2 CPA gastados sin ventas, la chance de que sea bueno y haya tenido mala suerte baja a 1 en 7, y ahí se corta. Se piden 3 ventas para escalar porque con 1 o 2 el CPA todavía es casualidad. Y se escala de a 20% porque los saltos grandes de presupuesto mandan a Meta de vuelta a la fase de aprendizaje y el CPA se dispara.

Las reglas ordenan la decisión; el criterio sigue siendo tuyo. Si un caso no encaja (un anuncio con 2 ventas y 15 pagos iniciados, un público que se cansó justo al llegar a 3 ventas), decí qué harías y por qué.

### Paso 7 · Próximos pasos
1. **Qué hacer mañana**: de 3 a 6 acciones concretas, en orden, que se hagan en 10 minutos en el Administrador de anuncios ("Apagá Caro 2 · Pinterest", "Poné el conjunto Caro en $8.340 por día"). Primero lo que más plata ahorra o más plata hace; si la medición está rota, primero eso.
2. **Presupuesto de los próximos 3-4 días**: la tabla del script, por conjunto, con el total por día. Con presupuesto por conjunto (ABO), cada conjunto lleva la suma de los anuncios que quedan: si el ganador comparte conjunto con perdedores, al apagarlos hay que bajar el conjunto a la cifra de la tabla; si no, el ganador recibe de golpe todo el presupuesto del conjunto. Con presupuesto de campaña (Advantage+), se sube la campaña. Los anuncios nuevos van en un conjunto aparte, con ~½ CPA de equilibrio por día cada uno (llegan a 2 CPA en 4 días) para no reiniciar el aprendizaje del ganador. Si el total no le da, que pruebe 2 en vez de 3, o de a uno; menos de ⅓ CPA por día por anuncio hace que tarde más de una semana en poder juzgarse.
3. **3 anuncios nuevos para probar**, basados en el que mejor funciona (el ganador; si nadie vende, el de mejor CTR): mismo ángulo y misma buyer persona, **otro gancho en los primeros 3 segundos**. Para cada uno: para quién es, el gancho (texto exacto de los primeros 3 s), qué se ve, texto en pantalla y por qué (qué dato del ganador lo justifica). Respetá las reglas de la marca: en VERDEA, solo Lucía y Marta, CTA suave y emocional (nada de "comprá ya"), la oferta en el texto en pantalla y solo reseñas o antes/después reales. Si el problema es la página o la medición, aclará que las ideas son para cuando eso esté resuelto.
4. **Cambios en la página o la oferta**, solo si el embudo dice que la venta se cae ahí: concretos, de a uno, con cómo se va a saber si funcionó. Si el repo tiene la landing de la marca (`<MARCA>/landing/`: `info.txt` y el snippet), abrila antes de opinar y revisala con la lista de `references/diagnostico-embudo.md` (sección 4): que la primera pantalla cumpla la promesa de los anuncios, el precio contra el mercado, el envío y la garantía a la vista. Mirá especialmente la prueba social: estrellas, cantidad de opiniones o de clientes, carteles de "compró hace X min" y sellos de "compra verificada" que no salen de ventas reales. Si hay algo inventado, va primero en la lista: rompe la regla de la marca, es publicidad engañosa y espanta justo a la clienta desconfiada.

Con días 1 o 2 la respuesta casi siempre es "no toques nada todavía": Meta está aprendiendo y un día de datos es ruido. Lo útil en ese caso es decir **cuándo** mirar de nuevo y **qué número** dispararía cada decisión ("si Lucía 2 pasa las 2.000 impresiones con CTR menor a 0,5%, se corta").

## Semáforo
- **VERDE**: 3 o más ventas y CPA total por debajo del de equilibrio. Se gana plata: escalar con cuidado.
- **AMARILLO**: todavía no alcanza para decidir (menos de 1 CPA de equilibrio por anuncio y menos de 3 ventas), señales mezcladas, medición rota con un CPA real que parece bueno, o faltan costo y precio.
- **ROJO**: 3+ CPA de equilibrio gastados sin ventas; CPA total mayor a 1,5 veces el de equilibrio con 3+ CPA gastados; la página no convierte; el producto no deja margen; o la medición está rota y aun con las ventas de Shopify el CPA no cierra.

Con ROJO decí sin vueltas si conviene **frenar todo** y qué revisar antes de volver a gastar: página, oferta, precio o el producto mismo (para eso está la skill validar-producto-ar).

## Formato de la respuesta

Usá esta estructura, en este orden, con estos títulos. El contenido, corto: el informe entero se tiene que poder leer en el celular en 4-5 minutos (unas 900 a 1.300 palabras). Para lograrlo, cada término se explica una sola vez, cada número aparece en un solo lugar, cada anuncio lleva una línea de porqué, cada idea de anuncio entra en 3 líneas, y los supuestos y escenarios alternativos van en una línea ("con costo $15.000, Caro 3 queda justo"), no en párrafos. Si algo no cambia ninguna decisión, no va.

```
# [Marca] · Diagnóstico de campaña ([fecha de inicio] al [fecha de fin], [N] días)

## Semáforo: [VERDE / AMARILLO / ROJO] · [una línea con el porqué]
Confianza en los datos: [alta / media / baja] · [qué faltó o qué la baja]

## Qué hacer mañana
- [ ] [acción concreta 1]
- [ ] [acción concreta 2]

## Resultados por anuncio
| Anuncio | Gasto | CTR | Gancho | CPC | Carritos | Compras | CPA | ROAS | Decisión |
[una fila por anuncio y una de total de la cuenta; "—" si falta el dato]
[debajo, una línea por anuncio: la decisión y su porqué con el número que la respalda]
CPA de equilibrio usado: $... [origen] · ROAS de equilibrio: ...

## Dónde se cae la venta
[embudo corto con cantidades y tasas, la etapa que falla y la lectura en una o dos líneas]
[si se cae en la página o la oferta: de 2 a 4 cambios concretos]

## Próximos anuncios para probar
1. [para quién] · Gancho (0-3 s): "..." · Qué se ve: ... · Texto en pantalla: ... · Por qué: ...
2. ...
3. ...
[presupuesto de los próximos 3-4 días: tabla corta por conjunto y total por día]

## Datos que me faltaron
[los 3-4 datos que más pueden cambiar una decisión, con instrucciones exactas para sacarlos de Meta o de Shopify; "nada" si no faltó nada]
```

Confianza en los datos: **alta** con export completo y ventas de Shopify que coinciden; **media** si faltan las ventas de Shopify o columnas del embudo, o el costo es estimado; **baja** con capturas parciales, 1-2 días de datos o medición rota.

## Si después te pasan más datos
Si el usuario manda las ventas de Shopify, el costo real o más días, volvé a correr el script y mostrá qué cambió (semáforo, decisiones, presupuesto) en vez de repetir todo el informe.
