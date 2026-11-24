"""Mockup vetorial do moletom (frente + costas) com as artes aplicadas.

uso: python3 mockup.py [lima rosa branco]  -> artes/<cor>/mockup.png
"""
import sys, subprocess
from pathlib import Path

AQUI = Path(__file__).parent
ROXO = "#996BB3"
SOMBRA = "#6E4687"
LUZ = "#B48ACB"


def corpo(x, costas=False):
    """silhueta do moletom oversized centrada em x (canvas 1000 de largura por peça)"""
    g = f'<g transform="translate({x} 0)">'
    # mangas
    for s in (-1, 1):
        g += (f'<path d="M{s*300} 300 C{s*390} 330 {s*430} 520 {s*445} 760 L{s*450} 950 '
              f'L{s*340} 960 L{s*330} 760 C{s*320} 600 {s*300} 520 {s*270} 470Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
        # punho
        g += (f'<path d="M{s*450} 950 L{s*452} 1010 L{s*338} 1018 L{s*340} 960Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
        for k in range(1, 8):
            xx = s * (340 + k * 14)
            g += f'<line x1="{xx}" y1="{960+2}" x2="{xx+s*1}" y2="{1015}" stroke="{SOMBRA}" stroke-width="1.5" opacity=".6"/>'
    # tronco
    g += (f'<path d="M-300 300 C-320 500 -320 800 -310 960 L310 960 C320 800 320 500 300 300 '
          f'C220 270 120 255 0 255 C-120 255 -220 270 -300 300Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
    # barra
    g += f'<path d="M-310 960 L-306 1040 L306 1040 L310 960Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>'
    for k in range(-21, 22):
        g += f'<line x1="{k*14}" y1="963" x2="{k*14}" y2="1037" stroke="{SOMBRA}" stroke-width="1.5" opacity=".55"/>'
    # costuras do ombro caído
    g += f'<path d="M-300 300 C-290 380 -285 430 -270 470" fill="none" stroke="{SOMBRA}" stroke-width="2.5" stroke-dasharray="6 5"/>'
    g += f'<path d="M300 300 C290 380 285 430 270 470" fill="none" stroke="{SOMBRA}" stroke-width="2.5" stroke-dasharray="6 5"/>'
    if costas:
        # capuz caído nas costas
        g += (f'<path d="M-190 270 C-210 120 -120 40 0 40 C120 40 210 120 190 270 C130 330 -130 330 -190 270Z" '
              f'fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
        g += f'<path d="M0 45 L0 300" stroke="{SOMBRA}" stroke-width="2.5" stroke-dasharray="6 5"/>'
    else:
        # capuz aberto com forro estampado
        g += (f'<path d="M-200 300 C-230 120 -130 30 0 30 C130 30 230 120 200 300 C150 330 60 340 0 350 '
              f'C-60 340 -150 330 -200 300Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
        g += (f'<clipPath id="forro{x}"><path d="M-150 300 C-170 150 -100 75 0 75 C100 75 170 150 150 300 '
              f'C100 330 40 345 0 350 C-40 345 -100 330 -150 300Z"/></clipPath>')
        g += f'<g clip-path="url(#forro{x})"><rect x="-200" y="40" width="400" height="330" fill="{ROXO}"/>' \
             f'<image href="FORRO" x="-260" y="60" width="520" height="347" opacity="1"/>' \
             f'<path d="M-150 300 C-170 150 -100 75 0 75 C100 75 170 150 150 300" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="40"/></g>'
        # gola V cruzada
        g += f'<path d="M-150 300 C-60 340 -20 380 0 420 C20 380 60 340 150 300" fill="none" stroke="{SOMBRA}" stroke-width="3"/>'
        # cordões
        for s in (-1, 1):
            g += f'<path d="M{s*40} 380 C{s*44} 470 {s*38} 520 {s*42} 560" fill="none" stroke="{LUZ}" stroke-width="9" stroke-linecap="round"/>'
        # bolso canguru
        g += (f'<path d="M-170 720 L-120 620 L120 620 L170 720 L170 900 L-170 900Z" fill="{ROXO}" stroke="{SOMBRA}" stroke-width="3"/>')
    # luz e sombra suaves
    g += (f'<path d="M-300 300 C-320 500 -320 800 -310 960 L310 960 C320 800 320 500 300 300Z" fill="url(#vol)" opacity=".5"/>')
    return g + "</g>"


def mockup(cor):
    d = AQUI / "artes" / cor
    W, H = 2100, 1180
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="vol" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/>
<stop offset=".3" stop-color="#fff" stop-opacity=".12"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/>
<stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="#ECEAF0"/>
<g transform="translate(0 60)">
{corpo(530).replace("FORRO", "forro-capuz.png")}
{corpo(1570, costas=True)}
<!-- frente: peito esquerdo (direita de quem olha) -->
<image href="peito.png" x="{530+95}" y="390" width="150" height="156"/>
<!-- costas -->
<image href="costas.png" x="{1570-215}" y="330" width="430" height="473"/>
<!-- manga esquerda (na foto de costas fica à esquerda) -->
<image href="manga.png" transform="translate({1570-392} 560) rotate(4)" x="-26" y="0" width="56" height="192"/>
</g>
<text x="530" y="1150" text-anchor="middle" font-family="sans-serif" font-size="26" fill="#6b6475" letter-spacing="6">FRENTE</text>
<text x="1570" y="1150" text-anchor="middle" font-family="sans-serif" font-size="26" fill="#6b6475" letter-spacing="6">COSTAS</text>
</svg>'''
    (d / "mockup.svg").write_text(svg)
    html = d / "_mockup.html"
    html.write_text('<!doctype html><body style="margin:0">' + svg)
    subprocess.run(["node", str(AQUI.parent / "tools/html-to-png.js"), str(html), str(d / "mockup.png"),
                    str(W), str(H), "1"], check=True)
    html.unlink()
    print("ok", d / "mockup.png")


if __name__ == "__main__":
    for c in sys.argv[1:] or ["lima", "rosa", "branco"]:
        mockup(c)
