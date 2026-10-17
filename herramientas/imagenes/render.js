// Renderiza a PNG las páginas generadas por generar_imagenes.py.
// Uso: node render.js /tmp/imagenes-build/jobs.json
const fs = require("fs");
const { chromium } = require(process.env.PW || "playwright");
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium" });
  const page = await browser.newPage();
  for (const j of jobs) {
    await page.setViewportSize({ width: j.w, height: j.h });
    await page.goto("file://" + j.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h } });
    console.log("ok", j.out.replace(process.cwd() + "/", ""));
  }
  await browser.close();
})();
