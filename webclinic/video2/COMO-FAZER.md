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
