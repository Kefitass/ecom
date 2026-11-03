# Perfumería de Barrio · tema de Shopify

Tema de Shopify (Online Store 2.0) hecho a medida para **Perfumería de Barrio**, una tienda de perfumes árabes.
Todo se edita desde el personalizador de Shopify (**Tienda online → Temas → Personalizar**), sin tocar código.

## Qué incluye

| Página | Secciones |
|---|---|
| **Inicio** | Barra de anuncios animada · Encabezado · Hero con sello de oferta · Barra de confianza · Productos destacados · Beneficios · Opiniones (oculta hasta que cargues reseñas reales) · Preguntas frecuentes · Llamado a WhatsApp · Pie |
| **Catálogo** | Título, chips de beneficios y tarjetas con puntaje, precio, cuotas, línea de oferta y botón |
| **Producto** | Galería, precio con % OFF, cuotas, selector de variantes (ej: packs x1 / x2 / x3), botón de compra, "Comprar ahora", consulta por WhatsApp y desplegables |
| **Contacto** | Tarjeta de WhatsApp, datos de contacto y formulario |
| **Carrito, búsqueda, blog, 404 y contraseña** | Con el mismo estilo |

Además, en todas las páginas aparece el botón flotante de WhatsApp.

## Cómo subirlo a Shopify

**Opción A, conectado a GitHub (recomendada).** Cada cambio en el repo se actualiza solo.
1. En Shopify: **Tienda online → Temas → Agregar tema → Conectar desde GitHub**.
2. Elegí el repositorio `kefitass/ecom` y la rama.

**Opción B, subir un ZIP.**
1. Descargá el repo como ZIP. El ZIP tiene que tener en la raíz las carpetas `layout`, `sections`, `templates`, etc.
2. En Shopify: **Tienda online → Temas → Agregar tema → Subir archivo zip**.

## Primeros pasos después de instalarlo

1. **Configuración del tema → Logo**: subí tu logo.
2. **Configuración del tema → Contacto y redes**: cargá tu WhatsApp (con +54 9…), email e Instagram.
3. **Configuración del tema → Colores**: si querés, cambiá la paleta (por defecto bordó + ámbar).
4. **Navegación**: el menú `main-menu` debería tener *Inicio*, *Catálogo* y *Contacto*, y el menú `footer` las páginas de ayuda.
5. **Páginas → Contacto**: en la página de contacto, elegí la plantilla **page.contact**.
6. **Hero**: subí la foto principal y ajustá el puntaje y la cantidad de clientes **con tus números reales**.
7. **Opiniones**: cargá reseñas reales de clientes y recién ahí activá la sección.

## Etiquetas especiales en los productos

En cada producto, en el campo **Etiquetas**:

- `badge:HASTA 35% OFF EN PACKS` muestra el sello naranja sobre la foto.
- `promo:Llevá 2 y ahorrá 30% · Llevá 3: 35% OFF + envío gratis` muestra la línea de oferta y cambia el botón a **"Ver ofertas"** (naranja).

Si el producto tiene precio de comparación (precio tachado) y no tiene `badge:`, se muestra solo el **% OFF**.

> Las promos "Llevá 2 / Llevá 3" solo se anuncian desde el tema. El descuento en sí se crea en **Shopify → Descuentos** (por ejemplo, un descuento automático por cantidad).

## Cuotas y transferencia

En **Configuración del tema → Cuotas y transferencia** elegís la cantidad de cuotas sin interés, si se muestra el valor de cada cuota y, opcionalmente, el precio con descuento por transferencia.
