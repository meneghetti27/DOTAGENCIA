"""Manual de marca (versão final, mais caprichado): final/terceirao-2027-manual-de-marca.pdf
Também copia todos os arquivos finais pra final/ (artes, variações, negativos, aplicações, vetores).
"""
import shutil, subprocess
from pathlib import Path

AQUI = Path(__file__).parent
FIN = AQUI / "final"
for sub in ("arte-principal", "variacoes-ano", "negativo", "vetor"):
    (FIN / sub).mkdir(parents=True, exist_ok=True)
PNG = AQUI / "midiakit/png"
VARS = [("ano30-01", "27 branco"), ("ano30-03", "27 lilás"), ("ano30-07", "27 no canto"), ("ano30-11", "27 King Jack"),
        ("ano30-19", "2027 branco"), ("ano30-22", "2027 centro"), ("ano30-23", "2027 no canto"), ("ano30-30", "27 meio a meio")]
# --- organiza os arquivos finais ---
for suf in ("transparente", "fundo-preto"):
    shutil.copy(PNG / f"integrado-25-{suf}.png", FIN / "arte-principal" / f"terceirao-2027-principal-{suf}.png")
for suf in ("negativo", "negativo-transparente"):
    shutil.copy(PNG / f"integrado-25-{suf}.png", FIN / "negativo" / f"terceirao-2027-principal-{suf}.png")
for i, (n, cap) in enumerate(VARS, 1):
    slug = cap.replace(" ", "-").replace("á", "a")
    for suf, pasta in (("transparente", "variacoes-ano"), ("fundo-preto", "variacoes-ano"), ("negativo", "negativo"),
                       ("negativo-transparente", "negativo")):
        shutil.copy(PNG / f"{n}-{suf}.png", FIN / pasta / f"variacao-{i:02d}-{slug}-{suf}.png")
for f in (AQUI / "pdf").glob("costas-04-til26.*"):
    if f.suffix in (".svg", ".pdf", ".eps"):
        shutil.copy(f, FIN / "vetor" / f"terceirao-letras-vetor{f.suffix}")

U = lambda p: Path(p).resolve().as_uri()
FD = U(AQUI / "fontes/dafont")
A = FIN / "aplicacoes"
ROXO, CLARO, ESCURO, UVA, PRETO = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353", "#0A0A0C"

CSS = f"""
@font-face{{font-family:G;src:url('{FD}/graffiti_youth.otf')}}
@page{{size:1920px 1080px;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact}}
.p{{width:1920px;height:1080px;page-break-after:always;position:relative;overflow:hidden;background:{PRETO};color:#fff}}
.cl{{background:#F4F1F7;color:{PRETO}}}
.num{{position:absolute;right:90px;top:70px;font-family:G;font-size:90px;color:{ROXO};opacity:.25}}
.tag{{position:absolute;left:90px;top:80px;font-size:18px;letter-spacing:.45em;color:{ROXO};font-weight:700}}
.tit{{font-family:G;font-size:120px;line-height:.9;color:#fff;-webkit-text-stroke:18px {PRETO};paint-order:stroke fill;filter:drop-shadow(8px 10px 0 {ROXO})}}
.cl .tit{{color:{PRETO};-webkit-text-stroke:0;filter:none}}
.txt{{font-size:22px;line-height:1.7;color:#bdb3c8;max-width:560px}} .cl .txt{{color:#5d5566}}
.rod{{position:absolute;left:90px;bottom:50px;right:90px;display:flex;justify-content:space-between;font-size:14px;letter-spacing:.35em;color:#5d5366}}
.cl .rod{{color:#9a92a5}}
.brilho{{position:absolute;width:var(--s);height:var(--s);background:var(--c);clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
.card{{border-radius:22px;overflow:hidden;background:#141018;position:relative}} .card img{{display:block;width:100%;height:100%;object-fit:contain}}
.cap{{position:absolute;left:16px;bottom:12px;font-size:14px;letter-spacing:.2em;color:#d9cfe3;background:rgba(10,10,12,.6);padding:6px 10px;border-radius:8px}}
.cl .card{{background:#fff;box-shadow:0 10px 30px rgba(62,35,83,.08)}} .cl .cap{{background:rgba(255,255,255,.8);color:#5d5566}}
"""
rod = lambda n, t: f'<div class=rod><span>TERCEIRÃO 2027 · MÃE DE DEUS</span><span>{n:02d} · {t}</span></div>'
br = lambda l: "".join(f'<i class=brilho style="--s:{s}px;--c:{c};left:{x}px;top:{y}px"></i>' for x, y, s, c in l)
img = lambda p: U(p)

