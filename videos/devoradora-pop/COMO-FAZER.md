# Vídeo "A devoradora": colagem pop-art retrô (aprovado: "tá top")

Reels vertical 1080×1920, 30 fps, ~49 s, feito em **Remotion**. Recriação de um anúncio de agência em colagem pop-art
(fotos retrô recortadas, cores vibrantes, textura de impresso), adaptado para a dot.

- Código da composição: `Video.tsx` (+ `audio.json` com o tempo de cada palavra da narração).
- Imagens prontas para o vídeo: `assets/` (já tratadas). Recortes originais (antes do tratamento): `recortes/`.
- Ferramentas: `tools/buscar-png.py`, `tools/recortar.py`, `tools/tratar-impresso.py`.

## Primeira versão reprovada ("muito longe da referência"): o que deu errado

Antes de tudo, comparar referência × versão nova **lado a lado nos mesmos segundos** (folha com 2 linhas por tempo).
A 1ª versão errou em 4 coisas:
1. **Fotos modernas** de banco (modelo de estúdio, executivo sorrindo). A referência é toda **foto anos 50/60**.
2. **Tudo azul.** "Mudar as cores para a dot" **não é** pintar tudo de azul: o dono escolheu manter a paleta vibrante
   da referência e trocar **só o vermelho dos fundos** pelo azul da dot.
3. **Sem textura.** Tudo limpo e digital. A referência tem cara de papel impresso.
4. **Composições simplificadas.** Copiar cada cena quase quadro a quadro: tamanho, posição, cor e movimento.

## Paleta

| Uso | Cor |
|---|---|
| Fundos que eram vermelhos na referência | azul dot `#2F6BFF` |
| Fundos que já eram azuis na referência | azul mais fundo `#1D4FE0` (para não ficar tudo igual) |
| Selos, estouros, "2 SEGUNDOS", "MILHARES" | amarelo `#FFD21F` |
| Destaques ("ELA.", "PASSAR.", faixa do adesivo) | rosa `#FF5FA2` · laranja `#FF6A1F` |
| Cena "isso não é alcance" | creme `#EFE6D6` |
| Trompetes | fundo vinho `#1A0612` → `#3A0E2C` |
| Texto escuro / sombras | marinho `#0B1A4A`, preto `#09090D` |
| Anúncio mediano | arco-íris de verdade (vermelho, laranja, amarelo, verde, ciano, azul, roxo, rosa) |

## Textura (em tudo, fundos inclusive). O dono cobrou: "tudo com textura inclusive fundo"

- **Fundo de papel** (`Papel`): cor chapada + luz radial no centro + `manchas.jpg` em `soft-light`.
- **Por cima de tudo** (`Textura`): grão animado (4 JPGs `grao0–3` trocando a cada 2 quadros, `overlay` 0,42),
  ~34 pontinhos de poeira claros/escuros mudando a cada 3 quadros, risco vertical de película às vezes e vinheta.
- **Trepidação de película**: deslocamento de ±1,5 px a cada 2 quadros.
- **Não** usar `feTurbulence` animado em tela cheia: o render ficou com 35 min. Grão em JPG pré-gerado é rápido.

## Fotos: onde achar e como tratar

1. **Buscar**: `python3 tools/buscar-png.py nome "vintage woman" pasta` e olhar a folha numerada.
   Funcionou: pngwing (termos curtos em inglês, ex.: "retro woman", "vintage man suit", "money pile", "retro tv",
   "hands reaching", "stressed man", "man pointing", "movie camera", "trumpet", "brain").
   Bloqueados neste ambiente: Pexels, Pixabay, Freepik, Canva, Unsplash (busca); Wikimedia dá 429; Bing devolve lixo.
   Para "foto retrô" o melhor termo foi **"retro woman"** (achou a pin-up com megafone; recortamos só a cabeça).
2. **Recortar**: os PNGs do pngwing vêm com o xadrez desenhado → `python3 tools/recortar.py in.png out.png [modelo]`.
   `isnet-general-use` na maioria; `u2net` para dinheiro em chamas; `u2net_human_seg` para pessoa com terno desfocado.
3. **Tratar como impresso**: `python3 tools/tratar-impresso.py recortes/ assets/`
   - devoradora: tom vintage (dessatura um pouco, puxa para o quente) + retícula leve + grão;
   - adesivo da devoradora: contorno branco + faixas **preta, laranja, rosa e pontilhado azul** (distância calculada com scipy;
     `MaxFilter` com raio grande trava);
   - TVs e mãos: posterizar em **roxos** (4–5 tons) + retícula;
   - cara estressado: posterizar em **3 tons** (marinho, azul, creme);
   - homem apontando e câmera: preto e branco posterizado + retícula;
   - trompetes: posterizar em vinho, rosa e amarelo;
   - pilha de dinheiro e cérebro: retícula forte.

## Roteiro e cenas (tempos vêm das palavras da narração)

