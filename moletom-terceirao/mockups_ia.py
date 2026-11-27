"""Aplica a marca nas fotos de mockup geradas por IA (ElevenLabs): camiseta preta e boné. -> final/aplicacoes/"""
from PIL import Image, ImageFilter
from mockup_foto import estampa, OUT
from pathlib import Path
R = Path(__file__).parent / "referencias/mockups"
ART = Image.open(Path(__file__).parent / "midiakit/png/integrado-25-transparente.png").convert("RGBA")
S27 = Image.open(Path(__file__).parent / "final/simbolo/simbolo-27-roxo.png").convert("RGBA")
K = 2
def base(f):
    im = Image.open(R / f).convert("RGB")
    return im.resize((im.width * K, im.height * K), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 50, 2)).convert("RGBA")
b = base("camiseta-preta.jpg"); estampa(b, ART, cx=700 * K, cy=360 * K, larg=250 * K, desloc=0.6 * K)
b.convert("RGB").save(OUT / "camiseta-mockup.png")
b = base("bone-preto.jpg"); estampa(b, S27, cx=688 * K, cy=420 * K, larg=190 * K, giro=0, desloc=0.5 * K)
b.convert("RGB").save(OUT / "bone-mockup.png")
print("ok")
