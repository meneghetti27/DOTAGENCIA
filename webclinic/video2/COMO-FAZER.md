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
