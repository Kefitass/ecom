# ORDI · Diagnóstico de campaña (7 al 9 de octubre, 3 días)

## Semáforo: AMARILLO · Meta no ve las compras, pero con las 7 ventas de Shopify la campaña parece rentable (~$9.000 por venta contra un máximo de $13.524)
Confianza en los datos: **baja** · Meta no registra ninguna compra. Además no sé cuántas de las 7 ventas vinieron de los anuncios ni qué packs eran, el costo por set es estimado y el export termina el 9/10.

**¿Apago los anuncios? No.** Todo indica que traen gente que compra:
- Meta vio 32 carritos y 19 pagos iniciados (gente que llegó a la pantalla de pago) [Meta], y tu tienda tuvo 7 ventas esos mismos días [Shopify].
- Si las 7 vinieron de los anuncios, pagaste **unos $9.000 de anuncios por venta** ($63.000 ÷ 7) [Calculado]. Eso es el **CPA** (lo que pagás en anuncios por cada venta). Lo máximo que podés pagar sin perder plata (**CPA de equilibrio**) es $13.524 [Calculado]. Alcanza con que 5 de las 7 ventas hayan venido de los anuncios para no perder plata, aunque todas fueran de 1 set.
- Los anuncios en sí andan bien. **CTR** de 1,43% a 1,88% (de cada 100 que ven el anuncio, cuántos hacen clic; flojo sería menos de 0,8%). **Gancho** de 31% a 37% (cuántos miran al menos 3 s del video; flojo, menos de 25%). **Frecuencia** 1,2 (cada persona lo vio poco más de una vez: no hay cansancio). [Calculado; las referencias son orientativas]

Lo que está roto es el **píxel**, el código que le avisa a Meta lo que pasa en tu tienda: ve a la gente hasta el pago, pero no se entera de la compra. Que de 19 pagos iniciados no termine ninguno mientras la tienda vende 7 es muy poco probable. Mientras no se arregle, no hay con qué juzgar cada anuncio, y Meta busca compradores a ciegas.

## Qué hacer mañana
- [ ] **Fijate si a Meta le llega alguna compra.** Entrá al Administrador de eventos → tu conjunto de datos (el píxel) → Información general → evento "Compra" (Purchase).
  - Si no aparece, o llegó por última vez hace días, la tienda no la está mandando: seguí con el paso 2.
  - Si aparece pero la campaña dice 0, la campaña está mirando otro píxel. Entrá a cada conjunto de anuncios → Conversión, y fijate que el evento sea Compra y que el conjunto de datos sea el mismo que conecta la app de Shopify.
- [ ] **Arreglalo desde Shopify.** Canal Facebook & Instagram → Configuración → Uso compartido de datos → **Máximo**. Tiene que estar conectado a tu cuenta publicitaria y al mismo píxel que usa la campaña.
  - Eso prende la API de conversiones: Shopify le avisa a Meta cada venta desde su servidor, aunque la persona pague con Mercado Pago y no vuelva a la página de "gracias por tu compra" (pasa muchísimo en Argentina).
  - Si además pegaste el píxel a mano en el tema, sacalo y dejá solo la app. Ese código no corre en el pago de Shopify, y con la app andando contaría doble.
- [ ] **Probalo con una compra real.** Abrí "Probar eventos" en el Administrador de eventos y comprá 1 set pagando con Mercado Pago: tiene que llegar "Compra" con el valor en pesos. Después cancelá y reembolsá el pedido. Es el punto "Evento de compra probado" del checklist de `anuncios/plan-testeo-meta-ads.md`.
- [ ] **Poné UTM en los 3 anuncios.** Son una etiqueta en el link para que Shopify sepa de qué anuncio viene cada venta. Editar anuncio → Seguimiento → Parámetros de URL → `utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`.
  - Editar el anuncio puede reiniciar la fase de aprendizaje (los días en que Meta prueba a quién mostrarlo). Pero hoy Meta no aprendió nada sobre compras, así que es el momento más barato para hacerlo.
- [ ] **Del resto, no toques nada.** No apagues anuncios, no subas ni bajes presupuestos (hoy son ~$21.000 por día entre los dos conjuntos [Calculado]) y no cambies textos ni públicos. Volvé a mirar cuando haya 1-2 días de compras medidas: si arreglás mañana, el martes 20 o el miércoles 21.

