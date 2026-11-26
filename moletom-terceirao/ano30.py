"""30 estilos de ano emendado no adesivo (a partir do emendado 25): costas/ano30/"""
import costas, tils
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "ano30"; P.mkdir(exist_ok=True)
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85
GS, KJ, BM, UG, UB, GY, BO, SS = ("grime_slime.ttf", "king_jack_style.ttf", "beat_mark.ttf", "urban_gear.ttf",
    "urban_blocker.ttf", "graffiti_youth.otf", "bostero.ttf", "street_shade.ttf")
D = lambda txt, f, tam, cor, ax=0.72, ay=0, rot=-6: (f, dict(txt=txt, fam="A", tam=tam, ax=ax, ay=ay, rot=rot, cor=cor, esc_dy=25))
V = [  # descrição, (fonte, params)
 ("'27 GS branco (o 25)", D("'27", GS, 260, "branco")),
 ("'27 GS meio branco/roxo", D("'27", GS, 260, "meio")),
 ("'27 GS lilás claro", D("'27", GS, 260, "lilas")),
 ("'27 GS preto c/ borda roxa", D("'27", GS, 260, "preto")),
 ("'27 GS branco menor", D("'27", GS, 210, "branco")),
 ("'27 GS branco + subido", D("'27", GS, 240, "branco", ay=-60)),
 ("'27 GS branco no canto", D("'27", GS, 240, "branco", ax=0.9, ay=-40, rot=-12)),
 ("'27 GS branco à esquerda", D("'27", GS, 240, "branco", ax=0.15, ay=-30, rot=-10)),
 ("'27 GS branco reto", D("'27", GS, 250, "branco", rot=0)),
 ("'27 GS branco bem torto", D("'27", GS, 250, "branco", rot=-14)),
 ("'27 King Jack branco", D("'27", KJ, 250, "branco")),
 ("'27 King Jack meio", D("'27", KJ, 250, "meio")),
 ("'27 Beat Mark branco", D("'27", BM, 260, "branco")),
 ("'27 Beat Mark lilás", D("'27", BM, 260, "lilas")),
 ("'27 Urban Gear branco", D("'27", UG, 250, "branco")),
 ("'27 Urban Blocker branco", D("'27", UB, 260, "branco")),
 ("'27 Bostero branco", D("'27", BO, 280, "branco")),
 ("'27 Street Shade branco", D("'27", SS, 270, "branco")),
 ("2027 GS branco", D("2027", GS, 200, "branco")),
 ("2027 GS meio", D("2027", GS, 200, "meio")),
 ("2027 GS lilás", D("2027", GS, 200, "lilas")),
 ("2027 GS branco centro", D("2027", GS, 190, "branco", ax=0.5)),
 ("2027 GS branco canto", D("2027", GS, 180, "branco", ax=0.82, ay=-50, rot=-12)),
 ("2027 Beat Mark branco", D("2027", BM, 200, "branco")),
 ("2027 Beat Mark meio", D("2027", BM, 200, "meio")),
 ("2027 Urban Gear branco", D("2027", UG, 200, "branco")),
 ("2027 Urban Blocker lilás", D("2027", UB, 210, "lilas")),
 ("2027 Bostero branco", D("2027", BO, 230, "branco")),
 ("27 sem apóstrofo GS", D("27", GS, 280, "branco")),
 ("27 sem apóstrofo meio", D("27", GS, 280, "meio")),
]
ims = []
for i, (desc, (f, v)) in enumerate(V, 1):
    costas.ANO_FONTE, costas.ANO_INT = f, v
    h = P / f"_{i}.html"; h.write_text(costas.html(GY, True, True))
    png = P / f"{i:02d}.png"; costas.render(h, png); h.unlink(); ims.append((i, desc, png))
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
fts = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
c = Image.new("RGB", (6 * 330, 5 * 440), "#0A0A0C")
for k, (i, desc, p) in enumerate(ims):
    im = Image.open(p).convert("RGB").crop((150, 700, 1350, 1800)).resize((330, 400))
    ImageDraw.Draw(im).text((8, 4), f"{i:02d}", font=ft, fill="#FFD84D")
    c.paste(im, ((k % 6) * 330, (k // 6) * 440))
    ImageDraw.Draw(c).text(((k % 6) * 330 + 6, (k // 6) * 440 + 408), desc, font=fts, fill="#BBB")
c.save(P / "todas.jpg", quality=86)
