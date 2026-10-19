// Genera las historias de las destacadas de VERDEA (1080x1920 PNG, 9:16).
// Identidad: papel kraft de la etiqueta, verde oscuro, letra Fraunces + manuscrita Caveat,
// fotos reales del producto y raíces dibujadas al pie.
// Uso: node generar-historias.js  (necesita playwright)
// Pedidos no va acá: esa destacada la arma el dueño con fotos reales.
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PW_PATH || 'playwright');

const OUT = __dirname;
const img = (f) => {
  const p = path.join(__dirname, '..', 'assets', f);
  return `data:image/${f.endsWith('.png') ? 'png' : 'jpeg'};base64,${fs.readFileSync(p).toString('base64')}`;
};
const FRASCO = img('frasco-verdea.png');
const ESQUEJE = img('foto-esqueje.jpg');
const REGADERA = img('foto-regadera.jpg');

// Íconos de línea (24x24)
const I = {
  sprout: '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
  scissors: '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
  pot: '<path d="M5 11h14l-2 9H7z"/><path d="M12 11V5"/><path d="M12 8c-2-2.2-4.2-2.2-5.2-1.2 1 2.2 3.2 2.4 5.2 1.2z"/><path d="M12 6.5c2-2.2 4.2-2.2 5.2-1.2-1 2.2-3.2 2.4-5.2 1.2z"/>',
  can: '<path d="M4 10h10l-1.2 10H5.2z"/><path d="M14 13.5l5.5-4.5"/><path d="m18.2 7.2 2.6 2.6"/><path d="M6.5 10a3.5 3.5 0 0 1 5 0"/>',
  card: '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
  wallet: '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
  lock: '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  box: '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.3 7 12 12l8.7-5"/><path d="M12 22V12"/><path d="m7.5 4.3 9 5.1"/>',
  truck: '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
  home: '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
  mail: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
  chat: '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
  cart: '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
  drop: '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
};
const ico = (n, cls = '') => `<svg class="ico ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${I[n]}</svg>`;
const STAR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>';
const stars = `<div class="stars">${STAR.repeat(5)}</div>`;

// Ramita decorativa
const SPRIG = (cls) => `<svg class="sprig ${cls}" viewBox="0 0 200 320" fill="currentColor">
<path d="M100 320 C 96 240 104 160 100 20" stroke="currentColor" stroke-width="5" fill="none"/>
<path d="M100 250 C 60 240 30 210 22 170 C 62 175 92 205 100 250Z"/>
<path d="M101 205 C 140 196 170 166 178 126 C 138 131 108 161 101 205Z"/>
<path d="M100 160 C 64 150 40 122 34 88 C 70 94 94 122 100 160Z"/>
<path d="M101 112 C 134 104 158 78 164 46 C 130 52 106 78 101 112Z"/>
<path d="M100 66 C 84 52 80 30 86 6 C 104 20 108 44 100 66Z"/></svg>`;

// Raíces al pie
const ROOTS = `<svg class="roots" viewBox="0 0 820 170" fill="none" stroke="currentColor" stroke-linecap="round">
<path d="M0 8 H820" stroke-width="3" stroke-dasharray="2 14"/>
<g stroke-width="4"><path d="M410 8 C 408 50 418 90 404 160"/><path d="M410 40 C 380 60 350 70 318 112"/><path d="M412 52 C 450 70 480 90 500 140"/>
<path d="M346 92 C 330 104 316 108 296 106"/><path d="M470 84 C 494 88 516 84 540 70"/><path d="M408 100 C 390 118 380 132 376 156"/><path d="M408 96 C 430 112 440 128 446 150"/></g>
<g stroke-width="2.5" opacity=".7"><path d="M318 112 C 310 124 300 130 286 132"/><path d="M500 140 C 506 150 516 156 530 158"/><path d="M296 106 C 284 112 276 120 270 132"/><path d="M540 70 C 552 80 560 92 562 108"/></g></svg>`;

const dots = (i, n) => `<div class="dots">${Array.from({ length: n }, (_, k) => `<span class="${k < i ? 'on' : ''}${k === i - 1 ? ' cur' : ''}"></span>`).join('')}</div>`;

// ---- tipos de historia ----
const S = (body, opt = {}) => ({ body, ...opt });
const G = { green: true };

const reviewCard = (titulo, texto, nombre, rot) => S(`
<p class="script center">lo que nos cuentan</p>
<div class="note" style="transform:rotate(${rot}deg)"><div class="tape"></div>
<div class="qm">“</div>${stars}<h2 class="ntitle">${titulo}</h2><p class="ntext">${texto}</p>
<div class="who"><span class="av">${nombre[0]}</span><span>${nombre}</span></div></div>`);

