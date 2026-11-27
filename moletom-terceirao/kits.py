"""Kit de adesivos (cartela recortada sobre madeira escura), convites de festa (4 versões) e kit da formatura (flat lay).
-> final/keyvisuals/kit-adesivos.png, final/keyvisuals/kit-formatura.png, final/convites/convite-*.png
"""
import subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from adesivo_cenas import adesivo, perspectiva, cola, superficie, acabamento, sem_brilhos, ART, S27

AQUI = Path(__file__).parent
KV = AQUI / "final/keyvisuals"; CV = AQUI / "final/convites"; CV.mkdir(parents=True, exist_ok=True)
TMP = AQUI / "final/_manual"
U = lambda p: Path(p).resolve().as_uri(); FO = U(AQUI / "fontes")
ROXO, LILAS, UVA = "#996BB3", "#E4CFF7", "#3E2353"
FONTS = f"""@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:K;src:url('{FO}/space-grotesk-500.woff2');font-weight:500}}
@font-face{{font-family:K;src:url('{FO}/space-grotesk-700.woff2');font-weight:700}}"""


def html_png(corpo, W, H, saida, transp=False, css=""):
    f = TMP / "_k.html"
    f.write_text(f"<!doctype html><html><head><meta charset=utf-8><style>{FONTS}*{{margin:0;box-sizing:border-box}}"
                 f"html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{'transparent' if transp else '#07060A'}}}{css}</style></head><body>{corpo}</body></html>")
    subprocess.run(["node", str(AQUI.parent / "tools/html-to-png-exato.js"), str(f), str(saida), str(W), str(H), "1", "t" if transp else ""], check=True)
    f.unlink()
    return Image.open(saida).convert("RGBA")


def texto_adesivo(txt, tam, cor, fundo=None, saida="x.png"):
    estilo = (f"font-family:G;font-size:{tam}px;color:{cor};-webkit-text-stroke:{tam*.14:.0f}px #0A0A0C;paint-order:stroke fill;"
              f"filter:drop-shadow({tam*.04:.0f}px {tam*.05:.0f}px 0 {UVA})")
    if fundo:
        estilo = (f"font-family:K;font-weight:700;font-size:{tam}px;letter-spacing:.12em;color:{cor};background:{fundo};"
                  f"padding:{tam*.5:.0f}px {tam*1.1:.0f}px;border-radius:999px")
    im = html_png(f'<div style="position:absolute;left:40px;top:40px;white-space:nowrap;line-height:1.1;{estilo}">{txt}</div>', 1600, 600, TMP / saida, True)
    return im.crop(im.getbbox())


def kit_adesivos():
    peças = [
        (sem_brilhos(ART), 300, (60, 50), -4),
        (S27, 230, (470, 70), 8),
        (texto_adesivo("ÚLTIMO ANO.", 120, "#fff", saida="_t1.png"), 360, (400, 330), -6),
        (texto_adesivo("TURMA 27", 44, "#fff", ROXO, "_t2.png"), 300, (60, 560), 3),
        (texto_adesivo("2027", 120, LILAS, saida="_t3.png"), 220, (520, 520), 6),
        (texto_adesivo("MÃE DE DEUS", 34, "#0A0A0C", "#E4CFF7", "_t4.png"), 320, (60, 720), -2),
        (S27, 150, (560, 720), -12),
        (texto_adesivo("TERCEIRÃO", 96, "#fff", saida="_t5.png"), 440, (170, 880), 2),
    ]
    SW, SH = 820, 1060
    folha = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    d = ImageDraw.Draw(folha); d.rounded_rectangle((0, 0, SW, SH), 36, fill=(236, 232, 240, 255))
    g = np.asarray(folha).astype(float); g[..., :3] += np.random.default_rng(4).normal(0, 2.5, g[..., :3].shape)
    folha = Image.fromarray(g.clip(0, 255).astype(np.uint8))
    for arte, larg, (x, y), giro in peças:
        st = adesivo(arte, larg, borda=12).rotate(giro, Image.BICUBIC, expand=True)
        corte = st.split()[3].point(lambda v: 255 if v > 30 else 0).filter(ImageFilter.MaxFilter(5))
        ln = Image.new("RGBA", st.size, (170, 160, 180, 0)); ln.putalpha(ImageChops_diff(corte))
        folha.alpha_composite(ln, (x - 2, y - 2)); folha.alpha_composite(st, (x, y))
    d = ImageDraw.Draw(folha)
    base, L = superficie("black_painted_planks", .9, .75, (.45, .4), forca=.3)
    folha = folha.resize((int(SW * .86), int(SH * .86)), Image.LANCZOS)
    st = perspectiva(folha, .04, 0, -9)
    base = cola(base, L, st, 340, 25, relevo=.15, sombra=(18, 30, 26, .7))
    solto = perspectiva(adesivo(sem_brilhos(ART), 300, borda=14), .05, 0, 14)
    base = cola(base, L, solto, 1230, 120, relevo=.2, sombra=(14, 24, 18, .6))
    solto2 = perspectiva(adesivo(S27, 210, borda=12), .03, 0, -18)
    base = cola(base, L, solto2, 1450, 640, relevo=.2, sombra=(12, 20, 16, .6))
    acabamento(base).save(KV / "kit-adesivos.png")


