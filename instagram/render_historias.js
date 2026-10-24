// node instagram/render_historias.js  →  instagram/historias/<destacada>/<n>.png
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "historias");
const ids = JSON.parse(fs.readFileSync(path.join(dir, "_ids.json"), "utf8"));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto("file://" + path.join(dir, "_historias.html"));
  await page.evaluate(() => document.fonts.ready);
  for (const id of ids) {
    const [folder, name] = id.split("--");
    fs.mkdirSync(path.join(dir, folder), { recursive: true });
    await page.locator('[id="' + id + '"]').screenshot({ path: path.join(dir, folder, name + ".png") });
  }
  await browser.close();
  console.log(ids.length + " PNG");
})();
