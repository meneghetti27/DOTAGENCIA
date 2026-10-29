# Vídeo "O sistema por trás do crescimento": tipografia cinética (aprovado: "tá top")

Reels 1080×1920, 30 fps, 28 s, feito em **Remotion**. Recriação de um anúncio de agência em tipografia cinética,
adaptado para a dot com os **posts e o site reais da dot** como "trabalhos".

- Vídeo final: `dot-sistema.mp4` (cópia comprimida).
- Código: `Video.tsx` + `audio.json` (tempo de cada palavra da narração).
- Imagens: `assets/` (posts da dot redimensionados para 540×675, prints do site, grão, narração).

## Estrutura e cores

A referência alterna **cenas claras** (branco → amarelo) e **cenas pretas** com brilho amarelo.
Na dot: claras = degradê **branco → gelo `#EEF3FF` → `#B9CCFF` → azul vivo `#2B6BFF`** com uma faixa de luz branca desfocada;
pretas = `#020308` com **brilho azul vindo de baixo** e uma linha azul curva. Grão leve (`overlay` 0,12) em tudo.
Texto escuro `#0A1230` nas claras, branco nas pretas. Fonte **Inter Tight** (600–800, tracking −0,04 em), itálico nas palavras de ênfase.

## Linguagem de movimento (o que faz parecer a referência)

- **Palavras entram com borrão de movimento**: deslizam 60 px na horizontal com `blur(12px → 0)`.
- **Texto digitado com cursor** piscando (`Digita`).
- **Câmera atravessando o texto**: escala 1 → 3,2 (ou 0,5 → 4,5) com desfoque crescente; o painel/próxima cena entra por trás.
- **Ícones 3D brilhantes desfocados** flutuando nas cenas claras (balões de conversa azuis com 3 pontos, "play"), cada um com desfoque diferente = profundidade.
- **Corte**: os primeiros 6 quadros de cada cena entram com zoom 1,08 → 1 e `blur(14px → 0)` + whoosh.

## Roteiro (ElevenLabs eleven_v4, voz Moutella, um take só)

"A maioria das agências vende anúncio. A gente constrói o sistema por trás do crescimento. Google Ads. Landing pages. Sites.
Perfil no Google. Cada peça conectada, feita pra funcionar como uma só. Nada roda isolado. Nada fica no achismo.
Isso não é teoria. É o que acontece quando o crescimento não fica por conta da sorte.
dot. A gente não faz um pouco de tudo. A gente faz o que traz cliente." (fecho = manifesto do site)

| # | Gatilho | Cena |
|---|---|---|
| 1 | início | Claro. "A maioria / das agências" → "vende [ícone megafone em quadrado preto] anúncio." Balões 3D desfocados. |
| 2 | "A gente" | "A gente constrói|" digitado gigante, câmera atravessa; painel escuro "Taxa de conversão 13% → 26% ▲ 12,8%" entra da direita, gráfico desenhando e barras subindo; zoom no painel em "por trás do crescimento". |
| 3 | "Google" | Preto. Pílulas de vidro **Google Ads → Landing pages → Sites** (barra de busca azul digitando + lupa) **→ Perfil no Google** (pin), câmera passando de uma para a outra; posts da dot voando em profundidade; no 2º "Google" recua e mostra a fileira. |
| 4 | "Cada" | Claro. "Cada peça" + pílula branca **Conectada** com brilho. |
| 5 | "feita" | "Feita pra funcionar como uma só." digitado pequeno, zoom lento. |
| 6 | "Nada" | Site da dot rolando dentro de moldura preta + lupa azul: "*Nada roda*" em cima, "*isolado.*" azul embaixo. |
| 7 | "Nada" (2º) | Carrossel dos posts da dot passando com borrão: "*Nada fica no*" / "**achismo.**" |
| 8 | "Isso" | Preto. "Isso *não é* **teoria**" + tabelas de resultado do Google Ads empilhadas em 3D (rotateX 55° → 18°), linha do meio clara com brilho azul. Números ilustrativos. |
| 9 | "É" | "É o que acontece quando o" → **crescimento** gigante passando pela câmera → "não fica por conta da sorte." digitado. |
| 10 | "dot" | Claro. Logo **dot.** em pílula de vidro → "A gente não faz um pouco de tudo." → "A gente faz o que traz cliente.|" |

## Dicas

- Tempo das cenas sai das palavras da narração (`em('palavra', n)`): cuidado com palavras repetidas
  ("a", "é", "nada", "crescimento") e use o índice certo da ocorrência.
- Prints do site: Playwright em 1280×800 abrindo `site/index.html` e rolando (0, 900, 1900 px).
- Render ~15 min; normalizar para −14 LUFS (pico ≤ −1 dBTP). Comprimir por taxa (`-b:v 6000k`) para mandar no chat.
