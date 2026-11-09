# Söz Duvarı

Motivasyon sözü duvar kağıdı ve çerçeve posteri üreticisi.

- `index.html`: söz + yazar → Sade / Bant / Minimal stil, picsum arkaplan, cihaz boyutlarında PNG/JPG indirme
- `duvar.html`: galeri duvarı önizlemesi. Söz, format ve stil seç, seçilenleri ZIP indir
- `cerceve/`: 21 sözün 126 görseli, 5 çerçeve oranında (630 görsel)

| Klasör | Boyut |
|---|---|
| `dikey-2x3` | 2400×3600 |
| `dikey-3x4` | 2400×3200 |
| `dikey-A-serisi` | 2480×3508 (A4, 300 dpi) |
| `kare` | 3000×3000 |
| `yatay-3x2` | 3600×2400 |

## Çalıştırma

```
python3 -m http.server 8905
```
→ `http://localhost:8905/` ve `http://localhost:8905/duvar.html`

## Araçlar

- `araclar/render.mjs`: `index.html`'in kendi `render()`'ını headless Chrome'da çalıştırıp yeni oranlarda basar (playwright-core). Örnek: `FORMATS='[["kare",3000,3000]]' node araclar/render.mjs`
- `araclar/drive_klasoru.py`: `cerceve/`'yi `drive/Söz Duvarı/<Yazar - Söz>/<Format>/` düzenine dizer, `cerceve/liste.js`'i yazar
- `araclar/kutuphane.py`: picsum kataloğunu etiketleyip `arkaplanlar.js`'i üretir

Arkaplan fotoğrafları [Lorem Picsum](https://picsum.photos) (Unsplash) kaynaklıdır.
