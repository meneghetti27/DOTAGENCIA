# dot. — Agência de Marketing

Este repositório é a memória da **dot.** Leia este arquivo inteiro antes de criar qualquer design, post ou página.
Toda vez que o dono corrigir algo ("não é assim", "sempre faça X"), **atualize este arquivo** e faça commit.

## A agência

- Nome: **dot.** (sempre minúsculo, com o ponto azul no final)
- Instagram: **@marketingdotagency**
- O que vende: **Sites e Google Ads** para empresas que querem ser **encontradas**.
- Conceito da marca: "dot" = ponto. Frase-chave: **"Todo grande resultado começa em um ponto."**
  Use esse trocadilho do ponto (bolinha azul, ponto final em destaque) sempre que fizer sentido.

## Site oficial

- Publicado em: https://claude.ai/artifact/LrAMsj9fehJMrUnzLa7bzm. A cópia do código está em `site/index.html`.
  Para editar o site, atualize o artifact nesse mesmo link (não crie outro).
- Título: **"dot. Marketing de Alta Conversão"**. Subtítulo: "Sites + Google Ads que transformam busca em cliente".
- Seções: 001 A dot (manifesto "Feito pra quem quer vender.") · 002 Serviços · 003 Método · 004 Resultado · 005 Contato.
- **Serviços**: 01 Sites · 02 Landing pages · 03 Google Ads · 04 Perfil no Google (Perfil da Empresa / Maps).
- **Método dot**: 01 Diagnóstico → 02 Execução → 03 Otimização (relatório todo mês).
- Manifesto: "A gente não faz um pouco de tudo. A gente faz o que traz cliente."
- **Dados que a dot usa** (sempre com a fonte):
  - 53% desistem se o site demora mais de 3 s no celular (Google)
  - 0,05 s para formar a primeira impressão de um site (Lindgaard et al., 2006)
  - 27,6% dos cliques vão para o 1º resultado orgânico (Backlinko)
  - US$ 8 de lucro médio para cada US$ 1 em Google Ads (Google Economic Impact, EUA)
  - +300% de contatos com site novo + Google Ads (resultado de cliente)
- **WhatsApp / contato**: (51) 98906-1441
- Identidade no site: fundo `#05060D`, azul `#2B6BFF`, azul claro `#8FB0FF`, gelo `#DCE6FF`, cinza `#A4AAC0`.
  Fontes: **Inter Tight 900** (títulos gigantes em maiúsculas, bem apertados), **Sriracha** (uma palavra "pincelada" por título, inclinada -3°),
  **JetBrains Mono** (rótulos numerados tipo `001`, botões). Esfera azul 3D, bordas em gradiente azul, botão flutuante do WhatsApp.

## Nível de qualidade desejado (padrão "foda") — LEIA ANTES DE CRIAR

O dono quer posts **mais modernos e profissionais**, com **imagens 3D/fotorrealistas, iluminação cinematográfica e qualidade insana**.
Inspirações (de outras agências, só como referência de nível, **nunca copiar**): `referencias/inspiracao/`.

O que faz esses posts parecerem profissionais:
1. **Uma imagem-herói forte é o post.** Um objeto ou personagem fotorrealista/3D que é uma **metáfora visual** da mensagem
   (bomba feita de dinheiro = lead que vai explodir; dardo no alvo = direção certa; marionetista = manipulação).
   Cards, mockups e gráficos viram secundários ou saem.
2. **Iluminação cinematográfica**: fundo escuro (low-key), luz de recorte (rim light) no objeto, holofote vindo de cima,
   brilho/névoa volumétrica, partículas, profundidade de campo. Na dot, **toda a luz é azul** (`#3D6EF5` / `#87A9FF`).
3. **Camadas texto × imagem**: o título gigante fica **atrás** do objeto/pessoa (a cabeça ou o objeto cobre parte das letras)
   ou o objeto sai por cima do título. Isso dá profundidade 3D.
4. **Tipografia enorme e ultra-condensada** ocupando a largura toda, em branco com gradiente leve para cinza/azul.
   Uma palavra de destaque na cor da marca. Às vezes letras vazadas (contorno).
5. **Pouquíssimo texto** na capa: frase curta acima + título gigante + no máximo 1 linha pequena ou etiqueta inclinada.
6. **Acabamento**: textura/grão sutil, vinheta, gradiente de cor nas bordas, detalhes de "interface de design"
   (caixa de seleção com cantos), contador de carrossel.

