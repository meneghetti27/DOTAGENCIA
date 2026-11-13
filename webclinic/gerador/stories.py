# Stories dos destaques (1080x1920), visuais: pouco texto, vetores grandes, elementos de site
_s=open('posts40.py').read(); exec(_s[:_s.index('P=[]')])
import os
os.makedirs('stories-html',exist_ok=True)
W='#fff'
CSS=f'''<link rel="stylesheet" href="../base.css"><style>
html,body{{width:1080px;height:1920px;overflow:hidden}}
.bx{{background:#fff;border:2px solid #E2EAF4;border-radius:36px;box-shadow:0 40px 80px -16px rgba(45,127,240,.26),0 10px 22px -8px rgba(11,31,58,.12)}}
.chip{{position:absolute;display:flex;align-items:center;gap:18px;background:#fff;border:2px solid #E2EAF4;border-radius:30px;padding:20px 28px;font-size:30px;font-weight:600;line-height:1.2;color:{N};box-shadow:0 30px 60px -10px rgba(45,127,240,.28),0 8px 18px -6px rgba(11,31,58,.12)}}
.chip .ic{{width:68px;height:68px;border-radius:20px;background:{G};display:grid;place-items:center}} .chip small{{display:block;font-size:21px;font-weight:400;color:{C}}}
.T{{position:absolute;left:80px;right:80px;letter-spacing:-.045em;line-height:.98}}
.T .a{{font-weight:300}} .T .b{{font-weight:700}}
.kick{{position:absolute;left:80px;font-size:24px;letter-spacing:.26em;font-weight:600}}
.blob{{position:absolute;border-radius:50%;filter:blur(70px)}}
</style>'''
def hdr(dark=False,n='',tot=''):
    c='#fff' if dark else N
    return f'''<div style="position:absolute;top:230px;left:80px;right:80px;display:flex;align-items:center;gap:16px">{roundlogo(64)}<div style="font-size:28px;font-weight:600;color:{c}">webclinic</div>
<div style="margin-left:auto;display:flex;gap:8px">{"".join(f'<i style="width:{46 if i==n else 14}px;height:14px;border-radius:9px;background:{(A if not dark else "#fff") if i==n else (M if not dark else "rgba(255,255,255,.3)")}"></i>' for i in range(1,tot+1)) if tot else ""}</div></div>'''
def T(a,b,top,fa=110,fb=128,ca=N,cb=A,align='left'):
    return f'<div class="T" style="top:{top}px;text-align:{align}"><div class="a" style="font-size:{fa}px;color:{ca}">{a}</div><div class="b" style="font-size:{fb}px;color:{cb}">{b}</div></div>'
def kick(t,top,c=A): return f'<div class="kick" style="top:{top}px;color:{c}">{t}</div>'
def ico(n,l,t,s,rot=0,bg='#fff',r=.28,z=4,extra=''):
    return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{s}px;height:{s}px;border-radius:{s*r:.0f}px;display:grid;place-items:center;transform:rotate({rot}deg);z-index:{z};background:{bg};{extra}">{ic(n,int(s*.66))}</div>'
def chp(l,t,icon,txt,sub,rot=0,side='left',z=6):
    return f'<div class="chip" style="{side}:{l}px;top:{t}px;z-index:{z};transform:rotate({rot}deg)"><div class="ic">{ic(icon,44)}</div><div>{txt}<small>{sub}</small></div></div>'
