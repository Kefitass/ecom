# Métricas, referencias y reglas de decisión

Contenido: 1. Fórmulas · 2. Referencias orientativas · 3. CPA y ROAS de equilibrio · 4. Impuestos sobre el
gasto en anuncios · 5. Reglas de decisión y su porqué · 6. Semáforo · 7. Presupuesto y escalado ·
8. Fase de aprendizaje

## 1. Fórmulas

| Métrica | Fórmula |
|---|---|
| CPM | gasto × 1.000 ÷ impresiones |
| CTR del enlace | clics en el enlace ÷ impresiones |
| CPC | gasto ÷ clics en el enlace |
| Gancho | reproducciones de video de 3 s ÷ impresiones |
| Retención | ThruPlays ÷ reproducciones de 3 s |
| Llegada a la página | visitas a la página de destino ÷ clics en el enlace |
| Tasa de carrito | agregados al carrito ÷ visitas a la página (o ÷ clics si no hay visitas) |
| Tasa de pago | pagos iniciados ÷ agregados al carrito |
| Tasa de compra | compras ÷ pagos iniciados |
| CPA | gasto ÷ compras |
| ROAS | valor de las compras ÷ gasto |
| Ticket promedio | valor de las compras ÷ compras |
| Frecuencia | impresiones ÷ alcance |

Siempre sobre sumas del período, nunca promediando porcentajes (el promedio de los CTR de cada día no es el
CTR del período). Si el export viene por día, el alcance sumado repite personas: la frecuencia queda aproximada.

## 2. Referencias orientativas

Son puntos de partida generales de ecommerce con anuncios en Meta, **no leyes**: cambian con el producto, el
precio, la temporada y la cuenta. Un producto caro convierte menos y banca un CPA más alto; uno barato, al
revés. Cuando las uses, decí que son orientativas y priorizá el promedio de la propia cuenta.

| Métrica | Flojo | Bueno |
|---|---|---|
| CTR del enlace | menos de 0,8% (menos de 0,5% con 2.000+ impresiones: muerto) | 1,5% o más |
| Gancho | menos de 25% | 35% o más |
| Retención (ThruPlay ÷ 3 s) | menos de 12% | 25% o más |
| Llegada a la página | menos de 70% | 85% o más |
| Tasa de carrito | menos de 4% | 8% o más |
| Tasa de pago | menos de 40% | 60% o más |
| Tasa de compra | menos de 40% | 60% o más |
| Frecuencia (7 días, público frío) | más de 2,5 | menos de 1,8 |

**CPM**: en pesos no hay una referencia fija que sirva (se mueve con la inflación, el dólar y la temporada).
Comparalo contra la propia cuenta en las últimas 2 a 4 semanas. Sube en fechas fuertes: Hot Sale (mayo), Día del
Padre (junio), Día del Niño (agosto), Día de la Madre (octubre), CyberMonday (noviembre), Black Friday y Navidad.

## 3. CPA y ROAS de equilibrio

Es la misma fórmula de `economia.py` de validar-producto-ar:

```
margen = precio − (costo × unidades + envío absorbido + empaque
                   + precio × (pasarela + cuotas + plataforma + impuestos + devoluciones))
CPA de equilibrio = margen          ROAS de equilibrio = precio ÷ margen
```

Por defecto: pasarela 7%, cuotas sin interés 8%, plataforma 2%, impuestos 4%, devoluciones 3%, empaque $1.000.
Cambian seguido: si el usuario tiene sus porcentajes reales, van esos.

**Con packs** (Kaching), cada pack tiene su propio CPA de equilibrio. Ejemplo ORDI, costo $12.000, envío gratis
en x3 que cuesta $8.000: x1 $34.900 → margen $13.524 · x2 $59.900 → $20.524 · x3 $79.900 → ~$15.700 (la
validación de ORDI dice $15.524: diferencia de supuestos de envío). Con ventas, el script deduce qué packs se
vendieron a partir del valor de las compras de cada anuncio (por ejemplo, 5 compras por $269.500 = 2 de x1, 2 de
x2 y 1 de x3) y usa el margen promedio de esa mezcla: en el ejemplo de ORDI, $17.838. Si el valor no cierra
exacto (incluye envío pagado por el cliente o cupones), interpola según el ticket promedio, que es una
aproximación: si la mayoría compra x2, el equilibrio sube. Sin ventas, usa el pack que menos deja, que es lo
prudente.

**Margen cero o negativo**: el producto pierde plata antes de pagar un solo anuncio. Ningún anuncio lo arregla:
hay que subir el precio, bajar el costo o cambiar la oferta (semáforo ROJO).

## 4. Impuestos sobre el gasto en anuncios

El "Importe gastado" del Administrador **no incluye impuestos**. En Argentina, al pago de servicios digitales del
exterior se le suma el IVA (21%) que percibe la tarjeta y, según la provincia, percepciones de Ingresos Brutos;
si la cuenta está en dólares, puede haber además percepciones por compras en moneda extranjera. Lo que el
usuario realmente paga está en el resumen de la tarjeta o en la factura de Meta.

- **Responsable inscripto** que computa el IVA como crédito fiscal: el costo real es casi el importe gastado.
- **Monotributista**: el IVA y las percepciones son costo. Usá `--recargo-anuncios` con el porcentaje real
  (por ejemplo 0.21, o más si hay percepciones). Sin ese dato, avisá que el CPA real es más alto que el que
  muestra Meta.

Estas reglas cambian: si lo usás, mencioná que conviene verificarlo con su contador o su resumen.

## 5. Reglas de decisión y su porqué

El script aplica las reglas en este orden (la primera que se cumple decide):

