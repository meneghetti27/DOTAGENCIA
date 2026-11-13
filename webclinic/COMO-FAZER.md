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
- Dados confirmados (13/11/2026): Instagram **@webclinicbrasil** (é o @ do cabeçalho de todas as artes, em `posts3.py`) e WhatsApp **(51) 98906-1441** (link da bio `https://wa.me/5551989061441` e botão de contato).

## Site (webclinic/site) — v2
- Direção v2 (ele achou a v1 "com cara de template de IA"): editorial, tipografia gigante Poppins + **Instrument Serif itálico** só nas palavras de destaque, fotos reais (Pexels), sem degradê no texto, sem grade de cards com ícone, sem rótulos "001".
- Movimento: abertura com linha de batimento, rolagem suave (Lenis), GSAP ScrollTrigger: site do topo cresce até tela cheia, jornada presa (pesquisa → site → agenda → WhatsApp → consulta marcada), projetos na horizontal, cursor e botões magnéticos.
- v3 (ele pediu "faz as coisas fazerem sentido, é um site pra vender site"): antes e depois arrastável (site comum x Web Clinic), serviços com a tela de cada um num painel fixo, projetos clicáveis (abre o exemplo no computador e no celular + "Quero um site assim" no WhatsApp), formulário de análise gratuita que monta a mensagem do WhatsApp, notificação "Nova consulta" girando no título.
- Tudo local (sem CDN): `js/` (gsap 3.12.5, ScrollTrigger, lenis 1.1.13), `fonts/`, `img/` (fotos + vídeo "sobre nós").
- Fonte: `gerador/site-v2-modelo.html` + `gerador/site2.py` (sites de exemplo por especialidade, serviços, FAQ, WhatsApp). Gerar: `cd gerador && python3 site2.py`.
- Testar local: `cd site && python3 -m http.server` (por file:// as fontes não carregam).
- `og.png` = print do topo em 1200x630.
- Vercel: importar o repositório com **Root Directory = `webclinic/site`** (sem build). Depois do domínio, trocar `og:image` para URL absoluta.
- v1 guardada em `historico/site-v1` (gerador `site-v1.py`).
