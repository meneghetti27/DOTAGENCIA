"""Aplicações da marca (versão final): final/aplicacoes/*.png
moletom preto (costas), camiseta branca (negativo), story do Instagram, adesivo recortado, faixa da turma, ingresso da formatura.
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
PNG = (AQUI / "midiakit/png").resolve().as_uri()
OUT = AQUI / "final/aplicacoes"; OUT.mkdir(parents=True, exist_ok=True)
FD = (AQUI / "fontes/dafont").resolve().as_uri()
ROXO, CLARO, UVA = "#996BB3", "#E4CFF7", "#3E2353"
ART, NEG = f"{PNG}/integrado-25-transparente.png", f"{PNG}/integrado-25-negativo-transparente.png"
BASE = f"""<style>@font-face{{font-family:G;src:url('{FD}/graffiti_youth.otf')}}
*{{box-sizing:border-box}} html,body{{margin:0;height:100%;overflow:hidden;font-family:Arial,Helvetica,sans-serif}}</style>"""

# silhueta de moletom (costas) / camiseta, em SVG
MOLETOM = """<svg viewBox="-520 -60 1040 1180" width="{w}" style="position:absolute;left:{x}px;top:{y}px;filter:drop-shadow(0 40px 50px rgba(0,0,0,.35))">
<defs><linearGradient id="vol" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset=".35" stop-color="#fff" stop-opacity=".06"/>
<stop offset=".65" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></linearGradient></defs>
<g fill="{cor}" stroke="#000" stroke-opacity=".25" stroke-width="3">
<path d="M-330 230 C-420 260 -470 470 -490 760 L-500 980 L-370 990 L-350 760 C-340 600 -320 520 -300 470Z"/>
<path d="M330 230 C420 260 470 470 490 760 L500 980 L370 990 L350 760 C340 600 320 520 300 470Z"/>
<path d="M-500 980 L-503 1050 L-368 1058 L-370 990Z"/><path d="M500 980 L503 1050 L368 1058 L370 990Z"/>
<path d="M-330 230 C-350 480 -350 820 -340 1000 L340 1000 C350 820 350 480 330 230 C240 195 130 180 0 180 C-130 180 -240 195 -330 230Z"/>
<path d="M-340 1000 L-336 1090 L336 1090 L340 1000Z"/>
<path d="M-215 200 C-235 40 -130 -40 0 -40 C130 -40 235 40 215 200 C150 260 -150 260 -215 200Z"/></g>
<path d="M0 -38 L0 235" stroke="#000" stroke-opacity=".3" stroke-width="3" stroke-dasharray="8 7"/>
<path d="M-330 230 C-350 480 -350 820 -340 1000 L340 1000 C350 820 350 480 330 230Z" fill="url(#vol)"/></svg>"""
CAMISETA = """<svg viewBox="-520 -40 1040 1140" width="{w}" style="position:absolute;left:{x}px;top:{y}px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.18))">
<path d="M-150 0 C-90 60 90 60 150 0 L360 80 L500 330 L360 420 L320 340 L320 1060 L-320 1060 L-320 340 L-360 420 L-500 330 L-360 80Z"
 fill="{cor}" stroke="#000" stroke-opacity=".12" stroke-width="3"/>
<path d="M-150 0 C-90 60 90 60 150 0" fill="none" stroke="#000" stroke-opacity=".15" stroke-width="10"/></svg>"""

PECAS = {
    "01-moletom-preto-costas": (1600, 1600, f"""<body style="background:radial-gradient(circle at 50% 40%,#ECE6F2,#C9C0D3)">
{MOLETOM.format(w=1100, x=250, y=120, cor="#141216")}
<img src="{ART}" style="position:absolute;left:545px;top:400px;width:510px">
<div style="position:absolute;left:60px;bottom:50px;font-size:22px;letter-spacing:.3em;color:#5d5566">MOLETOM PRETO · COSTAS</div></body>"""),
    "02-camiseta-branca": (1600, 1600, f"""<body style="background:radial-gradient(circle at 50% 40%,#3A2E44,#120E16)">
{CAMISETA.format(w=1150, x=225, y=160, cor="#F7F5F8")}
<img src="{NEG}" style="position:absolute;left:590px;top:420px;width:420px">
<div style="position:absolute;left:60px;bottom:50px;font-size:22px;letter-spacing:.3em;color:#a99fb3">CAMISETA BRANCA · VERSÃO NEGATIVO</div></body>"""),
    "03-story-instagram": (1080, 1920, f"""<body style="background:radial-gradient(ellipse 70% 50% at 50% 45%,#2A1838,#0A0A0C 75%)">
