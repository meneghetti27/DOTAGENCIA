"""Renderiza os favoritos do ano (arte principal + variações) no PRETO e em NEGATIVO nativo (sem inverter pixel).

uso: python3 favoritos.py  -> costas/ano-favoritos/<nome>.png e <nome>-negativo.png
- Sem apóstrofo no '27: ele caía em cima do pé do R e virava uma mancha (dono reclamou).
- Negativo: fundo claro, contorno de fora PRETO (forte), contorno de dentro preto, brilho branco, roxo igual,
  estrelas brancas viram pretas.
"""
import costas, tils
import numpy as np
from PIL import Image
from scipy import ndimage

P = costas.OUT / "ano-favoritos"
a, g, o, pt, fo, lg, inc, rot, j, fill = tils.V[25]
costas.TIL_D = tils.faixa(a, g, o, pt, fo, lg, inc); costas.TIL_ROT, costas.TIL_JOIN, costas.TIL_FILL = rot, j, fill
costas.TIL_ESC = 0.85
GS, KJ = "grime_slime.ttf", "king_jack_style.ttf"
D = lambda txt, f, tam, cor, ax=0.72, ay=0, rot=-6: (f, dict(txt=txt, fam="A", tam=tam, ax=ax, ay=ay, rot=rot, cor=cor, esc_dy=25))
FAV = {  # nome: (fonte, params)   — mesmos parâmetros das escolhidas, sem o apóstrofo
    "integrado-25": D("27", GS, 260, "branco"),
    "ano30-01": D("27", GS, 260, "branco"),
    "ano30-03": D("27", GS, 260, "lilas"),
    "ano30-07": D("27", GS, 240, "branco", ax=0.9, ay=-40, rot=-12),
    "ano30-11": D("27", KJ, 250, "branco"),
    "ano30-19": D("2027", GS, 200, "branco"),
    "ano30-22": D("2027", GS, 190, "branco", ax=0.5),
    "ano30-23": D("2027", GS, 180, "branco", ax=0.82, ay=-50, rot=-12),
    "ano30-30": D("27", GS, 280, "meio"),
}


def negativo(html):
    trocas = [
        ("background:radial-gradient(ellipse 60% 45% at 50% 45%,#1E1229 0%,#0A0A0C 72%)", "background:#F4F1F7"),
        ("-webkit-text-stroke:.15em #fff;color:#fff", "-webkit-text-stroke:.15em #0A0A0C;color:#0A0A0C"),  # contorno de fora
        ('fill="#fff" stroke="#fff"', 'fill="#0A0A0C" stroke="#0A0A0C"'),                                   # til
        ("--c:#fff", "--c:#0A0A0C"),                                                                          # estrelas
    ]
    for a, b in trocas:
        assert a in html, a
        html = html.replace(a, b)
    return html


MASCARA = ("</style>", ".l1,.l2,.l4,.st,.esc,svg{visibility:hidden!important}"
           ".l3{background:none!important;color:#f00!important;-webkit-text-fill-color:#f00!important}"
           "html,body{background:#000!important}</style>")


def buracos(nome):
    """máscara dos buracos de dentro das letras (contraforma), menos uma borda fina pra manter a linha preta"""
    h = P / f"_{nome}-m.html"
    h.write_text(costas.html("graffiti_youth.otf", True, True).replace(*MASCARA))
    png = P / f"_{nome}-m.png"; costas.render(h, png); h.unlink()
    a = np.asarray(Image.open(png).convert("RGB")).astype(int); png.unlink()
    F = (a[..., 0] > 120) & (a[..., 1] < 90)
    lab, n = ndimage.label(ndimage.binary_fill_holes(F) & ~F)
    tam = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    H = np.isin(lab, [i + 1 for i, t in enumerate(tam) if t < 40000])
    return ndimage.binary_erosion(H, iterations=7)


def pinta(arq, H):
    im = np.asarray(Image.open(arq).convert("RGB")).copy(); im[H] = 255
    Image.fromarray(im).save(arq)


if __name__ == "__main__":
    for nome, (f, v) in FAV.items():
        costas.ANO_FONTE, costas.ANO_INT = f, v
        base = costas.html("graffiti_youth.otf", True, True)
        for suf, html in (("", base), ("-negativo", negativo(base))):
            h = P / f"_{nome}{suf}.html"; h.write_text(html)
            costas.render(h, P / f"{nome}{suf}.png"); h.unlink()
        H = buracos(nome)
        for suf in ("", "-negativo"): pinta(P / f"{nome}{suf}.png", H)
        print("ok", nome)
