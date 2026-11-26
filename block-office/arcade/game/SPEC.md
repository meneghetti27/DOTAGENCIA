# HARD × BLOCK — especificação técnica (contrato entre arte, motor e som)

Leia antes: `../../ARCADE-IDEIA.md` (todas as decisões do dono) e `../../referencias/` (fotos da loja; `folha.jpg` = contato).
Jogo promocional do drop HARD JEANS SANTO × BLOCK OFFICE. Textos em **português**. Celular em pé.

## Resolução e estilo
- Tela lógica **270 × 480 px** (9:16), desenhada num canvas e ampliada por inteiro (nearest-neighbor, `image-rendering: pixelated`).
- Pixel art **16-bit detalhado**, com sombra e luz. Paleta base (pode estender com tons do mesmo matiz):
  `#0b0b0f #1d1d24 #34343d #55555f #7b7b86 #a6a6ae #d4d4d8 #f4f2ea` (concreto/blackwork)
  `#2f8f3a #6fd16a` (verde Veneno) `#6b3fa0 #a77be0` (roxo) `#c7261f #f0662a #ffc23d` (chamas/vermelho/amarelo Suzuki) `#3c5a8a` (jeans).
- Fontes (Google Fonts): títulos **"Pirata One"** (gótica, combina com o logo da Hard); números/menus **"Silkscreen"**.

## Arquivos (pasta `game/`)
- `index.html` — motor (formato artifact: sem doctype/html/head/body; começa com `<title>`). Dono: agente MOTOR.
- `audio.js` — define `window.HXB_AUDIO`. Dono: agente SOM.
- `card.js` — define `window.HXB_CARD`. Dono: agente SOM.
- `assets/` — PNGs com transparência. Dono: agente ARTE. Tamanhos em px lógicos (1:1 com a tela de 270×480):

| arquivo | tamanho | uso |
|---|---|---|
| bg1.png, bg2.png, bg3.png | 270×480 | fundos: 1 salão+escada da Block (concreto descascado, escada preta com corrente, spots no trilho) · 2 parede das Suzukis amarelas + mezanino (guarda-corpo de metal) · 3 inferno de noite (céu de cúpulas de vidro, chamas embaixo) |
| paddle.png / paddle-largo.png / paddle-curto.png | 48×12 / 72×12 / 32×12 | plataforma = bloco de concreto vazado (logo da Block) |
| pecas/p1.png … p8.png | altura 26 | as 8 peças do drop (de `../drop/0N-*/`), mesma ordem do `produtos.json` |
| puff1.png puff2.png puff3.png | 20×20 | fumaça ao trocar de peça |
| f1-bloco.png, f1-bloco-rachado.png | 24×12 | fase 1, bloco de concreto vazado (2 batidas: normal → rachado) |
| f1-arara.png | 24×12 | arara de andaime enferrujado (1 batida) |
| f1-placa.png | 36×14 | placa "349" (3 batidas) |
| f2-assento.png | 24×12 | assento de moto preto (1 batida) |
| f2-guarda.png, f2-guarda-torto.png | 24×12 | guarda-corpo de metal (2 batidas) |
| f2-moto.png, f2-moto-dano.png | 48×28 | Suzuki amarela com cintas vermelhas (4 batidas) |
| f3-cupula.png, f3-cupula-acesa.png | 20×14 | cúpula de vidro prismático (1 batida; acesa = brilho) |
| f3-caveira-1.png, f3-caveira-2.png, f3-caveira-dano.png | 72×60 | chefão: caveira do grafite (preto/branco, selo vermelho), 2 quadros de animação + quadro de dano |
| f3-fogo.png | 8×12 | cuspe de fogo da caveira (cai na direção do jogador) |
| pw-drop.png, pw-andaime.png, pw-touca.png | 14×14 | poderes bons (multi-peça, plataforma larga, vida extra = touca da Block) |
| pw-encolhe.png, pw-luz.png | 14×14 | armadilhas (plataforma encolhe, luz apaga) |
| logo-hard.png | ~200 de largura | logo HARD JEANS SANTO pixelado (de `../marca/hard-jeans-santo.jpg`, branco com contorno) |
| logo-block.png | ~64 de largura | bloco hexagonal da Block pixelado (de `../marca/block-logo.webp`) |
| vida.png | 10×10 | ícone de vida no HUD |

## Regras do jogo (para o MOTOR)
- 3 vidas, dificuldade média, partida de 3–5 min. Fases: 1 salão (aprender) → 2 motos/mezanino → 3 inferno com chefão caveira (12 batidas, anda de lado, cospe fogo; fogo tira a plataforma por 1 s se acertar).
- A "bola" é uma peça do drop desenhada girando; **colisão = círculo de raio 6** (igual pra todas).
  **A peça troca para a próxima (p1→p8→p1) a cada batida na plataforma**, com o puff. Parede/alvo não troca.
