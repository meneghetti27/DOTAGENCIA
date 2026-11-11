#!/usr/bin/env python3
"""Montagem dinâmica da apresentação da GCM (vertical 1080x1920, sem texto).
Uso: python3 montar.py <pasta_dos_takes> <saida.mp4>"""
import sys, os, glob, subprocess, numpy as np, wave, tempfile
SRC, OUT = sys.argv[1], sys.argv[2]
def take(code): return glob.glob(os.path.join(SRC, f"*{code}*.mp4"))[0]
TMP = tempfile.mkdtemp()
FPS = 30
# (take, inicio_no_take, duracao_final, velocidade, efeito)
SEG = [
 ("101606", 0.0, 1.0, 2.0, "punch"),   # ônibus/carro passando = abertura rápida
 ("101750", 5.0, 2.5, 1.5, "push"),    # fachada Centro de Treinamento GCM
 ("095858", 0.2, 1.5, 1.5, "punch"),   # banner "a guarda mais antiga do Brasil"
 ("095858", 2.4, 1.0, 1.0, "push"),
 ("100325", 2.0, 1.5, 1.0, "push"),    # brasão na parede
 ("100757", 0.3, 2.0, 1.5, "punch"),   # sala de aula (pan)
 ("100829", 0.2, 1.5, 1.0, "push"),    # costas GCM
 ("100829", 5.6, 1.5, 1.0, "punch"),
 ("100829", 10.2, 1.0, 1.0, "push"),
 ("101014", 1.0, 1.5, 1.0, "punch"),   # academia
 ("101123", 0.0, 1.0, 1.5, "punch"),   # halteres
 ("101123", 3.2, 1.0, 1.5, "punch"),
 ("101123", 6.2, 1.0, 1.5, "punch"),
 ("101123", 9.6, 1.0, 1.5, "punch"),
 # clímax: tropa em formação com o som original (5.4s→15.4s do take)
 ("110250", 5.4, 3.0, 1.0, "flash"),
 ("110656", 2.0, 1.0, 1.0, "punch"),  # tropa de costas (travelling)
 ("110250", 9.4, 2.0, 1.0, "punch"),
 ("110656", 5.5, 1.0, 1.0, "punch"),
 ("110250", 12.4, 3.0, 1.0, "push"),
 ("100325", 4.6, 3.0, 1.0, "final"),   # brasão final
]
GRADE = ("eq=contrast=1.10:saturation=1.18:gamma=0.96,"
         "curves=r='0/0 0.5/0.47 1/0.95':g='0/0 0.5/0.49 1/0.97':b='0/0.02 0.5/0.53 1/1',"
         "unsharp=5:5:0.6,vignette=PI/5")
parts = []
for i, (code, ss, dur, sp, fx) in enumerate(SEG):
    z = {"punch": f"1.04+0.14*max(0,1-t/0.35)+0.03*t/{dur}",
         "push":  f"1.04+0.06*t/{dur}",
         "flash": f"1.04+0.10*max(0,1-t/0.5)+0.03*t/{dur}",
         "final": f"1.04+0.10*t/{dur}"}[fx]
    vf = (f"setpts=(PTS-STARTPTS)/{sp},fps={FPS},"
          f"scale=w='trunc(1080*({z})/2)*2':h='trunc(1920*({z})/2)*2':eval=frame,"
          f"crop=1080:1920,{GRADE},format=yuv420p")
    if fx == "flash": vf += ",fade=in:st=0:d=0.25:color=white"
    if fx == "final": vf += f",fade=out:st={dur-0.8}:d=0.8"
    out = f"{TMP}/s{i:02d}.mp4"; parts.append(out)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur*sp+0.2),"-i",take(code),
        "-an","-vf",vf,"-t",str(dur),"-r",str(FPS),"-c:v","libx264","-crf","16","-preset","medium",out],check=True)
with open(f"{TMP}/list.txt","w") as f: f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{TMP}/list.txt","-c","copy",f"{TMP}/video.mp4"],check=True)

