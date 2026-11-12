exec(open('brand.py').read().split("head='''")[0])
exec(open('elem.py').read().split('names=list(V)')[0])
import os
R='#FA5F6D'
for _l in open('posts40.py'):
    if _l.startswith("V['"): exec(_l)
from PIL import Image
os.makedirs('th',exist_ok=True)
for i in range(1,41):
    f=f'th/{i:02d}.jpg'
    if not os.path.exists(f):
        im=Image.open(f'r40/p40-{i:02d}.png').convert('RGB'); im.thumbnail((720,900)); im.save(f,quality=88)
def ic(n,s=48): return f'<svg width="{s}" height="{s}" viewBox="0 0 200 200">{V[n]}</svg>'
CSS=f'''<link rel="stylesheet" href="base.css"><style>
body{{background:#F7F9FC}}
.pg{{position:absolute;inset:0;padding:96px 84px}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:56px}} .top .nm{{font-size:22px;font-weight:600}} .top .pn{{margin-left:auto;font-size:17px;color:{C};letter-spacing:.12em}}
h1{{font-size:68px;line-height:1.02;letter-spacing:-.04em;font-weight:300;color:{N}}} h1 b{{font-weight:700;color:{A};display:block}}
.lead{{font-size:26px;line-height:1.5;color:{N};margin-top:26px;max-width:860px}} .lead b{{color:{A};font-weight:600}}
.k{{font-size:15px;letter-spacing:.22em;color:{A};font-weight:600}}
.bx{{background:#fff;border:2px solid #E2EAF4;border-radius:28px}}
.thumb{{border-radius:18px;border:2px solid #E2EAF4;display:block}}
.tag{{display:inline-block;background:{A};color:#fff;font-weight:600;font-size:16px;border-radius:99px;padding:5px 14px;letter-spacing:.04em}}
.small{{font-size:18px;color:{C};line-height:1.45}}
table{{border-collapse:collapse;width:100%}} td{{padding:14px 0;border-bottom:2px solid #EEF2F7;vertical-align:top;font-size:21px;line-height:1.4}}
td:first-child{{font-weight:600;width:300px;padding-right:20px}}
code{{font-family:Inter,monospace;background:{G};border-radius:8px;padding:2px 8px;font-size:.92em;color:{N}}}
.foot{{position:absolute;bottom:56px;left:84px;right:84px;display:flex;justify-content:space-between;font-size:15px;letter-spacing:.22em;color:#8A97AA}}
</style>'''
pages=[]
def P(body,n):
    n=len(pages)+1
    pages.append(f'''<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body><div class="pg">
<div class="top">{roundlogo(52)}<div class="nm">webclinic</div><div class="pn">GUIA DE POSTS · {n:02d}</div></div>{body}</div>
<div class="foot"><span>WEBCLINIC</span><span>COMO CRIAR OS POSTS</span></div><div class="grain" style="opacity:.04"></div></body></html>''')

# 1 capa
pages.append(f'''<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body>
<div style="position:absolute;left:0;right:0;top:150px;display:flex;justify-content:center">{roundlogo(230)}</div>
<div style="position:absolute;left:0;right:0;top:470px;text-align:center"><div class="k">GUIA DE POSTS</div>
<h1 style="font-size:92px;margin-top:22px">Como criar<b>os posts.</b></h1>
<div class="lead" style="margin:30px auto 0;text-align:center;max-width:760px">O que você me manda, como eu monto e o que deixa um post da Web Clinic <b>com cara de Web Clinic.</b></div></div>
<div style="position:absolute;left:150px;right:150px;top:1000px;display:flex;justify-content:space-between">{''.join(f'<div class="bx" style="width:150px;height:150px;border-radius:40px;display:grid;place-items:center;box-shadow:0 30px 60px -10px rgba(45,127,240,.22)">{ic(n,100)}</div>' for n in ['calendar','zoom','chat','tick'])}</div>
<div class="grain" style="opacity:.04"></div></body></html>''')

