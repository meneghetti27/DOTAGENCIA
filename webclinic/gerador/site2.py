# Site v2 da Web Clinic: preenche gerador/site-v2-modelo.html e escreve em ../site/index.html
import urllib.parse, re, os, json
H=open('site-v2-modelo.html').read()
MSG='Olá! Vim pelo site da Web Clinic e quero saber mais sobre um site para o meu consultório.'
ZAP='https://wa.me/5551989061441?text='+urllib.parse.quote(MSG)
ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
LOCK='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 10V8a5 5 0 0 1 10 0v2h1a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h1zm2 0h6V8a3 3 0 0 0-6 0v2z"/></svg>'
SEARCH='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
PULSE='<svg viewBox="0 0 32 32" fill="none"><path d="M3 17h7l2.4-6 3.6 12 3-8.5 1.6 2.5H29" stroke="#5AA2FF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MUTE="<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M11 5L6 9H3v6h3l5 4V5z'/><path d='M22 9l-6 6M16 9l6 6'/></svg>"
SOUND="<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M11 5L6 9H3v6h3l5 4V5z'/><path d='M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14'/></svg>"
ZAPICO='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2zm5.8 14.01c-.24.68-1.42 1.3-1.96 1.35-.5.05-1.13.07-1.82-.11-.42-.13-.96-.31-1.65-.61-2.9-1.25-4.79-4.17-4.94-4.36-.14-.19-1.18-1.57-1.18-3 0-1.42.75-2.12 1.01-2.41.27-.29.58-.36.78-.36h.56c.18 0 .42-.07.65.5.24.58.82 2 .89 2.15.07.14.12.31.02.5-.1.19-.14.31-.29.48-.14.17-.3.38-.43.51-.14.14-.29.3-.13.59.17.29.74 1.22 1.59 1.98 1.09.97 2.01 1.27 2.3 1.42.29.14.46.12.63-.07.17-.19.72-.84.92-1.13.19-.29.38-.24.65-.14.26.1 1.68.79 1.97.94.29.14.48.21.55.33.07.12.07.69-.17 1.37z"/></svg>'
def ms(c,extra='',cls=''):
    foot=''.join(f'<div><b>{a}</b>{b}</div>' for a,b in c.get('foot',[]))
    return f'''<div class="ms {cls}" style="--bg:{c['bg']};--fg:{c['fg']};--ac:{c['ac']};--soft:{c['soft']}"><div class="ms-in"{extra}>
<div class="ms-nav"><div class="nm">{c['nome']}<small>{c['esp']}</small></div><span>Tratamentos</span><span>Sobre</span><span>Contato</span><i class="ms-b">Agendar consulta</i></div>
<div class="ms-txt"><small>{c['tag']}</small><h3>{c['h']}</h3><p>{c['p']}</p><div class="ms-row"><i class="ms-b ac">Agendar consulta</i><u>Falar no WhatsApp</u></div>{('<div class="ms-foot">'+foot+'</div>') if foot else ''}</div>
<div class="ms-foto"><img src="img/{c['img']}.jpg" alt="" loading="lazy" style="object-position:{c.get('pos','center')}"><div class="ms-card"><span class="dot"></span><div>Próximo horário<b>{c['hr']}</b></div></div></div>
</div></div>'''
C=[dict(nome='Helena Prado',esp='Dermatologia',tag='Dermatologia clínica e estética',h='Pele saudável começa na <i>consulta certa.</i>',p='Diagnóstico cuidadoso, tratamento explicado sem pressa e acompanhamento de perto.',img='dermato',pos='center 20%',hr='Quinta, 14:00',bg='#F6F1EB',fg='#2A2019',ac='#8C5B3F',soft='rgba(42,32,25,.62)',foot=[('Particular','e convênios'),('Moinhos','Porto Alegre')],url='drahelenaprado.com.br'),
   dict(nome='Lívia Moraes',esp='Pediatria',tag='Pediatria e puericultura',h='Cuidado <i>desde o primeiro dia.</i>',p='Consultas tranquilas, orientação clara para os pais e atendimento que a criança gosta.',img='pediatria',pos='62% center',hr='Hoje, 16:30',bg='#EDF3FA',fg='#11304D',ac='#3779C2',soft='rgba(17,48,77,.62)',url='draliviamoraes.com.br'),
   dict(nome='Clínica Sorrir',esp='Odontologia',tag='Odontologia para toda a família',h='Sorriso <i>sem medo</i> de dentista.',p='Atendimento acolhedor, tecnologia moderna e um plano de tratamento que você entende.',img='odonto',pos='center 25%',hr='Amanhã, 09:00',bg='#ECF4F1',fg='#0F3A33',ac='#1E8A6F',soft='rgba(15,58,51,.62)',url='clinicasorrir.com.br'),
   dict(nome='Ana Ribeiro',esp='Psicologia',tag='Psicoterapia para adultos',h='Um lugar seguro <i>pra falar.</i>',p='Sessões presenciais e online, no seu tempo, com escuta de verdade.',img='psico',pos='center 30%',hr='Segunda, 19:00',bg='#F0EEE8',fg='#2E3A2E',ac='#667C58',soft='rgba(46,58,46,.62)',url='anaribeiropsi.com.br'),
   dict(nome='Paulo Viana',esp='Cardiologia',tag='Cardiologia e check-up',h='Seu coração <i>em boas mãos.</i>',p='Avaliação completa, exames no consultório e acompanhamento contínuo.',img='cardio',pos='35% center',hr='Sexta, 10:30',bg='#0F1B2C',fg='#F1F4F9',ac='#7FB2FF',soft='rgba(241,244,249,.62)',url='drpauloviana.com.br')]
