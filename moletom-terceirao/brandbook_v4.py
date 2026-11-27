"""BRAND BOOK v4 — apresentação moderna (referência do dono: deck "MKT Digital" escuro com brilho, cartões de vidro,
pílula de rótulo, título em 2 tons, texto curto, botões com seta, faixa de letreiro no topo, objetos 3D flutuando).
-> final/terceirao-2027-brandbook.pdf
"""
import subprocess
from pathlib import Path

AQUI = Path(__file__).parent
F = AQUI / "final"; A = F / "aplicacoes"; KV = F / "keyvisuals"; M = F / "_manual"; R = AQUI / "render3d/out"
U = lambda p: Path(p).resolve().as_uri()
FO = U(AQUI / "fontes")
ROXO, LILAS, ESC, UVA, PRETO = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353", "#07060A"
ART = U(F / "arte-principal/terceirao-2027-principal-transparente.png")
BR1 = U(F / "versoes-1cor/terceirao-1cor-branco.png")
NEG = U(F / "negativo/terceirao-2027-principal-negativo-transparente.png")
S27, S27B = U(F / "simbolo/simbolo-27-roxo.png"), U(F / "simbolo/simbolo-27-branco.png")
A3D, T27, STK = U(R / "arte3d.png"), U(R / "t27.png"), U(R / "sticker-a.png")

CSS = f"""
@font-face{{font-family:G;src:url('{FO}/dafont/graffiti_youth.otf')}}
@font-face{{font-family:K;src:url('{FO}/space-grotesk-500.woff2');font-weight:500}}
@font-face{{font-family:K;src:url('{FO}/space-grotesk-700.woff2');font-weight:700}}
@font-face{{font-family:I;src:url('{FO}/inter-400.woff2');font-weight:400}}
@font-face{{font-family:I;src:url('{FO}/inter-700.woff2');font-weight:700}}
@page{{size:1920px 1080px;margin:0}} *{{box-sizing:border-box;margin:0}}
body{{font-family:I;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:1920px;height:1080px;page-break-after:always;position:relative;overflow:hidden;color:#fff;
  background:radial-gradient(ellipse 55% 60% at 50% 115%,rgba(153,107,179,.55),transparent 70%),
             radial-gradient(ellipse 45% 50% at 95% -10%,rgba(122,76,153,.45),transparent 70%),
             linear-gradient(180deg,#0B0812,{PRETO})}}
.tick{{position:absolute;left:0;right:0;top:0;height:46px;border-bottom:1px solid rgba(228,207,247,.12);display:flex;align-items:center;
  gap:34px;white-space:nowrap;font-family:K;font-weight:700;font-size:13px;letter-spacing:.18em;color:rgba(228,207,247,.55);padding-left:20px}}
.tick b{{color:{ROXO}}}
.pill{{display:inline-flex;align-items:center;gap:10px;font-family:K;font-weight:500;font-size:17px;color:#d9cce6}}
.pill i{{width:14px;height:14px;border-radius:50%;border:2px solid {ROXO};box-shadow:inset 0 0 0 3px #0B0812,inset 0 0 0 10px {ROXO}}}
.h{{font-family:K;font-weight:700;font-size:92px;line-height:.98;letter-spacing:-.03em}}
.h em{{font-style:normal;color:#B88FD6}}
.t{{font-size:20px;line-height:1.6;color:rgba(237,231,242,.72);max-width:560px}}
.btn{{display:inline-flex;align-items:center;gap:14px;padding:14px 22px;border:1.5px solid rgba(153,107,179,.7);border-radius:10px;
  font-family:K;font-weight:700;font-size:15px;letter-spacing:.12em;color:#fff;background:rgba(153,107,179,.12)}}
.card{{position:relative;border-radius:22px;background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02));
  border:1px solid rgba(228,207,247,.14);box-shadow:0 30px 70px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08);overflow:hidden}}
.num{{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:10px;border:1.5px solid {ROXO};
  font-family:K;font-weight:700;font-size:22px;color:#fff;background:rgba(153,107,179,.18)}}
.foot{{position:absolute;left:90px;right:90px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-family:K;font-size:14px;color:rgba(228,207,247,.5)}}
.foot img{{height:58px}}
.lado{{position:absolute;left:40px;top:50%;transform:translateY(-50%) rotate(-90deg);transform-origin:left center;font-family:K;font-size:13px;letter-spacing:.2em;color:rgba(228,207,247,.45);white-space:nowrap}}
.flt{{position:absolute;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}}
.img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
"""
TICK = "".join(f"<span>TERCEIRÃO 2027 <b>—</b> MÃE DE DEUS <b>—</b></span>" for _ in range(9))
pags = []
def pag(corpo, n=None, flt=""):
    logo = f'<img src="{BR1}">' if len(pags) >= 2 else '<span></span>'
    pags.append(f'<div class=p><div class=tick>{TICK}</div><div class=lado>○ Turma 2027</div>{flt}{corpo}'
                f'<div class=foot>{logo}<span>@terceirao.mdd · {len(pags)+1:02d}</span></div></div>')
