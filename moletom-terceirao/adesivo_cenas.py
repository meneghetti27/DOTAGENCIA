"""Logo como adesivo colado em superfícies reais (texturas Poly Haven 2K) -> final/keyvisuals/ad-*.png (1920x1080)
Adesivo: borda branca de recorte, leve brilho, perspectiva, a textura da superfície aparece por baixo (relevo), sombra suave.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
from scipy import ndimage
from pathlib import Path

AQUI = Path(__file__).parent
TX = AQUI / "referencias/texturas"; OUT = AQUI / "final/keyvisuals"
ART = Image.open(AQUI / "final/arte-principal/terceirao-2027-principal-transparente.png").convert("RGBA")
ART = ART.crop(ART.getbbox())
S27 = Image.open(AQUI / "final/simbolo/simbolo-27-roxo.png").convert("RGBA"); S27 = S27.crop(S27.getbbox())
W, H = 1920, 1080


def superficie(nome, escala=1.0, brilho=.8, luz=(0.5, 0.45), cor_luz=(170, 120, 210), forca=.35):
    t = Image.open(TX / f"{nome}.jpg").convert("RGB")
    w = int(W * escala); t = t.resize((w, int(w * t.height / t.width)), Image.LANCZOS)
    base = Image.new("RGB", (W, H))
    for y in range(0, H, t.height):
        for x in range(0, W, t.width): base.paste(t, (x, y))
    base = ImageEnhance.Brightness(ImageEnhance.Color(base).enhance(.55)).enhance(brilho)
    a = np.asarray(base).astype(float)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx / W - luz[0]) * 1.6) ** 2 + (yy / H - luz[1]) ** 2)
    spot = np.clip(1.25 - d * 1.5, .25, 1.25)[..., None]
    a = a * spot + np.array(cor_luz) * forca * np.clip(1 - d * 1.4, 0, 1)[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)), np.asarray(base.convert("L")).astype(float)


def sem_brilhos(im):
    """tira os brilhos soltos: fica só o maior bloco (as letras)"""
    al = np.asarray(im.split()[3]) > 20
    lab, n = ndimage.label(ndimage.binary_dilation(al, iterations=4))
    if n > 1:
        tam = ndimage.sum(al, lab, range(1, n + 1)); keep = lab == (np.argmax(tam) + 1)
        a = np.asarray(im).copy(); a[..., 3] = np.where(keep, a[..., 3], 0); im = Image.fromarray(a)
    return im.crop(im.getbbox())


def adesivo(arte, larg, borda=18):
    arte = sem_brilhos(arte)
    a = arte.resize((larg, int(larg * arte.height / arte.width)), Image.LANCZOS)
    pad = borda * 2 + 10
    c = Image.new("RGBA", (a.width + pad * 2, a.height + pad * 2), (0, 0, 0, 0)); c.alpha_composite(a, (pad, pad))
    al = np.asarray(c.split()[3]) > 40
    corte = ndimage.binary_closing(ndimage.binary_dilation(al, iterations=borda), iterations=borda)
    corte = ndimage.gaussian_filter(corte.astype(float), .8)
    s = Image.new("RGBA", c.size, (246, 244, 248, 0)); s.putalpha(Image.fromarray((corte * 255).astype(np.uint8)))
    s.alpha_composite(c)
    # brilho de vinil: faixa diagonal suave
    g = np.zeros((s.height, s.width)); yy, xx = np.mgrid[0:s.height, 0:s.width]
    g = np.clip(1 - np.abs((xx + yy * .6) / (s.width * 1.2) - .35) * 6, 0, 1) * 38
    arr = np.asarray(s).astype(float); arr[..., :3] = np.clip(arr[..., :3] + g[..., None], 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def perspectiva(im, kx=0.0, ky=0.0, giro=0.0):
    im = im.rotate(giro, Image.BICUBIC, expand=True)
    w, h = im.size; dx, dy = kx * w, ky * h
    # coeficientes: mapeia quad de saída -> entrada (leve trapézio)
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    dst = [(dx, dy), (w - dx, 0), (w, h), (0, h - dy)]
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    coef = np.linalg.solve(np.array(A, float), np.array(B, float))
    return im.transform((w, h), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)


def cola(base, L, st, x, y, relevo=.55, sombra=(10, 16, 18, .55)):
    base = base.convert("RGBA")
    al = st.split()[3]
    sh = Image.new("RGBA", st.size, (0, 0, 0, 0)); sh.putalpha(al.point(lambda v: int(v * sombra[3])))
    sh = sh.filter(ImageFilter.GaussianBlur(sombra[2]))
    base.alpha_composite(sh, (x + sombra[0], y + sombra[1]))
    # relevo: luminância local da superfície modula o adesivo (ele "assenta" na textura)
    reg = L[y:y + st.height, x:x + st.width]
    reg = np.pad(reg, ((0, max(0, st.height - reg.shape[0])), (0, max(0, st.width - reg.shape[1]))), mode="edge")
    hp = reg - ndimage.gaussian_filter(reg, 6)
    a = np.asarray(st).astype(float)
    a[..., :3] = np.clip(a[..., :3] * (1 + hp[..., None] / 255 * relevo * 3), 0, 255)
    base.alpha_composite(Image.fromarray(a.astype(np.uint8)), (x, y))
    return base


def acabamento(im, vinheta=.75):
    a = np.asarray(im.convert("RGB")).astype(float)
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    a *= np.clip(1.15 - d * vinheta * .55, .2, 1)[..., None]
    a += np.random.default_rng(2).normal(0, 3.2, a.shape)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


CENAS = {
    "ad1-muro-concreto": dict(tx="concrete_wall_008", esc=1.1, brilho=.62, luz=(.55, .4), itens=[(ART, 470, 720, 150, 0, .03, -6)]),
    "ad2-muro-tijolo": dict(tx="brick_wall_001", esc=.7, brilho=.55, luz=(.45, .45), itens=[(ART, 380, 520, 160, 0, 0, -7), (S27, 420, 1020, 420, 0, 0, 9)]),
    "ad3-mesa-madeira": dict(tx="black_painted_planks", esc=.9, brilho=.9, luz=(.5, .35), itens=[(ART, 400, 560, 150, .06, .0, 12), (S27, 340, 1080, 560, .05, 0, -16)]),
    "ad4-asfalto": dict(tx="asphalt_floor", esc=.6, brilho=.45, luz=(.5, .5), itens=[(S27, 520, 720, 290, .08, 0, -4)]),
}

if __name__ == "__main__":
    for nome, c in CENAS.items():
        base, L = superficie(c["tx"], c["esc"], c["brilho"], c["luz"])
        for arte, larg, x, y, kx, ky, giro in c["itens"]:
            st = perspectiva(adesivo(arte, larg), kx, ky, giro)
            base = cola(base, L, st, x, y)
        acabamento(base).save(OUT / f"{nome}.png"); print("ok", nome)
