// Efectos compartidos de los fondos: partículas desenfocadas, viñeta, cámara 3D y entradas cinematográficas.
// Cada fondo llama a FX.init() una vez y a FX.frame(t) en cada cuadro, antes de su propia animación.
(function () {
  const W = 1080, H = 1920;
  const rnd = (seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647)(42);
  const css = `
    .fx-bokeh{position:absolute;inset:0;overflow:hidden;z-index:0;pointer-events:none}
    .fx-bokeh i{position:absolute;border-radius:50%;filter:blur(18px)}
    .fx-vignette{position:absolute;inset:0;z-index:50;pointer-events:none;
      background:radial-gradient(ellipse at 50% 32%,rgba(0,0,0,0) 45%,rgba(0,0,0,.55) 100%)}
    .fx-cam{position:absolute;inset:0;z-index:5;perspective:1800px;perspective-origin:50% 30%}
    .fx-stage{position:absolute;inset:0;transform-style:preserve-3d}
    .fx-flash{position:absolute;inset:0;z-index:60;background:#fff;opacity:0;pointer-events:none}`;
  const P = [];
  window.FX = {
    init() {
      const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
      const b = document.createElement("div"); b.className = "fx-bokeh";
      for (let i = 0; i < 26; i++) {
        const d = document.createElement("i");
        const size = 40 + rnd() * 160, warm = rnd() < 0.35;
        d.style.width = d.style.height = size + "px";
        d.style.background = warm ? "rgba(232,99,46,.35)" : (rnd() < .5 ? "rgba(245,210,122,.18)" : "rgba(120,140,255,.22)");
        P.push({ el: d, x: rnd() * W, y: rnd() * H * 0.7, vx: (rnd() - .5) * 18, vy: -6 - rnd() * 14, ph: rnd() * 6.28 });
        b.appendChild(d);
      }
      document.body.prepend(b);
      // todo lo que no es efecto pasa a la "cámara"
      const cam = document.createElement("div"); cam.className = "fx-cam";
      const stage = document.createElement("div"); stage.className = "fx-stage"; stage.id = "fx-stage";
      [...document.body.children].forEach(c => { if (c !== b && c.tagName !== "SCRIPT") stage.appendChild(c); });
      cam.appendChild(stage); document.body.appendChild(cam);
      const v = document.createElement("div"); v.className = "fx-vignette"; document.body.appendChild(v);
      const f = document.createElement("div"); f.className = "fx-flash"; f.id = "fx-flash"; document.body.appendChild(f);
    },
    frame(t) {
      P.forEach(p => {
        p.el.style.transform = `translate(${p.x + p.vx * t}px, ${p.y + p.vy * t}px)`;
        p.el.style.opacity = 0.55 + 0.45 * Math.sin(t * 0.9 + p.ph);
      });
      // cámara: leve inclinación 3D que va cambiando, acercamiento lento
      const rx = 7 - 4 * Math.sin(t * 0.35), ry = -6 * Math.sin(t * 0.28), s = 1 + 0.035 * t / 10;
      document.getElementById("fx-stage").style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) scale(${s})`;
    },
    // entrada cinematográfica: escala + desenfoque + opacidad
    enter(el, t, a, d = 0.6) {
      const k = Math.max(0, Math.min(1, (t - a) / d)), e = 1 - Math.pow(1 - k, 3);
      el.style.opacity = e; el.style.filter = `blur(${(1 - e) * 16}px)`;
      return e;
    },
    flash(t, at, d = 0.25) { const k = (t - at) / d; document.getElementById("fx-flash").style.opacity = k > 0 && k < 1 ? 0.35 * (1 - k) : 0; },
    shake(el, t, at, d = 0.35, amp = 18) {
      const k = (t - at) / d;
      return k > 0 && k < 1 ? `translate(${Math.sin(t * 90) * amp * (1 - k)}px, ${Math.cos(t * 70) * amp * (1 - k)}px)` : "";
    }
  };
})();
