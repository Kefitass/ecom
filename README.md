# Casa del Oud · tema de Shopify

Tema de Shopify (Online Store 2.0) para **Casa del Oud**, con la identidad de marca propia (Oud, Jade, Terracota, Azafrán y Azulejo sobre Arena) y una landing oscura con dorado en cada producto. La guía de marca está en [`MARCA.md`](MARCA.md).
Todo se edita desde **Tienda online → Temas → Personalizar**, sin tocar código.

## Qué incluye

| Página | Secciones |
|---|---|
| **Todas** | Barra de anuncios animada · Franja "50% OFF" · Header oscuro (buscador, logo con etiqueta, Ayuda / Mi cuenta / Mi carrito, menú, "Seguí acá tu última compra") · Footer violeta con medios de pago y envío, Defensa del Consumidor y Botón de arrepentimiento · Botón flotante de WhatsApp |
| **Inicio** | Slider de banners · Instagram · Banners de categorías ("Combos de perfumes" / "Armá tu combo") · Videos "Compra seguro/a" (oculta hasta que subas videos) · Promociones actuales (grilla de 4) |
| **Catálogo** | Banner · Migas de pan · Ordenar por · Filtros (marca, precio) · Grilla de tarjetas |
| **Producto** | Galería con miniaturas, sello, precio tachado, precio, precio con transferencia, "Ahorrás un 5%", cuotas, envío gratis y botón de compra. Debajo va la **landing oscura**: portada 3X1, oferta, "Así llega tu pedido", "Uno para cada ocasión", "¿Por qué los árabes?", lista con tildes, "Los tres, uno por uno", "Qué incluye", "Hacé la cuenta" (oculta), "Tu combo" y "Comprá tranquilo". Después: reseñas (app), preguntas frecuentes y productos similares |
| **Otras** | Carrito, contacto, búsqueda, blog, 404 y contraseña |

Las **tarjetas de producto** muestran el sello de esquina, % OFF, ENVÍO GRATIS, estrellas (si usás una app de reseñas), precio tachado + precio, precio con TRANSFERENCIA y cuotas sin interés.

## Cómo subirlo a Shopify

**Opción A, conectado a GitHub (recomendada).**
1. En Shopify: **Tienda online → Temas → Agregar tema → Conectar desde GitHub**.
2. Elegí el repositorio `kefitass/ecom` y la rama.

**Opción B, ZIP.**
1. Descargá el repo como ZIP. El ZIP tiene que tener en la raíz las carpetas `layout`, `sections`, `templates`, etc. La carpeta `importar` no hace falta.
2. En Shopify: **Temas → Agregar tema → Subir archivo zip**.

## Cargar los productos con los precios

`importar/productos.csv` trae 5 combos árabes con los precios de la página de referencia:

| Combo | Precio | Tachado |
|---|---|---|
| 3x1 Asad | $79.990 | $160.000 |
| 3x1 Hawas | $79.990 | $160.000 |
| 3x1 Árabes mujer | $84.990 | $170.000 |
| 3x1 Árabes unisex | $84.990 | $170.000 |
| 3x1 Árabes de verano | $84.990 | $170.000 |

Para importarlos: **Productos → Importar → subir `productos.csv`**. Después les cargás las fotos.

> El stock viene en 20 unidades por producto: cambialo por tu stock real.

## Primeros pasos

1. **Configuración del tema → Logo**: logo en PNG con letras claras, más la etiqueta de abajo (por ejemplo, PROMO 3X1 o CYBER MONDAY).
2. **Configuración del tema → Contacto y redes**: WhatsApp, email, usuario y link de Instagram.
3. **Configuración del tema → Cuotas y transferencia**: 3 cuotas y 5% por transferencia ya vienen activados. El descuento real por transferencia se configura en Shopify.
4. **Navegación**: menú `main-menu` (Inicio, Productos, Seguir mi pedido, Contacto) y menú `footer`.
5. **Páginas → Contacto**: asignale la plantilla `page.contact`.
6. **Pie de página**: CUIT y link del **Botón de arrepentimiento**, que es obligatorio en Argentina.
7. **Reseñas**: instalá una app de reseñas (por ejemplo Judge.me, que es gratis) y agregá su bloque en la sección "Apps (reseñas, etc.)" del producto.

## Etiquetas especiales del producto

- `badge:MÁS VENDIDO` muestra la etiqueta arriba a la izquierda de la foto (también sirve `badge:NUEVO`, `badge:EN TENDENCIA`, etc.).
- El **% OFF** se calcula solo con el precio tachado.

## Landing por producto

La plantilla `product` trae la landing oscura completa, y `product.simple` es solo el producto, sin landing.
Para tener una landing distinta por combo: en el editor, **Productos → Crear plantilla** (basada en `product`), editá los textos y fotos, y asignala al producto.
