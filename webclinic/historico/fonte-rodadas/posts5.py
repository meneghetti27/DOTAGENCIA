exec(open('posts3.py').read().split('# POST 1')[0])
TILT='transform:perspective(1800px) rotateY(-12deg) rotateX(6deg)'
TILTR='transform:perspective(1800px) rotateY(12deg) rotateX(6deg)'
SH='box-shadow:0 30px 60px -10px rgba(45,127,240,.22),0 8px 18px -6px rgba(11,31,58,.10)'
def title(a,b,top=190,fa=76,fb=100): return f'<div class="t" style="top:{top}px"><div class="a" style="font-size:{fa}px">{a}</div><div class="b" style="font-size:{fb}px">{b}</div></div>'
def phone(inner,l,t,w=400,h=760,tilt=TILT,z=.8): return f'<div style="position:absolute;zoom:{z};left:{l/z:.0f}px;top:{t/z:.0f}px;width:{w}px;height:{h}px;border-radius:64px;background:{N};padding:16px;{tilt};{SH}"><div style="width:100%;height:100%;border-radius:50px;background:#fff;overflow:hidden;position:relative"><div style="position:absolute;top:14px;left:50%;transform:translateX(-50%);width:110px;height:30px;border-radius:20px;background:{N}"></div>{inner}</div></div>'
def bar(url): return f'<div style="height:54px;background:{G};display:flex;align-items:center;gap:9px;padding:0 22px;border-bottom:2px solid #E2EAF4"><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i><div style="margin-left:16px;flex:1;height:30px;border-radius:99px;background:#fff;border:2px solid #E2EAF4;font-size:15px;color:{C};display:flex;align-items:center;padding:0 14px">{url}</div></div>'
def phrase(t,src): return f'<div class="ph">{t}</div><div class="src">{src}</div>'
MOON=f'<svg width="26" height="26" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="{A}"/></svg>'
posts=[]
# 2 agenda
days=''.join(f'<div style="flex:1;text-align:center;padding:10px 0;border-radius:16px;{"background:"+A+";color:#fff" if d=="Qui" else ""}"><div style="font-size:13px;opacity:.7">{d}</div><div style="font-size:22px;font-weight:600">{n}</div></div>' for d,n in [("Seg",10),("Ter",11),("Qua",12),("Qui",13),("Sex",14)])
slots=''.join(f'<div style="padding:12px 0;text-align:center;border-radius:14px;font-size:18px;font-weight:500;{"background:"+A+";color:#fff" if s=="14:00" else "border:2px solid #E2EAF4;color:"+(N if s not in ("09:00","15:30") else "#B5C0D0")}">{s}</div>' for s in ["08:00","09:00","10:30","11:00","14:00","15:30","16:00","17:30"])
cal=f'''<div style="padding:66px 26px 0"><div style="font-size:14px;letter-spacing:.2em;color:{A};font-weight:600">AGENDAR CONSULTA</div><div style="font-size:26px;font-weight:700;margin:6px 0 2px;letter-spacing:-.02em">Dra. Ana Paula</div><div style="font-size:16px;color:{C}">Dermatologia · Novembro</div>
<div style="display:flex;gap:6px;margin:22px 0">{days}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{slots}</div>
<div style="margin-top:22px;background:{A};color:#fff;text-align:center;font-weight:600;font-size:20px;border-radius:99px;padding:15px">Confirmar horário</div></div>'''
posts.append(page(title('Sua agenda não fecha','às 18h.')+phone(cal,380,460,400,740)+
 f'<div class="chip" style="left:90px;top:640px;z-index:5"><div class="ic">{MOON}</div><div>Consulta marcada<small>Qui, 14h · agendada às 23h47</small></div></div>'+
 f'<div class="chip" style="right:80px;top:930px;z-index:5"><div class="ic">{CHECK}</div><div>Sem ligação<small>direto pelo site</small></div></div>'+
 phrase('Com agenda online no site, o paciente marca<br><b>a qualquer hora, sem precisar ligar.</b>','AGENDA ONLINE · WEBCLINIC')))
