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
