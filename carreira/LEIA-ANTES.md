# carreira/ = kit "AI Job Search" (MIT, github.com/ai-job-search-dev/ai-job-search), copiado em 19/11/2026 a pedido do Antônio

- Para usar as skills/comandos dele (/scrape, /rank, /apply, /interview, /expand, /outcome…), abra uma sessão do Claude Code
  **dentro desta pasta** (`cd carreira`), porque `.claude/` daqui só vale aqui dentro.
- O perfil já está preenchido em `CLAUDE.md` (falta e-mail, telefone e LinkedIn: troque `[EMAIL]`, `[PHONE]`, `[LINKEDIN_URL]`).
- Os CVs dele são em LaTeX (pasta `cv/`); compilar precisa de lualatex/xelatex.
- Ligação com o Radar de vagas (`../vagas/`): o Radar acha e dá nota às vagas e monta o portfólio sob medida;
  este kit serve para avaliar uma vaga a fundo (/rank), fazer CV + carta em PDF (/apply) e preparar entrevista (/interview).
- `.github/` daqui não roda (workflows só valem na raiz do repositório).
