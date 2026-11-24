"""Gera as artes do moletom do terceirão (vetor SVG + PNG 300 dpi).

uso: python3 gerar.py            -> gera todas as artes em artes/
As letras saem dos glifos das fontes (fontes/*.ttf) convertidos em caminhos vetoriais,
cada letra com giro/tamanho/posição próprios e sobreposta à anterior (cara de grafite).
"""
import json, math, random, subprocess, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

AQUI = Path(__file__).parent
FONTES = AQUI / "fontes"
SAIDA = AQUI / "artes"
SAIDA.mkdir(exist_ok=True)

# ---------- paleta (3 cores de serigrafia + cor do moletom) ----------
ROXO = "#996BB3"      # cor do moletom (amostra da cor enviada)
BRANCO = "#FFFFFF"
PRETO = "#140B1C"     # preto levemente roxo
ACENTO = "#C8FF3D"    # verde-limão (contraste máximo com o lilás)

_cache = {}
def fonte(nome):
    if nome not in _cache:
        t = TTFont(FONTES / f"{nome}.ttf")
        _cache[nome] = (t, t.getGlyphSet(), t.getBestCmap())
    return _cache[nome]

def glifo(nome, ch):
    """caminho SVG do caractere (eixo y para baixo, origem na linha de base) + caixa"""
    t, gs, cmap = fonte(nome)
    g = gs[cmap[ord(ch)]]
    pen = SVGPathPen(gs); g.draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
    bp = BoundsPen(gs); g.draw(bp)
    x0, y0, x1, y1 = bp.bounds or (0, 0, 0, 0)
    return pen.getCommands(), (x0, -y1, x1, -y0), g.width

