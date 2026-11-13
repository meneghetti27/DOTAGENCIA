# Vídeo "sobre nós" da Web Clinic (post fixado)

Reels 1080×1920, 30 fps, ~35 s, **Remotion**. Final: `out/webclinic-apresentacao.mp4` (−14 LUFS, pico −1 dB).
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

## Cenas (cada uma começa 4 quadros antes da palavra-gatilho; legenda entra palavra por palavra)
1 pesquisa no Google digitando · 2 site antigo (cinza, X) × site novo (borda azul, ✓) · 3 navy: logo + batimento
4 azul: 9 ícones de especialidades · 5 "Não é só um site bonito" riscado → cursor clica "Agendar consulta" + chip
6 navy: agenda com horários acendendo até 23h45 · 7 mapa com pin e card do Google · 8 azul: celular, toque no WhatsApp
9 navy: Google → Site → Agenda → Paciente · 10 "Você cuida das pessoas" → 3 "Nova consulta marcada" · 11 azul: logo, DM "SITE", @ e WhatsApp.
Corte = zoom 1,08 → 1 com desfoque; câmera sempre se aproxima 3,5% durante a cena; ícones balançam.
