# Trilha chiptune original (quadrada/triângulo/ruído) 44.1 kHz, 24 s + sfx nos cortes.
import numpy as np, wave
SR=44100; D=24.0; BPM=150; beat=60/BPM; N=int(SR*D); out=np.zeros(N)
f=lambda m:440*2**((m-69)/12)
def note(t0,dur,freq,kind,vol):
    a=int(t0*SR); n=int(dur*SR); n=min(n,N-a)
    if n<=0: return
    t=np.arange(n)/SR; ph=(t*freq)%1
    w={'sq':np.sign(ph-.5)*.5+np.sign(ph-.25)*.0,'pl':np.where(ph<.25,1,-1)*.5,'tri':(np.abs(ph*4-2)-1)}[kind]
    env=np.minimum(1,t/0.005)*np.exp(-t*3/dur)
    out[a:a+n]+=w*env*vol
def noise(t0,dur,vol,dec=30):
    a=int(t0*SR); n=min(int(dur*SR),N-a)
    if n<=0: return
    t=np.arange(n)/SR
    out[a:a+n]+=np.random.uniform(-1,1,n)*np.exp(-t*dec)*vol
prog=[45,41,43,40]  # Am F G E
lead=[69,72,76,72,74,72,71,67, 69,72,77,76,74,71,72,76]
for bar in range(int(D/(beat*4))+1):
    t=bar*beat*4; r=prog[bar%4]
    if t<1.1: continue
    for i in range(8): note(t+i*beat/2,beat/2*.9,f(r-12 if i%2==0 else r),'tri',.35)
    if t>3:
        for i in range(8): note(t+i*beat/2,beat/2*.8,f(lead[(bar%2)*8+i]+(0 if r!=40 else -1*(i%3==0))),'pl',.12)
    for i in range(4):
        noise(t+i*beat,.12,.25 if i%2==0 else .15,40 if i%2==0 else 18)
        if t>3: noise(t+i*beat+beat/2,.03,.06,120)
    for i in range(16): note(t+i*beat/4,beat/4*.7,f(r+24+[0,3,7,12][i%4]),'sq',.04)
# boot blips
for i,m in enumerate([84,88,91,96]): note(0.3+i*.18,.12,f(m),'sq',.15)
# sfx cortes: varredura + ruído
for tc in [3,6,10,12.5,14.5,16,20]:
    n=int(.25*SR);a=int(tc*SR);n=min(n,N-a);t=np.arange(n)/SR;fr=900*np.exp(-t*8)+120
    out[a:a+n]+=np.sign(np.sin(2*np.pi*np.cumsum(fr)/SR))*np.exp(-t*10)*.18; noise(tc,.3,.3,12)
noise(14.6,1.2,.45,4)  # explosão
out[int(23*SR):]*=np.linspace(1,0,N-int(23*SR))
out=out/np.max(np.abs(out))*.85
with wave.open('trilha.wav','wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
