# Perfil do Instagram: capas de destaque, stories dos destaques e PDF de configuração
exec(open('brand.py').read().split("head='''")[0])
_b=open('brand.py').read(); exec(_b[_b.index('icons={'):_b.index('hl=')])
import os, html
icons['Agenda']=f'<rect x="22" y="28" width="56" height="50" rx="10" fill="none" stroke="{N}" stroke-width="5"/><path d="M22 42H78" stroke="{N}" stroke-width="4"/><path d="M36 22v12M64 22v12" stroke="{N}" stroke-width="5" stroke-linecap="round"/><path d="M40 60l7 7 14-14" fill="none" stroke="{A}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>'
RAW='https://raw.githubusercontent.com/meneghetti27/DOTAGENCIA/main/webclinic/perfil/'
OUT='../perfil'; os.makedirs(OUT+'/destaques',exist_ok=True); os.makedirs('perfil-html',exist_ok=True)

PERFIL=dict(
 nome='Web Clinic | Sites p/ médicos',
 usuario='webclinicbrasil',
 categoria='Web designer (se não existir: Agência de marketing)',
 bio='Sites que viram consulta marcada.\nPara médicos e profissionais da saúde.\nAgenda online + Google + WhatsApp.\nMande SITE no direct ↓',
 link='https://wa.me/5551989061441  (WhatsApp da Web Clinic; no campo "Links" → Adicionar link externo, título: WhatsApp)',
 botoes='Opções de contato → WhatsApp: +55 51 98906-1441 (aparece o botão WhatsApp no perfil). Botão de ação: nenhum.',
)
# destaques: (nome, ícone, posts usados como stories)
DEST=[('Sobre','Sobre',[1,37,40]),('Sites','Sites',[7,21,31,22]),('Agenda','Agenda',[2,6,24,20]),('Dicas','Dicas',[8,26,13,9]),('Contato','Contato',[])]

STY=f'<link rel="stylesheet" href="../base.css"><style>html,body{{width:1080px;height:1920px;overflow:hidden;background:{G}}}</style>'
def capa(nome,ic):
    return f'''<!doctype html><html><head><meta charset="utf-8">{STY}</head><body>
<div style="position:absolute;left:190px;top:610px;width:700px;height:700px;border-radius:50%;background:#fff;border:6px solid #E2EAF4;display:grid;place-items:center">
<svg width="420" height="420" viewBox="0 0 100 100">{icons[ic]}</svg></div></body></html>'''
def story(n,nome,last=False):
    return f'''<!doctype html><html><head><meta charset="utf-8">{STY}</head><body>
<div style="position:absolute;top:150px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px">{roundlogo(76)}<div style="font-size:30px;font-weight:600">webclinic</div></div>
<div style="position:absolute;top:280px;left:0;right:0;text-align:center;font-size:24px;letter-spacing:.24em;color:{A};font-weight:600">{nome.upper()}</div>
<img src="../../posts/post-{n:02d}.png" style="position:absolute;left:90px;top:400px;width:900px;border-radius:36px;border:3px solid #E2EAF4;box-shadow:0 40px 80px -20px rgba(45,127,240,.25)">
<div style="position:absolute;bottom:200px;left:0;right:0;text-align:center;font-size:28px;color:{C}">mais no perfil · <b style="color:{A}">@webclinicbrasil</b></div></body></html>'''
contato=f'''<!doctype html><html><head><meta charset="utf-8">{STY}</head><body>
<div style="position:absolute;top:360px;left:0;right:0;display:flex;justify-content:center">{roundlogo(300)}</div>
<div style="position:absolute;top:760px;left:0;right:0;text-align:center;letter-spacing:-.04em;line-height:1.04"><div style="font-size:88px;font-weight:300;color:{N}">Vamos encher</div><div style="font-size:100px;font-weight:700;color:{A}">sua agenda?</div></div>
<div style="position:absolute;top:1080px;left:120px;right:120px;background:#fff;border:3px solid #E2EAF4;border-radius:40px;padding:44px 50px;font-size:36px;line-height:1.6;color:{N}">
<b style="color:{A}">Direct:</b> mande a palavra SITE<br><b style="color:{A}">Link na bio:</b> fale com a gente</div></body></html>'''
jobs=[]
for nome,ic,posts in DEST:
    k=nome.lower(); open(f'perfil-html/capa-{k}.html','w').write(capa(nome,ic)); jobs.append((f'capa-{k}.html',f'destaques/capa-{k}.png'))
