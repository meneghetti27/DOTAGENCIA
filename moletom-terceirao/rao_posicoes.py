"""20 posições do RÃO (só ele anda pra direita) pra escolher: costas/rao-posicoes/"""
import costas
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "rao-posicoes"
ims = []
for i, dx in enumerate(range(30, 230, 10), 1):
    costas.LINHAS = [("TER", -5, -15), ("CEI", -3, 15), ("RÃO", -5, dx)]
    h = P / f"_{i}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True))
    png = P / f"{i:02d}-rao-{dx}.png"; costas.render(h, png); h.unlink(); ims.append((i, dx, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
c = Image.new("RGB", (5 * 450, 4 * 540), "#0A0A0C")
for k, (i, dx, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((450, 540)); d = ImageDraw.Draw(im)
    d.text((14, 8), f"{i:02d}", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 5) * 450, (k // 5) * 540))
c.save(P / "todas.jpg", quality=85)
