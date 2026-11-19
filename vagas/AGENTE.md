# Agente "Radar de vagas gringas" (roda 2x por dia sozinho)

Painel: https://claude.ai/artifact/A7oWm5gPpGMQZcaEEU8Sjq (privado, banco `db` do artifact).
Coleções: `vagas/<id>` (uma por vaga), `kits/<id>` (portfólio sob medida, gerado pelo botão APLICAR no painel),
`meta/vistos` ({ids:[…]}), `meta/radar` ({ultima, novas, boas}), `meta/perfil` ({contato}).

## Passo a passo de cada rodada
0. **Fecha as vagas que sumiram**: `ArtifactData query vagas` com where status in ["nova","salva","fila"] → salve os ids em
   `/tmp/abertas.json` → `python3 vagas/checar.py /tmp/abertas.json` → para cada id devolvido, `update` {status:"encerrada"}
   (com `if_version`). Vaga com status "fila" que fechou: encerra também (o painel some com ela).
1. `ArtifactData get meta/vistos` → salve `ids` em `/tmp/vistos.json` (lista JSON). Guarde o `version`.
2. `python3 vagas/buscar.py /tmp/vistos.json > /tmp/novas.json`. Fonte = páginas de vaga das empresas em `vagas/empresas.json`
   (Greenhouse, Lever, Ashby: só lista vaga ABERTA e a candidatura é um formulário único, sem cadastro) + Himalayas só quando o
   link cai nessas plataformas. Já tira vaga que não é de design, presencial, diretor/head/staff, cripto/apostas/adulto e
   publicada há mais de 21 dias. **Nunca** volte a usar Jobicy, We Work Remotely, Remotive, Working Nomads, Remote OK
   (o dono reclamou: vaga velha, link morto, cadastro e entrevista com robô).
3. Leia `/tmp/novas.json` e escreva `/tmp/notas.json` dando nota a CADA vaga (rubrica abaixo). Texto em português, curto.
4. `python3 vagas/montar_docs.py /tmp/novas.json /tmp/notas.json /tmp/lote` → grava `writes.json` e `ids.json`.
5. `ArtifactData batch` com as entradas de `/tmp/lote/writes.json` (máx. 50 por chamada; são vagas novas, sem `if_version`).
6. Atualize `meta/vistos` (ids antigos + `/tmp/lote/ids.json`, mantenha os últimos 4000) com `if_version`,
   e `meta/radar` = {ultima: agora ISO UTC, novas: nº gravadas, boas: nº com nota ≥ 8} com `if_version`.
7. Resposta final (vira a notificação no celular): se houver vaga nota ≥ 8, liste até 3 assim
   "⭐ 9 · Cargo · Empresa · aceita Brasil · salário" + "Abre o Radar e toca em APLICAR."; se não houver, diga só
   "Radar rodou: N vagas novas, nenhuma nota 8+." Não peça nada ao dono, não crie outras tarefas agendadas.

## Quem é o Antônio (para dar nota)
Designer e diretor de arte em Porto Alegre (UTC-3), freelancer desde 2017, inglês fluente (Cambridge First), Design de Produto PUCRS.
Diretor de arte da Prefeitura de POA (prêmio nacional), designer chefe na Schaeffer Digital, único designer na All Education,
social media, anúncios, VSL, embalagem, sites (Web Clinic, Dreamz). **Muito especializado em sistemas de IA para design**
(imagem generativa, geradores automáticos de carrossel, vídeos em código com Remotion, sites feitos com agentes de IA).
Ferramentas: Illustrator, Photoshop, social media, web design, UX/UI. Quer **qualquer nível, fixo ou freela**, sem salário mínimo,
aceita até relocation.

## Rubrica da nota (0–10)
O dono pediu (19/11): não filtrar pelo país dele (inglês nativo), mas só vaga em **inglês ou português** e em que ele
**consegue se inscrever** (link vivo, formulário sem cadastro). O buscador já tira vaga só na Ásia/Europa continental, em
outra língua e com link morto. Vaga "Remote - US" entra, com alerta "o formulário pergunta se pode trabalhar nos EUA".
- +3 aceita Brasil/LATAM/mundo todo (marque `aceita_brasil: true`); remoto EUA/Canadá/UK = +1 e alerta.
- +3 área bate: brand/visual/gráfico, social media, motion/vídeo, web design, UX/UI, **IA generativa** (bônus +1 se a vaga fala de IA).
- +2 nível alcançável (júnior a sênior; diretor/head/staff/principal = −2).
- +1 contrato/freela remoto ou salário bom informado. +1 empresa interessante (marca forte, agência criativa, startup de IA).
- `pular: true` para: plataformas de talentos/marketplace (Lemon.io, Toptal, Turing, Braintrust, Andela, Crossover),
  vaga que exige cadastro com senha, teste ou entrevista em vídeo com IA antes de mandar o portfólio, e não é vaga de design de verdade, golpe/suspeita, cripto/apostas/adulto, estágio só para estudante.
- Campos: `nota`, `resumo` (o que é a vaga, 1–2 frases), `porque` (por que combina com ele), `alerta` (restrição de país,
  nível, red flag; vazio se nada), `area` (UX/UI | Brand | Motion | Vídeo | Web | IA), `aceita_brasil`.