### Fluxo de produção (Claude não gera fotos/3D sozinho)
1. Claude cria o conceito e escreve o **prompt da imagem** (em inglês) para o dono gerar numa IA de imagem
   (Midjourney, ChatGPT/DALL·E, Gemini, Freepik, Leonardo…), sempre com a luz azul da dot e fundo escuro, em 4:5.
2. O dono manda a imagem gerada.
3. Claude recorta o objeto (remoção de fundo com `rembg`) para colocar o título **entre o fundo e o objeto**,
   monta o layout em HTML/CSS e exporta PNG 1080×1350 com o Playwright.

## Estilo visual dos posts (obrigatório)

Referências em `referencias/` (10 posts). **Olhe as imagens antes de criar qualquer post.**
Todo post tem que parecer da mesma família: se colocar lado a lado com as referências, ninguém pode notar diferença.

### Formato e grid
- **1080 × 1350 px (4:5)**, retrato. Margem lateral de ~90 px (cards podem ir até ~130 px da borda).
- Tudo respira: muito espaço escuro entre os blocos. Nunca encher a tela.
- Ritmo vertical do layout central (o mais usado):
  | Faixa (y) | Conteúdo |
  |---|---|
  | ~85 px | Cabeçalho `dot. │ @MARKETINGDOTAGENCY`, centralizado |
  | 130–210 | Frase de abertura em serifada itálica |
  | 210–460 | **PALAVRA-HERÓI** gigante |
  | 500–980 | Visual central (card, gráfico, objeto 3D) |
  | 1000–1260 | Fechamento: frase pequena ou rótulo + título de 2 linhas + texto de apoio |
  | ~1250 | Nota de rodapé pequena (fonte / "Valores ilustrativos.") |

### Dois layouts
1. **Central (padrão, 7 de 10 posts)**: tudo centralizado; cabeçalho `dot. │ @MARKETINGDOTAGENCY` no topo
   (logo branco, barra vertical fina cinza, @ em cinza claro).
   Refs: 01, 03, 06, 07, 08, 09, 10.
2. **À esquerda (apresentação, listas e mockups)**: logo `dot.` grande no canto superior esquerdo, @ ou tema
   ("GOOGLE ADS") no canto superior direito, títulos alinhados à esquerda. Refs: 02, 04, 05.

### Cores
| Uso | Cor |
|---|---|
| Fundo | `#05060A` quase preto azulado, com **brilho radial azul-marinho** (`#0B1A4A` → `#12275E`) atrás do visual central |
| Gradiente da palavra-herói (cima → baixo) | `#E4ECFF` → `#B6CBFF` → `#5F8FFE` |
| Gradiente do título azul de fechamento | `#87A9FF` (topo) → `#3D6EF5` → `#2F5BEA` (base) |
| Azul da marca / bordas ativas / glow | `#3D6EF5` (faixa `#2F5BEA`–`#5082FB`) |
| Serifada itálica e rótulos espaçados | azul claro `#9DB5FF` (rótulos às vezes `#7B97D6`) |
| Fundo de card | gradiente `#0E142A` → `#0B1023` |
| Texto principal | `#FFFFFF` · secundário `#B8BFCC` · nota de rodapé `#7A8194` |
| Negativo / "erro" (queda, risco, tachado) | vermelho-coral `#FA5F6D`, com glow; rótulo `#FF8D96` |
| Estrelas de avaliação | dourado `#FFCA50` (vazias em cinza-azulado) |
| Palavra "errada" (ex.: MITO) | cinza claro chapado `#EBEBEB`, **sem gradiente** |

- **Sempre fundo escuro.** Nunca fundo branco ou claro.
- O azul é a única cor de destaque. Vermelho e dourado só com significado (erro e estrelas).

