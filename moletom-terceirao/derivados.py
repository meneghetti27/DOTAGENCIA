"""Versões derivadas pro manual: 1 cor (branco / roxo / preto), estampa corrida e exemplos de uso incorreto.
-> final/versoes-1cor/, final/padrao/, final/_manual/ (imagens só do manual)
"""
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

AQUI = Path(__file__).parent
F = AQUI / "final"
P = Image.open(AQUI / "midiakit/png/integrado-25-transparente.png").convert("RGBA")
S = Image.open(F / "simbolo/simbolo-27-roxo.png").convert("RGBA")
for d in ("versoes-1cor", "padrao", "_manual"): (F / d).mkdir(exist_ok=True)


def uma_cor(im, cor):
    """tudo que não é o contorno preto vira a cor; o preto vira buraco (cor do tecido) -> serigrafia 1 cor"""
    a = np.asarray(im).astype(int)
    preto = (a[..., :3].max(-1) < 45)
    alpha = np.where(preto, 0, a[..., 3]).astype(np.uint8)
    rgb = np.zeros_like(a[..., :3]); rgb[:] = Image.new("RGB", (1, 1), cor).getpixel((0, 0))
    return Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")


for nome, cor in (("branco", "#FFFFFF"), ("roxo", "#996BB3"), ("preto", "#0A0A0C")):
    uma_cor(P, cor).save(F / "versoes-1cor" / f"terceirao-1cor-{nome}.png")
    uma_cor(S, cor).save(F / "versoes-1cor" / f"simbolo-27-1cor-{nome}.png")

# estampa corrida: 27 + brilhos em grade intercalada
W, H = 2400, 2400
pat = Image.new("RGBA", (W, H), (10, 10, 12, 255))
s = S.crop(S.getbbox()); s = s.resize((260, int(260 * s.height / s.width)), Image.LANCZOS)
s1 = uma_cor(s, "#2A1D35")
for j, y in enumerate(range(-100, H + 200, 300)):
    for i, x in enumerate(range(-100 + (180 if j % 2 else 0), W + 200, 360)):
        t = s if (i + j) % 4 == 0 else s1
        pat.alpha_composite(t.rotate(-8 if (i + j) % 2 else 6, expand=True), (x, y))
pat.convert("RGB").save(F / "padrao" / "estampa-corrida-27.png")

# usos incorretos
bg = Image.new("RGBA", (900, 900), (10, 10, 12, 255))
def cena(im, fundo=None):
    c = (fundo or bg).copy(); im = im.copy(); im.thumbnail((760, 760)); c.alpha_composite(im, ((900 - im.width) // 2, (900 - im.height) // 2)); return c.convert("RGB")
cena(P.resize((P.width * 2, P.height)), ).save(F / "_manual" / "errado-esticar.png")
cor = P.copy(); r, g, b, a = cor.split(); cena(Image.merge("RGBA", (g, b, r, a))).save(F / "_manual" / "errado-cor.png")
cena(P.rotate(35, expand=True)).save(F / "_manual" / "errado-girar.png")
foto = Image.open(AQUI / "referencias/mockups/camiseta-preta.jpg").convert("RGB").resize((900, 900))
foto = ImageEnhance.Brightness(ImageEnhance.Color(foto).enhance(3)).enhance(2.6).convert("RGBA")
cena(P, foto).save(F / "_manual" / "errado-fundo.png")
neg = Image.open(AQUI / "midiakit/png/integrado-25-transparente.png").convert("RGBA")
cena(neg, Image.new("RGBA", (900, 900), (244, 241, 247, 255))).save(F / "_manual" / "errado-claro.png")
ef = P.copy(); al = ef.split()[3].point(lambda v: v * 0.35); ef.putalpha(al); cena(ef).save(F / "_manual" / "errado-transparencia.png")
print("ok")
