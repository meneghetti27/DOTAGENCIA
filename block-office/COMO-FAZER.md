# Block Hunt — jogo 3D da Block Office

Loja de streetwear/skate na R. Pelotas 349, Floresta, POA. Dono: **Louis** (@mynamelouis).
Rádio Block to Block FM: segundas 20h–00h.

## O jogo
- 3ª pessoa em 3D (three.js 0.160), jogabilidade igual ao jogo do Pepe & Gael (https://claude.ai/artifact/6cfo1HpnCMd5mV1xW4WJ5R):
  joystick no dedo esquerdo, câmera no direito, botão PEGA, brilho perto dos itens, cronômetro, minimapa, telas de início e fim.
- O jogador **é o Louis**. Itens: touca da Block, térmica de lean, baseadão, disco raro "Leviano" no forro.
  Achou os 4 → "ACHOU TUDO · BLOCK TO BLOCK FM LIBERADA". ("Achar o Louis" foi removido a pedido do dono.)
- Código: `jogo/index.html` (formato artifact, sem html/head). Assets em `jogo/assets/`:
  modelos .glb/.bin guardados em base64 (`.txt`) e .gltf como `.gltf.json`, porque o artifact não serve esses tipos;
  o `LoadingManager` decodifica para blob na abertura. Texturas e modelos CC0 da Poly Haven; corpo base Xbot (exemplo three.js).
- Testar: `node teste.js $PWD/jogo` (Playwright + swiftshader, gera prints t0–t10). Hook de debug: `window.__bh`.
- Publicação: slug reservado `da2480dd-578a-494a-9003-f98424660998` (ainda não publicado).

## Status (19/11/2026) — REPROVADO pelo dono
- "isso n tem nada a ver com a block, o personagem louis esta HORRIVEL" (prints em `prints/p3.png`, `p10.png`).
- O preview de estética (`preview-estetica.html`, `prints/preview.png`) tinha sido aprovado ("o grafico ta legal").
- Decisões para a próxima versão:
  1. **Louis estilizado caprichado** (não realista): modelado do zero, proporção de streetwear, cabeça um pouco maior,
     careca ou touca preta, bigode ferradura, óculos espelhado prata envolvente, correntes grossas prata com cruz,
     jaqueta verde-oliva com bordado amarelo, cargo preta, pele clara. Nada de boneco Xbot com roupa pintada/enchimento.
  2. **Usar as fotos reais da loja como textura/referência** de cada canto (`referencias/`, extraídas do PDF; resolução baixa ~480 px).
     O dono vai mandar mais fotos como arquivo.
- Elementos marcantes que têm que aparecer logo de cara: fachada de concreto com vidro espelhado escuro e placa 349, grafite de caveira
  com selo STOP; escada metálica central com corrente no corrimão; DJ booth embaixo da escada (painel grade, 2 Technics, mixer, neon do
  logo cubo hexagonal); parede de tijolo com prateleira de tênis e X neon azul, neon OÜS, arara curva, caixote OÜS; rack de andaime
  enferrujado com bancos de moto; duas Suzukis amarelas na parede; céu de cúpulas prismáticas; luminária de olhos LED de tênis;
  sofá de couro preto sob espelho redondo; jardim interno com trepadeiras, TV com o logo e mesa de vidro sobre raiz.

## Arquivos
- `referencias/Block_Office_referencias_jogo.pdf` e `relatorio_block_office_louis_brum.pdf` (enviados pelo dono)
- `referencias/r-*.jpg` fotos extraídas · `referencias/folha.jpg` folha de contato
- `prints/` capturas dos testes
