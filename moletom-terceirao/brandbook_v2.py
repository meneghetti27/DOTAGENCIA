"""BRAND BOOK v2 — editorial / conceitual -> final/terceirao-2027-brandbook.pdf

Narrativa em 5 capítulos: I O Muro (essência) · II A Tag (marca) · III A Cor · IV A Voz (tipo + linguagem) · V A Rua (aplicações).
Recursos: grão em todas as páginas, atmosfera roxa, páginas de processo (das 150 fontes à letra final), anatomia da assinatura,
closes de detalhe, citações em serifa itálica, voz da marca, calendário do ano, fotos sangradas.
"""
import subprocess
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).parent
F = AQUI / "final"; A = F / "aplicacoes"; M = F / "_manual"; M.mkdir(exist_ok=True)
U = lambda p: Path(p).resolve().as_uri()
FO = U(AQUI / "fontes")
ROXO, LILAS, ESC, UVA, PRETO, GELO = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353", "#0A0A0C", "#F2EEF5"
ARTp = F / "arte-principal/terceirao-2027-principal-transparente.png"
ART, NEG = U(ARTp), U(F / "negativo/terceirao-2027-principal-negativo-transparente.png")
S27, S27B = U(F / "simbolo/simbolo-27-roxo.png"), U(F / "simbolo/simbolo-27-branco.png")
PAT = U(F / "padrao/estampa-corrida-27.png")

# --- imagens auxiliares ---
art = Image.open(ARTp).convert("RGBA")
bg = Image.new("RGBA", art.size, PRETO); bg.alpha_composite(art)
bg.crop((330, 820, 1330, 1620)).save(M / "close-rao.png")            # close no RÃO + til + 27
bg.crop((200, 120, 1000, 640)).save(M / "close-ter.png")             # close no TER
atm = Image.open(AQUI / "referencias/mockups/bone-preto.jpg").convert("RGB").crop((0, 0, 1376, 300)).resize((1920, 1080))
atm.save(M / "atmosfera.jpg", quality=90)

GRAO = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'>"
        "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter>"
        "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
CSS = f"""
@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:I;src:url('{FO}/inter-400.woff2');font-weight:400}}
@font-face{{font-family:I;src:url('{FO}/inter-700.woff2');font-weight:700}}
@font-face{{font-family:I;src:url('{FO}/inter-900.woff2');font-weight:900}}
@font-face{{font-family:M;src:url('{FO}/space-mono-400.woff2');font-weight:400}}
@font-face{{font-family:M;src:url('{FO}/space-mono-700.woff2');font-weight:700}}
@font-face{{font-family:S;src:url('{FO}/playfair-display-400-italic.woff2');font-style:italic}}
@page{{size:1920px 1080px;margin:0}} *{{box-sizing:border-box;margin:0}}
body{{font-family:I;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:1920px;height:1080px;page-break-after:always;position:relative;overflow:hidden;background:{PRETO};color:#EDE7F2}}
.p::after{{content:"";position:absolute;inset:0;background:url("{GRAO}");opacity:.07;pointer-events:none;mix-blend-mode:overlay}}
.cl{{background:{GELO};color:{PRETO}}} .cl::after{{opacity:.12;mix-blend-mode:multiply}} .rx{{background:{ROXO};color:{PRETO}}}
.lbl{{font-family:M;font-size:14px;letter-spacing:.28em;text-transform:uppercase}}
.top{{position:absolute;left:110px;right:110px;top:60px;display:flex;justify-content:space-between;opacity:.45;z-index:5}}
.bot{{position:absolute;left:110px;right:110px;bottom:52px;display:flex;justify-content:space-between;opacity:.45;z-index:5}}
.h{{font-family:I;font-weight:900;font-size:96px;line-height:.92;letter-spacing:-.04em}}
.s{{font-family:S;font-style:italic;font-weight:400;letter-spacing:-.01em}}
.hg{{font-family:G;line-height:.88;color:#fff;-webkit-text-stroke:.15em {PRETO};paint-order:stroke fill;filter:drop-shadow(.05em .06em 0 {ROXO})}}
.t{{font-size:20px;line-height:1.7;opacity:.72;max-width:500px}}
.k{{color:{ROXO}}} .rule{{height:1px;background:currentColor;opacity:.18}}
.img{{position:absolute;overflow:hidden}} .img img{{width:100%;height:100%;object-fit:cover;display:block}}
.cap{{font-family:M;font-size:12px;letter-spacing:.22em;text-transform:uppercase;opacity:.55;margin-top:14px}}
.br{{position:absolute;width:var(--s);height:var(--s);background:var(--c);clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
.pin{{position:absolute;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 0 0 6px rgba(153,107,179,.45)}}
.ln{{position:absolute;height:1px;background:rgba(237,231,242,.5);transform-origin:0 0}}
.tag{{position:absolute;font-family:M;font-size:13px;letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}}
"""
pags, cnt = [], [0]
def pag(cls, corpo, secao="", rod=True):
    cnt[0] += 1
    t = (f'<div class="top lbl"><span>Terceirão 2027</span><span>{secao}</span></div>'
         f'<div class="bot lbl"><span>Brand Book — Colégio Mãe de Deus</span><span>{cnt[0]:02d}</span></div>') if rod else ""
    pags.append(f'<div class="p {cls}">{corpo}{t}</div>')