# 2 como funciona
steps=[('chat','Você me manda a ficha','Tema, título, frase e o formato. Pode ser em áudio, texto solto ou na ficha pronta (página 8).'),
       ('computer','Eu monto o post','Escolho o visual do formato, encaixo os textos, ajusto tamanho e espaço e exporto em 1080 × 1350.'),
       ('tick','Você aprova ou pede ajuste','Me diz o número do post e o que mudar. Eu refaço e mando o PDF de novo.')]
P(f'''<div class="k">COMO FUNCIONA</div><h1 style="margin-top:14px">Três passos,<b>um post pronto.</b></h1>
<div style="margin-top:60px;display:flex;flex-direction:column;gap:26px">{''.join(f'<div class="bx" style="display:flex;gap:30px;align-items:center;padding:30px 36px"><div style="width:110px;height:110px;flex:none;border-radius:30px;background:{G};display:grid;place-items:center">{ic(n,76)}</div><div><div class="k">PASSO 0{i+1}</div><div style="font-size:32px;font-weight:600;letter-spacing:-.02em;margin:6px 0 6px">{t}</div><div class="small" style="font-size:21px">{d}</div></div></div>' for i,(n,t,d) in enumerate(steps))}</div>
<div class="lead" style="margin-top:44px">Quanto mais clara a ficha, <b>menos rodadas de ajuste.</b></div>''',2)

# 3 anatomia
def lab(y,num,t,d): return f'<div style="position:absolute;left:560px;top:{y}px;width:400px"><div style="display:flex;gap:12px;align-items:center"><span style="width:38px;height:38px;border-radius:50%;background:{A};color:#fff;display:grid;place-items:center;font-weight:700;font-size:18px">{num}</span><b style="font-size:24px">{t}</b></div><div class="small" style="margin:6px 0 0 50px">{d}</div></div>'
P(f'''<div class="k">ANATOMIA DO POST</div><h1 style="margin-top:14px">Toda peça tem<b>as mesmas 5 partes.</b></h1>
<img class="thumb" src="th/02.jpg" style="position:absolute;left:84px;top:440px;width:440px">
{lab(450,1,'Cabeçalho','Logo redondo, webclinic e @webclinic. Fixo, eu coloco.')}
{lab(580,2,'Título em 2 linhas','Linha 1 fina (navy). Linha 2 em negrito azul: a parte que bate.')}
{lab(730,3,'Visual','Foto, ícone vetor, card de site, busca, lista… depende do formato.')}
{lab(880,4,'Frase de baixo','2 linhas. A 2ª linha em azul é a conclusão.')}
{lab(1010,5,'Rodapé','Categoria em caixa alta: AGENDA ONLINE, DICA, SITES PARA MÉDICOS…')}''',3)

# 4-5 formatos
F=[('FOTO','Foto + chips','Foto real de médico num card inclinado, com 2 chips de resultado.',[2,17]),
   ('ICONE','Ícone + chips','Ícone vetor grande no centro, 2 ou 3 chips em volta.',[13,27]),
   ('ICONE-CARD','Ícone + card','Ícone grande ao lado de um card (lista, mensagem, horários).',[12,19]),
   ('SITE','Card de site','Mockup de página com título e botão de agendar.',[1,31]),
   ('BUSCA','Busca no Google','Barra de busca e resultados, com o médico em destaque.',[5,28]),
   ('MENSAGEM','Mensagem','Conversa ou lembrete de WhatsApp com confirmação.',[6,33]),
   ('LISTA','Lista / checklist','Até 5 itens com ícone, título e subtítulo.',[8,26]),
   ('COMPARA','Comparação','Duas colunas: ✕ do lado ruim, ✓ do lado bom.',[7,20]),
   ('PASSOS','Passo a passo','4 etapas com ícone, nome e descrição curta.',[30,37]),
   ('NAVY','Frase forte','Fundo navy, só a frase grande. Para quebrar o ritmo do feed.',[16,29]),
   ('CTA','Chamada final','Logo + botão "Fale com a Web Clinic".',[40]),
   ('LIVRE','Formato livre','Instagram, avaliações, mapa, notificações, especialidades… me descreve a cena.',[4,36])]