## Resultados por anuncio
La campaña es 1 (ORDI · Ventas), con 2 conjuntos: Caro (Caro 1 y Caro 3) y Silvia (Silvia 2). El export trae todas las columnas que hacen falta [Meta].

| Anuncio | Gasto | CTR | Gancho | CPC | Carritos | Compras | CPA | ROAS | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| Caro 1 · Placard caos (dolor) | $21.350 | 1,88% | 36,9% | $222 | 13 | 0 | — | — | **NO DECIDIR** |
| Caro 3 · Se arman en 10 s (demo) | $20.980 | 1,43% | 31,1% | $266 | 10 | 0 | — | — | **NO DECIDIR** |
| Silvia 2 · Una caja para cada rincón | $20.670 | 1,45% | 31,3% | $291 | 9 | 0 | — | — | **NO DECIDIR** |
| **Total cuenta** | $63.000 | 1,58% | 33,1% | $256 | 32 | 0 [Meta] · 7 [Shopify] | $9.000 | — | **AMARILLO** |

De dónde sale cada número:
- Gasto, carritos y compras: [Meta]. CTR, gancho, CPC (lo que pagás por cada clic) y CPA: [Calculado].
- El CPA total sale de las 7 ventas de Shopify y es un piso: si alguna vino por otro lado, el CPA real es más alto.
- El ROAS (cuántos pesos facturás por cada $1 de anuncios) queda en "—" hasta saber cuánto facturaron esas 7 ventas.

Por anuncio:
- **Caro 1 → NO DECIDIR**: sin compras medidas no se puede juzgar. Con lo que Meta sí mide, va adelante: 13 carritos y 8 pagos iniciados, a $2.669 cada pago iniciado [Calculado].
- **Caro 3 → NO DECIDIR**: 10 carritos y 6 pagos iniciados, a $3.497 cada uno [Calculado].
- **Silvia 2 → NO DECIDIR**: 9 carritos y 5 pagos iniciados, a $4.134 cada uno [Calculado].

Esa diferencia es una pista, no una decisión: con 5 a 8 pagos por anuncio todavía puede ser casualidad.

Aunque le creyeras a Meta, tampoco tocaba apagarlos. Cada uno gastó 1,5-1,6 CPA de equilibrio y tiene 5 a 8 pagos iniciados, y en ese caso la regla es esperar hasta 2.

Cuando Meta mida, contá desde el día del arreglo:
- El que gaste $27.000 (2 CPA de equilibrio) sin ventas, se corta.
- El que junte 3 ventas a $13.524 o menos cada una, se escala de a 20% por día.

CPA de equilibrio usado: **$13.524** [Calculado con el pack de 1 set a $34.900, que es el que menos deja; costo de $12.000 por set [Estimado] y los supuestos de `validacion/validacion-ordi.md`]. Los otros packs dejan más: 2 sets $20.524 · 3 sets $15.724 [Calculado].

ROAS de equilibrio: **2,58** (lo mínimo que tenés que facturar por cada $1 de anuncios para no perder).

## Dónde se cae la venta
15.540 impresiones → 246 clics (CTR 1,58%) → 215 visitas (87% de los clics) → 32 carritos (15% de las visitas) → 19 pagos iniciados (59% de los carritos) → **0 compras según Meta · 7 según Shopify** [Meta y Shopify; tasas Calculado].

Hasta el pago todo está sano, lejos de los mínimos orientativos (clic 0,8% · llegada 70% · carrito 4% · pago 40%). La venta no se cae: **lo que se pierde es el aviso de la compra**. Por ahora no hay nada que cambiar en la página ni en la oferta.

Un dato para mirar cuando el píxel ande: si las 7 ventas vinieron de los anuncios, terminaron 7 de 19 pagos iniciados (37% [Calculado]). Eso queda apenas abajo del 40% orientativo, y con una venta más ya estaría arriba.

## Próximos anuncios para probar
Son para **cuando Meta ya vea las compras** (1-2 días después del arreglo), no antes.

Salen de Caro 1: es el de mejor CTR (1,88%) y mejor gancho (36,9%) de la cuenta, y el que más carritos y pagos trae. Mantienen el mismo dolor (el placard que se desarma), la misma Caro y los bloques 2 y 3 de Caro 1 tal cual, con "Te dejo el link" y la oferta en texto. Solo cambian los primeros 3 segundos.

