# @plagio.zip: como produzir e entregar (aprovado pelo dono)

**Central fixada no claude.ai:** https://claude.ai/artifact/HsL1Hf3SsueFcjawZ7qczc (código em `plagio/central.html`).
Atualizar sempre esse mesmo link (status da semana, atalhos). Não criar outro.

## Aprovação (regra do dono): pela Central, nunca por planilha
**Nada é agendado sem aprovação.** A aprovação é na própria Central (link acima): cada post mostra imagem + legenda,
com botão **Aprovar** e **lixeira** (Excluir; dá para restaurar).
- Dados: banco do artifact, coleção `posts`, doc `s<semana>-post-NN` com `ordem, semana, titulo, assunto, quando,
  status (pendente|aprovado|excluido), imagem (/_blob/<id>), legenda, conferir, drive_jpg, drive_legenda`.
- Nova rodada: subir os JPGs como assets do artifact (`Artifact` publish `asset:true`, `file_paths`) e criar os docs com `ArtifactData` batch.
- Ler o resultado com `ArtifactData` query em `posts`: agendar só `status == aprovado`; `excluido` → lixeira no Drive (JPG + legenda).

## Frequência
**2 posts por dia: 12h e 19h.** Uma semana usa 14 posts; cada rodada deve render isso depois das exclusões.

## Drive (organização exigida pelo dono)
`PLAGIO POSTS / Semana N (dd-mm a dd-mm) /` com, para cada post:
- `Post 03.jpg`: a arte 1080x1350 como **arquivo de imagem** (nunca Doc com imagem dentro).
- `Post 03 - legenda` (Google Doc): só a legenda, terminando em 🐈‍⬛; embaixo, linha cinza com o que conferir e o crédito da foto.
Pesquisa e rascunhos ficam em `PLAGIO POSTS / _pesquisa ...`.

## Subir JPG no Drive (automático)
O conector do Drive não sobe imagem. Usa-se um Apps Script do dono publicado como App da Web.
URL e senha estão no Drive em `PLAGIO POSTS / _config claude (nao apagar).txt` (ler com o conector; **não** commitar aqui, o repo é público).
1. Commit + push dos JPGs em `plagio/rodada-N/drive-semana-N/Post NN.jpg` (raw do GitHub é público).
2. `curl -sSL -H "Content-Type: application/json" --data @corpo.json URL` com
   `{"senha":..., "semana":"Semana N (...)", "arquivos":[{"nome":"Post 01.jpg","url":"<raw github>"}]}`.
   Resposta `{"ok":true,...}`. O script cria a pasta da semana e substitui arquivos de mesmo nome.
3. Legendas: criar Google Doc pelo conector (`contentMimeType: text/html`, parent = pasta da semana).

## Imagens
- Achar fotos na web (projeto fictício): capas pela API do Deezer (`api.deezer.com/search/album?q=`, `cover_xl` 1000 px);
  fotos de pessoas pela og:image de matérias (Rolling Stone BR, Billboard BR, Complex, HotNewHipHop...). Bing embaralha: não usar.
- **Sempre P&B**, ou P&B com **uma** cor de destaque: `python3 plagio/enquadrar.py FOTO -o PASTA [--foco X,Y] [--acento 340-20] [--inteira]`.
  Capas de disco: `--inteira --acento <cor da capa>` (roxo 260-330, vermelho 340-20, amarelo 42-65).
