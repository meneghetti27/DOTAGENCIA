# Moletom Terceirão (cliente: turma de 3º ano)

- **Cor do moletom**: lilás `#996BB3` (amostra que o dono mandou em `referencias/cor-do-moletom.jpg`). Não mudar.
- **Pedido da turma**: referências são **só pras letras**; **sem animal/personagem**; **grafite, não pixação**.
- Estilo escolhido pra 1ª rodada: grafite "bolha" (throw-up): letras Bagel Fat One sobrepostas e giradas,
  contorno preto, 3D roxo-escuro, linha externa no acento, recheio branco com metade de baixo no acento
  (onda + bolhinhas + brilho), escorridos, til desenhado à mão, brilhos de 4 pontas.
- Testado e descartado: estilo bloco com listras (Bungee/Titan): ficou ilegível ("TED CEI DÃO").
- Peças: costas (TER/CEI/RÃO + ano), peito esquerdo ("3" com capelo), manga (ano na vertical),
  forro do capuz (nomes em letra de tag, Sedgwick Ave Display — hoje com nomes de EXEMPLO).
- Cores de acento: `lima` #C8FF3D, `rosa` #FF4FB0, `branco` (só branco + preto).

## Gerar
```
python3 gerar.py [lima rosa branco]   # artes/<cor>/*.svg + *.png (fundo transparente)
python3 mockup.py [lima rosa branco]  # artes/<cor>/mockup.png (frente + costas)
```
Nomes do forro: lista `NOMES_EXEMPLO` em `gerar.py`. Ano: "2027" em `versao_bolha` e `versao_manga`.
Ajuste de letras: lista `jit` (dx, dy, tamanho, giro por letra) em `versao_bolha`.
