"""30 opções de til (RÃO pos. 12, espaço 2): costas/tils/"""
import math, costas
from PIL import Image, ImageDraw, ImageFont
P = costas.OUT / "tils"; P.mkdir(exist_ok=True)

def faixa(amp=45, grossa=50, ondas=1.0, ponta="redonda", forma="curva", larg=300, incl=0):
    """til como faixa preenchida ao longo de uma onda (unidades ~300 de largura)"""
    n = 40; top = []; bot = []
    for i in range(n + 1):
        u = i / n; x = -larg / 2 + larg * u
        if forma == "zigue":
            f = (u * 2 * ondas) % 2; y = -amp * (1 - 2 * abs(f - 1)) if True else 0
            y = amp * (2 * abs(((u * 2 * ondas) % 2) - 1) - 1)
        elif forma == "bolha":
            y = -amp * math.sin(u * 2 * math.pi * ondas) * (1 - 0.3 * abs(u - .5))
        else:
            y = -amp * math.sin(u * 2 * math.pi * ondas)
        y += incl * (u - .5)
        t = grossa / 2
        if ponta == "fina": t *= 0.25 + 0.75 * math.sin(math.pi * u)
        elif ponta == "seta": t *= 0.35 + 0.65 * u
        elif ponta == "gota": t *= 0.45 + 0.55 * (1 - u) + 0.25 * math.sin(math.pi * u)
        top.append((x, y - t)); bot.append((x, y + t))
    pts = top + bot[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"

G = "url(#gt)"; B = "#FFFFFF"
V = [  # (amp, grossa, ondas, ponta, forma, larg, incl, giro, junta, recheio)
 (45,55,1,"redonda","curva",300,0,-6,"round",G), (35,60,1,"redonda","curva",300,0,0,"round",G), (60,50,1,"redonda","curva",300,0,-8,"round",G),
 (45,75,1,"redonda","curva",300,0,-5,"round",G), (40,40,1,"redonda","curva",320,0,-6,"round",G), (45,55,1,"fina","curva",320,0,-6,"round",G),
 (55,70,1,"fina","curva",340,0,-4,"round",G), (45,60,1,"seta","curva",320,0,-6,"round",G), (45,65,1,"gota","curva",300,0,-6,"round",G),
 (40,55,1,"redonda","zigue",300,0,-6,"miter",G), (55,50,1,"redonda","zigue",300,0,0,"miter",G), (35,65,1,"fina","zigue",330,0,-6,"miter",G),
 (45,60,1,"redonda","bolha",300,0,-6,"round",G), (60,70,1,"redonda","bolha",300,0,-3,"round",G), (40,55,1.5,"redonda","curva",340,0,-6,"round",G),
 (30,50,1.5,"fina","curva",360,0,-4,"round",G), (45,55,1,"redonda","curva",300,-60,-6,"round",G), (45,55,1,"redonda","curva",300,60,-6,"round",G),
 (45,55,1,"redonda","curva",300,0,-15,"round",G), (45,55,1,"redonda","curva",300,0,10,"round",G), (45,55,1,"redonda","curva",300,0,-6,"round",B),
 (35,60,1,"redonda","curva",300,0,0,"round",B), (55,70,1,"fina","curva",340,0,-4,"round",B), (40,55,1,"redonda","zigue",300,0,-6,"miter",B),
 (60,70,1,"redonda","bolha",300,0,-3,"round",B), (50,85,1,"redonda","curva",280,0,-6,"round",G), (25,55,1,"redonda","curva",340,0,-3,"round",G),
 (45,45,1,"seta","zigue",340,0,-6,"miter",G), (50,60,1,"gota","bolha",300,0,-8,"round",G), (40,50,2,"fina","curva",380,0,-4,"round",G),
]
if __name__ == "__main__":
    ims = []
    for i, (a, g, o, pt, fo, lg, inc, rot, j, fill) in enumerate(V, 1):
        costas.TIL_D = faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
        h = P / f"_{i}.html"; h.write_text(costas.html("graffiti_youth.otf", True, True))
        png = P / f"{i:02d}.png"; costas.render(h, png); h.unlink(); ims.append(png)
    ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    c = Image.new("RGB", (6 * 400, 5 * 400), "#0A0A0C")
    for k, p in enumerate(ims):   # recorte no miolo (CEI / til / RÃO) pra ver o til grande
        im = Image.open(p).convert("RGB").crop((250, 450, 1250, 1450)).resize((400, 400))
        ImageDraw.Draw(im).text((10, 6), f"{k+1:02d}", font=ft, fill="#FFD84D")
        c.paste(im, ((k % 6) * 400, (k // 6) * 400))
    c.save(P / "todos.jpg", quality=85)
    