# Dónde se cae la venta: diagnóstico del embudo

Contenido: 1. Cómo leer el embudo · 2. En el anuncio · 3. Entre el clic y la página · 4. En la página ·
5. En el carrito y el pago · 6. En el público · 7. Medición · 8. Señales propias de Argentina

## 1. Cómo leer el embudo

Recorrelo de arriba para abajo: impresiones → clics en el enlace → visitas a la página → agregados al carrito →
pagos iniciados → compras. La primera etapa que queda claramente por debajo de lo normal es el cuello de botella:
arreglá esa primero, porque mejorar una etapa de más abajo no sirve si arriba no pasa nadie.

Compará también entre anuncios:
- **Todos se caen en la misma etapa** → el problema es común a todos: página, oferta, precio o medición.
- **Solo uno se cae** → es ese anuncio: su gancho, o una promesa que la página no cumple.

Antes de culpar a la página o a los anuncios por "no vender", descartá la medición (sección 7).

## 2. En el anuncio (gancho o CTR bajos)

Síntomas: gancho menor a 25%, CTR del enlace menor a 0,8%, CPC muy por encima del resto de la cuenta.

| Patrón | Qué pasa | Qué cambiar |
|---|---|---|
| Gancho flojo y CTR flojo | No frena el scroll | Los primeros 3 s: arrancar con el problema o el resultado, no con un saludo o el logo; texto grande en pantalla |
| Gancho bueno, CTR flojo | Entretiene pero no vende | Mostrar antes el producto y la oferta; decir para quién es; cierre claro (en VERDEA, suave) |
| Gancho bueno, retención floja | El medio aburre | Cortar más, mostrar el resultado antes, un solo mensaje por video |
| CTR bueno, nadie compra (solo ese anuncio) | La promesa atrae a curiosos o no coincide con la página | Mismo gancho con otra promesa o demostración |

Regla para iterar: cambiar **una sola cosa** por variante (casi siempre los primeros 3 s) y dejar igual el resto,
para saber qué funcionó.

## 3. Entre el clic y la página (llegada menor a 70%)

Muchos clics que nunca ven la página. Causas típicas: página lenta en el celular (imágenes pesadas, muchas
apps, video de fondo), link roto o que lleva a la página de inicio, redirecciones, clics sin querer en
ubicaciones como Audience Network.

Cómo confirmarlo: abrir el link del anuncio desde el celular con datos móviles; probar la página en PageSpeed
Insights; mirar en Shopify el informe de velocidad de la tienda. Si los clics vienen de una ubicación rara,
desglosar el informe por ubicación.

## 4. En la página (muchos clics, pocos carritos)

Es el caso de "me entran clics pero nadie compra". Si el CTR es bueno y la tasa de carrito es menor a 4%, los
anuncios ya hicieron su trabajo: **cortarlos no arregla nada**. Lo honesto es frenar o bajar el gasto, arreglar
la página y volver a prender los mismos anuncios.

Revisá en este orden (de lo que más pesa a lo que menos):
1. **Que funcione**: en el celular, el botón de agregar al carrito anda, las variantes y el stock están bien,
   Kaching aplica el pack y el precio correcto, y no hay pop-ups que tapen el botón. Compará los agregados al
   carrito de Shopify (Análisis → Tasa de conversión) con los de Meta: si Shopify tiene muchos más, es el
   evento de Meta el que falla, no la página.
2. **Que la página cumpla la promesa del anuncio**: lo primero que se ve tiene que ser lo mismo que prometió el
   anuncio (el problema, el resultado, el producto de la imagen).
3. **Primera pantalla del celular**, sin bajar: qué es, para quién, el beneficio principal, el precio con la
   oferta y el botón.
4. **Precio contra el mercado**: buscá el producto o uno parecido en Mercado Libre. Si el tuyo cuesta más del
   doble, la página tiene que justificarlo (cuánto rinde, precio por uso, garantía, regalo, pack) o hay que
   probar otra oferta. Con un CTR alto y casi ningún carrito, el precio es el primer sospechoso.
5. **Confianza**: reseñas reales con foto (nunca inventadas), garantía de devolución clara, medios de pago y
   cuotas visibles, WhatsApp a mano, envío y plazos de entrega claros.
6. **Oferta**: los packs se entienden de un vistazo (el x2 marcado como el más elegido), las cuotas sin interés
   se ven arriba, y el envío gratis desde cierto monto está bien a la vista.
