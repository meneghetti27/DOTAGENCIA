# gera os PDFs de case do LinkedIn (1080x1350 por página)
import subprocess, os
A='../assets/'
HEAD='''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><script src="ht.js"></script>
<style>
@page{size:1080px 1350px;margin:0}
.pg{width:1080px;height:1350px;position:relative;overflow:hidden;page-break-after:always;padding:96px 90px}
.top{position:absolute;left:90px;right:90px;top:56px;display:flex;justify-content:space-between;font-size:16px;font-weight:600;color:#6E6E73}
.top b{color:#1D1D1F}
h1.d{font-size:98px}
h2.d{font-size:68px;margin-top:24px}
p.lead{font-size:28px;line-height:1.38;color:#515154;margin-top:30px;max-width:860px;font-weight:500}
p.lead b{color:#1D1D1F;font-weight:700}
.img{border-radius:22px;box-shadow:0 30px 60px -28px rgba(0,0,0,.4);display:block}
.row{display:flex;gap:28px;position:absolute;left:90px;right:90px}
.row img{flex:1;min-width:0;width:100%;object-fit:cover}
.cap{font-size:20px;color:#6E6E73;margin-top:14px;font-weight:500}
.n{font-family:Syne;font-weight:800;letter-spacing:-.04em;font-size:96px;line-height:1}
.fade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(251,251,253,0) 0,rgba(251,251,253,.65) 55%,rgba(251,251,253,.96) 100%)}
</style></head><body>'''
TAIL='''<script>document.querySelectorAll('canvas.ht').forEach((c,i)=>halftone(c,(x,y,ph)=>Math.min(.8,1.05-Math.hypot((x-.85)*1.1,(y-.18)*1.1)*1.5+Math.sin(x*8+y*5+ph*6)*.1),15))</script></body></html>'''
def top(case,n,t): return f'<div class="top"><span><b>Antônio Meneghetti</b> · Diretor de arte</span><span>{case} · {n}/{t}</span></div>'
def capa(case,titulo,sub,t,img=''):
    return f'''<div class="pg"><canvas class="ht"></canvas><div class="fade"></div>{top(case,1,t)}
<div style="position:absolute;left:90px;right:90px;bottom:120px"><div class="lbl">Case</div><h1 class="d" style="margin-top:22px">{titulo}<span class="mag">.</span></h1>
<p class="lead">{sub}</p><div style="margin-top:44px"><span class="dots"></span></div></div>{img}</div>'''
def fim(case,t):
    return f'''<div class="pg"><canvas class="ht"></canvas><div class="fade"></div>{top(case,t,t)}
<div style="position:absolute;left:90px;right:90px;bottom:140px"><h1 class="d" style="font-size:100px">Design que<br>comunica<span class="mag">.</span></h1>
<p class="lead">Antônio Meneghetti, designer e diretor de arte em Porto Alegre.<br><b>Portfólio completo e contato no meu perfil.</b></p></div></div>'''
def pg(case,n,t,body): return f'<div class="pg">{top(case,n,t)}{body}</div>'
def build(nome,pages):
    open(nome+'.html','w').write(HEAD+''.join(pages)+TAIL)
    subprocess.run(['node','render.js',nome+'.html','../out/'+nome+'.pdf','1080','1350','1'],check=True)

# ---------- Prefeitura ----------
C='Prefeitura de Porto Alegre';T=7
build('case-prefeitura-poa',[
capa(C,'Prefeitura de<br>Porto Alegre','Direção de arte da comunicação oficial da cidade, 2026.',T,
 f'<img class="img" src="{A}7bffa1c7c1.webp" style="position:absolute;right:90px;top:150px;width:360px;transform:rotate(5deg)">'),
pg(C,2,T,f'''<div class="lbl" style="margin-top:60px">O desafio</div><h2 class="d">Falar com mais de<br>1 milhão de pessoas<br>com uma linguagem só<span class="mag">.</span></h2>
<p class="lead">Serviços do 156, educação, limpeza urbana, praças, acesso à informação e as datas da cidade. Assuntos diferentes, para públicos diferentes, que precisam parecer <b>uma única Prefeitura</b>.</p>
<div class="row" style="bottom:96px;height:400px"><img class="img" src="{A}94c81e28c2.webp"><img class="img" src="{A}cdcd82974e.webp"><img class="img" src="{A}94d947562b.webp"></div>'''),
pg(C,3,T,f'''<div class="lbl" style="margin-top:60px">Serviço vira campanha</div><h2 class="d">Castração gratuita<br>pelo 156<span class="mag">.</span></h2>
<p class="lead">Um serviço público explicado em carrossel de 8 artes: <b>um rosto que para a rolagem</b> e o passo a passo sem juridiquês.</p>
<div class="row" style="bottom:96px;height:520px"><img class="img" src="{A}7bffa1c7c1.webp"><img class="img" src="{A}8d73cd25f8.webp"><img class="img" src="{A}e5bcfedb52.webp"></div>'''),
pg(C,4,T,f'''<div class="lbl" style="margin-top:60px">Informação clara</div><h2 class="d">Sem cara<br>de governo<span class="mag">.</span></h2>
<p class="lead">Títulos grandes, uma mensagem por peça e a marca da Prefeitura sempre no mesmo lugar.</p>
<div class="row" style="bottom:96px;height:600px"><img class="img" src="{A}b02e403ec6.webp"><img class="img" src="{A}e544f1e6b4.webp"></div>'''),
pg(C,5,T,f'''<div class="lbl" style="margin-top:60px">Cultura e datas da cidade</div><h2 class="d">A cidade<br>que se celebra<span class="mag">.</span></h2>
<p class="lead">Aniversário do Grêmio, concertos no Capitólio e o Dia do Patrimônio: <b>cada data com personalidade própria</b>, sem sair da linguagem.</p>
<div class="row" style="bottom:96px;height:520px"><img class="img" src="{A}00d9a1998f.webp"><img class="img" src="{A}390ed1c383.webp"><img class="img" src="{A}78f94d16d5.webp"></div>'''),
pg(C,6,T,f'''<div class="lbl" style="margin-top:60px">Resultado</div><h2 class="d">Prêmio nacional<br>na categoria<br>Identidade<span class="mag">.</span></h2>
<p class="lead">O trabalho de comunicação visual da Prefeitura foi premiado no <b>Social Media Gov</b>, na categoria Identidade.</p>
<img class="img" src="{A}96627f251b.webp" style="position:absolute;left:90px;right:90px;bottom:96px;width:900px">'''),
fim(C,T)])

