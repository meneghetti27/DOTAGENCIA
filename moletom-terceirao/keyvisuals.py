"""Key visuals premium (estilo dos posts da dot: fundo escuro, luz de recorte, névoa, partículas, título atrás do objeto 3D)
-> final/keyvisuals/*.png  (cenas 1920x1080 pro brand book + posts 1080x1350 pro Instagram)
Objetos 3D renderizados em render3d/ (three.js, `node shot.js`).
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
OUT = AQUI / "final/keyvisuals"; OUT.mkdir(parents=True, exist_ok=True)
U = lambda p: Path(p).resolve().as_uri()
R = AQUI / "render3d/out"; A = AQUI / "final/aplicacoes"; FO = U(AQUI / "fontes")
ROXO, LILAS, UVA, PRETO = "#996BB3", "#E4CFF7", "#3E2353", "#0A0A0C"
PAT = U(AQUI / "final/padrao/estampa-corrida-27.png")

BASE = f"""<style>
@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:I;src:url('{FO}/inter-900.woff2');font-weight:900}}
@font-face{{font-family:M;src:url('{FO}/space-mono-700.woff2')}}
@font-face{{font-family:S;src:url('{FO}/playfair-display-400-italic.woff2');font-style:italic}}
*{{box-sizing:border-box;margin:0}} html,body{{height:100%;overflow:hidden;background:{PRETO}}}
.fx{{position:absolute;inset:0;pointer-events:none}}
.grao{{background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");opacity:.09;mix-blend-mode:overlay}}
.vin{{background:radial-gradient(ellipse 75% 75% at 50% 50%,transparent 55%,rgba(0,0,0,.75))}}
.titulo{{position:absolute;font-family:I;font-weight:900;letter-spacing:-.05em;line-height:.86;padding-top:.14em;text-align:center;white-space:nowrap;
  background:linear-gradient(180deg,#F4EAFB 0%,#C9A8E6 45%,{ROXO} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.lbl{{font-family:M;letter-spacing:.3em;text-transform:uppercase}}
.p{{position:absolute;border-radius:50%;background:#fff;filter:blur(var(--b));opacity:var(--o)}}
</style>"""

def particulas(n, W, H, seed=3, cor="#E4CFF7"):
    import random; random.seed(seed); s = ""
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.uniform(2, 9)
        s += f'<i class=p style="left:{x:.0f}px;top:{y:.0f}px;width:{r:.0f}px;height:{r:.0f}px;--b:{random.uniform(0,3):.1f}px;--o:{random.uniform(.25,.9):.2f};background:{cor}"></i>'
    return s

def nevoa(cor=ROXO, x=50, y=60, w=60, h=45, o=.55):
    return f'<div class=fx style="background:radial-gradient(ellipse {w}% {h}% at {x}% {y}%,{cor} 0%,transparent 70%);opacity:{o};filter:blur(30px)"></div>'

def holofote(x=50, larg=900, o=.22):
    return (f'<div class=fx style="background:conic-gradient(from 180deg at {x}% -10%,transparent 168deg,rgba(228,207,247,{o}) 180deg,transparent 192deg);filter:blur(18px)"></div>')

def reflexo(src, x, y, w):
    return (f'<img src="{src}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:scaleY(-1);opacity:.18;'
            f'-webkit-mask-image:linear-gradient(0deg,transparent 55%,#000);filter:blur(2px)">')

def chao(y, cor="#1a1020"):
    return f'<div class=fx style="top:{y}px;background:linear-gradient(180deg,{cor},{PRETO} 70%)"></div><div class=fx style="top:{y}px;height:2px;background:linear-gradient(90deg,transparent,rgba(228,207,247,.35),transparent)"></div>'

CENAS = {
    # --- cenas 1920x1080 ---
    "kv01-heroi": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 60% 70% at 50% 45%,#2E1A40 0%,#120B18 50%,{PRETO} 80%)"></div>
{holofote(50, o=.18)}{nevoa(ROXO, 50, 55, 55, 40, .45)}
<div class=titulo style="left:0;right:0;top:170px;font-size:520px;opacity:.95">2027</div>
<img src="{U(R/'arte3d.png')}" style="position:absolute;left:50%;top:40px;height:1000px;transform:translateX(-50%);filter:drop-shadow(0 40px 60px rgba(0,0,0,.7))">
{particulas(70, 1920, 1080)}
<div class=lbl style="position:absolute;left:90px;bottom:70px;font-size:15px;color:{LILAS};opacity:.7">Terceirão · Colégio Mãe de Deus</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "kv02-simbolo": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 50% 65% at 62% 48%,#33204A,{PRETO} 72%)"></div>
{holofote(62, o=.26)}{chao(820)}
<div class=titulo style="left:-40px;top:190px;font-size:400px;text-align:left;opacity:.9">ÚLTIMO<br>ANO.</div>
<img src="{U(R/'t27.png')}" style="position:absolute;left:880px;top:20px;width:960px;filter:drop-shadow(0 50px 50px rgba(0,0,0,.8))">
{reflexo(U(R/'t27.png'), 880, 1000, 960)}
{nevoa(LILAS, 62, 85, 40, 16, .25)}{particulas(50, 1920, 1080, 7)}
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "kv03-caneca": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 45% 60% at 58% 50%,#2B1A3A,{PRETO} 72%)"></div>
{holofote(58, o=.2)}{chao(860)}
<div class=titulo style="left:120px;top:200px;font-size:300px;text-align:left;opacity:.22">CAFÉ<br>DE PROVA</div>
<img src="{U(R/'caneca.png')}" style="position:absolute;left:780px;top:60px;width:1000px">
{nevoa(UVA, 58, 92, 50, 18, .6)}{particulas(40, 1920, 1080, 11)}
<div class=lbl style="position:absolute;left:120px;bottom:90px;font-size:15px;color:{LILAS};opacity:.7">Caneca · cerâmica preta fosca</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "kv04-bottons": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 60% 70% at 50% 50%,#2A1838,{PRETO} 75%)"></div>
<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.08">
{nevoa(ROXO, 50, 50, 50, 50, .4)}
<img src="{U(R/'bottonarte.png')}" style="position:absolute;left:300px;top:150px;width:720px;transform:rotate(-12deg);filter:drop-shadow(30px 40px 40px rgba(0,0,0,.7))">
<img src="{U(R/'botton27.png')}" style="position:absolute;left:930px;top:300px;width:620px;transform:rotate(14deg);filter:drop-shadow(30px 40px 40px rgba(0,0,0,.7))">
<img src="{U(R/'t27.png')}" style="position:absolute;left:1380px;top:-40px;width:520px;transform:rotate(18deg);filter:blur(5px) drop-shadow(20px 30px 30px rgba(0,0,0,.6));opacity:.85">
{particulas(60, 1920, 1080, 5)}
<div class=lbl style="position:absolute;left:90px;bottom:70px;font-size:15px;color:{LILAS};opacity:.7">Bottons · 58 mm</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "kv05-moletom": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 55% 75% at 50% 45%,#2C1A3C,{PRETO} 75%)"></div>
{holofote(50, o=.2)}
<div class=titulo style="left:0;right:0;top:300px;font-size:330px;opacity:.9">TURMA 27</div>
<img src="{U(AQUI/'final/_manual/moletom-recorte.png')}" style="position:absolute;left:50%;top:30px;height:1060px;transform:translateX(-50%);filter:drop-shadow(0 40px 60px rgba(0,0,0,.8)) brightness(1.05)">
{nevoa(ROXO, 50, 95, 60, 20, .5)}{particulas(45, 1920, 1080, 9)}
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "kv06-celular": (1920, 1080, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 55% 70% at 50% 50%,#2A1838,{PRETO} 75%)"></div>{nevoa(ROXO, 50, 55, 45, 50, .5)}
<div style="position:absolute;left:560px;top:110px;width:400px;height:860px;border-radius:64px;background:#08070a;padding:16px;transform:rotate(-8deg);box-shadow:0 60px 90px rgba(0,0,0,.8),inset 0 0 0 3px #2b2630">
 <div style="width:100%;height:100%;border-radius:50px;overflow:hidden;position:relative;background:{PRETO}">
  <img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55">
  <div style="position:absolute;top:90px;width:100%;text-align:center;font-family:I;font-weight:900;font-size:96px;color:#fff;letter-spacing:-.04em">07:27</div>
  <img src="{U(R/'t27.png')}" style="position:absolute;left:40px;bottom:120px;width:290px"></div></div>
<div style="position:absolute;left:1000px;top:150px;width:400px;height:860px;border-radius:64px;background:#08070a;padding:16px;transform:rotate(6deg);box-shadow:0 60px 90px rgba(0,0,0,.8),inset 0 0 0 3px #2b2630">
 <div style="width:100%;height:100%;border-radius:50px;overflow:hidden;position:relative;background:radial-gradient(ellipse at 50% 40%,#2E1A40,{PRETO})">
  <img src="{U(AQUI/'final/arte-principal/terceirao-2027-principal-transparente.png')}" style="position:absolute;left:30px;top:120px;width:310px">
  <div class=lbl style="position:absolute;bottom:60px;width:100%;text-align:center;font-size:12px;color:{LILAS}">wallpaper oficial</div></div></div>
{particulas(40, 1920, 1080, 13)}<div class=fx vin></div><div class="fx grao"></div></body>"""),
    # --- posts 1080x1350 (estilo dot: título atrás do objeto, frase embaixo) ---
    "post01-ultimo-ano": (1080, 1350, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 70% 55% at 50% 55%,#33204A,{PRETO} 75%)"></div>{holofote(50, o=.22)}
<div class=lbl style="position:absolute;top:70px;width:100%;text-align:center;font-size:16px;color:{LILAS};opacity:.8">Terceirão · Mãe de Deus</div>
<div class=titulo style="left:0;right:0;top:130px;font-size:270px">ÚLTIMO<br>ANO.</div>
<img src="{U(R/'t27.png')}" style="position:absolute;left:90px;top:430px;width:900px;filter:drop-shadow(0 40px 50px rgba(0,0,0,.8))">
{nevoa(ROXO, 50, 92, 70, 18, .5)}{particulas(40, 1080, 1350, 21)}
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(0deg,{PRETO},transparent)"></div>
<div style="position:absolute;bottom:110px;width:100%;text-align:center;font-family:I;font-weight:900;font-size:34px;color:#fff;letter-spacing:-.01em">A gente não pichou a escola. <span style="color:{ROXO}">A gente assinou.</span></div>
<div class=lbl style="position:absolute;bottom:64px;width:100%;text-align:center;font-size:13px;color:#8d7f99">Turma 2027</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "post02-moletom": (1080, 1350, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 70% 60% at 50% 50%,#2E1A40,{PRETO} 75%)"></div>
<div class=titulo style="left:0;right:0;top:90px;font-size:200px">CHEGOU.</div>
<img src="{U(R/'arte3d.png')}" style="position:absolute;left:140px;top:300px;width:800px;filter:drop-shadow(0 40px 50px rgba(0,0,0,.8))">
{nevoa(ROXO, 50, 90, 70, 20, .5)}{particulas(40, 1080, 1350, 4)}
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(0deg,{PRETO},transparent)"></div>
<div style="position:absolute;bottom:110px;width:100%;text-align:center;font-family:I;font-weight:900;font-size:34px;color:#fff">O moletom da turma. <span style="color:{ROXO}">Pedidos até sexta.</span></div>
<div class=lbl style="position:absolute;bottom:64px;width:100%;text-align:center;font-size:13px;color:#8d7f99">Arraste →</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
    "post03-contagem": (1080, 1350, f"""<body>
<div class=fx style="background:radial-gradient(ellipse 70% 55% at 50% 45%,#2A1838,{PRETO} 75%)"></div>{holofote(50, o=.2)}
<div class=lbl style="position:absolute;top:110px;width:100%;text-align:center;font-size:18px;color:{LILAS}">Faltam</div>
<div class=titulo style="left:0;right:0;top:170px;font-size:520px">200</div>
<img src="{U(R/'botton27.png')}" style="position:absolute;left:300px;top:600px;width:480px;transform:rotate(-10deg);filter:drop-shadow(20px 40px 40px rgba(0,0,0,.8))">
{nevoa(ROXO, 50, 92, 70, 18, .5)}{particulas(40, 1080, 1350, 8)}
<div style="position:absolute;bottom:110px;width:100%;text-align:center;font-family:I;font-weight:900;font-size:34px;color:#fff">dias pra formatura. <span style="color:{ROXO}">Aproveita.</span></div>
<div class=lbl style="position:absolute;bottom:64px;width:100%;text-align:center;font-size:13px;color:#8d7f99">Turma 2027</div>
<div class=fx vin></div><div class="fx grao"></div></body>"""),
}

if __name__ == "__main__":
    for nome, (w, h, corpo) in CENAS.items():
        f = OUT / f"_{nome}.html"; f.write_text(f"<!doctype html><html><head><meta charset=utf-8>{BASE}</head>{corpo}</html>")
        subprocess.run(["node", str(AQUI.parent / "tools/html-to-png-exato.js"), str(f), str(OUT / f"{nome}.png"), str(w), str(h), "1"], check=True)
        f.unlink(); print("ok", nome)