def bloco(pill, h, t="", btn="", x=110, y=230, w=640):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px"><div class=pill><i></i>{pill}</div>'
            f'<div class=h style="margin-top:22px">{h}</div>' + (f'<p class=t style="margin-top:28px">{t}</p>' if t else "")
            + (f'<div class=btn style="margin-top:36px">{btn} <span>↗</span></div>' if btn else "") + "</div>")
def foto(src, x, y, w, h, fit="cover", pad=0, bg="transparent"):
    return f'<div class=card style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg}"><img src="{src}" style="position:absolute;inset:{pad}px;width:calc(100% - {2*pad}px);height:calc(100% - {2*pad}px);object-fit:{fit}"></div>'
def flt(src, x, y, w, rot=0, blur=0, op=1):
    return f'<img class=flt src="{src}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);filter:blur({blur}px) drop-shadow(0 30px 40px rgba(0,0,0,.6));opacity:{op}">'

# 01 capa
pag(bloco("Manual de marca", "Terceirão<br><em>2027 começa aqui.</em>", "A identidade visual da turma: assinatura, cores, tipografia e aplicações.", "VER A MARCA", y=360, w=860),
    flt=f'<div style="position:absolute;right:140px;top:110px;width:780px;height:860px;border-radius:50%;background:radial-gradient(circle,rgba(153,107,179,.45),transparent 65%);filter:blur(30px)"></div>'
        + '<div style="position:absolute;right:300px;top:330px;width:420px;height:420px;border-radius:50%;border:1px solid rgba(228,207,247,.25)"></div>'
        + '<div style="position:absolute;right:220px;top:250px;width:580px;height:580px;border-radius:50%;border:1px solid rgba(228,207,247,.12)"></div>'
        + '<div style="position:absolute;right:420px;top:450px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,#E4CFF7,#996BB3 60%,transparent 72%);filter:blur(4px)"></div>')
# 02 sobre
cards = [("1", "Atitude", "Grafite com técnica e cor. Ousada, nunca bagunçada."), ("2", "União", "Letras encostadas no mesmo plano: ninguém fica pra trás."), ("3", "Legado", "O 27 é o nosso número. Assina hoje e daqui a 20 anos.")]
pag(bloco("Conheça a", "Nossa<br><em>marca.</em>", "Uma assinatura de grafite feita pra turma de 2027 do Colégio Mãe de Deus: forte no moletom preto, legível em qualquer tamanho.", y=250, w=560)
    + '<div style="position:absolute;left:760px;right:110px;top:300px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px">'
    + "".join(f'<div class=card style="padding:34px;height:380px"><span class=num>{n}</span><div class=h style="font-size:40px;margin-top:40px">{a}</div><p class=t style="margin-top:18px;font-size:18px">{b}</p></div>' for n, a, b in cards) + "</div>",
    )