def ImageChops_diff(corte):
    """linha de meio-corte (kiss cut) em volta do adesivo"""
    a = np.asarray(corte) > 0
    from scipy import ndimage
    borda = ndimage.binary_dilation(a, iterations=3) & ~a
    return Image.fromarray((borda * 140).astype(np.uint8))


CONVITES = [
    ("festa", ROXO, "#fff", "FESTA DO", "TERCEIRÃO", "Sexta · 22h", "Ingresso antecipado com a comissão"),
    ("baile", "#0B0812", ROXO, "BAILE", "27", "Dezembro · 2027", "Traje: preto e roxo"),
    ("100dias", LILAS, UVA, "FALTAM", "100 DIAS", "Festa dos 100 dias", "Só formandos e convidados"),
    ("ultimo", "#0B0812", "#fff", "ÚLTIMO", "SINAL.", "Despedida da turma", "Pátio · último dia de aula"),
]


def convites():
    ART_SB = TMP / "arte-sb.png"; sem_brilhos(ART).save(ART_SB)
    for nome, bg, acc, l1, l2, quando, obs in CONVITES:
        escuro = bg in ("#0B0812",)
        cor_txt = "#fff" if escuro or bg == ROXO else "#0B0812"
        fundo = (f"radial-gradient(ellipse 80% 60% at 50% 100%,rgba(153,107,179,.55),transparent 70%),{bg}" if escuro
                 else f"linear-gradient(160deg,{bg},{bg}dd)")
        grande = f"font-family:G;font-size:{300 if len(l2) < 5 else 210}px;line-height:.9;color:{acc if escuro else '#fff'};-webkit-text-stroke:{34 if len(l2) < 5 else 26}px #0A0A0C;paint-order:stroke fill;filter:drop-shadow(10px 12px 0 {UVA})"
        corpo = f"""<div style="position:absolute;inset:0;background:{fundo}"></div>
<div style="position:absolute;left:70px;right:70px;top:64px;display:flex;justify-content:space-between;font-family:K;font-weight:700;font-size:20px;letter-spacing:.3em;color:{cor_txt};opacity:.8"><span>TERCEIRÃO 2027</span><span>MÃE DE DEUS</span></div>
<div style="position:absolute;left:70px;top:200px;font-family:K;font-weight:700;font-size:96px;letter-spacing:-.03em;color:{cor_txt}">{l1}</div>
<div id=g style="position:absolute;left:60px;top:300px;white-space:nowrap;{grande}">{l2}</div>
<img src="{U(ART_SB)}" style="position:absolute;right:70px;top:640px;width:430px;transform:rotate(8deg);filter:drop-shadow(0 30px 40px rgba(0,0,0,.45))">
<script>document.fonts.ready.then(()=>{{const g=document.getElementById('g');let f=parseFloat(getComputedStyle(g).fontSize);
while(g.getBoundingClientRect().width>950&&f>60){{f-=4;g.style.fontSize=f+'px';g.style.webkitTextStroke=(f*.11)+'px #0A0A0C'}}}})</script>
<div style="position:absolute;left:70px;right:70px;bottom:70px;border-top:2px solid {cor_txt}33;padding-top:30px;color:{cor_txt}">
 <div style="font-family:K;font-weight:700;font-size:44px;letter-spacing:-.01em">{quando}</div>
 <div style="font-family:K;font-weight:500;font-size:24px;opacity:.75;margin-top:10px">{obs}</div></div>"""
        html_png(corpo, 1080, 1500, CV / f"convite-{nome}.png")