def letra(nome, ch, cx, cy, altura, rot=0, sx=1.0, skew=0):
    """devolve (d, transform) com a letra centrada em (cx, cy) e altura de caixa `altura`"""
    d, (x0, y0, x1, y1), w = glifo(nome, ch)
    s = altura / (y1 - y0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    tr = (f"translate({cx:.1f} {cy:.1f}) rotate({rot}) skewX({skew}) "
          f"scale({s*sx:.4f} {s:.4f}) translate({-mx:.1f} {-my:.1f})")
    return d, tr, s

def estrela(cx, cy, r, cor, giro=0):
    """brilho de 4 pontas"""
    k = r * 0.22
    pts = []
    for i in range(8):
        a = math.radians(giro + i * 45)
        rr = r if i % 2 == 0 else k
        pts.append(f"{cx + rr*math.sin(a):.1f},{cy - rr*math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{cor}"/>'


def arte_costas(v):
    """arte grande das costas: TER / CEI / RÃO em grafite empilhado"""
    J = v.get("join", "round")
    W, H = v.get("tamanho", (3000, 3300))
    F = v["fonte"]
    L = v["letras"]
    out = []
    defs = []
    ext = v.get("extrusao", (34, 44))
    contorno = v.get("contorno", 26)
    halo = v.get("halo", 70)
    peças = []
    for i, (ch, cx, cy, alt, rot) in enumerate(L):
        ch = ch.replace('Ã', 'A')
        d, tr, s = letra(F, ch, cx, cy, alt, rot, v.get("sx", 1.0), v.get("skew", 0))
        peças.append((i, ch, d, tr, s))

    # 1) silhueta geral: linha externa (acento) + massa preta (inclui extrusão)
    massa = []
    for i, ch, d, tr, s in peças:
        for k in range(0, 11):
            dx, dy = ext[0] * k / 10, ext[1] * k / 10
            massa.append(f'<path d="{d}" transform="translate({dx:.1f} {dy:.1f}) {tr}" '
                         f'stroke-width="{{SW}}" vector-effect="non-scaling-stroke"/>')
    m = "\n".join(massa)
    out.append(f'<g fill="{v["halo_cor"]}" stroke="{v["halo_cor"]}" stroke-linejoin="{J}">'
               + m.replace("{SW}", str(contorno * 2 + halo)) + "</g>")
    out.append(f'<g fill="{PRETO}" stroke="{PRETO}" stroke-linejoin="{J}">'
               + m.replace("{SW}", str(contorno * 2 + halo - 22)) + "</g>")

    # 2) letra por letra: extrusão, contorno, preenchimento com corte ondulado, brilhos
    for i, ch, d, tr, s in peças:
        cid = f"c{i}"
        defs.append(f'<clipPath id="{cid}"><path d="{d}" transform="{tr}"/></clipPath>')
        out += v.get("atras", {}).get(i, [])
        # extrusão 3D (cor escura)
        for k in range(1, 11):
            dx, dy = ext[0] * k / 10, ext[1] * k / 10
            out.append(f'<path d="{d}" transform="translate({dx:.1f} {dy:.1f}) {tr}" fill="{v["extrusao_cor"]}" '
                       f'stroke="{PRETO}" stroke-width="{contorno*2}" vector-effect="non-scaling-stroke" '
                       f'stroke-linejoin="{J}" paint-order="stroke"/>')
        # contorno + recheio
        pg = v.get("pingos", {}).get(i, [])
        out.append(f'<path d="{d}" transform="{tr}" fill="{PRETO}" stroke="{PRETO}" '
                   f'stroke-width="{contorno*2}" vector-effect="non-scaling-stroke" stroke-linejoin="{J}"/>')
        out += [a for a, b in pg]
        out.append(f'<path d="{d}" transform="{tr}" fill="{v["recheio"]}"/>')
        out += [b for a, b in pg]
        # faixa inferior ondulada no acento (dentro da letra)
        _, (x0, y0, x1, y1), _ = glifo(F, ch)
        out.append(f'<g clip-path="url(#{cid})">{v["faixa"](i, L[i])}</g>')
        out += v.get("frente", {}).get(i, [])
    # 3) enfeites por cima
    out += v["enfeites"]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<defs>{"".join(defs)}</defs>' + "\n".join(out) + "</svg>")
    return svg, W, H


def faixa_onda(y, amp, cor, x0=0, x1=3000, ondas=9, fase=0):
    pts = [f"M{x0} {y}"]
    n = 60
    for j in range(n + 1):
        x = x0 + (x1 - x0) * j / n
        yy = y + amp * math.sin(fase + j / n * ondas * math.pi * 2)
        pts.append(f"L{x:.0f} {yy:.0f}")
    pts.append(f"L{x1} 9999 L{x0} 9999Z")
    return f'<path d="{" ".join(pts)}" fill="{cor}"/>'


def salvar(nome, svg, W, H, png=True, fundo=None):
    p = SAIDA / f"{nome}.svg"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg)
    if png:
        html = p.parent / f"_{Path(nome).name}.html"
        bg = fundo or "transparent"
        html.write_text(f'<!doctype html><html><body style="margin:0;background:{bg}">'
                        f'<img src="{Path(nome).name}.svg" style="display:block;width:{W}px;height:{H}px"></body></html>')
        subprocess.run(["node", str(AQUI.parent / "tools/html-to-png.js"), str(html),
                        str(SAIDA / f"{nome}.png"), str(W), str(H), "1", "" if fundo else "t"], check=True)
        html.unlink()
    print("ok", p)


def montar_linhas(F, linhas, cx=1500, topo=420, alt=760, gap=-40, sobrep=0.10, jitter=None):
    """distribui as letras em linhas centralizadas; jitter = lista de (dx, dy, dalt, rot) por letra"""
    letras = []
    y = topo
    idx = 0
    for linha, escala in linhas:
        a = alt * escala
        larg = []
        for ch in linha:
            _, (x0, y0, x1, y1), _ = glifo(F, ch)
            # altura de referência = altura da caixa sem acento
            ref = glifo(F, ch.replace("Ã", "A"))[1]
            s = a / (ref[3] - ref[1])
            larg.append((x1 - x0) * s)
        total = sum(larg) - sobrep * sum(larg[1:])
        x = cx - total / 2
        for k, ch in enumerate(linha):
            j = jitter[idx] if jitter else (0, 0, 0, 0)
            ref = glifo(F, ch.replace("Ã", "A"))[1]
            _, (x0, y0, x1, y1), _ = glifo(F, ch)
            s = a / (ref[3] - ref[1])
            h = (y1 - y0) * s  # altura real (com acento)
            # base alinhada: centro vertical deslocado se tiver acento
            cy = y + a / 2 - (h - a) / 2
            letras.append((ch, x + larg[k] / 2 + j[0], cy + j[1], h * (1 + j[2]), j[3]))
            x += larg[k] * (1 - sobrep)
            idx += 1
        y += a + gap
    return letras


def til(cx, cy, larg, cor, giro=-6, esp=1.0):
    """til grafitado: onda gorda com contorno preto e sombra"""
    w, h = larg, larg * 0.22 * esp
    d = (f"M{-w*0.42} {h*0.35} C{-w*0.3} {-h*0.55} {-w*0.12} {-h*0.5} {0} {0} "
         f"C{w*0.12} {h*0.5} {w*0.3} {h*0.55} {w*0.42} {-h*0.35}")
    g = f'<g transform="translate({cx} {cy}) rotate({giro})">'
    g += f'<path d="{d}" transform="translate(16 22)" fill="none" stroke="{PRETO}" stroke-width="{h*0.9+48}" stroke-linecap="round"/>'
    g += f'<path d="{d}" fill="none" stroke="{PRETO}" stroke-width="{h*0.9+48}" stroke-linecap="round"/>'
    g += f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{h*0.9}" stroke-linecap="round"/>'
    return g + "</g>"


def pingo(x, y, comp, larg, cor):
    """escorrido de tinta saindo da base da letra"""
    r = larg / 2
    d = (f"M{x-r} {y-40} L{x-r} {y+comp} A{r} {r} 0 0 0 {x+r} {y+comp} L{x+r} {y-40}Z")
    bola = f'<circle cx="{x}" cy="{y+comp+r*1.9}" r="{r*0.75}"/>'
    return [f'<g fill="{PRETO}" stroke="{PRETO}" stroke-width="48" stroke-linejoin="round"><path d="{d}"/>{bola}</g>',
            f'<g fill="{cor}"><path d="{d}"/>{bola}</g>']


def recheio_grafite(acento, branco=BRANCO):
    def f(i, l):
        ch, cx, cy, h, rot = l
        y = cy + h * (0.30 if i % 2 else 0.34)
        g = faixa_onda(y, 26, PRETO, cx - 700, cx + 700, ondas=2.2, fase=i)
        g += faixa_onda(y + 22, 26, acento, cx - 700, cx + 700, ondas=2.2, fase=i)
        # bolhinhas de brilho dentro do acento
        random.seed(i * 11)
        for _ in range(3):
            bx = cx + random.uniform(-h * 0.35, h * 0.35)
            by = y + random.uniform(90, h * 0.3)
            g += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{random.uniform(14, 26):.0f}" fill="{branco}"/>'
        # brilho no topo esquerdo (traço + ponto em preto fino? -> acento)
        tx, ty = cx - h * 0.28, cy - h * 0.36
        g += (f'<path d="M{tx:.0f} {ty+60:.0f} Q{tx:.0f} {ty:.0f} {tx+70:.0f} {ty-10:.0f}" fill="none" '
              f'stroke="{acento}" stroke-width="22" stroke-linecap="round"/>')
        return g
    return f


def texto_tag(txt, x, y, alt, cor, giro=0, fonte_="sedgwick-ave-display"):
    """texto vetorial (centrado) com contorno preto e sombra"""
    partes, cur = [], 0
    ref = glifo(fonte_, "0")[1]
    s = alt / (ref[3] - ref[1])
    ws = [glifo(fonte_, c)[2] for c in txt]
    total = sum(ws) * s
    g = f'<g transform="translate({x} {y}) rotate({giro}) translate({-total/2:.0f} 0)">'
    camadas = [("translate(14 18)", PRETO, 40), ("", PRETO, 40), ("", cor, 0)]
    for tr0, c, sw in camadas:
        cur = 0
        for ch, w in zip(txt, ws):
            d = glifo(fonte_, ch)[0]
            g += (f'<path d="{d}" transform="{tr0} translate({cur*s:.0f} 0) scale({s:.4f})" fill="{c}" '
                  f'stroke="{c}" stroke-width="{sw}" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>')
            cur += w
    return g + "</g>"


def versao_bolha(acento=ACENTO, extr="#4A2D61", nome="costas-A-bolha"):
    F = "bagel-fat-one"
    # (dx, dy, dalt, giro) por letra: T E R / C E I / R A O
    jit = [(10, 40, 0.00, -10), (-10, -30, 0.08, 4), (60, 10, 0.02, 11),
           (-40, 10, 0.04, 7), (-20, 40, 0.00, -6), (40, -40, 0.06, 9),
           (-20, 150, 0.02, -8), (0, 170, 0.07, 3), (10, 180, 0.04, -9)]
    L = montar_linhas(F, [("TER", 1.0), ("CEI", 0.96), ("RAO", 1.04)], topo=330, alt=780, gap=-50,
                      sobrep=0.06, jitter=jit)
    enfeites = []
    for (x, y, r, c) in [(330, 470, 120, BRANCO), (2700, 330, 85, acento), (2800, 1380, 130, BRANCO),
                         (230, 1650, 80, acento), (2700, 2780, 95, acento), (380, 2950, 110, BRANCO),
                         (2880, 950, 55, BRANCO), (170, 1100, 50, BRANCO), (2500, 3080, 45, BRANCO)]:
        enfeites.append(estrela(x + 10, y + 14, r, PRETO))
        enfeites.append(estrela(x, y, r * 0.92, c))
    # til em cima do A (entre as linhas)
    A = L[7]
    enfeites.insert(0, til(A[1] - 10, A[2] - A[3] * 0.56, 500, BRANCO, giro=-8))
    pingos = {}
    def add(i, dx, fy, comp, larg):
        l = L[i]
        pingos.setdefault(i, []).append(tuple(pingo(l[1] + dx, l[2] + l[3] * fy, comp, larg, acento)))
    add(6, -150, 0.42, 170, 64)
    add(8, 90, 0.43, 260, 74)
    add(8, -120, 0.42, 110, 52)
    add(2, 60, 0.40, 90, 50)
    # ano em letra de spray embaixo
    enfeites.append(texto_tag("2027", 1500, 3200, 190, BRANCO, giro=-4, fonte_="bagel-fat-one"))
    return dict(fonte=F, letras=L, recheio=BRANCO, extrusao_cor=extr, halo_cor=acento,
                contorno=24, halo=70, extrusao=(30, 44), faixa=recheio_grafite(acento),
                enfeites=enfeites, pingos=pingos)


def recheio_listras(acento):
    """recheio de bloco: listras diagonais de acento na metade de baixo"""
    def f(i, l):
        ch, cx, cy, h, rot = l
        y0 = cy + h * 0.05
        g = faixa_onda(y0, 0, PRETO, cx - 700, cx + 700, ondas=0)
        g += faixa_onda(y0 + 20, 0, acento, cx - 700, cx + 700, ondas=0)
        for k in range(-8, 9):
            x = cx + k * 120
            g += (f'<path d="M{x} {y0+20} l-260 600" stroke="{PRETO}" stroke-width="26"/>')
        tx, ty = cx - h * 0.30, cy - h * 0.38
        g += f'<path d="M{tx:.0f} {ty:.0f} l120 0 M{tx:.0f} {ty+45:.0f} l50 0" stroke="{acento}" stroke-width="22" stroke-linecap="round"/>'
        return g
    return f


def versao_bloco(acento=ACENTO, extr=PRETO):
    F = "titan-one"
    jit = [(20, 30, 0.00, -6), (0, -20, 0.08, 3), (-10, 10, 0.02, 7),
           (-10, 0, 0.04, 4), (10, 30, 0.00, -5), (0, -20, 0.06, 6),
           (-20, 40, 0.02, -5), (0, 20, 0.07, 3), (10, 50, 0.04, -6)]
    L = montar_linhas(F, [("TER", 1.0), ("CEI", 0.96), ("RAO", 1.02)], topo=420, alt=740, gap=-30,
                      sobrep=0.10, jitter=jit)
    enfeites = []
    for (x, y, r, c) in [(300, 420, 120, BRANCO), (2720, 360, 85, acento), (2820, 1400, 120, BRANCO),
                         (210, 1650, 80, acento), (2700, 2820, 95, acento), (360, 2900, 110, BRANCO)]:
        enfeites.append(estrela(x + 10, y + 14, r, PRETO))
        enfeites.append(estrela(x, y, r * 0.92, c))
    A = L[7]
    enfeites.insert(0, til(A[1], A[2] - A[3] * 0.62, 470, acento, giro=-5))
    enfeites.append(texto_tag("2027", 1500, 3170, 200, BRANCO, giro=-3, fonte_="titan-one"))
    return dict(fonte=F, letras=L, recheio=BRANCO, extrusao_cor="#2A1838", halo_cor=acento,
                contorno=22, halo=64, extrusao=(26, 40), faixa=recheio_listras(acento),
                enfeites=enfeites, join="miter", skew=-6)


def capelo(cx, cy, larg, cor, giro=-12):
    """chapéu de formatura simples (vetor) com contorno preto"""
    w = larg
    topo = f"M{-w/2} 0 L0 {-w*0.26} L{w/2} 0 L0 {w*0.26}Z"
    base = f"M{-w*0.3} {w*0.1} L{-w*0.3} {w*0.32} Q0 {w*0.46} {w*0.3} {w*0.32} L{w*0.3} {w*0.1}Z"
    borla = f"M0 0 L{w*0.38} {w*0.05} L{w*0.4} {w*0.38}"
    g = f'<g transform="translate({cx} {cy}) rotate({giro})" stroke-linejoin="round" stroke-linecap="round">'
    for dx, c, sw in [(16, PRETO, 40), (0, PRETO, 40)]:
        g += f'<g transform="translate({dx} {dx*1.3})" fill="{c}" stroke="{c}" stroke-width="{sw}"><path d="{base}"/><path d="{topo}"/></g>'
    g += f'<path d="{base}" fill="{PRETO}"/><path d="{base}" fill="{cor}" transform="scale(0.86) translate(0 4)"/>'
    g += f'<path d="{topo}" fill="{BRANCO}"/>'
    g += f'<path d="{borla}" fill="none" stroke="{PRETO}" stroke-width="34"/><path d="{borla}" fill="none" stroke="{cor}" stroke-width="14"/>'
    g += f'<circle cx="{w*0.4}" cy="{w*0.42}" r="{w*0.06}" fill="{cor}" stroke="{PRETO}" stroke-width="14"/>'
    g += f'<circle r="{w*0.04}" fill="{PRETO}"/>'
    return g + "</g>"


def versao_peito(acento=ACENTO, extr="#4A2D61"):
    """frente (peito esquerdo): 3 grafitado com capelo"""
    F = "bagel-fat-one"
    L = [("3", 590, 650, 760, -6)]
    enf = [capelo(800, 300, 380, acento, giro=14)]
    for (x, y, r, c) in [(200, 330, 80, BRANCO), (1030, 900, 60, acento), (170, 1050, 45, BRANCO)]:
        enf.append(estrela(x + 8, y + 10, r, PRETO)); enf.append(estrela(x, y, r * 0.92, c))
    return dict(fonte=F, letras=L, recheio=BRANCO, extrusao_cor=extr, halo_cor=acento, tamanho=(1200, 1250),
                contorno=24, halo=70, extrusao=(30, 44), faixa=recheio_grafite(acento), enfeites=enf)


def versao_manga(acento=ACENTO, extr="#4A2D61", ano="2027"):
    """manga: ano empilhado na vertical + brilhos"""
    F = "bagel-fat-one"
    jit = [(-20, 0, 0, -8), (25, 0, 0, 6), (-20, 0, 0, -6), (20, 0, 0, 8)]
    L = montar_linhas(F, [(c, 1.0) for c in ano], cx=400, topo=260, alt=480, gap=40, sobrep=0, jitter=jit)
    enf = []
    for (x, y, r, c) in [(130, 120, 70, BRANCO), (680, 2450, 80, acento), (110, 2600, 50, BRANCO), (700, 140, 40, acento)]:
        enf.append(estrela(x + 8, y + 10, r, PRETO)); enf.append(estrela(x, y, r * 0.92, c))
    return dict(fonte=F, letras=L, recheio=BRANCO, extrusao_cor=extr, halo_cor=acento, tamanho=(800, 2750),
                contorno=22, halo=60, extrusao=(24, 36), faixa=recheio_grafite(acento), enfeites=enf)


NOMES_EXEMPLO = ["Ana", "Lucas", "Bia", "Pedro", "Júlia", "Gabi", "Rafa", "Duda", "Theo", "Lari",
                 "Mari", "Joãozinho", "Isa", "Caio", "Lelê", "Prof. Marcos", "Vini", "Nina", "Gui", "Malu"]

def forro_capuz(nomes, cor, fundo=ROXO, W=3000, H=2000):
    """estampa corrida do forro do capuz: nomes em letra de tag (handstyle)"""
    random.seed(3)
    out, i = [], 0
    y = 110
    while y < H + 100:
        x = -random.uniform(0, 250)
        while x < W:
            n = nomes[i % len(nomes)]; i += 1
            alt = random.uniform(95, 130)
            g = random.uniform(-14, 8)
            out.append(texto_tag_simples(n, x, y, alt, cor, g))
            x += len(n) * alt * 0.55 + 140
        y += 190
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + "".join(out) + "</svg>"), W, H


def texto_tag_simples(txt, x, y, alt, cor, giro, fonte_="sedgwick-ave-display"):
    ref = glifo(fonte_, "N")[1]
    s = alt / (ref[3] - ref[1])
    g = f'<g transform="translate({x:.0f} {y:.0f}) rotate({giro:.1f}) scale({s:.4f})" fill="{cor}">'
    cur = 0
    for ch in txt:
        d, _, w = glifo(fonte_, ch)
        g += f'<path d="{d}" transform="translate({cur} 0)"/>'
        cur += w
    return g + "</g>"


CORES = {"lima": "#C8FF3D", "rosa": "#FF4FB0", "branco": "#FFFFFF"}

if __name__ == "__main__":
    alvo = sys.argv[1:] or list(CORES)
    for nome in alvo:
        ac = CORES[nome]
        salvar(f"{nome}/costas", *arte_costas(versao_bolha(ac)))
        salvar(f"{nome}/peito", *arte_costas(versao_peito(ac)))
        salvar(f"{nome}/manga", *arte_costas(versao_manga(ac)))
        salvar(f"{nome}/forro-capuz", *forro_capuz(NOMES_EXEMPLO, ac if nome != "branco" else BRANCO))
