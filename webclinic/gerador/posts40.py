exec(open('posts5.py').read())
exec(open('elem.py').read().split('names=list(V)')[0])  # V vectors
import math
_t=title
def title(a,b,top=190,fa=None,fb=None):
    fa=fa or min(76,int(1000/(0.5*len(a))))
    fb=min(fb or 100,int(1000/(0.6*len(b))))
    return '<!--K-->'+_t(a,b,top,fa,fb)+'<!--/K-->'
_phr=phrase
def phrase(t,src): return '<!--K-->'+_phr(t,src)+'<!--/K-->'
R='#FA5F6D'
V['moon']=f'<circle cx="100" cy="100" r="74" fill="{N}"/><path d="M128 52a52 52 0 1 0 22 82 44 44 0 0 1-22-82z" fill="{L}"/><circle cx="62" cy="62" r="5" fill="#fff"/><circle cx="148" cy="152" r="4" fill="#fff" opacity=".6"/>'
V['pin']=f'<path d="M100 178s-58-56-58-98a58 58 0 0 1 116 0c0 42-58 98-58 98z" fill="{A}"/><circle cx="100" cy="80" r="24" fill="#fff"/><ellipse cx="100" cy="184" rx="34" ry="8" fill="{M}"/>'
V['x']=f'<circle cx="100" cy="100" r="70" fill="{R}"/><path d="M74 74l52 52M126 74l-52 52" stroke="#fff" stroke-width="16" stroke-linecap="round"/>'
V['phoneoff']=f'<circle cx="100" cy="100" r="74" fill="#FFE7EA"/><path d="M62 52h22l10 26-14 9a62 62 0 0 0 33 33l9-14 26 10v22a12 12 0 0 1-12 12A88 88 0 0 1 50 64a12 12 0 0 1 12-12z" fill="{R}"/>'
V['cursor']=f'<g transform="translate(62 40) scale(3)"><path d="M0 0L0 34L9 26L15 40L21 37L15 24L27 24Z" fill="{A}" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/></g>'
V['speed']=f'<path d="M30 140a70 70 0 0 1 140 0" fill="none" stroke="{M}" stroke-width="22" stroke-linecap="round"/><path d="M30 140a70 70 0 0 1 112-56" fill="none" stroke="{A}" stroke-width="22" stroke-linecap="round"/><path d="M100 140l38-44" stroke="{N}" stroke-width="10" stroke-linecap="round"/><circle cx="100" cy="140" r="14" fill="{N}"/>'
V['money']=f'<rect x="24" y="56" width="152" height="96" rx="20" fill="{A}"/><circle cx="100" cy="104" r="26" fill="#fff"/><path d="M100 90v28M92 96h12a6 6 0 0 1 0 12h-8a6 6 0 0 0 0 12h12" stroke="{A}" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="50" cy="104" r="7" fill="{M}"/><circle cx="150" cy="104" r="7" fill="{M}"/>'
V['user']=f'<circle cx="100" cy="100" r="74" fill="{M}"/><circle cx="100" cy="82" r="28" fill="{A}"/><path d="M52 150a48 40 0 0 1 96 0" fill="{A}"/>'
V['steth']=f'<path d="M62 30v50a38 38 0 0 0 76 0V30" fill="none" stroke="{N}" stroke-width="12" stroke-linecap="round"/><path d="M100 118v18a30 30 0 0 0 60 0v-14" fill="none" stroke="{N}" stroke-width="12" stroke-linecap="round"/><circle cx="160" cy="110" r="20" fill="{A}"/><circle cx="160" cy="110" r="8" fill="#fff"/>'

