"""Aplica a arte no mockup de foto real (moletom preto frente + costas): final/aplicacoes/moletom-mockup.png

Técnica: foto ampliada 4x; arte encolhida e levemente inclinada; o tecido "passa por cima" da estampa:
- sombreamento: a luminância local da foto (normalizada pela média do tecido) multiplica a arte -> dobras e sombras;
- deslocamento: a arte é deformada um pouco pelo relevo (gradiente da luminância) -> acompanha as dobras;
- textura: leve grão + um pouco de transparência (tinta de serigrafia).
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from pathlib import Path

AQUI = Path(__file__).parent
FOTO = AQUI / "referencias/mockups/moletom-preto-frente-costas.png"
ART = AQUI / "midiakit/png/integrado-25-transparente.png"
OUT = AQUI / "final/aplicacoes"; OUT.mkdir(parents=True, exist_ok=True)
K = 4  # ampliação


def estampa(base, arte, cx, cy, larg, giro=0.0, forca_sombra=1.0, desloc=6.0):
    arte = arte.crop(arte.getbbox())
    m = int(arte.width * 0.06)   # margem: a deformação não pode puxar pixel de fora (cortava o topo do TER)
    pad = Image.new('RGBA', (arte.width + 2 * m, arte.height + 2 * m), (0, 0, 0, 0)); pad.paste(arte, (m, m)); arte = pad
    h = int(arte.height * larg / arte.width)
    arte = arte.resize((larg, h), Image.LANCZOS).rotate(giro, Image.BICUBIC, expand=True)
    x0, y0 = int(cx - arte.width / 2), int(cy - arte.height / 2)
    reg = base.crop((x0, y0, x0 + arte.width, y0 + arte.height)).convert("L")
    L = np.asarray(reg).astype(float)
    Lb = ndimage.gaussian_filter(L, 2)
    ref = np.median(Lb[Lb > 0]) if (Lb > 0).any() else 30
    sombra = np.clip((Lb + 6) / (ref + 6), 0.45, 1.6) ** forca_sombra          # >1 = luz, <1 = dobra
    gy, gx = np.gradient(ndimage.gaussian_filter(L, 6))
    gx, gy = gx / (np.abs(gx).max() + 1e-6), gy / (np.abs(gy).max() + 1e-6)
    a = np.asarray(arte).astype(float)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]].astype(float)
    def warp(ch): return ndimage.map_coordinates(ch, [yy + gy * desloc, xx + gx * desloc], order=1, mode="nearest")
    a = np.dstack([warp(a[..., c]) for c in range(4)])
    rgb = a[..., :3] * sombra[..., None] * 0.93
    rgb += np.random.default_rng(1).normal(0, 4, rgb.shape)                      # grão da tinta
    alpha = a[..., 3] * 0.96 * ndimage.binary_erosion(L < 150, iterations=6)   # só onde é tecido
    out = Image.fromarray(np.dstack([rgb.clip(0, 255), alpha]).astype(np.uint8), "RGBA")
    base.alpha_composite(out, (x0, y0))


if __name__ == "__main__":
    foto = Image.open(FOTO).convert("RGB")
    base = foto.resize((foto.width * K, foto.height * K), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2)).convert("RGBA")
    arte = Image.open(ART).convert("RGBA")
    # costas (moletom da direita): centro do tronco, abaixo do capuz
    estampa(base, arte, cx=468 * K, cy=200 * K, larg=int(128 * 1.12) * K, giro=0, desloc=0.6 * K)
    # frente (moletom da esquerda): peito esquerdo de quem veste = direita na foto
    estampa(base, arte, cx=197 * K, cy=130 * K, larg=int(34 * 1.12) * K, giro=0, desloc=2)
    base.convert("RGB").save(OUT / "moletom-mockup.png")
    # recortes de detalhe
    base.crop((330 * K, 20 * K, 610 * K, 340 * K)).convert("RGB").save(OUT / "moletom-mockup-costas.png")
    print("ok")
