N='#0B1F3A';A='#2D7FF0';L='#5AA2FF';M='#CFE6F7';G='#EEF5FC';C='#6B7A90'
CUR="M0 0L0 34L9 26L15 40L21 37L15 24L27 24Z"
def logo(w,c1=N,c2=A,cp=A,pulse=True):
    p=f'<path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="{cp}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' if pulse else ''
    vb="26 86 190 100" if pulse else "26 86 190 46"
    h=w*(100 if pulse else 46)/190
    return f'<svg width="{w}" height="{h:.0f}" viewBox="{vb}"><text x="120" y="124" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" letter-spacing="-1.8"><tspan fill="{c1}">web</tspan><tspan fill="{c2}">clinic</tspan></text>{p}</svg>'
def roundlogo(size,bg='#fff',c1=N,c2=A,cp=A,border=True):
    b=f'stroke="#E2EAF4" stroke-width="3"' if border and bg=='#fff' else ''
    return f'<svg width="{size}" height="{size}" viewBox="0 0 240 240"><circle cx="120" cy="120" r="{118 if b else 120}" fill="{bg}" {b}/><text x="120" y="124" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" letter-spacing="-1.8"><tspan fill="{c1}">web</tspan><tspan fill="{c2}">clinic</tspan></text><path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="{cp}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PULSE_BIG=lambda w,c=A,sw=6: f'<svg width="{w}" height="{w*0.25:.0f}" viewBox="0 0 400 100"><path d="M4 50H150L166 18L190 86L210 32L222 50H396" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
