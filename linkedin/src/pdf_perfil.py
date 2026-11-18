# PDF de instruções para o Claude no Chrome montar o perfil do LinkedIn
import base64, html, pathlib, subprocess
E=html.escape
SITE="https://claude.ai/artifact/SzkpJxkCam8r5HVtsg2nZp"
RAW="https://raw.githubusercontent.com/meneghetti27/DOTAGENCIA/claude/loving-franklin-c8o6kc/linkedin/out/banner-linkedin.png"
banner=base64.b64encode(pathlib.Path('../out/banner-linkedin.png').read_bytes()).decode()
TIT="Diretor de arte e designer | Direção de arte da comunicação da Prefeitura de Porto Alegre | Identidade visual, campanhas e social media que vendem | Criador do @plagio.zip (+250 mil views/mês)"
SOBRE=f"""Eu faço design que comunica: da ideia ao anúncio que vende, com a estratégia e a peça final no mesmo lugar.

Hoje assino a direção de arte da comunicação oficial de Porto Alegre, uma linguagem visual que fala com mais de 1 milhão de pessoas e foi premiada no Social Media Gov, na categoria Identidade.

Comecei como freelancer em 2017. Desde então passei por estúdio, agências, educação e governo: fui designer chefe na Schaeffer Digital (projetos como a RenauxView), o único designer da All Education e assessor de comunicação na Câmara Municipal, onde vivi uma campanha política do planejamento à rua.

Fora do trabalho, criei o @plagio.zip, página autoral de rap e cultura de Porto Alegre que passa de 250 mil views por mês, com reels de 671 mil visualizações.

O que eu faço:
→ Direção de arte e campanhas
→ Identidade visual e branding
→ Social media, copy e reels
→ Sites e landing pages

Já trabalhei com Prefeitura de Porto Alegre, Olympikus, Maratona Internacional de POA, Museu do Inter, Museu do Grêmio, RenauxView, Câmara Municipal e outras.

Formado em Design de Produto pela PUCRS. Inglês fluente (Cambridge First).

Portfólio: {SITE}"""
# (cargo, empresa, tipo, inicio, fim, local, descricao, competencias)
EXP=[
("Diretor de arte e designer","Prefeitura de Porto Alegre","Tempo integral","2026","atual (marcar 'Trabalho atual neste cargo')","Porto Alegre, RS",
"""No Gabinete de Comunicação Social, lidero a execução da comunicação visual da cidade: 156, educação, limpeza urbana, praças, eventos e datas da cidade. Criei uma linguagem consistente para falar com mais de 1 milhão de pessoas.
→ Premiado no Social Media Gov, categoria Identidade.
→ Campanhas com Olympikus (Maratona Internacional de POA) e com os museus do Inter e do Grêmio.""","Direção de arte, Identidade visual, Campanhas publicitárias"),
("Assessor de comunicação parlamentar","Câmara Municipal de Porto Alegre","Tempo integral","2026","2026","Porto Alegre, RS",
"Comunicação política direta em gabinete de vereador: design, captação e edição de vídeo, relacionamento e gestão de crise. Campanha política completa, do planejamento à rua.","Edição de vídeo, Design gráfico"),
("Designer","All Education","Tempo integral","2025","2026","Porto Alegre, RS",
"Único designer da empresa. Estratégia e execução de toda a comunicação visual: narrativa e ganchos para lives de lançamento, anúncios, VSLs e a identidade da escola botânica @elmundodemusgo.","Copywriting, Edição de vídeo"),
("Designer chefe","Schaeffer Digital","Tempo integral","2023","2025","Porto Alegre, RS",
"Entre design, direção criativa e gestão de projetos. Conduzi projetos de grande porte do planejamento à entrega, com marcas como a RenauxView, maior empresa do setor, e liderei a equipe de design.","Direção criativa, Branding"),
("Social media","Modulo Marketing","Tempo integral","2023","2023","Porto Alegre, RS",
"Criação de conteúdo e peças para redes sociais de clientes da agência.","Social media"),
("Fundador","dot.","Autônomo","PERGUNTAR AO USUÁRIO","atual","Porto Alegre, RS",
"Sites e landing pages de alta conversão + Google Ads para empresas que querem ser encontradas no Google. Do diagnóstico ao relatório mensal.","Web design, Google Ads"),
("Fundador","Web Clinic","Autônomo","PERGUNTAR AO USUÁRIO","atual","Porto Alegre, RS",
"Sites para médicos e clínicas, pensados para o paciente achar, confiar e agendar. Design, texto e publicação.","Web design"),
("Fundador e diretor criativo","plagio.zip","Autônomo","PERGUNTAR AO USUÁRIO","atual","Porto Alegre, RS",
"Página autoral de rap, streetwear e eventos de Porto Alegre. +250 mil views por mês, reel com 671 mil views e 20,5 mil compartilhamentos. Direção de arte, roteiro, motion e IA generativa.","Direção criativa, Motion design"),
("Designer freelancer","Autônomo","Freelance","2017","atual","Porto Alegre, RS",
"Identidade, social media e sites para marcas como Claire Fancin Cosméticos, Pro Mais Vans, BTE Grupo, Dreamz Gallery, Dubal Advocacia, Achiev, Vinhos Meneghetti e InSound.","Identidade visual, Social media"),
]
SKILLS=["Direção de arte","Identidade visual","Campanhas publicitárias","Branding","Design gráfico","Social media","Copywriting","Direção criativa","Motion design","Edição de vídeo","Web design","Adobe Illustrator","Adobe Photoshop","Cinema 4D","IA generativa"]
def bloco(t): return f'<div class="cp">{E(t)}</div>'
exp="".join(f"""<div class="exp"><h3>{i}. {E(c)} · {E(e)}</h3><table>
<tr><td>Cargo</td><td>{E(c)}</td></tr><tr><td>Empresa</td><td>{E(e)} (se existir página oficial, escolher ela na lista para aparecer o logo)</td></tr>
<tr><td>Tipo</td><td>{E(t)}</td></tr><tr><td>Início</td><td>{E(a)}</td></tr><tr><td>Fim</td><td>{E(b)}</td></tr><tr><td>Local</td><td>{E(l)} · Híbrido/presencial: deixar em branco</td></tr>
<tr><td>Competências</td><td>{E(s)}</td></tr></table><p class="lab">Descrição (copiar exatamente):</p>{bloco(d)}</div>""" for i,(c,e,t,a,b,l,d,s) in enumerate(EXP,1))
H=f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:A4;margin:16mm 15mm}}
body{{font-family:Inter,Arial,sans-serif;font-size:10.5pt;color:#1D1D1F;line-height:1.45}}
h1{{font-size:30pt;letter-spacing:-.03em;margin:0 0 6px;line-height:1.05}} h1 span{{color:#D1007A}}
h2{{font-size:15pt;margin:22px 0 6px;border-bottom:2px solid #1D1D1F;padding-bottom:3px;page-break-after:avoid}}
h3{{font-size:11.5pt;margin:14px 0 4px;page-break-after:avoid}}
.tag{{font-size:9pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#6E6E73}}
.cp{{white-space:pre-wrap;background:#F3F3F6;border-left:4px solid #D1007A;padding:10px 12px;border-radius:6px;font-size:10.5pt}}
.lab{{font-size:9pt;font-weight:700;color:#6E6E73;margin:8px 0 3px;text-transform:uppercase;letter-spacing:.05em}}
.alert{{background:#FFF4D6;border:1px solid #E8C14A;padding:10px 12px;border-radius:6px}}
table{{border-collapse:collapse;width:100%;font-size:10pt}} td{{border:1px solid #ddd;padding:4px 7px;vertical-align:top}} td:first-child{{width:23%;color:#6E6E73;font-weight:600}}
.exp{{page-break-inside:avoid}} li{{margin:3px 0}} img{{width:100%;border:1px solid #ddd;border-radius:6px}} a{{color:#0A66C2}}
</style></head><body>
<div class="tag">Antônio Meneghetti · LinkedIn · montar o perfil</div>
<h1>Montar meu perfil<br>no LinkedIn<span>.</span></h1>
<p><b>Instruções para o Claude no Chrome.</b> Leia tudo antes de começar. O perfil é do usuário que está com o LinkedIn aberto e logado neste navegador.</p>

<h2>Regras</h2><div class="alert"><ul>
<li><b>Não publicar nada.</b> Nenhum post, nenhum artigo, nenhuma mensagem, nenhum convite de conexão.</li>
<li><b>Primeiro passo de tudo:</b> desligar o aviso de alterações para a rede (Configurações &gt; Visibilidade &gt; "Compartilhar alterações do perfil" = <b>Não</b>). Sempre que um formulário mostrar "Notificar a rede" ou "Compartilhar com a rede", deixar <b>desligado</b>.</li>
<li>Não mexer em senha, e-mail, telefone, pagamento, Premium nem configurações de privacidade além da de cima. Se pedir login ou verificação, <b>parar e chamar o usuário</b>.</li>
<li>Copiar os textos <b>exatamente</b> como estão (quebras de linha, setas →, acentos).</li>
<li>Onde estiver escrito <b>PERGUNTAR AO USUÁRIO</b>, perguntar antes de salvar aquele item.</li>
<li>Se o perfil já tiver algum item igual (mesma empresa e cargo), <b>editar</b> o existente em vez de criar outro. Não apagar nada que não esteja nesta lista sem perguntar.</li>
<li>Upload de arquivo: baixar pelo link, e quando abrir a janela de escolher arquivo, <b>pedir ao usuário</b> para selecionar.</li></ul></div>

<h2>Ordem</h2><ol>
<li>Desligar "Compartilhar alterações do perfil".</li><li>Idioma e URL personalizada.</li><li>Banner.</li><li>Apresentação (título, local, site).</li>
<li>Sobre.</li><li>Destaque.</li><li>Experiências (9).</li><li>Formação, certificado e prêmio.</li><li>Competências.</li><li>"Aberto a" &gt; Prestar serviços.</li><li>Conferência final.</li></ol>

<h2>1. URL personalizada e idioma</h2><ul>
<li>Em "Editar perfil público e URL", trocar a URL para <b>linkedin.com/in/antoniomeneghetti</b>. Se estiver ocupada, tentar <b>antonio-meneghetti</b>, depois <b>antoniomeneghetti-design</b>.</li>
<li>Idioma principal do perfil: <b>Português</b>.</li></ul>

<h2>2. Banner (foto de capa)</h2>
<p>Baixar: <a href="{RAW}">banner-linkedin.png</a><br><span style="font-size:8.5pt;color:#6E6E73">{E(RAW)}</span></p>
<p>Tamanho 1584×396. Subir sem cortar, sem zoom, sem filtro. A foto de perfil <b>não</b> muda (o usuário vai enviar uma nova depois).</p>
<img src="data:image/png;base64,{banner}">

<h2>3. Apresentação</h2><table>
<tr><td>Nome</td><td>Antônio · Sobrenome: Meneghetti (só conferir)</td></tr>
<tr><td>Pronomes</td><td>não mexer</td></tr>
<tr><td>Título</td><td>{E(TIT)}</td></tr>
<tr><td>Cargo atual</td><td>Prefeitura de Porto Alegre (depois de criar a experiência)</td></tr>
<tr><td>Formação no topo</td><td>PUCRS (marcar "mostrar")</td></tr>
<tr><td>Localidade</td><td>Porto Alegre, Rio Grande do Sul, Brasil</td></tr>
<tr><td>Site</td><td>URL: {SITE}<br>Texto do link: <b>Portfólio</b></td></tr></table>

<h2>4. Sobre</h2>{bloco(SOBRE)}

<h2>5. Destaque</h2><ul><li>Adicionar destaque &gt; <b>Adicionar link</b>: {SITE}</li>
<li>Título: <b>Portfólio · Antônio Meneghetti</b> · Descrição: <b>Identidade visual, campanhas e social media. Prefeitura de Porto Alegre, Olympikus, plagio.zip.</b></li>
<li>Se a imagem de prévia não carregar, deixar assim e avisar no fim. Só esse item no Destaque.</li></ul>

<h2>6. Experiências</h2><p>Criar na ordem abaixo. Em todas: "Notificar a rede" desligado. Sem mídia.</p>
{exp}

<h2>7. Formação, certificado e prêmio</h2><table>
<tr><td>Formação</td><td>Instituição: <b>PUCRS</b> (Pontifícia Universidade Católica do Rio Grande do Sul) · Diploma: Bacharelado · Área: Design de Produto · Fim: 2025 · Início: PERGUNTAR AO USUÁRIO</td></tr>
<tr><td>Licenças e certificados</td><td>Nome: <b>Cambridge English: First (FCE)</b> · Organização: Cambridge Assessment English · Data: PERGUNTAR AO USUÁRIO</td></tr>
<tr><td>Idiomas</td><td>Português: nativo ou bilíngue · Inglês: fluência profissional completa</td></tr>
<tr><td>Prêmios e honrarias</td><td>Título: <b>Social Media Gov · Categoria Identidade</b> · Associado a: Prefeitura de Porto Alegre · Emissor: Social Media Gov · Data: PERGUNTAR AO USUÁRIO · Descrição: Prêmio nacional recebido pela comunicação visual da Prefeitura de Porto Alegre.</td></tr></table>

<h2>8. Competências</h2><p>Adicionar estas 15 (remover sugestões automáticas que não estejam aqui só se o usuário concordar):</p>{bloco(chr(10).join(SKILLS))}
<p>Depois, em "Principais competências" (as que aparecem no topo), escolher: <b>Direção de arte, Identidade visual, Campanhas publicitárias</b>.</p>

<h2>9. Aberto a &gt; Prestar serviços</h2><ul>
<li>Serviços: Direção de arte, Design gráfico, Branding, Web design, Gerenciamento de mídias sociais (até 10, escolher os mais próximos da lista).</li>
<li>Local: Porto Alegre · Trabalho remoto: sim.</li>
<li>Sobre os serviços: <b>Design que comunica, da identidade visual ao anúncio que vende.</b></li>
<li>Na última tela, <b>não</b> publicar o post de anúncio dos serviços. Se o LinkedIn oferecer "Compartilhar", recusar.</li>
<li>"Aberto a trabalho" (procurando emprego): <b>não</b> ativar.</li></ul>

<h2>10. Conferência final</h2><ul>
<li>Abrir o perfil como visitante ("Ver como") e conferir banner, título, link do portfólio, Sobre e Destaque.</li>
<li>Mostrar ao usuário uma lista do que foi feito, do que ficou pendente (datas a perguntar, foto de perfil) e de qualquer erro.</li>
<li>Lembrar o usuário de religar "Compartilhar alterações do perfil" só quando quiser começar a postar.</li></ul>
</body></html>"""
pathlib.Path('perfil.html').write_text(H)
subprocess.run(['node','-e','''const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto("file://"+require("path").resolve("perfil.html"));await p.waitForTimeout(500);await p.pdf({path:"../MONTAR-PERFIL-LINKEDIN.pdf",format:"A4",printBackground:true,margin:{top:"16mm",bottom:"16mm",left:"15mm",right:"15mm"}});await b.close()})()'''],check=True)
