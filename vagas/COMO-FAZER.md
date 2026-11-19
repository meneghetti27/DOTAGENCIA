# Radar de vagas gringas (pedido do dono, 19/11/2026)

- Painel: https://claude.ai/artifact/A7oWm5gPpGMQZcaEEU8Sjq (código em `vagas/painel/index.html`, imagens copiadas do portfólio).
- Tarefa agendada roda 2x por dia (7h40 e 16h40, Brasília), segue `vagas/AGENTE.md` e manda notificação no celular quando tem vaga nota 8+.
- Botão **APLICAR** em cada vaga: o painel chama o Claude (capacidade `sample`) e monta um portfólio sob medida
  (título, "Why I fit", 3–5 projetos reordenados e reescritos para a vaga, experiência, contato), cover letter, respostas
  prontas e dicas em PT. Baixa em PDF (html2canvas + jsPDF, capacidade `downloads`). O kit fica salvo em `kits/<id>`.
  O envio da candidatura é feito pelo dono no site da vaga (o painel não aplica sozinho).
- Para mudar o perfil/projetos usados no kit: constantes `PERFIL`, `PROJETOS`, `XP` no painel. Novos projetos precisam de imagem em `img/`.
- Preferências: qualquer área de design (brand, UX/UI, motion, web, IA), qualquer nível + freelas, sem salário mínimo, até relocation.
