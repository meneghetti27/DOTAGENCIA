"""BRAND BOOK v3 — institucional e visual -> final/terceirao-2027-brandbook.pdf
Feedback do dono: sem "muro/pixo", capa institucional (degradê roxo + letra branca destacada), pouco texto,
sem processo/ajuste fino/til/espaço/voz/brilhos/bottons/celular/posts/chaveiro/caderno/bandeira; adesivo colado em superfícies reais.
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
F = AQUI / "final"; A = F / "aplicacoes"; KV = F / "keyvisuals"; M = F / "_manual"
U = lambda p: Path(p).resolve().as_uri()
FO = U(AQUI / "fontes")
ROXO, LILAS, ESC, UVA, PRETO = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353", "#0A0A0C"
ART = U(F / "arte-principal/terceirao-2027-principal-transparente.png")
BRANCO = U(F / "versoes-1cor/terceirao-1cor-branco.png")
NEG = U(F / "negativo/terceirao-2027-principal-negativo-transparente.png")
S27, S27B = U(F / "simbolo/simbolo-27-roxo.png"), U(F / "simbolo/simbolo-27-branco.png")
GRAD = f"linear-gradient(135deg,#1C1026 0%,{UVA} 30%,{ESC} 62%,{ROXO} 85%,#B48ACB 100%)"

CSS = f"""
@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:I;src:url('{FO}/inter-400.woff2');font-weight:400}}
@font-face{{font-family:I;src:url('{FO}/inter-700.woff2');font-weight:700}}
@font-face{{font-family:I;src:url('{FO}/inter-900.woff2');font-weight:900}}
@font-face{{font-family:M;src:url('{FO}/space-mono-400.woff2')}}
@page{{size:1920px 1080px;margin:0}} *{{box-sizing:border-box;margin:0}}
body{{font-family:I;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:1920px;height:1080px;page-break-after:always;position:relative;overflow:hidden;background:{PRETO};color:#fff}}
.g{{background:{GRAD}}}
.lbl{{font-family:M;font-size:14px;letter-spacing:.3em;text-transform:uppercase}}
.top{{position:absolute;left:100px;right:100px;top:60px;display:flex;justify-content:space-between;opacity:.5;z-index:5}}
.h{{font-weight:900;font-size:84px;line-height:.95;letter-spacing:-.04em}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.chip{{position:absolute;left:100px;bottom:80px;z-index:5}}
"""
pags, n = [], [0]
def pag(cls, corpo, sec=""):
    n[0] += 1
    top = f'<div class="top lbl"><span>Terceirão 2027</span><span>{sec} · {n[0]:02d}</span></div>' if sec else ""
    pags.append(f'<div class="p {cls}">{corpo}{top}</div>')
def titulo(txt, sub=""):
    return f'<div style="position:absolute;left:100px;top:150px"><div class=h>{txt}</div>{f"<div class=lbl style=margin-top:22px;opacity:.6>{sub}</div>" if sub else ""}</div>'
def cena(img, sec, legenda=""):
    pag("", f'<img class=full src="{U(img)}">' + (f'<div class="chip lbl" style="opacity:.75">{legenda}</div>' if legenda else ""), sec)
def divisoria(num, nome):
    pag("g", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 85% 20%,rgba(228,207,247,.35),transparent 60%)"></div>
<div class=lbl style="position:absolute;left:100px;top:150px;opacity:.75">{num}</div>
<div class=h style="position:absolute;left:96px;bottom:110px;font-size:190px">{nome}</div>""")

# 01 capa institucional: degradê roxo + letra branca destacada
pag("g", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 55% 75% at 78% 45%,rgba(228,207,247,.32),transparent 65%)"></div>
<img src="{BRANCO}" style="position:absolute;right:170px;top:110px;height:860px;filter:drop-shadow(0 30px 60px rgba(30,10,45,.45))">
<div style="position:absolute;left:100px;top:110px" class=lbl>Manual de Marca</div>
<div style="position:absolute;left:96px;bottom:170px"><div class=h style="font-size:150px">Terceirão<br>2027</div>
<div class=lbl style="margin-top:40px;opacity:.85">Colégio Mãe de Deus</div></div>""")
# 02 sumário
itens = [("01", "Marca"), ("02", "Cores"), ("03", "Tipografia"), ("04", "Aplicações")]
pag("", f"""<div style="position:absolute;left:100px;top:150px" class=lbl>Sumário</div>
<div style="position:absolute;left:100px;right:100px;bottom:120px">{''.join(f'<div style="display:flex;align-items:baseline;gap:60px;padding:30px 0;border-top:1px solid rgba(255,255,255,.14)"><span class=lbl style="color:{ROXO}">{a}</span><span class=h style="font-size:72px">{b}</span></div>' for a, b in itens)}</div>""")
# MARCA
divisoria("01", "Marca")
pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 45% 65% at 50% 50%,#2A1838,{PRETO} 72%)"></div>
<img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:900px">""", "Assinatura")
cena(KV / "kv01-heroi.png", "Assinatura")
V = [(ART, "Principal", PRETO), (NEG, "Negativo", "#F2EEF5"), (BRANCO, "Uma cor", "#141018"), (U(F / "versoes-1cor/terceirao-1cor-roxo.png"), "Uma cor", "#141018")]
pag("", titulo("Versões") + f"""<div style="position:absolute;left:100px;right:100px;top:330px;bottom:110px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px">{''.join(
 f'<div style="background:{b};position:relative;border-radius:6px"><img src="{s}" style="position:absolute;inset:50px 40px 80px;width:calc(100% - 80px);height:calc(100% - 130px);object-fit:contain"><div class=lbl style="position:absolute;left:30px;bottom:28px;color:{"#0A0A0C" if b != PRETO and b != "#141018" else "#fff"};opacity:.7">{t}</div></div>' for s, t, b in V)}</div>""", "Marca")
pag("", titulo("Símbolo") + f"""<div style="position:absolute;left:100px;right:100px;top:330px;bottom:110px;display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:20px">
<div style="background:radial-gradient(ellipse at 50% 45%,#2A1838,#0E0B12);border-radius:6px;position:relative"><img src="{S27}" style="position:absolute;inset:80px;width:calc(100% - 160px);height:calc(100% - 160px);object-fit:contain"></div>
<div style="background:{GRAD};border-radius:6px;position:relative"><img src="{S27B}" style="position:absolute;inset:50px;width:calc(100% - 100px);height:calc(100% - 100px);object-fit:contain"></div>
<div style="background:#F2EEF5;border-radius:6px;position:relative"><img src="{S27}" style="position:absolute;inset:50px;width:calc(100% - 100px);height:calc(100% - 100px);object-fit:contain"></div></div>""", "Marca")
pag("", titulo("Tamanho mínimo") + f"""<div style="position:absolute;left:100px;right:100px;bottom:130px;display:flex;align-items:flex-end;justify-content:space-between">{''.join(
 f'<div><img src="{s}" style="height:{h}px;display:block"><div class=lbl style="margin-top:24px;opacity:.6">{t}</div></div>' for s, h, t in
 [(ART, 460, "30 cm"), (ART, 220, "8 cm"), (ART, 110, "180 px"), (S27, 120, "3 cm"), (S27, 56, "48 px")])}</div>""", "Marca")
erros = ["errado-esticar", "errado-cor", "errado-girar", "errado-fundo", "errado-claro", "errado-transparencia"]
pag("", titulo("Não fazer") + f"""<div style="position:absolute;left:100px;right:100px;top:330px;bottom:110px;display:grid;grid-template-columns:repeat(6,1fr);gap:16px;align-content:center">{''.join(
 f'<div style="position:relative;aspect-ratio:1;border-radius:6px;overflow:hidden"><img class=full src="{U(M/(e+".png"))}"><i style="position:absolute;inset:0;background:linear-gradient(45deg,transparent 49.2%,#FA5F6D 49.2% 50.8%,transparent 50.8%)"></i></div>' for e in erros)}</div>""", "Marca")
# CORES (apresentação premium: cartões grandes em degradê)
divisoria("02", "Cores")
cores = [("Roxo turma", ROXO, "153 · 107 · 179", "40 · 60 · 0 · 0", "≈ 2577 C", f"linear-gradient(160deg,#B48ACB,{ROXO} 45%,{ESC})"),
         ("Uva", UVA, "62 · 35 · 83", "75 · 90 · 25 · 35", "≈ 2627 C", f"linear-gradient(160deg,#5A3A78,{UVA} 55%,#24132F)"),
         ("Lilás", LILAS, "228 · 207 · 247", "8 · 16 · 0 · 0", "≈ 263 C", f"linear-gradient(160deg,#F6EEFD,{LILAS} 60%,#CDB2E6)"),
         ("Preto", PRETO, "10 · 10 · 12", "75 · 68 · 67 · 90", "Black 6 C", "linear-gradient(160deg,#2A2530,#0A0A0C 55%)"),
         ("Branco", "#FFFFFF", "255 · 255 · 255", "0 · 0 · 0 · 0", "—", "linear-gradient(160deg,#FFFFFF,#ECE7F1)")]
pag("", f"""<div style="position:absolute;left:100px;right:100px;top:150px;bottom:110px;display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1fr;gap:18px">{''.join(
 f'<div style="background:{gr};border-radius:18px;position:relative;box-shadow:0 30px 60px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.25);color:{"#0A0A0C" if c in (LILAS, "#FFFFFF") else "#fff"}">'
 f'<div class=h style="position:absolute;left:34px;top:34px;font-size:{44 if i == 0 else 30}px">{nm}</div>'
 f'<div style="position:absolute;left:34px;bottom:34px;font-family:M;font-size:14px;line-height:2;opacity:.85"><b style="font-family:I;font-weight:900;font-size:{40 if i == 0 else 26}px;letter-spacing:-.02em;display:block;margin-bottom:10px">{c.upper()}</b>RGB {r}<br>CMYK {cm}<br>PMS {p}</div></div>' for i, (nm, c, r, cm, p, gr) in enumerate(cores))}</div>""", "Cores")
pag("", f"""<div style="position:absolute;inset:0;display:flex"><div style="flex:60;background:{PRETO}"></div><div style="flex:25;background:{GRAD}"></div><div style="flex:10;background:#fff"></div><div style="flex:5;background:{LILAS}"></div></div>
<div style="position:absolute;left:100px;bottom:90px;display:flex;gap:0;width:1720px" class=lbl><span style="flex:60">Preto 60%</span><span style="flex:25">Roxo 25%</span><span style="flex:10;color:#0A0A0C">10%</span><span style="flex:5;color:#0A0A0C">5%</span></div>""", "Cores")
# TIPOGRAFIA
divisoria("03", "Tipografia")
pag("", f"""<div style="position:absolute;left:100px;right:100px;top:180px;display:grid;grid-template-columns:1fr 1fr;gap:100px">
<div><div style="font-family:G;font-size:340px;line-height:.85;color:{LILAS}">Aa</div><div class=h style="font-size:46px;margin-top:40px">Graffiti Youth</div><div class=lbl style="margin-top:14px;opacity:.55">Assinatura</div>
<div style="font-family:G;font-size:46px;margin-top:40px;line-height:1.25">ABCDEFGHIJKLMN<br>OPQRSTUVWXYZ 0123456789</div></div>
<div><div style="font-weight:900;font-size:300px;line-height:.85;letter-spacing:-.05em">Aa</div><div class=h style="font-size:46px;margin-top:60px">Inter</div><div class=lbl style="margin-top:14px;opacity:.55">Textos e títulos</div>
<div style="font-weight:900;font-size:46px;margin-top:40px;line-height:1.25;letter-spacing:-.02em">ABCDEFGHIJKLMN<br>OPQRSTUVWXYZ 0123456789</div></div></div>""", "Tipografia")
# APLICAÇÕES
divisoria("04", "Aplicações")
cena(KV / "kv05-moletom.png", "Aplicações")
pag("", f'<div style="position:absolute;inset:0;background:#fff"></div><img src="{U(A/"moletom-mockup.png")}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1800px">', "Aplicações")
cena(A / "camiseta-mockup.png", "Aplicações")
for nome in ["ad1-muro-concreto", "ad2-muro-tijolo", "ad3-mesa-madeira", "ad4-asfalto"]:
    cena(KV / f"{nome}.png", "Adesivos")
cena(KV / "kv09-adesivos.png", "Adesivos")
cena(KV / "kv07-canecas.png", "Aplicações")
cena(KV / "kv16-pulseiras.png", "Aplicações")
cena(KV / "kv17-impressos.png", "Aplicações")
cena(KV / "kv13-neon.png", "Aplicações")
cena(KV / "kv14-telao.png", "Aplicações")
# contracapa
pag("g", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 50% 70% at 50% 45%,rgba(228,207,247,.3),transparent 65%)"></div>
<img src="{BRANCO}" style="position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);height:760px">
<div class=lbl style="position:absolute;width:100%;bottom:90px;text-align:center;opacity:.8">Terceirão 2027 · Colégio Mãe de Deus</div>""")

html = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pags)}</body></html>"
h = F / "_bb3.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);"
      "await p.pdf({path:process.argv[2],width:'1920px',height:'1080px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(F / "terceirao-2027-brandbook.pdf")], check=True)
h.unlink(); print("ok", n[0], "páginas")