- Ângulo de rebote depende de onde bate na plataforma. Velocidade sobe um pouco por fase.
- Alvos soltam poder com chance ~12%: Drop (+2 peças), Andaime (largo 10 s), Touca (+1 vida, máx 5), Encolhe (curto 8 s), Luz apaga (8 s: só um círculo de luz em volta das peças).
- Pontos: alvo 1 batida 50 · 2 batidas 100 · placa/moto 250 · caveira 2000 · bônus de vida restante no fim.
- Caveira morre → explode em chuva das 8 peças → tela final.
- Telas: início (logos piscando + "APERTE PRA COMEÇAR") · jogo (HUD: pontos, vidas, fase) · entre fases ("FASE 2 · AS MOTOS") · fim ("HARD × BLOCK / SUA PONTUAÇÃO: 0000",
  campo do @ do Instagram com aviso "seu @ aparece no ranking", TOP 10 geral, botões "VER O DROP" → https://blockoffice.com.br/search/?q=hardxblock, "POSTAR NOS STORIES", "JOGAR DE NOVO").
- Controles: arrastar o dedo/mouse em qualquer lugar move a plataforma; setas/A-D no teclado; toque/clique/espaço lança a peça. Vibração curta (navigator.vibrate) ao quebrar e mais longa ao perder vida.
- Ranking: `const db = await claude.use("db")` (capacidade do artifact); coleção `ranking`, documento por jogada `{arroba, pontos, fase, quando}`;
  ler com `db.collection("ranking").orderBy("pontos","desc").limit(10)`. Se `db` for null, usar só localStorage (try/catch).
  Validar @: `^@?[A-Za-z0-9._]{1,30}$`, guardar com "@".
- Se uma imagem não carregar, desenhar um retângulo colorido no lugar (o jogo nunca quebra).

## APIs entre arquivos
- `HXB_AUDIO.init()` (chamar no 1º gesto) · `.musica(nome)` com nome em `"menu"|"fase1"|"fase2"|"fase3"|"chefe"|"fim"|null` · `.sfx(nome)` com
  `"rebate"|"quebra"|"duro"|"troca"|"poder"|"armadilha"|"vida"|"perdeu"|"fase"|"chefe-dano"|"explode"|"fogo"` · `.mudo(bool)` · `.estaMudo()`.
- `HXB_CARD.gerar({pontos, arroba, fase, pecaImg, logoHard, logoBlock, fonteTitulo, fontePixel})` → `Promise<Blob>` PNG 1080×1920 (Stories),
  pixel art, com "HARD × BLOCK", a pontuação grande, a peça, os 2 logos, "@block.office × @hardjeanssanto" e "JOGUE: <link>" (link vem em `opts.link`).
  O motor salva com `const d = await claude.use("downloads"); d.save({filename:"hard-x-block-score.png", data: blob})`.

## REVISÃO 2 (pedido do dono: "aumentar as peças, mais rápido, mais temático: tem que ficar evidente que é BLOCK × HARD JEANS SANTO")
ARTE (só assets/):
- `pecas/p1..p8.png` agora com **altura 40 px** (era 26), estampa mais legível (mais contraste, usar a cor real das estampas).
- Marca em tudo: nos 3 fundos colocar elementos das duas marcas pintados na cena: logo "HARD JEANS SANTO" gótico grande pichado/lambe na parede,
  bloco hexagonal da Block em neon/placa, cartazes do drop (as peças) colados na parede, faixa "HARD × BLOCK" no mezanino, letreiro "349".
  Sem cobrir o miolo jogável (manter centro e base escuros).
- Novos alvos com marca: `t-hard.png` 24×12 (tijolo preto com letra gótica branca), `t-block.png` 24×12 (bloquinho hexagonal da Block),
  `t-caixa.png` 24×12 (caixa de papelão "HARD × BLOCK"), `t-cartaz.png` 24×16 (cartaz do drop, 2 batidas).
- Novo `banner.png` 270×36: faixa "HARD × BLOCK" com os dois logos (para topo do HUD/telas). `logo-collab.png` ~240×90: os dois logos com "×" no meio.
MOTOR (só index.html):
- Peça desenhada com 40 px de altura; colisor raio 11. Velocidades novas: fase1 230, fase2 260, fase3 290 (+ leve aceleração a cada 10 rebatidas, teto +25%).
- Layouts escrevem as marcas: fase 1 forma a palavra "BLOCK" com t-block/f1-bloco; fase 2 forma "HARD" com t-hard entre as motos; fase 3 tem fileira de t-cartaz acima das cúpulas.
  Misturar t-caixa nos layouts. Alvos t-hard/t-block 1 batida (75 pts), t-cartaz 2 batidas (150), t-caixa 1 (50).
- HUD com `banner.png` no topo; telas de início/entre fases/fim usam `logo-collab.png`; texto das fases: "FASE 1 · O SALÃO DA BLOCK", "FASE 2 · HARD NA PAREDE", "FASE 3 · INFERNO SANTO".
- A cada peça trocada, mostrar nome + preço maior (faixa embaixo por 2 s) e, ao quebrar t-cartaz, soltar a peça do cartaz por um instante ("NOVA PEÇA DO DROP").
