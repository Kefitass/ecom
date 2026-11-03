/* Perfumería de Barrio · interacciones del tema */
(function () {
  document.documentElement.classList.add('js');

  /* ---------- Formato de precios ---------- */
  function formatMoney(cents, format) {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    format = format || '${{amount}}';
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
    // Igual que money_without_trailing_zeros: saca ",00" / ".00"
    value = value.replace(/[.,]00$/, '');
    return format.replace(match[0], value).replace(/<[^>]*>/g, '');
  }

  /* ---------- Cerrar menús desplegables al tocar afuera ---------- */
  document.addEventListener('click', function (event) {
    document.querySelectorAll('.mobile-menu[open], .header-search[open]').forEach(function (details) {
      if (!details.contains(event.target)) details.removeAttribute('open');
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.mobile-menu[open], .header-search[open]').forEach(function (d) { d.removeAttribute('open'); });
  });
  document.querySelectorAll('.header-search').forEach(function (details) {
    details.addEventListener('toggle', function () {
      if (details.open) {
        var input = details.querySelector('input[type="search"]');
        if (input) input.focus();
      }
    });
  });

  /* ---------- Botones de cantidad (+ / -) ---------- */
  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-qty]');
    if (!button) return;
    var wrapper = button.closest('.qty');
    var input = wrapper && wrapper.querySelector('input');
    if (!input) return;
    var min = parseInt(input.min || '0', 10);
    var next = Math.max(min, (parseInt(input.value, 10) || 0) + parseInt(button.dataset.qty, 10));
    input.value = next;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  /* ---------- Carrito: actualizar al cambiar cantidades ---------- */
  var cartForm = document.querySelector('[data-cart-form]');
  if (cartForm) {
    var timer;
    cartForm.addEventListener('change', function (event) {
      if (!event.target.matches('[data-cart-qty]')) return;
      clearTimeout(timer);
      timer = setTimeout(function () {
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

    function selectedOptions() {
      var values = [];
      section.querySelectorAll('[data-option-index]:checked').forEach(function (input) {
        values[parseInt(input.dataset.optionIndex, 10)] = input.value;
      });
      return values;
    }

    function updateInstallments(price) {
      var box = section.querySelector('[data-installments]');
      if (!box) return;
      var html = '';
      if (data.installmentsShow && data.installments > 1) {
        html += '<p class="installments">' + data.installments + ' cuotas sin interés';
        if (data.installmentsAmount) html += ' de <strong>' + formatMoney(Math.floor(price / data.installments), data.moneyFormat) + '</strong>';
        html += '</p>';
      }
      if (data.transferDiscount > 0) {
        var transfer = Math.floor(price * (100 - data.transferDiscount) / 100);
        html += '<p class="transfer-price"><strong>' + formatMoney(transfer, data.moneyFormat) + '</strong> con transferencia (' + data.transferDiscount + '% OFF)</p>';
      }
      box.innerHTML = html;
    }

    function onOptionChange() {
      var options = selectedOptions();
      options.forEach(function (value, index) {
        var label = section.querySelector('[data-option-label="' + index + '"]');
        if (label) label.textContent = value;
      });

      var variant = data.variants.find(function (v) {
        return v.options.every(function (value, i) { return value === options[i]; });
      });

      if (!variant) {
        addButton.disabled = true;
        addLabel.textContent = 'No disponible';
        return;
      }

      idInput.value = variant.id;
      section.querySelector('[data-price]').textContent = formatMoney(variant.price, data.moneyFormat);

      var compare = section.querySelector('[data-compare]');
      var off = section.querySelector('[data-off]');
      if (variant.compare_at_price && variant.compare_at_price > variant.price) {
        compare.textContent = formatMoney(variant.compare_at_price, data.moneyFormat);
        compare.hidden = false;
        off.textContent = Math.floor((variant.compare_at_price - variant.price) * 100 / variant.compare_at_price) + '% OFF';
        off.hidden = false;
      } else {
        compare.hidden = true;
        off.hidden = true;
      }

      updateInstallments(variant.price);
      addButton.disabled = !variant.available;
      addLabel.textContent = variant.available ? data.addLabel : 'Sin stock';
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

        fetch((window.Shopify && Shopify.routes ? Shopify.routes.root : '/') + 'cart/add.js', {
          method: 'POST',
          headers: { Accept: 'application/json' },
          body: new FormData(form)
        })
          .then(function (response) { return response.json().then(function (json) { return { ok: response.ok, json: json }; }); })
          .then(function (result) {
            if (!result.ok) throw new Error(result.json.description || result.json.message || 'No pudimos agregar el producto.');
            window.location.href = (window.Shopify && Shopify.routes ? Shopify.routes.root : '/') + 'cart';
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
