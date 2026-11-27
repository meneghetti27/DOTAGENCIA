# Moletom Terceirão (cliente: turma de 3º ano)

- **Moletom PRETO.** O roxo `#996BB3` (amostra em `referencias/cor-do-moletom.jpg`) é a **cor principal das artes**, não do tecido.
- O trabalho é a **identidade visual do terceirão** (gráficos), **não** montar no moletom: mockup foi descartado pelo dono.
- **Pedido da turma**: referências são **só pras letras**; **sem animal/personagem**; **grafite, não pixação**.
- Estilo escolhido pra 1ª rodada: grafite "bolha" (throw-up): letras Bagel Fat One sobrepostas e giradas,
  contorno preto, 3D roxo-escuro, linha externa no acento, recheio branco com metade de baixo no acento
  (onda + bolhinhas + brilho), escorridos, til desenhado à mão, brilhos de 4 pontas.
- Testado e descartado: estilo bloco com listras (Bungee/Titan): ficou ilegível ("TED CEI DÃO").
- Peças: costas (TER/CEI/RÃO + ano), peito esquerdo ("3" com capelo), manga (ano na vertical),
  forro do capuz (nomes em letra de tag, Sedgwick Ave Display — hoje com nomes de EXEMPLO).
- Paletas (`PALETAS` em gerar.py): `principal` (branco + roxo + 3D uva #4B2C63), `contorno-branco`, `1cor-roxo`, `1cor-branco`.
  Nas versões de 1 cor, o preto da arte = tecido (sem tinta).
- Peças: logo-principal, logo-horizontal, simbolo-3, ano-vertical, estampa-nomes + `artes/painel-identidade.png` (painel.py).

## Gerar
```
python3 gerar.py [principal contorno-branco 1cor-roxo 1cor-branco]  # artes/<paleta>/*.svg + *.png transparentes
python3 previa.py artes/<paleta> saida.jpg                          # prévia no preto
python3 painel.py                                                   # painel da identidade
```
Nomes do forro: lista `NOMES_EXEMPLO` em `gerar.py`. Ano: "2027" em `versao_bolha` e `versao_manga`.
Ajuste de letras: lista `jit` (dx, dy, tamanho, giro por letra) em `versao_bolha`.

## Rodada 2 (dono: "muito feio extremamente") → 10 modelos de escrita
- A identidade com Bagel Fat One (fonte do Google) foi **reprovada**. Usar fontes de grafite de verdade (dafont, categoria graffiti).
- Escola: **Mãe de Deus**. Ano: **2027** (confirmado).
- `python3 modelos.py` → `modelos-escrita/01..10-*.png` + `todos.jpg`. Fontes em `fontes/dafont/`.
  Mesmo acabamento em todos (degradê roxo, contorno preto, linha branca, 3D uva) pra comparar só a letra.
- Fontes demo (decipher, spoken, dunker, splatink, polemic, urban_hustle) trocam números por marca d'água: não usar.
- Licença: a maioria das fontes do dafont é grátis só pra uso pessoal; moletom vendido pede licença comercial do autor.

## Rodada 3 — favoritos + 20 novos
- **Favoritos do dono (salvos em `modelos-escrita/favoritos/`)**: 01 Bloco clássico (beat_mark), 02 Bolha (urban_blocker),
  04 Bloco gordo (graffiti_youth), 09 Old school (grime_slime). Gosto: letra **gorda, legível, bloco/bolha**.
- `python3 modelos.py 2` → 20 novos modelos numerados 11–30 em `modelos-escrita/rodada2/` (+ `todos.jpg`).
- Fonte .otf/.ttf: conferir a extensão real em `fontes/dafont/` (fonte que não carrega vira serifada no PNG).

## Rodada 4 — escolhidas 12, 26, 29 → arte das costas
- Escolhidas: favoritos 01, 02, 04, 09 (rodada 1) **e** 12, 26, 29 (rodada 2) — NÃO descartar os anteriores quando ele escolher novos.
- Dono escolheu **12 Wild leve (break_rebel)**, **26 Bloco inclinado (street_shade)**, **29 Bloco pesado (thomas_2)** (também em `favoritos/`).
- `python3 costas.py` → `costas/<n>-<fonte>.png` (1500×1800 no preto) + `-transparente.png` + `comparar.jpg`.
  Cada linha (TER/CEI/RÃO) é medida pelo desenho real da letra (canvas measureText) e tem ~860 px; 2027 e MÃE DE DEUS centralizados embaixo.
- Til da break_rebel vira bolha preta: `til=True` em ESCOLHIDAS desenha um til grafitado à mão por cima do A.

## Rodada 5 — kit da identidade nos 7 favoritos
- `python3 identidade.py [n ...]` → `identidade/<n>-<fonte>/` com horizontal, peito (3 + capelo), manga (2027 vertical),
  forro (nomes de EXEMPLO em `NOMES`), tudo transparente, + `painel.jpg`; `identidade/todos.jpg` junta os 7.
- Lições: medir com canvas só depois de `document.fonts.load('300px G')` (senão mede a fonte errada);
  camadas com `padding:0 .5em; left:-.5em` pro degradê cobrir a ponta de letra inclinada;
  `tools/html-to-png-exato.js` recorta a janela exata (fullPage aumentava a imagem).
- **Mesmo plano (dono pediu):** as 3 linhas viram um adesivo só: todas as camadas brancas atrás, depois pretas, depois roxo (z-index por camada, rotação em cada camada, sem camada por linha). Nunca uma linha com contorno por cima da outra.

## ✅ ESCOLHIDA: 04 Bloco gordo (graffiti_youth.otf)
Arte final em `identidade/04-graffiti_youth/` + `costas/04-graffiti_youth*.png`. Til à mão menor (0.40 da fonte), entre CEI e RÃO.
Pendente: lista de nomes real (forro) e PDF completo.
- Ajuste: RÃO centralizado (LINHAS dx pequenos) e til novo: forma gorda preenchida com o mesmo acabamento das letras, num respiro entre CEI e RÃO (o til de traço fino foi reprovado: "horrível").
- **Só mexer no que o dono pediu.** TER (-5°, -15) e CEI (-3°, +15) estão aprovados; o ajuste de centro é só no RÃO (-5°, +20).
- RÃO posição aprovada: 12 das 20 (dx 140). Espaçamento CEI↔RÃO: 20 opções em `costas/rao-espaco/` (GAP 0.00–0.38, passo 0.02) aguardando escolha.
- Espaço CEI↔RÃO aprovado: opção 2 (GAP 0.02). Tils: 30 opções em `costas/tils/` (`tils.py`, lista V), aguardando escolha.

## PDF editável (Illustrator)
`python3 exportar_pdf.py` (o PDF do cairosvg abre EM BRANCO no Illustrator: usar o PDF do Chromium via `tools/svg-to-pdf.js`, + SVG e EPS) → `pdf/terceirao-costas-editavel.pdf` (1 página por til: 30 a 72%, 26 a 85%) + SVGs. Tudo vetor (letras em contorno via harfbuzz+fontTools, posições lidas do layout do navegador), grupos por camada; strokes editáveis; fundo preto num grupo pra apagar.
- Favoritos do 2027 salvos em `costas/ano-favoritos/`: 40 estilos nº25 (à direita) e nº30 (27 grande), e emendado nº25. Nenhum fechado ainda.
- Favorito do dono no ano: emendado nº25. Testando o "40 estilos 25" menor em 30 posições: `costas/ano25-menor/`.

## Mídia kit (PDF)
- Favoritos do ano (dono apagou 40-estilos 25 e 30): `costas/ano-favoritos/` = emendado 25 (**arte principal**) + novos 01, 03, 07, 11, 19, 22, 23, 30.
- `python3 midiakit.py` → `midiakit/terceirao-2027-midia-kit.pdf` (7 págs: capa, principal, variações no preto, preto×negativo,
  negativo principal, variações em negativo, cores e fontes) + `midiakit/png/` (cada variação: fundo-preto, transparente, negativo, negativo-transparente).
- Negativo = pra fundo claro: inverte só os neutros (branco↔preto), roxos ficam; feito sobre o recorte transparente (senão a vinheta vira cinza).
- Correções: apóstrofo do '27 removido (caía no pé do R); negativo agora é desenhado nativo (`favoritos.py`), não invertido pixel a pixel (a inversão sujava o brilho e deixava o contorno fraco).
- Buracos das letras (R, A, O, 0) **brancos** com linha preta fina em volta (dono pediu): `favoritos.py` acha as contraformas pela máscara do recheio e pinta de branco.

## ✅ VERSÃO FINAL (dono: "salve todas essas versões, elas serão as finais")
Tudo em **`final/`**:
- `terceirao-2027-manual-de-marca.pdf` (10 págs: capa, conceito, arte principal, mockup, variações, negativo, cores, tipografia, aplicações, bom uso) — `python3 marca.py`
- `arte-principal/` (transparente + fundo preto), `variacoes-ano/` (8), `negativo/`, `vetor/` (SVG/PDF/EPS das letras)
- `aplicacoes/`: **mockup em FOTO real** (`mockup_foto.py`, foto do dono em `referencias/mockups/`) + story, adesivo, faixa, ingresso (`aplicacoes.py`).
- ❌ Moletom/camiseta desenhados em vetor foram reprovados ("muito ruim"): sempre usar foto real de mockup.
- Mídia kit anterior continua em `midiakit/`.

### Como o mockup em foto é feito (`mockup_foto.py`)
1. Foto do mockup (vinda do dono) em `referencias/mockups/`, ampliada 4× (Lanczos + nitidez).
2. Arte = `midiakit/png/integrado-25-transparente.png`, recortada no conteúdo e com **margem de 6% em volta**
   (sem margem a deformação puxa pixel de fora e **corta o topo do TER** — erro já cometido).
3. Sombreamento: luminância local da foto (borrada) ÷ mediana do tecido multiplica a arte → dobras e luz do pano.
4. Deformação leve pelo gradiente do relevo (`desloc` ≈ 0,6×K; mais que isso entorta o MÃE DE DEUS).
5. Grão de tinta + 96% de opacidade; alpha só onde é tecido (luminância < 150, erodido) → nada vaza pro fundo branco.
6. Costas: centro (468,200)×K, largura ≈143×K. Peito: (213,128)×K, largura ≈38×K. Coordenadas da foto original 661×360.

## ⭐ BRAND BOOK PREMIUM (`final/terceirao-2027-brandbook.pdf`, 26 págs) — `python3 manual_premium.py`
Estrutura de brand book de marca grande: capa, índice, 5 capítulos com divisória roxa + pattern (Essência, Marca, Cor & Tipo,
Linguagem, Aplicações), manifesto ("A gente não pichou a escola. A gente assinou."), construção/área de proteção (x = altura do 27),
versões (principal, negativo, 1 cor branco/roxo), símbolo 27, tamanhos mínimos, paleta com HEX/RGB/CMYK/PMS aprox., proporção 60/25/10/5,
tipografia (Graffiti Youth + Inter + Space Mono), elementos, estampa corrida, 6 usos incorretos, aplicações, contracapa.
- Peças novas: `final/simbolo/` (27 sozinho), `final/versoes-1cor/`, `final/padrao/estampa-corrida-27.png` (`derivados.py`).
- Mockups em foto: moletom (foto do dono) + **camiseta e boné gerados no ElevenLabs** (`gemini-3.1-flash-lite-image`, 206 créditos cada;
  `bytedance-seedream-5-pro` custa 818). Fotos em `referencias/mockups/`, aplicação em `mockups_ia.py`.
- Impressos/digital (`aplicacoes.py`): story, adesivo, faixa, ingresso, posts do feed, credencial, convite.

## ⭐ BRAND BOOK v2 — editorial/conceitual (dono: "muito mais premium, profissional, conceitual, com profundidade")
`python3 brandbook_v2.py` → `final/terceirao-2027-brandbook.pdf` (36 págs). Substitui o v1 (`manual_premium.py` fica como histórico).
- Narrativa em 5 capítulos: **I O Muro** (manifesto, valores Atitude/União/Legado, território) · **II A Tag** (processo 150→30→7→1,
  ajuste fino, assinatura, anatomia com 9 marcações, close, construção, versões, símbolo, mínimos) · **III A Cor** (roxo full-bleed,
  paleta HEX/RGB/CMYK/PMS, equilíbrio 60/25/10/5) · **IV A Voz** (tipografia, tom de voz com frases, pattern, elementos, 6 usos proibidos)
  · **V A Rua** (moletom, camiseta, boné em foto sangrada; impressos; digital; calendário do ano) + contracapa "até o último sinal."
- Linguagem: grão SVG em todas as páginas, Inter Black + Playfair Italic (citações) + Space Mono (rótulos) + Graffiti Youth;
  divisórias com luz roxa + pattern 27 a 7% (NÃO usar foto do boné de fundo: aparecia o boné repetido).
- Anatomia: pinos em coordenadas reais da arte (px da arte 1503×1800), não chutar porcentagem.

## ⭐ Imagens premium / key visuals (dono: "imagens mais profissionais, profundidade, gradiente, premium")
- **3D real** em `render3d/` (three.js 0.170, `cena.html` + `node shot.js "query" out.png W H`, sem servidor: Playwright intercepta
  `http://cena.local/`). Modos: `slab` (adesivo grosso 2.5D da arte/27), `caneca` (`gira=3.1416`), `botton` (`tg=-1.5708`).
  Garrafa ficou distorcida (UV do lathe): não usar.
- `python3 keyvisuals.py` → `final/keyvisuals/`: kv01 herói (2027 atrás da assinatura 3D), kv02 ÚLTIMO ANO + 27 3D com reflexo,
  kv03 caneca, kv04 bottons, kv05 moletom recortado com TURMA 27 atrás, kv06 dois celulares com wallpaper; posts 1080×1350
  (ÚLTIMO ANO., CHEGOU., FALTAM 200) no estilo dos posts da dot: título gigante em degradê atrás do objeto, holofote, névoa,
  partículas, vinheta, grão, frase de 1 linha com virada em roxo.
- Títulos com acento: `padding-top:.14em` no texto com background-clip (senão o acento some).
- Brand book v2 agora com 43 págs (key visuals sangrados no capítulo V).

## Rodada "mais visual, menos texto" (dono)
- **Sem "MÃE DE DEUS" embaixo do TERCEIRÃO** (favoritos.py esconde `.esc`). Reprocessar tudo: favoritos → midiakit → marca → derivados → mockups → render3d → keyvisuals → aplicacoes → brandbook_v2.
- **Pattern 27 removido** ("não faz sentido"): não usar estampa corrida em lugar nenhum.
- **Boné excluído** ("horrível"). Peito do moletom mais à esquerda (cx=197).
- **Caneca branca** = arte NEGATIVO (`cor=%23F2EEF5`), preta = arte principal.
- Brand book: parágrafos escondidos (`.t{display:none}`), só títulos + imagens. 49 págs.
- Novas cenas premium (kv07–kv15): canecas preta+branca, chaveiro acrílico 3D, kit de adesivos 3D com desfoque,
  capa de celular, caderno, pulseiras do baile, letreiro neon 27, telão da formatura com plateia, bandeira da turma.

## ⭐ BRAND BOOK v3 — institucional (`python3 brandbook_v3.py`, 29 págs). v1/v2 ficam como histórico.
Dono reprovou: textos de "muro / a gente não pichou", capa escura, páginas de processo (150 fontes, ajuste fino), til/close,
espaço pra respirar (construção), voz, brilhos/figurinhas, bottons, celular, posts, chaveiro, caderno, bandeira, boné.
Estrutura atual: capa em **degradê roxo com letra branca** (logo 1 cor branco) · sumário · 01 Marca (assinatura, logo 3D, versões,
símbolo, mínimo, não fazer) · 02 Cores (cartões em degradê com sombra + proporção) · 03 Tipografia (Graffiti Youth + Inter) ·
04 Aplicações (moletom cena + foto, camiseta, 4 adesivos colados em superfície real, kit 3D, canecas, pulseiras 3D, impressos, neon, telão) · contracapa.
- **BUG corrigido:** PNG transparente da arte tirava o contorno preto (chroma key no preto). Agora `favoritos.py` renderiza sem fundo.
- **Adesivos colados** (`adesivo_cenas.py`): texturas Poly Haven 2K (`referencias/texturas/`), recorte branco, relevo da superfície,
  sombra, perspectiva; brilhos da arte removidos (`sem_brilhos`). 3D usa `render3d/img/arte-sb.png` (sem brilhos).
- Moletom: costas menor (larg 112×1.12). Camiseta: estampa no peito à esquerda de quem olha.
- **Revisar TODAS as páginas em tamanho grande antes de enviar** (dono cobrou logo cortado na pág. 28 do v2).
- Pendente: 5 mockups de moletom diferentes — precisa de foto (dono manda) ou créditos ElevenLabs.
- Mockups nas fotos do dono: **só o close (dono-2) ficou aprovado**. Remoção de estampa em foto de preview com JPG baixo/estampa grande deu resultado quebrado (True Romance ficou com manchas e logo flutuando: dono reclamou). NÃO entregar sem olhar cada um em tamanho grande. Melhor caminho: PSD/foto lisa.