1. **Caro 1B · La pila que se cae** · Para Caro
   - Gancho (0-3 s), voz en off: "Sacás una remera y se te cae toda la pila." Sigue la avatar: "A mí me pasaba todos los días."
   - Qué se ve: sin avatar, plano fijo de una pila de remeras en el placard; una mano saca la de abajo y se derrumba todo. En el segundo 3 entra la avatar.
   - Texto en pantalla: "¿Tu placard también hace esto?" y después "Set x3 · 2 sets 14% OFF + guía de regalo".
   - Por qué: el dolor de Caro 1 es el que más frena el scroll (gancho 36,9%), y mostrarlo en vez de contarlo es la versión más directa. Es el error 1 del carrusel "5 errores".
2. **Caro 1C · El error** · Para Caro
   - Gancho (0-3 s): "Tu placard no se desordena solo: lo desordena este error." Sigue: "Y yo lo cometía todos los días."
   - Qué se ve: la avatar sobre el placard revuelto de Caro 1, levantando un dedo como quien cuenta un secreto.
   - Texto en pantalla: "El error que desarma tu placard en 3 días" y después la misma oferta.
   - Por qué: es el mismo dolor, con curiosidad (es la portada del carrusel "5 errores"). El bloque 2 de Caro 1 ("cada cosa en una caja, en vertical, a la vista") ya responde cuál es el error, así que no hay que tocar nada más.
3. **Caro 1D · 7:40 de la mañana** · Para Caro
   - Gancho (0-3 s): "Son las 7:40, llegás tarde y la remera negra no aparece." Sigue: "A mí me pasaba siempre."
   - Qué se ve: la avatar mirando la hora en el celular, apurada, sobre el placard revuelto.
   - Texto en pantalla: "7:40 · ¿y la remera negra?" y después la misma oferta.
   - Por qué: lleva el dolor de Caro 1 a un momento que Caro vive todas las mañanas. Lo que más quiere es "paz al abrir el placard a la mañana" (su buyer persona), y el texto 2 de `copys-meta-ads.txt` ya va por ese lado.

Presupuesto de los próximos 3-4 días [Calculado]:

| Conjunto | Anuncios | Gasto por día (7-9/10) | Próximos 3-4 días |
|---|---|---|---|
| Caro · mujeres 25-40 | Caro 1, Caro 3 | $14.110 | igual |
| Silvia · mujeres 32-50 | Silvia 2 | $6.890 | igual |
| Pruebas Caro 1 (conjunto nuevo) | Caro 1B, 1C, 1D | — | $0 hasta que Meta vea compras; después ~$6.762 por anuncio |
| **Total por día** | | **$21.000** | **$21.000** (~$41.300 con los 3 nuevos) |

Los nuevos van en un conjunto aparte, para no tocar los que ya andan, con ~½ CPA de equilibrio por día cada uno: así llegan a 2 CPA en 4 días. Si no te da el presupuesto, empezá con 2 ($13.524 por día) o de a uno.

## Datos que me faltaron
1. **El detalle de las 7 ventas.** Shopify → Pedidos → filtrá del 7 al 9 de octubre y contá solo los pagados (sin cancelados ni pruebas). De cada uno necesito:
   - cuánto pagó;
   - qué pack eligió (1, 2 o 3 sets);
   - de dónde vino: en el pedido, la tarjeta "Resumen de conversión" dice si la visita llegó desde Facebook o Instagram.

   Con eso saco el ROAS real y cuánto podés pagar por venta según lo que de verdad compran.
2. **El export actualizado, del 7 al 16 de octubre** (hasta ayer), desde la pestaña Anuncios con las mismas columnas, más las ventas de Shopify de esas fechas. El que me pasaste termina el 9: si la campaña siguió prendida, hay una semana más para mirar.
3. **Tu costo real por set**: sigue estimado en $12.000. Si fuera $15.000, el pack de 3 sets con envío gratis deja solo $6.724 y pagar $9.000 por venta ya no cierra; con 1 o 2 sets, sí [Calculado].
4. **Si sos monotributista**: el IVA (21%) que te cobran arriba del gasto de Meta es costo para vos. En ese caso el gasto real fue ~$76.230 y el CPA ~$10.890 [Calculado]: sigue cerrando, pero más justo. Lo ves en el resumen de la tarjeta o en la factura de Meta. Si sos responsable inscripto y computás el IVA, no cambia nada.
5. **Una captura del Administrador de eventos** con el evento Compra (si aparece y cuándo llegó por última vez): con eso te digo exactamente dónde está la falla.

Cuando me lo pases, lo vuelvo a correr y te digo qué cambió.