# 03 assinatura
pag(bloco("Assinatura", "A tag<br><em>da turma.</em>", "TER / CEI / RÃO empilhado, til desenhado à mão e o 27 encaixado como assinatura de grafiteiro.", "BAIXAR ARQUIVOS", w=600)
    + f'<div class=card style="position:absolute;left:780px;top:120px;width:1030px;height:840px;background:radial-gradient(ellipse at 50% 45%,rgba(153,107,179,.3),rgba(255,255,255,.02) 70%)"><img src="{ART}" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:760px"></div>')
# 04 logo em 3D (cena)
pag(f'<img class=img src="{U(KV/"kv01-heroi.png")}">')
# 05 versões
V = [(ART, "Principal", "Fundos escuros", "#0E0B12"), (NEG, "Negativo", "Fundos claros", "#EFEAF3"), (BR1, "Uma cor", "Serigrafia 1 tinta", "#0E0B12"), (U(F/"versoes-1cor/terceirao-1cor-roxo.png"), "Uma cor roxo", "Bordado", "#0E0B12")]
pag(bloco("Versões", "Uma marca,<br><em>quatro jeitos.</em>", w=900, y=150)
    + '<div style="position:absolute;left:110px;right:110px;top:440px;display:grid;grid-template-columns:repeat(4,1fr);gap:22px">'
    + "".join(f'<div><div class=card style="height:420px;background:{b}"><img src="{s}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div><div style="display:flex;gap:14px;align-items:center;margin-top:18px"><span class=num style="width:36px;height:36px;font-size:16px">{i}</span><div><div style="font-family:K;font-weight:700;font-size:20px">{t}</div><div style="font-size:14px;color:rgba(237,231,242,.55)">{d}</div></div></div></div>' for i, (s, t, d, b) in enumerate(V, 1)) + "</div>")
# 06 símbolo
pag(bloco("Símbolo", "O 27<br><em>sozinho.</em>", "Quando a assinatura não cabe: boné, manga, foto de perfil, botton.", w=560)
    + f'<div style="position:absolute;left:760px;right:110px;top:130px;bottom:130px;display:grid;grid-template-columns:1.4fr 1fr;grid-template-rows:1fr 1fr;gap:22px">'
    + f'<div class=card style="grid-row:span 2;background:radial-gradient(circle at 50% 45%,rgba(153,107,179,.35),rgba(255,255,255,.02) 70%)"><img src="{T27}" style="position:absolute;inset:50px;width:calc(100% - 100px);height:calc(100% - 100px);object-fit:contain"></div>'
    + f'<div class=card style="background:linear-gradient(135deg,{UVA},{ROXO})"><img src="{S27B}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div>'
    + f'<div class=card style="background:#F2EEF5"><img src="{S27}" style="position:absolute;inset:40px;width:calc(100% - 80px);height:calc(100% - 80px);object-fit:contain"></div></div>')
# 08 cores (estilo "pacotes")
cores = [("1", "Roxo turma", ROXO, "153 · 107 · 179", "40 · 60 · 0 · 0", "2577 C"), ("2", "Uva", UVA, "62 · 35 · 83", "75 · 90 · 25 · 35", "2627 C"), ("3", "Lilás", LILAS, "228 · 207 · 247", "8 · 16 · 0 · 0", "263 C")]
pag(bloco("Conheça nossas", "<em>Cores.</em>", w=900, y=150)
    + '<div style="position:absolute;left:110px;right:110px;top:330px;display:grid;grid-template-columns:repeat(3,1fr);gap:26px">'
    + "".join(f'<div class=card style="height:560px;padding:0"><div style="height:300px;background:linear-gradient(160deg,{c},{c}cc);position:relative"><span class=num style="position:absolute;left:30px;top:30px;background:rgba(0,0,0,.25);border-color:rgba(255,255,255,.6)">{n}</span></div>'
              f'<div style="padding:30px"><div style="font-family:K;font-weight:700;font-size:34px">{nm}</div><div style="font-family:K;font-weight:700;font-size:44px;color:{c if c != UVA else "#B48ACB"};margin-top:6px">{c.upper()}</div>'
              f'<div style="font-size:15px;color:rgba(237,231,242,.6);margin-top:14px;line-height:1.8">RGB {r}<br>CMYK {cm} · PMS ≈ {p}</div></div></div>' for n, nm, c, r, cm, p in cores) + "</div>"
    + '<div style="position:absolute;right:110px;top:200px;display:flex;gap:12px"><div class=card style="width:120px;height:70px;background:#fff"></div><div class=card style="width:120px;height:70px;background:#07060A"></div></div>')
