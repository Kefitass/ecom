// node instagram/fondos/grabar.js fondo-bloque3  →  instagram/fondos/fondo-bloque3.mp4 (1080x1920, 30 fps, 10 s)
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const name = process.argv[2] || "fondo-bloque3";
const secs = Number(process.argv[3] || 10);
const fps = 30;
const html = path.join(__dirname, name + ".html");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), name + "-"));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto("file://" + html);
  await page.evaluate(() => document.fonts.ready);
  for (let f = 0; f < secs * fps; f++) {
    await page.evaluate(t => render(t), f / fps);
    await page.screenshot({ path: path.join(tmp, String(f).padStart(4, "0") + ".png") });
  }
  await browser.close();
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(tmp, "%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", path.join(__dirname, name + ".mp4")]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(name + ".mp4 listo");
})();