def fmt(code,t,d,ex):
    return f'''<div class="bx" style="padding:16px 20px;display:flex;gap:20px;align-items:center"><div style="display:flex;gap:8px">{''.join(f'<img class="thumb" src="th/{e:02d}.jpg" style="width:110px;border-radius:10px">' for e in ex[:2])}</div>
<div><span class="tag">{code}</span><div style="font-size:24px;font-weight:600;margin:8px 0 4px">{t}</div><div class="small">{d}</div><div class="small" style="font-size:15px;margin-top:4px">ex.: post {", ".join(str(e) for e in ex)}</div></div></div>'''
for k,(a,b) in enumerate([(0,4),(4,8),(8,12)]):
    P(f'''<div class="k">FORMATOS · {k+1}/3</div><h1 style="margin-top:14px">{["Escolha o formato","Mais formatos","E pra variar"][k]}<b>{["pelo código.","pra cada assunto.","o ritmo do feed."][k]}</b></h1>
<div style="margin-top:40px;display:flex;flex-direction:column;gap:16px">{''.join(fmt(*f) for f in F[a:b])}</div>''',4+k)

# 6 ficha
rows=[('Tema','A dor, a dica ou a ideia. Ex.: <i>paciente que liga fora do horário</i>.'),
      ('Formato','Um código das páginas 4 a 6. Se não souber, deixa em branco que eu escolho.'),
      ('Título linha 1','Fina. Até ~24 caracteres. Ex.: <code>Sua agenda não fecha</code>'),
      ('Título linha 2','Negrito azul. Até ~20 caracteres. Ex.: <code>às 18h.</code>'),
      ('Conteúdo do visual','Chips (até 3, título + detalhe), itens de lista (até 5), passos (4), colunas da comparação (4 + 4), texto da mensagem ou da busca.'),
      ('Foto (se FOTO)','Descreve a cena (médica sorrindo no consultório, médico com paciente…) ou manda o link/arquivo.'),
      ('Frase de baixo','Linha 1 normal + linha 2 em azul. Até ~45 caracteres cada.'),
      ('Rodapé','AGENDA ONLINE · SITES PARA MÉDICOS · DICA · SITE + GOOGLE · WEBCLINIC'),
      ('Especialidade / nome','Opcional. Nome fictício e especialidade que aparecem nos cards (padrão: Dra. Ana Paula, dermatologia).')]
P(f'''<div class="k">A FICHA DO POST</div><h1 style="margin-top:14px">O que eu preciso<b>pra cada post.</b></h1>
<div class="bx" style="margin-top:40px;padding:12px 36px"><table>{''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in rows)}</table></div>''',6)

# 7 modelo pra copiar
mod='''POST __
Tema:
Formato:
Título 1:
Título 2:
Visual:
  -
  -
  -
Foto:
Frase 1:
Frase 2:
Rodapé:'''
P(f'''<div class="k">MODELO PRA COPIAR</div><h1 style="margin-top:14px">Cola no chat<b>e preenche.</b></h1>
<div style="display:flex;gap:30px;margin-top:44px">
<div class="bx" style="flex:1;padding:34px 36px"><pre style="font-family:Inter,monospace;font-size:24px;line-height:1.6;color:{N};white-space:pre-wrap">{mod}</pre></div>
<div style="width:330px"><div class="bx" style="padding:26px"><div class="k">DICAS</div><div class="small" style="font-size:20px;margin-top:12px;line-height:1.55">• Pode mandar vários posts numa mensagem só.<br><br>• Campo que você não souber, deixa vazio que eu completo.<br><br>• Para mudar um post pronto, manda <b style="color:{A}">“post 12: …”</b> com o que trocar.</div></div></div></div>''',7)

# 8 exemplo
ex='''POST 06
Tema: paciente que esquece a consulta
Formato: MENSAGEM
Título 1: Paciente que esquece
Título 2: a consulta?
Visual:
  - mensagem de lembrete 24h antes
    com Confirmar / Remarcar
  - chip: Maria confirmou ·
    menos faltas na agenda
  - ícone: clock
Frase 1: Lembrete automático pela
         agenda online.
Frase 2: Menos falta, agenda cheia.
Rodapé: AGENDA ONLINE'''
P(f'''<div class="k">EXEMPLO</div><h1 style="margin-top:14px">Da ficha<b>pro post.</b></h1>
<div style="display:flex;gap:28px;margin-top:44px;align-items:flex-start">
<div class="bx" style="flex:1;padding:28px 30px"><pre style="font-family:Inter,monospace;font-size:19px;line-height:1.55;color:{N};white-space:pre-wrap">{ex}</pre></div>
<img class="thumb" src="th/06.jpg" style="width:440px;box-shadow:0 30px 60px -10px rgba(45,127,240,.22)"></div>''',8)

