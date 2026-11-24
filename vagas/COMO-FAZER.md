# Radar de vagas gringas (pedido do dono, 19/11/2026)

- Painel: https://claude.ai/artifact/A7oWm5gPpGMQZcaEEU8Sjq (código em `vagas/painel/index.html`, imagens copiadas do portfólio).
- Tarefa agendada roda 2x por dia (7h40 e 16h40, Brasília), segue `vagas/AGENTE.md` e manda notificação no celular quando tem vaga nota 8+.
- Botão **APLICAR** em cada vaga: o painel chama o Claude (capacidade `sample`) e monta um portfólio sob medida
  (título, "Why I fit", 3–5 projetos reordenados e reescritos para a vaga, experiência, contato), cover letter, respostas
  prontas e dicas em PT. Baixa em PDF (html2canvas + jsPDF, capacidade `downloads`). O kit fica salvo em `kits/<id>`.
  O envio da candidatura é feito pelo dono no site da vaga (o painel não aplica sozinho).
- Para mudar o perfil/projetos usados no kit: constantes `PERFIL`, `PROJETOS`, `XP` no painel. Novos projetos precisam de imagem em `img/`.
- Preferências: qualquer área de design (brand, UX/UI, motion, web, IA), qualquer nível + freelas, sem salário mínimo, até relocation.

## Inscrição (decidido pelo dono em 19/11/2026)
- Fontes trocadas: só páginas de vaga das empresas (Greenhouse/Lever/Ashby, lista em `empresas.json`), vaga aberta e recente,
  formulário único sem cadastro. Agregadores antigos foram reprovados (vaga sumida, cadastro + entrevista com robô de IA, link quebrado).
- Fluxo: no Radar ele marca "＋ Quero me inscrever" (status `fila`) → "PREPARAR INSCRIÇÃO" → preenche os dados uma vez
  (`meta/perfil`) → "MONTAR KITS E BAIXAR PDFs" → "COPIAR PEDIDO" e cola no **Claude in Chrome** do computador dele,
  que abre cada formulário, preenche, anexa o PDF da pasta Downloads, cola a carta e envia. Pula a vaga se pedir senha,
  captcha, teste ou vídeo, e no fim lista enviadas/puladas. Depois ele marca "Já me inscrevi".
- Claude na nuvem não cria conta no nome dele nem faz entrevista em vídeo.
- `vagas/checar.py` encerra vagas que sumiram da página da empresa (roda em toda busca).
- Vagas remotas abertas ao Brasil são raras nas empresas grandes (a maioria é "Remote - US"). Para ampliar, adicionar mais
  empresas em `empresas.json` (testar o slug nas APIs com o script de teste) com foco em quem contrata LATAM/mundo.

## Ajustes de 19/11 (2ª rodada)
- `empresas.json` com 322 empresas (descobertas testando nomes de empresas de agregadores nas APIs Greenhouse/Lever/Ashby).
- Filtros: idioma inglês/português, fora vaga só em Ásia/Oriente Médio/Europa continental, link do formulário testado, vagas
  repetidas em várias cidades viram uma, link "Achar recrutador" (busca de pessoas no LinkedIn).
- LinkedIn bloqueia busca vinda da nuvem (429). Por isso o painel tem "＋ Adicionar vagas do LinkedIn": copia um pedido para o
  Claude no Chrome buscar (Remoto, últimas 24 h, Candidatura simplificada, Brasil/LATAM/Worldwide), cola a lista de volta e
  o painel dá nota (capacidade `sample`) e grava como `manual-<id>`. Inscrição no LinkedIn = Candidatura simplificada.
- Ideias tiradas de github.com/ai-job-search-dev/ai-job-search (skill job-scraper): janela curta de data, porta de idioma,
  detectar vaga fechada, juntar vaga repetida, link de recrutador.

## Brasileiras + ideias do radar de TI (pedido do dono, 24/11/2026)
- **Vagas brasileiras entraram**: só as que pagam **mais de R$ 3.000/mês** (faixa que para em 3.000 não serve; júnior/assistente
  sem salário publicado sai) e são **remotas** ou **presenciais/híbridas em Porto Alegre** (Grande POA entra com etiqueta e nota menor).
  Fontes: LinkedIn (API pública de visitante funciona da nuvem: Porto Alegre e Brasil remoto, 1 s entre pedidos), Trampos.co
  (API aberta, vagas criativas) e Remotar (remotas para quem mora no Brasil, BR e gringas; tag "Vaga internacional" = gringa).
  Gupy não tem API pública que funcione (testado: 404).
- Campo `origem` ("br" | "gringa") em cada vaga. Rubrica separada para cada lado em `AGENTE.md`.
- **Painel**: no topo, as **3 melhores brasileiras e as 3 melhores gringas** (entre novas/salvas); filtro "Brasil + gringas / Só
  Brasil / Só gringas"; etiquetas na vaga; "Por que algumas vagas não entraram" (descartes por categoria da última busca).
  Kit (portfólio + carta) de vaga brasileira sai **em português**, com sugestão de pretensão salarial.
- **Notificação no celular**: 3 melhores 🇧🇷 + 3 melhores 🌎 da rodada (nota 7+).
- Ideias tiradas do radar de TI de um amigo (repo `meneghetti27/vagas`, só a técnica, nenhum dado dele):
  - restrição de país escondida ("US-based", "anywhere in the US", W-2, "No C2C", local só "Remote") → `restricao` + nota máx. 4;
    restrição dura (cidadania, autorização sem patrocínio) já sai no buscador;
  - LinkedIn: o campo de local manda (cidade dos EUA = presa lá, mesmo marcada remota); gringa do LinkedIn só entra se o texto abre
    para LATAM/mundo ou o local é Europa/LATAM;
  - agregador só vale com link para o site/ATS da empresa; slugs de Greenhouse/Lever/Ashby vistos nos links viram `meta/empresas`
    e entram nas próximas buscas (o empresas.json cresce sem commit);
  - categoria de descarte em tudo (`rel.descartes` + pulos da nota) e falhas de fonte no resumo, para calibrar os filtros;
  - descarta banco de talentos, treino de IA pago por tarefa (Outlier, Alignerr, micro1), repost de vaga já aplicada;
    marca "2ª vaga na empresa", "recrutadora", "cliente anônimo", "pede teste ou vídeo", "exige conta no site";
  - pedido do Chrome com as **pegadinhas de formulário** (PDF primeiro, clicar a opção exata no menu, conferir campo por campo antes
    de enviar, código por e-mail do Greenhouse, "enviada?" quando não aparece confirmação e conferir no e-mail);
  - carta sem cara de IA: frases curtas, 1 case principal por vaga, lacuna assumida como "onde vou crescer", ownership.
- `checar.py` agora fecha vagas do LinkedIn, Trampos e Remotar, e não fecha mais as coladas à mão (`manual-`) sem motivo.
- A tarefa agendada lê o branch `claude/great-albattani-fy4j41`.