<div style="position:absolute;top:120px;width:100%;text-align:center;font-size:30px;letter-spacing:.5em;color:{ROXO};font-weight:700">CONTAGEM REGRESSIVA</div>
<img src="{ART}" style="position:absolute;left:140px;top:260px;width:800px">
<div style="position:absolute;bottom:200px;width:100%;text-align:center;font-family:G;font-size:150px;color:#fff;-webkit-text-stroke:24px #0A0A0C;paint-order:stroke fill;filter:drop-shadow(8px 9px 0 {ROXO})">FALTAM 200</div>
<div style="position:absolute;bottom:140px;width:100%;text-align:center;font-size:26px;letter-spacing:.4em;color:#bfb3cc">DIAS PRA FORMATURA</div></body>"""),
    "04-adesivo": (1400, 1400, f"""<body style="background:#E9E5EE">
<img src="{ART}" style="position:absolute;left:330px;top:120px;width:740px;transform:rotate(-8deg);
 filter:drop-shadow(0 0 0 #fff) drop-shadow(14px 0 0 #fff) drop-shadow(-14px 0 0 #fff) drop-shadow(0 14px 0 #fff) drop-shadow(0 -14px 0 #fff) drop-shadow(10px 22px 18px rgba(0,0,0,.35))">
<div style="position:absolute;left:60px;bottom:50px;font-size:22px;letter-spacing:.3em;color:#6d6478">ADESIVO RECORTADO</div></body>"""),
    "05-faixa-turma": (2400, 900, f"""<body style="background:#0A0A0C">
<div style="position:absolute;inset:40px;border-radius:30px;background:repeating-linear-gradient(-45deg,#120E16 0 40px,#17121c 40px 80px);border:6px solid {ROXO}"></div>
<img src="{ART}" style="position:absolute;left:120px;top:20px;height:860px">
<div style="position:absolute;left:1000px;top:250px;font-family:G;font-size:230px;line-height:.95;color:#fff;-webkit-text-stroke:30px #0A0A0C;paint-order:stroke fill;filter:drop-shadow(10px 12px 0 {ROXO})">FORMANDOS<br>2027</div>
<div style="position:absolute;left:1010px;top:740px;font-size:34px;letter-spacing:.5em;color:{ROXO};font-weight:700">COLÉGIO MÃE DE DEUS</div></body>"""),
    "06-ingresso-formatura": (1800, 800, f"""<body style="background:#D9D2E1">
<div style="position:absolute;left:100px;top:100px;width:1600px;height:600px;border-radius:30px;background:#0A0A0C;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.3)">
 <div style="position:absolute;right:360px;top:0;bottom:0;border-left:6px dashed #3a3240"></div>
 <img src="{ART}" style="position:absolute;left:40px;top:-10px;height:620px">
 <div style="position:absolute;left:560px;top:120px;font-size:24px;letter-spacing:.4em;color:{ROXO};font-weight:700">BAILE DE FORMATURA</div>
 <div style="position:absolute;left:560px;top:170px;font-family:G;font-size:120px;color:#fff;-webkit-text-stroke:18px #0A0A0C;paint-order:stroke fill;filter:drop-shadow(6px 7px 0 {ROXO})">TERCEIRÃO 2027</div>
 <div style="position:absolute;left:560px;top:360px;font-size:26px;line-height:1.7;color:#bfb3cc">DATA · LOCAL · HORÁRIO<br><b style="color:#fff">CONVIDADO(A):</b> ____________________</div>
 <div style="position:absolute;right:0;top:0;width:360px;height:100%;display:flex;align-items:center;justify-content:center;flex-direction:column;color:#fff">
  <div style="font-family:G;font-size:150px;color:{ROXO}">27</div><div style="font-size:22px;letter-spacing:.4em;color:#8d7f99">Nº 0001</div></div>
</div></body>"""),
}

if __name__ == "__main__":
    for nome, (w, h, corpo) in PECAS.items():
        f = OUT / f"_{nome}.html"; f.write_text(f"<!doctype html><html><head><meta charset=utf-8>{BASE}</head>{corpo}</html>")
        subprocess.run(["node", str(AQUI.parent / "tools/html-to-png-exato.js"), str(f), str(OUT / f"{nome}.png"), str(w), str(h), "1"], check=True)
        f.unlink(); print("ok", nome)