const SETS = {
  resenas: ['Reseñas', 'sprout', [
    S(`<div class="center">
<p class="script big-script">nuestros clientes dicen</p>
<div class="score">4,9</div>${stars.replace('stars', 'stars lg')}
<p class="lead">sobre 5, con <b>54 opiniones</b> en la tienda</p>
<div class="pill-row"><span class="chip">+1.083 clientes</span><span class="chip">cuidando sus plantas</span></div></div>`, G),
    reviewCard('Chau estrés por trasplante', 'Cada vez que pasaba una planta a una maceta más grande terminaba sufriendo. Con este enraizante prenden enseguida y no sienten el cambio. Súper recomendado.', 'Carlos Y.', -1.5),
    reviewCard('Súper fácil de usar y efectivo', 'Recién estoy arrancando con mis primeras plantas y tenía miedo de mandarme una macana. Fue facilísimo y los resultados se re notan.', 'Sofía L.', 1.2),
    reviewCard('Aproveché la promo y valió la pena', 'Súper contento con la compra. Aproveché el descuento llevando el pack x2 y la verdad que un golazo. Las plantas respondieron re bien.', 'Nacho R.', -1),
    reviewCard('Muy buena compra', 'Aproveché el pack de 3 por el envío gratis y el 35%. Tenía plantas medio trabadas y se nota un montón la diferencia. La guía de regalo también suma.', 'Mariana G.', 1.4),
    S(`<div class="arch"><img src="${ESQUEJE}"></div>
<h1 class="title">Tu planta puede ser <em>la próxima</em></h1>
<p class="lead">Mandanos una foto de tus raíces por mensaje y la compartimos acá.</p>`, G),
  ]],
  'modo-de-uso': ['Modo de uso', 'drop', [
    S(`<div class="arch"><img src="${REGADERA}"></div>
<h1 class="title">Así se usa <em>VERDEA</em></h1>
<p class="lead">Es concentrado: con poquito alcanza. Te lo contamos en cinco pasos.</p>`),
    S(`<div class="split"><div>
<p class="script">¿cuánto pongo?</p><div class="dose">3-4<small>ml</small></div>
<p class="lead">por cada <b>litro de agua</b>, en la regadera o en el frasco del esqueje.</p>
<div class="warn">${ico('drop')}Nunca puro: siempre diluido</div></div>
<img class="bottle" src="${FRASCO}"></div>`),
    S(`<p class="script">¿dónde lo uso?</p><h1 class="title sm">En todo lo que <em>tiene que echar raíz</em></h1>
<div class="rows">
<div class="row">${ico('scissors', 'circ')}<div><b>Esquejes</b><span>para que prendan más rápido</span></div></div>
<div class="row">${ico('pot', 'circ')}<div><b>Trasplantes</b><span>para evitar el golpe del cambio</span></div></div>
<div class="row">${ico('can', 'circ')}<div><b>Riego</b><span>raíces más fuertes en huerta y macetas</span></div></div></div>`),
    S(`<p class="script">¿cada cuánto?</p><h1 class="title">Una vez <em>por semana</em></h1>
<div class="weeks">${[1, 2, 3, 4].map((w) => `<div class="wk">${ico('sprout')}<span>semana ${w}</span></div>`).join('')}</div>
<p class="lead">Durante 4 semanas. Después, cada vez que la planta lo necesite.</p>`, G),
    S(`<p class="script">¿cuánto rinde?</p><div class="yield"><img class="bottle sm" src="${FRASCO}"><span class="eq">=</span><div><div class="dose">80<small>litros</small></div></div></div>
<div class="cans">${Array.from({ length: 15 }, () => ico('can')).join('')}</div>
<p class="lead center">Unas <b>15 regaderas</b> de 5 litros. Sale menos de <b>$1.000 por litro</b> preparado.</p>`),
    S(`<div class="arch"><img src="${ESQUEJE}"></div>
<h1 class="title">Raíces fuertes, <em>plantas más sanas</em></h1>
<p class="lead">Fórmula orgánica · Alta concentración · Sin químicos agresivos</p>`, G),
  ]],
  pagos: ['Pagos', 'card', [
    S(`<div class="center"><p class="script big-script">pagalo tranqui</p>
<div class="circle-num">3</div><h1 class="title">cuotas <em>sin interés</em></h1>
<p class="lead">Con tarjeta de crédito, en cualquier pack.</p></div>`),
    S(`<p class="script">¿cómo puedo pagar?</p><h1 class="title sm">Elegí <em>como te quede mejor</em></h1>
<div class="rows">
<div class="row">${ico('card', 'circ')}<div><b>Tarjeta de crédito</b><span>3 cuotas sin interés</span></div></div>
<div class="row">${ico('card', 'circ')}<div><b>Tarjeta de débito</b><span>en un pago</span></div></div>
<div class="row">${ico('wallet', 'circ')}<div><b>Mercado Pago</b><span>rápido y seguro</span></div></div></div>`),
    S(`<p class="script center">elegí tu pack</p>
<div class="packs">
<div class="pack"><div class="bots">${`<img src="${FRASCO}">`}</div><b>1 frasco</b><span class="price">$58.000</span></div>
<div class="pack hot"><span class="badge">30% OFF + guía</span><div class="bots">${`<img src="${FRASCO}">`.repeat(2)}</div><b>2 frascos</b><span class="price">$81.200</span></div>
<div class="pack"><span class="badge">35% OFF + envío gratis</span><div class="bots">${`<img src="${FRASCO}">`.repeat(3)}</div><b>3 frascos</b><span class="price">$113.100</span></div></div>
<p class="lead center">Todos en 3 cuotas sin interés · guía de regalo con x2 y x3</p>`),
    S(`<div class="center"><div class="big-ico">${ico('lock')}</div>
<h1 class="title">Pago <em>100% seguro</em></h1>
<p class="lead">Todo se procesa en el checkout seguro de Shopify. Nunca te pedimos datos por mensaje.</p></div>`, G),
  ]],
  envios: ['Envíos', 'truck', [
    S(`<div class="center"><div class="big-ico">${ico('box')}</div>
<h1 class="title">Llegamos a <em>todo el país</em></h1>
<p class="lead">Por Correo Argentino, de nuestra casa a la tuya.</p></div>`),
    S(`<p class="script">¿cuánto tarda?</p><h1 class="title sm">Del carrito <em>a tu puerta</em></h1>
<div class="tl">
<div class="st">${ico('cart', 'circ')}<div><b>Comprás</b><span>en la tienda, cuando quieras</span></div></div>
<div class="st">${ico('box', 'circ')}<div><b>Despachamos</b><span>dentro de las 24 hs hábiles</span></div></div>
<div class="st">${ico('truck', 'circ')}<div><b>Viaja</b><span>2 a 3 días hábiles, según tu zona</span></div></div>
<div class="st">${ico('home', 'circ')}<div><b>¡Llegó!</b><span>a regar se ha dicho</span></div></div></div>`),
    S(`<p class="script">¿cómo lo sigo?</p><h1 class="title sm">Te avisamos <em>apenas sale</em></h1>
<div class="rows">
<div class="row">${ico('mail', 'circ')}<div><b>Por mail</b><span>con el código de Correo Argentino</span></div></div>
<div class="row">${ico('chat', 'circ')}<div><b>Por WhatsApp</b><span>si preferís tenerlo a mano</span></div></div></div>`),
    S(`<div class="center"><p class="script big-script">llevando 3</p>
<div class="bots3">${`<img src="${FRASCO}">`.repeat(3)}</div>
<h1 class="title">El envío <em>es gratis</em></h1>
<p class="lead">Y además 35% OFF y la guía de regalo.</p></div>`, G),
  ]],
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
:root{--kraft:#EFE6D3;--paper:#FBF7EE;--green:#1F4A2C;--sprout:#6BA342;--orange:#E07A2E;--ink:#24301F;--muted:#6B6A58}
html,body{width:1080px;height:1920px}
body{font-family:'DM Sans',sans-serif;background:var(--kraft);color:var(--ink);position:relative;overflow:hidden}
body:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.35;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .45  0 0 0 0 .38  0 0 0 0 .25  0 0 0 .55 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
body.green{background:var(--green);color:var(--kraft)}
body.green:after{opacity:.18}
.sprig{position:absolute;color:var(--sprout);opacity:.22;width:230px}
.sprig.tr{top:120px;right:-40px;transform:rotate(18deg)}
.sprig.bl{bottom:380px;left:-70px;transform:rotate(-24deg) scaleX(-1);width:200px}
.green .sprig{color:#8CC063;opacity:.16}
.head{position:absolute;top:250px;left:90px;right:90px;display:flex;justify-content:space-between;align-items:center}
.tag{display:flex;align-items:center;gap:14px;background:var(--green);color:var(--kraft);padding:16px 32px 16px 24px;border-radius:999px;font-weight:700;font-size:34px}
.tag .ico{width:38px;height:38px}
.green .tag{background:var(--kraft);color:var(--green)}
.dots{display:flex;gap:12px}.dots span{width:18px;height:18px;border-radius:50%;border:3px solid var(--sprout)}
.dots span.on{background:var(--sprout)}.dots span.cur{width:42px;border-radius:9px}
.green .dots span{border-color:#8CC063}.green .dots span.on{background:#8CC063}
.mid{position:absolute;left:90px;right:90px;top:400px;bottom:430px;display:flex;flex-direction:column;justify-content:center}
.foot{position:absolute;left:0;right:0;bottom:250px;display:flex;flex-direction:column;align-items:center;color:var(--green)}
.green .foot{color:var(--kraft)}
.roots{width:620px;opacity:.55;margin-bottom:-10px}
.word{font-family:'Fraunces',serif;font-weight:800;font-size:58px;letter-spacing:6px;margin-top:-40px;background:var(--kraft);padding:0 26px}
.green .word{background:var(--green)}
.word small{display:block;text-align:center;font-family:'DM Sans';font-size:20px;letter-spacing:7px;font-weight:700;opacity:.7;margin-top:2px}
.center{text-align:center;align-items:center}
.script{font-family:'Caveat',cursive;font-size:64px;color:var(--orange);font-weight:700;line-height:1;margin-bottom:14px}
.big-script{font-size:76px}
.green .script{color:#F2A35E}
.title{font-family:'Fraunces',serif;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-1.5px;color:var(--green)}
.title.sm{font-size:84px}
.title em{font-style:italic;font-weight:600;color:var(--sprout)}
.green .title{color:var(--kraft)}.green .title em{color:#9FD06F}
.lead{font-size:42px;line-height:1.45;color:var(--muted);margin-top:30px}
.lead b{color:var(--green)}.green .lead{color:#CFD8C4}.green .lead b{color:#fff}
.arch{width:100%;height:640px;border-radius:450px 450px 40px 40px;overflow:hidden;margin-bottom:56px;box-shadow:0 30px 60px -30px rgba(40,30,10,.5);border:10px solid var(--paper)}
.green .arch{border-color:#2B5C38}
.arch img{width:100%;height:100%;object-fit:cover}
.score{font-family:'Fraunces',serif;font-weight:800;font-size:300px;line-height:1;color:var(--kraft);margin-top:10px}
.stars{display:flex;gap:10px;color:var(--orange);justify-content:center}.stars svg{width:46px;height:46px}
.stars.lg svg{width:72px;height:72px}
.green .stars{color:#F2A35E}
.pill-row{display:flex;gap:16px;justify-content:center;margin-top:44px;flex-wrap:wrap}
.chip{background:rgba(239,230,211,.12);border:2px solid rgba(239,230,211,.35);padding:14px 30px;border-radius:999px;font-size:36px;font-weight:600}
.note{position:relative;background:var(--paper);border-radius:28px;padding:80px 64px 56px;box-shadow:0 40px 70px -40px rgba(60,40,10,.55);margin-top:30px}
.note .stars{justify-content:flex-start}
.tape{position:absolute;top:-28px;left:50%;width:220px;height:58px;transform:translateX(-50%) rotate(-3deg);background:rgba(200,180,140,.55)}
.qm{position:absolute;top:10px;right:46px;font-family:'Fraunces';font-size:220px;line-height:1;color:var(--sprout);opacity:.25}
.ntitle{font-family:'Fraunces',serif;font-weight:800;font-size:64px;line-height:1.08;color:var(--green);margin:26px 0 22px}
.ntext{font-size:40px;line-height:1.5;color:#4C4B3D}
.who{display:flex;align-items:center;gap:20px;margin-top:40px;font-weight:700;font-size:36px;color:var(--green)}
.av{width:70px;height:70px;border-radius:50%;background:var(--sprout);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Fraunces';font-size:36px}
.split{display:flex;align-items:center;gap:30px}.split>div{flex:1}
.bottle{height:760px;filter:drop-shadow(0 30px 30px rgba(50,35,10,.35))}
.bottle.sm{height:430px}
.dose{font-family:'Fraunces',serif;font-weight:800;font-size:230px;line-height:.95;color:var(--green);letter-spacing:-6px}
.dose small{font-size:80px;letter-spacing:0;margin-left:14px;color:var(--sprout);font-style:italic;font-weight:600}
.warn{display:inline-flex;align-items:center;gap:14px;margin-top:40px;background:var(--green);color:var(--kraft);padding:18px 30px;border-radius:999px;font-weight:700;font-size:34px}
.warn .ico{width:38px;height:38px}
.rows,.tl{display:flex;flex-direction:column;gap:30px;margin-top:56px}
.row,.st{display:flex;align-items:center;gap:34px;background:var(--paper);border-radius:28px;padding:30px 36px;box-shadow:0 20px 40px -30px rgba(60,40,10,.5)}
.row b,.st b{display:block;font-family:'Fraunces';font-weight:800;font-size:54px;color:var(--green);line-height:1.1}
.row span,.st span{display:block;font-size:36px;color:var(--muted);margin-top:6px}
.ico.circ{flex:0 0 120px;height:120px;padding:28px;border-radius:50%;background:#E3EBD2;color:var(--green)}
.tl{gap:0;position:relative}.tl:before{content:"";position:absolute;left:96px;top:60px;bottom:60px;border-left:5px dashed var(--sprout);opacity:.6}
.st{background:none;box-shadow:none;padding:22px 36px}
.st .ico.circ{position:relative;background:var(--green);color:var(--kraft)}
.weeks{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-top:56px}
.wk{background:rgba(239,230,211,.1);border:2px solid rgba(239,230,211,.3);border-radius:28px;padding:34px 10px;display:flex;flex-direction:column;align-items:center;gap:16px;font-size:30px;font-weight:600}
.wk .ico{width:84px;height:84px;color:#9FD06F}
.yield{display:flex;align-items:center;justify-content:center;gap:50px;margin-top:10px}
.eq{font-family:'Fraunces';font-size:150px;color:var(--sprout);font-weight:800}
.cans{display:grid;grid-template-columns:repeat(5,1fr);gap:22px 30px;margin:46px auto 0;width:640px;color:var(--green)}
.cans .ico{width:100px;height:100px}
.circle-num{width:330px;height:330px;border-radius:50%;background:var(--green);color:var(--kraft);font-family:'Fraunces';font-weight:800;font-size:250px;line-height:330px;margin:20px auto 30px;box-shadow:0 30px 60px -30px rgba(31,74,44,.8)}
.big-ico{width:250px;height:250px;border-radius:50%;background:#E3EBD2;color:var(--green);padding:62px;margin:0 auto 50px}
.green .big-ico{background:#2B5C38;color:#9FD06F}
.big-ico .ico{width:100%;height:100%}
.packs{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px;align-items:end}
.pack{position:relative;background:var(--paper);border-radius:28px;padding:70px 14px 34px;text-align:center;box-shadow:0 20px 40px -30px rgba(60,40,10,.5);display:flex;flex-direction:column;align-items:center}
.pack.hot{outline:5px solid var(--sprout)}
.bots{height:300px;display:flex;align-items:flex-end;justify-content:center}
.bots img{height:270px;margin:0 -16px}
.pack:first-child .bots img{height:290px}
.pack b{font-family:'Fraunces';font-size:42px;color:var(--green);margin-top:20px}
.price{font-family:'Fraunces';font-weight:800;font-size:52px;color:var(--ink);margin-top:6px}
.badge{position:absolute;top:-30px;left:50%;transform:translateX(-50%);width:88%;text-align:center;line-height:1.15;background:var(--orange);color:#fff;font-weight:700;font-size:25px;padding:10px 18px;border-radius:999px}
.bots3{display:flex;justify-content:center;margin:30px 0 40px}.bots3 img{height:420px;margin:0 -28px;filter:drop-shadow(0 25px 25px rgba(0,0,0,.35))}
.bots3 img:nth-child(2){height:470px;position:relative;z-index:1}
`;

const page = (label, icon, i, n, s) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,800;1,9..144,600&family=DM+Sans:wght@400;500;600;700&family=Caveat:wght@700&display=block" rel="stylesheet">
<style>${CSS}</style></head><body class="${s.green ? 'green' : ''}">
${SPRIG('tr')}${SPRIG('bl')}
<div class="head"><div class="tag">${ico(icon)}${label}</div>${dots(i, n)}</div>
<div class="mid">${s.body}</div>
<div class="foot">${ROOTS}<div class="word">VERDEA<small>HUERTA DOMÉSTICA</small></div></div>
</body></html>`;

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || undefined });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [slug, [label, icon, slides]] of Object.entries(SETS)) {
    fs.mkdirSync(path.join(OUT, slug), { recursive: true });
    for (let i = 0; i < slides.length; i++) {
      await p.setContent(page(label, icon, i + 1, slides.length, slides[i]), { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(OUT, slug, `${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await b.close();
})();
