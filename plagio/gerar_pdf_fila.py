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
<h1>Agendar a fila<br>no Instagram<span>.</span></h1><h2>Instruções para o Claude no Chrome</h2><ol>
<li>Abra <b>business.facebook.com</b> &gt; <b>Planejador</b> do Instagram <b>@plagio.zip</b>.</li>
<li><b>Primeiro, confira o que já está agendado</b> de 12/11 a 22/11. Compare pela imagem e pela 1ª linha da legenda (título em maiúsculas). <b>O que já estiver agendado, deixe como está</b> e pule.</li>
<li>Agende os que faltam <b>na ordem da fila</b>, a partir do primeiro horário livre, mantendo <b>2 posts por dia</b>: um de manhã/almoço (entre 11h e 13h) e um à noite (entre 18h e 21h). Use o dia e a hora sugeridos em cada página.</li>
<li><b>Varie os horários</b>: não repita o mesmo horário em dois dias seguidos. Os horários sugeridos já são variados; se precisar mudar, mantenha a variação e as faixas acima.</li>
<li>Posts com <b>DATA FIXA</b> não mudam de dia. Se um horário sugerido já passou, agende o post no próximo horário livre (exceto os de DATA FIXA: nesse caso, pule e me avise).</li>
<li>Publique <b>somente no Instagram</b>. <b>Desmarque o Facebook</b> em todos. Nunca publicar no Facebook.</li>
<li>Escolha <b>Agendar</b> (nunca publicar agora). Horário de Brasília.</li>
<li>Imagem: baixe pelo link "Baixar imagem" do post. Quando abrir a janela de arquivo, peça para o usuário selecionar.</li>
<li>Copie a legenda exatamente como está, com quebras de linha e emojis (termina com 🐈‍⬛).</li>
<li>No fim, mostre ao usuário a lista de tudo que ficou agendado de 12 a 22/11, dia a dia, com horário.</li></ol>
<table><tr><th>#</th><th>Sugerido</th><th>Post</th><th>Regra</th></tr>{rows}</table></section>"""]
for i,(k,d,h,r) in enumerate(fila,1):
    x=D(k); n=x["titulo"].split()[-1]
    img=base64.b64encode((R/local[n]).read_bytes()).decode()
    link=f"https://drive.google.com/uc?export=download&id={x['drive_jpg']}"
    pags.append(f"""<section><div class="tag">Fila {i} de {len(fila)} · {E(x['titulo'])}</div><h1 class="q">{E(d)} às {h}</h1>
<div class="grid"><img src="data:image/jpeg;base64,{img}"><div><p class="lab">Só Instagram · Agendar</p>
<p class="lab">Regra: {E(regra_txt[r])}</p><p class="lab">Arquivo: {E(x['titulo'])}.jpg</p>
<p><a href="{link}">Baixar imagem</a><br><span class="url">{E(link)}</span></p></div></div>
<p class="lab">Legenda (copiar exatamente)</p><div class="leg">{E(x['legenda'])}</div></section>""")
css=pathlib.Path(sys.argv[3]).read_text().split("<style>")[1].split("</style>")[0]
pathlib.Path(sys.argv[2]).write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css} table{{font-size:9.5pt}}</style></head><body>'+"".join(pags)+"</body></html>")
print(len(fila))
