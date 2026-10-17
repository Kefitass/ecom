# Cómo sacar los datos: export de Meta, capturas y ventas de Shopify

Pasale estas instrucciones al usuario, tal cual o resumidas, cuando falte un dato. Los nombres de los botones
cambian un poco según la versión y el idioma de la cuenta: si algo no aparece con ese nombre, que busque el
parecido.

## 1. Export del Administrador de anuncios (lo ideal)

1. Entrá al **Administrador de anuncios** (adsmanager.facebook.com, o desde Meta Business Suite →
   Todas las herramientas → Administrador de anuncios) desde la compu. Arriba a la izquierda, elegí la cuenta
   publicitaria correcta.
2. **Fechas**: arriba a la derecha, elegí el período del análisis (por ejemplo, del primer día del test hasta
   **ayer**). Mejor no incluir hoy: el día en curso está incompleto.
3. Tildá la campaña que querés analizar y pasá a la pestaña **Anuncios** (no Campañas ni Conjuntos): el
   diagnóstico se hace anuncio por anuncio.
4. **Columnas**: botón **Columnas: Rendimiento** → **Personalizar columnas**. Buscá cada una por nombre y tildala:

   | En español | En inglés | Para qué sirve |
   |---|---|---|
   | Importe gastado | Amount spent | todo |
   | Impresiones | Impressions | CPM, CTR, gancho |
   | Alcance | Reach | frecuencia |
   | Frecuencia | Frequency | cansancio del público |
   | CPM (costo por mil impresiones) | CPM (cost per 1,000 impressions) | costo de mostrarse |
   | Clics en el enlace | Link clicks | CTR, CPC |
   | CTR (porcentaje de clics en el enlace) | CTR (link click-through rate) | gancho del anuncio |
   | CPC (costo por clic en el enlace) | CPC (cost per link click) | costo del clic |
   | Reproducciones de video de 3 segundos | 3-second video plays | gancho (videos) |
   | ThruPlays | ThruPlays | retención (videos) |
   | Visitas a la página de destino | Landing page views | si la página carga |
   | Artículos agregados al carrito | Adds to cart | tasa de carrito |
   | Pagos iniciados | Checkouts initiated | tasa de pago |
   | Compras | Purchases | CPA |
   | Valor de conversión de compras | Purchases conversion value | ROAS y ticket promedio |
   | ROAS (retorno de la inversión en publicidad) de compras | Purchase ROAS | control |

   Los de carrito, pagos y compras están en la sección de **Conversiones** (eventos del sitio web): en cada
   fila tildá **Total**, y en Compras también **Valor**. En la sección **Configuración** de la misma ventana
   sumá **Nombre de la campaña** y **Nombre del conjunto de anuncios** (hacen falta para el presupuesto por
   conjunto).
5. Abajo a la izquierda tildá **Guardar como preset**, ponele de nombre "Diagnóstico" y tocá **Aplicar**. La
   próxima vez elegís "Columnas: Diagnóstico" y listo.
6. **Desglose (opcional)**: **Desglose → Por tiempo → Día** muestra la evolución diaria. El script la suma por
   anuncio y además detecta si el público se está cansando (CPM que sube, CTR que baja).
7. **Exportar**: botón **Exportar** (o **Informes → Exportar datos de la tabla**) → elegí **.csv** o **.xlsx** →
   **Exportar**. Mandá el archivo tal como baja, sin abrirlo y guardarlo de nuevo (Excel a veces cambia los
   números o el separador).

## 2. Si solo podés mandar capturas

- Desde la compu, pestaña **Anuncios**, con las columnas del preset "Diagnóstico".
- Que se vean **las fechas** (arriba a la derecha) y **la fila de totales** de abajo.
- Si no entran todas las columnas, mandá 2 capturas corriendo la tabla hacia la derecha; que en las dos se vea el
  nombre del anuncio.
- Desde el celular se ven menos columnas: sirve para un vistazo, no para decidir.

Lo que la captura no muestra (carritos, pagos, reproducciones de 3 s) no se completa a ojo: se pide.

## 3. Ventas de Shopify del mismo período (para controlar el píxel)

- **Shopify → Pedidos**: filtrá por fecha (el mismo período del export) y contá los pedidos **pagados**, sin
  cancelados ni pruebas. Si en Shopify se puede filtrar por canal o por "Facebook / Instagram", mejor.
- Alternativa: **Análisis → Informes → Ventas a lo largo del tiempo** (o "Pedidos a lo largo del tiempo") con el
  mismo período.
- Para cruzar el embudo: en **Análisis**, la tarjeta **Tasa de conversión** muestra cuántas sesiones agregaron
  al carrito, llegaron al pago y compraron. Si los agregados al carrito de Shopify son muchos más que los de
  Meta, el evento de carrito de Meta no está disparando bien.

## 4. Saber qué anuncio trajo cada venta (UTM)

En cada anuncio, sección **Seguimiento → Parámetros de URL**, pegá:

```
utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

Desde ahí Shopify registra de qué campaña y de qué anuncio viene cada visita y cada venta (**Marketing →
Atribución**, o en **Análisis → Informes** buscando "UTM"). Es lo que permite decidir por anuncio cuando el
píxel falla.

## 5. Problemas comunes del export

- **Exportó desde la pestaña Campañas**: solo trae el total. Pedí el export desde **Anuncios**.
- **Hay "Resultados" en vez de "Compras"**: solo sirve si el objetivo de la campaña es Ventas optimizando por
  compra; si es Tráfico o Interacción, "Resultados" son clics o interacciones, no ventas.
- **El gasto dice (USD)**: la cuenta está en dólares. Hace falta el tipo de cambio que realmente cobra la tarjeta
  (`--tipo-cambio`).
- **Nombres de columna distintos** ("Compras en el sitio web", "Agregados al carrito en el sitio web"): el
  script reconoce las variantes habituales en español e inglés; si alguna no la toma, avisa en
  "FALTAN COLUMNAS".
- **Ventana de atribución cambiada**: por defecto Meta usa 7 días después del clic y 1 día después de ver el
  anuncio. Si alguien la cambió, las compras de Meta no se comparan igual con Shopify.