### Tipografia
| Papel | Fonte | Como usar |
|---|---|---|
| Palavra-herói / títulos | **Anton** (condensada, extra pesada) | MAIÚSCULAS, entrelinha ~0,9, tracking 0; a palavra-herói ocupa quase toda a largura (até ~830 px) |
| Frase de abertura | **Playfair Display Italic** | minúsculas, ~64–72 px, azul claro; é o começo da frase que a palavra-herói termina |
| Textos de apoio | **Inter** Regular | 28–34 px, branco/cinza; **o final da frase em Inter Bold branco** |
| Rótulos | **Inter SemiBold** | MAIÚSCULAS, ~26 px, letter-spacing ~0,3 em, azul claro ("VERDADE", "ORÇAMENTO DIÁRIO") |
| @MARKETINGDOTAGENCY | Inter Medium | maiúsculas, ~20 px, letter-spacing ~0,35 em, cinza claro |
| Nomes em cards | Inter Bold ou **Plus Jakarta Sans** ExtraBold | ~34 px |
| Números | **Anton** | sempre com gradiente branco → azul, mesmo dentro de cards |

### A fórmula do texto (estrutura que se repete)
1. **Abertura em serifada itálica** (curiosidade, minúscula, sem ponto):
   *"o primeiro do Google"*, *"o cliente escolhe pelas"*, *"quanto custa anunciar no Google?"*,
   *"leva 20 anos para construir uma"*, *"o custo de não aparecer"*.
2. **PALAVRA-HERÓI** gigante com gradiente, que completa a frase: `#1`, `ESTRELAS`, `VOCÊ DECIDE.`, `REPUTAÇÃO`, `300`, `MITO`.
3. **Visual que prova a ideia** (ver abaixo).
4. **Fechamento em 2 linhas Anton**: **linha 1 branca** (preparação) + **linha 2 azul com gradiente** (a virada), **terminando com ponto ou "?"**.
   Ex.: "PEÇA AVALIAÇÃO PRA / **TODO CLIENTE FELIZ.**", "COMECE PEQUENO. / **ESCALE O QUE FUNCIONA.**",
   "QUANTAS ESTÃO INDO / **PRO SEU CONCORRENTE?**", "E 5 MINUTOS / **PARA ARRUINAR.**".
   Às vezes vem antes uma linha pequena em Inter ("Você escolheria qual?", "leva em média") ou um rótulo espaçado ("VERDADE").
5. **Texto de apoio** (opcional, 1–2 linhas): começa normal e **termina em negrito**.
   Ex.: "Caro é anúncio mal configurado. **Bem feito, ele se paga.**", "Site fora do ar, anúncio enganoso, avaliação sem resposta. **Cuide de cada detalhe.**"
6. **Rodapé honesto**: "Fonte: …", "Valores ilustrativos.", "Exemplo ilustrativo." ou "— Autor" em citações.

### Visual central (escolha 1 por post)
- **Card de vidro**: cantos ~28 px, fundo `#0E142A`→`#0B1023`, borda 2 px `#3D6EF5` com **glow azul externo** quando é o card "bom/ativo".
- **Comparação A × B** (ref 06): card ruim em cima, apagado (texto cinza, borda quase invisível, 2 estrelas) e card bom embaixo, mais largo, aceso (borda azul + glow, 5 estrelas, nota grande em Anton).
- **Interface simulada** (ref 07): rótulo espaçado, valor grande em Anton (`R$ 50` + `/dia` cinza menor), slider azul com bolinha branca brilhante, pílulas com contorno ("Pausa quando quiser", "Sem fidelidade").
- **Gráfico** (ref 08): linha azul clara com glow e área azul embaixo, linhas de grade sutis, ponto branco no pico, queda em vermelho com ponto vermelho; rótulos em Inter Bold maiúsculo (azul claro / vermelho).
- **Conta / fórmula** (ref 09): `10 × 30 = 300` dentro de um card, números em Anton com gradiente, operadores azuis, legenda pequena embaixo de cada número.
- **Objetos 3D azuis** (refs 01, 02, 05, 09, 10): esfera, cubos arredondados, rosquinha (torus), troféu. Material de plástico/vidro azul brilhante, luz suave, alguns desfocados (profundidade). Podem sair pela borda ou ficar atrás dos números.
- **Mockups** (refs 03, 04): janela de navegador com `suaempresa.com.br`, barra de pesquisa do Google, anúncio "Patrocinado", botão "Falar no WhatsApp".
- **Lista em cards** (ref 05): `01 02 03` em Anton azul + frase em Inter; etiqueta azul inclinada (~-3°).
- **Tachado** (ref 10): palavra cinza com uma linha vermelha grossa, arredondada, com glow, cruzando na diagonal.
- **Holofote** (ref 01): cone de luz atrás do objeto principal.

