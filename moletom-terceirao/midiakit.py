"""Media kit em PDF: capa, arte principal, variações do 2027, versões em negativo, paleta e fontes.

uso: python3 midiakit.py -> midiakit/terceirao-2027-midia-kit.pdf (+ PNGs transparentes e negativos em midiakit/)
Arte principal = 'emendado 25' (costas/ano-favoritos/integrado-25.png).
Negativo = pra fundo claro: tons neutros invertidos (branco<->preto), roxos mantidos.
"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

AQUI = Path(__file__).parent
FAV = AQUI / "costas/ano-favoritos"
OUT = AQUI / "midiakit"; (OUT / "png").mkdir(parents=True, exist_ok=True)
FUNDO = np.array([10, 10, 12])

VARS = [("integrado-25", "Principal · 27 emendado (Grime Slime, branco)"),
        ("ano30-01", "27 branco"), ("ano30-03", "27 lilás claro"), ("ano30-07", "27 no canto"),
        ("ano30-11", "27 King Jack"), ("ano30-19", "2027 branco"), ("ano30-22", "2027 branco centralizado"),
        ("ano30-23", "2027 branco no canto"), ("ano30-30", "27 meio branco / meio roxo")]


def recorta_fundo(im):
    """tira o fundo preto (vira transparente) pra estampa"""
    a = np.asarray(im.convert("RGB")).astype(int)
    dist = np.abs(a - FUNDO).sum(-1)
    alpha = np.clip((dist - 18) * 8, 0, 255).astype(np.uint8)   # o preto do contorno é #0A0A0C: só some se encostar no fundo
    return a, alpha


def negativo(im):
    """inverte só os neutros (branco<->preto) e deixa os roxos; fundo vira branco"""
    a = np.asarray(im.convert("RGB")).astype(float)
    mx, mn = a.max(-1), a.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1)
    inv = 255 - a
    w = np.clip((0.22 - sat) / 0.12, 0, 1)[..., None]           # 1 = neutro (inverte), 0 = colorido (mantém)
    return Image.fromarray((inv * w + a * (1 - w)).clip(0, 255).astype(np.uint8))


paginas_img = []
for nome, _ in VARS:
    im = Image.open(FAV / f"{nome}.png").convert("RGB")
    im.save(OUT / "png" / f"{nome}-fundo-preto.png")
    rgb, alpha = recorta_fundo(im)
    Image.open(FAV / f"{nome}-transparente.png").save(OUT / "png" / f"{nome}-transparente.png")  # renderizado sem fundo
    # negativo nativo (favoritos.py): fundo claro #F4F1F7 -> transparente
    ng = Image.open(FAV / f"{nome}-negativo.png").convert("RGB"); ng.save(OUT / "png" / f"{nome}-negativo.png")
    na = np.asarray(ng).astype(int); dn = np.abs(na - np.array([244, 241, 247])).sum(-1)
    an = np.clip((dn - 12) * 8, 0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([na, an]).astype(np.uint8), "RGBA").save(OUT / "png" / f"{nome}-negativo-transparente.png")

R = (OUT / "png").resolve().as_uri()
ROXO, CLARO, ESCURO, UVA = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353"
CSS = f"""
@page{{size:1600px 1000px;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Arial,Helvetica,sans-serif}}
.p{{width:1600px;height:1000px;page-break-after:always;position:relative;overflow:hidden;background:#0A0A0C;color:#fff;padding:70px 80px}}
.p.cl{{background:#F4F1F7;color:#0A0A0C}}
h1{{font-size:20px;letter-spacing:.35em;color:{ROXO};margin:0 0 30px;font-weight:700}}
h2{{font-size:64px;margin:0;font-weight:900;letter-spacing:-.02em}}
.rod{{position:absolute;left:80px;bottom:40px;font-size:15px;letter-spacing:.25em;color:#6d6478}}
.cl .rod{{color:#8a8295}}
.grid{{display:grid;gap:22px}} .grid figure{{margin:0;text-align:center}} .grid img{{width:100%;max-height:390px;object-fit:contain;display:block;border-radius:14px}}
figcaption{{font-size:15px;margin-top:10px;color:#b9b0c4;letter-spacing:.05em}} .cl figcaption{{color:#5d5566}}
.sw{{display:flex;gap:20px;margin-top:20px}} .sw div{{flex:1}} .sw i{{display:block;height:150px;border-radius:16px;border:2px solid #2a2530}}
.sw b{{display:block;margin-top:12px;font-size:20px}} .sw span{{font-family:monospace;font-size:18px;color:#aaa}}
"""
def fig(src, cap): return f'<figure><img src="{R}/{src}"><figcaption>{cap}</figcaption></figure>'

capa = f"""<div class=p style="display:flex;align-items:center;gap:80px">
<img src="{R}/integrado-25-transparente.png" style="height:880px">
<div><h1>MÍDIA KIT · IDENTIDADE VISUAL</h1><h2>TERCEIRÃO<br>2027</h2>
<p style="font-size:26px;color:{ROXO};letter-spacing:.3em;margin-top:30px">MÃE DE DEUS</p>
<p style="font-size:18px;color:#8d7f99;max-width:520px;line-height:1.6;margin-top:50px">Arte das costas do moletom (preto), variações do ano,
versões em negativo para fundo claro, paleta e tipografia.</p></div>
<div class=rod>01 · CAPA</div></div>"""

principal = f"""<div class=p style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center">
<div><h1>ARTE PRINCIPAL</h1><h2 style="font-size:46px">Costas do moletom</h2>
<p style="font-size:19px;color:#b9b0c4;line-height:1.7;margin-top:30px">TER / CEI / RÃO no mesmo plano (um adesivo só), fonte Graffiti Youth,
recheio em degradê roxo, contorno preto, linha branca e sombra 3D uva. Til desenhado à mão.
Ano 27 emendado no RÃO (sem apóstrofo).</p>
<p style="font-size:16px;color:#8d7f99;margin-top:30px">Arquivos: png/integrado-25-transparente.png (estampa) · -fundo-preto · -negativo</p></div>
<img src="{R}/integrado-25-transparente.png" style="height:860px;justify-self:center">
<div class=rod>02 · ARTE PRINCIPAL</div></div>"""

def pagina_vars(titulo, suf, claro, n):
    figs = "".join(fig(f"{nm}-{suf}.png", f"{i:02d} · {cap}") for i, (nm, cap) in enumerate(VARS[1:], 1))
    return (f'<div class="p{" cl" if claro else ""}"><h1>{titulo}</h1>'
            f'<div class=grid style="grid-template-columns:repeat(4,1fr);width:1080px;margin:0 auto">{figs}</div><div class=rod>{n}</div></div>')

def pagina_lado(titulo, n):
    figs = "".join(f'<figure><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">'
                   f'<img src="{R}/{nm}-fundo-preto.png" style="max-height:330px"><img src="{R}/{nm}-negativo.png" style="max-height:330px"></div><figcaption>{cap}</figcaption></figure>'
                   for nm, cap in VARS[1:9:2])
    return f'<div class=p><h1>{titulo}</h1><div class=grid style="grid-template-columns:repeat(2,1fr);width:1000px;margin:0 auto">{figs}</div><div class=rod>{n}</div></div>'

negativo_principal = f"""<div class="p cl" style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center">
<div><h1>VERSÃO EM NEGATIVO</h1><h2 style="font-size:46px">Pra fundo claro</h2>
<p style="font-size:19px;color:#5d5566;line-height:1.7;margin-top:30px">Contorno de fora preto, brilho branco e roxos iguais; estrelas pretas.
Use em camiseta branca, convite, papel e posts com fundo claro.</p></div>
<img src="{R}/integrado-25-negativo-transparente.png" style="height:860px;justify-self:center">
<div class=rod>05 · NEGATIVO</div></div>"""

paleta = f"""<div class=p><h1>CORES E FONTES</h1>
<div class=sw>{''.join(f'<div><i style="background:{c}"></i><b>{n}</b><span>{c}</span></div>' for n, c in
 [("Roxo turma", ROXO), ("Lilás claro", CLARO), ("Roxo escuro", ESCURO), ("Uva (sombra)", UVA), ("Branco", "#FFFFFF"), ("Preto", "#0A0A0C")])}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:70px;font-size:20px;line-height:1.8;color:#b9b0c4">
<div><b style="color:#fff;font-size:26px">Graffiti Youth</b><br>TERCEIRÃO (letras principais)<br>
<b style="color:#fff;font-size:26px">Grime Slime / King Jack Style</b><br>ano (27 / 2027)</div>
<div><b style="color:#fff;font-size:26px">Arial Bold</b><br>MÃE DE DEUS (espaçado)<br>
<span style="color:#8d7f99">Fontes do dafont: grátis pra uso pessoal; pra vender o moletom, comprar a licença comercial com o autor.</span></div></div>
<div class=rod>07 · CORES E FONTES</div></div>"""

html = (f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>"
        + capa + principal
        + pagina_vars("VARIAÇÕES DO ANO · MOLETOM PRETO", "fundo-preto", False, "03 · VARIAÇÕES")
        + pagina_lado("PRETO × NEGATIVO", "04 · COMPARAÇÃO")
        + negativo_principal
        + pagina_vars("VARIAÇÕES DO ANO · NEGATIVO", "negativo", True, "06 · VARIAÇÕES NEGATIVO")
        + paleta + "</body></html>")
h = OUT / "_kit.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.waitForTimeout(800);"
      "await p.pdf({path:process.argv[2],width:'1600px',height:'1000px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(OUT / "terceirao-2027-midia-kit.pdf")], check=True)
h.unlink(); print("ok")