7. **Velocidad** (sección 3).

Un cambio por vez y medido: dejá correr cada cambio al menos unas 300-500 visitas antes de comparar la tasa de
carrito (es orientativo; con pocas visitas, cualquier diferencia es casualidad).

## 5. En el carrito y el pago (oferta y precio)

**Carrito → pago bajo (menos de 40%)**: algo sorprende en el carrito. Envío que aparece recién ahí, precio final
más alto que el esperado, el descuento del pack que no se ve, apps de "agregá esto también" que distraen, carrito
lento.

**Pago → compra bajo (menos de 40%)**: medios de pago (falta Mercado Pago, transferencia o las tarjetas de
siempre), cuotas sin interés que no aparecen en el pago, tarjetas rechazadas, pedir crear una cuenta, costo de
envío final, poca confianza en el último paso. Activá los mensajes de carrito y pago abandonados (mail y
WhatsApp; si la marca los tiene, están en `<MARCA>/mensajes/`).

Si hay muchos pagos iniciados y Shopify tiene ventas que Meta no ve, no es el checkout: es la medición.

## 6. En el público (cansancio)

Señales: frecuencia mayor a 2,5 en 7 días con públicos fríos, CPM que sube y CTR que baja día a día (el script lo
calcula si el export viene por día), comentarios del tipo "otra vez este anuncio".

Qué hacer: anuncios nuevos con el mismo ángulo y otro gancho, público más amplio (Advantage+ o sin intereses),
excluir a quienes ya compraron y llevar el remarketing a un conjunto aparte. Con presupuestos chicos, el
cansancio casi nunca aparece en las primeras 2 semanas; si aparece, suele ser un público demasiado chico.

## 7. Medición (píxel y API de conversiones)

Síntomas: Shopify tiene ventas y Meta muestra 0 o muchas menos; pagos iniciados sin compras; compras sin valor;
muchos clics y 0 carritos; Meta cuenta más compras que Shopify (duplicado).

Qué revisar, en orden:
1. **Shopify → app Facebook & Instagram** (la de Meta): que esté conectada a la cuenta publicitaria y al píxel
   (conjunto de datos) que usa la campaña. En la configuración de **uso compartido de datos**, elegir el nivel
   más alto (Máximo): activa la API de conversiones, que manda las compras desde el servidor. Es clave en
   Argentina, porque quien paga con Mercado Pago muchas veces no vuelve a la página de "gracias por tu compra",
   y sin la API esa venta no se registra.
2. **Administrador de eventos** de Meta → el conjunto de datos → **Información general**: que lleguen
   Purchase, InitiateCheckout y AddToCart en las últimas horas, idealmente por "Navegador" y por "Servidor".
3. **Probar eventos**: hacer una compra de prueba (o una compra real chica) y ver que llegue Purchase con el valor
   en pesos.
4. **Duplicados**: si el píxel está pegado a mano en el tema y además conectado por la app, Meta cuenta doble.
   Dejá solo la app.
5. **La campaña optimiza por Compra** en el conjunto de datos correcto (configuración del conjunto → evento de
   conversión).
6. **Dominio verificado** en la configuración del negocio (Seguridad de la marca → Dominios).

Mientras la medición está rota: no se apaga nada por "no vender", se juzga con las ventas de Shopify (y con UTM
para saber de qué anuncio vino cada una; ver `exportar-informe-meta.md`), y Meta optimiza a ciegas, así que
arreglarlo es lo más urgente. Después del arreglo, esperá 1-2 días de datos correctos antes de decidir por ventas.

## 8. Señales propias de Argentina

- **Fechas fuertes**: Hot Sale (mayo), Día del Padre (junio), Día del Niño (agosto), Día de la Madre (octubre),
  CyberMonday (noviembre), Black Friday y Navidad. Suben el CPM y también las ganas de comprar: compará contra las
  mismas semanas, no contra el mes anterior.
- **Precios y CPM en pesos** se mueven con la inflación y el dólar: compará con las últimas 2-4 semanas de la
  propia cuenta, no con números viejos.
- **Cuotas sin interés**: si no se ven en la página y en el pago, se pierden ventas; su costo ya está en el CPA de
  equilibrio.
- **Envío**: el costo y el plazo de entrega claros desde la página reducen el abandono en el carrito.
- **Mercado Pago**: ver Medición, punto 1.
