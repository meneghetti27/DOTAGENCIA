# Agente "Radar de vagas" (roda 1x por dia sozinho, 7h40)

Painel: https://claude.ai/artifact/A7oWm5gPpGMQZcaEEU8Sjq (privado, banco `db` do artifact).
Coleções: `vagas/<id>` (uma por vaga), `kits/<id>` (portfólio sob medida, gerado pelo botão no painel),
`meta/vistos` ({ids:[…]}), `meta/radar` ({ultima, novas, novas_br, novas_gringas, boas, descartes, falhas}),
`meta/perfil` (dados e banco de respostas do formulário), `meta/empresas` ({greenhouse,lever,ashby}: slugs descobertos).

Desde 24/11/2026 o radar traz **gringas e brasileiras** (campo `origem`: "gringa" | "br"). O painel mostra no topo as
3 melhores de cada lado.

## Passo a passo de cada rodada
0. **Fecha as vagas que sumiram**: `ArtifactData query vagas` com where status in ["nova","salva","fila"] → salve os ids em
   `/tmp/abertas.json` → `python3 vagas/checar.py /tmp/abertas.json` → para cada id devolvido, `update` {status:"encerrada"}
   (com `if_version`).
1. Leituras: `get meta/vistos` → `ids` em `/tmp/vistos.json` (guarde o `version`); `get meta/empresas` → `/tmp/extras.json`
   (se não existir, `{}`); `query vagas` com where status == "aplicada" → `/tmp/aplicadas.json` como lista de {empresa, titulo}.
2. `python3 vagas/buscar.py /tmp/vistos.json --extras /tmp/extras.json --aplicadas /tmp/aplicadas.json --relatorio /tmp/rel.json > /tmp/novas.json`
   (leva uns 5–8 min; timeout de 10). Fontes:
   - gringas: páginas de vaga das empresas (`empresas.json` + `meta/empresas`), Himalayas e Remotar só quando o link cai no
     site/ATS da empresa, LinkedIn remoto LATAM/Worldwide;
   - brasileiras: LinkedIn (Porto Alegre e Brasil remoto), Trampos.co e Remotar.
   O script já tira: vaga que não é de design, setor ruim, banco de talentos/treino de IA, idioma fora de pt/en/es, vaga velha,
   link morto, repost de vaga já aplicada, gringa com restrição dura de país (cidadania/autorização EUA sem patrocínio),
   brasileira com salário publicado abaixo de R$ 3.000, júnior/assistente sem salário, presencial fora de Porto Alegre.
   **Nunca** volte a usar Jobicy, We Work Remotely, Remotive, Working Nomads, Remote OK (vaga velha, link morto, cadastro).
3. Leia `/tmp/novas.json` (a descrição INTEIRA de cada vaga) e escreva `/tmp/notas.json` dando nota a CADA vaga pela rubrica
   do lado certo (`origem`). Texto em português, curto. Pulada leva `pular: true`, `categoria` e `motivo` com o trecho da vaga.
4. `python3 vagas/montar_docs.py /tmp/novas.json /tmp/notas.json /tmp/lote` → grava `writes.json`, `ids.json`,
   `descartes.json` e `melhores.json`.
5. `ArtifactData batch` com as entradas de `/tmp/lote/writes.json` (máx. 50 por chamada; vagas novas, sem `if_version`).
6. Atualize com `if_version`:
   - `meta/vistos` = ids antigos + `/tmp/lote/ids.json` (mantenha os últimos 6000);
   - `meta/empresas` = extras antigos + `slugs_novos` do `/tmp/rel.json` (o empresas.json cresce sozinho, sem commit);
   - `meta/radar` = {ultima: agora ISO UTC, novas, novas_br, novas_gringas, boas: nº com nota ≥ 8,
     descartes: soma de `rel.descartes` e `/tmp/lote/descartes.json` por categoria, falhas: `rel.falhas`}.
7. Resposta final (vira a notificação no celular), com `/tmp/lote/melhores.json`:
   ```
   🇧🇷 9 · Cargo · Empresa · Remoto · R$ 6–8 mil
   🇧🇷 …(até 3)
   🌎 9 · Cargo · Empresa · aceita Brasil · US$ …
   🌎 …(até 3)
   Abre o Radar e marca as que quer.
   ```
   Lado sem vaga nota 7+: uma linha "🇧🇷 nenhuma brasileira boa hoje" (ou 🌎). Se alguma fonte falhou (`rel.falhas`), uma
   linha no fim: "⚠ fonte X falhou nesta rodada". Não peça nada ao dono, não crie outras tarefas agendadas.