1. **Faltan compras o costo/precio** → FALTAN DATOS (salvo CTR muerto con 2.000+ impresiones: CORTAR).
2. **Margen cero o negativo** → SIN MARGEN.
3. **Medición rota** (Shopify con ventas, Meta con 0) → NO DECIDIR.
4. **Fuga en la página** (toda la cuenta: CTR de 0,8% o más, 200+ clics, tasa de carrito menor a 4%, sin ser
   rentable y con 2+ CPA de equilibrio gastados) → PAUSAR los anuncios con buen CTR; los de CTR flojo siguen las
   reglas de abajo.
5. **Sin ventas**:
   - menos de 1 CPA gastado → NO TOCAR (salvo CTR menor a 0,5% con 2.000+ impresiones → CORTAR);
   - 1 CPA o más y no engancha (CTR menor a 0,8% y gancho menor a 25%) → CORTAR;
   - entre 1 y 1,5 CPA → MANTENER, o ITERAR si el gancho o el CTR están flojos;
   - entre 1,5 y 2 CPA con 2+ pagos iniciados → MANTENER hasta 2;
   - 1,5 CPA o más con muy buen gancho (CTR de 1,5% o más, o gancho de 35% o más) → ITERAR: el gancho sirve, la
     promesa o la demostración no;
   - si no → CORTAR.
6. **1-2 ventas**: menos de 1 CPA gastado → NO TOCAR (prometedor, no subir); CPA por debajo del de equilibrio →
   MANTENER hasta llegar a 3 ventas; 3+ CPA gastados → CORTAR; si no → MANTENER (vende caro, vigilar).
7. **3 o más ventas**: CPA hasta el de equilibrio → ESCALAR (con menos de 3 días de datos, MANTENER hasta el
   día 3); CPA mayor a 1,5 veces → CORTAR; en el medio → ITERAR si el gancho es flojo, MANTENER si está hasta
   1,2 veces, ITERAR si no.

**Por qué esperar 1 CPA y cortar entre 1,5 y 2.** Si un anuncio vende justo en equilibrio, hace en promedio
1 venta por cada CPA de equilibrio gastado. La chance de que todavía no haya vendido nada, por pura suerte, es:

| Gasto, en CPA de equilibrio | 0,5 | 1 | 1,5 | 2 | 3 |
|---|---|---|---|---|---|
| Chance de 0 ventas aunque el anuncio sea "de equilibrio" | 61% | 37% | 22% | 14% | 5% |

Con menos de 1 CPA, 0 ventas no dice nada. A partir de 1,5–2, es más probable que el anuncio sea malo que
desafortunado, y seguir pagándolo cuesta más que perder un anuncio que quizás era bueno.

**Por qué 3 ventas para escalar.** Con 1 venta, el CPA real puede ser la mitad o el doble del que se ve, por
casualidad. Con 3 ya hay una señal; con 10, una certeza razonable.

**Señales que no son decisiones pero importan**: pagos iniciados sin compra (alguien casi compra: mirar el
checkout), CTR muy por debajo del resto de la cuenta, frecuencia arriba de 2,5 en el ganador (preparar su
reemplazo antes de que se canse), CPM que sube y CTR que baja día a día.

## 6. Semáforo

- **VERDE**: 3+ ventas y CPA total menor o igual al de equilibrio.
- **ROJO**: margen negativo; fuga en la página (punto 4); 0 ventas con 3+ CPA gastados; o CPA total mayor a
  1,5 veces el de equilibrio con 3+ CPA gastados. Con medición rota: ROJO si aun con las ventas de Shopify el CPA
  supera el de equilibrio.
- **AMARILLO**: todo lo demás, en especial "todavía no alcanza para decidir" (menos de 3 ventas y menos de 1 CPA
  por anuncio), medición rota con CPA real bueno, o faltan costo y precio.

## 7. Presupuesto y escalado

- **De a 20% por día como máximo** en el conjunto (ABO) o en la campaña (presupuesto de campaña). Si al día
  siguiente el CPA se fue arriba del equilibrio, se vuelve al presupuesto anterior y se espera.
- **Ganador en un conjunto con perdedores**: al apagar los perdedores, el ganador se lleva todo el presupuesto
  del conjunto de golpe. Para que suba solo 20%, el conjunto se baja a lo que gastaba el ganador × 1,2 (es lo
  que muestra la tabla del script).
- **Escalar "para el costado"**: además de subir, se puede duplicar el ganador en un conjunto nuevo con un
  público más amplio (Advantage+ o sin intereses). Sirve cuando subir el presupuesto empieza a encarecer el CPA.
- **Anuncios nuevos**: en un conjunto aparte, de 2 a 3 por vez, con ~½ CPA de equilibrio por día cada uno (llegan
  a 2 CPA en 4 días). Con menos de ⅓ de CPA por día tardan más de una semana en poder juzgarse.
- **Cuándo frenar todo**: 3 a 5 CPA de equilibrio gastados en total con 0-1 ventas. Antes de seguir, revisar
  dónde se cae la venta (`diagnostico-embudo.md`) y, si todo el embudo es flojo, el producto o el precio
  (validar-producto-ar).

## 8. Fase de aprendizaje

Meta necesita unos 50 eventos de optimización (compras) por semana en un conjunto para salir de la fase de
aprendizaje. Las cuentas chicas casi nunca salen, y está bien: lo que importa es no reiniciarla a cada rato.
Los cambios grandes la reinician: subir o bajar mucho el presupuesto, cambiar el público, la ubicación o el
evento de conversión, agregar o editar anuncios del conjunto, o pausarlo varios días. Por eso:

- Un cambio por vez, y esperar 48-72 h para ver su efecto.
- No editar un anuncio que funciona (se pierde lo aprendido y los comentarios): para probar algo, duplicarlo.
- Los primeros 1-2 días de un anuncio son ruidosos: salvo un CTR muerto, no se decide nada.