pags = []
# 1 capa
pags.append(f"""<div class=p style="background:radial-gradient(ellipse 55% 70% at 70% 50%,#2A1838,{PRETO} 70%)">
{br([(140,180,90,"#fff"),(1780,160,60,ROXO),(1700,900,70,"#fff"),(980,980,40,ROXO)])}
<img src="{img(FIN/'arte-principal/terceirao-2027-principal-transparente.png')}" style="position:absolute;right:120px;top:40px;height:1000px">
<div style="position:absolute;left:120px;top:300px"><div class=tag style="position:static;margin-bottom:40px">MANUAL DE MARCA</div>
<div class=tit style="font-size:170px">TERCEIRÃO<br>2027</div>
<div style="font-size:28px;letter-spacing:.5em;color:{ROXO};margin-top:50px;font-weight:700">COLÉGIO MÃE DE DEUS</div></div>
{rod(1,'CAPA')}</div>""")
# 2 conceito
pags.append(f"""<div class=p><div class=tag>CONCEITO</div><div class=num>02</div>
<div style="position:absolute;left:90px;top:200px"><div class=tit>GRAFITE,<br>NÃO PIXO.</div>
<p class=txt style="margin-top:50px">Uma marca com cara de muro: letras de bloco gordas, recheio roxo em degradê, contorno preto,
linha branca por fora e sombra 3D, tudo no mesmo plano, como um adesivo só. O ano entra emendado no RÃO, como uma assinatura.</p>
<p class=txt>Moletom preto. Roxo da turma como cor principal.</p></div>
<img src="{img(A/'moletom-mockup-costas.png')}" style="position:absolute;right:90px;top:120px;height:860px;border-radius:28px">
{rod(2,'CONCEITO')}</div>""")
# 3 arte principal
pags.append(f"""<div class=p style="background:radial-gradient(ellipse 50% 60% at 35% 50%,#24162F,{PRETO} 70%)"><div class=tag>ARTE PRINCIPAL</div><div class=num>03</div>
<img src="{img(FIN/'arte-principal/terceirao-2027-principal-transparente.png')}" style="position:absolute;left:220px;top:60px;height:960px">
<div style="position:absolute;left:1120px;top:260px"><div class=tit style="font-size:90px">COSTAS DO<br>MOLETOM</div>
<p class=txt style="margin-top:40px">TER / CEI / RÃO empilhado · til desenhado à mão · ano 27 emendado · MÃE DE DEUS espaçado.</p>
<p class=txt>Buracos das letras sempre brancos, com uma linha preta fina em volta.</p>
<p style="font-size:16px;letter-spacing:.2em;color:#7d7389;margin-top:40px">ARQUIVOS: final/arte-principal/ · final/vetor/</p></div>
{rod(3,'ARTE PRINCIPAL')}</div>""")
# 4 mockup
pags.append(f"""<div class="p cl"><div class=tag>APLICAÇÃO · MOLETOM</div><div class=num>04</div>
<img src="{img(A/'moletom-mockup.png')}" style="position:absolute;left:50%;top:150px;transform:translateX(-50%);width:1700px">
<p class=txt style="position:absolute;left:90px;bottom:110px;max-width:900px">Costas: arte principal grande. Peito esquerdo: a mesma arte em tamanho pequeno.</p>
{rod(4,'MOLETOM')}</div>""")
# 5 variações do ano
cards = "".join(f'<div class=card style="height:400px"><img src="{img(FIN/"variacoes-ano"/f"variacao-{i:02d}-{c.replace(" ","-").replace("á","a")}-fundo-preto.png")}"><span class=cap>{i:02d} · {c.upper()}</span></div>'
                for i, (n, c) in enumerate(VARS, 1))
pags.append(f"""<div class=p><div class=tag>VARIAÇÕES DO ANO</div><div class=num>05</div>
<div style="position:absolute;left:90px;right:90px;top:160px;display:grid;grid-template-columns:repeat(4,1fr);gap:24px">{cards}</div>
{rod(5,'VARIAÇÕES')}</div>""")
# 6 negativo
cards = "".join(f'<div class=card style="height:400px"><img src="{img(FIN/"negativo"/f"variacao-{i:02d}-{c.replace(" ","-").replace("á","a")}-negativo.png")}"><span class=cap>{i:02d} · {c.upper()}</span></div>'
                for i, (n, c) in enumerate(VARS[:4], 1))
pags.append(f"""<div class="p cl"><div class=tag>VERSÃO NEGATIVO · FUNDO CLARO</div><div class=num>06</div>
<img src="{img(FIN/'negativo/terceirao-2027-principal-negativo-transparente.png')}" style="position:absolute;left:90px;top:150px;height:860px">
<div style="position:absolute;left:820px;right:90px;top:170px;display:grid;grid-template-columns:repeat(2,1fr);gap:24px">{cards}</div>
{rod(6,'NEGATIVO')}</div>""")
# 7 cores
sw = [("ROXO TURMA", ROXO, "153 · 107 · 179"), ("LILÁS", CLARO, "228 · 207 · 247"), ("ROXO ESCURO", ESCURO, "122 · 76 · 153"),
      ("UVA", UVA, "62 · 35 · 83"), ("BRANCO", "#FFFFFF", "255 · 255 · 255"), ("PRETO", PRETO, "10 · 10 · 12")]
