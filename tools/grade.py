#!/usr/bin/env python3
"""Color grade da dot: deixa qualquer foto com a mesma cara (sombras azul-marinho, luzes branco-azuladas,
azul vivo nos meios-tons, bloom nos realces e vinheta) e recorta em 1080x1350.

Uso: python3 tools/grade.py entrada.jpg saida.png [--foco X Y] [--forca 0.55] [--escuro 0.85] [--zoom 1.0]
  --foco: ponto (0–1) que fica no centro do recorte 4:5 (padrão 0.5 0.5)
  --forca: quanto puxar para a paleta (0 = original, 1 = duotone total)
  --escuro: brilho final (1 = igual)
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--foco", nargs=2, type=float, default=[0.5, 0.5])
ap.add_argument("--forca", type=float, default=0.55)
ap.add_argument("--escuro", type=float, default=0.85)
ap.add_argument("--zoom", type=float, default=1.0)
ap.add_argument("--sat", type=float, default=1.35)
ap.add_argument("--contraste", type=float, default=1.3)
ap.add_argument("--descer", type=int, default=0, help="empurra a foto N px para baixo; o topo vira água/céu escuro")
a = ap.parse_args()

W, H = 1080, 1350
im = Image.open(a.inp).convert("RGB")
# recorte 4:5 em torno do foco
iw, ih = im.size
ch = ih / a.zoom; cw = ch * W / H
if cw > iw / a.zoom:
    cw = iw / a.zoom; ch = cw * H / W
cx = min(max(a.foco[0] * iw, cw / 2), iw - cw / 2); cy = min(max(a.foco[1] * ih, ch / 2), ih - ch / 2)
im = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS)
im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
if a.descer:
    n = a.descer; cv = Image.new("RGB", (W, H))
    topo = im.crop((0, 0, W, 8)).resize((1, 1)).getpixel((0, 0))
    fundo = tuple(int(c * 0.55) for c in topo)
    grad = Image.linear_gradient("L").resize((W, n + 1))
    cv.paste(Image.composite(Image.new("RGB", (W, n + 1), topo), Image.new("RGB", (W, n + 1), fundo), grad), (0, 0))
    cv.paste(im.crop((0, 0, W, H - n)), (0, n))
    seam = 220; m = Image.linear_gradient("L").resize((W, seam))
    cv.paste(Image.composite(cv.crop((0, n, W, n + seam)), Image.new("RGB", (W, seam), topo), m), (0, n))
    im = cv.filter(ImageFilter.GaussianBlur(0)) 

x = np.asarray(im).astype(np.float32) / 255.0
lum = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
# curva em S suave no brilho
lum_c = np.clip((lum - 0.5) * a.contraste + 0.5, 0, 1)
# paleta: preto azulado -> azul dot -> azul claro -> branco gelo
stops = np.array([[0.00, 4, 6, 16], [0.28, 14, 30, 90], [0.55, 52, 100, 235], [0.80, 150, 185, 255], [1.00, 236, 242, 255]], np.float32)
duo = np.stack([np.interp(lum_c[..., 0], stops[:, 0], stops[:, k]) for k in (1, 2, 3)], -1) / 255.0
y = x * (1 - a.forca) + duo * a.forca
# realça azuis e tira amarelo/verde demais
y[..., 2] = np.clip(y[..., 2] * 1.06, 0, 1); y[..., 1] = y[..., 1] * 0.97
# contraste + saturação (cor viva)
y = np.clip((y - 0.5) * (1 + (a.contraste - 1) * 0.6) + 0.5, 0, 1)
g = y.mean(-1, keepdims=True); y = np.clip(g + (y - g) * a.sat, 0, 1)
y = y * a.escuro
# vinheta
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
y = y * np.clip(1.15 - 0.55 * d ** 2, 0.35, 1)[..., None]
out = Image.fromarray((np.clip(y, 0, 1) * 255).astype(np.uint8))
# bloom nos realces
hi = out.convert("L").point(lambda v: 0 if v < 175 else int((v - 175) * 3.1))
glow = Image.merge("RGB", [hi.point(lambda v: int(v * .55)), hi.point(lambda v: int(v * .75)), hi]).filter(ImageFilter.GaussianBlur(22))
o = np.asarray(out).astype(np.float32) / 255; g = np.asarray(glow).astype(np.float32) / 255
o = 1 - (1 - o) * (1 - g * 0.8)
Image.fromarray((np.clip(o, 0, 1) * 255).astype(np.uint8)).save(a.out)
print("ok", a.out)