# 3 secretária
PH=f'<svg width="30" height="30" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2" fill="#FA5F6D"/></svg>'
calls=''.join(f'<div style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #EEF2F7"><div style="width:38px;height:38px;border-radius:50%;background:#FFE7EA;display:grid;place-items:center"><svg width="18" height="18" viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2" fill="#FA5F6D"/></svg></div><div style="flex:1"><div style="font-size:17px;font-weight:600;color:#FA5F6D">{n}</div><div style="font-size:13px;color:{C}">Chamada perdida</div></div><div style="font-size:14px;color:{C}">{h}</div></div>' for n,h in [("(51) 9 8812-...","08:12"),("(51) 9 9734-...","09:47"),("(51) 9 9120-...","11:05"),("(51) 9 8456-...","12:30"),("(51) 9 9901-...","13:58")])
phone_calls=f'<div style="padding:70px 24px 0"><div style="display:flex;align-items:center;justify-content:space-between"><div style="font-size:26px;font-weight:700">Recentes</div><div style="background:#FA5F6D;color:#fff;font-size:16px;font-weight:600;border-radius:99px;padding:5px 14px">12 perdidas</div></div><div style="margin-top:12px">{calls}</div></div>'
site_ok=f'''<div class="bx" style="position:absolute;left:470px;top:640px;width:520px;height:390px;overflow:hidden;{TILT};z-index:4">{bar('draanapaula.com.br/agendar')}
<div style="padding:36px 38px"><div style="width:70px;height:70px;border-radius:50%;background:{G};display:grid;place-items:center"><svg width="36" height="36" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10" fill="none" stroke="{A}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div style="font-size:34px;font-weight:700;letter-spacing:-.02em;margin-top:18px">Consulta confirmada</div><div style="font-size:19px;color:{C};margin-top:6px">Qui, 13 nov · 14h · Dra. Ana Paula</div>
<div style="display:flex;gap:10px;margin-top:24px"><span style="background:{A};color:#fff;font-weight:600;font-size:17px;border-radius:99px;padding:10px 20px">Adicionar à agenda</span><span style="border:2px solid #E2EAF4;font-weight:500;font-size:17px;border-radius:99px;padding:8px 18px">Remarcar</span></div></div></div>'''
posts.append(page(title('Você precisa de uma secretária','só pra atender telefone?',185,62,74)+phone(phone_calls,100,470,380,740,'transform:perspective(1800px) rotateY(14deg) rotateX(6deg)')+site_ok+
 phrase('A agenda online agenda, confirma e remarca.<br><b>Sua equipe cuida do que importa.</b>','AGENDA ONLINE · WEBCLINIC')))
# 5 instagram
insta=f'''<div style="padding:70px 24px 0;text-align:center"><div style="width:120px;height:120px;border-radius:50%;margin:0 auto;padding:5px;background:linear-gradient(135deg,{L},{A})"><div style="width:100%;height:100%;border-radius:50%;background:{M};border:4px solid #fff"></div></div>
<div style="font-size:24px;font-weight:700;margin-top:14px">Dra. Ana Paula</div><div style="font-size:15px;color:{C}">Dermatologista · CRM 00000</div>
<div style="display:flex;justify-content:space-around;margin:20px 0"><div><b style="font-size:20px">312</b><div style="font-size:13px;color:{C}">posts</div></div><div><b style="font-size:20px">18,4 mil</b><div style="font-size:13px;color:{C}">seguidores</div></div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px">{''.join(f'<div style="aspect-ratio:1;background:{c}"></div>' for c in [M,G,"#DCEBFB",G,"#DCEBFB",M,"#DCEBFB",M,G])}</div>
<div style="margin-top:16px;border:2px dashed {A};color:{A};border-radius:99px;padding:10px;font-size:16px;font-weight:600">🔗 link na bio</div></div>'''
site_ag=f'''<div class="bx" style="position:absolute;left:520px;top:590px;width:470px;height:420px;overflow:hidden;{TILT};z-index:4">{bar('draanapaula.com.br')}
<div style="padding:34px 34px"><div style="font-size:13px;font-weight:600;letter-spacing:.22em;color:{A}">DERMATOLOGIA</div><div style="font-size:34px;line-height:1.08;letter-spacing:-.03em;margin:12px 0 16px"><b>Pele saudável</b><span style="font-weight:300"> começa na consulta certa.</span></div>
<div style="height:10px;border-radius:6px;background:{G};width:90%;margin-bottom:9px"></div><div style="height:10px;border-radius:6px;background:{G};width:66%"></div>
<div style="display:inline-block;margin-top:24px;background:{A};color:#fff;font-weight:600;font-size:20px;border-radius:99px;padding:13px 26px">Agendar consulta</div></div></div>'''
arrow=f'<svg style="position:absolute;left:420px;top:760px;z-index:6" width="140" height="80" viewBox="0 0 140 80"><path d="M6 50H40L48 30L60 68L70 40L76 50H118" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><path d="M106 38L120 50L106 62" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
posts.append(page(title('Instagram não','marca consulta.')+phone(insta,90,470,380,740,'transform:perspective(1800px) rotateY(14deg) rotateX(6deg)')+site_ag+arrow+
 phrase('O Instagram atrai. <b>Quem converte é o site.</b><br>O link da bio precisa levar pra uma agenda.','SITES PARA MÉDICOS · WEBCLINIC')))