Narração: ElevenLabs **eleven_v4**, voz **Moutella** (masculina BR), um take só, com marcações de emoção
(`[mischievously]`, `[serious]`, `[sarcastic]`, `[intense]`, `[frustrated]`, `[confident]`, `[excited]`, `[playful]`).
Cada cena começa 4 quadros antes da sua palavra-gatilho; textos entram junto com a palavra (`em('palavra', n)`).

| # | Gatilho | Cena |
|---|---|---|
| 1 | início | Fundo azul. Devoradora grande embaixo, boca aberta. Mão vindo de cima segura o homenzinho vintage pelo chapéu (pinça calculada no PNG: ponto entre polegar e indicador, braço girado 187°). "ELA É UMA..." + *Devoradora!* em Lora marinho no canto. Tarja "SEUS ANÚNCIOS MEDIANOS" nos olhos + seta desenhada. "SEU ORÇAMENTO" no homenzinho. Em "jantar" ele cai na boca, "NHAC!" (Bangers azul em estouro amarelo) e depois tela cheia com a boca e notas voando; fade branco. |
| 2 | "todo" | Preto. Pilha de dinheiro (8 cópias) crescendo de baixo + chamas de desenho em 4 camadas tremendo. "QUEIMADO EM ANÚNCIOS ESTE MÊS", contador R$ até 48.750 (sombra azul), "TODO. MÊS.", selo "VENDAS: 0" vazado azul, "MILHARES" amarelo, "NINGUÉM LEMBRA." em Permanent Marker. Sai com glitch em fatias. |
| 3 | "mesmo" | Azul. 3 TVs roxas empilhadas; telas: banco de imagem (2 executivos), "QUALIDADE PREMIUM" + selo 1998, "NOVO!!!". Selo amarelo "IGUAL." batendo em cada "mesmo/mesma". Cursor entra e clica em "pulo" → chiado. Saída em chicote borrado. |
| 4 | "você" | Azul fundo. Estouro laranja girando, 12 mãos roxas avançando, celular com anúncios rolando. "VOCÊ TEM 1,7s → 0,0s / ANTES DO DEDÃO DECIDIR". |
| 5 | "anúncio" | Arco-íris em zigue-zague girando, cara estressado em 3 tons, "ANÚNCIO MEDIANO NÃO SOBREVIVE / 2 SEGUNDOS." (amarelo), chips mono pretos (CTR, ROAS, FREQ.), palavras soltas em mono. "DE NOVO." branco com contorno e separação RGB se multiplicando. |
| 6 | "isso" | Papel creme. "ISSO NÃO É / ~~ALCANCE.~~" (risco azul), "ISSO É ALIMENTAR / *a devoradora.*", notas voando, adesivo da devoradora subindo. Saída: pontos azuis crescendo (retícula). |
| 7 | "Nielsen" | Azul fundo + retícula de pontos embaixo. Selos creme "NIELSEN, 2017." e "NÃO É O ORÇAMENTO.", "CRIATIVO" creme gigante, cérebro voando de pequeno até grande, raios amarelos piscando, "≈25% → 47%". |
| 8 | "orçamento" (2º) | Fundo começa azul-claro e vai para o azul. Homem apontando (PB) com câmera antiga na cabeça, flash girando, "● REC". "O ORÇAMENTO COMPRA / A TELA." e "SÓ A IDEIA / COMPRA ATENÇÃO." com círculo amarelo desenhado em IDEIA. |
| 9 | "então" | Vinho. 5 trompetes rosa/amarelo em fileira diagonal tocando, ondas sonoras. "PARA DE / ALIMENTAR / ELA." (amarelo/branco/rosa) → "FAÇA UM ANÚNCIO / QUE NINGUÉM / CONSIGA / PASSAR.". Sai com catavento colorido. |
| 10 | "isso" (3º) | Raios coloridos girando, estouro amarelo com contorno preto: "É ISSO QUE A GENTE FAZ NA..." → logo **dot.** Homenzinho correndo no topo, @marketingdotagency, "MANDA “POP”" (caixa branca, borda preta) + "E GANHE UMA IDEIA DE ANÚNCIO". |

Títulos: **Anton** maiúsculo com **sombra dura deslocada** (marinho, preta ou azul), entrando com mola.
Cada corte: soco de zoom (1,07 → 1) + tremida de 5 quadros + whoosh.

## Sons

Whoosh em cada corte; impacto no "NHAC!"; carimbo em cada "IGUAL."; tique no clique do cursor; risco no glitch e no chiado;
pop nos "DE NOVO." e no CTA; batida no risco do "ALCANCE"; ding no logo. Trilha baixinha (0,05) que sobe no fecho.

## Render e entrega

- Render ~20 min (textura pesa). Normalizar para −14 LUFS com pico ≤ −1 dBTP (limiter + loudnorm em 2 passadas).
- O grão deixa o arquivo enorme: para mandar pelo chat, comprimir por taxa (`-b:v 4300k -maxrate 5000k`), não por CRF.

## Legenda usada

Gancho com emoji ("🍽️ Seus anúncios são uma devoradora..."), os pontos do roteiro em linhas curtas com emoji,
dado da Nielsen, "🔵 É isso que a gente faz na dot." e CTA "📩 Manda "POP" no direct...", hashtags no fim.
