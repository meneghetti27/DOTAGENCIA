"""20 espaçamentos entre CEI e RÃO (RÃO na posição 12 = dx 140): costas/rao-espaco/"""
import costas
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "rao-espaco"
ims = []
for i in range(1, 21):
    costas.GAP = round(0.02 * (i - 1), 2)   # 0.00 ... 0.38
    h = P / f"_{i}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True).replace("{GAP}", str(costas.GAP)))
    png = P / f"{i:02d}-espaco-{costas.GAP}.png"; costas.render(h, png); h.unlink(); ims.append((i, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
c = Image.new("RGB", (5 * 450, 4 * 540), "#0A0A0C")
for k, (i, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((450, 540)); ImageDraw.Draw(im).text((14, 8), f"{i:02d}", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 5) * 450, (k // 5) * 540))
c.save(P / "todas.jpg", quality=85)