head='''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>
body{background:#fff;padding:80px 90px}
.k{font-size:18px;font-weight:600;letter-spacing:.22em;color:var(--azul);text-transform:uppercase}
.pg{position:absolute;bottom:56px;left:90px;right:90px;display:flex;justify-content:space-between;font-size:16px;color:var(--cinza);letter-spacing:.1em}
h2{font-size:64px;font-weight:300;letter-spacing:-.035em;line-height:1.05;margin:14px 0 50px} h2 b{font-weight:700}
.box{border:2px solid #E2EAF4;border-radius:32px}
p.s{font-size:22px;line-height:1.5;color:var(--cinza)}
</style></head><body>'''
def foot(n,t): return f'<div class="pg"><span>WEB CLINIC · MANUAL DE MARCA</span><span>{n:02d} · {t}</span></div><div class="grain" style="opacity:.05"></div></body></html>'
pages=[]
# 1 capa
pages.append(head+f'''<style>body{{background:{G}}}</style>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px">
{logo(640)}
<div style="font-size:34px;font-weight:300;letter-spacing:-.02em;text-align:center;line-height:1.35">Sites que <b style="font-weight:700;color:{A}">viram consulta marcada</b><br>para médicos e profissionais da saúde.</div></div>
<div style="position:absolute;top:80px;left:90px" class="k">Manual de marca · v1</div>'''+foot(1,'CAPA'))
# 2 logo
pages.append(head+f'''<div class="k">01 · Logo</div><h2>A escrita é o site.<br><b>O batimento é a saúde.</b></h2>
<div class="box" style="height:360px;display:grid;place-items:center;position:relative">{logo(560)}
<div style="position:absolute;inset:34px 70px;border:2px dashed {M};border-radius:16px"></div></div>
<p class="s" style="margin:18px 0 40px">Área de respiro: deixe em volta do logo, no mínimo, a altura do "b" livre de qualquer elemento.</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
<div class="box" style="height:220px;display:grid;place-items:center">{logo(250)}</div>
<div style="height:220px;border-radius:32px;background:{N};display:grid;place-items:center">{logo(250,'#fff',L,L)}</div>
<div style="height:220px;border-radius:32px;background:{A};display:grid;place-items:center">{logo(250,'#fff',M,'#fff')}</div></div>
<div style="display:flex;align-items:center;gap:40px;margin-top:48px">
{roundlogo(190)}{roundlogo(110)}{roundlogo(60)}
<p class="s" style="max-width:380px">Foto de perfil: sempre no círculo, fundo branco. Nas versões escuras, use navy ou azul de fundo.</p></div>'''+foot(2,'LOGO'))
# 3 cores e fontes
sw=lambda c,n,h,t='#fff',b='': f'<div style="flex:1"><div style="height:230px;border-radius:28px;background:{c};{b}"></div><div style="font-size:24px;font-weight:600;margin-top:16px">{n}</div><div style="font-size:18px;color:{C};font-family:Inter">{h}</div></div>'
pages.append(head+f'''<div class="k">02 · Cores e fonte</div><h2>Branco de clínica,<br><b>azul de confiança.</b></h2>
<div style="display:flex;gap:18px">{sw('#FFFFFF','Branco','#FFFFFF · base','', 'border:2px solid #E2EAF4')}{sw(A,'Azul Web Clinic','#2D7FF0 · destaque')}{sw(N,'Navy','#0B1F3A · textos')}</div>
<div style="display:flex;gap:18px;margin-top:22px">{sw(G,'Gelo','#EEF5FC · fundos','','border:2px solid #E2EAF4')}{sw(M,'Máscara','#CFE6F7 · apoio')}{sw(L,'Azul claro','#5AA2FF · no escuro')}{sw('#FA5F6D','Alerta','#FA5F6D · só p/ erro')}</div>
<div class="box" style="margin-top:48px;padding:40px 44px;display:flex;justify-content:space-between;align-items:flex-end">
<div><div style="font-size:120px;line-height:.9;letter-spacing:-.05em"><span style="font-weight:300">Aa</span><b style="font-weight:700;color:{A}">Aa</b></div><div style="font-size:30px;font-weight:600;margin-top:18px">Poppins</div></div>
<div style="text-align:right;font-size:22px;line-height:1.7;color:{C}"><span style="font-weight:300;color:{N};font-size:34px">Light 300</span> · frase de abertura<br><span style="font-weight:700;color:{N};font-size:34px">Bold 700</span> · a palavra que vende<br>Mistura fino + negrito na mesma frase.</div></div>'''+foot(3,'CORES E FONTE'))
# 4 elementos
chip=lambda ic,t,s,bg: f'<div style="display:inline-flex;align-items:center;gap:14px;background:#fff;border:2px solid #E2EAF4;border-radius:22px;padding:14px 20px"><div style="width:44px;height:44px;border-radius:14px;background:{bg};display:grid;place-items:center">{ic}</div><div style="font-size:20px;font-weight:600;line-height:1.2">{t}<div style="font-size:15px;font-weight:400;color:{C}">{s}</div></div></div>'
pages.append(head+f'''<div class="k">03 · Elementos</div><h2>Menos foto,<br><b>mais interface.</b></h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
<div class="box" style="height:230px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:16px">{PULSE_BIG(340)}<div class="s" style="font-size:18px;color:{C}">Batimento: a assinatura da marca</div></div>
<div class="box" style="height:230px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:22px"><div style="display:flex;gap:40px;align-items:center"><svg width="56" height="80" viewBox="-2 -2 32 44"><path d="{CUR}" fill="{A}" stroke="{A}" stroke-width="2.5" stroke-linejoin="round"/></svg><svg width="70" height="70" viewBox="0 0 70 70"><path d="M35 8v54M8 35h54" stroke="{A}" stroke-width="14" stroke-linecap="round"/></svg></div><div style="font-size:18px;color:{C}">Cursor e mais: site + saúde</div></div>
<div style="grid-column:span 2;height:300px;border-radius:32px;background:{N};padding:0;overflow:hidden;position:relative">
<div style="height:50px;background:#0C1C38;display:flex;align-items:center;gap:10px;padding:0 22px"><i style="width:12px;height:12px;border-radius:50%;background:#FA5F6D"></i><i style="width:12px;height:12px;border-radius:50%;background:#2A3B5C"></i><i style="width:12px;height:12px;border-radius:50%;background:#2A3B5C"></i><div style="margin-left:16px;height:28px;flex:1;border-radius:99px;background:{N};font-size:15px;color:#7F92B5;display:flex;align-items:center;padding:0 14px">suaclinica.com.br</div></div>
<div style="position:absolute;left:40px;top:100px">{PULSE_BIG(560,L,5)}</div><div style="position:absolute;right:44px;top:86px;text-align:right;color:#fff"><div style="font-size:13px;letter-spacing:.22em;color:#6E84AD">CONVERSÃO</div><div style="font-size:78px;font-weight:600;letter-spacing:-.04em;color:{L}">+38%</div></div>
<div style="position:absolute;left:40px;bottom:30px;font-size:16px;color:#7F92B5">Janela de site / monitor: o visual principal dos posts</div></div>
<div class="box" style="height:200px;display:grid;place-items:center">{chip('<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12l5 5 9-10" fill="none" stroke="#2D7FF0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>','Nova consulta marcada','via site · agora',G)}</div>
<div class="box" style="height:200px;display:grid;place-items:center"><span class="pill" style="box-shadow:none;border:2px solid #E2EAF4"><i><svg width="24" height="24" viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg></i>Fale com a gente</span></div></div>
<div style="display:flex;gap:28px;margin-top:34px;font-size:20px;color:{N}"><b style="color:{A}">Regras:</b> sem sombras ou brilho atrás · cantos bem arredondados · muito respiro · no máximo ~25 palavras por post</div>'''+foot(4,'ELEMENTOS'))
# 5 aplicações: destaques + post
icons={
'Sites':f'<rect x="20" y="26" width="60" height="48" rx="10" fill="none" stroke="{N}" stroke-width="5"/><path d="M20 40H80" stroke="{N}" stroke-width="4"/><path d="M30 58H42L46 50L52 66L56 56L59 58H70" fill="none" stroke="{A}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
'Resultados':f'<path d="M22 72H78" stroke="{N}" stroke-width="5" stroke-linecap="round"/><path d="M26 62L42 46L54 54L76 30" fill="none" stroke="{A}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M64 30H76V42" fill="none" stroke="{A}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>',
'Dicas':f'<path d="M50 22a18 18 0 0 0-10 33v7h20v-7a18 18 0 0 0-10-33z" fill="none" stroke="{N}" stroke-width="5" stroke-linejoin="round"/><path d="M42 72h16" stroke="{N}" stroke-width="5" stroke-linecap="round"/><path d="M50 32v14M43 39h14" stroke="{A}" stroke-width="5" stroke-linecap="round"/>',
'Sobre':f'<path d="M18 52H36L42 38L52 66L58 46L62 52H82" fill="none" stroke="{A}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>',
'Contato':f'<path d="M24 30h52a6 6 0 0 1 6 6v26a6 6 0 0 1-6 6H44l-14 10v-10h-6a6 6 0 0 1-6-6V36a6 6 0 0 1 6-6z" fill="none" stroke="{N}" stroke-width="5" stroke-linejoin="round"/><path d="M50 40v16M42 48h16" stroke="{A}" stroke-width="5" stroke-linecap="round"/>',
}
hl=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px"><svg width="150" height="150" viewBox="0 0 100 100"><circle cx="50" cy="50" r="49" fill="{G}" stroke="#E2EAF4" stroke-width="1.5"/>{v}</svg><div style="font-size:19px">{k}</div></div>' for k,v in icons.items())
pages.append(head+f'''<div class="k">04 · Aplicações</div><h2>Destaques e <b>post.</b></h2>
<div class="box" style="padding:40px 30px;display:flex;justify-content:space-between">{hl}</div>
<div style="display:flex;gap:30px;margin-top:40px;align-items:flex-start">
<img src="post-uti-v3.png" style="width:440px;border-radius:24px;border:2px solid #E2EAF4">
<div style="padding-top:20px"><div style="display:flex;align-items:center;gap:18px">{roundlogo(96)}<div><div style="font-size:26px;font-weight:600">webclinic</div><div style="font-size:18px;color:{C}">Sites para médicos e clínicas</div></div></div>
<p class="s" style="margin-top:30px;max-width:380px">Post: título em Poppins fino + negrito, um elemento de interface no centro, um dado com fonte embaixo e um botão em pílula.</p>
<p class="s" style="margin-top:20px;max-width:380px">Destaques: círculo gelo, ícone em linha navy com detalhe azul.</p></div></div>'''+foot(5,'APLICAÇÕES'))
for i,p in enumerate(pages,1): open(f'brand-{i}.html','w').write(p)
