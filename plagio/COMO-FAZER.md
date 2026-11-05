# @plagio.zip: como produzir e entregar (aprovado pelo dono)

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
