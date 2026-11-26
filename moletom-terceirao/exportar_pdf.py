"""Exporta a arte das costas em VETOR editável (SVG + PDF pro Illustrator).

uso: python3 exportar_pdf.py  -> pdf/costas-04-til30.pdf, pdf/costas-04-til26.pdf, pdf/terceirao-costas-editavel.pdf
Cada letra vira contorno (path); camadas em grupos: fundo, sombra-3d, contorno-branco, contorno-preto,
recheio-degrade, brilho, til, ano-2027, mae-de-deus, estrelas. Contornos são strokes (dá pra mudar a espessura).
"""
import json, math, subprocess
from pathlib import Path
import uharfbuzz as hb
import cairosvg
from pypdf import PdfWriter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import costas, tils

AQUI = Path(__file__).parent
OUT = AQUI / "pdf"; OUT.mkdir(exist_ok=True)
FONTE = AQUI / "fontes/dafont/graffiti_youth.otf"
ARIAL_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
ROXO, CLARO, ESCURO, UVA = costas.ROXO, costas.CLARO, costas.ESCURO, costas.UVA
SOMBRA = [(7, 8, UVA), (14, 16, UVA), (20, 23, UVA), (25, 29, "#000000")]  # = drop-shadows do CSS acumulados


def texto_path(fonte, txt, fs, espaco=0.0):
    """path SVG do texto já com kerning (harfbuzz), origem na linha de base"""
    blob = hb.Blob.from_file_path(str(fonte)); face = hb.Face(blob); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(font, buf)
    tt = TTFont(str(fonte)); gs = tt.getGlyphSet(); upem = tt["head"].unitsPerEm; s = fs / upem
    order = tt.getGlyphOrder(); x = 0; ds = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs)
        gs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s)))
        ds.append(pen.getCommands()); x += pos.x_advance * s + espaco
    return " ".join(ds), x


def layout(html):
    h = OUT / "_l.html"; h.write_text(html)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
          "const p=await b.newPage({viewport:{width:1500,height:1800}});await p.goto('file://'+process.argv[1]);"
          "await p.waitForFunction(()=>document.body.dataset.layout);"
          "console.log(await p.evaluate(()=>document.body.dataset.layout));await b.close();})()")
    r = subprocess.run(["node", "-e", js, str(h.resolve())], capture_output=True, text=True, check=True)
    h.unlink(); return json.loads(r.stdout)