br = lambda l: "".join(f'<i class=br style="--s:{s}px;--c:{c};left:{x}px;top:{y}px"></i>' for x, y, s, c in l)
def capitulo(rom, nome, frase):
    pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 55% at 70% 0%,#3A2350 0%,#160F1C 45%,{PRETO} 75%)"></div>
<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.07">
<div style="position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(0deg,{PRETO},transparent)"></div>
<div style="position:absolute;left:110px;top:150px" class="lbl k">Capítulo {rom}</div>
<div class=hg style="position:absolute;left:100px;top:300px;font-size:300px">{nome}</div>
<div class=s style="position:absolute;left:115px;bottom:150px;font-size:44px;max-width:900px;opacity:.85">{frase}</div>
<div style="position:absolute;right:110px;bottom:140px;font-family:S;font-style:italic;font-size:220px;opacity:.12">{rom}</div>""", nome.title())

# ============ ABERTURA ============
pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 42% 70% at 70% 52%,#2D1A3C,{PRETO} 72%)"></div>
{br([(160,250,56,'#fff'),(1750,190,38,ROXO),(1780,860,48,'#fff'),(1060,940,26,LILAS)])}
<img src="{ART}" style="position:absolute;right:190px;top:80px;height:930px">
<div style="position:absolute;left:110px;top:120px" class="lbl k">Brand Book · Edição 01</div>
<div style="position:absolute;left:110px;bottom:220px"><div class=s style="font-size:40px;opacity:.7">a identidade da turma</div>
<div class=hg style="font-size:200px;margin-top:20px">TERCEIRÃO</div>
<div style="display:flex;gap:40px;margin-top:40px" class=lbl><span>2027</span><span style="opacity:.5">—</span><span>Colégio Mãe de Deus</span></div></div>""", rod=False)
pag("", f"""<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;width:1300px">
<div class=s style="font-size:76px;line-height:1.2">“Todo muro guarda o nome<br>de quem <span class=k>passou</span> por ele.”</div>
<div class=lbl style="margin-top:60px;opacity:.5">— Ponto de partida desta identidade</div></div>""", "Abertura")
idx = [("I", "O Muro", "Essência, manifesto, valores", "04"), ("II", "A Tag", "Processo, assinatura, anatomia, versões", "08"),
       ("III", "A Cor", "Roxo da turma, paleta, proporção", "19"), ("IV", "A Voz", "Tipografia, tom, elementos, usos", "23"),
       ("V", "A Rua", "Vestuário, impressos, digital, calendário", "30")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Sumário</div>
<div style="position:absolute;left:110px;right:110px;top:230px">{''.join(
 f'<div style="display:grid;grid-template-columns:150px 620px 1fr 80px;align-items:baseline;padding:34px 0;border-top:1px solid rgba(237,231,242,.15)">'
 f'<span class=s style="font-size:54px;color:{ROXO}">{a}</span><span class=h style="font-size:62px">{b}</span><span class=t style="max-width:none">{c}</span><span class=lbl style="text-align:right">{d}</span></div>' for a, b, c, d in idx)}</div>""", "Sumário")

# ============ I · O MURO ============
capitulo("I", "O MURO", "O terceirão é o último muro antes do mundo.")
pag("", f"""<div style="position:absolute;left:110px;top:170px;width:1080px">
<div class="lbl k">Manifesto</div>
<div class=h style="font-size:118px;margin-top:40px">A gente não<br>pichou a escola.</div>
<div class="s k" style="font-size:118px;line-height:1;margin-top:10px">A gente assinou.</div></div>
<div style="position:absolute;right:110px;top:300px;width:520px">
<p class=t style="font-size:22px;max-width:none">Três anos de corredor, prova, intervalo e amizade cabem numa assinatura. Ela é grafite, não pixo: tem técnica, cor e cuidado. É gorda porque é coletiva. É roxa porque é nossa.</p>
<div class=rule style="margin:40px 0"></div>
<p class=t style="font-size:22px;max-width:none">Essa marca não é só do moletom. É a tag que a turma deixa no último muro antes do mundo — e que continua valendo depois que a gente sair.</p></div>""", "Manifesto")
vals = [("Atitude", "Grafite tem regra: legibilidade, técnica e respeito pelo espaço. Ousada, nunca bagunçada."),
        ("União", "Todas as letras no mesmo plano, encostadas. Ninguém fica pra trás, ninguém fica por cima."),
        ("Legado", "O 27 é o nosso número. Assina o boné hoje e a foto de formatura daqui a vinte anos.")]
pag("cl", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Valores</div>
<div style="position:absolute;left:110px;right:110px;top:260px;display:grid;grid-template-columns:repeat(3,1fr);gap:70px">{''.join(
 f'<div><div class=s style="font-size:30px;color:{ROXO}">0{i}</div><div class=h style="font-size:92px;margin-top:20px">{a}</div><div class=rule style="margin:34px 0"></div><p class=t style="font-size:21px">{b}</p></div>' for i, (a, b) in enumerate(vals, 1))}</div>""", "Valores")