# 09 tipografia
pag(bloco("Tipografia", "Duas fontes,<br><em>uma voz.</em>", w=700, y=150)
    + f'<div style="position:absolute;left:110px;right:110px;top:440px;display:grid;grid-template-columns:1fr 1fr;gap:26px">'
    + f'<div class=card style="height:460px;padding:44px"><div style="font-family:G;font-size:190px;line-height:.9;color:{LILAS}">Aa</div><div style="font-family:K;font-weight:700;font-size:30px;margin-top:30px">Graffiti Youth</div><p class=t style="font-size:17px;margin-top:10px">Só na assinatura e em títulos de impacto.</p></div>'
    + f'<div class=card style="height:460px;padding:44px"><div style="font-family:K;font-weight:700;font-size:190px;line-height:.9;letter-spacing:-.05em">Aa</div><div style="font-family:K;font-weight:700;font-size:30px;margin-top:30px">Space Grotesk + Inter</div><p class=t style="font-size:17px;margin-top:10px">Títulos modernos e textos de apoio.</p></div></div>')
# 10 abertura aplicações: mosaico de cartões inclinados
MOS = [(A/"moletom-mockup.png", 980, 120, 520, 330, -4), (A/"dono-2-close.png", 1520, 90, 330, 330, 5), (KV/"kv07-canecas.png", 900, 480, 470, 265, 3),
       (A/"camiseta-mockup.png", 1390, 450, 470, 265, -3), (KV/"ad1-muro-concreto.png", 1000, 770, 420, 236, -5), (KV/"kit-formatura.png", 1440, 750, 420, 236, 4)]
pag(bloco("Explore as", "<em>Aplicações.</em>", "Onde a marca vive: no corpo, no papel e na tela.", y=380, w=700)
    + "".join(f'<div class=card style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg);background:#fff"><img class=img src="{U(src)}"></div>' for src, x, y, w, h, r in MOS))
# aplicações com moldura de vidro + texto curto
APS = [
    ("Moletom", "A peça<br><em>principal.</em>", "Arte grande nas costas e assinatura pequena no peito esquerdo.", A / "moletom-mockup.png", "contain", "#fff"),
    ("Moletom", "Detalhe<br><em>no peito.</em>", "Serigrafia sobre moletom preto: o contorno branco garante leitura.", A / "dono-2-close.png", "cover", None),
    ("Camiseta", "Camiseta<br><em>oversized.</em>", "Mesma arte das costas, aplicada na frente.", A / "camiseta-mockup.png", "cover", None),
    ("Camiseta", "Versão<br><em>time.</em>", "Assinatura pequena no peito, como escudo de time.", A / "camiseta-time.png", "cover", None),
    ("Adesivos", "Cola<br><em>em tudo.</em>", "Vinil com recorte branco: muro, mesa, caderno, garrafa.", KV / "ad1-muro-concreto.png", "cover", None),
    ("Adesivos", "Cartela de<br><em>adesivos.</em>", "Assinatura, símbolo 27 e frases da turma numa cartela meio-corte.", KV / "kit-adesivos.png", "cover", None),
    ("Canecas", "Preta<br><em>e branca.</em>", "Principal na preta, negativo na branca.", KV / "kv07-canecas.png", "cover", None),
    ("Baile", "Pulseiras<br><em>de acesso.</em>", "Três cores pra separar convidados, formandos e staff.", KV / "kv16-pulseiras.png", "cover", None),
    ("Formatura", "Kit da<br><em>formatura.</em>", "Envelope com lacre 27, convite frente e verso, ingresso, crachá e adesivo.", KV / "kit-formatura.png", "cover", None),
]
for i, (pl, h, t, src, fit, bg) in enumerate(APS):
    quad = "close" in str(src)
    pag(bloco(pl, h, t, w=540, y=300) + (foto(U(src), 1000, 110, 810, 860, "cover", 0) if quad else foto(U(src), 720, 233, 1090, 613, fit, 0, bg or "#0E0B12")))
