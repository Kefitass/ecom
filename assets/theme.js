/* Perfumería de Barrio · interacciones del tema */
(function () {
  document.documentElement.classList.add('js');
  var root = (window.Shopify && Shopify.routes && Shopify.routes.root) || '/';

  /* ---------- Formato de precios (igual al de la tienda) ---------- */
  function formatMoney(cents, format) {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    format = format || '${{amount_with_comma_separator}}';
    var match = format.match(/\{\{\s*(\w+)\s*\}\}/);
    if (!match) return String(cents);

    function withDelimiters(number, precision, thousands, decimal) {
      if (isNaN(number) || number == null) return '0';
      number = (number / 100).toFixed(precision);
      var parts = number.split('.');
      var whole = parts[0].replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1' + thousands);
      return parts[1] ? whole + decimal + parts[1] : whole;
    }

    var value;
    switch (match[1]) {
      case 'amount': value = withDelimiters(cents, 2, ',', '.'); break;
      case 'amount_no_decimals': value = withDelimiters(cents, 0, ',', '.'); break;
      case 'amount_with_comma_separator': value = withDelimiters(cents, 2, '.', ','); break;
      case 'amount_no_decimals_with_comma_separator': value = withDelimiters(cents, 0, '.', ','); break;
      case 'amount_with_apostrophe_separator': value = withDelimiters(cents, 2, "'", '.'); break;
      default: value = withDelimiters(cents, 2, ',', '.');
    }
    return format.replace(match[0], value).replace(/<[^>]*>/g, '');
  }

  /* ---------- Menú celular: cerrar al tocar afuera ---------- */
  document.addEventListener('click', function (event) {
    document.querySelectorAll('.mobile-menu[open]').forEach(function (details) {
      if (!details.contains(event.target)) details.removeAttribute('open');
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.mobile-menu[open]').forEach(function (d) { d.removeAttribute('open'); });
  });

  /* ---------- Barra "Seguí acá tu última compra" ---------- */
  document.querySelectorAll('[data-tracking-close]').forEach(function (button) {
    button.addEventListener('click', function () {
      var bar = button.closest('[data-tracking-bar]');
      if (bar) bar.hidden = true;
      try { sessionStorage.setItem('tracking-closed', '1'); } catch (e) {}
    });
  });
  try {
    if (sessionStorage.getItem('tracking-closed') === '1') {
      document.querySelectorAll('[data-tracking-bar]').forEach(function (bar) { bar.hidden = true; });
    }
  } catch (e) {}

  /* ---------- Slider de banners ---------- */
  document.querySelectorAll('[data-slideshow]').forEach(function (slider) {
    var track = slider.querySelector('[data-slideshow-track]');
    var slides = track.children;
    var dots = slider.querySelectorAll('[data-slideshow-dot]');
    var seconds = parseInt(slider.dataset.autoplay || '0', 10);
    var timer;

    function current() { return Math.round(track.scrollLeft / track.clientWidth); }
    function go(index) {
      var total = slides.length;
      index = (index + total) % total;
      track.scrollTo({ left: index * track.clientWidth, behavior: 'smooth' });
    }
    function restart() {
      clearInterval(timer);
      if (seconds > 0 && slides.length > 1) timer = setInterval(function () { go(current() + 1); }, seconds * 1000);
    }

    var prev = slider.querySelector('[data-slideshow-prev]');
    var next = slider.querySelector('[data-slideshow-next]');
    if (prev) prev.addEventListener('click', function () { go(current() - 1); restart(); });
    if (next) next.addEventListener('click', function () { go(current() + 1); restart(); });
    dots.forEach(function (dot) {
      dot.addEventListener('click', function () { go(parseInt(dot.dataset.slideshowDot, 10)); restart(); });
    });
    track.addEventListener('scroll', function () {
      var i = current();
      dots.forEach(function (dot, n) { dot.classList.toggle('is-active', n === i); });
    }, { passive: true });
    slider.addEventListener('mouseenter', function () { clearInterval(timer); });
    slider.addEventListener('mouseleave', restart);
    restart();
  });

  /* ---------- Carrusel de videos ---------- */
  document.querySelectorAll('[data-scroll]').forEach(function (button) {
    button.addEventListener('click', function () {
      var scroller = button.closest('.page-width').querySelector('[data-scroller]');
      if (scroller) scroller.scrollBy({ left: parseInt(button.dataset.scroll, 10) * scroller.clientWidth * 0.8, behavior: 'smooth' });
    });
  });

  /* ---------- Filtros: cerrados de entrada en celu y tablet ---------- */
  if (window.matchMedia('(max-width: 989px)').matches) {
    document.querySelectorAll('.filters__wrap[open]').forEach(function (d) { d.removeAttribute('open'); });
  }

  /* ---------- Reseñas: ver más ---------- */
  document.querySelectorAll('[data-review-more]').forEach(function (button) {
    button.addEventListener('click', function () {
      var grid = button.closest('.page-width').querySelector('[data-review-grid]');
      if (grid) grid.classList.add('is-open');
      button.parentElement.style.display = 'none';
    });
  });

  /* ---------- Ordenar catálogo ---------- */
  document.querySelectorAll('[data-sort-select]').forEach(function (select) {
    select.addEventListener('change', function () {
      var url = new URL(window.location.href);
      url.searchParams.set('sort_by', select.value);
      url.searchParams.delete('page');
      window.location.href = url.toString();
    });
  });

  /* ---------- Botones de cantidad (+ / -) ---------- */
  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-qty]');
    if (!button) return;
    var input = button.closest('.qty') && button.closest('.qty').querySelector('input');
    if (!input) return;
    var min = parseInt(input.min || '0', 10);
    input.value = Math.max(min, (parseInt(input.value, 10) || 0) + parseInt(button.dataset.qty, 10));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  /* ---------- Carrito: actualizar al cambiar cantidades ---------- */
  var cartForm = document.querySelector('[data-cart-form]');
  if (cartForm) {
    var cartTimer;
    cartForm.addEventListener('change', function (event) {
      if (!event.target.matches('[data-cart-qty]')) return;
      clearTimeout(cartTimer);
      cartTimer = setTimeout(function () {
        var update = cartForm.querySelector('[data-cart-update]');
        if (cartForm.requestSubmit) cartForm.requestSubmit(update);
        else update.click();
      }, 500);
    });
  }

  /* ---------- Página de producto ---------- */
  document.querySelectorAll('[data-product-section]').forEach(function (section) {
    var dataEl = section.querySelector('[data-product-json]');
    if (!dataEl) return;
    var data = JSON.parse(dataEl.textContent);
    var form = section.querySelector('[data-product-form]');
    var idInput = section.querySelector('[data-variant-id]');
    var addButton = section.querySelector('[data-add-button]');
    var addLabel = section.querySelector('[data-add-label]');
    var errorEl = section.querySelector('[data-form-error]');

    function setText(selector, text) {
      section.querySelectorAll(selector).forEach(function (el) { el.textContent = text; });
    }

    function showMedia(mediaId) {
      if (!mediaId) return;
      var slide = section.querySelector('.product__slide[data-media-id="' + mediaId + '"]');
      if (!slide) return;
      section.querySelectorAll('.product__slide').forEach(function (s) { s.classList.toggle('is-active', s === slide); });
      section.querySelectorAll('[data-thumb]').forEach(function (t) { t.classList.toggle('is-active', t.dataset.thumb === String(mediaId)); });
    }

    section.querySelectorAll('[data-thumb]').forEach(function (thumb) {
      thumb.addEventListener('click', function () { showMedia(thumb.dataset.thumb); });
    });

    function onOptionChange() {
      var options = [];
      section.querySelectorAll('[data-option-index]:checked').forEach(function (input) {
        options[parseInt(input.dataset.optionIndex, 10)] = input.value;
      });
      options.forEach(function (value, index) { setText('[data-option-label="' + index + '"]', value); });

      var variant = data.variants.find(function (v) {
        return v.options.every(function (value, i) { return value === options[i]; });
      });
      if (!variant) {
        addButton.disabled = true;
        addLabel.textContent = 'NO DISPONIBLE';
        return;
      }

      idInput.value = variant.id;
      setText('[data-price]', formatMoney(variant.price, data.moneyFormat));
      var compare = section.querySelector('[data-compare]');
      if (variant.compare_at_price && variant.compare_at_price > variant.price) {
        compare.textContent = formatMoney(variant.compare_at_price, data.moneyFormat);
        compare.hidden = false;
      } else {
        compare.hidden = true;
      }
      if (data.transferDiscount > 0) {
        setText('[data-transfer]', formatMoney(Math.floor(variant.price * (100 - data.transferDiscount) / 100), data.moneyFormat));
      }
      if (data.installments > 1) {
        setText('[data-installment]', formatMoney(Math.floor(variant.price / data.installments), data.moneyFormat));
        var ok = variant.price >= (data.installmentsMin || 0);
        section.querySelectorAll('[data-installments-yes]').forEach(function (el) { el.hidden = !ok; });
        section.querySelectorAll('[data-installments-no]').forEach(function (el) { el.hidden = ok; });
      }

      addButton.disabled = !variant.available;
      addLabel.textContent = variant.available ? data.addLabel : 'SIN STOCK';
      if (variant.featured_media) showMedia(variant.featured_media.id);

      var url = new URL(window.location.href);
      url.searchParams.set('variant', variant.id);
      window.history.replaceState({}, '', url.toString());
    }

    section.querySelectorAll('[data-option-index]').forEach(function (input) {
      input.addEventListener('change', onOptionChange);
    });

    /* Agregar al carrito sin recargar y llevar al carrito */
    if (form && window.fetch) {
      form.addEventListener('submit', function (event) {
        if (event.submitter && event.submitter.closest('.shopify-payment-button')) return;
        event.preventDefault();
        errorEl.hidden = true;
        addButton.disabled = true;
        addButton.setAttribute('aria-busy', 'true');

        fetch(root + 'cart/add.js', { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
          .then(function (response) { return response.json().then(function (json) { return { ok: response.ok, json: json }; }); })
          .then(function (result) {
            if (!result.ok) throw new Error(result.json.description || result.json.message || 'No pudimos agregar el producto.');
            window.location.href = root + 'cart';
          })
          .catch(function (error) {
            errorEl.textContent = error.message;
            errorEl.hidden = false;
            addButton.disabled = false;
            addButton.removeAttribute('aria-busy');
          });
      });
    }
  });
})();