pag("", f"""<div class=img style="left:0;top:0;width:960px;height:1080px"><img src="{U(A/'moletom-mockup-costas.png')}"></div>
<div style="position:absolute;left:1060px;top:300px;width:700px"><div class="lbl k">Território</div>
<div class=h style="font-size:84px;margin-top:30px">Rua, escola<br>e arquibancada.</div>
<p class=t style="margin-top:40px">A marca vive entre o streetwear e o orgulho de turma. Referências: grafite de bloco dos anos 90, uniforme esportivo americano, adesivo de skate. Nada de pixação, nada de clichê de formatura.</p></div>""", "Território")

# ============ II · A TAG ============
capitulo("II", "A TAG", "Cada milímetro dessa letra foi escolhido.")
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Processo · 01</div>
<div class=h style="position:absolute;left:110px;top:220px;font-size:80px">De 150 fontes<br>a uma letra.</div>
<div style="position:absolute;left:110px;top:470px;display:flex;gap:46px;align-items:flex-end">{''.join(
 f'<div><div class=s style="font-size:120px;line-height:1;color:{c}">{a}</div><div class=lbl style="margin-top:8px;opacity:.6">{b}</div></div>' for a, b, c in [("150", "fontes testadas", "#5d5366"), ("30", "modelos", "#7d6c8c"), ("7", "favoritas", ESC), ("1", "escolhida", ROXO)])}</div>