sws = "".join(f'<div><div style="height:420px;border-radius:24px;background:{c};border:2px solid #2a2530"></div>'
              f'<div style="font-size:22px;font-weight:700;margin-top:18px">{n}</div><div style="font-family:monospace;font-size:20px;color:#a59bb0">{c.upper()}</div>'
              f'<div style="font-size:15px;color:#6d6478;margin-top:4px">RGB {r}</div></div>' for n, c, r in sw)
pags.append(f"""<div class=p><div class=tag>CORES</div><div class=num>07</div>
<div style="position:absolute;left:90px;right:90px;top:200px;display:grid;grid-template-columns:repeat(6,1fr);gap:26px">{sws}</div>
{rod(7,'CORES')}</div>""")
# 8 tipografia
pags.append(f"""<div class=p><div class=tag>TIPOGRAFIA</div><div class=num>08</div>
<div style="position:absolute;left:90px;top:190px;right:90px;display:grid;grid-template-columns:1.3fr 1fr;gap:80px">
<div><div style="font-family:G;font-size:200px;line-height:1;color:{CLARO}">Aa</div><div style="font-family:G;font-size:56px;color:#fff;margin-top:20px">ABCDEFGHIJKLM<br>NOPQRSTUVWXYZ 0123456789</div>
<p class=txt style="margin-top:30px"><b style="color:#fff">Graffiti Youth</b> · letras principais (TERCEIRÃO). <b style="color:#fff">Grime Slime</b> · ano (27 / 2027).</p></div>
<div><div style="font-size:120px;font-weight:700;letter-spacing:.3em;color:{ROXO};line-height:1">MÃE</div>
<p class=txt style="margin-top:30px"><b style="color:#fff">Arial Bold</b>, maiúsculas, espaçamento largo · textos de apoio (MÃE DE DEUS).</p>
<p class=txt style="font-size:17px;color:#8d7f99">Fontes do dafont: grátis só pra uso pessoal. Pra vender o moletom, comprar a licença comercial com o autor.</p></div></div>
{rod(8,'TIPOGRAFIA')}</div>""")
# 9 aplicações
ap = [("03-story-instagram.png", "STORY"), ("04-adesivo.png", "ADESIVO"), ("05-faixa-turma.png", "FAIXA"), ("06-ingresso-formatura.png", "INGRESSO")]
pags.append(f"""<div class="p cl"><div class=tag>OUTRAS APLICAÇÕES</div><div class=num>09</div>
<div style="position:absolute;left:90px;right:90px;top:160px;bottom:110px;display:grid;grid-template-columns:420px 1fr 1fr;grid-template-rows:1fr 1fr;gap:24px">
<div class=card style="grid-row:span 2"><img src="{img(A/ap[0][0])}" style="object-fit:cover"><span class=cap>STORY</span></div>
<div class=card><img src="{img(A/ap[1][0])}"><span class=cap>ADESIVO</span></div>
<div class=card><img src="{img(A/ap[3][0])}" style="object-fit:cover"><span class=cap>INGRESSO</span></div>
<div class=card style="grid-column:span 2"><img src="{img(A/ap[2][0])}" style="object-fit:cover"><span class=cap>FAIXA DA TURMA</span></div></div>
{rod(9,'APLICAÇÕES')}</div>""")
# 10 usos
pags.append(f"""<div class=p><div class=tag>BOM USO</div><div class=num>10</div>
<div style="position:absolute;left:90px;right:90px;top:200px;display:grid;grid-template-columns:1fr 1fr;gap:80px;font-size:24px;line-height:2;color:#cfc6d9">
<div><b style="color:{ROXO};letter-spacing:.3em">FAZER</b><br>✓ Usar a arte principal em fundo preto<br>✓ Versão negativo em fundo claro<br>✓ Manter a área de respiro em volta (≈ altura do 27)<br>✓ Estampar o PNG transparente ou o vetor</div>
<div><b style="color:#FA5F6D;letter-spacing:.3em">NÃO FAZER</b><br>✗ Esticar ou achatar a arte<br>✗ Trocar as cores das letras<br>✗ Usar a versão de contorno branco em fundo claro<br>✗ Separar as linhas TER / CEI / RÃO</div></div>
{rod(10,'BOM USO')}</div>""")

html = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pags)}</body></html>"
h = FIN / "_marca.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1200);"
      "await p.pdf({path:process.argv[2],width:'1920px',height:'1080px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(FIN / "terceirao-2027-manual-de-marca.pdf")], check=True)
h.unlink(); print("ok")
