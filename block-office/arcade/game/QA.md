# QA — HARD × BLOCK (26/11/2026)

## Como foi testado
- Playwright + Chromium, viewport 390×844 com toque, bot que lê `window.__hxb.dbg()` a cada ~16 ms, prevê onde a bola mais baixa
  vai cair (com reflexo nas paredes) e move a plataforma com `__hxb.setX()`; ofsete aleatório para variar ângulo; versões "0,95" e "0,9"
  erram de propósito de vez em quando. 16 partidas completas (4 rodadas de ajuste); os números abaixo são das 7 com a regulagem final.
- Poderes forçados um a um com `__hxb.pw(tipo)`; fim de jogo, ranking (sem `claude.use` → localStorage), salvar @, card dos Stories
  (via `HXB_CARD.gerar` e pelo botão, com download real), layouts 360×640 / 390×844 / 430×932, console.
- Ganchos de debug adicionados (inofensivos): `__hxb.setX`, `__hxb.pw`, `__hxb.dbg` e o contador interno `DBG`.

## Números (regulagem final, 7 partidas)
| | mín | médio | máx |
|---|---|---|---|
| Fase 1 (HARD NA PAREDE) | 38 s | ~62 s | 98 s |
| Fase 2 (INFERNO SANTO, caveira) | 28 s | ~50 s | 80 s |
| Jogo inteiro | 67 s | ~112 s | 156 s |

- Antes do ajuste: fase 1 65–150 s, chefe derrotado em ~25 s (fácil demais).
- Vidas perdidas: 0–5 por partida (média ~1,5); 1 de 7 partidas terminou em game over na caveira. O chefe é derrotável.
- Poderes: 21–37 caem por partida, de ~95 blocos quebrados = **27–33 %** (alvo 30 %). Todos os 5 foram pegos e funcionam:
  Drop (+2 bolas), Andaime (plataforma 52→76 px, 10 s), Touca (+1 vida, máx. 5), Encolhe (36 px, 8 s), Luz apaga (8 s de escuro com
  luz só em volta das bolas e da plataforma).
- Troca de produto: em 100 % dos rebatidas (ex.: 135/135, 116/116, 119/119).
- Sem túnel nem bola presa: subpassos de 3 px; maior tempo sem quebrar nada = 2,8–9,4 s (antes até 14,7 s).
- Console: 0 erros em todas as partidas e telas. Acentos (PONTUAÇÃO, APAGÃO, ATÉ, NINGUÉM) renderizam certo.
- Mobile: 360×640, 390×844 e 430×932 sem rolagem lateral; tela final cabe inteira em 360×640.

## Bugs corrigidos
1. Faltava `<meta charset="utf-8">` (acentos podiam virar lixo) → adicionado no topo.
2. **Card dos Stories falhava** ("NÃO DEU") quando as imagens deixam o canvas "contaminado" (file:// ou assets servidos de outra origem)
   → agora tenta de novo sem as imagens (desenho de reserva) e sempre entrega o PNG.
3. Link no rodapé do card estourava a largura → tira `https://`, query e `file:`, reduz a fonte e corta com "…".
4. Card dizia "chegou até a fase 2" mesmo quando a pessoa venceu → "derrubou a caveira!".
5. Barra de vida/velocidade/tiro do chefe tinham `8` fixo → usam `boss.max`.
6. Fim de fase arrastado caçando os últimos blocos → depois de 4 s sem quebrar nada, a rebatida ganha um pequeno desvio aleatório.
7. Bola desenhada com 40 px de altura para um raio de colisão de 11 → desenhada com 30 px (parece bater onde bate).

## Ajustes de tempo / dificuldade
- Fase 1: 3 fileiras em vez de 4, a de baixo com 1 de vida; velocidade 265 → 285.
- Caveira: 8 → 10 de vida; tiro a cada 2–3,5 s (antes 1,3–2,7, ficando mais rápido) e acelera menos; fogo some a plataforma 0,6 s (antes 1 s).
- Touca (+1 vida) caía demais (vidas sempre em 5) → peso 2 → 1 na sorteio.
- Bônus de tempo do final: `(120 − tempo) × 25` (antes 140).

## Pendências
- O fundo da fase 1 (`bg2.png`) tem a placa "HARD JEANS SANTO × BLOCK" com velas na faixa y 42–63, logo abaixo do HUD e atrás das motos:
  parece um cabeçalho duplicado. Ajustar em `assets/_gerar_arte.py` (subir/tirar a placa).
- Variância grande de duração (67–156 s): natural em quebra-tijolo; se quiser mais previsível, dá para colocar um "último bloco pisca e
  atrai a bola" ou cronômetro.
- A intro de fase é pulada no primeiro toque (o toque lança a bola): ok para quem joga rápido, mas o nome da fase quase não aparece.
- Ranking online (`claude.use('db')`) só pode ser testado publicado; aqui foi testado o modo local.

## Ideias novas para o drop
1. **Código de cupom secreto**: derrubar a caveira revela um cupom HARDXBLOCK de 10 % no site da Block (converte jogo em venda).
2. **Peça desbloqueada = link direto**: a peça que estava na bola no fim vira botão "VER ESSA PEÇA" com a página do produto.
3. **Contagem regressiva do drop no menu** ("DROP EM 2D 4H") e a tela muda para "JÁ DISPONÍVEL" no dia (gera expectativa).
4. **Bloco dourado raro** (1 por partida) que dá sorteio de uma peça entre quem salvar o @ no ranking (captura de leads).
5. **Ranking semanal com prêmio**: top 3 da semana ganham peça/brinde na loja física da Block (traz gente para a loja).
6. **Modo dupla "marca com o amigo"**: card dos Stories desafia um @ ("@fulano, bate 12.375?") para viralizar.
7. **Skins de plataforma por peça do drop** (calça Dilacerado, jaqueta Artefato) liberadas jogando, mostrando o produto em loop.
8. **Fase bônus "Provador Santo"**: 15 s de chuva de peças para pegar; as que você pegar montam um look que aparece no card.
9. **Efeito sonoro/trilha da Hard Jeans Santo** (vinheta da marca) ao derrotar a caveira, reforçando a identidade.
10. **QR code na etiqueta das peças físicas** que abre o jogo com uma vida extra (liga o produto comprado ao jogo e vice-versa).