def svg_costas(L, til_d, til_k, til_rot):
    linhas = []
    for i, l in enumerate(L["linhas"]):
        d, _ = texto_path(FONTE, l["t"], l["fs"])
        cx, cy = l["x"] + l["ox"], l["y"] + l["oy"]
        tr = f'rotate({l["rot"]} {cx:.2f} {cy:.2f}) translate({l["x"]:.2f} {l["y"] + l["base"]:.2f})'
        linhas.append((i, l, d, tr, cx, cy))
    g = {k: [] for k in ("sombra-3d", "contorno-branco", "contorno-preto", "recheio-degrade", "brilho", "til")}
    defs = []
    for i, l, d, tr, cx, cy in linhas:
        fs = l["fs"]; sw1, sw2 = 0.15 * fs, 0.075 * fs
        for dx, dy, c in SOMBRA:
            g["sombra-3d"].append(f'<path d="{d}" transform="translate({dx} {dy}) {tr}" fill="{c}" stroke="{c}" stroke-width="{sw1:.2f}" stroke-linejoin="round"/>')
        g["contorno-branco"].append(f'<path d="{d}" transform="{tr}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="{sw1:.2f}" stroke-linejoin="round"/>')
        g["contorno-preto"].append(f'<path d="{d}" transform="{tr}" fill="#0A0A0C" stroke="#0A0A0C" stroke-width="{sw2:.2f}" stroke-linejoin="round"/>')
        top = -l["base"]  # topo da caixa da linha, em coordenadas locais (base = 0)
        defs.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{top:.1f}" x2="0" y2="{top + fs:.1f}">'
                    f'<stop offset="0" stop-color="{CLARO}"/><stop offset=".5" stop-color="{ROXO}"/><stop offset="1" stop-color="{ESCURO}"/></linearGradient>')
        defs.append(f'<linearGradient id="b{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{top:.1f}" x2="0" y2="{top + fs:.1f}">'
                    f'<stop offset="0" stop-color="#fff" stop-opacity=".33"/><stop offset=".11" stop-color="#fff" stop-opacity=".33"/>'
                    f'<stop offset=".115" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        g["recheio-degrade"].append(f'<path d="{d}" transform="{tr}" fill="url(#g{i})"/>')
        g["brilho"].append(f'<path d="{d}" transform="{tr}" fill="url(#b{i})"/>')
        if l.get("til"):
            tx, ty = l["x"] + l["til"]["x"], l["y"] + l["til"]["y"]
            ttr = f'rotate({l["rot"]} {cx:.2f} {cy:.2f}) translate({tx:.2f} {ty:.2f}) scale({til_k:.5f}) rotate({til_rot})'
            defs.append('<linearGradient id="gt" gradientUnits="userSpaceOnUse" x1="0" y1="-90" x2="0" y2="110">'
                        f'<stop offset="0" stop-color="{CLARO}"/><stop offset=".5" stop-color="{ROXO}"/><stop offset="1" stop-color="{ESCURO}"/></linearGradient>')
            g["til"] += [f'<g transform="{ttr}" stroke-linejoin="round">',
                         f'<path d="{til_d}" fill="{UVA}" stroke="{UVA}" stroke-width="78" transform="translate(18 21)"/>',
                         f'<path d="{til_d}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="78"/>',
                         f'<path d="{til_d}" fill="#0A0A0C" stroke="#0A0A0C" stroke-width="39"/>',
                         f'<path d="{til_d}" fill="url(#gt)"/></g>']
    # 2027 (branco, contorno preto, sombra roxa, -5°)
    a = L["ano"]; fs = 170
    d, w = texto_path(FONTE, "2027", fs)
    base = a["y"] + (a["h"] - (a["FA"] + a["FD"])) / 2 + a["FA"]
    acx, acy = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    atr = f'rotate(-5 {acx:.2f} {acy:.2f}) translate({acx - w / 2:.2f} {base:.2f})'
    ano = [f'<path d="{d}" transform="translate(6 7) {atr}" fill="{ROXO}" stroke="{ROXO}" stroke-width="{0.15*fs:.1f}" stroke-linejoin="round"/>',
           f'<path d="{d}" transform="{atr}" fill="#FFFFFF" stroke="#0A0A0C" stroke-width="{0.15*fs:.1f}" stroke-linejoin="round" paint-order="stroke"/>',
           f'<path d="{d}" transform="{atr}" fill="#FFFFFF"/>']
    # MÃE DE DEUS (Arial Bold 40, espaçamento .45em, -5°)
    e = L["esc"]; d, w = texto_path(ARIAL_B, "MÃE DE DEUS", 40, espaco=18)
    ecx, ecy = e["x"] + e["w"] / 2, e["y"] + e["h"] / 2
    esc = [f'<path d="{d}" transform="rotate(-5 {ecx:.2f} {ecy:.2f}) translate({ecx - w / 2:.2f} {ecy + 14:.2f})" fill="{ROXO}"/>']
    # estrelas (mesmas posições do costas.py)
    est = []
    for x, y, sz, c in [(120, 250, 90, "#FFFFFF"), (1310, 200, 60, ROXO), (1330, 1000, 70, "#FFFFFF"), (110, 1150, 44, ROXO), (1250, 1560, 50, "#FFFFFF")]:
        pts = [(50, 0), (58, 42), (100, 50), (58, 58), (50, 100), (42, 58), (0, 50), (42, 42)]
        est.append('<polygon fill="%s" points="%s"/>' % (c, " ".join(f"{x + px * sz / 100:.1f},{y + py * sz / 100:.1f}" for px, py in pts)))
    grupo = lambda nome, itens, extra="": f'<g id="{nome}" {extra}>' + "".join(itens) + "</g>"
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1800" viewBox="0 0 1500 1800">'
            f'<defs>{"".join(defs)}</defs>'
            + grupo("fundo-apagar-pra-estampa", ['<rect width="1500" height="1800" fill="#0A0A0C"/>'])
            + "".join(grupo(k, v) for k, v in g.items() if k != "til")
            + grupo("til", g["til"]) + grupo("ano-2027", ano) + grupo("mae-de-deus", esc) + grupo("estrelas", est)
            + "</svg>")


if __name__ == "__main__":
    pdfs = []
    for n, esc_til in ((30, 0.72), (26, 0.85)):
        a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[n - 1]
        costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
        costas.TIL_ESC = esc_til
        L = layout(costas.html("graffiti_youth.otf", True, True))
        fs3 = L["linhas"][2]["fs"]
        svg = svg_costas(L, costas.TIL_D, fs3 / 520 * esc_til, rot)
        base = OUT / f"costas-04-til{n}"
        base.with_suffix(".svg").write_text(svg)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(base.with_suffix(".pdf")))
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(base.with_suffix(".png")))
        pdfs.append(base.with_suffix(".pdf")); print("ok", base.name)
    w = PdfWriter()
    for p in pdfs: w.append(str(p))
    w.write(str(OUT / "terceirao-costas-editavel.pdf"))
