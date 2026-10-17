# ORDI: no apagues los anuncios (todavía)

**Casi seguro lo que está roto es el píxel, no los anuncios.** Del 7 al 9 Meta registró 32 carritos y 19 pagos iniciados, pero ni una compra, y Shopify tiene 7 ventas esos mismos días. Antes de tocar nada, fijate de dónde vinieron esas 7 ventas y arreglá el evento de compra. Te lleva menos de una hora y no hace falta pausar nada.

## Por qué digo que es el píxel

Los 3 anuncios juntos, del 7 al 9/10 (gasto: $63.000):

| Paso | Cantidad | Tasa |
|---|---|---|
| Clics en el enlace | 246 | CTR 1,58% |
| Visitas a la página | 215 | 87% de los clics |
| Agregados al carrito | 32 | 15% de las visitas |
| Pagos iniciados | 19 | 59% de los carritos |
| Compras según Meta | **0** | 0% |
| Ventas en Shopify | **7** | 37% de los pagos iniciados |

- Hasta el pago anda todo bien: el CTR está muy por encima del 0,8% que pide el plan, casi 9 de cada 10 clics llegan a cargar la página y el 15% agrega al carrito.
- De los que inician el pago, en general termina comprando un 30–50%. Con 19 pagos iniciados esperarías **entre 6 y 9 compras**, y Shopify muestra 7. Que Meta vea 0 de 19 por azar es casi imposible, y el checkout funciona, porque Shopify vendió.
- Que los 3 anuncios den 0 compras y $0 de valor no quiere decir que los 3 sean malos. Quiere decir que a Meta no le llega el evento "Compra".
- Tampoco es una demora. Meta a veces tarda hasta 3 días en sumar compras (si exportaste el 9 o el 10, volvé a exportar hoy), pero no deja todo en cero.

> **Ojo con el plan.** Dice que hay que cortar cada anuncio que gastó $20.000–$27.000 sin ventas. Cada uno lleva unos $21.000, así que hoy cortarías los 3. Esa regla da por hecho que Meta cuenta bien las compras. Hasta que lo arregles, decidí mirando Shopify.

## 1. ¿De dónde vinieron las 7 ventas? (5 min)

En Shopify entrá a **Pedidos**, abrí cada pedido del 7 al 9 y mirá la tarjeta **"Resumen de conversión"**: ahí dice si la visita vino de Facebook o de Instagram. No cuentes tus pedidos de prueba ni los cancelados. Mirá también la columna **"Canal"**: si dice "Pedido en borrador", es un pedido que cargaste a mano (por ejemplo, una venta por WhatsApp), y esos el píxel nunca los ve.

| De las 7, ¿cuántas vinieron de Facebook/Instagram? | Costo por venta | Qué hacer |
|---|---|---|
| 5 a 7 | $9.000 – $12.600 | Te dejan plata aunque todas sean de 1 set (el equilibrio es $13.524). **Dejalos prendidos**, sin escalar hasta arreglar el píxel. |
| 3 o 4 | $15.750 – $21.000 | Estás en el límite: depende de cuántas personas llevaron 2 o 3 sets. Dejalos 3–4 días más con el píxel andando y decidí anuncio por anuncio. |
| 0 a 2 | $31.500 o más | No están vendiendo. En ese caso sí, cortá como dice el plan. |

- Si las 7 vinieron de los anuncios, después de pagar los anuncios te quedaron unos $31.700 o más en esos 3 días. Para tener el número exacto, sumá $13.524 por cada pedido de 1 set, $20.524 por cada uno de 2 sets y $15.524 por cada uno de 3, y restale $63.000 (⚠️ son márgenes con el costo estimado de $12.000 por set que usamos en la validación).
- Si alguna figura como "Directo" y no hiciste otra difusión (ORDI es nueva), seguramente también vino de un anuncio: el navegador de Instagram a veces no pasa de dónde viene la visita.
- Si los anuncios siguieron prendidos después del 9, hacé la misma cuenta hasta hoy.

## 2. ¿Qué está fallando en el píxel? (10 min)

Entrá al **Administrador de eventos**, abrí tu píxel (ahí figura como "conjunto de datos"), andá a **Información general** y buscá el evento **Compra (Purchase)** del 7 al 9:

