#!/usr/bin/env python3
"""Recorta personagens de uma folha com fundo verde (#00FF00).
Uso: python3 recortar.py folha.png pasta_saida prefixo
Gera prefixo-1.png, prefixo-2.png... (um por personagem, da esquerda pra direita), fundo transparente."""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
src, out, pre = sys.argv[1:4]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
verde = (g - np.maximum(r, b))  # quanto "mais verde" que o resto
alfa = np.clip(1 - (verde - 40) / 60, 0, 1)  # >100 = fundo, <40 = personagem
# tira o verde que vaza na borda
desp = a.copy(); m = g > np.maximum(r, b); desp[..., 1] = np.where(m, np.maximum(r, b), g)
mask = alfa > 0.5
lab, n = ndimage.label(ndimage.binary_closing(mask, iterations=3))
tam = ndimage.sum(mask, lab, range(1, n + 1))
grandes = [i + 1 for i, t in enumerate(tam) if t > mask.size * 0.01]
objs = ndimage.find_objects(lab)
grandes.sort(key=lambda i: objs[i - 1][1].start)
for k, i in enumerate(grandes, 1):
    sl = objs[i - 1]; pad = 6
    y0, y1 = max(sl[0].start - pad, 0), min(sl[0].stop + pad, a.shape[0])
    x0, x1 = max(sl[1].start - pad, 0), min(sl[1].stop + pad, a.shape[1])
    al = (alfa * (lab == i))[y0:y1, x0:x1]
    al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)))
    rgba = np.dstack([desp[y0:y1, x0:x1].astype(np.uint8), al])
    Image.fromarray(rgba, 'RGBA').save(f'{out}/{pre}-{k}.png')
    print(f'{pre}-{k}.png', x1 - x0, y1 - y0, 'base y', y1, 'x0', x0)