def kit_formatura():
    ARTB = U(AQUI / "final/versoes-1cor/terceirao-1cor-branco.png")
    ART_SB = U(TMP / "arte-sb.png"); S27B = U(AQUI / "final/simbolo/simbolo-27-branco.png")
    tx = U(AQUI / "referencias/texturas/black_painted_planks.jpg")
    sh = "box-shadow:0 2px 3px rgba(0,0,0,.4),0 30px 60px rgba(0,0,0,.6)"
    corpo = f"""<div style="position:absolute;inset:0;background:url('{tx}') center/900px;filter:brightness(.38) saturate(.4)"></div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 50% 40%,rgba(153,107,179,.22),transparent 70%),radial-gradient(ellipse 80% 80% at 50% 50%,transparent 50%,rgba(0,0,0,.7))"></div>
<!-- envelope -->
<div style="position:absolute;left:140px;top:150px;width:620px;height:430px;background:linear-gradient(160deg,#4a2d61,{UVA});border-radius:6px;transform:rotate(-7deg);{sh}">
 <div style="position:absolute;inset:0;background:linear-gradient(155deg,transparent 49.6%,rgba(0,0,0,.18) 50%,transparent 50.4%),linear-gradient(25deg,transparent 49.6%,rgba(0,0,0,.18) 50%,transparent 50.4%)"></div>
 <div style="position:absolute;left:250px;top:150px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#c49be0,{ROXO} 55%,#6e4789);box-shadow:0 6px 10px rgba(0,0,0,.4),inset 0 -6px 10px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center">
  <img src="{S27B}" style="width:80px;opacity:.9"></div>
 <div style="position:absolute;left:30px;bottom:24px;font-family:K;font-weight:700;font-size:15px;letter-spacing:.3em;color:#E4CFF7;opacity:.7">PARA: ______________</div></div>
<!-- convite frente -->
<div style="position:absolute;left:820px;top:90px;width:460px;height:640px;background:radial-gradient(ellipse 90% 60% at 50% 100%,rgba(153,107,179,.6),transparent 70%),#0B0812;border-radius:8px;transform:rotate(3deg);{sh};overflow:hidden">
 <img src="{ART_SB}" style="position:absolute;left:70px;top:70px;width:320px">
 <div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;font-family:K;font-weight:700;font-size:16px;letter-spacing:.35em;color:#E4CFF7">FORMATURA · 2027</div></div>
<!-- convite verso -->
<div style="position:absolute;left:1340px;top:150px;width:440px;height:610px;background:#F2EEF5;border-radius:8px;transform:rotate(-4deg);{sh};padding:56px 50px;color:#0B0812">
 <div style="font-family:K;font-weight:700;font-size:15px;letter-spacing:.35em;color:{ROXO}">CERIMÔNIA DE FORMATURA</div>
 <div style="font-family:G;font-size:92px;line-height:.92;color:{ROXO};-webkit-text-stroke:12px #0B0812;paint-order:stroke fill;margin-top:30px">TURMA<br>2027</div>
 <div style="font-family:K;font-weight:500;font-size:21px;line-height:1.6;margin-top:36px">Os formandos do 3º ano do<br><b>Colégio Mãe de Deus</b><br>convidam você para<br>celebrar esse fim de ciclo.</div>
 <div style="position:absolute;left:50px;right:50px;bottom:50px;display:flex;justify-content:space-between;font-family:K;font-weight:700;font-size:16px;letter-spacing:.15em"><span>DATA</span><span>HORA</span><span>LOCAL</span></div></div>
<!-- ingresso -->
<div style="position:absolute;left:230px;top:660px;width:720px;height:270px;background:linear-gradient(115deg,{ROXO},#7A4C99);border-radius:16px;transform:rotate(4deg);{sh};overflow:hidden">
 <div style="position:absolute;right:190px;top:0;bottom:0;border-left:3px dashed rgba(10,10,12,.35)"></div>
 <i style="position:absolute;right:172px;top:-18px;width:36px;height:36px;border-radius:50%;background:#1a1420"></i><i style="position:absolute;right:172px;bottom:-18px;width:36px;height:36px;border-radius:50%;background:#1a1420"></i>
 <div style="position:absolute;left:44px;top:40px;font-family:K;font-weight:700;font-size:15px;letter-spacing:.35em;color:#0B0812;opacity:.7">BAILE DE FORMATURA</div>
 <div style="position:absolute;left:40px;top:76px;font-family:G;font-size:92px;line-height:1;color:#fff;-webkit-text-stroke:12px #0B0812;paint-order:stroke fill">BAILE 27</div>
 <div style="position:absolute;left:44px;bottom:38px;font-family:K;font-weight:700;font-size:15px;letter-spacing:.25em;color:#0B0812">DEZ · 2027 · 22H</div>
 <div style="position:absolute;right:0;top:0;width:190px;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
  <img src="{S27B}" style="width:110px"><div style="font-family:K;font-weight:700;font-size:14px;letter-spacing:.25em;color:#0B0812">Nº 0001</div></div></div>
<!-- crachá -->
<div style="display:none;background:repeating-linear-gradient(90deg,{ROXO} 0 14px,#0B0812 14px 28px);transform:rotate(-8deg);transform-origin:top;{sh}"></div>
<div style="position:absolute;left:1020px;top:770px;width:200px;height:260px;background:#0B0812;border-radius:16px;transform:rotate(-8deg);{sh};overflow:hidden;border:1px solid #2a2330">
 <div style="height:120px;background:linear-gradient(120deg,{ROXO},{UVA})"></div>
 <img src="{ARTB}" style="position:absolute;left:75px;top:30px;width:110px">
 <div style="position:absolute;left:0;right:0;top:200px;text-align:center;font-family:K;font-weight:700;font-size:22px;color:#fff">NOME DO ALUNO</div>
 <div style="position:absolute;left:0;right:0;top:236px;text-align:center;font-family:K;font-weight:700;font-size:11px;letter-spacing:.3em;color:{ROXO}">FORMANDO · 3º ANO</div></div>
<!-- adesivo redondo -->
<div style="position:absolute;left:1440px;top:800px;width:230px;height:230px;border-radius:50%;background:{ROXO};border:10px solid #F2EEF5;{sh};display:flex;align-items:center;justify-content:center"><img src="{S27B}" style="width:150px"></div>"""
    html_png(corpo, 1920, 1080, KV / "kit-formatura.png")


if __name__ == "__main__":
    convites(); kit_adesivos(); kit_formatura(); print("ok")