V['calendar']=f'<rect x="28" y="42" width="144" height="132" rx="26" fill="#fff" stroke="{M}" stroke-width="4"/><path d="M28 68a26 26 0 0 1 26-26h92a26 26 0 0 1 26 26v16H28z" fill="{A}"/><rect x="60" y="26" width="14" height="32" rx="7" fill="{N}"/><rect x="126" y="26" width="14" height="32" rx="7" fill="{N}"/>'+''.join(f'<rect x="{48+i*28}" y="{98+j*26}" width="20" height="16" rx="5" fill="{G if (i+j)%3 else M}"/>' for j in range(3) for i in range(4) if not (i==2 and j==1))+f'<rect x="99" y="117" width="34" height="30" rx="9" fill="{A}"/><path d="M108 132l5 5 10-10" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
V['mobile']=f'<rect x="54" y="16" width="92" height="170" rx="24" fill="{N}"/><rect x="62" y="26" width="76" height="150" rx="17" fill="#fff"/><rect x="86" y="32" width="28" height="7" rx="3.5" fill="{N}"/><rect x="70" y="50" width="60" height="24" rx="7" fill="{G}"/><rect x="76" y="58" width="30" height="8" rx="4" fill="{A}"/>'+''.join(f'<rect x="{70+(k%2)*31}" y="{82+(k//2)*20}" width="29" height="15" rx="6" fill="{A if k==3 else G}"/>' for k in range(6))+f'<rect x="70" y="148" width="60" height="16" rx="8" fill="{A}"/>'
V['computer']=f'<rect x="18" y="36" width="164" height="128" rx="18" fill="#fff" stroke="{M}" stroke-width="4"/><path d="M18 54a18 18 0 0 1 18-18h128a18 18 0 0 1 18 18v8H18z" fill="{G}"/>'+''.join(f'<circle cx="{34+i*12}" cy="49" r="4" fill="{[R,"#F5B83D",A][i]}"/>' for i in range(3))+f'<rect x="34" y="78" width="54" height="66" rx="10" fill="{M}"/><circle cx="61" cy="102" r="11" fill="{A}"/><path d="M42 140a19 15 0 0 1 38 0z" fill="{A}"/><rect x="100" y="80" width="64" height="10" rx="5" fill="{N}"/><rect x="100" y="98" width="52" height="7" rx="3.5" fill="{M}"/><rect x="100" y="124" width="54" height="18" rx="9" fill="{A}"/>'
V['money']=f'<rect x="20" y="52" width="160" height="100" rx="20" fill="{A}"/><rect x="32" y="64" width="136" height="76" rx="12" fill="none" stroke="#fff" stroke-width="3" opacity=".35"/><text x="100" y="116" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="44" fill="#fff">R$</text><circle cx="50" cy="102" r="7" fill="#fff" opacity=".5"/><circle cx="150" cy="102" r="7" fill="#fff" opacity=".5"/>'
V['steth']=f'<path d="M58 30c-8 0-12 4-12 12v34a40 40 0 0 0 80 0V42c0-8-4-12-12-12" fill="none" stroke="{N}" stroke-width="10" stroke-linecap="round"/><circle cx="58" cy="30" r="9" fill="{A}"/><circle cx="114" cy="30" r="9" fill="{A}"/><path d="M86 116v14a32 32 0 0 0 64 0v-18" fill="none" stroke="{N}" stroke-width="10" stroke-linecap="round"/><circle cx="150" cy="96" r="24" fill="{A}"/><circle cx="150" cy="96" r="11" fill="#fff"/><circle cx="150" cy="96" r="5" fill="{M}"/>'
V['steth']=f'<path d="M64 30C62 82 78 106 100 112M136 30C138 82 122 106 100 112" fill="none" stroke="{N}" stroke-width="9" stroke-linecap="round"/><circle cx="64" cy="28" r="9" fill="{A}"/><circle cx="136" cy="28" r="9" fill="{A}"/><path d="M100 112C100 168 152 176 152 146" fill="none" stroke="{N}" stroke-width="9" stroke-linecap="round"/><circle cx="152" cy="130" r="24" fill="{A}"/><circle cx="152" cy="130" r="11" fill="#fff"/>'
V['tooth']=f'<path d="M60 40c18-10 30 0 40 0s22-10 40 0c22 12 18 44 8 66-6 14-8 52-22 52-12 0-10-38-26-38s-14 38-26 38c-14 0-16-38-22-52-10-22-14-54 8-66z" fill="{A}"/><path d="M70 62c6-6 14-6 20-2" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/>'
V['apple']=f'<path d="M100 66c-20-14-62-10-62 36 0 40 28 70 46 70 8 0 10-4 16-4s8 4 16 4c18 0 46-30 46-70 0-46-42-50-62-36z" fill="{A}"/><path d="M100 66c0-16 6-28 20-36" stroke="{N}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M104 52c10-16 30-18 40-12-6 14-26 18-40 12z" fill="{M}"/>'
V['bone']=f'<g transform="rotate(-40 100 100)"><rect x="54" y="86" width="92" height="28" rx="12" fill="{A}"/><circle cx="52" cy="84" r="20" fill="{A}"/><circle cx="52" cy="116" r="20" fill="{A}"/><circle cx="148" cy="84" r="20" fill="{A}"/><circle cx="148" cy="116" r="20" fill="{A}"/></g>'
V['drop']=f'<path d="M100 24c30 40 54 68 54 98a54 54 0 0 1-108 0c0-30 24-58 54-98z" fill="{A}"/><path d="M76 120a26 26 0 0 0 18 26" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".7"/>'
V['baby']=f'<circle cx="100" cy="108" r="64" fill="{M}"/><circle cx="100" cy="108" r="50" fill="#fff"/><circle cx="82" cy="104" r="6" fill="{N}"/><circle cx="118" cy="104" r="6" fill="{N}"/><path d="M86 126a16 12 0 0 0 28 0" stroke="{A}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M100 44c-10 0-14 10-6 14" stroke="{A}" stroke-width="7" fill="none" stroke-linecap="round"/>'
V['brain']=f'<path d="M100 40c-12-12-40-8-44 12-18 2-28 22-18 38-10 16 0 38 18 40 4 20 30 26 44 14z" fill="{A}"/><path d="M100 40c12-12 40-8 44 12 18 2 28 22 18 38 10 16 0 38-18 40-4 20-30 26-44 14z" fill="{L}"/><path d="M100 40v104" stroke="#fff" stroke-width="5"/><path d="M60 84c10 0 16 6 16 14M140 84c-10 0-16 6-16 14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'
V['pulse']=f'<rect x="24" y="40" width="152" height="120" rx="28" fill="{A}"/><path d="M40 104h30l12-26 18 48 14-34 10 12h36" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

def ic(n,s=48): return f'<svg width="{s}" height="{s}" viewBox="0 0 200 200">{V[n]}</svg>'
def chip(l,t,icon,txt,sub,rot=0,red=False,side='left'):
    pos=f'{side}:{l}px;top:{t}px'
    return f'<div class="chip" style="{pos};z-index:6;transform:rotate({rot}deg)"><div class="ic"{" style=background:#FFE7EA" if red else ""}>{ic(icon,30)}</div><div{f" style=color:{R}" if red else ""}>{txt}<small>{sub}</small></div></div>'