<div class=img style="right:110px;top:150px;width:860px;height:780px;border-radius:6px"><img src="{U(AQUI/'modelos-escrita/rodada2/todos.jpg')}" style="object-position:top"></div>""", "Processo")
pag("cl", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Processo · 02</div>
<div class=h style="position:absolute;left:110px;top:220px;font-size:80px">Ajuste fino.</div>
<p class=t style="position:absolute;left:110px;top:340px">Posição do RÃO em 20 passos, espaço entre linhas em 20, til em 30 desenhos, ano em mais de 100 testes. A versão final é a soma das melhores decisões.</p>
<div style="position:absolute;left:110px;right:110px;top:520px;bottom:120px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px">{''.join(
 f'<div><div class=img style="position:relative;height:330px;border-radius:6px"><img src="{U(AQUI/p)}"></div><div class=cap>{c}</div></div>' for p, c in
 [("costas/rao-posicoes/todas.jpg", "20 posições do RÃO"), ("costas/tils/todos.jpg", "30 desenhos de til"), ("costas/ano30/todas.jpg", "Estudos do ano")])}</div>""", "Processo")
pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 45% 60% at 62% 50%,#251630,{PRETO} 70%)"></div>
<img src="{ART}" style="position:absolute;left:820px;top:60px;height:960px">
<div style="position:absolute;left:110px;top:300px;width:560px"><div class="lbl k">Assinatura principal</div>
<div class=h style="margin-top:30px">A tag<br>da turma.</div>
<p class=t style="margin-top:40px">TER / CEI / RÃO empilhado e emendado num plano só, til desenhado à mão, o 27 encaixado no RÃO como assinatura de grafiteiro, e Mãe de Deus espaçado na base.</p></div>""", "Assinatura")
# anatomia (posições em % da caixa da arte)
X0, Y0, H = 760, 70, 940; W = H * 1503 / 1800
pts = [(0.255, 0.104, "Contorno branco", -1), (0.108, 0.163, "Brilho de 4 pontas", -1), (0.316, 0.135, "Contorno preto", -1), (0.469, 0.372, "Recheio em degradê", 1), (0.745, 0.232, "Sombra 3D uva", 1), (0.591, 0.500, "Til desenhado à mão", -1), (0.775, 0.653, "Buracos sempre brancos", 1), (0.683, 0.756, "27 emendado", 1), (0.530, 0.883, "Mãe de Deus · espaçado", -1)]
an = ""
for px, py, txt, lado in pts:
    x, y = X0 + px * W, Y0 + py * H
    tx = X0 - 60 if lado < 0 else X0 + W + 60
    an += f'<i class=pin style="left:{x-8}px;top:{y-8}px"></i>'
    l, r = (tx, x) if lado < 0 else (x, tx)
    an += f'<i class=ln style="left:{l}px;top:{y}px;width:{r-l}px"></i>'
    an += f'<span class=tag style="top:{y-9}px;{"right:" + str(1920 - tx + 14) if lado < 0 else "left:" + str(tx + 14)}px">{txt}</span>'
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Anatomia</div>
<img src="{ART}" style="position:absolute;left:{X0}px;top:{Y0}px;height:{H}px">{an}""", "Anatomia")
pag("", f"""<div class=img style="inset:0"><img src="{U(M/'close-rao.png')}"></div>
<div style="position:absolute;left:110px;bottom:130px;max-width:620px;background:rgba(10,10,12,.78);padding:36px 40px;border-left:3px solid {ROXO}">
<div class="lbl k">Detalhe</div><div class=s style="font-size:46px;margin-top:16px;line-height:1.15">O til é gordo como as letras.<br>O 27 encosta no RÃO.</div></div>""", "Detalhe")
grade = "".join(f'<i style="position:absolute;left:{x}px;top:0;bottom:0;width:1px;background:rgba(153,107,179,.28)"></i>' for x in range(0, 781, 78)) + \
        "".join(f'<i style="position:absolute;top:{y}px;left:0;right:0;height:1px;background:rgba(153,107,179,.28)"></i>' for y in range(0, 937, 78))
