"""tils 8, 30 e 26 em 3 tamanhos menores: costas/tils-menores/"""
import costas, tils
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "tils-menores"; P.mkdir(exist_ok=True)
ims = []
for n in (8, 30, 26):
    a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[n - 1]
    for esc in (0.85, 0.72, 0.60):
        costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
        costas.TIL_ESC = esc
        nome = f"til{n:02d}-{int(esc*100)}"
        h = P / f"_{nome}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True))
        png = P / f"{nome}.png"; costas.render(h, png); h.unlink(); ims.append((nome, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
c = Image.new("RGB", (3 * 500, 3 * 500), "#0A0A0C")
for k, (nome, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").crop((250, 450, 1250, 1450)).resize((500, 500))
    ImageDraw.Draw(im).text((10, 6), nome.replace("til", "").replace("-", " · ") + "%", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 3) * 500, (k // 3) * 500))
c.save(P / "todos.jpg", quality=88)