# 9 ícones
icons=['calendar','clock','zoom','chat','bell','tick','x','mobile','computer','heart','plus','shield','star','pin','moon','phoneoff','speed','money','user','steth','tooth','apple','bone','drop','baby','brain','pulse','cursor']
P(f'''<div class="k">BANCO DE ÍCONES</div><h1 style="margin-top:14px">Pede o ícone<b>pelo nome.</b></h1>
<div style="margin-top:40px;display:grid;grid-template-columns:repeat(7,1fr);gap:14px">{''.join(f'<div class="bx" style="padding:14px 6px 10px;text-align:center;border-radius:22px">{ic(n,78)}<div style="font-size:15px;color:{C};margin-top:6px;font-family:Inter">{n}</div></div>' for n in icons)}</div>
<div class="lead" style="font-size:22px;margin-top:30px">Precisa de um que não está aqui? Me diz o objeto que <b>eu desenho no mesmo estilo.</b></div>''',9)

# 10 regras
do=['Branco e gelo de fundo, azul #2D7FF0 e navy #0B1F3A','Poppins: título fino + negrito, sem outra fonte','Muito espaço em branco, até ~25 palavras por post','Cards arredondados com borda clara e sombra azul bem fraca','Fotos reais e bonitas de médico (Pexels), nunca banco datado','Ícones vetor 2D desenhados no estilo da marca']
dont=['Celular/mockup de telefone em todo post','Sombra pesada ou brilho forte atrás','3D de banco ou foto recortada mal','Foto de baixa qualidade ou com marca d’água','Números e estatísticas inventados','Texto técnico ("anamnese", "conversão de leads")']
li=lambda xs,n:''.join(f'<div style="display:flex;gap:14px;align-items:center;padding:12px 0;font-size:21px;line-height:1.35">{ic(n,34)}<span>{x}</span></div>' for x in xs)
P(f'''<div class="k">REGRAS DE ESTILO</div><h1 style="margin-top:14px">O que deixa<b>com cara de Web Clinic.</b></h1>
<div style="display:flex;gap:24px;margin-top:40px"><div class="bx" style="flex:1;padding:26px 28px"><div class="k">SEMPRE</div>{li(do,'tick')}</div>
<div class="bx" style="flex:1;padding:26px 28px"><div class="k" style="color:{R}">NUNCA</div>{li(dont,'x')}</div></div>
<div style="display:flex;gap:12px;margin-top:30px">{''.join(f'<div style="flex:1"><div style="height:80px;border-radius:18px;background:{c};border:2px solid #E2EAF4"></div><div class="small" style="font-size:15px;margin-top:8px;font-family:Inter">{n}<br>{c}</div></div>' for n,c in [('Azul',A),('Navy',N),('Azul claro',L),('Máscara',M),('Gelo',G),('Alerta',R)])}</div>''',10)

# 11 os 40
P(f'''<div class="k">OS 40 POSTS</div><h1 style="margin-top:14px" >Referência rápida<b>por número.</b></h1>
<div style="margin-top:34px;display:grid;grid-template-columns:repeat(8,1fr);gap:10px">{''.join(f'<div style="position:relative"><img class="thumb" src="th/{i:02d}.jpg" style="width:100%;border-radius:8px;border-width:1px"><span style="position:absolute;left:4px;top:4px;background:{A};color:#fff;font-size:13px;font-weight:700;border-radius:6px;padding:1px 6px">{i}</span></div>' for i in range(1,41))}</div>''',11)

for i,p in enumerate(pages,1): open(f'guia-{i:02d}.html','w').write(p)
print(len(pages))