def case(i,c):
    return f'''<article class="case"><div class="bw"><div class="bar"><i></i><i></i><i></i><span>{LOCK}{c['url']}</span></div>{ms(c)}</div><div class="cap"><b>{c['esp']} · {c['nome']}</b><span>0{i+1} · Conceito</span></div></article>'''
ROWS=[('Site sob medida','Design exclusivo, textos que explicam sem jargão e um botão de agendar em cada página.','retrato'),
('Agenda online','O paciente escolhe o horário e confirma sozinho, 24 horas por dia, sem ligar.','consulta'),
('Google e Maps','Perfil da Empresa configurado pra você aparecer na busca e no mapa da sua região.','clinica'),
('WhatsApp integrado','Um toque e o paciente fala com você, com a mensagem já escrita.','psico'),
('Lembretes automáticos','Confirmação e lembrete antes da consulta pra diminuir as faltas.','pediatria'),
('Rápido, seguro e ético','Leve no celular, com cadeado de segurança e textos dentro das regras do seu conselho.','odonto')]
rows=''.join(f'<div class="row up"><span class="n">{i+1:02d}</span><h3>{t}</h3><p>{d}</p><span class="ar">{ARROW}</span></div>' for i,(t,d,_) in enumerate(ROWS))
peeks=''.join(f'<img src="img/{im}.jpg" alt="" loading="lazy">' for _,_,im in ROWS)
ESP=['Dermatologia','Pediatria','Odontologia','Psicologia','Cardiologia','Nutrição','Ortopedia','Fisioterapia']
SEP='<svg viewBox="0 0 80 40" fill="none"><path d="M0 20h26l5-12 8 24 6-16 4 4h31" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
marq=''.join(f'<span>{e}</span>{SEP}' for e in ESP)
FAQ=[('Quanto tempo leva pra ficar pronto?','Depende do tamanho do projeto. Na primeira conversa a gente entende o que você precisa e já te passa o prazo certinho.'),
('Preciso ter domínio e hospedagem?','Não. A gente cuida de tudo: domínio, hospedagem, cadeado de segurança e configuração. Se você já tiver um domínio, usamos o seu.'),
('Funciona para clínica com vários profissionais?','Sim. O site e a agenda podem ter vários profissionais e especialidades, cada um com seus horários.'),
('Vocês configuram meu perfil no Google?','Sim. Configuramos e otimizamos o seu Perfil da Empresa no Google, pra você aparecer na busca e no Maps da sua região.'),
('Já tenho um site. Vale a pena trocar?','A gente analisa o seu site atual sem compromisso e te mostra o que muda pra ele virar consulta marcada.'),
('Os textos respeitam as regras de publicidade?','Sim. Escrevemos pensando nas normas do seu conselho profissional: informação clara, sem promessa de resultado e sem sensacionalismo.')]
faq=''.join(f'<details><summary>{q}<i></i></summary><p>{a}</p></details>' for q,a in FAQ)
rep={'{{ZAP}}':ZAP.replace('&','&amp;'),'{{ARROW}}':ARROW,'{{LOCK}}':LOCK,'{{SEARCH}}':SEARCH,'{{PULSE}}':PULSE,'{{MUTE_JS}}':MUTE,'{{SOUND_JS}}':SOUND,'{{MUTE}}':MUTE,'{{ZAPICO}}':ZAPICO,
     '{{MS_HERO}}':ms(C[0]),'{{MS_PHONE}}':ms(C[0],' style="top:40px"'),'{{CASES}}':''.join(case(i,c) for i,c in enumerate(C)),
     '{{ROWS}}':rows,'{{PEEKS}}':peeks,'{{MARQ}}':marq,'{{FAQ}}':faq}
for k,v in rep.items(): H=H.replace(k,v)
assert '{{' not in H, re.findall(r'\{\{[^}]*\}\}',H)
open('../site/index.html','w').write(H)
open('../site/vercel.json','w').write('{ "cleanUrls": true }\n')
print('ok',len(H)//1024,'KB')
