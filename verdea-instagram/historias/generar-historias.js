// Genera las historias de las destacadas de VERDEA (1080x1920 PNG).
// Uso: node generar-historias.js  (necesita playwright)
// Pedidos no va acá: esa destacada la arma el dueño con fotos reales.
const path = require('path');
const { chromium } = require(process.env.PW_PATH || 'playwright');

const OUT = __dirname;
const A = (t) => `<span class="ac">${t}</span>`;
const LEAF = `<svg viewBox="0 0 24 24" width="54" height="54" fill="currentColor"><path d="M20 3C10 3 4 8.5 4 16c0 1.6.3 3 .8 4.2C6 15 9.5 11 15 9c-4.3 2.6-7.2 6.3-8.6 11.6 1.3.9 2.9 1.4 4.6 1.4 7 0 10-7 9-19z"/></svg>`;
const STAR = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>`;
const stars = (n = 5) => `<div class="stars">${STAR.repeat(n)}</div>`;

const hero = (h, sub, opt = {}) => ({ ...opt, body: `<h1 class="h1">${h}</h1>${sub ? `<p class="sub">${sub}</p>` : ''}` });
const big = (q, n, unit, sub, opt = {}) => ({ ...opt, body: `<h2 class="q">${q}</h2><div class="rule"></div><div class="bigrow"><span class="big">${n}</span>${unit ? `<span class="unit">${unit}</span>` : ''}</div>${sub ? `<p class="sub">${sub}</p>` : ''}` });
const checks = (h, items, sub, opt = {}) => ({ ...opt, body: `<h1 class="h2">${h}</h1><ul class="checks">${items.map(([ok, t, d]) => `<li class="${ok ? 'ok' : 'no'}"><i>${ok ? '✓' : '✕'}</i><div><b>${t}</b>${d ? `<span>${d}</span>` : ''}</div></li>`).join('')}</ul>${sub ? `<p class="sub">${sub}</p>` : ''}` });
const quote = (titulo, texto, nombre, opt = {}) => ({ ...opt, body: `${stars()}<h1 class="h2">“${titulo}”</h1><p class="quote">${texto}</p><p class="who">— ${nombre}</p>` });
const math = (q, rows, sub, opt = {}) => ({ ...opt, body: `<h2 class="q">${q}</h2><div class="rule"></div><div class="math">${rows.map(([op, n, u, cls]) => `<div class="mrow ${cls || ''}"><span class="op">${op}</span><span class="mn">${n}</span><span class="mu">${u}</span></div>`).join('')}</div>${sub ? `<p class="sub">${sub}</p>` : ''}` });
const steps = (h, items, sub, opt = {}) => ({ ...opt, body: `<h1 class="h2">${h}</h1><ol class="steps">${items.map((t, i) => `<li><i>${i + 1}</i><div>${t}</div></li>`).join('')}</ol>${sub ? `<p class="sub">${sub}</p>` : ''}` });
const L = { lime: true };

const SETS = {
  'resenas': ['RESEÑAS', [
    big('¿Qué dicen los que ya lo usan?', '4,9', `de 5 ${stars()}`, `${A('54 opiniones')} en la tienda y más de 1.083 clientes cuidando sus plantas con VERDEA.`),
    quote('Chau estrés por trasplante', 'Cada vez que pasaba una planta a una maceta más grande terminaba sufriendo. Con este enraizante prenden enseguida y no sienten el cambio. Súper recomendado.', 'Carlos Y.'),
    quote('Súper fácil de usar y efectivo', 'Recién estoy arrancando con mis primeras plantas y tenía miedo de mandarme una macana. Fue facilísimo y los resultados se re notan.', 'Sofía L.'),
    quote('Aproveché la promo y valió la pena', 'Súper contento con la compra. Aproveché el descuento llevando el pack x2 y la verdad que un golazo. Las plantas respondieron re bien.', 'Nacho R.', L),
    quote('Muy buena compra', 'Aproveché el pack de 3 por el envío gratis y el 35%. Tenía plantas medio trabadas y se nota un montón la diferencia. La guía de regalo también suma.', 'Mariana G.'),
    hero(`Tu planta puede ser ${A('la próxima.')}`, 'Mandanos una foto de tus raíces por mensaje y la compartimos acá.', L),
  ]],
  'modo-de-uso': ['MODO DE USO', [
    hero(`Así se usa ${A('VERDEA.')}`, 'Es concentrado: con poquito alcanza. Te lo contamos en cinco historias.'),
    big('¿Cuánto pongo?', '3-4', 'ml por litro de agua', 'Medilo con la tapita y mezclalo en la regadera o en el frasco del esqueje. Nunca puro.'),
    checks('¿Dónde lo uso?', [[1, 'Esquejes', 'para que prendan más rápido'], [1, 'Trasplantes', 'para evitar el golpe del cambio'], [1, 'Riego', 'raíces más fuertes en huerta y macetas']]),
    big('¿Cada cuánto?', '7', 'días', 'Una vez por semana, durante 4 semanas. Después, cuando la planta lo necesite.'),
    math('¿Cuánto rinde un frasco?', [['', '250', 'ml'], ['÷', '3', 'ml por litro'], ['=', '80', 'litros', 'res']], 'Unas 15 regaderas de 5 litros. Sale menos de $1.000 por litro preparado.'),
    hero(`Raíces fuertes, ${A('plantas más sanas.')}`, 'Fórmula orgánica · Alta concentración · Sin químicos agresivos.', L),
  ]],
  'pagos': ['PAGOS', [
    big('¿Puedo pagar en cuotas?', '3', 'cuotas sin interés', 'Con tarjeta de crédito, en cualquier pack.'),
    checks('¿Cómo puedo pagar?', [[1, 'Tarjeta de crédito', '3 cuotas sin interés'], [1, 'Tarjeta de débito', 'en un pago'], [1, 'Mercado Pago', 'rápido y seguro']]),
    math('Elegí tu pack', [['x1', '$58.000', ''], ['x2', '$81.200', '30% OFF + guía'], ['x3', '$113.100', '35% OFF + envío gratis', 'res']], 'Todos en 3 cuotas sin interés. Guía de regalo con x2 y x3.'),
    hero(`Pago ${A('100% seguro.')}`, 'Todo se procesa en el checkout seguro de Shopify. Nunca te pedimos datos por mensaje.', L),
  ]],
  'envios': ['ENVÍOS', [
    hero(`Enviamos a ${A('todo el país.')}`, 'Por Correo Argentino, de nuestra casa a la tuya.'),
    math('¿Cuánto tarda?', [['', '24 hs', 'hábiles para despachar'], ['+', '2-3', 'días hábiles de viaje', 'res']], 'Depende de tu zona. Apenas sale, te avisamos.'),
    hero(`¿Cómo lo ${A('sigo?')}`, 'Te mandamos el código de seguimiento de Correo Argentino por mail o WhatsApp.'),
    big('¿El envío es gratis?', 'x3', 'llevando 3 frascos', 'Con el pack x3 el envío no te cuesta nada, más 35% OFF y la guía de regalo.', L),
  ]],
  'pedidos': ['PEDIDOS', [
    hero(`Pedir es ${A('fácil.')}`, 'Tres pasos y tus plantas ya tienen lo que necesitan.'),
    steps('Así funciona', ['Elegí tu pack en la tienda', 'Pagá en 3 cuotas sin interés', 'Recibí el seguimiento y esperalo en casa']),
    checks('¿Qué llega en la caja?', [[1, 'Tu frasco VERDEA', '250 ml concentrado, rinde hasta 80 L'], [1, 'Guía de cuidado', 'de regalo con los packs x2 y x3']]),
    hero(`¿Ya compraste? ${A('Escribinos.')}`, 'Mandanos tu número de pedido por mensaje y te decimos dónde está. Lo lee una persona, no un bot.', L),
  ]],
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
body{font-family:'Poppins',sans-serif;background:#0B130D;color:#F3F1E7;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(900px 700px at 95% 8%,rgba(107,163,66,.20),transparent 70%)}
body.lime{background:#9CD45B;color:#0B130D}
body.lime:before{background:radial-gradient(900px 700px at 95% 8%,rgba(255,255,255,.25),transparent 70%)}
.wrap{position:absolute;inset:0;padding:0 130px}
.top{position:absolute;top:290px;left:130px;right:130px;display:flex;justify-content:space-between;font-size:30px;letter-spacing:10px;font-weight:600}
.top .lab{color:#9CD45B}.lime .top .lab{color:#0B130D}
.top .cnt{color:#5E6A60;letter-spacing:4px;font-weight:500}.lime .top .cnt{color:#4B6B2B}
.mid{position:absolute;left:130px;right:120px;top:50%;transform:translateY(-48%)}
.logo{position:absolute;left:130px;bottom:330px;display:flex;align-items:center;gap:12px;color:#9CD45B;font-weight:800;font-size:66px;letter-spacing:2px}
.lime .logo{color:#0B130D}
.ac{color:#9CD45B}.lime .ac{color:#24461F}
.h1{font-weight:800;font-size:118px;line-height:1.02;letter-spacing:-3px}
.h2{font-weight:800;font-size:86px;line-height:1.06;letter-spacing:-2px}
.q{font-weight:800;font-size:72px;line-height:1.1;letter-spacing:-1.5px;color:#9CD45B}.lime .q{color:#0B130D}
.rule{width:120px;height:5px;background:#3A463C;margin:44px 0 30px}.lime .rule{background:#6E9A3F}
.sub{font-size:44px;line-height:1.45;color:#9AA39B;margin-top:44px;max-width:820px}.lime .sub{color:#2E4A22}
.sub .ac{font-weight:600}
.bigrow{display:flex;align-items:baseline;gap:34px;flex-wrap:wrap}
.big{font-weight:800;font-size:250px;line-height:.95;letter-spacing:-8px;color:#9CD45B}.lime .big{color:#0B130D}
.unit{font-size:54px;color:#C9CEC6;font-weight:500;max-width:520px;line-height:1.2}.lime .unit{color:#24461F}
.unit .stars{display:inline-flex;margin-left:10px;vertical-align:middle}
.stars{display:flex;gap:8px;color:#9CD45B;margin-bottom:34px}.lime .stars{color:#0B130D}
.stars svg{width:54px;height:54px}.unit .stars svg{width:42px;height:42px}.unit .stars{margin-bottom:0}
.quote{font-size:48px;line-height:1.5;color:#C9CEC6;margin-top:40px}.lime .quote{color:#1E3A1A}
.who{font-size:36px;color:#7D877F;margin-top:40px;font-weight:600}.lime .who{color:#3C5F2A}
.checks{list-style:none;margin-top:56px;display:flex;flex-direction:column;gap:44px}
.checks li{display:flex;gap:34px;align-items:flex-start}
.checks i{font-style:normal;font-weight:800;font-size:58px;line-height:1.1;color:#9CD45B;width:50px}.lime .checks i{color:#0B130D}
.checks li.no i,.checks li.no b{color:#5E6A60}
.checks b{display:block;font-weight:800;font-size:62px;line-height:1.15}
.checks span{display:block;font-size:42px;color:#9AA39B;margin-top:6px}.lime .checks span{color:#2E4A22}
.steps{list-style:none;margin-top:56px;display:flex;flex-direction:column;gap:46px}
.steps li{display:flex;gap:36px;align-items:center;font-weight:700;font-size:56px;line-height:1.2}
.steps i{font-style:normal;flex:0 0 96px;height:96px;border-radius:50%;background:#9CD45B;color:#0B130D;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:52px}
.math{display:flex;flex-direction:column}
.mrow{display:grid;grid-template-columns:110px auto 1fr;align-items:baseline;gap:30px;padding:18px 0}
.mrow.res{border-top:4px solid #3A463C;margin-top:14px;padding-top:34px}.lime .mrow.res{border-color:#6E9A3F}
.op{font-weight:800;font-size:76px;color:#9CD45B}
.mn{font-weight:800;font-size:120px;letter-spacing:-3px;line-height:1}
.mrow.res .mn{color:#9CD45B}
.mu{font-size:44px;color:#9AA39B;line-height:1.2}
`;

const page = (label, i, n, s) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=block" rel="stylesheet">
<style>${CSS}</style></head><body class="${s.lime ? 'lime' : ''}"><div class="wrap">
<div class="top"><span class="lab">${label}</span><span class="cnt">${String(i).padStart(2, '0')} / ${String(n).padStart(2, '0')}</span></div>
<div class="mid">${s.body}</div>
<div class="logo">${LEAF}VERDEA</div></div></body></html>`;

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [slug, [label, slides]] of Object.entries(SETS)) {
    for (let i = 0; i < slides.length; i++) {
      await p.setContent(page(label, i + 1, slides.length, slides[i]), { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(OUT, slug, `${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await b.close();
})();