# ---------- plagio.zip ----------
C='plagio.zip';T=5
reels=[('37f053bc06','671 mil','49,9 mil curtidas · 20,5 mil compartilhamentos'),('079b15a241','347 mil','28,6 mil curtidas · 14,8 mil compartilhamentos'),('350ec8da26','158 mil','visualizações')]
cards=''.join(f'<div style="flex:1"><img class="img" src="{A}{i}.webp" style="width:100%;height:470px;object-fit:cover"><div class="n" style="font-size:64px;margin-top:22px">{n}</div><div class="cap">views · {d}</div></div>' for i,n,d in reels)
grid=['0538c84000','0cb0007df9','f556efbf4a','130e40c402','0decfd3d50','9e26ed9ed8','ddf3a13b8d','a5a02b679c','dde768028b','5e7298f2ef','dab48d5f95','65bac2f7a1']
build('case-plagio-zip',[
capa(C,'plagio.zip','Projeto autoral de rap, streetwear e eventos de Porto Alegre. <b>+250 mil views por mês.</b>',T,
 f'<img class="img" src="{A}37f053bc06.webp" style="position:absolute;right:90px;top:150px;width:340px;transform:rotate(5deg)">'),
pg(C,2,T,f'''<div class="lbl" style="margin-top:60px">O projeto</div><h2 class="d">Notícia de rap<br>com cara de<br>jornal de TV<span class="mag">.</span></h2>
<p class="lead">Criei a página do zero: nome, identidade, moldura dos posts, roteiro, motion e IA generativa nos reels. Tudo feito por mim, <b>do conceito ao post agendado</b>.</p>
<div class="row" style="bottom:96px;height:420px"><img class="img" src="{A}079b15a241.webp"><img class="img" src="{A}b7cd8db5b2.webp" style="flex:.6"></div>'''),
pg(C,3,T,f'''<div class="lbl" style="margin-top:60px">Números</div><h2 class="d">Reels que<br>viajaram<span class="mag">.</span></h2>
<div class="row" style="bottom:110px">{cards}</div>'''),
pg(C,4,T,f'''<div class="lbl" style="margin-top:60px">Feed</div><h2 class="d">Uma moldura,<br>reconhecível de longe<span class="mag">.</span></h2>
<div style="position:absolute;left:90px;right:90px;bottom:96px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px">{''.join(f'<img class="img" src="{A}{g}.webp" style="width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:14px">' for g in grid)}</div>'''),
fim(C,T)])

# ---------- Campanhas ----------
C='Campanhas';T=4
build('case-campanhas',[
capa(C,'Campanhas','Olympikus + Maratona Internacional de Porto Alegre e os museus do Inter e do Grêmio, com a Prefeitura.',T,
 f'<img class="img" src="{A}8df309b71d.webp" style="position:absolute;right:90px;top:170px;width:560px;transform:rotate(4deg)">'),
pg(C,2,T,f'''<div class="lbl" style="margin-top:60px">Olympikus + Maratona</div><h2 class="d">Reta final<br>de inscrições<span class="mag">.</span></h2>
<p class="lead">Peças da última chamada da Maratona Internacional de Porto Alegre, em parceria com a Olympikus: <b>urgência sem perder a marca</b>.</p>
<img class="img" src="{A}8df309b71d.webp" style="position:absolute;left:90px;bottom:96px;width:900px">'''),
pg(C,3,T,f'''<div class="lbl" style="margin-top:60px">Museu do Inter e Museu do Grêmio</div><h2 class="d">Dois rivais,<br>uma campanha<span class="mag">.</span></h2>
<p class="lead">Divulgação dos museus dos dois clubes com a Prefeitura. O desafio: <b>dar a cada um a própria personalidade</b> sem quebrar a linguagem da campanha.</p>
<img class="img" src="{A}62eb568f37.webp" style="position:absolute;left:90px;bottom:420px;width:600px;transform:rotate(-2deg)"><img class="img" src="{A}721e599824.webp" style="position:absolute;right:90px;bottom:96px;width:600px;transform:rotate(2deg)">'''),
fim(C,T)])