pag(bloco("Festas", "Convites<br><em>da turma.</em>", "Graffiti Youth no impacto, Space Grotesk na informação.", w=480, y=300)
    + '<div style="position:absolute;left:640px;right:110px;top:290px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px">'
    + "".join(f'<div class=card style="aspect-ratio:1080/1500"><img class=img src="{U(F/"convites"/f"convite-{n}.png")}"></div>' for n in ["festa", "baile", "100dias", "ultimo"]) + "</div>")
pag(f'<div style="position:absolute;left:110px;right:110px;top:130px;bottom:130px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px">'
    + "".join(f'<div class=card><img class=img src="{U(KV/(n+".png"))}"></div>' for n in ["ad2-muro-tijolo", "ad3-mesa-madeira", "ad4-asfalto"]) + "</div>"
    + '<div style="position:absolute;left:110px;top:70px"><div class=pill><i></i>Adesivos em superfícies reais</div></div>')
# cuidados (perto do fim)
erros = [("errado-esticar", "Esticar"), ("errado-cor", "Trocar cores"), ("errado-girar", "Girar"), ("errado-fundo", "Fundo poluído"), ("errado-claro", "Principal no claro"), ("errado-transparencia", "Transparência")]
pag(bloco("Cuidados", "O que<br><em>não fazer.</em>", "Tamanho mínimo: 8 cm impresso e 180 px na tela. O símbolo 27: 3 cm / 48 px.", w=560)
    + '<div style="position:absolute;left:760px;right:110px;top:150px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px">'
    + "".join(f'<div><div class=card style="height:300px"><img class=img src="{U(M/(e+".png"))}"><i style="position:absolute;inset:0;background:linear-gradient(45deg,transparent 49.4%,#FA5F6D 49.4% 50.6%,transparent 50.6%)"></i></div><div style="margin-top:12px;font-family:K;font-size:16px;color:rgba(237,231,242,.7)">✕ {t}</div></div>' for e, t in erros) + "</div>")
# fim
pag(bloco("Turma 2027", "Obrigado<br><em>pela atenção.</em>", "Colégio Mãe de Deus · Terceirão 2027. Até o último sinal.", "@terceirao.mdd", y=360, w=860),
    flt=f'<div style="position:absolute;right:140px;top:110px;width:780px;height:860px;border-radius:50%;background:radial-gradient(circle,rgba(153,107,179,.45),transparent 65%);filter:blur(30px)"></div>' + flt(T27, 1080, 200, 700, -6))

html = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pags)}</body></html>"
h = F / "_bb4.html"; h.write_text(html)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      "await p.goto('file://'+process.argv[1]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);"
      "await p.pdf({path:process.argv[2],width:'1920px',height:'1080px',printBackground:true});await b.close();})()")
subprocess.run(["node", "-e", js, str(h.resolve()), str(F / "terceirao-2027-brandbook.pdf")], check=True)
h.unlink(); print("ok", len(pags), "páginas")
