import { chromium } from '/Users/yerdekalmazer/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core/index.mjs';
import fs from 'fs'; import path from 'path';
const ROOT = '/Users/yerdekalmazer/Desktop/Projeler/Bireysel/soz-duvari';
const Q = JSON.parse(fs.readFileSync(new URL('./quotes.json', import.meta.url)));
const FORMATS = JSON.parse(process.env.FORMATS);
const only = process.env.ONLY;
const out = process.env.OUT || path.join(ROOT, 'cerceve');
const b = await chromium.launch({ channel: 'chrome' });
const pg = await b.newPage({ viewport: { width: 1400, height: 900 } });
await pg.goto('http://localhost:8905/index.html'); await pg.waitForTimeout(800);
const jobs = [];
for (const d of fs.readdirSync(path.join(ROOT, 'uretilen'))) {
  if (!Q[d] || (only && !d.includes(only))) continue;
  for (const f of fs.readdirSync(path.join(ROOT, 'uretilen', d))) {
    const m = f.match(/^(sade|bant|minimal)-(\d+)\.jpg$/); if (!m) continue;
    for (const [fmt, W, H] of FORMATS) jobs.push({ d, style: m[1], id: +m[2], fmt, W, H });
  }
}
let n = 0, fails = 0;
for (const j of jobs) {
  const dst = path.join(out, j.fmt, `${j.d}__${j.style}-${j.id}.jpg`);
  if (fs.existsSync(dst)) { n++; continue; }
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  const [q, a] = Q[j.d];
  let ok = false;
  for (let t = 0; t < 8 && !ok; t++) try {
    if (t) await pg.waitForTimeout(3000 * t);
    const data = await pg.evaluate(async ({ j, q, a }) => {
      const st = STYLES[j.style];
      S = { ...DEF, quote: q, author: a, style: j.style, font: st.font, size: st.size, W: j.W, H: j.H, preset: 'custom', bg: { type: 'id', id: j.id } };
      const F = FONTS[S.font];
      await document.fonts.load(`${F.it ? 'italic ' : ''}${F.w} 40px "${F.fam}"`, q);
      await document.fonts.load(`${F.aW} 40px "${F.aFam}"`, a);
      img = await loadImg(bgURL());
      const cv = document.createElement('canvas'); cv.width = j.W; cv.height = j.H;
      render(cv, j.W, j.H);
      return cv.toDataURL('image/jpeg', 0.92);
    }, { j, q, a });
    fs.writeFileSync(dst, Buffer.from(data.split(',')[1], 'base64'));
    ok = true;
  } catch (e) { console.error('retry', dst, e.message); }
  if (!ok) { console.error('BASARISIZ', dst); fails++; }
  await pg.waitForTimeout(400);
  if (++n % 25 === 0) console.log(n, '/', jobs.length);
}
console.log('bitti', n, jobs.length, 'basarisiz', fails);
await b.close();
