(function () {
  // Reading progress
  var bar = document.getElementById("progress-bar");
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Copy buttons on templates
  document.querySelectorAll("blockquote").forEach(function (bq) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copiar";
    btn.addEventListener("click", function () {
      var clone = bq.cloneNode(true);
      clone.querySelectorAll(".bq-tag, .copy-btn").forEach(function (n) { n.remove(); });
      var text = Array.from(clone.querySelectorAll("p")).map(function (p) { return p.innerText.trim(); }).join("\n\n") || clone.innerText.trim();
      function done() { btn.textContent = "Copiado"; setTimeout(function () { btn.textContent = "Copiar"; }, 1600); }
      function fallback() {
        var r = document.createRange();
        r.selectNodeContents(bq);
        var s = window.getSelection();
        s.removeAllRanges();
        s.addRange(r);
        btn.textContent = "Seleccionado";
      }
      try {
        navigator.clipboard.writeText(text).then(done, fallback);
      } catch (e) { fallback(); }
    });
    bq.appendChild(btn);
  });

  // Checklists, remembered on this device
  var KEY = "ct30-checks";
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { state = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  document.querySelectorAll(".checklist").forEach(function (cl, ci) {
    var items = cl.querySelectorAll("li");
    var head = cl.querySelector(".cl-head");
    var count = document.createElement("span");
    count.className = "cl-count";
    head.appendChild(count);
    function refresh() {
      var n = cl.querySelectorAll("li.done").length;
      count.textContent = n + " de " + items.length;
    }
    items.forEach(function (li, i) {
      var id = ci + "-" + i;
      li.setAttribute("role", "checkbox");
      li.tabIndex = 0;
      function set(on) {
        li.classList.toggle("done", on);
        li.setAttribute("aria-checked", on ? "true" : "false");
      }
      set(!!state[id]);
      function toggle() {
        state[id] = !state[id];
        set(state[id]);
        save();
        refresh();
      }
      li.addEventListener("click", toggle);
      li.addEventListener("keydown", function (e) {
        if (e.key === " " || e.key === "Enter") { e.preventDefault(); toggle(); }
      });
    });
    refresh();
  });
})();
