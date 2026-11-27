"""Manual de marca PREMIUM do Terceirão 2027 -> final/terceirao-2027-brandbook.pdf (1920x1080, ~22 págs)

Estrutura inspirada em brand books de grandes marcas (Nike, Spotify, Airbnb, streetwear):
capa, índice, manifesto, divisórias de capítulo, construção/área de proteção, versões, símbolo, tamanho mínimo,
cores (HEX/RGB/CMYK), tipografia, elementos gráficos, estampa corrida, usos incorretos, aplicações em foto e impressos, contracapa.
Tipografia do manual: Graffiti Youth (títulos), Inter (texto), Space Mono (rótulos técnicos).
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
F = AQUI / "final"; A = F / "aplicacoes"
U = lambda p: Path(p).resolve().as_uri()
FO = U(AQUI / "fontes")
ROXO, LILAS, ESC, UVA, PRETO, GELO = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353", "#0A0A0C", "#F4F1F7"
ART = U(F / "arte-principal/terceirao-2027-principal-transparente.png")
NEG = U(F / "negativo/terceirao-2027-principal-negativo-transparente.png")
S27, S27B = U(F / "simbolo/simbolo-27-roxo.png"), U(F / "simbolo/simbolo-27-branco.png")
PAT = U(F / "padrao/estampa-corrida-27.png")

CSS = f"""
@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:I;src:url('{FO}/inter-400.woff2');font-weight:400}}
@font-face{{font-family:I;src:url('{FO}/inter-700.woff2');font-weight:700}}
@font-face{{font-family:I;src:url('{FO}/inter-900.woff2');font-weight:900}}
@font-face{{font-family:M;src:url('{FO}/space-mono-400.woff2');font-weight:400}}
@font-face{{font-family:M;src:url('{FO}/space-mono-700.woff2');font-weight:700}}
@page{{size:1920px 1080px;margin:0}} *{{box-sizing:border-box;margin:0}}
body{{font-family:I;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:1920px;height:1080px;page-break-after:always;position:relative;overflow:hidden;background:{PRETO};color:#fff}}
.cl{{background:{GELO};color:{PRETO}}} .rx{{background:{ROXO};color:{PRETO}}}
.lbl{{font-family:M;font-size:15px;letter-spacing:.25em;text-transform:uppercase}}
.top{{position:absolute;left:96px;right:96px;top:64px;display:flex;justify-content:space-between;opacity:.6}}
.bot{{position:absolute;left:96px;right:96px;bottom:56px;display:flex;justify-content:space-between;opacity:.5}}
.h{{font-family:I;font-weight:900;font-size:88px;line-height:.95;letter-spacing:-.035em}}
.hg{{font-family:G;font-size:120px;line-height:.9;color:#fff;-webkit-text-stroke:18px {PRETO};paint-order:stroke fill;filter:drop-shadow(8px 10px 0 {ROXO})}}
.t{{font-size:21px;line-height:1.65;opacity:.75;max-width:520px}}
.rule{{height:2px;background:currentColor;opacity:.15}}
.box{{position:relative;border-radius:18px;overflow:hidden}} .box img{{display:block;width:100%;height:100%;object-fit:cover}}
.cap{{position:absolute;left:18px;bottom:16px;font-family:M;font-size:13px;letter-spacing:.2em;text-transform:uppercase;
      background:rgba(10,10,12,.72);color:#fff;padding:7px 11px;border-radius:6px}}
.brilho{{position:absolute;width:var(--s);height:var(--s);background:var(--c);clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
"""
pags = []
n = [0]
def pag(cls, corpo, secao=""):
    n[0] += 1
    pags.append(f'<div class="p {cls}"><div class="top lbl"><span>Terceirão 2027 · Brand Book</span><span>{secao}</span></div>'
                f'{corpo}<div class="bot lbl"><span>Colégio Mãe de Deus</span><span>{n[0]:02d}</span></div></div>')
def capitulo(num, nome, sub):
    pag("rx", f"""<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.18;mix-blend-mode:multiply">
<div style="position:absolute;left:96px;bottom:150px"><div class=lbl style="opacity:.7">Capítulo {num}</div>
<div class=h style="font-size:200px;margin-top:20px">{nome}</div><div class=t style="margin-top:24px;opacity:.8;max-width:700px">{sub}</div></div>
<div style="position:absolute;right:96px;top:120px;font-family:G;font-size:420px;line-height:1;color:{PRETO};opacity:.9">{num}</div>""", nome)
br = lambda l: "".join(f'<i class=brilho style="--s:{s}px;--c:{c};left:{x}px;top:{y}px"></i>' for x, y, s, c in l)

# 01 capa
pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 45% 75% at 72% 50%,#2E1B3E,{PRETO} 70%)"></div>
{br([(150,230,70,'#fff'),(1760,170,46,ROXO),(1790,880,58,'#fff'),(1010,960,34,ROXO)])}
<img src="{ART}" style="position:absolute;right:160px;top:70px;height:950px">
<div style="position:absolute;left:96px;top:300px"><div class=lbl style="color:{ROXO};opacity:1">Brand Book · Identidade Visual</div>
<div class=hg style="font-size:180px;margin-top:40px">TERCEIRÃO<br>2027</div>
<div class=lbl style="margin-top:60px;opacity:.6">Colégio Mãe de Deus · Turma de formandos</div></div>""", "Capa")
# 02 índice
itens = [("01", "Essência", "Manifesto e conceito"), ("02", "Marca", "Construção, versões, símbolo, mínimos"),
         ("03", "Cor & Tipo", "Paleta, códigos, fontes"), ("04", "Linguagem", "Elementos, estampa, usos incorretos"),
         ("05", "Aplicações", "Vestuário, impressos e digital")]
lista = "".join(f'<div style="display:grid;grid-template-columns:140px 1fr 1fr;align-items:baseline;padding:30px 0;border-top:2px solid rgba(255,255,255,.12)">'
                f'<span style="font-family:G;font-size:64px;color:{ROXO}">{a}</span><span class=h style="font-size:56px">{b}</span><span class=t>{c}</span></div>' for a, b, c in itens)
pag("", f'<div style="position:absolute;left:96px;right:96px;top:170px"><div class=lbl style="color:{ROXO};opacity:1;margin-bottom:30px">Índice</div>{lista}</div>', "Índice")
# capítulo 1
capitulo("01", "Essência", "O que essa marca é, de onde ela vem e o que ela precisa fazer sentir.")
pag("", f"""<div style="position:absolute;left:96px;top:190px;width:1000px">
<div class=lbl style="color:{ROXO};opacity:1">Manifesto</div>
<div class=h style="font-size:104px;margin-top:30px">A gente não<br>pichou a escola.<br><span style="color:{ROXO}">A gente assinou.</span></div>
<p class=t style="margin-top:50px;max-width:760px">O terceirão é o último muro antes do mundo. Essa marca é a nossa tag nele: grafite, não pixo. Letra gorda, cor da turma, tudo no mesmo plano, como um adesivo só. Feita pra durar mais que o ano.</p></div>
<img src="{U(A/'moletom-mockup-costas.png')}" style="position:absolute;right:96px;top:150px;height:780px;border-radius:24px">""", "Essência")
pag("cl", f"""<div style="position:absolute;left:96px;right:96px;top:200px;display:grid;grid-template-columns:repeat(3,1fr);gap:60px">
{''.join(f'<div><div style="font-family:G;font-size:110px;color:{ROXO};-webkit-text-stroke:12px {PRETO};paint-order:stroke fill">{a}</div><div class=h style="font-size:48px;margin-top:30px">{b}</div><div class=rule style="margin:26px 0"></div><p class=t>{c}</p></div>'
 for a, b, c in [("01", "Grafite, não pixo", "Letras legíveis, gordas e trabalhadas. Atitude de rua sem virar rabisco."), ("02", "Um adesivo só", "Todas as camadas no mesmo plano: contorno branco, contorno preto, recheio roxo, sombra uva."), ("03", "Nosso número", "O 27 é a assinatura da turma. Ele vive sozinho no boné, na manga e nas redes.")])}</div>""", "Conceito")
# capítulo 2
capitulo("02", "Marca", "Como a assinatura é construída, quais versões existem e como protegê-la.")
pag("", f"""<div style="position:absolute;left:96px;top:190px"><div class=lbl style="color:{ROXO};opacity:1">Assinatura principal</div>
<div class=h style="margin-top:24px">A tag da<br>turma.</div>
<p class=t style="margin-top:40px">TER / CEI / RÃO empilhado na fonte Graffiti Youth, til desenhado à mão, ano 27 emendado no RÃO e MÃE DE DEUS espaçado embaixo. Buracos das letras sempre brancos.</p>
<div class=lbl style="margin-top:50px;opacity:.5">Arquivo · final/arte-principal/</div></div>
<div style="position:absolute;right:96px;top:110px;width:900px;height:860px;border-radius:28px;background:radial-gradient(ellipse 60% 60% at 50% 50%,#24162F,#0E0B12)">
<img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:820px"></div>""", "Marca")
grade = "".join(f'<div style="position:absolute;left:{x}px;top:0;bottom:0;width:1px;background:rgba(153,107,179,.35)"></div>' for x in range(0, 821, 82)) + \
        "".join(f'<div style="position:absolute;top:{y}px;left:0;right:0;height:1px;background:rgba(153,107,179,.35)"></div>' for y in range(0, 985, 82))
pag("", f"""<div style="position:absolute;left:96px;top:190px"><div class=lbl style="color:{ROXO};opacity:1">Construção & área de proteção</div>
<div class=h style="margin-top:24px">Respira.</div>
<p class=t style="margin-top:40px">Em volta da assinatura fica sempre uma área livre igual à altura do "27" (medida <b>x</b>). Nada entra nesse espaço: texto, foto, outra marca ou borda.</p></div>
<div style="position:absolute;right:240px;top:70px;width:820px;height:940px">{grade}
<div style="position:absolute;inset:82px;border:3px dashed {ROXO};border-radius:8px"></div>
<img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:760px">
<span class=lbl style="position:absolute;left:20px;top:24px;color:{ROXO};opacity:1">x</span><span class=lbl style="position:absolute;right:20px;bottom:24px;color:{ROXO};opacity:1">x</span></div>""", "Construção")
V = [(ART, "Principal", PRETO, "Fundo preto ou escuro"), (NEG, "Negativo", GELO, "Fundo claro"),
     (U(F/"versoes-1cor/terceirao-1cor-branco.png"), "1 cor · branco", PRETO, "Serigrafia econômica"), (U(F/"versoes-1cor/terceirao-1cor-roxo.png"), "1 cor · roxo", PRETO, "Bordado / 1 tinta")]
pag("", f"""<div style="position:absolute;left:96px;top:150px" class=lbl><span style="color:{ROXO};opacity:1">Versões</span></div>
<div style="position:absolute;left:96px;right:96px;top:210px;bottom:120px;display:grid;grid-template-columns:repeat(4,1fr);gap:24px">
{''.join(f'<div class=box style="background:{bg};border:1px solid #2a2530"><img src="{s}" style="object-fit:contain;padding:40px 30px 90px"><span class=cap>{t} · {d}</span></div>' for s, t, bg, d in V)}</div>""", "Versões")
pag("cl", f"""<div style="position:absolute;left:96px;top:190px"><div class=lbl style="color:{ROXO};opacity:1">Símbolo</div>
<div class=h style="margin-top:24px">O 27<br>sozinho.</div>
<p class=t style="margin-top:40px">Quando a assinatura não cabe (boné, manga, ícone de perfil, botton), entra o símbolo 27. Mesma fonte do ano, mesmo acabamento.</p></div>
<div style="position:absolute;right:96px;top:150px;display:grid;grid-template-columns:1fr 1fr;gap:24px;width:1060px">
<div class=box style="height:390px;background:{PRETO}"><img src="{S27}" style="object-fit:contain;padding:40px"></div>
<div class=box style="height:390px;background:{PRETO}"><img src="{S27B}" style="object-fit:contain;padding:40px"></div>
<div class=box style="height:390px;background:{ROXO}"><img src="{U(F/'versoes-1cor/simbolo-27-1cor-preto.png')}" style="object-fit:contain;padding:40px"></div>
<div class=box style="height:390px;background:#fff"><img src="{S27}" style="object-fit:contain;padding:40px"></div></div>""", "Símbolo")
pag("", f"""<div style="position:absolute;left:96px;top:190px"><div class=lbl style="color:{ROXO};opacity:1">Tamanhos mínimos</div>
<div class=h style="margin-top:24px">Pequeno,<br>mas legível.</div></div>
<div style="position:absolute;left:96px;right:96px;bottom:150px;display:flex;align-items:flex-end;gap:90px">
{''.join(f'<div><img src="{s}" style="height:{h}px;display:block"><div class=lbl style="margin-top:20px">{t}</div></div>' for s, h, t in [(ART, 420, 'Estampa costas · 28–32 cm'), (ART, 200, 'Peito · mín. 8 cm'), (ART, 110, 'Digital · mín. 180 px'), (S27, 120, 'Símbolo · mín. 3 cm'), (S27, 60, 'Ícone · mín. 48 px')])}</div>""", "Mínimos")
# capítulo 3
capitulo("03", "Cor & Tipo", "Uma paleta curta e forte. Roxo da turma no comando, preto e branco de apoio.")
cores = [("Roxo turma", ROXO, "153 107 179", "40 60 0 0", "~ 2577 C"), ("Lilás", LILAS, "228 207 247", "8 16 0 0", "~ 263 C"),
         ("Roxo escuro", ESC, "122 76 153", "55 75 0 5", "~ 2587 C"), ("Uva", UVA, "62 35 83", "75 90 25 35", "~ 2627 C"),
         ("Branco", "#FFFFFF", "255 255 255", "0 0 0 0", "—"), ("Preto", PRETO, "10 10 12", "75 68 67 90", "Black 6 C")]
pag("", f"""<div style="position:absolute;left:96px;top:150px" class=lbl><span style="color:{ROXO};opacity:1">Paleta</span></div>
<div style="position:absolute;left:96px;right:96px;top:200px;bottom:120px;display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr 1fr 1fr;gap:18px">
{''.join(f'<div style="border-radius:20px;background:{c};border:1px solid #2a2530;position:relative;color:{"#0A0A0C" if c in (LILAS,"#FFFFFF") else "#fff"};padding:28px">'
         f'<div style="font-weight:900;font-size:28px">{nm}</div><div style="position:absolute;left:28px;bottom:28px;font-family:M;font-size:15px;line-height:1.8">HEX {c.upper()}<br>RGB {rgb}<br>CMYK {cm}<br>PMS {pms}</div></div>' for nm, c, rgb, cm, pms in cores)}</div>""", "Cores")
pag("", f"""<div style="position:absolute;left:96px;top:150px" class=lbl><span style="color:{ROXO};opacity:1">Proporção de uso</span></div>
<div style="position:absolute;left:96px;right:96px;top:220px;height:220px;display:flex;border-radius:20px;overflow:hidden">
<div style="flex:60;background:{PRETO};border:1px solid #2a2530"></div><div style="flex:25;background:{ROXO}"></div><div style="flex:10;background:#fff"></div><div style="flex:5;background:{LILAS}"></div></div>
<div style="position:absolute;left:96px;right:96px;top:470px;display:flex" class=lbl><span style="flex:60">Preto 60%</span><span style="flex:25">Roxo 25%</span><span style="flex:10">Branco 10%</span><span style="flex:5">5%</span></div>
<p class=t style="position:absolute;left:96px;top:600px;max-width:900px">O preto é o palco (o moletom), o roxo é a voz e o branco faz a letra saltar. O lilás aparece só em brilhos e degradês.</p>""", "Cores")
pag("", f"""<div style="position:absolute;left:96px;top:150px" class=lbl><span style="color:{ROXO};opacity:1">Tipografia</span></div>
<div style="position:absolute;left:96px;right:96px;top:210px;display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:60px">
<div><div style="font-family:G;font-size:260px;line-height:.9;color:{LILAS}">Aa</div><div class=h style="font-size:40px;margin-top:20px">Graffiti Youth</div><div class=lbl style="margin-top:10px">Assinatura · títulos de impacto</div>
<div style="font-family:G;font-size:46px;margin-top:30px;line-height:1.2">ABCDEFGHIJKLM<br>NOPQRSTUVWXYZ<br>0123456789</div></div>
<div><div style="font-family:I;font-weight:900;font-size:200px;line-height:1;letter-spacing:-.04em">Aa</div><div class=h style="font-size:40px;margin-top:40px">Inter</div><div class=lbl style="margin-top:10px">Texto · títulos limpos</div>
<p class=t style="margin-top:30px">Regular pra texto corrido, Black pra títulos editoriais. Leitura fácil do lado da letra de grafite.</p></div>
<div><div style="font-family:M;font-weight:700;font-size:170px;line-height:1.15">Aa</div><div class=h style="font-size:40px;margin-top:40px">Space Mono</div><div class=lbl style="margin-top:10px">Rótulos · datas · números técnicos</div>
<p class=t style="margin-top:30px">Sempre em maiúsculas e espaçada. Também serve Arial Bold espaçado (MÃE DE DEUS).</p></div></div>""", "Tipografia")
# capítulo 4
capitulo("04", "Linguagem", "Os elementos que acompanham a marca e o que nunca fazer com ela.")
pag("", f"""<div style="position:absolute;left:96px;top:190px"><div class=lbl style="color:{ROXO};opacity:1">Elementos gráficos</div>
<div class=h style="margin-top:24px">Brilhos,<br>til e 27.</div>
<p class=t style="margin-top:40px">Brilho de 4 pontas (branco e roxo) espalhado em volta, nunca em cima das letras. O til gordo e o 27 podem aparecer soltos como figurinhas.</p></div>
<div style="position:absolute;right:96px;top:170px;width:1000px;height:760px;border-radius:28px;background:#141018">
{br([(120,120,180,'#fff'),(420,160,110,ROXO),(640,90,70,'#fff'),(800,260,130,LILAS),(150,420,90,ROXO),(330,520,150,'#fff')])}
<img src="{S27}" style="position:absolute;right:60px;bottom:50px;width:420px"></div>""", "Elementos")
pag("", f"""<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
<div style="position:absolute;left:96px;bottom:130px;background:{PRETO};padding:40px 50px;border-radius:24px;border:2px solid {ROXO}">
<div class=lbl style="color:{ROXO};opacity:1">Estampa corrida</div><div class=h style="font-size:64px;margin-top:16px">Pattern 27</div>
<p class=t style="margin-top:16px;max-width:520px">Forro do capuz, fundo de credencial, papel de presente, wallpaper. Arquivo: final/padrao/.</p></div>""", "Estampa")
erros = [("errado-esticar", "Não esticar"), ("errado-cor", "Não trocar as cores"), ("errado-girar", "Não girar"),
         ("errado-fundo", "Não usar em fundo poluído"), ("errado-claro", "Versão principal no claro, não"), ("errado-transparencia", "Não aplicar transparência")]
pag("", f"""<div style="position:absolute;left:96px;top:150px" class=lbl><span style="color:#FA5F6D;opacity:1">Usos incorretos</span></div>
<div style="position:absolute;left:96px;right:96px;top:210px;bottom:120px;display:grid;grid-template-columns:repeat(6,1fr);gap:18px">
{''.join(f'<div><div class=box style="aspect-ratio:1"><img src="{U(F/"_manual"/(e+".png"))}"><div style="position:absolute;inset:0;background:linear-gradient(45deg,transparent 48.5%,#FA5F6D 48.5% 51.5%,transparent 51.5%)"></div></div><div class=lbl style="margin-top:18px;opacity:.8">✕ {t}</div></div>' for e, t in erros)}</div>""", "Usos incorretos")
# capítulo 5
capitulo("05", "Aplicações", "Onde a marca vive: no corpo, no papel e na tela.")
pag("cl", f'<img src="{U(A/"moletom-mockup.png")}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"><span class=cap style="left:96px;bottom:110px">Moletom · costas e peito</span>', "Vestuário")
pag("", f"""<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr">
<div class=box style="border-radius:0"><img src="{U(A/'camiseta-mockup.png')}"><span class=cap style="left:96px;bottom:110px">Camiseta oversized</span></div>
<div class=box style="border-radius:0"><img src="{U(A/'bone-mockup.png')}"><span class=cap style="bottom:110px">Boné · símbolo 27</span></div></div>""", "Vestuário")
pag("cl", f"""<div style="position:absolute;left:96px;right:96px;top:150px;bottom:120px;display:grid;grid-template-columns:1fr 1fr;gap:24px">
<div class=box><img src="{U(A/'09-convite.png')}"><span class=cap>Convite de formatura</span></div>
<div style="display:grid;grid-template-rows:1fr 1fr;gap:24px"><div class=box><img src="{U(A/'06-ingresso-formatura.png')}"><span class=cap>Ingresso do baile</span></div>
<div class=box><img src="{U(A/'05-faixa-turma.png')}"><span class=cap>Faixa da turma</span></div></div></div>""", "Impressos")
pag("", f"""<div style="position:absolute;left:96px;right:96px;top:150px;bottom:120px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px">
<div class=box><img src="{U(A/'08-credencial.png')}"><span class=cap>Credencial</span></div>
<div class=box><img src="{U(A/'04-adesivo.png')}"><span class=cap>Adesivo recortado</span></div>
<div class=box><img src="{U(A/'03-story-instagram.png')}"><span class=cap>Story · contagem</span></div></div>""", "Impressos & digital")
pag("", f"""<div style="position:absolute;left:96px;right:96px;top:200px"><div class=lbl style="color:{ROXO};opacity:1;margin-bottom:30px">Feed do Instagram</div>
<img src="{U(A/'07-posts-feed.png')}" style="width:100%;border-radius:20px;display:block"></div>""", "Digital")
# contracapa
pag("rx", f"""<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.18;mix-blend-mode:multiply">
<img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-52%);height:820px">""", "Fim")

html = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pags)}</body></html>"
h = F / "_brandbook.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);"
      "await p.pdf({path:process.argv[2],width:'1920px',height:'1080px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(F / "terceirao-2027-brandbook.pdf")], check=True)
h.unlink(); print("ok", n[0], "páginas")
