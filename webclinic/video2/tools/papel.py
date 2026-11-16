#!/usr/bin/env python3
"""Texturas da colagem editorial da Web Clinic.

Uso:
  python3 tools/papel.py texturas public/            # papel-*.jpg e rasgo-*.png
  python3 tools/papel.py impresso entrada.png saida.png [ponto]
    recorte (PNG com alfa) -> P&B com retícula de impressão sutil + borda de papel branco cortada à mão
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

rng = np.random.default_rng(7)


def ruido(w, h, s):
    n = rng.random((h // s + 2, w // s + 2)).astype(np.float32)
    return np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255


def papel(w, h, base):
    b = np.array(Image.new('RGB', (w, h), base)).astype(np.float32)
    n = (ruido(w, h, 2) - .5) * 10 + (ruido(w, h, 9) - .5) * 8 + (ruido(w, h, 60) - .5) * 10
    im = Image.fromarray(np.clip(b + n[..., None], 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(int(w * h / 2500)):  # fibras
        x, y = rng.integers(0, w), rng.integers(0, h)
        l, a = rng.integers(6, 26), rng.random() * 6.28
        c = int(rng.integers(0, 2)) * 255
        d.line([(x, y), (x + l * np.cos(a), y + l * np.sin(a))], fill=(c, c, c, int(rng.integers(8, 22))), width=1)
    return im


def rasgo(w, h, cor, seed):
    r = np.random.default_rng(seed)
    pts, y = [], 40.0
    for x in range(0, w + 8, 8):
        y += r.normal(0, 4)
        y = min(max(y, 10), 70)
        pts.append((x, y + r.normal(0, 1.5)))
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).polygon(pts + [(w, h), (0, h)], fill=255)
    fib = Image.new('L', (w, h), 0)
    ImageDraw.Draw(fib).polygon([(x, y - r.uniform(4, 12)) for x, y in pts] + [(w, h), (0, h)], fill=255)
    fib = fib.filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste(Image.new('RGBA', (w, h), (250, 250, 247, 255)), (0, 0), fib)
    out.paste(papel(w, h, cor).convert('RGBA'), (0, 0), m)
    return out


def impresso(src, dst, dot=6):
    im = Image.open(src).convert('RGBA')
    a = im.split()[3]
    g = ImageOps.autocontrast(im.convert('L'), cutoff=1)
    arr = np.array(g).astype(np.float32) / 255
    h, w = arr.shape
    yy, xx = np.mgrid[0:h, 0:w]
    u = ((xx + yy) / np.sqrt(2)) % dot / dot - .5
    v = ((xx - yy) / np.sqrt(2)) % dot / dot - .5
    tela = (np.sqrt(u * u + v * v) / 0.7071 > np.sqrt(1 - arr)).astype(np.float32)
    g2 = Image.fromarray((np.clip(arr * 0.82 + tela * 0.18, 0, 1) * 255).astype(np.uint8))
    am = np.array(a) > 40
    borda = Image.fromarray((am * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15))
    jit = np.array(Image.fromarray((ruido(w, h, 5) * 255).astype(np.uint8))) / 255
    borda = Image.fromarray(((np.array(borda.filter(ImageFilter.GaussianBlur(2))) / 255 * (0.75 + 0.5 * jit)) > 0.62).astype(np.uint8) * 255)
    res = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    res.paste(papel(w, h, (250, 250, 247)).convert('RGBA'), (0, 0), borda)
    res.alpha_composite(Image.merge('RGBA', (g2, g2, g2, a)))
    res.save(dst)


if __name__ == '__main__':
    if sys.argv[1] == 'texturas':
        d = sys.argv[2].rstrip('/') + '/'
        for nome, cor in [('gelo', (238, 241, 244)), ('azul', (45, 127, 240)), ('navy', (11, 31, 58)), ('branco', (250, 250, 247))]:
            papel(1080, 1920, cor).save(f'{d}papel-{nome}.jpg', quality=92)
        for i, (nome, cor) in enumerate([('gelo', (238, 241, 244)), ('azul', (45, 127, 240)), ('branco', (250, 250, 247)), ('navy', (11, 31, 58))]):
            rasgo(1080, 600, cor, i + 1).save(f'{d}rasgo-{nome}.png')
    else:
        impresso(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 6)
