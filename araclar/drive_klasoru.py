"""cerceve/ çıktısını Drive'a atmalık düzenli klasöre dizer + duvar.html için cerceve/liste.js yazar.

Yapı:  drive/Söz Duvarı/<Yazar - Söz>/<Format>/<Yazar - Format - Stil N>.jpg
Dosyalar hard link'tir (diskte ikinci kopya yer kaplamaz).

Kullanım: python3 araclar/drive_klasoru.py
"""
import json, os, re, shutil
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CER = KOK / 'cerceve'
HEDEF = KOK / 'drive' / 'Söz Duvarı'
Q = json.loads((Path(__file__).parent / 'quotes.json').read_text())

FORMAT = {
    'dikey-2x3':      'Dikey 2x3 (2400x3600)',
    'dikey-3x4':      'Dikey 3x4 (2400x3200)',
    'dikey-A-serisi': 'Dikey A serisi (2480x3508)',
    'kare':           'Kare (3000x3000)',
    'yatay-3x2':      'Yatay 3x2 (3600x2400)',
}
KISA = {'dikey-2x3': 'Dikey 2x3', 'dikey-3x4': 'Dikey 3x4', 'dikey-A-serisi': 'Dikey A',
        'kare': 'Kare', 'yatay-3x2': 'Yatay 3x2'}
STIL = {'sade': 'Sade', 'bant': 'Bant', 'minimal': 'Minimal'}


def temiz(s, n=70):
    s = re.sub(r'[\\/:*?"<>|]', '', s).replace('’', "'").strip()
    if len(s) > n:
        s = s[:n].rsplit(' ', 1)[0] + '…'
    return s.rstrip('. ')


def soz_klasoru(anahtar):
    soz, yazar = Q[anahtar]
    return temiz(f'{yazar} - {soz}')


# her söz içinde stil sırası (bant-281 → Bant 1)
sira = {}
for d in sorted(Q):
    dosyalar = sorted({f.split('__', 1)[1] for fmt in FORMAT for f in os.listdir(CER / fmt) if f.startswith(d + '__')},
                      key=lambda f: (f.split('-')[0], int(re.search(r'-(\d+)\.', f).group(1))))
    sayac = {}
    for f in dosyalar:
        st = f.split('-')[0]; sayac[st] = sayac.get(st, 0) + 1
        sira[(d, f)] = f'{STIL[st]} {sayac[st]}'

if HEDEF.exists():
    shutil.rmtree(HEDEF)
liste, sozler = [], {}
for fmt in FORMAT:
    for f in sorted(os.listdir(CER / fmt)):
        if not f.endswith('.jpg'):
            continue
        d, rest = f.split('__', 1)
        soz, yazar = Q[d]
        yol = f'{soz_klasoru(d)}/{FORMAT[fmt]}/{temiz(yazar)} - {KISA[fmt]} - {sira[(d, rest)]}.jpg'
        hedef = HEDEF / yol
        hedef.parent.mkdir(parents=True, exist_ok=True)
        os.link(CER / fmt / f, hedef)
        liste.append([fmt, f, d, rest.split('-')[0], yol])
        sozler[d] = [soz, yazar]

(CER / 'liste.js').write_text(
    '// araclar/drive_klasoru.py üretir: [format, dosya, söz, stil, drive yolu]\n'
    f'const CERCEVELER = {json.dumps(liste, ensure_ascii=False)};\n'
    f'const SOZLER = {json.dumps(sozler, ensure_ascii=False)};\n'
    f'const FORMAT_AD = {json.dumps(FORMAT, ensure_ascii=False)};\n')
print(len(liste), 'görsel →', HEDEF)