def cursor(l,t,s=1.6,c=N): return f'<svg style="position:absolute;left:{l}px;top:{t}px;z-index:9;filter:drop-shadow(0 10px 12px rgba(11,31,58,.25))" width="{36*s:.0f}" height="{50*s:.0f}" viewBox="-3 -3 33 46"><path d="{CUR}" fill="{c}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>'
def pulse(top,c=A,op=1,sw=5): return f'<div style="position:absolute;left:-40px;right:-40px;top:{top}px;opacity:{op}">{PULSE_BIG(1160,c,sw)}</div>'
def bigbtn(t,sz=40): return f'<span style="display:inline-block;background:{A};color:#fff;font-weight:600;font-size:{sz}px;border-radius:99px;padding:{sz*.6:.0f}px {sz*1.3:.0f}px">{t}</span>'
def foot(t,c=C): return f'<div style="position:absolute;bottom:250px;left:80px;right:80px;font-size:30px;line-height:1.4;color:{c}">{t}</div>'
def browser(inner,url,l,t,w,h=None,tilt='',z=3):
    return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{w}px;{f"height:{h}px;" if h else ""}overflow:hidden;{tilt};z-index:{z}">{bar(url).replace("height:54px","height:70px").replace("font-size:15px","font-size:20px").replace("height:30px","height:40px")}{inner}</div>'
