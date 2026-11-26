"""2027 com o mesmo acabamento das letras: 12 opções (fonte x tamanho): costas/ano-letras/"""
import costas, tils
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "ano-letras"; P.mkdir(exist_ok=True)
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85; costas.ANO_ESTILO = "letras"
OP = [("graffiti_youth.otf", 190), ("graffiti_youth.otf", 240), ("beat_mark.ttf", 200), ("beat_mark.ttf", 250),
      ("king_jack_style.ttf", 190), ("king_jack_style.ttf", 230), ("grime_slime.ttf", 200), ("urban_gear.ttf", 200),
      ("urban_heroes.ttf", 210), ("drop_shade.ttf", 190), ("urban_blocker.ttf", 210), ("street_shade.ttf", 220)]
ims = []
for i, (f, t) in enumerate(OP, 1):
    costas.ANO_FONTE, costas.ANO_TAM = f, t
    h = P / f"_{i}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True))
    png = P / f"{i:02d}-{f.split('.')[0]}-{t}.png"; costas.render(h, png); h.unlink(); ims.append(png)
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
c = Image.new("RGB", (4 * 500, 3 * 600), "#0A0A0C")
for k, p in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((500, 600)); ImageDraw.Draw(im).text((12, 8), f"{k+1:02d}", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 4) * 500, (k // 4) * 600))
c.save(P / "todas.jpg", quality=88)
