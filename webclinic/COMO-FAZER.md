# Web Clinic — como fazer os posts

Web Clinic é o Instagram do Antônio de **sites que convertem para médicos e profissionais da saúde**.
Mesmo método de design da dot., mas com **marca própria** (branco + azul de máscara + navy).
Guia para o dono alimentar os posts: `guia/webclinic-guia-de-posts.pdf` (ficha, formatos, ícones, regras).

## Pastas
- `marca/` — logo final (`logo-final/webclinic-perfil-4.png/.svg`) e manual de marca (PDF).
- `posts/` — os 40 posts aprovados (v2, 2160×2700) + PDF.
- `gerador/` — tudo que gera os posts e o guia (Python escreve HTML, Playwright tira o PNG).
- `guia/` — PDF "Como criar os posts".
- `historico/` — rodadas anteriores (logos testados, testes de Q/K, posts v1–v4, opções de elementos).

## Marca (travada)
- Escrita **webclinic** (com C). Logo de perfil = opção 4: círculo branco, "web" navy `#0B1F3A` + "clinic" azul `#2D7FF0`, Poppins 700, linha de batimento azul embaixo.
- Cores: azul `#2D7FF0`, navy `#0B1F3A`, azul claro `#5AA2FF`, máscara `#CFE6F7`, gelo `#EEF5FC`, alerta `#FA5F6D`.
- Fonte: só **Poppins** (título linha 1 light 300 navy, linha 2 bold 700 azul).

## Regras aprovadas pelo dono
- Muito espaço em branco, ~25 palavras por post, frase de baixo em 2 linhas (2ª em azul) + rodapé em caixa alta.
- Profundidade com perspectiva leve (cards inclinados, chips flutuando). **Só sombra azul bem fraca**, nada de brilho forte.
- Elementos = **vetores 2D próprios** (opção C, `V` em `gerador/elem.py` + extras no topo de `posts40.py`).
  Reprovados: 3D do Poly Haven ("não tá legal"), 3dicons (só 400 px), 3D procedural, celular em todo post.
- Fotos: reais e bonitas do **Pexels** (`https://images.pexels.com/photos/ID/pexels-photo-ID.jpeg?w=2000`).
  Busca do Bing dá foto de banco datada; Unsplash/Google/DDG bloqueiam robô. Projeto fictício: sem crédito.
- Não inventar estatística. Linguagem simples (nada de "anamnese", "leads").
- Entregar em **PDF** e mandar rápido uma primeira versão; depois revisar com calma se ele pedir.

## Como gerar
```bash
cd webclinic/gerador
python3 posts40.py                       # escreve p40-01..40.html
mkdir -p out && node shotm.js "$PWD" p40- 2 "$PWD/out"   # PNG 2x
python3 guia.py && for f in guia-*.html; do node shot.js "$PWD/$f" "$PWD/out/${f%.html}.png" 2; done
```
- `posts40.py` reaproveita helpers de `posts5.py` → `posts3.py` → `brand.py` (logo, cores) e `elem.py` (vetores).
- Funções: `title()` (tamanho automático), `chip()`, `bigicon()`, `floaticon()`, `photo()`, `card()`, `lst()`, `site()`/`sitebox()`,
  `vs()` (comparação), `steps()`, `ph()` (frase + rodapé). `add(..., DARK, fit=False)` = post navy.
- `add()` envolve o visual num **palco que se ajusta sozinho** (script FIT) entre o título e a frase: não precisa acertar o `top` na mão.
- Novo post: copiar uma linha `add(...)` do mesmo formato e trocar textos. Formatos/códigos estão no guia (FOTO, ICONE, ICONE-CARD,
  SITE, BUSCA, MENSAGEM, LISTA, COMPARA, PASSOS, NAVY, CTA, LIVRE).

## Checklist antes de mandar
Título sem quebrar em 3 linhas · nada encostando no título/frase · chips sem cobrir texto importante · textos dos cards legíveis
no celular · variar formato entre posts vizinhos · conferir folha de contato de todos os posts.

## Postagem (Meta Business Suite, só Instagram)
- `posts/webclinic-40-posts-como-postar.pdf`: instruções para quem posta (outro Claude no Business Suite), cronograma
  4 posts por dia (9h, 12h, 15h, 19h) de 13 a 22/11/2026 e uma página por post (data, arquivo/link raw do PNG, texto alternativo, legenda, hashtags).
- `posts/legendas.txt`: as mesmas legendas em texto puro.
- Gerar de novo: `cd gerador && python3 postar.py && node pdf.js "$PWD/postar.html" "$PWD/../posts/webclinic-40-posts-como-postar.pdf"`
  (`page.pdf` do Chromium = texto copiável). Legendas, hashtags e datas ficam no topo de `postar.py`.
- Regra do dono: **só Instagram** (Facebook desmarcado), feed, 1 imagem 4:5. Arte e números são exemplos ilustrativos.

## Perfil do Instagram (foto, bio, destaques)
- `perfil/webclinic-configurar-perfil.pdf`: instruções para quem configura o perfil (outro Claude / Business Suite): ordem das tarefas,
  foto, nome/bio/categoria/link para copiar, prévia, 5 destaques (Sobre, Sites, Agenda, Dicas, Contato) e quais stories vão em cada um.
- `perfil/foto-perfil.png` (1080×1080) e `perfil/destaques/` (capas `capa-*.png` + stories `story-*.png`, 1080×1920).
- Stories dos destaques (v2, aprovados como direção: "mais visual"): `gerador/stories.py`, desenhados direto em 9:16, pouco texto,
  vetores grandes, mockups de site/celular/agenda, fundos alternando gelo, navy e azul, indicador de página no topo.
  Área segura: nada importante acima de y=220 nem abaixo de y=1680 (interface do Instagram).
- JPEG por destaque em `perfil/destaques-jpeg/1-sobre … 5-contato/` (0-capa.jpg + story-N.jpg) e zip `perfil/webclinic-destaques-jpeg.zip`.
- Gerar de novo: `cd gerador && python3 stories.py && node shots.js out-st && for f in out-st/*.png; do cp $f ../perfil/destaques/story-$(basename $f); done`
  e depois `python3 perfil.py && node shotp.js && node pdf.js "$PWD/perfil.html" "$PWD/../perfil/webclinic-configurar-perfil.pdf"`
- Pendências do dono: @ definitivo (artes usam @webclinic) e link da bio / botão de contato (WhatsApp ou site).
