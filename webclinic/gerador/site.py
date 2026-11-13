# Gera o site da Web Clinic (../site/index.html) a partir de site-modelo.html, com vetores e logo do gerador.
import re, json, urllib.parse, os
_s=open('posts40.py').read(); exec(_s[:_s.index('P=[]')])
html=open('site-modelo.html').read()
MSG='Olá! Vim pelo site da Web Clinic e quero saber mais sobre um site para o meu consultório.'
ZAP='https://wa.me/5551989061441?text='+urllib.parse.quote(MSG)
ZAPICO='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1.2-1.4-2-1-1 .8a4 4 0 0 1-2.1-2.1l.8-1-1-2z" fill="currentColor" stroke="none"/></svg>'
def ico(n,s): return f'<svg width="{s}" height="{s}" viewBox="0 0 200 200" aria-hidden="true">{V[n]}</svg>'
logo=roundlogo(240).replace('width="240" height="240"','width="100%" height="100%"')
faixa=''.join(f'<span>{ico(n,30)}{t}</span>' for n,t in [('drop','Dermatologia'),('baby','Pediatria'),('heart','Cardiologia'),('tooth','Odontologia'),('bone','Ortopedia'),('apple','Nutrição'),('brain','Psicologia'),('steth','Clínica geral'),('pulse','Fisioterapia')])
def card(tag,a,b,url,ic,d):
    return f'''<div class="rv d{d}"><div class="nav-b"><div class="barra"><i style="background:#FA5F6D"></i><i style="background:#F5B83D"></i><i style="background:#3CC48A"></i><div class="url">🔒 {url}</div></div>
<div class="site"><div><div class="tg">{tag}</div><h4><b>{a}</b> {b}</h4><div class="ln" style="width:90%"></div><div class="ln" style="width:62%"></div><span class="mini-btn">Agendar consulta</span></div><div class="foto">{ico(ic,64)}</div></div></div></div>'''
vitrine=card('PEDIATRIA','Cuidado','desde o primeiro dia.','drjoaoped.com.br','baby',0)+card('ODONTOLOGIA','Sorriso','sem medo de dentista.','clinicasorrir.com.br','tooth',1)+card('NUTRIÇÃO','Comer bem','sem dieta impossível.','nutricarla.com.br','apple',2)
FAQ=[('Quanto tempo leva pra ficar pronto?','Depende do tamanho do projeto. Na primeira conversa a gente entende o que você precisa e já te passa o prazo certinho.'),
('Preciso ter domínio e hospedagem?','Não. A gente cuida de tudo: domínio, hospedagem, cadeado de segurança e configuração. Se você já tiver um domínio, usamos o seu.'),
('Funciona para clínica com vários profissionais?','Sim. O site e a agenda podem ter vários profissionais e especialidades, cada um com seus horários.'),
('Vocês configuram meu perfil no Google?','Sim. Configuramos e otimizamos o seu Perfil da Empresa no Google, pra você aparecer na busca e no Maps da sua região.'),
('Já tenho um site. Vale a pena trocar?','A gente analisa o seu site atual sem compromisso e te mostra o que muda pra ele virar consulta marcada.'),
('Os textos respeitam as regras de publicidade?','Sim. Escrevemos pensando nas normas do seu conselho profissional: informação clara, sem promessa de resultado e sem sensacionalismo.')]
faq=''.join(f'<details class="rv"><summary>{q}<i></i></summary><p>{a}</p></details>' for q,a in FAQ)
rep={'{{logo}}':logo,'{{logobig}}':logo,'{{zap}}':ZAP.replace('&','&amp;'),'{{zapico}}':ZAPICO,'{{faixa}}':faixa,'{{vitrine}}':vitrine,'{{faq}}':faq}
for k,v in rep.items(): html=html.replace(k,v)
html=re.sub(r'\{\{ic:(\w+):(\d+)\}\}',lambda m:ico(m.group(1),int(m.group(2))),html)
html=html.replace('.marca .lg{','.marca .lg{display:block;')
assert '{{' not in html, re.findall(r'\{\{[^}]*\}\}',html)
os.makedirs('../site',exist_ok=True)
open('../site/index.html','w').write(html)
open('../site/vercel.json','w').write('{ "cleanUrls": true }\n')
open('../site/favicon.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="#fff" stroke="#E2EAF4" stroke-width="2"/><path d="M8 34h16l4-10 6 20 5-14 3 4h14" fill="none" stroke="#2D7FF0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
# imagem de compartilhamento (og.png, 1200x630)
og=f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>html,body{{width:1200px;height:630px;overflow:hidden;background:radial-gradient(900px 500px at 80% 30%,rgba(45,127,240,.45),transparent 65%),linear-gradient(180deg,#040917,#0B1F3A)}}</style></head><body>
<div style="position:absolute;left:80px;top:70px;display:flex;align-items:center;gap:16px;color:#fff;font-size:30px;font-weight:600"><div style="width:64px;height:64px">{logo}</div>webclinic</div>
<div style="position:absolute;left:80px;top:200px;color:#fff;font-size:70px;line-height:1;letter-spacing:-.05em;font-weight:300;width:700px">Seu paciente está te procurando<b style="display:block;font-weight:700;background:linear-gradient(100deg,#fff,#5AA2FF);-webkit-background-clip:text;color:transparent">no Google agora.</b></div>
<div style="position:absolute;left:80px;top:480px;color:rgba(255,255,255,.65);font-size:26px">Sites para médicos que viram consulta marcada.</div>
<div style="position:absolute;right:70px;top:150px;width:330px;height:330px;border-radius:50%;box-shadow:0 0 120px rgba(45,127,240,.7)">{logo}</div></body></html>'''
open('og.html','w').write(og)
print('ok', len(html)//1024, 'KB')
