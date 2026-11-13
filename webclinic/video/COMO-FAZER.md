# Vídeo "sobre nós" da Web Clinic (post fixado)

Reels 1080×1920, 30 fps, ~41 s, **Remotion** (v2, depois do pedido "mais profissional, gradiente, sombras, profundidade e gancho como os vídeos da dot"). Final: `out/webclinic-apresentacao.mp4` (−14 LUFS, pico −1 dB).
Pedido do dono: "sobre nós e o que fazemos", **voz masculina com autoridade**, **sem música, só efeitos sonoros**, ElevenLabs **v4**.

- Narração: ElevenLabs `eleven_v4`, voz **Moutella** (`X3j2R63Qu4Gdv6dsU2hB`), um take só, texto com tags em `roteiro.txt`.
  `python3 voz.py` usa `sva/tools/video/falas.py` (chave no `.env` do repo sva) e grava `src/audio.json` (tempo por palavra);
  depois `ffmpeg -i public/voz-bruta.mp3 -af loudnorm=I=-16:TP=-1.5 public/voz.mp3`.
- Vetores e logo vêm do gerador Python: `python3 exportar.py` → `src/vetores.json`.
- Fonte Poppins local em `public/fonts/` (o Chrome do render não aceita o certificado do proxy para baixar do Google Fonts).
- Efeitos: `public/*.mp3` (whoosh em cada corte, pop, tique, ding, impacto).
- Render: `npm install` e
  `npx remotion render src/index.ts Apresentacao out/bruto.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --crf=16`
  e `ffmpeg -i out/bruto.mp4 -c:v copy -af loudnorm=I=-14:TP=-1 -c:a aac -b:a 192k out/webclinic-apresentacao.mp4`.

## v2: o que mudou e por quê
- **Gancho** nos primeiros 10 s, escuro e cinematográfico: "Neste exato momento... um paciente está digitando a sua especialidade no Google.
  E ele vai marcar... com quem aparecer primeiro. Se não for você... é o seu concorrente." (celular em 3D digitando, "1º" gigante, cartão "VOCÊ" afundando cinza e "SEU CONCORRENTE" vindo pra frente).
- **Voz com emoção por frase** (tags v4 em `roteiro.txt`: mysterious/slowly, softly, serious, dramatic, intense, determined, proud, dismissive, emphatic, energetic, playful, warm, reassuring).
- **Profundidade**: fundos em degradê (escuro navy com brilho azul, claro gelo → azul, azul vivo), perspectiva 3D em celular/sites/agenda,
  blocos de ícone com brilho interno e sombra forte, desfoque de profundidade (ícones na frente desfocados), faixa de luz passando nos cartões,
  vidro (backdrop blur) na agenda e no campo do direct, grão e vinheta. Aqui **sombras são liberadas** (nos posts não).
- **Transição**: a cena sai "atravessando a câmera" (escala 1 → 1,45 + desfoque) e a próxima entra de trás (0,9 → 1).
- Legenda palavra por palavra no tempo exato da voz, com borrão de movimento; ênfase em degradê.
