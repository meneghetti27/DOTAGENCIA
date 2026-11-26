"""ano no mesmo plano do adesivo (emendado no RÃO), variações das 25 e 30: costas/ano-integrado/"""
import costas, tils
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "ano-integrado"; P.mkdir(exist_ok=True)
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85
KJ, GS, GY = "king_jack_style.ttf", "grime_slime.ttf", "graffiti_youth.otf"
V = []
for txt, tams in (("2027", (190, 240)), ("'27", (260, 330))):
    for fonte in (KJ, GS):
        for tam in tams:
            for cor in ("branco", "roxo"):
                for ax in (0.72, 0.5):
                    V.append(dict(txt=txt, fonte=fonte, fam="A", tam=tam, ax=ax, ay=0, rot=-6, cor=cor, esc_dy=25))
V = V[:40]
ims = []
for i, v in enumerate(V, 1):
    costas.ANO_FONTE = v.pop("fonte"); costas.ANO_INT = v
    h = P / f"_{i}.html"; h.write_text(costas.html(GY, True, True))
    png = P / f"{i:02d}.png"; costas.render(h, png); h.unlink(); ims.append((i, v, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
fts = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
c = Image.new("RGB", (8 * 300, 5 * 400), "#0A0A0C")
for k, (i, v, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").resize((300, 360)); ImageDraw.Draw(im).text((8, 4), f"{i:02d}", font=ft, fill="#FFD84D")
    t = Image.new("RGB", (300, 40), "#0A0A0C")
    ImageDraw.Draw(t).text((6, 8), f"{v['txt']} {costas.ANO_FONTE[:0]}{v['tam']} {v['cor']} {'dir' if v['ax']>0.6 else 'centro'}", font=fts, fill="#BBB")
    c.paste(im, ((k % 8) * 300, (k // 8) * 400)); c.paste(t, ((k % 8) * 300, (k // 8) * 400 + 360))
c.save(P / "todas.jpg", quality=86)