pag("", f"""<div style="position:absolute;left:110px;top:300px;width:520px"><div class="lbl k">Construção</div>
<div class=h style="margin-top:30px">Espaço<br>pra respirar.</div>
<p class=t style="margin-top:40px">A área de proteção mede <b>x</b> — a altura do 27 — em todos os lados. Nada invade: texto, foto, borda ou outra marca.</p></div>
<div style="position:absolute;right:220px;top:72px;width:780px;height:936px">{grade}
<div style="position:absolute;inset:78px;border:2px dashed {ROXO}"></div>
<img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:740px">
<span class="tag k" style="left:30px;top:30px">x</span><span class="tag k" style="right:30px;bottom:30px">x</span></div>""", "Construção")
V = [(ART, "Principal", PRETO, "fundos escuros"), (NEG, "Negativo", GELO, "fundos claros"),
     (U(F / "versoes-1cor/terceirao-1cor-branco.png"), "Uma cor · branco", "#141018", "serigrafia 1 tinta"),
     (U(F / "versoes-1cor/terceirao-1cor-roxo.png"), "Uma cor · roxo", "#141018", "bordado / 1 tinta")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Versões</div>
<div style="position:absolute;left:110px;right:110px;top:220px;bottom:130px;display:grid;grid-template-columns:repeat(4,1fr);gap:22px">{''.join(
 f'<div style="display:flex;flex-direction:column"><div style="flex:1;background:{b};border:1px solid rgba(237,231,242,.08);position:relative"><img src="{s}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div>'
 f'<div class=h style="font-size:30px;margin-top:22px;letter-spacing:-.02em">{t}</div><div class=cap>{d}</div></div>' for s, t, b, d in V)}</div>""", "Versões")
pag("cl", f"""<div style="position:absolute;left:110px;top:300px;width:540px"><div class="lbl k">Símbolo</div>
<div class=h style="margin-top:30px">O 27<br>sozinho.</div>
<p class=t style="margin-top:40px">Quando a assinatura não cabe — boné, manga, ícone de perfil, botton —, o número fala pela turma.</p></div>
<div style="position:absolute;right:110px;top:150px;width:1060px;height:800px;display:grid;grid-template-columns:1.4fr 1fr;grid-template-rows:1fr 1fr;gap:20px">
<div style="grid-row:span 2;background:{PRETO};position:relative"><img src="{S27}" style="position:absolute;inset:60px;width:calc(100% - 120px);height:calc(100% - 120px);object-fit:contain"></div>
<div style="background:{ROXO};position:relative"><img src="{U(F/'versoes-1cor/simbolo-27-1cor-preto.png')}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div>
<div style="background:#fff;position:relative"><img src="{S27}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div></div>""", "Símbolo")
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Tamanhos mínimos</div>
<div class=h style="position:absolute;left:110px;top:220px;font-size:80px">Pequena,<br>nunca ilegível.</div>
<div style="position:absolute;left:110px;right:110px;bottom:150px;display:flex;align-items:flex-end;justify-content:space-between">{''.join(
 f'<div><img src="{s}" style="height:{h}px;display:block"><div class=rule style="margin:22px 0 14px"></div><div class=lbl style="opacity:.7">{t}</div></div>' for s, h, t in
 [(ART, 440, "Costas · 28–32 cm"), (ART, 210, "Peito · mín. 8 cm"), (ART, 110, "Tela · mín. 180 px"), (S27, 120, "Símbolo · mín. 3 cm"), (S27, 56, "Ícone · 48 px")])}</div>""", "Mínimos")

# ============ III · A COR ============
capitulo("III", "A COR", "Roxo não é a cor da escola. É a cor da turma.")
pag("rx", f"""<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.13;mix-blend-mode:multiply">
<div style="position:absolute;left:110px;top:200px"><div class=lbl style="opacity:.7">Cor principal</div>
<div class=h style="font-size:220px;margin-top:20px">Roxo<br>turma.</div></div>
<div style="position:absolute;right:110px;bottom:150px;font-family:M;font-size:20px;line-height:2.1;text-align:right">HEX #996BB3<br>RGB 153 · 107 · 179<br>CMYK 40 · 60 · 0 · 0<br>PANTONE ≈ 2577 C</div>
<div class=s style="position:absolute;left:115px;bottom:150px;font-size:34px;max-width:720px">Vibrante sem gritar. Funciona no moletom preto, no papel branco e na tela do celular.</div>""", "Cor")
cores = [("Roxo turma", ROXO, "153 107 179", "40 60 0 0", "≈ 2577 C"), ("Lilás", LILAS, "228 207 247", "8 16 0 0", "≈ 263 C"),
         ("Roxo escuro", ESC, "122 76 153", "55 75 0 5", "≈ 2587 C"), ("Uva", UVA, "62 35 83", "75 90 25 35", "≈ 2627 C"),
         ("Branco", "#FFFFFF", "255 255 255", "0 0 0 0", "—"), ("Preto", PRETO, "10 10 12", "75 68 67 90", "Black 6 C")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Paleta</div>
<div style="position:absolute;left:110px;right:110px;top:220px;bottom:130px;display:grid;grid-template-columns:2.3fr repeat(5,1fr);gap:14px">{''.join(
 f'<div style="background:{c};position:relative;padding:30px;border:1px solid rgba(237,231,242,.08);color:{PRETO if c in (LILAS, "#FFFFFF") else "#fff"}">'
 f'<div class=h style="font-size:30px;letter-spacing:-.02em">{nm}</div><div style="position:absolute;left:30px;bottom:30px;font-family:M;font-size:14px;line-height:1.9;opacity:.85">HEX {c.upper()}<br>RGB {r}<br>CMYK {cm}<br>PMS {p}</div></div>' for nm, c, r, cm, p in cores)}</div>""", "Paleta")
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Equilíbrio</div>
<div class=h style="position:absolute;left:110px;top:220px;font-size:80px">O preto é o palco.<br><span class=k>O roxo é a voz.</span></div>
<div style="position:absolute;left:110px;right:110px;top:560px;height:180px;display:flex">
<div style="flex:60;background:#000;border:1px solid rgba(237,231,242,.12)"></div><div style="flex:25;background:{ROXO}"></div><div style="flex:10;background:#fff"></div><div style="flex:5;background:{LILAS}"></div></div>
<div style="position:absolute;left:110px;right:110px;top:770px;display:flex" class=lbl><span style="flex:60">Preto · 60</span><span style="flex:25">Roxo · 25</span><span style="flex:10">Branco · 10</span><span style="flex:5">5</span></div>""", "Proporção")

# ============ IV · A VOZ ============
capitulo("IV", "A VOZ", "A gente fala como escreve no muro: pouco, alto e com estilo.")
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Tipografia</div>
<div style="position:absolute;left:110px;right:110px;top:230px;display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:70px">
<div><div style="font-family:G;font-size:300px;line-height:.85;color:{LILAS}">Aa</div><div class=rule style="margin:30px 0"></div><div class=h style="font-size:38px">Graffiti Youth</div><div class=cap>Assinatura · impacto</div>
<div style="font-family:G;font-size:40px;margin-top:26px;line-height:1.25">ABCDEFGHIJKLMN<br>OPQRSTUVWXYZ<br>0123456789</div></div>
<div><div style="font-weight:900;font-size:230px;line-height:.85;letter-spacing:-.05em">Aa</div><div class=rule style="margin:30px 0"></div><div class=h style="font-size:38px">Inter</div><div class=cap>Títulos limpos · texto</div>
<p class=t style="margin-top:26px">Black nos títulos editoriais, Regular no texto corrido.</p></div>
<div><div class=s style="font-size:230px;line-height:.85">Aa</div><div class=rule style="margin:30px 0"></div><div class=h style="font-size:38px">Playfair Italic</div><div class=cap>Citações · emoção</div>
<p class=t style="margin-top:26px">Com Space Mono para rótulos e datas, sempre em maiúsculas espaçadas.</p></div></div>""", "Tipografia")
frases = [("ÚLTIMO ANO.", ROXO), ("A GENTE ASSINOU.", "#fff"), ("TURMA 27", LILAS), ("ATÉ O ÚLTIMO SINAL.", "#fff")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">Tom de voz</div>
<div style="position:absolute;left:110px;top:230px;display:flex;flex-direction:column;gap:18px">{''.join(
 f'<div class=hg style="font-size:118px;color:{c}">{f}</div>' for f, c in frases)}</div>
<div style="position:absolute;right:110px;top:300px;width:460px"><p class=t style="font-size:22px;max-width:none">Frases curtas, em maiúsculas, com ponto final. Tom de orgulho e despedida, nunca de nostalgia triste. Humor permitido, deboche não.</p>
<div class=rule style="margin:36px 0"></div><div class=cap style="opacity:.75">Sim · “Último ano.” “Turma 27.”<br><br>Não · “Saudades eternas” “Melhor turma de todas”</div></div>""", "Voz")
pag("", f"""<img src="{PAT}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,{PRETO} 0,{PRETO}c0 38%,transparent 70%)"></div>
<div style="position:absolute;left:110px;top:300px;width:560px"><div class="lbl k">Estampa corrida</div>
<div class=h style="margin-top:30px">Pattern 27.</div>
<p class=t style="margin-top:40px">Forro do capuz, verso de credencial, papel de presente, wallpaper de celular. O número repetido vira textura de turma.</p></div>""", "Pattern")
pag("cl", f"""<div style="position:absolute;left:110px;top:300px;width:520px"><div class="lbl k">Elementos</div>
<div class=h style="margin-top:30px">Brilhos<br>e figurinhas.</div>
<p class=t style="margin-top:40px">Brilho de 4 pontas em branco, roxo e lilás, sempre em volta e nunca por cima das letras. O 27 e o til podem aparecer soltos, como adesivos.</p></div>
<div style="position:absolute;right:110px;top:150px;width:1000px;height:800px;background:{PRETO}">
{br([(110,110,200,'#fff'),(420,150,120,ROXO),(640,80,80,'#fff'),(820,240,140,LILAS),(140,440,96,ROXO),(320,540,170,'#fff')])}
<img src="{S27}" style="position:absolute;right:60px;bottom:60px;width:430px"></div>""", "Elementos")
erros = [("errado-esticar", "Esticar ou achatar"), ("errado-cor", "Trocar as cores"), ("errado-girar", "Girar"),
         ("errado-fundo", "Fundo poluído"), ("errado-claro", "Principal no fundo claro"), ("errado-transparencia", "Transparência")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class=lbl><span style="color:#FA5F6D">Nunca</span></div>
<div style="position:absolute;left:110px;right:110px;top:220px;display:grid;grid-template-columns:repeat(3,1fr);gap:26px 22px">{''.join(
 f'<div><div class=img style="position:relative;height:300px"><img src="{U(M/(e+".png"))}"><i style="position:absolute;inset:0;background:linear-gradient(45deg,transparent 49.3%,#FA5F6D 49.3% 50.7%,transparent 50.7%)"></i></div><div class=cap style="opacity:.8">✕ {t}</div></div>' for e, t in erros)}</div>""", "Usos incorretos")