## Quem é o Antônio (para dar nota)
Designer e diretor de arte em Porto Alegre (UTC-3), freelancer desde 2017, inglês fluente (Cambridge First), espanhol avançado,
Design de Produto PUCRS. Diretor de arte da Prefeitura de POA (prêmio nacional), designer chefe na Schaeffer Digital, único
designer na All Education, social media, anúncios, VSL, embalagem, sites (Web Clinic, Dreamz). **Muito especializado em sistemas
de IA para design** (imagem generativa, geradores automáticos de carrossel, vídeos em código com Remotion, sites feitos com
agentes de IA). Ferramentas: Illustrator, Photoshop, After Effects, Premiere, Figma, web design, UX/UI. Quer qualquer nível,
fixo ou freela. Cidadão **brasileiro, italiano e português** (UE). EUA/Canadá: só visto de estudante, precisa de patrocínio.

## Rubrica GRINGA (0–10)
- +3 aceita Brasil/LATAM/mundo todo/UE (marque `aceita_brasil: true`); remoto EUA/Canadá/UK = +1 e alerta.
- Campo `restricao` preenchido (o buscador achou "US-based", "anywhere in the US", "só diz Remote"…): **nota máx. 4** e alerta
  citando o trecho ("o texto diz 'US-based': precisa morar nos EUA"). Exceção: o texto também abre para LATAM/mundo.
- +3 área bate: brand/visual/gráfico, social media, motion/vídeo, web design, UX/UI, **IA generativa** (bônus +1 se fala de IA).
- +2 nível alcançável (júnior a sênior, art director; head/diretor de design = +0 e alerta).
- +1 contrato/freela remoto ou salário bom informado. +1 empresa interessante (marca forte, agência criativa, startup de IA).

## Rubrica BRASILEIRA (0–10) — pedido do dono em 24/11/2026
Serve: paga **mais de R$ 3.000/mês**, e é **remota** ou **presencial/híbrida em Porto Alegre**.
- +3 área bate (mesmas áreas da gringa; direção de arte e IA contam muito).
- +2 salário: faixa que passa de R$ 6.000 = +2; R$ 3.000–6.000 = +1; não informado = 0 e alerta "salário não informado".
- +2 modelo: remoto = +2; presencial/híbrido em Porto Alegre = +1; Grande POA (Canoas etc.) = +0 e alerta com a cidade.
- +2 nível: pleno, sênior, diretor de arte = +2; júnior com salário publicado ≥ R$ 3.000 = +1.
- +1 empresa interessante (agência criativa, marca forte, produto digital, IA).
- `pular`: salário publicado ≤ R$ 3.000 (categoria `salario`), presencial fora de POA (`presencial`), estágio/aprendiz,
  não é design de verdade (`nao-e-design`), MLM/golpe, banco de talentos (`nao-e-vaga`).

## Regras dos dois lados
- `pular: true` também para: plataformas de talentos/marketplace (Lemon.io, Toptal, Turing, Braintrust, Andela, Crossover),
  vaga que exige teste ou entrevista em vídeo com IA antes de mandar o portfólio, golpe, cripto/apostas/adulto,
  treino de IA pago por tarefa (Outlier, Alignerr, micro1), estágio só para estudante.
- Leia o texto inteiro: restrição de país às vezes vem numa frase sem palavra-chave ("US based candidates only", estados listados,
  faixa salarial por região dos EUA, "No C2C").
- Campos: `nota`, `resumo` (o que é a vaga, 1–2 frases), `porque` (por que combina com ele), `alerta` (restrição de país,
  nível, salário, red flag; vazio se nada), `area` (UX/UI | Brand | Motion | Vídeo | Web | IA), `aceita_brasil`,
  `etiquetas` (opcional, do vocabulário: `exige conta no site`, `pede teste ou vídeo`, `recrutadora`, `cliente anônimo`,
  `2ª vaga na empresa`, `freela`, `PJ`, `CLT`).
- Banco de respostas e regras do formulário ficam em `meta/perfil` (o painel usa no pedido do Chrome).
