# Tratamento "impresso" dos recortes: posterização em paleta, retícula, grão, tom vintage e adesivo com faixas.
# Uso: python3 tratar-impresso.py pasta_dos_recortes pasta_saida
# As receitas de cada imagem estão no fim do arquivo (paleta de posterização, tamanho da retícula, força do grão).
import sys
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image, ImageDraw, ImageFilter, ImageChops
REC, OUT = sys.argv[1], sys.argv[2]

def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def carrega(n, larg=None):
    im = Image.open(f'{REC}/{n}.png').convert('RGBA')
    if larg and im.width != larg: im = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    return im

def luminancia(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    return (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255

def posteriza(im, cores, contraste=1.2):
    L = np.clip((luminancia(im) - 0.5) * contraste + 0.5, 0, 1)
    idx = np.minimum((L * len(cores)).astype(int), len(cores) - 1)
    pal = np.array([hexrgb(c) for c in cores], dtype=np.uint8)
    rgb = pal[idx]
    out = Image.fromarray(rgb, 'RGB').convert('RGBA'); out.putalpha(im.getchannel('A'))
    return out

def retícula(im, celula=9, cor='#0B0B14', forca=0.55, limiar=0.0):
    L = luminancia(im)
    h, w = L.shape
    camada = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(camada)
    for y in range(0, h, celula):
        for x in range(0, w, celula):
            esc = 1 - L[y:y + celula, x:x + celula].mean()
            if esc <= limiar: continue
            r = celula * 0.62 * np.sqrt(esc)
            cx, cy = x + celula / 2 + (celula / 2 if (y // celula) % 2 else 0), y + celula / 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    camada = ImageChops.multiply(camada, im.getchannel('A'))
    tinta = Image.new('RGBA', im.size, hexrgb(cor) + (0,)); tinta.putalpha(camada.point(lambda v: int(v * forca)))
    return Image.alpha_composite(im, tinta)

def grao(im, forca=28, semente=1):
    rng = np.random.default_rng(semente)
    a = np.asarray(im).astype(np.int16)
    ruido = rng.normal(0, forca, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + ruido, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

def vintage(im):
    a = np.asarray(im).astype(np.float32)
    rgb = a[..., :3]
    cinza = rgb.mean(axis=2, keepdims=True)
    rgb = rgb * 0.75 + cinza * 0.25
    rgb = rgb * np.array([1.06, 1.0, 0.86]) + np.array([10, 4, -6])
    rgb = (rgb - 128) * 1.15 + 128
    a[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

def faixas(im, faixas, desloc=(-0.035, 0.0)):
    # Adesivo: contorno branco + faixas coloridas empilhadas e deslocadas (de fora para dentro).
    A = im.getchannel('A')
    m = max(f[1] for f in faixas) + 40
    W, H = im.width + 2 * m, im.height + 2 * m
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mask = Image.new('L', (W, H), 0); mask.paste(A, (m, m))
    dist = distance_transform_edt(np.asarray(mask) < 128)
    dilata = lambda r: Image.fromarray(((dist <= r) * 255).astype(np.uint8), 'L')
    for k, (cor, raio) in enumerate(faixas):
        dx = int(desloc[0] * im.width * (raio / faixas[0][1])); dy = int(desloc[1] * im.height * (raio / faixas[0][1]))
        dil = dilata(raio)
        dil = ImageChops.offset(dil, dx, dy)
        if cor == 'pontos':
            camada = Image.new('RGBA', (W, H), hexrgb('#16205A') + (255,))
            dd = ImageDraw.Draw(camada)
            for y in range(0, H, 14):
                for x in range(0, W, 14):
                    dd.ellipse([x + 3, y + 3, x + 10, y + 10], fill=hexrgb('#3A6BFF') + (255,))
        else:
            camada = Image.new('RGBA', (W, H), hexrgb(cor) + (255,))
        camada.putalpha(dil)
        base = Image.alpha_composite(base, camada)
    branco = Image.new('RGBA', (W, H), (255, 255, 255, 255)); branco.putalpha(dilata(8))
    base = Image.alpha_composite(base, branco)
    corpo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); corpo.paste(im, (m, m))
    return Image.alpha_composite(base, corpo)

def salva(im, n): im.save(f'{OUT}/{n}.png', optimize=True); print(n, im.size)

dev = carrega('devoradora', 900)
dev = grao(retícula(vintage(dev), 7, '#2A1A10', 0.28, 0.35), 14)
salva(dev, 'devoradora')
salva(faixas(dev, [('#0B0B14', 150), ('#FF7A1A', 120), ('#FF5FA2', 88), ('pontos', 56)]), 'devoradora_adesivo')
salva(grao(vintage(carrega('homenzinho', 500)), 10), 'homenzinho')
salva(grao(vintage(carrega('mao', 900)), 10), 'mao')
salva(grao(retícula(posteriza(carrega('pilha', 900), ['#1E1408', '#4A3A1A', '#8C7A45', '#D8CC98', '#F4EDD0']), 7, '#120C04', 0.6), 12), 'pilha')
salva(grao(retícula(posteriza(carrega('tv', 800), ['#140A3A', '#3B1F9E', '#6A4BE0', '#B79CFF', '#F0E6FF'], 1.3), 8, '#0A0420', 0.45), 10), 'tv')
salva(grao(posteriza(carrega('empresario', 400), ['#0E1A48', '#2F6BFF', '#A9C2FF', '#F4F0E6']), 8), 'executivo')
salva(grao(retícula(posteriza(carrega('agarra', 700), ['#2A1466', '#6B3FD6', '#B48CFF', '#EBDDFF'], 1.3), 8, '#14082E', 0.4), 10), 'agarra')
salva(grao(retícula(posteriza(carrega('celular', 800), ['#2A1466', '#6B3FD6', '#B48CFF', '#EBDDFF'], 1.3), 8, '#14082E', 0.4), 10), 'celular')
salva(grao(posteriza(carrega('estresse', 900), ['#0E1A48', '#2348C8', '#6E93FF', '#F2E9D8'], 1.35), 10), 'estresse')
salva(grao(retícula(carrega('cerebro', 800), 8, '#4A1A10', 0.45), 12), 'cerebro')
salva(grao(retícula(posteriza(carrega('aponta', 900), ['#111111', '#3A3A3A', '#777777', '#B8B8B8', '#ECECEC'], 1.25), 7, '#000000', 0.35), 16), 'aponta')
salva(grao(retícula(posteriza(carrega('camera', 600), ['#111111', '#3A3A3A', '#777777', '#B8B8B8', '#ECECEC'], 1.2), 7, '#000000', 0.3), 14), 'camera')
salva(grao(posteriza(carrega('trompete', 600), ['#3A0A2A', '#D42A7A', '#FF6FB0', '#FFD84A'], 1.4), 8), 'trompete')