def doc(body,bg=G): return f'<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body style="background:{bg}">{body}<div class="grain" style="opacity:.05"></div></body></html>'
TL='transform:perspective(2200px) rotateY(-14deg) rotateX(7deg)'
TR='transform:perspective(2200px) rotateY(14deg) rotateX(7deg)'
S={}
# ---------------- SOBRE ----------------
S['sobre']=[
doc(hdr(True,1,3)+f'<div class="blob" style="width:900px;height:900px;left:90px;top:520px;background:{A};opacity:.45"></div>'+
 f'<div style="position:absolute;left:290px;top:560px;z-index:3">{roundlogo(500)}</div>'+
 ico('calendar',90,470,210,-10)+ico('heart',780,540,190,9)+ico('zoom',110,930,170,8)+ico('steth',810,910,190,-7)+
 T('Sites para','médicos.',1210,120,140,'#fff',L)+pulse(1420,L,.8,4)+foot('e profissionais da saúde.','#9FB3CF').replace('bottom:250px','bottom:200px'),N),
doc(hdr(False,2,3)+kick('O QUE A GENTE FAZ',380)+T('Três coisas,','bem feitas.',430,96,112)+
 f'<div class="bx" style="position:absolute;left:80px;top:760px;width:760px;height:250px;display:flex;align-items:center;gap:40px;padding:0 44px;{TL};z-index:3">{ic("computer",170)}<div><div style="font-size:24px;letter-spacing:.2em;color:{A};font-weight:600">01</div><div style="font-size:56px;font-weight:700;letter-spacing:-.03em">Site</div></div></div>'+
 f'<div class="bx" style="position:absolute;left:240px;top:1060px;width:760px;height:250px;display:flex;align-items:center;gap:40px;padding:0 44px;{TL};z-index:4">{ic("calendar",170)}<div><div style="font-size:24px;letter-spacing:.2em;color:{A};font-weight:600">02</div><div style="font-size:56px;font-weight:700;letter-spacing:-.03em">Agenda online</div></div></div>'+
 f'<div class="bx" style="position:absolute;left:80px;top:1360px;width:760px;height:250px;display:flex;align-items:center;gap:40px;padding:0 44px;{TL};z-index:5">{ic("zoom",170)}<div><div style="font-size:24px;letter-spacing:.2em;color:{A};font-weight:600">03</div><div style="font-size:56px;font-weight:700;letter-spacing:-.03em">Google</div></div></div>'+
 cursor(780,1480,2.2)),
doc(hdr(True,3,3)+kick('PRA QUEM',380,'#CFE6F7')+T('Toda a área','da saúde.',430,100,120,'#fff','#fff')+
 ''.join(ico(n,100+(i%3)*310,720+(i//3)*300,260,[-6,4,-3,5,-5,3,6,-4,2][i]) for i,n in enumerate(['steth','tooth','apple','bone','brain','baby','drop','heart','pulse']))+
 foot('Médicos, dentistas, nutris, fisios, psicólogos…','#DCEBFB'),A),
]
# ---------------- SITES ----------------
hero=f'''<div style="padding:50px 52px"><div style="font-size:20px;font-weight:600;letter-spacing:.22em;color:{A}">DERMATOLOGIA</div>
<div style="font-size:62px;line-height:1.04;letter-spacing:-.035em;margin:18px 0 26px"><b>Pele saudável</b><span style="font-weight:300"> começa na consulta certa.</span></div>
<div style="height:16px;border-radius:9px;background:{G};width:90%;margin-bottom:14px"></div><div style="height:16px;border-radius:9px;background:{G};width:64%"></div>
<div style="margin-top:40px">{bigbtn("Agendar consulta",34)}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:46px">{"".join(f'<div style="height:150px;border-radius:24px;background:{c};display:grid;place-items:center">{ic(n,90)}</div>' for n,c in [("steth",G),("calendar",G),("pin",G)])}</div></div>'''
mob=f'''<div style="padding:84px 30px 0"><div style="font-size:16px;font-weight:600;letter-spacing:.2em;color:{A}">PEDIATRIA</div><div style="font-size:38px;line-height:1.06;letter-spacing:-.03em;margin:10px 0 18px"><b>Cuidado</b><span style="font-weight:300"> desde o primeiro dia.</span></div>
<div style="height:150px;border-radius:24px;background:{G};display:grid;place-items:center">{ic("baby",120)}</div>
<div style="margin-top:22px;background:{A};color:#fff;text-align:center;font-weight:600;font-size:24px;border-radius:99px;padding:18px">Agendar consulta</div>
<div style="margin-top:12px;border:2px solid #E2EAF4;text-align:center;font-weight:600;font-size:22px;border-radius:99px;padding:15px">WhatsApp</div>
<div style="display:flex;gap:12px;margin-top:22px">{"".join(f'<div style="flex:1;border-radius:20px;background:{G};padding:16px 0;text-align:center">{ic(n,54)}<div style="font-size:15px;font-weight:600;margin-top:4px">{t}</div></div>' for n,t in [("pin","Endereço"),("star","Avaliações"),("calendar","Horários")])}</div></div>'''
old=f'''<div style="padding:34px;filter:grayscale(1);opacity:.75"><div style="display:flex;gap:10px;flex-wrap:wrap">{"".join(f'<span style="font-size:15px;background:#E5E8EE;padding:6px 10px">{t}</span>' for t in ["Home","Quem somos","Serviços","Convênios","Blog","Galeria","Notícias","Contato"])}</div>
<div style="margin-top:20px;font-family:Times New Roman,serif;font-size:30px">Bem-vindo ao site oficial da Clínica</div><div style="margin-top:12px;font-size:15px;line-height:1.5;color:#777">Lorem ipsum dolor sit amet, texto longo sem foco, sem botão, sem horário, sem mapa, sem nada para o paciente fazer…</div>
<div style="display:flex;gap:10px;margin-top:16px">{"".join('<div style="flex:1;height:90px;background:#DADDE3"></div>' for _ in range(3))}</div></div>'''
new=f'''<div style="padding:40px 44px"><div style="font-size:42px;line-height:1.06;letter-spacing:-.03em"><b>Ortopedia</b><span style="font-weight:300"> pra voltar a se mexer sem dor.</span></div><div style="margin-top:26px">{bigbtn("Agendar consulta",28)}</div></div>'''
S['sites']=[
doc(hdr(False,1,4)+T('Seu site,','assim.',380,110,140)+
 f'<div class="blob" style="width:800px;height:700px;left:140px;top:820px;background:{L};opacity:.35"></div>'+
 browser(hero,'draanapaula.com.br',70,700,900,None,TL)+cursor(470,1170,2.2)+
 chp(70,1520,'tick','Nova consulta marcada','agora, pelo site',-3,'right')),
doc(hdr(True,2,4)+T('Pensado pro','celular.',380,104,130,'#fff',L)+
 f'<div class="blob" style="width:760px;height:900px;left:160px;top:760px;background:{A};opacity:.5"></div>'+
 phone(mob,290,720,460,900,TR,1.08)+
 chp(40,1200,'speed','Abre rápido','sem travar',-4)+chp(40,1500,'chat','WhatsApp','a um toque',3,'right'),N),
doc(hdr(False,3,4)+T('Antes','e depois.',380,110,130)+
 f'<div style="position:absolute;left:80px;top:640px;font-size:24px;letter-spacing:.24em;font-weight:600;color:{R}">ANTES</div>'+
 browser(old,'clinica-site-antigo.com.br/home.html',80,690,820,None,'transform:rotate(-2deg)')+ico('x',830,640,130,8,'#fff',.5)+
 f'<div style="position:absolute;left:180px;top:1150px;font-size:24px;letter-spacing:.24em;font-weight:600;color:{A};z-index:5">DEPOIS</div>'+
 browser(new,'ortopediajoao.com.br',180,1200,820,None,'transform:rotate(2deg)',5)+ico('tick',110,1360,150,-8,'#fff',.5,7)),
doc(hdr(True,4,4)+f'<div class="blob" style="width:900px;height:900px;left:90px;top:480px;background:{A};opacity:.4"></div>'+
 f'<div style="position:absolute;left:190px;top:520px;width:700px;height:700px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 50px 100px -20px rgba(0,0,0,.4)">{ic("speed",470)}</div>'+
 T('Leve.','Rápido. No ar.',1310,120,120,'#fff',L)+foot('Site que abre na hora, no Google e no celular.','#9FB3CF'),N),
]
# ---------------- AGENDA ----------------
days=''.join(f'<div style="flex:1;text-align:center;padding:18px 0;border-radius:24px;{"background:"+A+";color:#fff" if d=="Qui" else "background:"+G}"><div style="font-size:20px;opacity:.75">{d}</div><div style="font-size:36px;font-weight:600">{n}</div></div>' for d,n in [("Seg",10),("Ter",11),("Qua",12),("Qui",13),("Sex",14)])
slots=''.join(f'<div style="padding:22px 0;text-align:center;border-radius:22px;font-size:30px;font-weight:500;{"background:"+A+";color:#fff" if s=="14:00" else "border:2px solid #E2EAF4;color:"+(N if s not in ("09:00","15:30") else "#B5C0D0")}">{s}</div>' for s in ["08:00","09:00","10:30","11:00","14:00","15:30"])
calbig=f'<div style="padding:48px 48px 52px"><div style="font-size:22px;letter-spacing:.2em;color:{A};font-weight:600">AGENDAR CONSULTA</div><div style="font-size:44px;font-weight:700;margin:8px 0 30px;letter-spacing:-.02em">Dra. Ana Paula</div><div style="display:flex;gap:12px;margin-bottom:26px">{days}</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">{slots}</div></div>'
bub=lambda t,me=False,sz=30:f'<div style="max-width:84%;{"margin-left:auto;background:#DCEBFB;border-radius:30px 8px 30px 30px" if me else "background:"+G+";border-radius:8px 30px 30px 30px"};padding:24px 28px;font-size:{sz}px;line-height:1.4;margin-top:20px">{t}</div>'
chat=f'''<div style="padding:40px 40px 46px"><div style="display:flex;align-items:center;gap:18px;padding-bottom:24px;border-bottom:2px solid #EEF2F7"><div style="width:76px;height:76px;border-radius:50%;background:{A};display:grid;place-items:center;color:#fff;font-weight:700;font-size:28px">AP</div><div><div style="font-size:30px;font-weight:600">Clínica Dra. Ana Paula</div><div style="font-size:22px;color:{C}">mensagem automática</div></div></div>
{bub("Olá, Maria! Sua consulta é <b>amanhã, às 14h</b>.")}{bub("Confirma presença?",sz=30)}
<div style="display:flex;gap:16px;margin-top:26px"><div style="flex:1;background:{A};color:#fff;text-align:center;font-weight:600;font-size:30px;border-radius:24px;padding:22px">Confirmar</div><div style="flex:1;text-align:center;font-weight:500;font-size:30px;border-radius:24px;padding:20px;border:2px solid #E2EAF4">Remarcar</div></div></div>'''
flow=[('zoom','Google','acha você'),('computer','Site','conhece'),('calendar','Agenda','escolhe o horário'),('heart','Paciente','na sua cadeira')]
S['agenda']=[
doc(hdr(False,1,4)+T('O paciente','escolhe.',380,110,140)+
 f'<div class="blob" style="width:820px;height:700px;left:130px;top:900px;background:{L};opacity:.35"></div>'+
 f'<div class="bx" style="position:absolute;left:80px;top:730px;width:920px;{TL};z-index:3">{calbig}</div>'+cursor(560,1230,2.4)+
 chp(60,1520,'tick','Consulta marcada','Qui, 13 · 14h',-3,'right')),
doc(hdr(True,2,4)+f'<div class="blob" style="width:900px;height:900px;left:90px;top:440px;background:{A};opacity:.35"></div>'+
 f'<div style="position:absolute;left:240px;top:480px">{ic("moon",600)}</div>'+''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:#fff;opacity:{o}"></div>' for x,y,s,o in [(150,560,10,.8),(900,700,14,.6),(820,470,8,.9),(200,1000,12,.5),(950,1080,9,.7)])+
 chp(80,1060,'calendar','Consulta marcada','agendada às 23h47',-3)+
 T('Agenda aberta','até de madrugada.',1290,96,92,'#fff',L),N),
doc(hdr(False,3,4)+T('Lembrete','automático.',380,110,130)+
 f'<div class="bx" style="position:absolute;left:80px;top:740px;width:920px;{TR};z-index:3">{chat}</div>'+ico('bell',800,640,190,10,z=6)+
 chp(70,1450,'tick','Maria confirmou','menos falta na agenda',2,'left')),
doc(hdr(True,4,4)+T('Do Google','à consulta.',380,104,128,'#fff',L)+
 f'<div style="position:absolute;left:186px;top:760px;width:6px;height:900px;background:repeating-linear-gradient({L} 0 18px,transparent 18px 34px)"></div>'+
 ''.join(f'<div style="position:absolute;left:80px;top:{720+i*240}px;display:flex;align-items:center;gap:40px;z-index:3"><div class="bx" style="width:220px;height:220px;border-radius:60px;display:grid;place-items:center;border:none">{ic(n,140)}</div><div><div style="font-size:24px;letter-spacing:.22em;color:{L};font-weight:600">0{i+1}</div><div style="font-size:60px;font-weight:700;color:#fff;letter-spacing:-.03em;line-height:1.05">{t}</div><div style="font-size:30px;color:#9FB3CF">{s}</div></div></div>' for i,(n,t,s) in enumerate(flow)),N),
]
# ---------------- DICAS ----------------
def dica(n,a,b,body,bg=G,dark=False):
    return doc(hdr(dark,n,4)+f'<div style="position:absolute;left:66px;top:330px;font-size:300px;font-weight:700;letter-spacing:-.06em;line-height:1;color:transparent;-webkit-text-stroke:4px {L if dark else M}">0{n}</div>'+
      kick('DICA 0'+str(n),680,L if dark else A)+T(a,b,730,96,112,'#fff' if dark else N,L if dark else A)+f'<div style="position:absolute;inset:0;transform:translateY(150px)">{body}</div>',bg)
topo=f'''<div style="padding:30px 44px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #EEF2F7"><div style="font-size:30px;font-weight:700">Dra. Ana Paula</div>{bigbtn("Agendar",26)}</div>
<div style="padding:40px 44px">{"".join(f'<div style="height:18px;border-radius:9px;background:{G};width:{w}%;margin-bottom:16px"></div>' for w in [92,80,66])}<div style="height:220px;border-radius:26px;background:{G};margin-top:26px"></div></div>'''
mapa=f'''<div style="height:470px;position:relative;background:{G};overflow:hidden"><svg width="920" height="470" style="position:absolute;inset:0"><path d="M0 120H920M0 330H920M210 0V470M640 0V470" stroke="#fff" stroke-width="34"/><path d="M0 460L920 40" stroke="#fff" stroke-width="22"/><rect x="260" y="160" width="330" height="130" rx="18" fill="{M}" opacity=".6"/></svg><div style="position:absolute;left:340px;top:60px">{ic("pin",240)}</div></div>
<div style="padding:30px 40px;display:flex;align-items:center;justify-content:space-between"><div><div style="font-size:32px;font-weight:700">Clínica Bem Estar</div><div style="font-size:24px;color:{C}">Rua das Flores, 120 · Centro</div></div>{bigbtn("Rotas",26)}</div>'''
S['dicas']=[
dica(1,'Botão de agendar','no topo.',browser(topo,'draanapaula.com.br',80,860,920,None,TL)+cursor(870,1035,2.2)+
 f'<div style="position:absolute;left:700px;top:915px;width:320px;height:140px;border-radius:99px;border:5px dashed {A};z-index:8"></div>'+chp(80,1380,'cursor','1 toque','e já marcou',-3)),
dica(2,'Foto real,','não de banco.',photo('../px-a.jpg',140,850,800,620,'50% 25%',TR)+chp(60,1340,'shield','Dr. Rafael Lima','CRM 00000 · Ortopedia',-3)+ico('tick',820,800,150,8,'#fff',.5,6)),
dica(3,'Endereço','com mapa.',browser(mapa,'clinicabemestar.com.br/contato',80,860,920,None,TR)),
dica(4,'WhatsApp','à vista.',f'<div class="blob" style="width:700px;height:700px;left:190px;top:900px;background:{A};opacity:.45"></div>'+
 f'<div style="position:absolute;left:250px;top:830px;width:520px;height:520px;border-radius:50%;background:#fff;display:grid;place-items:center">{ic("chat",380)}</div>'+
 f'<div style="position:absolute;left:0;right:0;top:1400px;text-align:center;z-index:5">{bigbtn("Falar no WhatsApp",36)}</div>'+cursor(700,1450,2.2,N),N,True),
]
# ---------------- CONTATO ----------------
dm=f'''<div style="display:flex;align-items:center;gap:20px;background:#fff;border-radius:99px;padding:18px 18px 18px 40px;font-size:40px;color:{N}"><span style="flex:1"><b>SITE</b><span style="display:inline-block;width:3px;height:44px;background:{A};margin-left:6px;vertical-align:middle"></span></span>
<span style="width:96px;height:96px;border-radius:50%;background:{A};display:grid;place-items:center"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M4 12l16-8-6 16-3-7z" fill="#fff"/></svg></span></div>'''
S['contato']=[
doc(hdr(True,1,1)+f'<div class="blob" style="width:900px;height:800px;left:90px;top:520px;background:{L};opacity:.6"></div>'+
 f'<div style="position:absolute;left:290px;top:440px;z-index:3">{roundlogo(500)}</div>'+ico('calendar',110,520,190,-10)+ico('chat',790,780,190,9)+
 T('Vamos encher','sua agenda?',990,96,124,'#fff','#fff')+
 kick('MANDE NO DIRECT',1300,'#DCEBFB')+f'<div style="position:absolute;left:80px;right:80px;top:1360px">{dm}</div>'+
 f'<div style="position:absolute;left:80px;right:80px;top:1530px;display:flex;align-items:center;gap:22px;color:#fff;font-size:40px;font-weight:600"><span style="width:96px;height:96px;border-radius:50%;background:#fff;display:grid;place-items:center">{ic("chat",60)}</span><span><span style="display:block;font-size:22px;letter-spacing:.24em;font-weight:600;color:#DCEBFB">OU NO WHATSAPP</span>(51) 98906-1441</span></div>',A),
]
jobs=[]
for k,lst in S.items():
    for i,h in enumerate(lst,1):
        open(f'stories-html/{k}-{i}.html','w').write(h); jobs.append(f'{k}-{i}.html')
open('stories-jobs.txt','w').write('\n'.join(jobs)); print(len(jobs))
