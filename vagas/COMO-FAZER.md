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
