"""Teste: arte aplicada em 3 fotos de mockup enviadas pelo dono (11 azul frente/costas, 15 close preto, 14 camiseta no plástico).
Remove a estampa original (máscara por cor + preenchimento por convolução normalizada que mantém o sombreado),
recolore o moletom azul pra preto e aplica a arte com sombra do tecido (mockup_foto.estampa). -> final/aplicacoes/dono-*.png
"""
import numpy as np
from PIL import Image
from scipy import ndimage
from pathlib import Path
from mockup_foto import estampa

AQUI = Path(__file__).parent
D = AQUI / "referencias/mockups/dono"; OUT = AQUI / "final/aplicacoes"
ART = Image.open(AQUI / "final/arte-principal/terceirao-2027-principal-transparente.png").convert("RGBA")


def preencher(a, m, sig=18):
    """apaga a área m preenchendo com o entorno borrado (por canal), várias escalas"""
    a = a.astype(float); keep = (~m).astype(float); out = a.copy()
    for s in (sig * 3, sig, sig / 2):
        num = np.dstack([ndimage.gaussian_filter(a[..., c] * keep, s) for c in range(3)])
        den = ndimage.gaussian_filter(keep, s)[..., None] + 1e-6
        out[m] = (num / den)[m]
    return out


def foto11():
    a = np.asarray(Image.open(D / "11.jpg").convert("RGB")).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    tecido = (b > 90) & (b > r + 40)                       # azul do moletom
    tecido = ndimage.binary_closing(tecido, iterations=6); tecido = ndimage.binary_fill_holes(tecido)
    estampa_m = tecido & ~((b > r + 40) & (b - g > 25) & (a.max(-1) < 245) & (r < 120))   # branco/amarelo dentro do moletom
    estampa_m = ndimage.binary_dilation(estampa_m, iterations=5) & tecido
    a = preencher(a, estampa_m, 14)
    L = a.mean(-1)
    base_l = np.median(L[tecido])
    preto = np.clip(L / base_l, .35, 1.7)[..., None] * np.array([28, 27, 31])   # recolor: mantém o sombreado, cor preta
    a = np.where(tecido[..., None], preto, a)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    estampa(im, ART, cx=1180, cy=1060, larg=330, desloc=2)            # costas
    estampa(im, ART, cx=720, cy=590, larg=78, desloc=1)               # peito
    im.convert("RGB").save(OUT / "dono-1-frente-costas.png")


def foto15():
    a = np.asarray(Image.open(D / "15.jpg").convert("RGB")).astype(float)
    L = a.mean(-1)
    m = (L > 70) & (np.arange(a.shape[1])[None, :] < 1700) & (np.arange(a.shape[0])[:, None] > 250)
    m = ndimage.binary_dilation(m, iterations=6)
    a = preencher(a, m, 22)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    estampa(im, ART, cx=1000, cy=1250, larg=1250, desloc=4)
    im.convert("RGB").save(OUT / "dono-2-close.png")


def foto14():
    a = np.asarray(Image.open(D / "14.jpg").convert("RGB")).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((r > g + 25) | ((r > 110) & (g > 80) & (b < 120))) & (np.arange(a.shape[0])[:, None] < 1100)
    m = ndimage.binary_dilation(m, iterations=4)
    plast = a.copy()
    a = preencher(a, m, 16)
    # devolve os reflexos do plástico (pixels claros e neutros) por cima
    brilho = (plast.min(-1) > 150) & (plast.max(-1) - plast.min(-1) < 30) & ~ndimage.binary_dilation(m, iterations=10)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    estampa(im, ART, cx=555, cy=660, larg=420, desloc=3)
    out = np.asarray(im.convert("RGB")).astype(float)
    out[brilho] = out[brilho] * .25 + plast[brilho] * .75
    out[1150:1240, :] = out[1100:1110, :].mean(axis=0)  # tira a legenda do autor
    Image.fromarray(out.astype(np.uint8)).save(OUT / "dono-3-plastico.png")


if __name__ == "__main__":
    foto11(); foto15(); foto14(); print("ok")


def generico(n, roupa, estampas, aplic, recolor=False, crop=None, saida=None):
    """roupa(a)->máscara do tecido; estampas(a, roupa)->máscara a apagar; aplic=[(cx,cy,larg)] em px da foto original"""
    im0 = Image.open(D / f"{n}.jpg").convert("RGB")
    K = 3 if im0.width < 1200 else 1
    im0 = im0.resize((im0.width * K, im0.height * K), Image.LANCZOS)
    a = np.asarray(im0).astype(float)
    R = ndimage.binary_fill_holes(ndimage.binary_closing(roupa(a), iterations=8))
    m = ndimage.binary_dilation(estampas(a, R), iterations=4 * K) & R
    a = preencher(a, m, 10 * K)
    if recolor:
        L = a.mean(-1); base = np.median(L[R])
        a = np.where(R[..., None], np.clip(L / base, .3, 1.8)[..., None] * np.array([30, 29, 33]), a)
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    for cx, cy, lg in aplic:
        estampa(im, ART, cx=cx * K, cy=cy * K, larg=lg * K, desloc=K)
    if crop: im = im.crop(tuple(c * K for c in crop))
    im.convert("RGB").save(OUT / saida)


def lote2():
    lum = lambda a: a.mean(-1)
    # 20: preto em fundo branco — True Romance
    generico(20, lambda a: lum(a) < 90, lambda a, R: lum(a) > 70,
             [(592, 262, 140), (225, 245, 62)], crop=(0, 100, 808, 632), saida="dono-4-relaxed.png")
    # 18: creme de costas -> preto
    sat = lambda a: a.max(-1) - a.min(-1)
    generico(18, lambda a: lum(a) > 120, lambda a, R: (sat(a) > 45) | (lum(a) < 150),
             [(540, 760, 400)], recolor=True, saida="dono-5-costas.png")
    # 17: preto com estampa e texto grande — tudo claro/colorido dentro da roupa
    generico(17, lambda a: (lum(a) < 70), lambda a, R: (lum(a) > 55) | (sat(a) > 35),
             [(505, 260, 170), (250, 230, 55)], saida="dono-6-bundle.png")
    # 19: verde/roxo -> preto
    generico(19, lambda a: (sat(a) > 18) & (lum(a) > 45), lambda a, R: (lum(a) > 120) | (sat(a) < 12),
             [(255, 380, 230), (640, 300, 70)], recolor=True, crop=(0, 120, 808, 632), saida="dono-7-oversize.png")
    # 16: meio zíper branco -> preto
    generico(16, lambda a: lum(a) > 150, lambda a, R: lum(a) < 140,
             [(440, 360, 150)], recolor=True, crop=(0, 90, 808, 540), saida="dono-8-ziper.png")


if __name__ == "__main__":
    lote2(); print("ok2")
