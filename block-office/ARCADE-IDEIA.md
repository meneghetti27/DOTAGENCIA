# BLOCK OFFICE × HARD JEANS SANTO · ARCADE (ideia fechada em 26/11/2026, ainda não gerado)

Substitui o Block Hunt 3D (arquivado nesta pasta). Mecânica de quebra-tijolo (inspirada no Brick Breaker do BlackBerry,
mas com nome, arte e sons 100% originais: nada do BlackBerry).

- **Plataforma**: bloco de concreto vazado do logo da Block, pixel art.
- **"Bolinha"**: produto do drop com a silhueta real (camiseta, jeans, boné) girando; colisão = círculo invisível (pedido do dono).
- **Alvos**: elementos da loja em pixel art (tijolos OÜS, cúpulas, tênis da prateleira, toca-discos, caixote OÜS, placa 349);
  alguns quebram com 1 batida, concreto/aço com 2–3.
- **3 fases** (escolha do dono): 1 Fachada 349 → 2 Corredor OÜS (tijolo + neon azul) → 3 Noite das cúpulas com as 2 Suzukis amarelas de chefão.
- **Poderes**: Drop (multi-bola), Andaime (plataforma larga), Corrente (atravessa), Lento, Touca (vida extra).
- **Telas**: PRESS START · HUD (pontos, vidas, fase) · fim "BLOCK OFFICE × HARD JEANS SANTO / YOUR SCORE: 0000" + **ranking com apelido**
  (top 10 do dia e geral, banco do artifact) + botão "VER O DROP".
- Pixel art anos 2000, chiptune, celular (arrastar o dedo) e computador (mouse/setas).
- **Material que o dono vai mandar**: logo da Hard Jeans Santo, fotos dos produtos do drop, paleta da collab, link de compra.
- Referências da loja: `ARCADE-IDEIA.md` + `referencias/` + dossiê (Jogo_Block_Office_dossie_completo.pdf, enviado em 26/11).

## Material recebido (26/11)
- `arcade/marca/hard-jeans-santo.jpg` (logo gótico branco no preto) e `arcade/marca/block-logo.webp` (bloco hexagonal vazado).
- `arcade/drop/`: 8 peças (frente `foto-01`, costas `foto-02`) + `produtos.json` com nome, preço e link de cada uma.
- Cores: tiradas das peças (blackwork preto/branco, verde e roxo das asas "Veneno", vermelho/laranja das chamas) + concreto da Block.
- Ajuste proposto: fase 2 com peças atrás de grades ("Revolta"), fase 3 vira "INFERNO" (chamas do raglan) com as Suzukis de chefão.

## Decisões de 26/11 (rodada de perguntas)
- **Fase 1 · Salão + escada** (DENTRO da Block): concreto descascado, escada preta com corrente, spots; alvos = blocos vazados, araras de andaime, placa 349.
- **Fase 2 · Motos e mezanino**: parede das 2 Suzukis amarelas e o mezanino (guarda-corpo de metal, assentos de moto). Corredor OÜS com grades foi reprovado.
- **Fase 3 · Inferno** (noite das cúpulas, chamas): **chefão = caveira do grafite** (gigante, selo vermelho, anda de lado e cospe chamas).
- Celular **em pé**; **3 vidas, médio**; **chiptune + efeitos** com mudo.
- A peça **troca a cada batida na plataforma** (puff de fumaça); parede/alvo não troca. Hitbox circular igual pra todas.
- **Produtos em pixel art** (pedido do dono: JPEG não combina): `arcade/sprites/gerar_sprites.py` recorta, reduz a 48/64 px, paleta de 16 cores,
  contorno claro (peças pretas sumiam no fundo escuro) e usa o lado com a estampa mais forte. Prévia: `arcade/sprites/previa.png`.

## Decisões finais (26/11, 2ª rodada) — é um JOGO PROMOCIONAL pra divulgar o drop
- Nome no jogo: **HARD × BLOCK**. Textos em **português**. Pixel **16-bit detalhado**; fonte gótica pixelada nos títulos + pixel clássica nos números.
- Ranking **só geral**, com o **@ do Instagram** (avisar que fica público). Sem prêmio por enquanto.
- Botão final leva pra **coleção inteira**: https://blockoffice.com.br/search/?q=hardxblock
- **Card pros Stories** (9:16, pixel art, score + peça + logos, marcando @block.office e @hardjeanssanto).
- Poderes: **Drop** (multi-peça), **Andaime** (plataforma larga), **Touca** (vida extra). Armadilhas: **plataforma encolhe**, **luz apaga**.
- Tela inicial: **logos Hard × Block piscando** + "APERTE PRA COMEÇAR". Vibração curta no Android.
- Louis **não aparece**. Partida de **3 a 5 min**. Caveira morre → **explode em chuva das 8 peças** → tela de pontuação.
- Publicar **primeiro como artifact pra teste**; Vercel (link próprio, ranking público) só depois do ok.