def bigicon(n,l,t,s=380,tilt=TILT,z=3):
    return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{s}px;height:{s}px;border-radius:{s*.2:.0f}px;display:grid;place-items:center;{tilt};z-index:{z};background:linear-gradient(160deg,#fff 55%,{G})">{ic(n,int(s*.62))}<svg style="position:absolute;right:{s*.1:.0f}px;top:{s*.1:.0f}px" width="{s*.09:.0f}" height="{s*.09:.0f}" viewBox="0 0 20 20"><path d="M10 2v16M2 10h16" stroke="{A}" stroke-width="4" stroke-linecap="round"/></svg><i style="position:absolute;left:{s*.11:.0f}px;bottom:{s*.12:.0f}px;width:{s*.045:.0f}px;height:{s*.045:.0f}px;border-radius:50%;background:{M}"></i></div>'
def floaticon(n,l,t,s=120,rot=0):
    return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{s}px;height:{s}px;border-radius:{s*.28:.0f}px;display:grid;place-items:center;transform:rotate({rot}deg);z-index:5">{ic(n,int(s*.68))}</div>'
def photo(src,l,t,w,h,pos='50% 30%',tilt=TILT):
    return f'<div style="position:absolute;left:{l}px;top:{t}px;width:{w}px;height:{h}px;border-radius:40px;overflow:hidden;{tilt};{SH};z-index:2"><img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>'
def card(inner,l,t,w,tilt=TILT,pad=34,z=3,extra=''):
    return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{w}px;padding:{pad}px;{tilt};z-index:{z};{extra}">{inner}</div>'
def row(icon,txt,sub='',last=False):
    return f'<div style="display:flex;align-items:center;gap:20px;padding:16px 0;{"" if last else "border-bottom:2px solid #EEF2F7"}">{ic(icon,52)}<div style="flex:1"><div style="font-size:25px;font-weight:600;letter-spacing:-.01em">{txt}</div>{f"<div style=font-size:19px;color:{C}>{sub}</div>" if sub else ""}</div></div>'
def lst(items,kind='tick'):
    return ''.join(row(k if k else kind,t,s,i==len(items)-1) for i,(k,t,s) in enumerate(items))
def btn(t,big=False): return f'<span style="display:inline-block;background:{A};color:#fff;font-weight:600;font-size:{22 if big else 18}px;border-radius:99px;padding:{"14px 30px" if big else "11px 22px"}">{t}</span>'
def site(head,sub,url='draanapaula.com.br',cta='Agendar consulta',tag='DERMATOLOGIA',extra=''):
    return f'''{bar(url)}<div style="padding:34px 36px"><div style="font-size:13px;font-weight:600;letter-spacing:.22em;color:{A}">{tag}</div><div style="font-size:36px;line-height:1.08;letter-spacing:-.03em;margin:12px 0 16px"><b>{head}</b><span style="font-weight:300"> {sub}</span></div>
<div style="height:10px;border-radius:6px;background:{G};width:90%;margin-bottom:9px"></div><div style="height:10px;border-radius:6px;background:{G};width:66%"></div><div style="margin-top:24px">{btn(cta,True)}</div>{extra}</div>'''
def sitebox(l,t,w,inner,tilt=TILT,z=3): return f'<div class="bx" style="position:absolute;left:{l}px;top:{t}px;width:{w}px;overflow:hidden;{tilt};z-index:{z}">{inner}</div>'
def ph(a,b,src): return phrase(f'{a}<br><b>{b}</b>',src)
DARK=f'body{{background:{N}!important}} .hdr .nm{{color:#fff}} .t .a{{color:#fff}} .ph{{color:#fff}} .src{{color:#6F86A6}} .grain{{opacity:.08!important}}'
AG,SG,DI,WC='AGENDA ONLINE · WEBCLINIC','SITES PARA MÉDICOS · WEBCLINIC','DICA · WEBCLINIC','WEBCLINIC'
TL='transform:perspective(1800px) rotateY(12deg) rotateX(6deg)'

P=[]
import re
FIT="""<script>document.fonts.ready.then(()=>{const st=document.querySelector('.stage');if(!st){window.READY=1;return}
let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;for(const c of st.children){const r=c.getBoundingClientRect();if(!r.width)continue;x0=Math.min(x0,r.left);y0=Math.min(y0,r.top);x1=Math.max(x1,r.right);y1=Math.max(y1,r.bottom)}
const t=document.querySelector('.t');const ph=document.querySelector('.ph');const T=(t?t.getBoundingClientRect().bottom:380)+70;const B=(ph&&ph.textContent.trim()?ph.getBoundingClientRect().top:1180)-64;
const L=56,Rr=1024;const s=Math.min(+st.dataset.max||1.22,(B-T)/(y1-y0),(Rr-L)/(x1-x0));const X=(L+Rr)/2-s*(x0+x1)/2,Y=(T+B)/2-s*(y0+y1)/2;
st.style.transformOrigin='0 0';st.style.transform=`translate(${X}px,${Y}px) scale(${s})`;window.READY=1;})</script>"""
UP=""".chip{font-size:23px!important;padding:16px 22px!important;border-radius:24px!important} .chip small{font-size:17px!important} .chip .ic{width:54px!important;height:54px!important;border-radius:16px!important}"""
def add(body,css='',fit=True,mx=1.22):
    keep=''.join(re.findall(r'<!--K-->.*?<!--/K-->',body,flags=re.S)); rest=re.sub(r'<!--K-->.*?<!--/K-->','',body,flags=re.S)
    if fit: body=keep+f'<div class="stage" data-max="{mx}" style="position:absolute;left:0;top:0;width:1080px;height:1350px">{rest}</div>'+FIT
    P.append(page(body,UP+css))

# 1 apresentação
add(title('Sites que viram','consulta marcada.')+sitebox(150,480,640,site('Seu consultório,','agora com agenda aberta 24h.',cta='Agendar consulta',tag='WEBCLINIC'))+
    floaticon('calendar',800,440,150,6)+f'<svg style="position:absolute;left:390px;top:790px;z-index:7" width="58" height="82" viewBox="-3 -3 33 46"><path d="{CUR}" fill="{N}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>'+chip(60,880,'tick','Consulta marcada','pelo site, sem ligação',-2,side='right')+
    ph('Sites para médicos e profissionais da saúde','que transformam visita em agendamento.',SG))
# 2 agenda 18h (photo)
add(title('Sua agenda não fecha','às 18h.')+photo('px-a.jpg',170,480,740,520,'50% 28%')+chip(70,820,'moon','Consulta marcada','Qui, 14h · agendada às 23h47',-3)+chip(70,560,'tick','Sem ligação','direto pelo site',2,side='right')+
    ph('Com agenda online no site, o paciente marca','a qualquer hora, sem precisar ligar.',AG))
# 3 secretária (photo)
add(title('Você precisa de uma secretária','só pra atender telefone?',185,62,74)+photo('px-c.jpg',150,470,780,520,'50% 40%')+chip(80,640,'phoneoff','12 chamadas perdidas','hoje, até as 14h',red=True)+chip(70,900,'tick','Consulta confirmada','pela agenda online',side='right')+
    ph('A agenda online agenda, confirma e remarca.','Sua equipe cuida do que importa.',AG))
# 4 instagram
ig=f'''<div class="bx" style="position:absolute;left:80px;top:500px;width:420px;overflow:hidden;{TL};z-index:3"><div style="display:flex;align-items:center;gap:12px;padding:16px 18px"><div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,{L},{A});padding:3px"><div style="width:100%;height:100%;border-radius:50%;background:{M};border:2px solid #fff"></div></div><div style="font-size:17px;font-weight:600">dra.anapaula</div></div>
<img src="px-b.jpg" style="width:100%;height:360px;object-fit:cover;object-position:50% 20%;display:block"><div style="padding:14px 18px;font-size:16px">{ic('heart',26)} {ic('chat',26)}<div style="margin-top:6px"><b>2.481 curtidas</b></div><div style="color:{C};font-size:14px;margin-top:2px">0 consultas marcadas</div></div></div>'''
add(title('Instagram não','marca consulta.')+ig+sitebox(540,600,450,site('Pele saudável','começa na consulta certa.'))+arrow.replace('left:420px;top:760px','left:440px;top:780px')+
    ph('O Instagram atrai. <b>Quem converte é o site.</b>','O link da bio precisa levar pra uma agenda.',SG))
# 5 pesquisa
add(title('O paciente te pesquisa','antes de ligar.')+search.replace('left:120px;top:490px;width:840px','left:80px;top:560px;width:720px')+floaticon('zoom',770,430,200,8)+
    ph('Se você não aparece bem na busca,','ele marca com quem aparece.','SITE + GOOGLE · WEBCLINIC'))
# 6 lembrete
msg=f'''<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px"><div style="width:46px;height:46px;border-radius:50%;background:{A};display:grid;place-items:center;color:#fff;font-weight:700">AP</div><div><div style="font-size:18px;font-weight:600">Clínica Dra. Ana Paula</div><div style="font-size:13px;color:{C}">lembrete automático · 24h antes</div></div></div>
<div style="background:{G};border-radius:6px 22px 22px 22px;padding:16px 18px;font-size:19px;line-height:1.45">Olá, Maria! Sua consulta é <b>amanhã, às 14h</b>, com a Dra. Ana Paula.</div>
<div style="display:flex;gap:10px;margin-top:14px"><div style="flex:1;background:{A};color:#fff;text-align:center;font-weight:600;font-size:18px;border-radius:16px;padding:13px">Confirmar</div><div style="flex:1;text-align:center;font-weight:500;font-size:18px;border-radius:16px;padding:11px;border:2px solid #E2EAF4">Remarcar</div></div>'''
add(title('Paciente que esquece','a consulta?')+card(msg,470,560,520,pad=26)+bigicon('clock',90,520,340,TL)+chip(560,840,'tick','Maria confirmou','menos faltas na agenda',-2)+
    ph('Lembrete automático pela agenda online.','Menos falta, agenda cheia.',AG))
# 7 versus bonito x converte
def vs(lt,litems,rt,ritems):
    L_=card(f'<div style="font-size:17px;letter-spacing:.2em;color:{C};font-weight:600">{lt}</div>'+''.join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:22px;font-size:25px;color:#6B7A90">{ic("x",36)}{t}</div>' for t in litems),90,500,430,TL,pad=36)
    R_=card(f'<div style="font-size:17px;letter-spacing:.2em;color:{A};font-weight:600">{rt}</div>'+''.join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:22px;font-size:25px;font-weight:600">{ic("tick",36)}{t}</div>' for t in ritems),560,560,430,TILT,pad=36,extra=f'border-color:{A}')
    return L_+R_
add(title('Site bonito','não basta.')+vs('SITE BONITO',['Muita animação','Sem botão de agendar','Lento no celular','Texto difícil'],'SITE QUE CONVERTE',['Agenda online','Botão em toda página','Abre em segundos','Linguagem simples'])+
    ph('Design chama atenção.','Estrutura é o que marca consulta.',SG))
# 8 checklist 5 coisas
add(title('5 coisas que todo','site médico precisa.',190,70,88)+card(lst([('calendar','Agenda online','o paciente marca sozinho'),('chat','WhatsApp visível','um toque pra falar'),('mobile','Abre bem no celular','onde o paciente está'),('star','Avaliações reais','prova de confiança'),('pin','Endereço e mapa','fácil de chegar')]),140,470,800,'transform:perspective(1800px) rotateX(5deg)',pad=34)+
    phrase('Salva esse post e confere no seu site.',DI))
# 9 velocidade
load=f'''<div style="font-size:15px;letter-spacing:.2em;color:{C};font-weight:600">CARREGANDO…</div><div style="height:16px;border-radius:9px;background:{G};margin:18px 0 26px;overflow:hidden"><div style="width:38%;height:100%;background:{R};border-radius:9px"></div></div>
<div style="display:flex;justify-content:space-between;font-size:20px"><span>Seu site</span><b style="color:{R}">8,4 s</b></div><div style="display:flex;justify-content:space-between;font-size:20px;margin-top:12px"><span>Site otimizado</span><b style="color:{A}">1,2 s</b></div>'''
add(title('Seu site abre','em 3 segundos?')+bigicon('speed',90,500,340,TL)+card(load,480,560,500,pad=34)+chip(480,880,'phoneoff','Paciente voltou pro Google','cansou de esperar',red=True)+
    ph('Paciente não espera site carregar.','Se demora, ele marca com outro.',DI))
# 10 link na bio
add(title('Link na bio','que leva pro nada.')+sitebox(120,480,560,f'{bar("linktr.ee/draanapaula")}<div style="padding:30px 34px">'+''.join(f'<div style="border:2px solid #E2EAF4;border-radius:99px;padding:14px;text-align:center;font-size:20px;margin-bottom:12px;color:#6B7A90">{t}</div>' for t in ['Meu Instagram','Meu Facebook','Meu YouTube','Fale comigo'])+'</div>',TL)+
    sitebox(600,640,400,site('Agende','em 1 minuto.',tag='LINK CERTO'),TILT,4)+
    ph('Lista de links não agenda nada.','Leve o paciente direto pra agenda.',DI))
# 11 noite
add(title('Quem marca à noite','não liga de dia.')+bigicon('moon',110,500,360,TL)+chip(520,560,'calendar','Nova consulta','Ter, 09h · marcada às 22h14')+chip(560,720,'calendar','Nova consulta','Qua, 15h · marcada às 23h02',-2)+chip(520,880,'calendar','Nova consulta','Sex, 10h · marcada às 00h37',2)+
    ph('O paciente decide quando tem tempo.','Sua agenda precisa estar aberta.',AG))
# 12 horário vago
slots=''.join(f'<div style="padding:16px 0;text-align:center;border-radius:16px;font-size:21px;font-weight:600;{"border:2px dashed "+R+";color:"+R if v else "background:"+G+";color:"+N}">{s}</div>' for s,v in [("08:00",0),("09:00",1),("10:30",0),("11:00",1),("14:00",0),("15:30",1),("16:00",0),("17:30",1)])
add(title('Horário vago','é dinheiro parado.')+card(f'<div style="font-size:15px;letter-spacing:.2em;color:{C};font-weight:600;margin-bottom:18px">AGENDA DE HOJE</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{slots}</div>',360,500,620,TILT,pad=34)+bigicon('money',60,560,320,TL,4)+
    ph('Agenda online preenche horários livres','e remarca faltas sozinha.',AG))
# 13 celular
add(title('Seu paciente','está no celular.')+bigicon('mobile',350,470,380,'transform:perspective(1800px) rotateX(5deg)')+chip(80,560,'zoom','Pesquisou','“pediatra perto de mim”',-3)+chip(70,760,'cursor','Clicou','no seu site',2,side='right')+chip(90,930,'tick','Agendou','em menos de 1 minuto',-2)+
    ph('Se o site não funciona no celular,','ele não funciona.',DI))
# 14 avaliações
stars=''.join(ic('star',34) for _ in range(5))
rev=f'<div style="display:flex;align-items:center;gap:14px">{ic("user",56)}<div><div style="font-size:20px;font-weight:600">Carla M.</div><div>{stars}</div></div></div><div style="font-size:21px;line-height:1.45;margin-top:16px">“Atendimento incrível e consegui marcar pelo site em 1 minuto.”</div>'
add(title('Avaliação no Google','vale ouro.')+card(rev,400,520,560,TILT)+card(rev.replace('Carla M.','Rafael S.').replace('Atendimento incrível e consegui marcar pelo site em 1 minuto.','Médica atenciosa, explicou tudo com calma.'),120,780,520,TL,z=4)+floaticon('star',120,500,150,-8)+
    ph('Paciente confia em outro paciente.','Mostre suas avaliações no site.',DI))
# 15 whatsapp lotado
faq=''.join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:2px solid #EEF2F7;font-size:21px">{q}<span style="color:{A};font-weight:700">+</span></div>' for q in ['Atende convênio?','Qual o valor da consulta?','Onde fica a clínica?','Como remarcar?'])
add(title('WhatsApp lotado','de pergunta repetida?')+card(f'<div style="font-size:15px;letter-spacing:.2em;color:{A};font-weight:600">PERGUNTAS FREQUENTES</div>{faq}',100,520,580,TL)+bigicon('chat',680,790,260,TILT,5)+
    ph('O site responde as dúvidas comuns.','Você só fala com quem já quer marcar.',SG))
# 16 dark statement
add(f'<div class="t" style="top:470px"><div class="a" style="font-size:84px">Ninguém agenda</div><div class="b" style="font-size:96px">com quem<br>não encontra.</div></div>'+floaticon('zoom',470,830,140,0)+phrase('',WC),DARK,fit=False)
# 17 trabalha enquanto atende (photo)
add(title('O site trabalha','enquanto você atende.')+photo('ph-5998445.jpg',150,480,780,520,'50% 35%')+chip(70,560,'calendar','3 consultas marcadas','durante o seu turno',2,side='right')+chip(80,880,'tick','Sem interromper','a consulta',-3)+
    ph('Você cuida do paciente.','O site cuida da agenda.',AG))
# 18 confirmação automática
add(title('Confirmação automática.','Sem planilha.',190,70,92)+card(lst([('tick','Maria Souza','Ter, 09h · confirmou'),('tick','João Lima','Ter, 10h30 · confirmou'),('clock','Ana Costa','Ter, 14h · aguardando'),('tick','Pedro Alves','Ter, 16h · confirmou')]),300,500,640,TILT)+bigicon('tick',70,560,250,TL,4)+
    ph('Lembrete e confirmação saem sozinhos.','Sua equipe ganha horas na semana.',AG))
# 19 confiança
add(title('Seu site passa','confiança?')+card(lst([('tick','CRM visível',''),('tick','Fotos reais da clínica',''),('tick','Depoimentos de pacientes',''),('tick','Endereço e horários','')]),100,560,580,TL)+bigicon('shield',630,470,300,TILT,5)+
    ph('Paciente escolhe quem parece confiável.','O site é a primeira impressão.',DI))
# 20 antes x depois
add(title('Antes e depois','da agenda online.')+vs('ANTES',['Telefone tocando','Planilha e caderno','Faltas sem aviso','Agenda furada'],'DEPOIS',['Agenda pelo site','Tudo num só lugar','Lembrete automático','Agenda cheia'])+
    ph('Mesma clínica, mesma equipe.','Outra rotina.',AG))
# 21 botão em toda página
add(title('Botão de agendar','em todas as páginas.')+sitebox(130,480,620,site('Ortopedia','pra voltar a se mover sem dor.',url='drcarlos.com.br',tag='ORTOPEDIA')+'',TILT)+f'<svg style="position:absolute;left:370px;top:800px;z-index:7" width="58" height="82" viewBox="-3 -3 33 46"><path d="{CUR}" fill="{N}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>'+chip(70,560,'calendar','Sempre à vista','no topo e no rodapé',3,side='right')+
    ph('Se o paciente precisa procurar o botão,','ele desiste.',DI))
# 22 clínica sem site
res3=res('Clínica Bem Estar','★ 4,8 · 1,5 km · agendar online',btn('Agendar'),True)+res('Clínica Vida','★ 4,6 · sem site · 2,1 km',f'<span style="color:{R};font-weight:600;font-size:17px">sem site</span>',False)
add(title('Clínica sem site','parece fechada.')+card(f'<div style="display:flex;align-items:center;gap:14px;border:2px solid #E2EAF4;border-radius:99px;padding:16px 24px;font-size:22px;margin-bottom:24px">{ic("zoom",30)}clínica perto de mim</div>'+res3,120,520,820,TILT,pad=30)+
    ph('Sem site, o paciente não sabe se você existe.','E escolhe quem ele consegue ver.',SG))
# 23 recepção digital (photo)
add(title('Seu site é a sua','recepção digital.')+photo('ph-4173251.jpg',150,480,780,520,'50% 30%')+chip(70,560,'chat','Tira dúvidas','24 horas por dia',2,side='right')+chip(80,880,'calendar','Recebe agendamentos','sem fila, sem espera',-3)+
    ph('A primeira recepção do paciente','acontece no celular dele.',SG))
# 24 domingo 22h
notif=f'<div style="display:flex;gap:16px;align-items:center">{ic("calendar",64)}<div style="flex:1"><div style="display:flex;justify-content:space-between"><b style="font-size:21px">Nova consulta agendada</b><span style="font-size:15px;color:{C}">agora</span></div><div style="font-size:18px;color:{C};margin-top:4px">Lucas Prado · Seg, 08h30</div></div></div>'
add(title('Domingo, 22h.','Alguém quer marcar.')+card(notif,140,560,800,'transform:perspective(1800px) rotateX(6deg)',pad=28)+card(notif.replace('Lucas Prado · Seg, 08h30','Beatriz Rocha · Seg, 11h').replace('agora','há 4 min'),180,720,720,'transform:perspective(1800px) rotateX(6deg) scale(.96)',pad=26,z=2,extra='opacity:.75')+floaticon('moon',800,440,140,8)+
    ph('Com agenda online, você acorda','com consultas marcadas.',AG))
# 25 perder paciente na ligação
add(title('Pare de perder paciente','na ligação.',190,70,88)+bigicon('phoneoff',90,500,330,TL)+card(calls,450,520,520,TILT,pad=26)+
    ph('Cada ligação perdida é um paciente','marcando com outro médico.',AG))
# 26 3 erros
add(title('3 erros que afastam','pacientes do seu site.',190,70,80)+card(lst([('x','Sem botão de agendar','o paciente não sabe o próximo passo'),('x','Texto técnico demais','ninguém entende “anamnese”'),('x','Não abre no celular','e quase todo mundo está nele')]),140,500,800,'transform:perspective(1800px) rotateX(5deg)')+
    phrase('Seu site tem algum desses? Conta aqui.',DI))
# 27 paciente quer facilidade
add(title('Paciente quer','facilidade.')+bigicon('heart',350,470,380,'transform:perspective(1800px) rotateX(5deg)')+chip(70,540,'calendar','Agenda em 1 minuto','sem ligação',-3)+chip(70,760,'bell','Lembrete automático','no WhatsApp',2,side='right')+chip(90,930,'pin','Como chegar','mapa no site',-2)+
    ph('Quanto mais fácil marcar,','mais gente marca.',DI))
# 28 concorrente
add(title('Seu concorrente','já tem agenda online.')+card(f'<div style="display:flex;align-items:center;gap:14px;border:2px solid #E2EAF4;border-radius:99px;padding:16px 24px;font-size:22px;margin-bottom:24px">{ic("zoom",30)}dermatologista em Porto Alegre</div>'+res('Dra. Júlia Mendes','★ 4,9 · agendar online',btn('Agendar'),True)+res('Você','★ 4,9 · ligar no horário comercial','',False),120,520,820,TILT,pad=30)+
    ph('Mesma nota, mesmo bairro.','Ganha quem é mais fácil de marcar.',SG))
# 29 dark seguidor
add(f'<div class="t" style="top:470px"><div class="a" style="font-size:84px">Seguidor não paga</div><div class="b" style="font-size:96px">consulta.</div></div><div class="ph" style="bottom:420px;font-size:56px;font-weight:600;color:{L}">Paciente paga.</div><svg style="position:absolute;left:0;top:1010px" width="1080" height="120" viewBox="0 0 1080 120"><path d="M0 70H420L450 20L490 110L520 40L540 70H1080" fill="none" stroke="{A}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/></svg>'+phrase('',WC),DARK,fit=False)
# 30 do clique à consulta (steps)
def steps(items,top=520):
    w=210;out=''
    for i,(n,t,s) in enumerate(items):
        x=90+i*235
        out+=f'<div style="position:absolute;left:{x}px;top:{top}px;width:{w}px;text-align:center"><div class="bx" style="width:{w}px;height:{w}px;border-radius:44px;display:grid;place-items:center;margin-bottom:22px">{ic(n,130)}</div><div style="font-size:15px;letter-spacing:.2em;color:{A};font-weight:600">0{i+1}</div><div style="font-size:27px;font-weight:600;margin-top:6px">{t}</div><div style="font-size:20px;color:{C};margin-top:4px">{s}</div></div>'
        if i<len(items)-1: out+=f'<svg style="position:absolute;left:{x+w+2}px;top:{top+w/2-14}px" width="30" height="28" viewBox="0 0 30 28"><path d="M4 14h20M16 6l8 8-8 8" fill="none" stroke="{A}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return out
add(title('Do clique','à consulta.')+steps([('zoom','Busca','no Google'),('computer','Site','claro e rápido'),('calendar','Agenda','escolhe o horário'),('tick','Confirmado','sem ligação')])+
    ph('Um caminho simples, sem atrito.','É assim que site vira consulta.',SG))
# 31 primeira tela
note=lambda l,t,txt:f'<div style="position:absolute;left:{l}px;top:{t}px;z-index:6;display:flex;align-items:center;gap:10px;font-size:23px;font-weight:600;color:{A}"><span style="width:40px;height:40px;border-radius:50%;background:{A};color:#fff;display:grid;place-items:center;font-size:17px">{txt[0]}</span>{txt[1:]}</div>'
add(title('O que vai na','primeira tela do site?')+sitebox(120,520,600,site('Dra. Ana Paula','dermatologista em Porto Alegre.'),TILT)+note(760,560,'1Nome e especialidade')+note(760,660,'2Cidade ou bairro')+note(760,760,'3Foto real')+note(760,860,'4Botão de agendar')+
    ph('Em 3 segundos o paciente precisa entender','quem você é e como marcar.',DI))
# 32 mais tempo (photo)
add(title('Mais tempo','pra atender.')+photo('ph-5407206.jpg',150,480,780,520,'50% 35%')+chip(70,560,'clock','–6h por semana','no telefone',2,side='right')+chip(80,880,'calendar','Agenda organizada','sozinha',-3)+
    ph('Menos tempo agendando,','mais tempo cuidando.',AG))
# 33 lembrete whatsapp reduz faltas
bub=lambda t,me=False:f'<div style="max-width:78%;{"margin-left:auto;background:#DCEBFB;border-radius:22px 6px 22px 22px" if me else "background:"+G+";border-radius:6px 22px 22px 22px"};padding:14px 18px;font-size:19px;line-height:1.4;margin-top:12px">{t}</div>'
add(title('Faltou de novo?','Manda lembrete.')+card(bub('Oi, Pedro! Lembrete da sua consulta <b>amanhã, 10h</b>. Confirma?')+bub('Confirmo, obrigado!',True)+bub('Perfeito, até amanhã!'),100,520,580,TL,pad=26)+bigicon('bell',640,700,280,TILT,5)+
    ph('Lembrete automático 24h antes.','O paciente lembra, a agenda agradece.',AG))
# 34 médico precisa de marketing?
add(title('Médico precisa','de marketing?')+bigicon('steth',350,470,380,'transform:perspective(1800px) rotateX(5deg)')+chip(70,560,'user','Ser encontrado','no Google',-3)+chip(70,760,'shield','Passar confiança','antes da consulta',2,side='right')+chip(90,930,'calendar','Facilitar o agendamento','sem ligação',-2)+
    ph('Não é sobre dancinha no Reels.','É sobre o paciente te achar e marcar.',SG))
# 35 especialidades
specs=['Dermatologia','Odontologia','Pediatria','Psicologia','Nutrição','Ortopedia','Ginecologia','Fisioterapia']
SI=['drop','tooth','baby','brain','apple','bone','heart','pulse']
grid=''.join(f'<div class="bx" style="display:flex;align-items:center;gap:18px;padding:18px 22px;border-radius:26px;font-size:25px;font-weight:600"><span style="width:60px;height:60px;border-radius:18px;background:{G};display:grid;place-items:center">{ic(i,42)}</span>{s}</div>' for s,i in zip(specs,SI))
add(title('Um site pra cada','especialidade.')+f'<div style="position:absolute;left:120px;top:500px;width:840px;display:grid;grid-template-columns:1fr 1fr;gap:20px;transform:perspective(1800px) rotateX(5deg)">{grid}</div>'+
    ph('Cada especialidade tem um paciente diferente.','O site precisa falar com ele.',SG))
# 36 google maps
mp=f'<div style="height:300px;border-radius:22px;background:{G};position:relative;overflow:hidden"><svg width="100%" height="100%" viewBox="0 0 500 300" preserveAspectRatio="none"><path d="M0 200L160 140L300 190L500 90M120 0L180 300M340 0L300 300" stroke="#fff" stroke-width="18" fill="none"/></svg><div style="position:absolute;left:210px;top:60px">{ic("pin",110)}</div></div><div style="margin-top:20px;display:flex;justify-content:space-between;align-items:center"><div><b style="font-size:22px">Clínica Dra. Ana Paula</b><div style="font-size:17px;color:{C}">★ 4,9 · aberto agora</div></div>{btn("Site")}</div>'
add(title('Você aparece','no Google Maps?')+card(mp,220,500,620,TILT,pad=24)+chip(60,975,'pin','“perto de mim”','é a busca que mais agenda',-3)+
    ph('Perfil no Google + site com agenda.','A dupla que traz paciente do bairro.','SITE + GOOGLE · WEBCLINIC'))
# 37 como funciona
add(title('Como funciona','a Web Clinic.')+steps([('zoom','Diagnóstico','do seu momento'),('computer','Site','com sua cara'),('calendar','Agenda','online integrada'),('heart','Pacientes','marcando sozinhos')])+
    ph('Você atende.','A gente cuida do caminho até a consulta.',WC))
# 38 photo médica smiling - agende
add(title('Seu paciente quer','marcar agora.')+photo('ph-5215024.jpg',170,470,740,540,'50% 25%')+chip(70,820,'cursor','Agendar consulta','1 clique',-3)+chip(70,560,'tick','Horário escolhido','Qua, 16h',2,side='right')+
    ph('Não deixe pra amanhã','quem quer marcar hoje.',AG))
# 39 depoimento/resultado (fictitious-safe: generic)
add(title('Menos telefone,','mais consulta.')+photo('ph-8376277.jpg',150,480,780,520,'50% 35%')+chip(80,560,'calendar','Agenda online','aberta 24h',-3)+chip(70,880,'chat','WhatsApp','só pra quem já marcou',2,side='right')+
    ph('Uma rotina mais leve começa','por um site que agenda por você.',WC))
# 40 CTA
add(title('Vamos encher','sua agenda?')+f'<div style="position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center">{roundlogo(330)}</div>'+
    f'<div style="position:absolute;left:0;right:0;top:930px;display:flex;justify-content:center"><div style="display:flex;align-items:center;gap:18px;background:#fff;border:2px solid #E2EAF4;border-radius:99px;padding:16px 16px 16px 40px;font-size:34px;font-weight:600;{SH}">Fale com a Web Clinic<span style="width:60px;height:60px;border-radius:50%;background:{A};display:grid;place-items:center">{ARROW}</span></div></div>'+
    floaticon('calendar',150,540,150,-8)+floaticon('heart',790,660,140,8)+
    ph('Sites que convertem para médicos.','Link na bio.',WC),mx=1.7)

for i,p in enumerate(P,1): open(f'p40-{i:02d}.html','w').write(p)
print(len(P))
