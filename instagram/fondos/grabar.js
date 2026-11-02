// node instagram/fondos/grabar.js fondo-bloque3  →  instagram/fondos/fondo-bloque3.mp4 (1080x1920, 30 fps, 10 s)
// Opcional: segundos, ancho, alto y nombre de salida → grabar.js fondo-fundador 10 1920 1080 fondo-fundador-horizontal
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const name = process.argv[2] || "fondo-bloque3";
const secs = Number(process.argv[3] || 10);
const width = Number(process.argv[4] || 1080), height = Number(process.argv[5] || 1920);
const out = process.argv[6] || name;
const fps = 30;
const html = path.join(__dirname, name + ".html");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), path.basename(name) + "-"));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto("file://" + html);
  await page.evaluate(() => document.fonts.ready);
  for (let f = 0; f < secs * fps; f++) {
    await page.evaluate(t => render(t), f / fps);
    await page.screenshot({ path: path.join(tmp, String(f).padStart(4, "0") + ".png") });
  }
  await browser.close();
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(tmp, "%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", path.join(__dirname, out + ".mp4")]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(out + ".mp4 listo");
})();
