# Gera o PDF "como postar" dos 40 posts (texto copiável: Chromium page.pdf)
exec(open('brand.py').read().split("head='''")[0])
import datetime, os, html
from PIL import Image

RAW='https://raw.githubusercontent.com/meneghetti27/DOTAGENCIA/main/webclinic/posts/post-{:02d}.png'
BASE=['#marketingmedico','#sitemedico','#agendaonline','#consultorio','#medicos']
CTA_LINK='Quer um site que agenda por você? O link está na bio.'
CTA_DM='Manda SITE no direct que a gente te mostra como fica no seu consultório.'

# (legenda, hashtags extras, texto alternativo)
L=[
("Sites que viram consulta marcada.\n\nA Web Clinic cria sites para médicos e profissionais da saúde com um objetivo: transformar quem visita em paciente agendado.\n\nAgenda online, botão de agendar sempre à vista e um texto que o paciente entende.\n\nSegue a gente pra ver como funciona.",['#webclinic','#marketingparamedicos'],"Card de site de consultório com botão Agendar consulta e o título Sites que viram consulta marcada."),
("Seu consultório fecha às 18h. Sua agenda não precisa fechar.\n\nCom agenda online no site, o paciente escolhe o horário à noite, no fim de semana, quando tiver tempo. Sem ligação e sem esperar a recepção abrir.\n\n"+CTA_LINK,['#agendamentoonline','#clinica'],"Foto de médico com chips: consulta marcada às 23h47 e sem ligação. Título: Sua agenda não fecha às 18h."),
("Sua secretária passa o dia no telefone?\n\nA agenda online marca, confirma e remarca sozinha. Sua equipe fica livre para receber bem quem já está no consultório.\n\n"+CTA_DM,['#secretariamedica','#gestaodeclinica'],"Foto de médica atendendo paciente, com chips de 12 chamadas perdidas e consulta confirmada."),
("Instagram atrai. Site converte.\n\nCurtida não marca consulta. Se o link da bio leva para um lugar confuso, o paciente desiste no meio do caminho.\n\nO link da bio precisa levar direto para uma agenda.\n\n"+CTA_LINK,['#instagrammedico','#linknabio'],"Post de Instagram de médica com muitas curtidas e zero consultas, ligado por uma seta a um site com botão Agendar consulta."),
("Antes de ligar, o paciente pesquisa no Google.\n\nSe o seu nome aparece com site, avaliações e agenda online, ele marca com você. Se não aparece, marca com quem aparece.\n\n"+CTA_DM,['#googlemeunegocio','#seo'],"Resultado de busca dermatologista perto de mim com a Dra. Ana Paula em destaque e botão Agendar online."),
("Paciente que esquece a consulta é horário perdido.\n\nCom lembrete automático 24h antes, ele confirma ou remarca com um toque. Menos falta, agenda mais cheia.\n\n"+CTA_LINK,['#lembreteautomatico','#faltas'],"Relógio e mensagem de lembrete da clínica com os botões Confirmar e Remarcar. Chip: Maria confirmou."),
("Site bonito não basta.\n\nAnimação e foto bonita chamam atenção. Quem marca consulta é a estrutura: agenda online, botão em toda página, site rápido e linguagem simples.\n\nSalva esse post para comparar com o seu site.",['#webdesign','#siteprofissional'],"Comparação entre site bonito, com itens marcados em vermelho, e site que converte, com itens marcados em azul."),
("5 coisas que todo site médico precisa ter:\n\n1. Agenda online\n2. WhatsApp visível\n3. Abrir bem no celular\n4. Avaliações reais\n5. Endereço e mapa\n\nQuantas o seu site tem? Conta aqui nos comentários.",['#dicasdemarketing','#sitemedico2'],"Lista com cinco itens: agenda online, WhatsApp visível, abre bem no celular, avaliações reais, endereço e mapa."),
("Seu site abre em 3 segundos?\n\nNo celular, ninguém espera página carregar. Se demora, o paciente volta para o Google e clica no próximo.\n\nTesta agora no seu celular e conta aqui quanto tempo levou.",['#velocidadedosite','#mobile'],"Velocímetro e barra de carregamento comparando um site lento e um site otimizado. Valores ilustrativos."),
("O link da sua bio leva para onde?\n\nLista com Instagram, Facebook e YouTube não agenda nada. O paciente que clicou já quer marcar. Leve ele direto para a agenda.\n\n"+CTA_LINK,['#linknabio','#instagrammedico'],"Lista de links genérica ao lado de uma página com o botão Agendar consulta."),
("Quem marca à noite não liga de dia.\n\nMuita gente só tem tempo de cuidar da saúde depois do trabalho. Com a agenda aberta 24h no site, essas consultas não se perdem.\n\n"+CTA_DM,['#agendamentoonline','#pacientes'],"Lua e três notificações de nova consulta marcadas às 22h, 23h e meia-noite."),
("Horário vago é dinheiro parado.\n\nA agenda online mostra os horários livres para o paciente e preenche as faltas com quem quer remarcar.\n\n"+CTA_LINK,['#gestaodeclinica','#agenda'],"Agenda do dia com horários vagos destacados em vermelho e ícone de dinheiro."),
("Seu paciente está no celular.\n\nEle pesquisa, clica e agenda tudo pelo telefone. Se o seu site não funciona bem no celular, ele não funciona.\n\nSalva esse post como lembrete.",['#mobile','#sitemedico'],"Celular com tela de agendamento e chips: pesquisou, clicou no seu site, agendou em menos de 1 minuto."),
("Avaliação no Google vale ouro.\n\nPaciente confia em outro paciente. Peça avaliação para quem saiu satisfeito e mostre as melhores no seu site.\n\n"+CTA_DM,['#avaliacoes','#googlemeunegocio'],"Dois cards de avaliação cinco estrelas com comentários de pacientes. Exemplo ilustrativo."),
("WhatsApp lotado de pergunta repetida?\n\nConvênio, valor, endereço, como remarcar. Uma página de perguntas frequentes no site responde tudo isso antes da mensagem chegar.\n\nVocê só conversa com quem já quer marcar.",['#whatsapp','#atendimento'],"Ícone de conversa e card de perguntas frequentes: atende convênio, valor da consulta, onde fica, como remarcar."),
("Ninguém agenda com quem não encontra.\n\nSite, Google e agenda online. É assim que o paciente chega até você.\n\n"+CTA_LINK,['#webclinic','#marketingparamedicos'],"Frase em fundo azul escuro: Ninguém agenda com quem não encontra."),
("O site trabalha enquanto você atende.\n\nVocê cuida do paciente na sua frente. O site cuida de quem quer marcar a próxima consulta.\n\n"+CTA_DM,['#pediatria','#agendaonline2'],"Foto de médica examinando uma criança, com chip de 3 consultas marcadas durante o turno."),
("Confirmação automática. Sem planilha.\n\nLembrete e confirmação saem sozinhos e a agenda se atualiza. Sua equipe ganha horas na semana.\n\n"+CTA_LINK,['#automacao','#gestaodeclinica'],"Lista de pacientes com status confirmado e aguardando, ao lado de um grande ícone de confirmação."),
("Seu site passa confiança?\n\nCRM visível, fotos reais da clínica, depoimentos de pacientes, endereço e horários. O paciente escolhe quem parece confiável, e o site é a primeira impressão.\n\nSalva esse checklist.",['#confianca','#sitemedico'],"Escudo com check e lista: CRM visível, fotos reais, depoimentos, endereço e horários."),
("Antes e depois da agenda online.\n\nAntes: telefone tocando, planilha, faltas sem aviso.\nDepois: paciente agenda pelo site, tudo num lugar só, lembrete automático.\n\nMesma clínica, outra rotina.\n\n"+CTA_DM,['#agendaonline','#rotina'],"Comparação antes e depois da agenda online em duas colunas."),
("Botão de agendar em todas as páginas.\n\nSe o paciente precisa procurar como marcar, ele desiste. O botão tem que estar no topo, no meio e no fim de cada página.\n\nConfere aí no seu site.",['#webdesign','#conversao'],"Página de ortopedia com botão Agendar consulta e cursor clicando nele."),
("Clínica sem site parece fechada.\n\nNa busca, quem tem site e agenda online passa segurança. Quem não tem some da lista.\n\n"+CTA_LINK,['#googlemeunegocio','#clinica'],"Resultados de busca: clínica com agendamento online em destaque e clínica sem site apagada."),
("Seu site é a sua recepção digital.\n\nÉ ali que o paciente tira dúvidas, conhece você e marca a consulta, muitas vezes antes de falar com alguém.\n\n"+CTA_DM,['#recepcao','#experienciadopaciente'],"Foto de médica sorrindo no corredor com chips: tira dúvidas 24 horas, recebe agendamentos."),
("Domingo, 22h. Alguém quer marcar consulta.\n\nCom agenda online, você acorda na segunda com horários preenchidos, sem atender nenhuma ligação.\n\n"+CTA_LINK,['#agendamentoonline','#fimdesemana'],"Duas notificações de nova consulta agendada no domingo à noite."),
("Pare de perder paciente na ligação.\n\nCada chamada perdida é um paciente que liga para o próximo médico da lista. Com agenda online, ele marca sozinho.\n\n"+CTA_DM,['#atendimento','#secretariamedica'],"Ícone de telefone e lista de chamadas perdidas ao longo da manhã."),
("3 erros que afastam pacientes do seu site:\n\n1. Não ter botão de agendar\n2. Texto técnico demais\n3. Não abrir bem no celular\n\nSeu site tem algum desses? Conta aqui.",['#dicasdemarketing','#webdesign'],"Lista de três erros marcados com X vermelho."),
("Paciente quer facilidade.\n\nAgendar em 1 minuto, receber lembrete no WhatsApp, saber como chegar. Quanto mais fácil marcar, mais gente marca.\n\n"+CTA_LINK,['#experienciadopaciente','#agendaonline'],"Coração com batimento e chips: agenda em 1 minuto, lembrete automático, como chegar."),
("Seu concorrente já tem agenda online.\n\nMesma nota, mesmo bairro. O paciente escolhe quem dá para marcar agora, sem esperar o horário comercial.\n\n"+CTA_DM,['#concorrencia','#googlemeunegocio'],"Busca no Google com concorrente com botão Agendar e você apenas com ligação em horário comercial."),
("Seguidor não paga consulta. Paciente paga.\n\nAudiência é ótimo. Mas o que mantém o consultório é o caminho do seguidor até a agenda.\n\n"+CTA_LINK,['#marketingmedico2','#instagrammedico'],"Frase em fundo azul escuro: Seguidor não paga consulta. Paciente paga."),
("Do clique à consulta em 4 passos:\n\n1. Busca no Google\n2. Site claro e rápido\n3. Agenda com horário disponível\n4. Consulta confirmada, sem ligação\n\nÉ assim que site vira consulta.",['#jornadadopaciente','#sitemedico'],"Quatro passos com ícones: busca, site, agenda e confirmado."),
("O que vai na primeira tela do seu site?\n\n1. Nome e especialidade\n2. Cidade ou bairro\n3. Foto real\n4. Botão de agendar\n\nEm 3 segundos o paciente precisa entender quem você é e como marcar.",['#webdesign','#dicasdemarketing'],"Primeira tela de site de dermatologista com quatro itens numerados ao lado."),
("Mais tempo pra atender.\n\nMenos tempo agendando no telefone, mais tempo cuidando de quem está na sua frente.\n\n"+CTA_DM,['#produtividade','#gestaodeclinica'],"Foto de médica escrevendo na mesa com chips: menos horas no telefone, agenda organizada. Valor ilustrativo."),
("Faltou de novo? Manda lembrete.\n\nUm lembrete automático 24h antes, com botão para confirmar. O paciente lembra e a agenda agradece.\n\n"+CTA_LINK,['#lembreteautomatico','#whatsapp'],"Conversa de lembrete de consulta com confirmação do paciente e um sino."),
("Médico precisa de marketing?\n\nNão é sobre dancinha no Reels. É sobre ser encontrado no Google, passar confiança antes da consulta e facilitar o agendamento.\n\nConcorda? Comenta aqui.",['#marketingparamedicos','#medicos'],"Estetoscópio com chips: ser encontrado, passar confiança, facilitar o agendamento."),
("Um site pra cada especialidade.\n\nDermatologia, odontologia, pediatria, psicologia, nutrição, ortopedia, ginecologia, fisioterapia. Cada uma tem um paciente diferente, e o site precisa falar com ele.\n\nQual é a sua? Comenta aqui.",['#odontologia','#psicologia','#nutricao'],"Grade com oito especialidades da saúde, cada uma com um ícone."),
("Você aparece no Google Maps?\n\nPerfil no Google bem cuidado junto com um site com agenda é a dupla que traz o paciente do bairro.\n\n"+CTA_DM,['#googlemaps','#googlemeunegocio'],"Mapa com pino de localização e card da clínica com botão Site."),
("Como funciona a Web Clinic:\n\n1. Diagnóstico do seu momento\n2. Site com a sua cara\n3. Agenda online integrada\n4. Pacientes marcando sozinhos\n\nVocê atende. A gente cuida do caminho até a consulta.\n\n"+CTA_LINK,['#webclinic','#sitemedico'],"Quatro passos da Web Clinic: diagnóstico, site, agenda e pacientes."),
("Seu paciente quer marcar agora.\n\nNão deixe para amanhã quem quer marcar hoje. Com agenda online, o horário é escolhido em um clique.\n\n"+CTA_DM,['#agendaonline','#pacientes'],"Foto de médica de óculos com chips: agendar consulta em 1 clique, horário escolhido."),
("Menos telefone, mais consulta.\n\nAgenda online aberta 24h e WhatsApp só para quem já marcou. Uma rotina mais leve começa por um site que agenda por você.\n\n"+CTA_LINK,['#rotina','#consultorio'],"Foto de médica em consultório com chips: agenda online aberta 24h e WhatsApp."),
("Vamos encher sua agenda?\n\nA Web Clinic cria sites que convertem para médicos e profissionais da saúde.\n\nFale com a gente pelo link na bio ou mande SITE no direct.",['#webclinic','#marketingparamedicos'],"Logo da Web Clinic com o botão Fale com a Web Clinic."),
]
assert len(L)==40
TIT=["Sites que viram consulta marcada","Sua agenda não fecha às 18h","Secretária só pra atender telefone?","Instagram não marca consulta","O paciente te pesquisa antes de ligar","Paciente que esquece a consulta?","Site bonito não basta","5 coisas que todo site médico precisa","Seu site abre em 3 segundos?","Link na bio que leva pro nada","Quem marca à noite não liga de dia","Horário vago é dinheiro parado","Seu paciente está no celular","Avaliação no Google vale ouro","WhatsApp lotado de pergunta repetida?","Ninguém agenda com quem não encontra","O site trabalha enquanto você atende","Confirmação automática. Sem planilha","Seu site passa confiança?","Antes e depois da agenda online","Botão de agendar em todas as páginas","Clínica sem site parece fechada","Seu site é a sua recepção digital","Domingo, 22h. Alguém quer marcar","Pare de perder paciente na ligação","3 erros que afastam pacientes","Paciente quer facilidade","Seu concorrente já tem agenda online","Seguidor não paga consulta","Do clique à consulta","O que vai na primeira tela do site?","Mais tempo pra atender","Faltou de novo? Manda lembrete","Médico precisa de marketing?","Um site pra cada especialidade","Você aparece no Google Maps?","Como funciona a Web Clinic","Seu paciente quer marcar agora","Menos telefone, mais consulta","Vamos encher sua agenda?"]

