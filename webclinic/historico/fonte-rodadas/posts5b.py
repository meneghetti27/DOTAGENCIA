exec(open('posts5.py').read())
posts=[]
def img3d(src,l,t,w,extra=''): return f'<img src="{src}" style="position:absolute;left:{l}px;top:{t}px;width:{w}px;z-index:4;filter:drop-shadow(0 30px 40px rgba(45,127,240,.25));{extra}">'
# 2 agenda: 3D calendar + chips
posts.append(page(title('Sua agenda não fecha','às 18h.')+
 img3d('x-cal-c.png',300,470,480)+
 f'<div class="chip" style="left:80px;top:560px;z-index:5;transform:rotate(-3deg)"><div class="ic">{MOON}</div><div>Consulta marcada<small>Qui, 14h · agendada às 23h47</small></div></div>'+
 f'<div class="chip" style="right:70px;top:880px;z-index:5;transform:rotate(2deg)"><div class="ic">{CHECK}</div><div>Sem ligação<small>direto pelo site</small></div></div>'+
 phrase('Com agenda online no site, o paciente marca<br><b>a qualquer hora, sem precisar ligar.</b>','AGENDA ONLINE · WEBCLINIC')))
# 3 secretária: photo card + 3D handset
posts.append(page(title('Você precisa de uma secretária','só pra atender telefone?',185,62,74)+
 f'<div style="position:absolute;left:150px;top:470px;width:780px;height:520px;border-radius:40px;overflow:hidden;{TILT};{SH}"><img src="foto-medico.jpg" style="width:100%;height:100%;object-fit:cover;object-position:40% 30%"></div>'+
 img3d('x-hand-c.png',60,400,330,'transform:rotate(-12deg)')+
 f'<div class="chip" style="left:80px;top:640px;z-index:5"><div class="ic" style="background:#FFE7EA">{PH.replace("30","24")}</div><div style="color:#FA5F6D">12 chamadas perdidas<small>hoje, até as 14h</small></div></div>'+
 f'<div class="chip" style="right:70px;top:900px;z-index:5"><div class="ic">{CHECK}</div><div>Consulta confirmada<small>pela agenda online</small></div></div>'+
 phrase('A agenda online agenda, confirma e remarca.<br><b>Sua equipe cuida do que importa.</b>','AGENDA ONLINE · WEBCLINIC')))
# 5 instagram: insta post card with photo -> site card
ig=f'''<div class="bx" style="position:absolute;left:80px;top:500px;width:420px;overflow:hidden;transform:perspective(1800px) rotateY(12deg) rotateX(6deg)">
<div style="display:flex;align-items:center;gap:12px;padding:16px 18px"><div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,{L},{A});padding:3px"><div style="width:100%;height:100%;border-radius:50%;background:{M};border:2px solid #fff"></div></div><div style="font-size:17px;font-weight:600">dra.anapaula</div></div>
<img src="foto-medica.jpg" style="width:100%;height:360px;object-fit:cover;object-position:50% 25%;display:block">
<div style="padding:14px 18px;font-size:16px"><span style="font-size:22px">♡ 💬 ↗</span><div style="margin-top:6px"><b>2.481 curtidas</b></div><div style="color:{C};font-size:14px;margin-top:2px">0 consultas marcadas</div></div></div>'''
posts.append(page(title('Instagram não','marca consulta.')+ig+site_ag.replace('left:520px;top:590px','left:540px;top:600px')+arrow.replace('left:420px;top:760px','left:440px;top:780px')+
 phrase('O Instagram atrai. <b>Quem converte é o site.</b><br>O link da bio precisa levar pra uma agenda.','SITES PARA MÉDICOS · WEBCLINIC')))
# 6 pesquisa: search card + 3D magnifier
posts.append(page(title('O paciente te pesquisa','antes de ligar.')+search.replace('left:120px;top:490px;width:840px','left:80px;top:560px;width:720px')+
 img3d('x-mag-c.png',700,430,330,'transform:rotate(8deg)')+
 phrase('Se você não aparece bem na busca,<br><b>ele marca com quem aparece.</b>','SITE + GOOGLE · WEBCLINIC')))
# 7 lembrete: 3D clock + message card
msg=f'''<div class="bx" style="position:absolute;left:470px;top:560px;width:520px;padding:26px;{TILT};z-index:3">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px"><div style="width:46px;height:46px;border-radius:50%;background:{A};display:grid;place-items:center;color:#fff;font-weight:700">AP</div><div><div style="font-size:18px;font-weight:600">Clínica Dra. Ana Paula</div><div style="font-size:13px;color:{C}">lembrete automático · 24h antes</div></div></div>
<div style="background:{G};border-radius:6px 22px 22px 22px;padding:16px 18px;font-size:19px;line-height:1.45">Olá, Maria! 👋 Sua consulta é <b>amanhã, às 14h</b>, com a Dra. Ana Paula.</div>
<div style="display:flex;gap:10px;margin-top:14px"><div style="flex:1;background:{A};color:#fff;text-align:center;font-weight:600;font-size:18px;border-radius:16px;padding:13px">Confirmar</div><div style="flex:1;text-align:center;font-weight:500;font-size:18px;border-radius:16px;padding:11px;border:2px solid #E2EAF4">Remarcar</div></div></div>'''
posts.append(page(title('Paciente que esquece','a consulta?')+msg+img3d('x-clock-c.png',90,500,400,'transform:rotate(-8deg)')+
 f'<div class="chip" style="right:90px;top:920px;z-index:5"><div class="ic">{CHECK}</div><div>Maria confirmou<small>menos faltas na agenda</small></div></div>'+
 phrase('Lembrete automático pela agenda online.<br><b>Menos falta, agenda cheia.</b>','AGENDA ONLINE · WEBCLINIC')))
for n,p in zip([2,3,5,6,7],posts): open(f'p5b-{n}.html','w').write(p)
