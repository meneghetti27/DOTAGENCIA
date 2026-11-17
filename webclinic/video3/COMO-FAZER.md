# Vídeo 3 da Web Clinic: "Aguarde na linha" (16/11/2026)

Comédia em áudio, ~44 s, 1080×1920, Remotion. A tela é uma chamada de celular (escura, marca Web Clinic): avatar "BE",
"Clínica Bem Estar", status (discando/chamando/em ligação/em espera/chamada encerrada), cronômetro grande, onda da voz
(envelope.json), legenda grande (URA em serifada itálica entre aspas, paciente em Poppins 700 azul). Na espera o cronômetro
acelera de 00:14 até 04:37 com "um/dois/quatro minutos depois…"; a chamada cai (carimbo "4min37s de espera. Pra nada.").
Virada clara: "Seu paciente não tem 4 minutos." + celular com o site marcando em 8 s (cronômetro 00:00→00:08,
"Consulta marcada"). Fim: azul com logo, "Sites que viram consulta marcada.", "Manda SITE no direct".

## Áudio (ElevenLabs, flow https://elevenlabs.io/app/flows/UXg6RJAmUQg8NMiNbcgQ)
- URA: Fernanda – Agente URA IA (`7iqXtOF3wl3pomwXFY7G`), filtro de telefone no ffmpeg (passa-faixa 320–3300 Hz + compressor).
- Paciente: Gabriel – Casual e Amigável (`urYO2UqU0Q6zAxYEYEYV`). Narrador: Moutella (`X3j2R63Qu4Gdv6dsU2hB`).
- Música de espera: ElevenLabs Music v2.5 (bossa de elevador), filtrada como telefone. SFX: discagem, tecla, queda, sucesso.
- Tom de chamando e de ocupado: gerados no ffmpeg (425 Hz, padrão brasileiro).
- `public/trilha.mp3` é a mixagem final (script no histórico: trechos com atrim + adelay + amix, música abaixando quando há fala).
- Tempos por palavra: faster-whisper → `src/falas.json`. Créditos: ~1.700 (falas 670, música 900, sfx ~70).

## Render
`npx remotion render src/index.ts Apresentacao out/bruto.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --crf=16`
e `ffmpeg -i out/bruto.mp4 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out/webclinic-aguarde-na-linha.mp4`.
`node_modules` é link para `../video2/node_modules`.

## v2 (17/11/2026) — a v1 foi reprovada: "amador, escrita por cima, não prende, devagar"
Diagnóstico (quadros a cada 2 s): 28 s com a mesma tela parada; 7 s sem nada no começo (00:00 apagado + toque);
legenda pequena em itálico no meio da interface, encostando na onda e no teclado; interface em tamanho real de celular
(miúda no vídeo); virada com título pequeno e cronômetro encavalado no celular.
O que mudou: gancho "POV: você tenta marcar uma consulta." no quadro 0; trilha recortada de 44 para 33,6 s (URA atende em
1,8 s, sem "Vamos lá", frase longa encurtada); edição em planos de 2–4 s (chamada → close no teclado → chamada com câmera
indo pro cronômetro → cronômetro gigante "EM ESPERA ♪" com selos "+1/+2/+4 min" → tela vermelha "04:37 de espera. Pra nada."
→ azul "Seu paciente não tem 4 minutos." → celular grande com 00:00→00:08 em cima → assinatura); cada plano entra com
"soco" de 1,06→1 e empurra a câmera; legenda Poppins 66–96 px numa faixa fixa (y 1360–1660) onde nada mais aparece.
Regra: nunca deixar a mesma composição mais de ~4 s; legenda nunca por cima de outro elemento.
