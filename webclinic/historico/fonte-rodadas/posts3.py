exec(open('brand.py').read().split("head='''")[0])  # reuse logo helpers & colors
CHECK='<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10" fill="none" stroke="#2D7FF0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW='<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
VER='<svg width="22" height="22" viewBox="0 0 24 24"><path d="M12 1l2.6 2.2 3.4-.3.9 3.3 3 1.7-1.2 3.2 1.2 3.2-3 1.7-.9 3.3-3.4-.3L12 23l-2.6-2.2-3.4.3-.9-3.3-3-1.7L3.3 12 2.1 8.8l3-1.7.9-3.3 3.4.3z" fill="#2D7FF0"/><path d="M7.5 12.2l3 3 6-6" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(body,extra_css='',n=1):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
body{{background:#F7F9FC}}
.hdr{{position:absolute;top:72px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px}}
.hdr .nm{{font-size:25px;font-weight:600;display:flex;align-items:center;gap:6px;line-height:1.1}} .hdr .at{{font-size:19px;color:{C}}}
.t{{position:absolute;left:0;right:0;text-align:center;letter-spacing:-.04em;line-height:1.02}}
.t .a{{font-weight:300;color:{N}}} .t .b{{font-weight:700;color:{A}}}
.ph{{position:absolute;bottom:118px;left:110px;right:110px;text-align:center;font-size:28px;line-height:1.45;color:{N}}} .ph b{{font-weight:600;color:{A}}}
.src{{position:absolute;bottom:66px;width:100%;text-align:center;font-size:15px;letter-spacing:.24em;color:#8A97AA}}
.bx{{background:#fff;border:2px solid #E2EAF4;border-radius:30px;box-shadow:0 30px 60px -10px rgba(45,127,240,.22),0 8px 18px -6px rgba(11,31,58,.10)}}
.chip{{position:absolute;display:flex;align-items:center;gap:14px;background:#fff;border:2px solid #E2EAF4;border-radius:22px;padding:14px 20px;font-size:20px;font-weight:600;line-height:1.2;box-shadow:0 30px 60px -10px rgba(45,127,240,.22),0 8px 18px -6px rgba(11,31,58,.10)}}
.chip .ic{{width:46px;height:46px;border-radius:14px;background:{G};display:grid;place-items:center}} .chip small{{display:block;font-size:15px;font-weight:400;color:{C}}}
.cnt{{position:absolute;top:84px;right:80px;font-size:17px;color:{C};letter-spacing:.1em}}
{extra_css}</style></head><body>
<div class="hdr">{roundlogo(62)}<div><div class="nm">webclinic {VER}</div><div class="at">@webclinic</div></div></div>
{body}<div class="grain" style="opacity:.05"></div></body></html>'''

# POST 1 — apresentação
p1=page(f'''
<div class="t" style="top:190px"><div class="a" style="font-size:84px">Seu site pode</div><div class="b" style="font-size:100px">marcar consulta.</div></div>
<div style="position:absolute;left:140px;top:540px;width:800px;height:500px;border-radius:60px;background:linear-gradient(135deg,#5AA2FF,#2D7FF0 55%,#1F66D1);filter:blur(40px);opacity:.2"></div>
<div class="bx" style="position:absolute;left:130px;top:520px;width:820px;height:500px;overflow:hidden;transform:perspective(1800px) rotateY(-12deg) rotateX(6deg)">
 <div style="height:54px;background:{G};display:flex;align-items:center;gap:9px;padding:0 22px;border-bottom:2px solid #E2EAF4"><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i><i style="width:12px;height:12px;border-radius:50%;background:#C9D6E6"></i>
 <div style="margin-left:16px;flex:1;height:30px;border-radius:99px;background:#fff;border:2px solid #E2EAF4;font-size:15px;color:{C};display:flex;align-items:center;padding:0 14px">draanapaula.com.br</div></div>
 <div style="padding:44px 48px;display:flex;gap:36px">
  <div style="flex:1"><div style="font-size:14px;font-weight:600;letter-spacing:.22em;color:{A}">DERMATOLOGIA · PORTO ALEGRE</div>
  <div style="font-size:44px;line-height:1.08;letter-spacing:-.03em;margin:16px 0 18px"><b style="font-weight:700">Pele saudável</b><span style="font-weight:300"> começa na consulta certa.</span></div>
  <div style="height:11px;border-radius:6px;background:{G};width:92%;margin-bottom:10px"></div><div style="height:11px;border-radius:6px;background:{G};width:70%"></div>
  <div style="display:inline-block;margin-top:30px;background:{A};color:#fff;font-weight:600;font-size:22px;border-radius:99px;padding:15px 30px">Agendar consulta</div></div>
  <div style="width:230px;height:300px;border-radius:26px;background:{G};position:relative;overflow:hidden">
   <svg width="230" height="300" viewBox="0 0 230 300"><circle cx="115" cy="110" r="46" fill="{M}"/><path d="M30 300C30 220 70 180 115 180S200 220 200 300Z" fill="{M}"/><path d="M60 250H96L104 232L116 268L126 242L132 250H170" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
 </div></div>
<svg style="position:absolute;left:392px;top:915px;z-index:6;filter:drop-shadow(0 8px 10px rgba(11,31,58,.25))" width="52" height="68" viewBox="-2 -2 32 44"><path d="{CUR}" fill="{N}" stroke="#fff" stroke-width="2.5" stroke-linejoin="round"/></svg>
<div class="chip" style="right:70px;top:470px;transform:perspective(1200px) rotateY(-12deg) translateZ(60px) scale(1.08);z-index:5"><div class="ic">{CHECK}</div><div>Nova consulta marcada<small>Quinta, 14h · pelo site</small></div></div>
<div class="ph">A <b>webclinic</b> cria sites para médicos e clínicas<br>que transformam visita em <b>paciente agendado.</b></div>
<div class="src">SITES · LANDING PAGES · GOOGLE</div>''')

# POST 2 — UTI (from v3 html, swap header to new logo)
import re
s=open('post-uti3.html').read()
s=re.sub(r'<div class="hdr">.*?</div></div></div>', f'<div class="hdr">{roundlogo(62)}<div><div class="nm">webclinic {VER}</div><div class="at">@webclinic</div></div></div>', s, count=1, flags=re.S)
p2=s.replace('overflow:hidden}','overflow:hidden;box-shadow:0 34px 70px -12px rgba(45,127,240,.30),0 10px 20px -8px rgba(11,31,58,.18)}',1).replace('border:2px solid #E2EAF4}','border:2px solid #E2EAF4;box-shadow:0 24px 44px -10px rgba(45,127,240,.25)}').replace('<div class="stage">','<div style="position:absolute;left:170px;top:570px;width:740px;height:480px;border-radius:60px;background:linear-gradient(135deg,#5AA2FF,#2D7FF0 55%,#1F66D1);filter:blur(40px);opacity:.2"></div><div class="stage">',1)

# POST 3 — como funciona
step=lambda n,t,s,ic: f'<div class="bx" style="display:flex;align-items:center;gap:26px;padding:28px 34px;height:150px"><div style="font-size:54px;font-weight:700;color:{A};letter-spacing:-.04em;width:80px">{n}</div><div style="flex:1"><div style="font-size:32px;font-weight:600;letter-spacing:-.02em">{t}</div><div style="font-size:21px;color:{C};margin-top:4px">{s}</div></div><div style="width:74px;height:74px;border-radius:22px;background:{G};display:grid;place-items:center">{ic}</div></div>'
I1=f'<svg width="40" height="40" viewBox="0 0 40 40"><circle cx="17" cy="17" r="11" fill="none" stroke="{N}" stroke-width="4"/><path d="M25 25l9 9" stroke="{N}" stroke-width="4.5" stroke-linecap="round"/><path d="M10 17h4l2-4 3 8 2-4h3" fill="none" stroke="{A}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I2=f'<svg width="42" height="40" viewBox="0 0 42 40"><rect x="3" y="5" width="36" height="30" rx="7" fill="none" stroke="{N}" stroke-width="4"/><path d="M3 14h36" stroke="{N}" stroke-width="3.5"/><path d="M21 19v11M15.5 24.5h11" stroke="{A}" stroke-width="4" stroke-linecap="round"/></svg>'
I3=f'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 4a16 16 0 0 0-13.8 24L4 36l8.3-2.1A16 16 0 1 0 20 4z" fill="none" stroke="{N}" stroke-width="4" stroke-linejoin="round"/><path d="M13 20l5 5 9-10" fill="none" stroke="{A}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
p3=page(f'''
<div class="t" style="top:190px"><div class="a" style="font-size:80px">Do clique à</div><div class="b" style="font-size:94px">consulta marcada.</div></div>
<div style="position:absolute;left:130px;top:520px;width:820px;height:500px;border-radius:60px;background:linear-gradient(135deg,#5AA2FF,#2D7FF0 55%,#1F66D1);filter:blur(40px);opacity:.2"></div>
<div style="position:absolute;left:100px;right:150px;top:500px;display:flex;flex-direction:column;gap:22px;transform:perspective(1600px) rotateY(-10deg) rotateX(5deg)">
<div style="transform:translateX(-30px)">{step('01','Diagnóstico','A gente mostra onde seu site perde paciente.',I1)}</div>
{step('02','Site que converte','Rápido, claro e feito pro celular.',I2)}
<div style="transform:translateX(30px)">{step('03','Agenda cheia','O paciente marca pelo WhatsApp em 1 clique.',I3)}</div>
</div>
<div style="position:absolute;left:0;right:0;top:1070px;display:flex;justify-content:center"><span class="pill" style="box-shadow:none;border:2px solid #E2EAF4"><i>{ARROW}</i>Fale com a gente</span></div>
<div class="src" style="bottom:70px">WEBCLINIC · SITES PARA MÉDICOS E CLÍNICAS</div>''')
for i,p in enumerate([p1,p2,p3],1): open(f'pp-{i}.html','w').write(p)
