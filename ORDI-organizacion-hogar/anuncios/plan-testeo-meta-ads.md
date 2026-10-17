# ORDI · Plan de testeo en Meta Ads (14 días)

**Objetivo:** encontrar 1–2 anuncios que vendan con un costo por venta (CPA) **menor a $13.500**: lo máximo que podés pagar por venta del set x1 sin perder plata, con costo de $12.000 por set (ver `validacion/`).

## Antes de empezar (checklist)
- [ ] Píxel de Meta + API de conversiones conectados en Shopify (app "Facebook & Instagram").
- [ ] Evento de compra ("Purchase") probado con una compra real o de prueba.
- [ ] Landing con `slugURL` cargado, fotos reales y los packs en Kaching.
- [ ] 4 videos listos (de `creativos/guiones-videos.txt`): **Caro 1, Caro 2, Caro 3 y Silvia 1**.
- [ ] Textos de `anuncios/copys-meta-ads.txt` (1, 4, 6 y 8).

## Estructura
- **1 campaña** · objetivo **Ventas** · presupuesto **por conjunto de anuncios (ABO)** para controlar el gasto de cada uno.
- **Conjunto A · "Caro"**: mujeres 25–40, Argentina, intereses deco / organización del hogar / IKEA / Pinterest. $14.000 por día.
- **Conjunto B · "Silvia"**: mujeres 32–50, Argentina, intereses maternidad / hogar / limpieza. $14.000 por día.
- Ubicaciones automáticas (Advantage+). Excluí a quienes ya compraron.
- 2 anuncios por conjunto (cada uno con su texto).

## Calendario
| Días | Qué hacer |
|---|---|
| 1–4 | Dejar correr sin tocar. **Gasto total ≈ $112.000.** |
| 5 | **Cortar** cada anuncio que gastó **$20.000–$27.000 sin ventas**. Revisar CTR (porcentaje de clics; < 0,8% = el gancho no engancha) y CPC. |
| 5–7 | Los que venden: dejarlos. Agregar 2 anuncios nuevos copiando el ángulo ganador con otro gancho (los primeros 3 segundos). |
| 8–10 | **Escalar** el ganador: +20% de presupuesto por día si el CPA sigue < $13.500. |
| 11–14 | Retargeting: conjunto nuevo con quienes visitaron la página (7 días) y no compraron, con el texto 13. $5.000 por día. |

## Cómo leer los números
- **CPA < $13.500** → ganador, escalar despacio.
- **CPA $13.500–$20.000** → mirá el ticket promedio: si la mayoría compra 2 sets (margen $20.500), igual cierra.
- **CPA > $20.000** → cortar o cambiar el gancho.
- **Muchos clics y pocas ventas** → el problema está en la página o el precio, no en el anuncio.

## Cuándo frenar todo
Si después de gastar ~$150.000 no hay ninguna venta, frená y revisá oferta, precio y página antes de seguir.
