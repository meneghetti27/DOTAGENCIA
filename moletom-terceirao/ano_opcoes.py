"""12 fontes pro 2027 (resto da arte igual; til 26 a 85%): costas/ano-opcoes/"""
import costas, tils
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "ano-opcoes"; P.mkdir(exist_ok=True)
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85
FONTES = ["graffiti_youth.otf", "beat_mark.ttf", "urban_blocker.ttf", "grime_slime.ttf", "street_shade.ttf", "thomas_2.otf",
          "king_jack_style.ttf", "urban_heroes.ttf", "drop_shade.ttf", "urban_gear.ttf", "smoke_in_the_city.ttf", "bostero.ttf"]
ims = []
for i, f in enumerate(FONTES, 1):
    costas.ANO_FONTE = f
    h = P / f"_{i}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True))
    png = P / f"{i:02d}-{f.split('.')[0]}.png"; costas.render(h, png); h.unlink(); ims.append((i, f, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
c = Image.new("RGB", (4 * 500, 3 * 600), "#0A0A0C")
for k, (i, f, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((500, 600)); ImageDraw.Draw(im).text((12, 8), f"{i:02d}", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 4) * 500, (k // 4) * 600))
c.save(P / "todas.jpg", quality=88)
# zoom só no ano
z = Image.new("RGB", (4 * 500, 3 * 260), "#0A0A0C")
for k, (i, f, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").crop((300, 1330, 1200, 1730)).resize((500, 222)); d = ImageDraw.Draw(im)
    d.text((10, 6), f"{i:02d}", font=ft, fill="#FFD84D")
    z.paste(im, ((k % 4) * 500, (k // 4) * 260 + 30))
z.save(P / "zoom-ano.jpg", quality=88)
