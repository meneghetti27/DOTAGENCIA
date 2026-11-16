# Vídeo 2 da Web Clinic: "A recepção que não dá conta" (em produção)

- Ideia escolhida pelo dono (16/11/2026): nº 3, "a secretária que não dorme" (recepção soterrada de ligações → o site atende sozinho).
- Estilo escolhido: **E, colagem editorial** ("MT PROFISSIONAL"): foto real recortada em P&B sobre azul `#2D7FF0` chapado,
  papel rasgado gelo `#EEF5FC`, fita adesiva azul clara, número gigante vazado (contorno branco), etiquetas brancas arredondadas
  com texto navy, grão. Fonte Poppins (300 navy/branco + 700). Quadro de referência: `estilo-E-escolhido.png`;
  comparação com os outros estilos: `estilos-video2.jpg`.
- Mesma base técnica do vídeo 1 (`webclinic/video` na main): Remotion 1080×1920, voz Moutella (ElevenLabs v4), só efeitos sonoros.

## Narração (gravada 16/11/2026, 1 take, 968 créditos)
- Conector ElevenLabs do claude.ai (`creative_generate_speech`, `eleven_v4`, voz Moutella `X3j2R63Qu4Gdv6dsU2hB`, `generations_count: 1`
  pra não gastar crédito). Flow: https://elevenlabs.io/app/flows/Mw6ujXwnMhfWq9eV3F08
- Texto com tags em `roteiro.txt`. Arquivo: `public/voz-bruta.mp3` (41,3 s) → `public/voz.mp3` (loudnorm −16 LUFS).

## Roteiro aprovado: "A Cláudia não dá conta" (~41 s)
Cláudia (recepcionista) atende telefone, WhatsApp, porta e Instagram → perguntas repetidas ("Qual o valor?") → 47 vezes por dia →
três pacientes desistem e marcam no concorrente → às 18h ela vai pra casa ("merecido") → 22:47 paciente quer marcar, sem resposta →
a Web Clinic: site responde, mostra horários e marca sozinho (carimbo CONSULTA MARCADA) → "A Cláudia cuida de quem chega. O site cuida
de quem procura." → logo + "Manda SITE no direct".

## Imagens
- Cláudia gerada por IA pelo conector ElevenLabs (`gemini-3.1-flash-image`, ~400 créditos; edições a partir da base ~610 cada,
  `creative_edit_image` com a base ligada, o que mantém o mesmo rosto). Flow: https://elevenlabs.io/app/flows/S601X7QFMpraqhoVjO4z
  Poses: `claudia-base` (sorrindo, headset), `claudia-estresse` (mãos na cabeça), `claudia-tchau` (sobretudo, bolsa, acenando),
  `claudia-cafe` (caneca, tranquila). `paciente0..2` vêm de uma imagem só com 3 pessoas. Todas recortadas com rembg (isnet),
  alfa < 40 zerado, recorte no bbox e ampliadas 2x (LANCZOS + unsharp).
- Telefone de mesa: pngwing (recortado). Relógio, celular e site: desenhados no código.
- Total gasto no ElevenLabs: voz 968 + imagens ~2.640 créditos.

## Código e render
- `src/Video.tsx`: componentes `Recorte` (P&B + borda de papel branco por drop-shadow), `Etiqueta` (pílula com mola), `Fita`,
  `Rasgo` (papel rasgado com borda aleatória fixa por seed), `Vazado` (número de contorno), `Legenda` (tira branca, palavra ativa em azul).
  Cada cena entra subindo por baixo (corte "rasgando"), whoosh em cada corte, pop nas etiquetas, impacto no "QUAL O VALOR?", no 47 e no carimbo.
- Tempo por palavra: faster-whisper `small` (pt) com o áudio passado como array (o PyAV instalado não aceita o arquivo direto) → `src/audio.json`
  (números corrigidos à mão: "um", "três", "seis", "dez", "mostra", "pra").
- Render: `npm install` e
  `npx remotion render src/index.ts Apresentacao out/bruto.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --crf=16`
  e `ffmpeg -i out/bruto.mp4 -c:v copy -af loudnorm=I=-14:TP=-1 -c:a aac -b:a 192k out/webclinic-claudia.mp4`.

## v2 EDITORIAL (16/11/2026) — a v1 foi reprovada: "amador, não profissional, efeitos sonoros horríveis"
O que estava errado na v1 (não repetir): emojis nas etiquetas, etiqueta demais por cena, legenda em caixa branca o tempo todo,
movimento de "mola" genérico, layout centralizado repetido, rasgo desenhado em CSS, sons de banco (pop/whoosh).
Direção aprovada (quadros-chave em `../../webclinic-ref` / `video2-quadros-editorial.jpg`): **revista impressa**.
- Cabeçalho de edição em toda página: logo + fio fino + "Nº 02 · seção". Títulos gigantes Poppins 700/300 + Instrument Serif itálico
  (fonte do site) nas palavras de destaque. Legendas de foto "Fig. 01" — **texto pequeno nunca abaixo de ~36–40 px, rótulos 25–27 px**
  (o dono reclamou: "legenda imoral de pequena e ilegível").
- Texturas reais geradas por `tools/papel.py`: papel com fibras (gelo, azul, navy, branco), rasgo com borda fibrosa, fotos com
  retícula sutil e borda de papel cortado (`*-imp.png`). Fita adesiva, recados de papel, carimbo com tinta falhada (máscara de papel).
- Sem emoji; no máximo 2–3 elementos por quadro; fotos saindo pela borda e na frente dos títulos.
- Movimento em stop-motion: tempo quantizado de 2 em 2 quadros (12 qps) + leve tremida de papel por degrau; cada cena é uma folha
  que entra deslizando por cima da anterior.
- Texto da narração aparece como título da página (palavra por palavra), sem legenda corrida.
- Sons gerados no ElevenLabs (Sound Effects v2, ~17 créditos cada) em `public/sfx/`: pagina, desliza, fita, papelzinho, carimbo,
  relogio, telefone (cortado em 2,6 s), notificacao, rasgo. Silêncio inicial cortado e loudnorm −18.

## Legenda (16/11/2026): reprovada 6 vezes, o dono vai fazer em outro lugar
Erros que ele apontou: (1) sem emoji; (2) emoji demais ("árvore de natal"); (3) só transcrever o roteiro do vídeo;
(4) longa demais; (5) curta demais e sem graça. Próxima vez: perguntar antes o tamanho e mostrar 2–3 opções curtas
de tom diferente, com 2–4 emojis, sem repetir o roteiro.
