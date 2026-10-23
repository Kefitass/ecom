const { chromium } = require('playwright');
(async () => {
  const [,, inp, out] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'load' });
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font-family:Inter;font-size:8px;color:#9CA3AF;padding:0 20mm;display:flex;justify-content:space-between"><span>Conseguí trabajo en 30 días</span><span class="pageNumber"></span></div>' });
  await b.close();
})();
