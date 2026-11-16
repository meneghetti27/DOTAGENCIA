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

## FOTO = EXATAMENTE O ASSUNTO (bronca do dono, 16/11/2026)
Se o post fala de um tênis, a foto é ESSE tênis. Se fala de um show específico, a foto é DESSE show (ou da capa do disco ao vivo dele).
Se fala de uma turnê, foto da turnê; de um desfile, foto do desfile. Nunca foto genérica do artista no lugar do objeto/evento.
Não achou a foto certa? Troca a pauta.

## Pautas (cobrança do dono, 11/11/2026)
- **Quanto mais atual, melhor.** Prioridade: assuntos da semana (notícias, lançamentos, desfiles, polêmicas, clipes, shows).
  Clássicos e curiosidades só para completar.
- **Título que chama atenção:** curto, provocativo, gancho de curiosidade (não só o nome do disco/artista).
- **Foto que chama atenção:** a imagem mais forte da notícia (momento, expressão, look), nunca foto genérica, pequena ou de produto parado.
- Histórico de reprovação: capas de disco antigas, títulos descritivos, pautas "de enciclopédia".
- Semana 3 (16/11): reprovou TODAS as pautas de Grammy (Latin e Grammy 2027, Beyoncé, J Dilla, Don Toliver), DJ Khaled,
  desfile Yeezy, Duquesa, Rael, Celo Dut, exposição do Racionais. Aprovou: BK' lotando estádio, 808s 18 anos, Criolo (foto forte),
  tênis do A$AP na Puma, entrevista inédita do Tupac, recorde de ouvintes do Racionais, Drake 2 bi, turnê Usher/Chris Brown US$ 77 mi.
  Regra prática: dinheiro e números grandes, tênis/moda, lendas (Tupac, Biggie, Kanye clássico) e rap BR grande; nada de prêmio repetido.

## Facebook: NUNCA postar
O Instagram está ligado a uma página do Facebook só para liberar a postagem automática. **Nada vai para o Facebook**: postar só no Instagram e manter desligado o compartilhamento automático para o Facebook.

## Frequência
**2 posts por dia: 12h e 19h.** Uma semana usa 14 posts; cada rodada deve render isso depois das exclusões.

## Google Drive: NÃO USAR MAIS (dono, 16/11/2026)
O dono não abre o Drive: aprova na Central e agenda pelo PDF. A partir da Semana 3 as artes ficam só no repositório
(`plagio/semana-N/drive/Post NN.jpg`) e o PDF baixa a imagem pelo link raw do GitHub. Não criar pasta nem legenda no Drive.
(Semanas 1 a 3 já estão lá; deixar como está.)

## Drive (histórico, até a Semana 3)
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
  **Nunca faixa preta na janela.** Capas de disco: preencher a janela (corte leve nas laterais, `--foco`); se o corte comer texto
  da capa, `--inteira` (fundo branco, some na moldura). Cor de destaque: roxo 260-330, vermelho 340-20, amarelo 42-65.

## Agendar (Claude no Chrome, um PDF só)
`plagio/gerar_pdf_fila.py` gera um PDF com a fila inteira (instruções + 1 página por post com imagem, link do JPG no Drive e legenda).
O dono anexa no Claude do Chrome. Regras do PDF: conferir no Planejador o que já está agendado e deixar; agendar o resto em ordem,
**2 por dia** (11h–13h e 18h–21h), **variando horários** (nunca o mesmo horário em dias seguidos); posts com DATA FIXA não mudam de dia;
só Instagram, nunca Facebook; no fim listar tudo que ficou agendado.