# 6 pesquisa
def res(name,sub,act,hi):
    st=f'border:2px solid {A};background:#fff;{SH}' if hi else 'border:2px solid #EEF2F7;background:#fff;opacity:.55'
    return f'<div style="border-radius:22px;padding:20px 24px;{st};display:flex;align-items:center;gap:18px;margin-bottom:14px"><div style="width:58px;height:58px;border-radius:50%;background:{M if hi else G}"></div><div style="flex:1"><div style="font-size:22px;font-weight:600">{name}</div><div style="font-size:16px;color:{C}">{sub}</div></div>{act}</div>'
search=f'''<div class="bx" style="position:absolute;left:120px;top:490px;width:840px;padding:30px 30px 18px;{TILT}">
<div style="display:flex;align-items:center;gap:14px;border:2px solid #E2EAF4;border-radius:99px;padding:16px 24px;font-size:22px;margin-bottom:24px"><svg width="26" height="26" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="7" fill="none" stroke="{N}" stroke-width="2.6"/><path d="M16 16l5 5" stroke="{N}" stroke-width="2.6" stroke-linecap="round"/></svg>dermatologista perto de mim<span style="width:2px;height:26px;background:{A};margin-left:-8px"></span></div>
{res('Dra. Ana Paula · Dermatologia','★ 4,9 · 1,2 km · aberto agora',f'<span style="background:{A};color:#fff;font-weight:600;font-size:17px;border-radius:99px;padding:11px 20px">Agendar online</span>',True)}
{res('Clínica Pele & Cia','★ 4,1 · 2,8 km','',False)}{res('Dr. Roberto Lima','sem site · 3,5 km','',False)}</div>'''
posts.append(page(title('O paciente te pesquisa','antes de ligar.')+search+
 f'<div class="chip" style="right:70px;top:450px;z-index:5"><div class="ic">{CHECK}</div><div>1º resultado<small>com agenda online</small></div></div>'+
 phrase('Se você não aparece bem na busca,<br><b>ele marca com quem aparece.</b>','SITE + GOOGLE · WEBCLINIC')))
# 7 lembrete
chat=f'''<div style="padding:62px 0 0"><div style="display:flex;align-items:center;gap:12px;padding:10px 20px 14px;border-bottom:1px solid #EEF2F7"><div style="width:44px;height:44px;border-radius:50%;background:{A};display:grid;place-items:center;color:#fff;font-weight:700">AP</div><div><div style="font-size:18px;font-weight:600">Clínica Dra. Ana Paula</div><div style="font-size:13px;color:{C}">mensagem automática</div></div></div>
<div style="background:{G};height:600px;padding:22px 18px">
<div style="background:#fff;border-radius:6px 22px 22px 22px;padding:16px 18px;font-size:17px;line-height:1.45;border:1px solid #E2EAF4">Olá, Maria! 👋<br>Lembrete: sua consulta é <b>amanhã, às 14h</b>, com a Dra. Ana Paula.</div>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:10px"><div style="background:{A};color:#fff;text-align:center;font-weight:600;font-size:18px;border-radius:16px;padding:13px">Confirmar presença</div><div style="background:#fff;text-align:center;font-weight:500;font-size:18px;border-radius:16px;padding:12px;border:2px solid #E2EAF4">Remarcar</div></div>
<div style="margin:16px 0 0 auto;width:max-content;background:#DCEBFB;border-radius:22px 6px 22px 22px;padding:12px 16px;font-size:17px">Confirmo! ✅</div></div></div>'''
posts.append(page(title('Paciente que esquece','a consulta?')+phone(chat,380,460,400,740)+
 f'<div class="chip" style="left:80px;top:700px;z-index:5"><div class="ic">{CHECK}</div><div>Maria confirmou<small>enviado 24h antes</small></div></div>'+
 f'<div class="chip" style="right:70px;top:900px;z-index:5"><div class="ic" style="background:#FFE7EA"><svg width="24" height="24" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke="#FA5F6D" stroke-width="3" stroke-linecap="round"/></svg></div><div>Menos faltas<small>horário vago é remarcado</small></div></div>'+
 phrase('Lembrete automático pela agenda online.<br><b>Menos falta, agenda cheia.</b>','AGENDA ONLINE · WEBCLINIC')))
for n,p in zip([2,3,5,6,7],posts): open(f'p5-{n}.html','w').write(p)
