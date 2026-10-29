// Motor de los anuncios animados sin voz (1080x1920, 18 s). Cada anuncio define window.AD y llama a AD_init().
// Escenas: 0-3.5 hook con visual · 3.5-7.5 dolor · 7.5-11.5 por qué · 11.5-15.5 solución · 15.5-18 botón.
// El texto queda entre y=230 y y=1450 para no chocar con la interfaz de Reels.
(function () {
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const span = (t, a, b) => clamp((t - a) / (b - a));
  const ease = k => 1 - Math.pow(1 - k, 3);
  const $ = id => document.getElementById(id);
  const TAPA1 = "../../ebook/tapas/tapa-consegui-trabajo.png", TAPA2 = "../../ebook/tapas/tapa-secretos-de-reclutador.png";
  const css = `
  *{box-sizing:border-box;margin:0;padding:0}
  body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;color:#fff;background:radial-gradient(circle at 50% 30%,#2B3A8C 0%,#14213D 45%,#0B1226 100%)}
  .sc{position:absolute;inset:0;opacity:0}
  .big{position:absolute;left:80px;right:80px;font:900 92px/1.05 "Inter Display",Inter;letter-spacing:-.03em;text-align:center}
  .big em{font-style:normal;color:#F5D27A}.big .r{color:#FF6B81;font-weight:900}
  .w{display:inline-block;opacity:0}
  .line{position:absolute;left:90px;right:90px;text-align:center;font:800 76px/1.15 "Inter Display",Inter;letter-spacing:-.02em;opacity:0}
  .line em{font-style:normal;color:#FF6B81}
  .card{position:absolute;left:120px;right:120px;border-radius:36px;background:#fff;color:#14213D;box-shadow:0 40px 100px rgba(0,0,0,.55)}
  .logo{position:absolute;left:0;right:0;text-align:center;font:900 120px/1 "Inter Display",Inter;letter-spacing:-.03em}
  .logo em{font-style:normal;background:#E8632E;border-radius:22px;padding:0 22px;margin-left:16px}
  .ck{position:absolute;left:140px;right:140px;display:flex;align-items:center;gap:22px;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.2);border-radius:26px;padding:24px 28px;font:800 40px/1.15 Inter;opacity:0}
  .ck i{flex:none;width:64px;height:64px;border-radius:50%;background:#16A34A;font:900 36px/64px Inter;font-style:normal;text-align:center}
  .books img{position:absolute;width:300px;border-radius:6px 12px 12px 6px;box-shadow:0 40px 90px rgba(0,0,0,.6)}
  .cta{position:absolute;left:0;right:0;text-align:center}
  .cta b{display:inline-block;background:#E8632E;color:#fff;font:900 84px/1 "Inter Display",Inter;padding:34px 56px;border-radius:30px;box-shadow:0 30px 80px rgba(232,99,46,.6)}
  .cta small{display:block;margin-top:34px;font:800 44px/1.3 Inter;color:#F5D27A}
  .arrow{position:absolute;left:50%;width:170px;margin-left:-85px}
  .arrow svg{width:170px;height:170px;filter:drop-shadow(0 0 30px rgba(232,99,46,.8))}
  /* visuales del hook */
  .cvs{position:absolute;left:150px;right:150px;top:930px;height:420px}
  .cv{position:absolute;left:50%;width:250px;height:330px;margin-left:-125px;border-radius:20px;background:#fff;padding:30px 26px;box-shadow:0 20px 50px rgba(0,0,0,.5)}
  .cv i{display:block;height:14px;border-radius:7px;background:#E2E8F0;margin-bottom:14px}.cv i:first-child{background:#14213D;width:70%;height:22px;margin-bottom:24px}
  .ctr{position:absolute;left:0;right:0;top:1380px;display:flex;justify-content:center;gap:30px;font:900 44px/1 Inter}
  .ctr span{background:rgba(255,255,255,.1);border-radius:20px;padding:20px 26px}.ctr b{color:#FF6B81}
  .mail .mh{display:flex;align-items:center;gap:20px;padding:30px 36px;border-bottom:2px solid #E2E8F0;font:800 32px/1.2 Inter}
  .mail .av{width:76px;height:76px;border-radius:50%;background:#14213D;color:#F5D27A;display:flex;align-items:center;justify-content:center;font:900 30px Inter}
  .mail .mb{padding:30px 36px 40px;font:600 36px/1.45 Inter;color:#334155;min-height:200px}
  .mail mark{background:linear-gradient(transparent 50%,rgba(225,29,72,.25) 50%);color:#9F1239;font-weight:800}
  .chat{position:absolute;left:120px;right:120px;top:930px;display:flex;flex-direction:column;gap:22px}
  .bub{align-self:flex-end;max-width:760px;background:#2563EB;border-radius:34px 34px 8px 34px;padding:26px 34px;font:600 36px/1.35 Inter;opacity:0}
  .seen{align-self:flex-end;font:700 30px Inter;color:#94A3B8;opacity:0}
  `;
  window.AD_init = function () {
    const A = window.AD, st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    // *palabra* va en dorado y !palabra! en rojo
    const words = A.hook.split(' ').map(w => `<span class="w">${w.replace(/^\*(.+)\*$/, '<em>$1</em>').replace(/^!(.+)!$/, '<b class="r">$1</b>').replace(/^!(.+)!\?$/, '<b class="r">$1</b>?')}</span>`).join(' ');
    let vis = '';
    if (A.visual === 'cvs') vis = `<div class="cvs" id="cvs">${'<div class="cv"><i></i><i></i><i></i><i></i><i></i><i></i></div>'.repeat(6)}</div><div class="ctr" id="ctr"><span>Enviados: <b id="sent">0</b></span><span>Respuestas: <b>0</b></span></div>`;
    if (A.visual === 'mail') vis = `<div class="card mail" id="vis" style="top:900px"><div class="mh"><div class="av">RH</div>Recursos Humanos</div><div class="mb" id="mb"></div></div>`;
    if (A.visual === 'visto') vis = `<div class="chat" id="vis">${A.msgs.map((m, i) => `<div class="bub" id="b${i}">${m}</div>`).join('')}<div class="seen" id="seen">Visto ✓✓</div></div>`;
    document.body.innerHTML = `
    <div class="sc" id="s1"><div class="big" style="top:300px">${words}</div>${vis}</div>
    <div class="sc" id="s2">${A.pain.map((p, i) => `<div class="line" id="p${i}" style="top:${420 + i * 300}px">${p}</div>`).join('')}</div>
    <div class="sc" id="s3"><div class="big" id="w1" style="top:420px">${A.why[0]}</div><div class="line" id="w2" style="top:820px;color:#CBD5E1">${A.why[1]}</div></div>
    <div class="sc" id="s4"><div class="logo" id="lg" style="top:280px">Método<em>30</em></div>
      ${A.sol.map((s, i) => `<div class="ck" id="c${i}" style="top:${480 + i * 150}px"><i>✓</i>${s}</div>`).join('')}
      <div class="books" id="bk" style="position:absolute;left:0;right:0;top:960px;height:460px;opacity:0"><img src="${TAPA1}" style="left:210px;top:20px;transform:rotate(-7deg);z-index:2"><img src="${TAPA2}" style="left:560px;top:50px;transform:rotate(7deg)"></div></div>
    <div class="sc" id="s5"><div class="big" style="top:330px">${A.cta}</div><div class="cta" style="top:700px"><b>Tocá el botón</b><small>Hasta 3 cuotas sin interés</small></div>
      <div class="arrow" id="ar" style="top:1130px"><svg viewBox="0 0 24 24"><path d="M12 3v15M5 12l7 7 7-7" fill="none" stroke="#E8632E" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>`;
    FX.init();
  };
  const SC = [[0, 3.5], [3.5, 7.5], [7.5, 11.5], [11.5, 15.5], [15.5, 18.2]];
  window.render = function (t) {
    const A = window.AD; FX.frame(t);
    SC.forEach(([a, b], i) => {
      const el = $('s' + (i + 1)), k = span(t, a, a + 0.25) * (i === 4 ? 1 : 1 - span(t, b - 0.2, b));
      el.style.opacity = k; el.style.transform = `scale(${1.06 - 0.06 * ease(span(t, a, a + 0.35))})`;
    });
    // 1 · hook palabra por palabra + visual
    const ws = document.querySelectorAll('#s1 .w');
    ws.forEach((w, i) => { const k = span(t, 0.05 + i * 0.09, 0.2 + i * 0.09); w.style.opacity = k; w.style.transform = `translateY(${30 - 30 * ease(k)}px) scale(${1.25 - 0.25 * ease(k)})`; });
    if (A.visual === 'cvs') {
      const n = Math.round(40 * span(t, 0.6, 3.1)); $('sent').textContent = n;
      document.querySelectorAll('.cv').forEach((c, i) => { const a = 0.6 + i * 0.4, k = span(t, a, a + 0.6);
        c.style.transform = `translate(${(i % 2 ? 1 : -1) * 520 * k}px, ${-60 + 500 * k * k}px) rotate(${(i % 2 ? 1 : -1) * 70 * k}deg)`; c.style.opacity = k < 1 ? 1 : 0; });
    }
    if (A.visual === 'mail') {
      const e = FX.enter($('vis'), t, 0.5, 0.4); $('vis').style.transform = `translateY(${40 - 40 * e}px)`;
      const T = A.mail, plain = T.replace(/<[^>]+>/g, ''); let n = Math.round(plain.length * span(t, 0.8, 2.4)), out = '', c = 0, i = 0;
      while (i < T.length && c < n) { if (T[i] === '<') { const j = T.indexOf('>', i); out += T.slice(i, j + 1); i = j + 1; continue; } out += T[i]; i++; c++; }
      if ((out.match(/<mark>/g) || []).length > (out.match(/<\/mark>/g) || []).length) out += '</mark>';
      $('mb').innerHTML = out;
    }
    if (A.visual === 'visto') {
      A.msgs.forEach((_, i) => { const k = span(t, 0.6 + i * 0.6, 0.85 + i * 0.6); $('b' + i).style.opacity = k; $('b' + i).style.transform = `translateY(${30 - 30 * k}px)`; });
      const s = span(t, 0.6 + A.msgs.length * 0.6, 0.9 + A.msgs.length * 0.6); $('seen').style.opacity = s;
    }
    // 2 · dolor, frase por frase
    A.pain.forEach((_, i) => { const a = 3.7 + i * 1.15, k = span(t, a, a + 0.3); $('p' + i).style.opacity = k; $('p' + i).style.transform = `translateY(${40 - 40 * ease(k)}px)`; });
    // 3 · por qué
    const w1 = span(t, 7.6, 7.9); $('w1').style.opacity = w1; $('w1').style.transform = `scale(${1.3 - 0.3 * ease(w1)})`;
    FX.flash(t, 7.9, 0.2);
    const w2 = span(t, 8.6, 9.0); $('w2').style.opacity = w2; $('w2').style.transform = `translateY(${30 - 30 * ease(w2)}px)`;
    // 4 · solución
    const l = span(t, 11.6, 11.85); $('lg').style.opacity = l; $('lg').style.transform = `scale(${2 - ease(l)})`;
    FX.flash(t, 11.85, 0.2);
    A.sol.forEach((_, i) => { const a = 12.3 + i * 0.5, k = span(t, a, a + 0.3); $('c' + i).style.opacity = k; $('c' + i).style.transform = `translateX(${80 - 80 * ease(k)}px)`; });
    const b = span(t, 14.0, 14.4); $('bk').style.opacity = b; $('bk').style.transform = `scale(${1.25 - 0.25 * ease(b)}) translateY(${Math.sin(t * 1.5) * 8}px)`;
    // 5 · botón
    const a = span(t, 16.0, 16.3); $('ar').style.opacity = a; $('ar').style.transform = `translateY(${a * 30 * Math.abs(Math.sin(t * 6))}px)`;
  };
})();