- **No aparece o está en 0.** La tienda no le está mandando la compra a Meta. Lo más común es que el píxel esté pegado en el código del tema, en los "Scripts adicionales" del checkout o en una app de píxel que no está actualizada. Nada de eso funciona hoy en la página de "gracias por tu compra" de Shopify, y por eso a Meta le llegan el carrito y el pago iniciado, pero no la compra.
- **Aparece con compras.** El píxel funciona, pero los anuncios están mirando otro. Pasa cuando hay más de un píxel en el Business (por ejemplo, el de VERDEA). Revisá que el conjunto de anuncios (evento de conversión: Compra) y cada anuncio (en la sección Seguimiento) usen el mismo píxel que está conectado a la tienda de ORDI.

## 3. Cómo arreglarlo

1. En Shopify instalá o volvé a conectar la app oficial **Facebook & Instagram** (de Meta). Elegí el mismo píxel que usan los anuncios y poné el uso compartido de datos en **Máximo**. Eso prende la API de conversiones, que le manda la compra a Meta desde Shopify aunque el cliente no vuelva a la página de gracias (por ejemplo, si paga en Mercado Pago y cierra la ventana).
2. En **Configuración → Eventos de clientes**, el píxel de Facebook & Instagram tiene que decir "Conectado".
3. Borrá el código viejo del píxel (del tema, de "Scripts adicionales" o de otra app), así no se duplican los eventos.
4. **Probalo.** En el Administrador de eventos andá a **Probar eventos**, abrí la tienda desde ahí y hacé una compra de prueba (te sirve un código de 100% de descuento con envío gratis, y después cancelás el pedido). Tiene que aparecer "Purchase". Si no aparece ahí, fijate en Información general a los 20–30 minutos. No uses el Pixel Helper de Chrome para esto: en el checkout de Shopify el píxel corre aislado y la extensión puede no mostrar nada.
5. Poné **parámetros UTM** en los anuncios (en Seguimiento → Parámetros de URL):
   ```
   utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}
   ```
   Así cada pedido de Shopify te dice qué anuncio lo trajo, aunque el píxel vuelva a fallar. Podés ponerlos también en los 3 anuncios que ya tenés: como Meta no registró compras, siguen en aprendizaje y no perdés casi nada.

## Mientras tanto

- **No los apagues ni subas el presupuesto**: dejá el mismo hasta que la compra empiece a llegar.
- Arreglarlo es urgente por algo más que ver los números. La campaña optimiza por "Compra" y a Meta no le llega ninguna, así que no aprende a quién mostrarle los anuncios.
- Las compras que Meta no registró no se recuperan. Para estos días, la cuenta hacela con Shopify.
- Cuando el píxel ya registre las compras, esperá 3–4 días y volvé a usar las reglas del plan.

## Si después tenés que elegir un anuncio

Como no hay compras registradas, lo que más se acerca es el costo por pago iniciado:

| Anuncio | CTR | Pagos iniciados | Costo por pago iniciado |
|---|---|---|---|
| Caro 1 · Placard caos (dolor) | 1,88% | 8 | $2.669 |
| Caro 3 · Se arman en 10 s (demo) | 1,43% | 6 | $3.497 |
| Silvia 2 · Una caja para cada rincón | 1,45% | 5 | $4.134 |

Caro 1 viene mejor en todo y Silvia 2 es el más flojo. Pero con 5 a 8 pagos iniciados por anuncio, la diferencia todavía no alcanza para cortar ninguno.

## Dos detalles

- El CSV trae 3 anuncios (el plan tenía 4) y el conjunto de Silvia gastó unos $6.900 por día, cuando el plan decía $14.000. Si hay otro anuncio que no salió en la exportación, sumá lo que gastó. Con unos $84.000 en total, 7 ventas darían $12.000 por venta, que sigue por debajo del equilibrio.
- En `ORDI-organizacion-hogar/anuncios/plan-testeo-meta-ads.md`, los dos primeros puntos del checklist (conectar el píxel con la API de conversiones y probar el evento de compra) siguen sin tildar. Es justo lo que falta hacer.

Mandame las capturas del "Resumen de conversión" de los 7 pedidos y la del evento Compra en el Administrador de eventos, y te digo qué anuncio dejar y cuánto estás ganando de verdad.
