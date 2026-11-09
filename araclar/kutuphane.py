"""Picsum kataloğunu çekip her fotoğrafa ton etiketi verir → arkaplanlar.js

Kullanım: python3 araclar/kutuphane.py
"""
import colorsys, io, json, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image

MIN_KENAR = 2400  # bundan küçük fotoğraflar büyük ekranlarda bulanıklaşır


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "soz-duvari"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def katalog():
    out, page = [], 1
    while True:
        items = json.loads(get(f"https://picsum.photos/v2/list?page={page}&limit=100"))
        if not items:
            return out
        out += items
        page += 1


def etiketle(p):
    try:
        im = Image.open(io.BytesIO(get(f"https://picsum.photos/id/{p['id']}/48/32"))).convert("RGB")
    except Exception:
        return None
    px = list(im.getdata())
    r, g, b = (sum(c[i] for c in px) / len(px) for i in range(3))
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # ortalama renk doygunluğu düşük kalabilir; piksel başı doygunluğa da bak
    sat = sum(colorsys.rgb_to_hls(*(v / 255 for v in c))[2] for c in px) / len(px)
    tags = []
    if lum < 75: tags.append("koyu")
    if lum > 160: tags.append("aydinlik")
    if sat < 0.12: tags.append("renksiz")
    else:
        hd = h * 360
        if hd < 50 or hd >= 330: tags.append("sicak")
        elif hd < 160: tags.append("yesil")
        elif hd < 260: tags.append("soguk")
    return [int(p["id"]), p["author"], "#%02x%02x%02x" % (int(r), int(g), int(b)), tags]


def main():
    items = [p for p in katalog() if max(p["width"], p["height"]) >= MIN_KENAR]
    with ThreadPoolExecutor(24) as ex:
        rows = [r for r in ex.map(etiketle, items) if r]
    rows.sort(key=lambda r: r[0])
    hedef = Path(__file__).resolve().parent.parent / "arkaplanlar.js"
    hedef.write_text("// araclar/kutuphane.py üretir: [picsum id, fotoğrafçı, ortalama renk, etiketler]\n"
                     "const ARKAPLANLAR = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n")
    from collections import Counter
    print(len(rows), "fotoğraf", Counter(t for r in rows for t in r[3]))


main()