# ============ V · A RUA ============
capitulo("V", "A RUA", "Onde a marca vive: no corpo, no papel e na tela.")
pag("cl", f"""<div class=img style="inset:0"><img src="{U(A/'moletom-mockup.png')}" style="object-fit:cover"></div>
<div style="position:absolute;left:110px;bottom:130px" class=lbl>Moletom · costas e peito</div>""", "Vestuário")
pag("", f"""<div class=img style="inset:0"><img src="{U(A/'camiseta-mockup.png')}"></div>
<div style="position:absolute;left:110px;bottom:130px" class=lbl>Camiseta oversized · assinatura principal</div>""", "Vestuário")
pag("", f"""<div class=img style="inset:0"><img src="{U(A/'bone-mockup.png')}"></div>
<div style="position:absolute;left:110px;bottom:130px" class=lbl>Boné · símbolo 27</div>""", "Vestuário")
pag("cl", f"""<div class=img style="left:110px;top:150px;width:1040px;height:800px"><img src="{U(A/'09-convite.png')}"></div>
<div class=img style="left:1180px;top:150px;width:630px;height:390px"><img src="{U(A/'06-ingresso-formatura.png')}"></div>
<div class=img style="left:1180px;top:560px;width:630px;height:390px"><img src="{U(A/'08-credencial.png')}"></div>""", "Impressos")
pag("", f"""<div class=img style="left:0;top:0;width:1920px;height:720px"><img src="{U(A/'05-faixa-turma.png')}"></div>
<div style="position:absolute;left:110px;top:780px;width:700px"><div class="lbl k">Faixa da turma</div>
<p class=t style="margin-top:20px">Arquibancada, festa dos 100 dias, foto oficial. A assinatura à esquerda, a mensagem em grafite à direita.</p></div>""", "Impressos")
pag("", f"""<div class=img style="left:110px;top:150px;width:520px;height:800px"><img src="{U(A/'03-story-instagram.png')}"></div>
<div class=img style="left:660px;top:150px;width:1150px;height:383px"><img src="{U(A/'07-posts-feed.png')}"></div>
<div class=img style="left:660px;top:563px;width:560px;height:387px"><img src="{U(A/'04-adesivo.png')}"></div>
<div style="position:absolute;left:1260px;top:600px;width:520px"><div class="lbl k">Digital</div>
<p class=t style="margin-top:20px">Story de contagem regressiva, grade de feed alternando preto, roxo e claro, e adesivos pra notebook e garrafa.</p></div>""", "Digital")
cal = [("FEV", "Volta às aulas", "Lançamento da marca"), ("MAR", "Moletom", "Pedido e entrega"), ("JUN", "Festa junina", "Adesivos e camisetas"),
       ("AGO", "100 dias", "Faixa e story"), ("NOV", "Baile", "Convite e ingresso"), ("DEZ", "Formatura", "Credencial e foto oficial")]
