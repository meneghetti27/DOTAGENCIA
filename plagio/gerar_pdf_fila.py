import json, html, base64, pathlib, sys
E=html.escape
DB=pathlib.Path(sys.argv[1]); R=pathlib.Path("/home/user/DOTAGENCIA/plagio")
docs={p.stem: json.load(open(p)) for p in DB.glob("*.json")}
def D(k): d=docs[k]; return d.get("data",d)
local={"02":"rodada-1/drive-semana-1/Post 02.jpg","13":"rodada-2/drive/Post 13.jpg","14":"rodada-2/drive/Post 14.jpg","16":"rodada-2/drive/Post 16.jpg","19":"rodada-2/drive/Post 19.jpg",
 "21":"rodada-3/drive/Post 21.jpg","22":"rodada-3/drive/Post 22.jpg","25":"rodada-3/drive/Post 25.jpg","26":"rodada-3/drive/Post 26.jpg"}
for n in range(42,62): local[str(n)]=f"semana-2/drive/Post {n}.jpg"
# (id, data, hora, regra)
fila=[("s1-post-02","quinta 12/11","12:00","ja-agendado?"),("s1-post-14","quinta 12/11","19:00","ja-agendado?"),
("s1-post-25","sexta 13/11","12:00","ja-agendado?"),("s1-post-22","sexta 13/11","19:00","ja-agendado?"),
("s1-post-26","sábado 14/11","12:00","ja-agendado?"),("s1-post-13","sábado 14/11","19:00","ja-agendado?"),
("s1-post-21","domingo 15/11","12:00","ja-agendado?"),("s1-post-19","domingo 15/11","19:00","ja-agendado?"),
("s2-post-42","segunda 16/11","11:30",""),("s2-post-58","segunda 16/11","18:40",""),
("s2-post-44","terça 17/11","12:10","FIXA"),("s2-post-45","terça 17/11","20:15",""),
("s2-post-46","quarta 18/11","11:45","ATÉ 19/11"),("s2-post-47","quarta 18/11","19:30",""),
("s2-post-49","quinta 19/11","12:30",""),("s2-post-52","quinta 19/11","18:50",""),
("s2-post-50","sexta 20/11","11:20","FIXA"),("s2-post-56","sexta 20/11","19:45",""),
("s2-post-57","sábado 21/11","12:40",""),("s2-post-61","sábado 21/11","20:00",""),
("s1-post-16","domingo 22/11","12:20",""),("s2-post-55","domingo 22/11","18:30","FIXA")]
regra_txt={"FIXA":"DATA FIXA: a legenda fala \"hoje\". Não mudar o dia.","ATÉ 19/11":"Postar no máximo até 19/11 (dia do lançamento do GTA VI).","ja-agendado?":"Provavelmente já foi agendado pelos PDFs anteriores. Conferir antes.","":"Data flexível."}
rows="".join(f"<tr><td>{i}</td><td>{E(d)} · {h}</td><td>{E(D(k)['legenda'].split(chr(10))[0])}</td><td>{E(r or 'flexível')}</td></tr>" for i,(k,d,h,r) in enumerate(fila,1))
pags=[f"""<section><div class="tag">@plagio.zip · fila de agendamento · 12 a 22/11/2026 · {len(fila)} posts</div>
<h1>Agendar a fila<br>no Instagram<span>.</span></h1><h2>Instruções para o Claude no Chrome (leia tudo antes de começar)</h2>
<h3>Conta e destino</h3><ul>
<li>Conta: Instagram <b>@plagio.zip</b> (conta profissional). Antes de tudo, confirme no topo do Meta Business Suite que a conta selecionada é a do <b>@plagio.zip</b>. Se for outra conta ou outro negócio, <b>pare e pergunte ao usuário</b>.</li>
<li><b>SÓ INSTAGRAM. NUNCA FACEBOOK.</b> A conta está ligada a uma página do Facebook só por exigência técnica. Em <b>todos</b> os posts: em "Publicar em" deixe marcado <b>apenas o Instagram @plagio.zip</b> e <b>desmarque a página do Facebook</b>. Se aparecer "Compartilhar também no Facebook", "Publicar no Facebook" ou parecido: <b>desligado</b>.</li>
<li>Formato: <b>post no feed</b> (foto única). <b>Não</b> é Story, <b>não</b> é Reels, <b>não</b> é carrossel. Desligue "Compartilhar no Story" se aparecer.</li>
<li>Nunca clique em "Publicar agora" nem em "Impulsionar/Promover". Sempre <b>Agendar</b>.</li></ul>
<h3>Antes de agendar: conferir o que já existe</h3><ul>
<li>Abra <b>business.facebook.com</b> &gt; <b>Planejador</b> (Planner), filtro Instagram, e veja <b>12/11 a 22/11/2026</b>.</li>
<li>Compare pela imagem e pela <b>1ª linha da legenda</b> (título em maiúsculas, listado na tabela abaixo). <b>O que já estiver agendado fica como está</b>: não edite, não apague, não reagende.</li>
<li>Se encontrar algo agendado errado (por exemplo, no Facebook, ou duplicado), <b>não apague</b>: anote e avise o usuário no fim.</li></ul>
<h3>Como agendar cada post que falta</h3><ol>
<li>Siga a <b>ordem da fila</b>. Use o dia e a hora sugeridos na página do post.</li>
<li>Mantenha <b>2 posts por dia</b>: um entre <b>11h e 13h</b> e outro entre <b>18h e 21h</b>, horário de Brasília (GMT-3). Confira o fuso do Planejador; se não for Brasília, converta.</li>
<li><b>Varie os horários</b>: nunca o mesmo horário em dois dias seguidos. Os horários sugeridos já são variados.</li>
<li>Se o horário sugerido já passou ou já está ocupado, use o próximo horário livre nas faixas acima e empurre a fila, mantendo 2 por dia. <b>Exceção: DATA FIXA</b> (a legenda diz "hoje") nunca muda de dia; se não der, pule e avise.</li>
<li><b>Imagem</b>: baixe pelo link "Baixar imagem" da página do post (vai para Downloads, nome "Post NN.jpg"). Quando abrir a janela de escolher arquivo, <b>peça ao usuário</b> para selecionar o arquivo certo.</li>
<li><b>Recorte</b>: a imagem é 1080×1350 (4:5). Mantenha <b>4:5 / original</b>. Não deixe virar quadrado 1:1, não aplique filtro nem edição.</li>
<li><b>Legenda</b>: copie <b>exatamente</b> como está, com as quebras de linha entre parágrafos e os emojis. Ela sempre termina com 🐈‍⬛. <b>Não</b> acrescente hashtags, menções, links, local, música, marcação de pessoas nem colaboradores.</li>
<li>Comentários: deixe o padrão (ativados). Não escreva primeiro comentário.</li>
<li>Clique em <b>Agendar</b>, defina data e hora, confirme. Depois confira no Planejador: só o ícone do <b>Instagram</b>, dia e hora certos.</li></ol>
<h3>Se algo der errado</h3><ul>
<li>Pedido de login, verificação, conta diferente, erro de upload, botão diferente do esperado: <b>pare e pergunte ao usuário</b>. Não invente alternativa.</li>
<li>Na dúvida entre publicar agora e agendar: <b>não publique</b>.</li></ul>
<h3>No fim</h3><ul><li>Mostre ao usuário uma tabela de <b>12/11 a 22/11</b>: dia, hora, título do post e se já estava agendado ou foi agendado agora. Liste também o que foi pulado e por quê.</li></ul>
<table><tr><th>#</th><th>Sugerido</th><th>Post</th><th>Regra</th></tr>{rows}</table></section>"""]
for i,(k,d,h,r) in enumerate(fila,1):
    x=D(k); n=x["titulo"].split()[-1]
    img=base64.b64encode((R/local[n]).read_bytes()).decode()
    link=f"https://drive.google.com/uc?export=download&id={x['drive_jpg']}"
    pags.append(f"""<section><div class="tag">Fila {i} de {len(fila)} · {E(x['titulo'])}</div><h1 class="q">{E(d)} às {h}</h1>
<div class="grid"><img src="data:image/jpeg;base64,{img}"><div><p class="lab"><b>Conta @plagio.zip · SÓ Instagram (Facebook desmarcado) · Post no feed · Recorte 4:5 · Agendar, nunca publicar agora</b></p><p class="lab">Antes: confira no Planejador se este já está agendado. Se sim, pule.</p>
<p class="lab">Regra: {E(regra_txt[r])}</p><p class="lab">Arquivo: {E(x['titulo'])}.jpg</p>
<p><a href="{link}">Baixar imagem</a><br><span class="url">{E(link)}</span></p></div></div>
<p class="lab">Legenda (copiar exatamente)</p><div class="leg">{E(x['legenda'])}</div></section>""")
css=pathlib.Path(sys.argv[3]).read_text().split("<style>")[1].split("</style>")[0]
pathlib.Path(sys.argv[2]).write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css} table{{font-size:9.5pt}} h3{{font-size:11.5pt;margin:12px 0 4px}} ul,ol{{margin:4px 0}} li{{margin:3px 0;font-size:10.5pt}}</style></head><body>'+"".join(pags)+"</body></html>")
print(len(fila))
