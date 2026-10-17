# Fuentes de datos para Argentina

Para cada fuente: cómo consultarla, qué anotar y qué pedirle al usuario si no podés entrar.
Muchas de estas páginas bloquean el acceso automático (login, captcha, "403"). Eso es normal:
no lo escondas, pedí la captura y seguí con el resto.

## 1. Mercado Libre Argentina (la más importante)

**Cómo buscar**
- Búsqueda web: `https://listado.mercadolibre.com.ar/<producto-con-guiones>` (ej: `.../enraizante-organico`).
- Ordenar por relevancia (default) y mirar los primeros 10-20 resultados.
- API pública (a veces pide token): `https://api.mercadolibre.com/sites/MLA/search?q=<producto>&limit=50`.
  Si responde, sirven `results[].price`, `title`, `shipping.free_shipping`, `seller`, `available_quantity`.
- Si no podés abrir nada de ML, usá la búsqueda web general con `site:mercadolibre.com.ar <producto>`
  para al menos ver títulos y precios indexados.

**Qué anotar**
- Cantidad aproximada de resultados (indica oferta, no demanda).
- De los 5-10 primeros: precio, "+X vendidos" (ML muestra rangos: +5, +25, +50, +100, +500, +1000…),
  reputación del vendedor, si es Full, envío gratis, cuotas sin interés, y si es la misma foto/producto
  repetido por muchos vendedores (señal de saturación).
- Rango de precios (mínimo, típico, máximo).
- Preguntas de las publicaciones más vendidas: son las dudas y objeciones reales del comprador argentino.

**Cómo leerlo**
- Varios vendedores con "+500 vendidos" o más → demanda probada.
- Todos venden la misma foto al mismo precio bajo → saturado; solo entra con diferenciación.
- Pocas publicaciones y ninguna con ventas → puede ser oportunidad o falta de demanda; necesita otra señal (Trends, anuncios).

**Captura a pedir si está bloqueado**
> "Entrá a mercadolibre.com.ar, buscá "<producto>" y mandame una captura de los primeros resultados
> (que se vean precios y la cantidad de vendidos). Si podés, abrí la publicación más vendida y mandame
> también una captura de la sección de Preguntas."

## 2. Google Trends (estacionalidad y tendencia)

**Cómo buscar**
- `https://trends.google.com/trends/explore?geo=AR&q=<término>&date=today%2012-m`
- Probá 2-3 términos como los diría un argentino (ej: "enraizante", "hormona de enraizamiento", "esquejes").
- Comparar con los últimos 5 años (`date=today%205-y`) muestra si es moda pasajera o demanda estable.

**Qué anotar**
- Tendencia: subiendo / estable / bajando.
- Picos por temporada y en qué meses (hemisferio sur: primavera sep–nov, verano dic–feb, otoño mar–may, invierno jun–ago).
- Si estamos entrando o saliendo de la temporada fuerte (afecta cuándo conviene testear).

**Captura a pedir si está bloqueado**
> "Entrá a trends.google.com, poné "<término>", elegí Argentina y "últimos 12 meses",
> y mandame una captura del gráfico."

## 3. Biblioteca de Anuncios de Meta (competencia que pauta)

**Cómo buscar**
- `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AR&q=<producto>&search_type=keyword_unordered`
- Suele requerir navegador real; casi siempre vas a necesitar capturas.

**Qué anotar**
- Cuántos anunciantes distintos lo pautan.
- Anuncios activos hace **más de 30 días** (la fecha "Circulando desde…"): son las señales más fuertes de que es rentable.
- Ángulos y ganchos que usan, formato (video UGC, imagen, carrusel), ofertas y precios.
- Si varios anuncios usan el mismo video: producto muy copiado.

**Captura a pedir**
> "Entrá a facebook.com/ads/library, elegí país Argentina, tipo "Todos los anuncios", buscá "<producto>"
> y mandame capturas de los anuncios que aparezcan. Lo más importante es que se vea la fecha
> "Circulando desde" de cada uno."

## 4. Tiendas propias en Argentina

**Cómo buscar**
- Búsqueda web: `"<producto>" comprar argentina`, `"<producto>" cuotas sin interés`,
  `"<producto>" site:mitiendanube.com`, `"<producto>" myshopify`.

**Qué anotar**
- Precio y oferta (packs, 2x1, envío gratis), calidad de la página, si muestran reseñas.

## 5. Redes (TikTok / Instagram)

**Cómo buscar**
- Búsqueda web: `"<producto>" tiktok argentina`, hashtags en español.
- Mirá si hay creadores argentinos mostrándolo y qué comentan (preguntas de precio, "¿dónde lo consigo?" = demanda).

## 6. Proveedor

- Si el usuario pasa link de AliExpress/Temu/Alibaba: precio, opciones de envío a Argentina, tiempos,
  valoraciones del producto y del vendedor, cantidad de pedidos.
- Para traer stock a Argentina, contemplá costo de importación y los límites del régimen de envíos
  vigente (cambia seguido: verificar). Si el usuario compra a un proveedor local, pedí ese costo.
