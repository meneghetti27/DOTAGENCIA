"""40 estilos de 2027 (+ MÃE DE DEUS) sobre a mesma arte das costas: costas/ano40/
A arte base é renderizada sem o bloco do ano; cada variação é um HTML transparente colado embaixo do RÃO."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import costas, tils

P = costas.OUT / "ano40"; P.mkdir(exist_ok=True)
FD = costas.FD
ROXO, CLARO, ESCURO, UVA = costas.ROXO, costas.CLARO, costas.ESCURO, costas.UVA

# arte base sem ano / sem MÃE DE DEUS (til 26 a 85%)
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85
base_html = costas.html("graffiti_youth.otf", True, True).replace(
    "</style>", ".ano,.esc{visibility:hidden!important}</style>")
hb = P / "_base.html"; hb.write_text(base_html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:1800}});"
      "await p.goto('file://'+process.argv[1]);await p.waitForFunction(()=>document.body.dataset.layout);await p.waitForTimeout(400);"
      "await p.screenshot({path:process.argv[2]});console.log(await p.evaluate(()=>document.body.dataset.layout));await b.close();})()")
r = subprocess.run(["node", "-e", js, str(hb.resolve()), str(P / "_base.png")], capture_output=True, text=True, check=True)
hb.unlink()
L = json.loads(r.stdout)
fim = L["ano"]["y"] - 10          # onde o ano começava (logo abaixo do RÃO)

CAM = f"""
.w{{position:absolute;left:0;top:0;width:1500px;height:520px;display:flex;align-items:center;justify-content:center;flex-direction:column}}
.t{{position:relative;line-height:1;white-space:nowrap}}
.t span{{position:absolute;left:-.5em;top:0;padding:0 .5em;white-space:nowrap}}
.f{{visibility:hidden;position:static!important;padding:0!important}}
.o1{{-webkit-text-stroke:.15em #fff;color:#fff;filter:drop-shadow(.025em .03em 0 {UVA}) drop-shadow(.02em .025em 0 #000)}}
.o2{{-webkit-text-stroke:.075em #0A0A0C;color:#0A0A0C}}
.cb{{color:#fff}} .cr{{background:linear-gradient(180deg,{CLARO},{ROXO} 50%,{ESCURO});-webkit-background-clip:text;background-clip:text;color:transparent}}
.cs{{color:#fff;filter:drop-shadow(.04em .05em 0 {ROXO})}}
.vz{{color:transparent;-webkit-text-stroke:.05em #fff}}
.esc{{font:700 34px/1 Arial,sans-serif;letter-spacing:.45em;color:{ROXO};margin-top:22px;padding-left:.45em}}
.esc.b{{color:#fff}}
.fx{{padding:14px 70px 18px;background:{ROXO};border:10px solid #0A0A0C;box-shadow:0 0 0 9px #fff, 12px 14px 0 9px {UVA};border-radius:16px}}
.fxp{{padding:10px 60px 14px;background:#0A0A0C;border:8px solid #fff;border-radius:999px;box-shadow:10px 12px 0 0 {ROXO}}}
.lin{{display:flex;align-items:center;gap:30px}} .lin i{{display:block;width:150px;height:12px;background:#fff;border-radius:6px;box-shadow:5px 6px 0 {ROXO}}}
"""

def txt(t, fonte, tam, cor="cb", contorno=True):
    lay = (["o1", "o2"] if contorno else []) + [cor]
    return (f'<div class=t style="font-family:\'{fonte}\';font-size:{tam}px"><span class=f>{t}</span>'
            + "".join(f'<span class={c}>{t}</span>' for c in lay) + "</div>")

def pagina(corpo, giro=-5, dx=0, esc=True, escb=False):
    fontes = "".join(f"@font-face{{font-family:'{n}';src:url('{FD}/{n}')}}" for n in FONTES_USADAS)
    e = f'<div class="esc{" b" if escb else ""}">MÃE DE DEUS</div>' if esc else ""
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{fontes}html,body{{margin:0;width:1500px;height:520px;background:transparent}}{CAM}"
            f"</style></head><body><div class=w style='transform:translate({dx}px,0) rotate({giro}deg)'>{corpo}{e}</div></body></html>")

GY, BM, KJ, GS, UG, UH, DS, UB, SS, TG, EL, GF, BO = ("graffiti_youth.otf", "beat_mark.ttf", "king_jack_style.ttf", "grime_slime.ttf",
    "urban_gear.ttf", "urban_heroes.ttf", "drop_shade.ttf", "urban_blocker.ttf", "street_shade.ttf", "tagdo.ttf", "endlove.otf",
    "the_graffiti_font.ttf", "bostero.ttf")
FONTES_USADAS = [GY, BM, KJ, GS, UG, UH, DS, UB, SS, TG, EL, GF, BO]

V = [  # (descrição, corpo html, giro, dx, esc_branco)
 ("branco contorno · Grime Slime", txt("2027", GS, 210), -5, 0, False),
 ("branco contorno · King Jack", txt("2027", KJ, 200), -5, 0, False),
 ("branco contorno · Urban Gear", txt("2027", UG, 210), -5, 0, False),
 ("branco contorno · Beat Mark", txt("2027", BM, 220), -5, 0, False),
 ("roxo contorno · Grime Slime", txt("2027", GS, 210, "cr"), -5, 0, False),
 ("roxo contorno · King Jack", txt("2027", KJ, 200, "cr"), -5, 0, False),
 ("branco GRANDE · King Jack", txt("2027", KJ, 290), -5, 0, False),
 ("branco GRANDE · Grime Slime", txt("2027", GS, 300), -5, 0, False),
 ("branco pequeno · Grime Slime", txt("2027", GS, 140), -5, 0, False),
 ("branco pequeno · King Jack", txt("2027", KJ, 130), -5, 0, False),
 ("faixa roxa · King Jack", f'<div class=fx>{txt("2027", KJ, 150, "cb", False)}</div>', -5, 0, False),
 ("faixa roxa · Grime Slime", f'<div class=fx>{txt("2027", GS, 160, "cb", False)}</div>', -5, 0, False),
 ("faixa roxa · Urban Gear", f'<div class=fx>{txt("2027", UG, 160, "cb", False)}</div>', -3, 0, False),
 ("pílula preta · King Jack", f'<div class=fxp>{txt("2027", KJ, 140, "cb", False)}</div>', -5, 0, False),
 ("pílula preta · Grime Slime", f'<div class=fxp>{txt("2027", GS, 150, "cb", False)}</div>', -5, 0, False),
 ("tag spray · Tagdo", txt("2027", TG, 230, "cs", False), -8, 0, False),
 ("tag spray · Endlove", txt("2027", EL, 220, "cs", False), -8, 0, False),
 ("tag spray grande · Tagdo", txt("2027", TG, 320, "cs", False), -10, 0, False),
 ("tag com contorno · Tagdo", txt("2027", TG, 230), -8, 0, False),
 ("vazado branco · King Jack", txt("2027", KJ, 220, "vz", False), -5, 0, False),
 ("vazado branco · Grime Slime", txt("2027", GS, 230, "vz", False), -5, 0, False),
 ("linhas laterais · King Jack", f'<div class=lin><i></i>{txt("2027", KJ, 150)}<i></i></div>', -5, 0, False),
 ("linhas laterais · Grime Slime", f'<div class=lin><i></i>{txt("2027", GS, 160)}<i></i></div>', -5, 0, False),
 ("à direita · King Jack", txt("2027", KJ, 200), -5, 260, False),
 ("à direita · Grime Slime", txt("2027", GS, 210), -5, 260, False),
 ("à esquerda · King Jack", txt("2027", KJ, 200), -5, -230, False),
 ("bem inclinado · King Jack", txt("2027", KJ, 210), -12, 0, False),
 ("reto · Grime Slime", txt("2027", GS, 210), 0, 0, False),
 ("reto · Urban Gear", txt("2027", UG, 210), 0, 0, False),
 ("'27 grande · King Jack", txt("'27", KJ, 300), -5, 0, False),
 ("'27 grande roxo · King Jack", txt("'27", KJ, 300, "cr"), -5, 0, False),
 ("'27 faixa · Grime Slime", f'<div class=fx>{txt("’27", GS, 170, "cb", False)}</div>', -5, 0, False),
 ("CLASS OF 2027 · Grime Slime", txt("CLASS OF 2027", GS, 110), -5, 0, False),
 ("TURMA 2027 · King Jack", txt("TURMA 2027", KJ, 110), -5, 0, False),
 ("2027 + MÃE DE DEUS branco", txt("2027", KJ, 200), -5, 0, True),
 ("escorrido · Drop Shade", txt("2027", DS, 200), -5, 0, False),
 ("pingos · Urban Heroes", txt("2027", UH, 210), -5, 0, False),
 ("bolha · Urban Blocker", txt("2027", UB, 210), -5, 0, False),
 ("condensado · Bostero", txt("2027", BO, 220), -5, 0, False),
 ("old school · The Graffiti Font", txt("2027", GF, 210), -5, 0, False),
]

base = Image.open(P / "_base.png").convert("RGBA")
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
fts = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
pngs = []
for i, (desc, corpo, giro, dx, escb) in enumerate(V, 1):
    h = P / f"_{i}.html"; h.write_text(pagina(corpo, giro, dx, True, escb))
    tmp = P / f"_{i}.png"
    subprocess.run(["node", str(costas.AQUI.parent / "tools/html-to-png-exato.js"), str(h), str(tmp), "1500", "520", "1", "t"], check=True)
    h.unlink()
    im = base.copy(); bloco = Image.open(tmp).convert("RGBA"); tmp.unlink()
    bb = bloco.getbbox(); top = bb[1] if bb else 0
    im.alpha_composite(bloco, (0, int(fim - top)))
    out = P / f"{i:02d}.png"; im.convert("RGB").save(out); pngs.append((i, desc, out))
    print("ok", i)
(P / "_base.png").unlink()

c = Image.new("RGB", (8 * 300, 5 * 400), "#0A0A0C")
for k, (i, desc, p) in enumerate(pngs):
    im = Image.open(p).resize((300, 360)); d = ImageDraw.Draw(im)
    d.text((8, 4), f"{i:02d}", font=ft, fill="#FFD84D")
    t = Image.new("RGB", (300, 40), "#0A0A0C"); ImageDraw.Draw(t).text((6, 8), desc[:30], font=fts, fill="#BBBBBB")
    c.paste(im, ((k % 8) * 300, (k // 8) * 400)); c.paste(t, ((k % 8) * 300, (k // 8) * 400 + 360))
c.save(P / "todas.jpg", quality=86)
# zoom no ano
z = Image.new("RGB", (5 * 480, 8 * 230), "#0A0A0C")
for k, (i, desc, p) in enumerate(pngs):
    im = Image.open(p).crop((150, int(fim) - 80, 1350, int(fim) + 470)).resize((480, 220)); d = ImageDraw.Draw(im)
    d.text((8, 4), f"{i:02d}", font=ft, fill="#FFD84D")
    z.paste(im, ((k % 5) * 480, (k // 5) * 230))
z.save(P / "zoom.jpg", quality=86)