pag("", f"""<div style="position:absolute;left:110px;top:150px" class="lbl k">O ano da marca</div>
<div class=h style="position:absolute;left:110px;top:220px;font-size:80px">2027, mês a mês.</div>
<div style="position:absolute;left:110px;right:110px;top:560px;height:2px;background:{ROXO}"></div>
<div style="position:absolute;left:110px;right:110px;top:520px;display:grid;grid-template-columns:repeat(6,1fr)">{''.join(
 f'<div><i style="display:block;width:22px;height:22px;border-radius:50%;background:{PRETO};border:4px solid {ROXO};margin:30px 0 40px"></i>'
 f'<div class=s style="font-size:44px;color:{ROXO}">{m}</div><div class=h style="font-size:32px;margin-top:10px;letter-spacing:-.02em">{a}</div><div class=cap>{b}</div></div>' for m, a, b in cal)}</div>""", "Calendário")
pag("", f"""<div style="position:absolute;inset:0;background:radial-gradient(ellipse 40% 60% at 50% 50%,#2D1A3C,{PRETO} 70%)"></div>
{br([(300,260,50,'#fff'),(1580,220,36,ROXO),(1500,820,44,'#fff'),(420,800,30,LILAS)])}
<img src="{S27}" style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);width:620px">
<div class=s style="position:absolute;width:100%;top:760px;text-align:center;font-size:48px">até o último sinal.</div>
<div class=lbl style="position:absolute;width:100%;bottom:110px;text-align:center;opacity:.5">Terceirão 2027 · Colégio Mãe de Deus</div>""", rod=False)

html = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pags)}</body></html>"
h = F / "_bb2.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1800);"
      "await p.pdf({path:process.argv[2],width:'1920px',height:'1080px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(F / "terceirao-2027-brandbook.pdf")], check=True)
h.unlink(); print("ok", cnt[0], "páginas")