# ---------- trilha sintetizada (120 BPM) ----------
SR = 44100; TOTAL = sum(s[2] for s in SEG); T_CANTO = 19.0; T_FIM = 29.0
n = int(SR*TOTAL); mus = np.zeros(n); rng = np.random.default_rng(7)
def add(sig, t, g=1.0):
    i = int(t*SR); j = min(n, i+len(sig));
    if i < n: mus[i:j] += g*sig[:j-i]
def env(d, a=0.002, k=8.0):
    tt = np.arange(int(d*SR))/SR; return np.minimum(tt/a,1)*np.exp(-k*tt), tt
def kick(g=1):
    e, tt = env(0.45, k=9); f = 45+90*np.exp(-tt*30); return g*e*np.sin(2*np.pi*np.cumsum(f)/SR)
def snare():
    e, tt = env(0.25, k=18); return e*(0.7*rng.standard_normal(len(tt))+0.4*np.sin(2*np.pi*190*tt))
def hat():
    e, tt = env(0.05, k=80); x = rng.standard_normal(len(tt)); return e*np.diff(x, prepend=0)
def boom(d=3.0):
    e, tt = env(d, a=0.005, k=1.6); f = 30+60*np.exp(-tt*6)
    return e*(np.sin(2*np.pi*np.cumsum(f)/SR) + 0.25*rng.standard_normal(len(tt))*np.exp(-tt*5))
def riser(d):
    tt = np.arange(int(d*SR))/SR; x = rng.standard_normal(len(tt))
    x = np.convolve(x, np.ones(6)/6, "same"); return x*(tt/d)**2.5
BEAT = 0.5
for b in range(int(T_CANTO/BEAT)):
    t = b*BEAT
    fast = t >= 13.5
    add(kick(), t, 0.9)
    if b % 2 == 1: add(snare(), t, 0.45)
    add(hat(), t+0.25, 0.25)
    if fast: add(hat(), t+0.125, 0.18); add(hat(), t+0.375, 0.18)
    if fast and b % 2 == 1: add(kick(0.6), t+0.25)
# baixo pulsando (Ré menor) e pad
tt = np.arange(int(T_CANTO*SR))/SR
bass = np.sin(2*np.pi*36.7*tt)*(0.5+0.5*np.sign(np.sin(2*np.pi*4*tt)))*0.35
pad = sum(np.sin(2*np.pi*f*tt+np.sin(2*np.pi*0.3*tt)) for f in (146.8,174.6,220.0))*0.05
mus[:len(tt)] += bass + pad*np.minimum(tt/2,1)
for t in (0.0, 7.5, 13.5): add(boom(2.0), t, 0.7)
add(riser(2.0), T_CANTO-2.0, 0.35)
add(boom(4.0), T_CANTO, 1.0)
# pad baixo sob o canto
tc = np.arange(int((T_FIM-T_CANTO)*SR))/SR
add(sum(np.sin(2*np.pi*f*tc) for f in (73.4,110.0))*0.06*np.minimum(tc/1,1), T_CANTO)
add(boom(3.0), T_FIM, 1.0)
for k in range(4): add(kick(0.5*(0.6**k)), T_FIM+0.5*k)
mus = np.tanh(mus*1.2)*0.8
with wave.open(f"{TMP}/musica.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mus*32767).astype(np.int16).tobytes())

# canto original da tropa (take 110250, 5.4s → 15.4s) entra no T_CANTO
d = int(T_CANTO*1000)
af = (f"[1:a]atrim=5.4:15.6,asetpts=PTS-STARTPTS,highpass=f=80,acompressor=threshold=-18dB:ratio=3,"
      f"volume=1.6,afade=in:d=0.15,afade=out:st=9.6:d=0.4,adelay={d}|{d}[canto];"
      f"[2:a]aformat=channel_layouts=stereo,volume=0.9[mus];"
      f"[mus][canto]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{TMP}/video.mp4","-i",take("110250"),"-i",f"{TMP}/musica.wav",
    "-filter_complex",af,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",
    "-movflags","+faststart","-shortest",OUT],check=True)
print(OUT, TOTAL, "s")