open('perfil-jobs.txt','w').write('\n'.join(a+' '+b for a,b in jobs))
# stories v2: desenhados em stories.py (renderizados por shots.js e copiados como destaques/story-NOME-N.png)
_sj=open('stories-jobs.txt').read().split()
STORIES={nome:[f'destaques/story-{h[:-5]}.png' for h in _sj if h.startswith(nome.lower()+'-')] for nome,_,_ in DEST}

# ---------- PDF ----------
def esc(s): return html.escape(s).replace('\n','<br>')
CSS=f'''<link rel="stylesheet" href="base.css"><style>
@page{{size:1080px 1350px;margin:0}} html,body{{width:auto;height:auto;overflow:visible;background:#F7F9FC}}
.pg{{width:1080px;height:1350px;position:relative;overflow:hidden;padding:80px 80px;page-break-after:always;background:#F7F9FC}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:36px}} .top .nm{{font-size:22px;font-weight:600}} .top .pn{{margin-left:auto;font-size:16px;color:{C};letter-spacing:.12em}}
h1{{font-size:62px;line-height:1.04;letter-spacing:-.04em;font-weight:300;color:{N}}} h1 b{{font-weight:700;color:{A};display:block}}
.k{{font-size:14px;letter-spacing:.22em;color:{A};font-weight:600}}
.bx{{background:#fff;border:2px solid #E2EAF4;border-radius:24px}}
.alert{{background:#FFF1F2;border:2px solid #FBC9CE;border-radius:20px;padding:18px 22px;font-size:20px;line-height:1.45;color:{N}}} .alert b{{color:#D63848}}
ol{{padding-left:30px}} li{{font-size:20px;line-height:1.5;margin-bottom:8px}} li b{{color:{A}}}
.lab{{font-size:13px;letter-spacing:.2em;color:{C};font-weight:600;margin-bottom:6px}}
.val{{font-size:21px;line-height:1.45;color:{N}}} .url{{font-size:13px;color:{C};word-break:break-all}}
.cap{{font-family:Inter,sans-serif;font-size:22px;line-height:1.5;color:{N}}}
</style>'''
pages=[]
def top(t): return f'<div class="top">{roundlogo(46)}<div class="nm">webclinic</div><div class="pn">{t}</div></div>'
pages.append(f'''<div class="pg"><div style="display:flex;justify-content:center;margin-top:90px">{roundlogo(210)}</div>
<div style="text-align:center;margin-top:50px"><div class="k">CONFIGURAÇÃO DO PERFIL</div><h1 style="font-size:88px;margin-top:18px">Perfil pronto<b>pra receber.</b></h1>
<div style="font-size:26px;line-height:1.5;margin:28px auto 0;max-width:780px">Foto, nome, bio, link e destaques do Instagram da Web Clinic. Fazer <b style="color:{A}">antes do primeiro post</b> do plano de postagem.</div></div></div>''')
pages.append(f'''<div class="pg">{top("ORDEM DAS TAREFAS")}<div class="k">PASSO A PASSO</div><h1 style="margin-top:12px">O que fazer<b>e onde.</b></h1>
<div class="bx" style="margin-top:28px;padding:18px 22px;font-size:20px;line-height:1.45"><b style="color:#2D7FF0">Dados confirmados pelo dono:</b> perfil <b>@webclinicbrasil</b> (é o @ que aparece nas artes) · WhatsApp <b>(51) 98906-1441</b> (link da bio e botão de contato).</div>
<div class="bx" style="margin-top:24px;padding:28px 34px"><ol>
<li><b>Foto de perfil</b> → instagram.com (navegador) → Perfil → Editar perfil → Alterar foto. Arquivo: <b>foto-perfil.png</b>.</li>
<li><b>Nome, bio e link</b> → no mesmo Editar perfil (instagram.com ou app). Copiar da página 4.</li>
<li><b>Categoria e botões de contato</b> → app do Instagram → Editar perfil → Categoria / Opções de contato. (Ou Meta Business Suite → Configurações → Contas → Instagram, se aparecer.)</li>
<li><b>Destaques</b> → <b>só pelo app do Instagram</b> (o navegador e o Business Suite não criam destaques). Ver páginas 6 e 7.</li>
<li><b>Stories dos destaques</b> podem ser publicados pelo Business Suite (Criar story → só Instagram) ou pelo app. Depois adicionar ao destaque pelo app.</li>
<li><b>Posts fixados</b> → quando forem publicados, fixar no perfil os posts <b>01, 37 e 40</b> (três dedinhos do post → Fixar no perfil).</li></ol></div>
<div class="alert" style="margin-top:20px"><b>Só Instagram.</b> Nada de publicar no Facebook, nem a Página nem stories.</div></div>''')
pages.append(f'''<div class="pg">{top("FOTO DE PERFIL")}<div class="k">FOTO DE PERFIL</div><h1 style="margin-top:12px">Logo redondo<b>da Web Clinic.</b></h1>
<div style="display:flex;gap:40px;margin-top:50px;align-items:center"><img src="../marca/logo-final/webclinic-perfil-4.png" style="width:440px;border-radius:50%;border:3px solid #E2EAF4">
<div style="flex:1;display:flex;flex-direction:column;gap:16px"><div class="bx" style="padding:18px 22px"><div class="lab">ARQUIVO</div><div class="val"><b>foto-perfil.png</b> (1080 × 1080)<br><span class="url">{RAW}foto-perfil.png</span></div></div>
<div class="bx" style="padding:18px 22px"><div class="lab">COMO SUBIR</div><div class="val">Editar perfil → Alterar foto → Carregar foto. Não recortar: o Instagram já mostra em círculo.</div></div></div></div></div>''')
fld=lambda l,v,u=False:f'<div class="bx" style="padding:20px 24px"><div class="lab">{l}</div><div class="{"cap" if u else "val"}">{esc(v)}</div></div>'
pages.append(f'''<div class="pg">{top("TEXTOS DO PERFIL")}<div class="k">COPIAR E COLAR</div><h1 style="margin-top:12px">Nome, bio<b>e link.</b></h1>
<div style="display:flex;flex-direction:column;gap:14px;margin-top:34px">
{fld("NOME (máx. 30 caracteres; aparece em negrito e entra na busca)",PERFIL["nome"],True)}
{fld("NOME DE USUÁRIO (confirmado)","@"+PERFIL["usuario"],True)}
{fld("CATEGORIA",PERFIL["categoria"])}
{fld("BIO (até 150 caracteres, manter as quebras de linha)",PERFIL["bio"],True)}
{fld("LINK",PERFIL["link"])}
{fld("BOTÕES",PERFIL["botoes"])}
</div></div>''')
# prévia do perfil
hlrow=''.join(f'<div style="text-align:center"><svg width="104" height="104" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="{G}" stroke="#D6DEE9" stroke-width="2"/>{icons[ic]}</svg><div style="font-size:15px;margin-top:4px">{nome}</div></div>' for nome,ic,_ in DEST)
grid=''.join(f'<img src="perfil-html/th/post-{n:02d}.jpg" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block">' for n in [40,39,38])
pages.append(f'''<div class="pg">{top("PRÉVIA")}<div class="k">COMO VAI FICAR</div><h1 style="margin-top:12px">Prévia<b>do perfil.</b></h1>
<div class="bx" style="margin:30px auto 0;width:620px;padding:30px 30px 0;overflow:hidden">
<div style="display:flex;align-items:center;gap:34px">{roundlogo(150)}<div style="display:flex;gap:30px;text-align:center;font-size:16px"><div><b style="font-size:22px">40</b><br>posts</div><div><b style="font-size:22px">—</b><br>seguidores</div><div><b style="font-size:22px">—</b><br>seguindo</div></div></div>
<div style="margin-top:16px;font-size:17px;line-height:1.45"><b>{esc(PERFIL["nome"])}</b><br><span style="color:{C}">Web designer</span><br>{esc(PERFIL["bio"])}</div>
<div style="display:flex;justify-content:space-between;margin:22px 0 18px">{hlrow}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin:0 -30px">{grid}</div></div></div>''')
# destaques
caps=''.join(f'<div style="text-align:center"><img src="../perfil/destaques/capa-{nome.lower()}.png" style="width:150px;height:150px;object-fit:cover;object-position:center;border-radius:50%;border:2px solid #E2EAF4"><div style="font-size:18px;font-weight:600;margin-top:8px">{nome}</div></div>' for nome,_,_ in DEST)
pages.append(f'''<div class="pg">{top("DESTAQUES · 1/2")}<div class="k">DESTAQUES</div><h1 style="margin-top:12px">5 destaques,<b>nesta ordem.</b></h1>
<div class="bx" style="margin-top:34px;padding:30px;display:flex;justify-content:space-between">{caps}</div>
<div class="bx" style="margin-top:24px;padding:28px 34px"><ol>
<li>Publicar os stories do destaque (página 7), <b>só no Instagram</b>, na ordem.</li>
<li>No app: abrir o primeiro story → <b>Destacar</b> → Novo → nome do destaque (exatamente como acima).</li>
<li>Adicionar os outros stories daquele destaque.</li>
<li>Segurar o destaque → <b>Editar destaque → Editar capa</b> → escolher <b>capa-NOME.png</b> da galeria. Centralizar (o círculo já está no meio).</li>
<li>Ordem no perfil: <b>Sobre, Sites, Agenda, Dicas, Contato</b> (o mais recente fica à esquerda: criar na ordem inversa, começando por Contato).</li></ol></div>
<div class="val" style="margin-top:18px;font-size:18px;color:{C}">Obs.: no manual de marca havia "Resultados"; troquei por <b style="color:{A}">Agenda</b> porque ainda não há resultados reais de clientes para mostrar.</div></div>''')
rows=''.join(f'<div class="bx" style="padding:16px 22px"><div class="lab">{nome.upper()} · capa-{nome.lower()}.png</div><div class="val" style="font-size:17px">'+(', '.join(s.split("/")[-1] for s in STORIES[nome]))+'</div></div>' for nome,_,posts in DEST)
pages.append(f'''<div class="pg">{top("DESTAQUES · 2/2")}<div class="k">STORIES DE CADA DESTAQUE</div><h1 style="margin-top:12px">Quais stories<b>vão em cada um.</b></h1>
<div style="display:flex;flex-direction:column;gap:12px;margin-top:30px">{rows}</div>
<div class="bx" style="margin-top:18px;padding:16px 22px"><div class="lab">ONDE ESTÃO OS ARQUIVOS</div><div class="val" style="font-size:17px">Pasta <b>webclinic/perfil/destaques/</b> do repositório DOTAGENCIA (1080 × 1920).<br><span class="url">{RAW}destaques/NOME-DO-ARQUIVO.png</span></div></div>
<div style="display:flex;gap:10px;margin-top:18px">{''.join(f'<img src="../perfil/{s}" style="width:110px;border-radius:10px;border:1px solid #E2EAF4">' for s in [STORIES["Sobre"][0],STORIES["Sites"][0],STORIES["Agenda"][0],STORIES["Dicas"][0],STORIES["Contato"][0]])}</div></div>''')
open('perfil.html','w').write(f'<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body>{"".join(pages)}</body></html>')
from PIL import Image
os.makedirs('perfil-html/th',exist_ok=True)
for n in [40,39,38]: Image.open(f'../posts/post-{n:02d}.png').convert('RGB').resize((540,675)).save(f'perfil-html/th/post-{n:02d}.jpg',quality=88)
print(len(pages),len(jobs))