### Detalhes que fazem diferença
- O título gigante pode **sobrepor** o objeto 3D ou o card (camadas = profundidade).
- **Glow azul** atrás de títulos azuis e de cards ativos. Nunca sombra preta dura.
- Pontos finais em títulos são intencionais e lembram o "dot." (ponto).
- Acentos e cedilhas em Anton precisam caber: deixe espaço acima da palavra-herói.
- No máximo **~25 palavras** no post inteiro (fora a nota de rodapé).

## Temas e formatos de conteúdo
- **Estatística** com fonte (01, 09) · **Comparação** (06) · **Mito × Verdade** (10) · **Citação famosa adaptada ao negócio** (08)
- **Simulação de ferramenta** (07) · **Pergunta provocativa** (03, 04) · **Lista de sinais/erros** (05) · **Apresentação da marca** (02)
- Assuntos: Google Ads (custo, orçamento, aparecer no topo), sites que convertem, avaliações e Perfil no Google, reputação, concorrência, WhatsApp.

## Tom dos textos

- Português do Brasil, **direto, curto e provocativo**. Fala com o dono de empresa ("você", "sua empresa").
- Usa **perguntas que incomodam**: "Seu site é bonito. MAS ELE VENDE?", "Seu cliente está procurando. VOCÊ APARECE?"
- Contraste/problema → solução da dot. Ex.: "Site bonito que não gera contato é **cartão de visita caro**. A gente cria site pra converter."
- Linguagem próxima: "a gente", "pra", sem formalidade.
- Temas: aparecer no Google, Google Ads, sites que convertem, WhatsApp, concorrência, ser encontrado.
- Dados sempre com fonte citada.

## Como produzir os designs

- Gerar em HTML/CSS (1080×1350) e exportar PNG com o Playwright (Chromium já instalado).
  Fontes via Google Fonts: Anton, Inter, Playfair Display.
- Salvar os trabalhos prontos em `designs/` (ex.: `designs/2026-10-nome-do-post.png`) e o HTML-fonte junto.
- Antes de entregar, comparar lado a lado com `referencias/`: se não parecer da mesma família, refazer.

## Referências

| Arquivo | O que mostra |
|---|---|
| `referencias/01-primeiro-do-google.jpg` | Estatística com #1 gigante, troféu, holofote, frase serifada itálica |
| `referencias/02-todo-grande-resultado.jpg` | Post de apresentação, esfera 3D, trocadilho do ponto, CTA de carrossel |
| `referencias/03-mas-ele-vende.jpg` | Pergunta provocativa, mockup de navegador com botão WhatsApp |
| `referencias/04-voce-aparece.jpg` | Google Ads, barra de pesquisa e anúncio patrocinado |
| `referencias/05-3-sinais.jpg` | Lista numerada em cards, etiqueta azul inclinada |
| `referencias/06-estrelas.jpg` | Comparação Empresa A × B com estrelas (avaliações) |
| `referencias/07-voce-decide.jpg` | Simulador de orçamento diário com slider e pílulas |
| `referencias/08-reputacao.jpg` | Citação (Warren Buffett) com gráfico de subida e queda em vermelho |
| `referencias/09-custo-de-nao-aparecer.jpg` | Número gigante com cubos 3D e conta 10 × 30 = 300 |
| `referencias/10-mito-google-ads-caro.jpg` | Mito × Verdade, MITO tachado em vermelho, rosquinha 3D |

### Inspirações externas (`referencias/inspiracao/`)
| Arquivo | O que aproveitar |
|---|---|
| `alaska-3-motivos.jpg` | Título ultra-condensado enorme, objeto fotorrealista (bomba de dinheiro) sobrepondo o título, etiqueta inclinada |
| `alaska-ia-no-feed.jpg` | Título gigante atrás do personagem, letras vazadas, "?" na cor de destaque, caixa de seleção com cantos |
| `seta-direcao-certa.jpg` | Layout à esquerda, objeto 3D com luz na cor da marca, gráfico brilhando no fundo, CTA de arrastar |
| `next-mentira.jpg` | Pessoa na frente da palavra gigante "MENTIRA.", holofote azul, metáfora visual (marionetes) |
| `setup-aventura.jpg` | Personagem 3D hiper-detalhado, luz cinematográfica, partículas, textura no título |
