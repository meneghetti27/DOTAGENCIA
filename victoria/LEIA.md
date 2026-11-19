# Site Dra. Victoria Oss-Emer

No ar em https://dra-victoria-oss-emer.vercel.app (projeto Vercel sem Git, publicado pela API: `python3 victoria/deploy_vercel.py <arquivo-com-token> <pasta-do-site>`; o token NUNCA vai pro repo) e no artifact https://claude.ai/artifact/GgoPnPAcY8DoAKQ3pdr8xp.
`index.html` = versão atual para a Vercel (sem o invólucro do artifact). Imagens e vídeos ficam em img/ e video/ no projeto da Vercel.
Mudanças de 18/11/2026: WhatsApp Business 5551991890776, sem botão iPhone/Outlook, aviso Porto Alegre maio 2027 (topo, faixa, agendamento, rodapé), pop estilo notificação.

## Área da doutora (19/11/2026)
- `site/` = projeto completo da Vercel (sem Git): `index.html`, `admin/` (painel estilo 07, preto e dourado), `api/` (funções), `package.json`.
  Imagens e vídeos não estão no repo: baixar de https://dra-victoria-oss-emer.vercel.app/img/... e /video/... antes de publicar (o deploy substitui tudo).
- Login em /admin (link "Área da doutora →" no rodapé). Senha inicial passada ao dono; ela troca na aba Senha (hash scrypt no Blob, privado com nome aleatório).
- Dados no Vercel Blob "victoria-agenda" (store_dY9exiutf6sM0nfQ, ligado ao projeto): `dados/agenda.json` (semana, dias, ocupados, textos do site) e `privado/pedidos-*.json`.
- Paciente reserva → POST /api/pedido grava o pedido e marca o horário como ocupado; cancelar no painel libera.
- Publicar: copiar `site/` + img/ + video/ numa pasta e rodar `python3 victoria/deploy_vercel.py <arquivo-token> <pasta>`.