# cronograma: 4 posts por dia (9h, 12h, 15h, 19h), todos os dias, a partir de 13/11/2026
INICIO=datetime.date(2026,11,13); HORAS=['9h','12h','15h','19h']
DATAS=[INICIO+datetime.timedelta(days=i//4) for i in range(40)]; HR=[HORAS[i%4] for i in range(40)]
DS=['seg','ter','qua','qui','sex','sáb','dom']
fd=lambda d:f'{DS[d.weekday()]} {d:%d/%m/%Y}'

os.makedirs('pdfimg',exist_ok=True)
for i in range(1,41):
    f=f'pdfimg/{i:02d}.jpg'
    if not os.path.exists(f):
        im=Image.open(f'../posts/post-{i:02d}.png').convert('RGB').resize((1080,1350)); im.save(f,quality=88)

def tags(extra):
    t=[]; [t.append(x) for x in BASE+extra if x not in t]
    return ' '.join(x.rstrip('2') for x in t)
def esc(s): return html.escape(s).replace('\n','<br>')
CSS=f'''<link rel="stylesheet" href="base.css"><style>
@page{{size:1080px 1350px;margin:0}} html,body{{width:auto;height:auto;overflow:visible;background:#F7F9FC}}
.pg{{width:1080px;height:1350px;position:relative;overflow:hidden;padding:84px 80px;page-break-after:always;background:#F7F9FC}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:40px}} .top .nm{{font-size:22px;font-weight:600}} .top .pn{{margin-left:auto;font-size:16px;color:{C};letter-spacing:.12em}}
h1{{font-size:62px;line-height:1.04;letter-spacing:-.04em;font-weight:300;color:{N}}} h1 b{{font-weight:700;color:{A};display:block}}
.k{{font-size:14px;letter-spacing:.22em;color:{A};font-weight:600}}
.bx{{background:#fff;border:2px solid #E2EAF4;border-radius:24px}}
.alert{{background:#FFF1F2;border:2px solid #FBC9CE;border-radius:20px;padding:18px 22px;font-size:20px;line-height:1.45;color:{N}}} .alert b{{color:#D63848}}
ol{{padding-left:30px}} li{{font-size:20px;line-height:1.5;margin-bottom:8px}} li b{{color:{A}}}
table{{border-collapse:collapse;width:100%}} td{{font-size:16px;padding:7px 8px;border-bottom:1px solid #EEF2F7}} td:first-child{{color:{A};font-weight:700;width:46px}}
.lab{{font-size:13px;letter-spacing:.2em;color:{C};font-weight:600;margin-bottom:6px}}
.val{{font-size:19px;line-height:1.4;color:{N}}} .url{{font-size:14px;color:{C};word-break:break-all}}
.cap{{font-family:Inter,sans-serif;font-size:19px;line-height:1.5;color:{N}}}
</style>'''
pages=[]
def top(t): return f'<div class="top">{roundlogo(46)}<div class="nm">webclinic</div><div class="pn">{t}</div></div>'

# capa
pages.append(f'''<div class="pg"><div style="display:flex;justify-content:center;margin-top:80px">{roundlogo(200)}</div>
<div style="text-align:center;margin-top:50px"><div class="k">PLANO DE POSTAGEM</div><h1 style="font-size:88px;margin-top:18px">40 posts<b>pra postar.</b></h1>
<div style="font-size:26px;line-height:1.5;margin:28px auto 0;max-width:760px">Imagem, legenda, hashtags, texto alternativo e data de cada post. Feito para publicar pelo <b style="color:{A}">Meta Business Suite, só no Instagram.</b></div></div>
<div class="alert" style="margin:60px auto 0;max-width:820px;text-align:center;font-size:24px"><b>SÓ INSTAGRAM.</b> Nada destes posts vai para o Facebook.</div></div>''')

# instruções
steps=[("Abra o <b>Meta Business Suite</b> (business.facebook.com) e selecione a conta da <b>Web Clinic</b>.",),
("Vá em <b>Planejador</b> (ou Conteúdo) e clique em <b>Criar post</b>.",),
("Em <b>Publicar em</b>, deixe marcada <b>somente a conta do Instagram</b> da Web Clinic. <b>Desmarque a Página do Facebook.</b>",),
("Tipo: <b>post de feed</b> com <b>uma imagem</b>. Não é Reels, não é Story, não é carrossel.",),
("Em <b>Adicionar mídia</b>, envie o arquivo <b>post-XX.png</b> do post (link na página dele). Mantenha a proporção <b>4:5</b> (1080 × 1350), sem cortar.",),
("Em <b>Texto</b>, cole a <b>legenda</b> exatamente como está e, numa linha abaixo, as <b>hashtags</b>.",),
("Em <b>Texto alternativo</b> (configurações avançadas da imagem), cole o texto alternativo.",),
("Clique na seta ao lado de Publicar → <b>Programar</b>. Use a <b>data e hora</b> da página do post (horário de Brasília).",),
("Confira a prévia do Instagram (imagem inteira, legenda sem cortes) e confirme. Marque o post como feito no checklist.",)]
pages.append(f'''<div class="pg">{top("INSTRUÇÕES · PARA QUEM VAI POSTAR")}<div class="k">PASSO A PASSO</div><h1 style="margin-top:12px">Como publicar<b>cada post.</b></h1>
<div class="alert" style="margin-top:30px"><b>Só Instagram, só feed.</b> Não publicar no Facebook, não fazer Reels/Stories, não impulsionar, não marcar pessoas, não responder comentários ou mensagens sem o dono pedir.</div>
<div class="bx" style="margin-top:26px;padding:28px 34px"><ol>{''.join(f'<li>{s[0]}</li>' for s in steps)}</ol></div>
<div style="display:flex;gap:20px;margin-top:22px"><div class="bx" style="flex:1;padding:20px 24px"><div class="lab">ORDEM</div><div class="val">Publicar do <b>post 01 ao 40</b>, na ordem. Depois que o 01 sair, <b>fixar no perfil</b>.</div></div>
<div class="bx" style="flex:1;padding:20px 24px"><div class="lab">CADÊNCIA</div><div class="val"><b>4 posts por dia</b>, às <b>9h, 12h, 15h e 19h</b>, todos os dias. {DATAS[0]:%d/%m} a {DATAS[-1]:%d/%m/%Y}.</div></div></div></div>''')

# cuidados
pages.append(f'''<div class="pg">{top("INSTRUÇÕES · CUIDADOS")}<div class="k">ANTES DE COMEÇAR</div><h1 style="margin-top:12px">Confira<b>estes pontos.</b></h1>
<div class="bx" style="margin-top:34px;padding:28px 34px"><ol>
<li><b>Arroba:</b> as artes mostram <b>@webclinic</b>. Se o perfil real tiver outro @, pare e peça para o Claude gerar as artes de novo antes de postar.</li>
<li><b>Arquivos:</b> use sempre o PNG em alta (link de cada página ou pasta <b>webclinic/posts/</b> do repositório DOTAGENCIA). As imagens deste PDF são só prévia.</li>
<li><b>Legendas:</b> copie sem editar. Se o Business Suite cortar as quebras de linha, mantenha os parágrafos separados por uma linha em branco.</li>
<li><b>Hashtags:</b> no fim da legenda, numa linha separada. Não adicionar outras.</li>
<li><b>Exemplos ilustrativos:</b> nomes (Dra. Ana Paula, Maria…), avaliações e números das artes são exemplos de como um site pode ficar, não resultados de clientes. Não dizer o contrário na legenda nem nos comentários.</li>
<li><b>Mudou a data?</b> Pode reprogramar, mas mantenha a ordem dos posts.</li>
<li><b>Deu erro</b> (imagem cortada, conta errada, post no Facebook): apague, avise o dono e refaça.</li></ol></div></div>''')

# cronograma
rows=''.join(f'<tr><td>{i+1:02d}</td><td>{fd(DATAS[i])} · {HR[i]}</td><td>{html.escape(TIT[i])}</td><td style="color:#B5C0D0">☐</td></tr>' for i in range(40))
half=lambda a,b:f'<table>{"".join(rows.split("</tr>")[a:b]).replace("<tr>","<tr>")}</table>'
R=[f'<tr><td>{i+1:02d}</td><td style="width:200px">{fd(DATAS[i])} · {HR[i]}</td><td>{html.escape(TIT[i])}</td><td style="width:30px;color:#9AA8BC">☐</td></tr>' for i in range(40)]
for k in range(2):
    pages.append(f'''<div class="pg">{top(f"CRONOGRAMA · {k+1}/2")}<div class="k">CHECKLIST</div><h1 style="margin-top:12px">{"Quando postar" if k==0 else "Continuação"}<b>{"cada um." if k==0 else "do cronograma."}</b></h1>
<div class="bx" style="margin-top:30px;padding:16px 26px"><table>{"".join(R[k*20:(k+1)*20])}</table></div></div>''')

# 40 posts
for i,(cap,ex,alt) in enumerate(L):
    n=i+1; url=RAW.format(n)
    pages.append(f'''<div class="pg" style="padding:70px 80px">{top(f"POST {n:02d} DE 40")}
<div style="display:flex;gap:30px;align-items:flex-start">
<img src="pdfimg/{n:02d}.jpg" style="width:420px;border-radius:18px;border:2px solid #E2EAF4">
<div style="flex:1;display:flex;flex-direction:column;gap:14px">
<div class="bx" style="padding:16px 20px;background:{A};border-color:{A}"><div class="lab" style="color:#CFE6F7">QUANDO</div><div class="val" style="color:#fff;font-size:26px;font-weight:600">{fd(DATAS[i])} · {HR[i]}</div></div>
<div class="bx" style="padding:16px 20px"><div class="lab">ONDE</div><div class="val"><b>Só Instagram</b> · feed · 1 imagem 4:5<br><span style="color:#D63848">Facebook desmarcado</span></div></div>
<div class="bx" style="padding:16px 20px"><div class="lab">ARQUIVO</div><div class="val"><b>post-{n:02d}.png</b><br><span class="url">{url}</span></div></div>
<div class="bx" style="padding:16px 20px"><div class="lab">TEXTO ALTERNATIVO</div><div class="val" style="font-size:16px">{esc(alt)}</div></div>
</div></div>
<div class="bx" style="margin-top:24px;padding:24px 28px"><div class="lab">LEGENDA (COPIAR EXATAMENTE)</div><div class="cap">{esc(cap)}</div>
<div class="lab" style="margin-top:18px">HASHTAGS</div><div class="cap" style="color:{A}">{tags(ex)}</div></div></div>''')

open('postar.html','w').write(f'<!doctype html><html><head><meta charset="utf-8">{CSS}</head><body>{"".join(pages)}</body></html>')
# legendas em texto puro também
with open('../posts/legendas.txt','w') as f:
    for i,(cap,ex,alt) in enumerate(L):
        f.write(f'===== POST {i+1:02d} · {fd(DATAS[i])} {HR[i]} · arquivo post-{i+1:02d}.png · SÓ INSTAGRAM =====\n{cap}\n\n{tags(ex)}\n\n[texto alternativo] {alt}\n\n')
print(len(pages))
