#!/bin/bash
# Monta o vídeo final (rodar dentro de video/src depois de gravar.js, render.js e trilha.py)
G=rec/gameplay.webm
S="scale=1080:1920:flags=neighbor,setsar=1,fps=30,format=yuv420p"
ffmpeg -v error -y -framerate 30 -i fr/intro/%04d.png -framerate 30 -i fr/cta/%04d.png -i $G -i fr/c1.png -i fr/c2.png -i fr/c3.png -i fr/c4.png -i scan.png -i trilha.wav -filter_complex "
[0]format=rgba,$S[in];
[2]split=5[g1][g2][g3][g4][g5];
[g1]trim=3:7,setpts=PTS-STARTPTS[a1];[a1][3]overlay=enable='lt(t,2.2)'[A];
[g2]trim=10:12.5,setpts=PTS-STARTPTS[a2];[a2][4]overlay=enable='lt(t,2)'[B];
[g3]trim=19:21,setpts=PTS-STARTPTS[C0];[C0][5]overlay[C];
[g4]trim=24.4:27.4,setpts=(PTS-STARTPTS)/2[D];
[g5]trim=31.6:35.2,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.4[E0];[E0][6]overlay=enable='gte(t,0.5)'[E];
[A]$S[A1];[B]$S[B1];[C]$S[C1];[D]$S[D1];[E]$S[E1];
[1]format=rgba,$S[ct];
[in][A1][B1][C1][D1][E1][ct]concat=n=7:v=1:a=0[v];
[v][7]overlay,eq=brightness='0.02*sin(t*47)':eval=frame,format=yuv420p[vo]" -map "[vo]" -map 8:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart ../hard-x-block-promo.mp4
ffmpeg -v error -y -ss 21.8 -i ../hard-x-block-promo.mp4 -frames:v 1 ../hard-x-block-poster.png
