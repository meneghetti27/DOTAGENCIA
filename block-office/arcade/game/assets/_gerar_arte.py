# Gera toda a arte pixel do HARD x BLOCK. Rodar: python3 _gerar_arte.py (de qualquer pasta)
import os, glob, math, random
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

AQ = os.path.dirname(os.path.abspath(__file__))
ARC = os.path.normpath(os.path.join(AQ, '..', '..'))
os.makedirs(os.path.join(AQ, 'pecas'), exist_ok=True)

def H(c): return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
K0,K1,K2,K3,K4,K5,K6,K7 = [H(c) for c in "#0b0b0f #1d1d24 #34343d #55555f #7b7b86 #a6a6ae #d4d4d8 #f4f2ea".split()]
VD,VC,RX,RC,VM,LR,AM,JE = [H(c) for c in "#2f8f3a #6fd16a #6b3fa0 #a77be0 #c7261f #f0662a #ffc23d #3c5a8a".split()]
BAYER = np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16.0

class C:  # canvas RGBA simples
    def __init__(s, w, h, bg=None):
        s.w, s.h = w, h
        s.a = np.zeros((h, w, 4), np.uint8)
        if bg: s.a[..., :3] = bg; s.a[..., 3] = 255
    def p(s, x, y, c, a=255):
        x, y = int(x), int(y)
        if 0 <= x < s.w and 0 <= y < s.h:
            if a >= 255: s.a[y, x, :3] = c; s.a[y, x, 3] = 255
            else:
                t = a/255; s.a[y, x, :3] = (s.a[y, x, :3]*(1-t) + np.array(c)*t).astype(np.uint8)
                s.a[y, x, 3] = max(s.a[y, x, 3], a)
    def r(s, x0, y0, x1, y1, c, a=255):
        for y in range(int(y0), int(y1)+1):
            for x in range(int(x0), int(x1)+1): s.p(x, y, c, a)
    def save(s, n): Image.fromarray(s.a, 'RGBA').save(os.path.join(AQ, n))
    def img(s): return Image.fromarray(s.a, 'RGBA')

def outline(arr, col=K0):
    m = arr[..., 3] > 0; o = nd.binary_dilation(m) & ~m
    arr[o, :3] = col; arr[o, 3] = 255; return arr

def mix(a, b, t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def dith(c1, c2, t, x, y): return c2 if t > BAYER[y % 4, x % 4] else c1

# ---------------- PADDLE: bloco de concreto vazado visto de frente ----------------
def bloco(w, h, nfuros, rachado=False, seed=1):
    rnd = random.Random(seed); c = C(w, h)
    for y in range(h):
        for x in range(w):
            col = K4
            if y <= 1: col = K6 if y == 0 else K5
            elif y >= h-2: col = K3 if y == h-2 else K2
            elif x == 0 or x == w-1: col = K3
            n = rnd.random()
            if col == K4 and n < .12: col = K5
            elif col == K4 and n < .22: col = K3
            c.p(x, y, col)
    fw = (w-4)//nfuros
    for i in range(nfuros):
        x0 = 2 + i*fw + 2; x1 = 2 + (i+1)*fw - 3
        y0, y1 = 3, h-4
        c.r(x0, y0, x1, y1, K0)
        c.r(x0, y0, x1, y0, K1)            # sombra interna em cima
        c.r(x0, y0, x0, y1, K1)
        c.r(x0+1, y1, x1, y1, K2)          # luz no fundo do furo
        c.p(x1+1, y0, K3); c.r(x0, y1+1, x1+1, y1+1, K6)  # aresta de baixo iluminada
    if rachado:
        x, y = w//2 + 1, 0
        while y < h:
            c.p(x, y, K0); c.p(x+1, y, K2); y += 1; x += rnd.choice([-1, 0, 1])
        for k in range(5): c.p(rnd.randrange(2, w-2), rnd.randrange(2, h-2), K1)
        c.r(1, h-2, 3, h-1, K1, 0); c.a[h-2:, :3, 3] = 0  # canto lascado
    return c

bloco(48, 12, 2).save('paddle.png')
bloco(72, 12, 3).save('paddle-largo.png')
bloco(32, 12, 2).save('paddle-curto.png')
bloco(24, 12, 2, seed=3).save('f1-bloco.png')
bloco(24, 12, 2, True, seed=3).save('f1-bloco-rachado.png')

# ---------------- alvos fase 1 ----------------
def arara():
    c = C(24, 12)
    for x in range(24):  # cano de cima
        c.p(x, 1, K5); c.p(x, 2, LR if (x*7) % 5 == 0 else K4); c.p(x, 3, K2)
    for x in (1, 22):
        for y in range(1, 12): c.p(x, y, K4); c.p(x+1, y, K2)
        c.p(x, 4 + (x % 3), LR); c.p(x, 8, VM)
    for x in range(2, 22): c.p(x, 10, K3)
    c.r(0, 0, 3, 1, K6); c.r(20, 0, 23, 1, K6)  # braçadeiras
    c.p(1, 0, K7); c.p(21, 0, K7)
    for x in range(5, 20, 4):  # cabides com roupinha
        c.p(x, 4, K6); c.r(x-1, 5, x+1, 5, K5)
        c.r(x-1, 6, x+1, 9, [JE, K1, K3, VD][(x//4) % 4])
    c.save('f1-arara.png')
arara()

FONT35 = {'3': ["111", "001", "011", "001", "111"], '4': ["101", "101", "111", "001", "001"],
          '9': ["111", "101", "111", "001", "111"]}
def placa349():
    c = C(36, 14)
    c.r(0, 0, 35, 13, K1); c.r(1, 1, 34, 12, K0)
    for x in range(1, 35): c.p(x, 1, K3); c.p(x, 12, K1)
    c.r(2, 2, 33, 11, (18, 18, 22))
    for (x, y) in [(2, 2), (33, 2), (2, 11), (33, 11)]: c.p(x, y, K5)
    x = 8
    for ch in "349":
        g = FONT35[ch]
        for gy in range(5):
            for gx in range(3):
                if g[gy][gx] == '1':
                    for dy in range(2):
                        for dx in range(2): c.p(x+gx*2+dx, 3+gy*2//1+dy if False else 3+gy*1.6+dy, K7)
        x += 7
    # brilho
    for x in range(3, 33, 9): c.p(x, 3, (60, 60, 70))
    c.save('f1-placa.png')
# placa: número em pixels 2x (altura 9)
def placa349b():
    c = C(36, 14)
    c.r(0, 0, 35, 13, K3); c.r(1, 1, 34, 12, K0)
    for x in range(1, 35): c.p(x, 1, K2)
    for (x, y) in [(2, 2), (33, 2), (2, 11), (33, 11)]: c.p(x, y, K5)
    x = 7
    for ch in "349":
        g = FONT35[ch]
        for gy in range(5):
            for gx in range(3):
                if g[gy][gx] == '1':
                    yy = [3, 5, 6, 8, 9][gy]; hh = [2, 1, 2, 1, 2][gy]
                    for dy in range(hh):
                        for dx in range(2): c.p(x+gx*2+dx, yy+dy, K7 if dy == 0 else K6)
        x += 8
    c.save('f1-placa.png')
placa349b()

# ---------------- fase 2 ----------------
def assento():
    c = C(24, 12)
    for x in range(24):
        top = 3 + int(2*((x-12)/12)**2) if x > 2 else 6 - x
        for y in range(top, 10):
            col = K1
            if y == top: col = K4
            elif y == top+1: col = K2
            if y >= 8: col = K0
            c.p(x, y, col)
    for x in range(4, 20, 3): c.p(x, 6, K2)  # costura
    c.r(2, 10, 21, 11, K3); c.r(2, 11, 21, 11, K2)  # base
    c.r(10, 10, 13, 10, AM)
    c.save('f2-assento.png')
assento()

def guarda(torto=False):
    c = C(24, 12)
    def off(x): return int(3*math.sin(x/24*math.pi)) if torto else 0
    for x in range(24):
        o = off(x)
        c.p(x, 1+o, K4); c.p(x, 2+o, K1)
        c.p(x, 9, K3); c.p(x, 10, K1)
    for x in (0, 6, 12, 18, 23):
        for y in range(1+off(x), 11): c.p(x, y, K2 if x % 12 else K3)
        c.p(x, 1+off(x), K5)
    if torto:
        c.p(12, 4, LR); c.p(13, 5, LR)
    c.save('f2-guarda-torto.png' if torto else 'f2-guarda.png')
guarda(); guarda(True)

def moto(dano=False):
    c = C(48, 28); rnd = random.Random(5)
    def roda(cx, cy, r):
        for y in range(-r, r+1):
            for x in range(-r, r+1):
                d = math.hypot(x, y)
                if d <= r+.3:
                    col = K1 if d > r-2 else (K3 if d < 1.5 else (K0 if d > 2.5 else K2))
                    if d > r-2 and (x+y) % 3 == 0: col = K2  # cravos
                    c.p(cx+x, cy+y, col)
        c.p(cx-1, cy-1, K5)
    roda(9, 20, 7); roda(38, 20, 7)
    # quadro e motor
    c.r(17, 15, 29, 21, K2); c.r(18, 16, 28, 20, K3)
    for x in range(19, 28, 2): c.p(x, 17, K5)
    c.r(20, 21, 30, 22, K4)  # escape
    c.r(29, 13, 31, 14, K4)
    for i in range(10): c.p(9+i, 19-i, K4); c.p(10+i, 19-i, K2)  # balança
    for i in range(12): c.p(38-i//2, 20-i, K5); c.p(39-i//2, 20-i, K3)  # garfo
    # tanque + carenagem amarelos
    for x in range(14, 36):
        y0 = 9 - (2 if 22 < x < 32 else 0); y1 = 15
        for y in range(y0, y1):
            col = AM if y > y0+1 else (255, 230, 140)
            if y >= y1-2: col = (196, 140, 30)
            c.p(x, y, col)
    c.r(16, 11, 27, 12, K7); c.r(17, 11, 18, 12, VM)  # faixa / logo
    # paralama dianteiro e traseiro
    for x in range(32, 46): c.p(x, 10 + (x-38)**2//12, AM); c.p(x, 11+(x-38)**2//12, (196, 140, 30))
    for x in range(2, 16): c.p(x, 8 + abs(x-6)//3, AM); c.p(x, 9+abs(x-6)//3, (196, 140, 30))
    c.r(6, 7, 22, 8, K1)  # banco
    c.r(30, 5, 36, 6, K2); c.p(29, 5, K5); c.p(37, 5, K5)  # guidão
    c.r(36, 8, 40, 11, K6); c.p(37, 9, K0); c.r(38, 9, 39, 10, AM)  # placa numero
    # cintas vermelhas penduradas
    for (x, top) in [(12, 0), (34, 0)]:
        for y in range(top, 13):
            c.p(x, y, VM); c.p(x+1, y, (140, 20, 20))
        c.r(x-1, 0, x+2, 0, K4)
    if dano:
        for _ in range(14): x = rnd.randrange(12, 36); y = rnd.randrange(8, 16); c.p(x, y, K1)
        for i in range(6): c.p(20+i, 9+i % 3, K0)
        c.r(43, 13, 45, 15, (0, 0, 0), 0); c.a[13:16, 42:46, 3] = 0
        c.p(25, 6, K4); c.p(26, 4, K3); c.p(24, 3, K2)  # fumacinha
    outline(c.a, K0)
    c.save('f2-moto-dano.png' if dano else 'f2-moto.png')
moto(); moto(True)

# ---------------- fase 3 ----------------
def cupula(acesa):
    c = C(20, 14)
    c.r(9, 0, 10, 2, K3)  # fio/canopla
    for y in range(3, 13):
        t = (y-3)/9; half = int(2 + 7.5*math.sin(min(1, t*1.25)*math.pi/2))
        for x in range(10-half, 10+half):
            band = (y - 3) % 3 == 0
            if acesa:
                col = K7 if band else mix(AM, (255, 240, 200), 1-t)
                if abs(x-9.5) > half-1.2: col = LR
            else:
                col = K4 if band else (K2 if (x+y) % 2 else K3)
                if abs(x-9.5) > half-1.2: col = K1
            c.p(x, y, col)
    for x in range(3, 17): c.p(x, 12, K6 if acesa else K4)
    if acesa:
        c.p(9, 13, K7); c.p(10, 13, K7); c.p(8, 13, AM); c.p(11, 13, AM)
        c.p(6, 5, K7)
    else:
        c.p(6, 5, K5)
    outline(c.a, K0)
    c.save('f3-cupula-acesa.png' if acesa else 'f3-cupula.png')
cupula(False); cupula(True)

def caveira(fr):
    W, Hh = 72, 60; c = C(W, Hh); rnd = random.Random(9)
    jaw = 4 if fr == 2 else 0
    cx = 36
    # crânio (elipse)
    for y in range(2, 40):
        for x in range(4, 68):
            if ((x-cx)/31)**2 + ((y-22)/20)**2 <= 1: c.p(x, y, K7)
    # maçãs/temporas
    for y in range(28, 44):
        for x in range(10, 62):
            if ((x-cx)/26)**2 + ((y-32)/12)**2 <= 1: c.p(x, y, K7)
    # mandíbula
    for y in range(42+jaw, 56+jaw):
        for x in range(16, 56):
            if ((x-cx)/20)**2 + ((y-(44+jaw))/12)**2 <= 1 and y >= 42+jaw: c.p(x, y, K7)
    # sombreado blackwork (hachura) lado direito/baixo
    for y in range(Hh):
        for x in range(W):
            if c.a[y, x, 3] and c.a[y, x, :3].tolist() == list(K7):
                t = (x-cx)/34 + (y-20)/60
                if t > .45 and (x+y) % 3 == 0: c.p(x, y, K0)
                elif t > .25 and (x+2*y) % 5 == 0: c.p(x, y, K5)
    # olhos
    for ex in (22, 50):
        for y in range(16, 32):
            for x in range(ex-9, ex+10):
                if ((x-ex)/8.5)**2 + ((y-24)/7.5)**2 <= 1: c.p(x, y, K0)
        c.p(ex-3, 22, VM); c.p(ex-2, 22, LR); c.p(ex-3, 23, VM)  # brilho vermelho no olho
    # nariz
    for i in range(6):
        for x in range(cx-i//2-1, cx+i//2+2): c.p(x, 31+i, K0)
    # dentes superiores e boca
    c.r(20, 40, 52, 41+jaw, K0)
    for x in range(21, 52, 4):
        c.r(x, 38, x+2, 40, K7); c.p(x+3, 38, K0); c.p(x+3, 39, K0); c.p(x+3, 40, K0); c.p(x, 40, K5)
        c.r(x, 42+jaw, x+2, 44+jaw, K7); c.p(x+3, 42+jaw, K0); c.p(x+3, 43+jaw, K0); c.p(x+2, 42+jaw, K5)
    if jaw:
        c.r(22, 42, 50, 41+jaw, VM, 255)  # garganta incandescente
        for x in range(24, 49, 3): c.p(x, 43, LR); c.p(x+1, 42, AM)
    # rachaduras de grafite
    for (x, y) in [(30, 3), (48, 6)]:
        for i in range(8): c.p(x, y+i, K0); x += rnd.choice([-1, 0, 1])
    # selo/carimbo vermelho na testa
    sx, sy = 50, 8
    for y in range(-6, 7):
        for x in range(-6, 7):
            d = math.hypot(x, y)
            if 4.5 <= d <= 6.2 or (d < 3.5 and (x+y) % 2 == 0): c.p(sx+x, sy+y, VM)
    c.p(sx, sy, K7)
    # respingos de tinta
    for _ in range(12):
        x, y = rnd.randrange(2, 70), rnd.randrange(0, 58)
        if c.a[y, x, 3] == 0: c.p(x, y, K7 if rnd.random() < .5 else VM)
    if fr == 3:  # dano: tudo avermelhado e rachado
        m = c.a[..., 3] > 0
        rgb = c.a[..., :3].astype(int)
        lum = rgb.mean(2, keepdims=True)
        c.a[..., :3] = np.where(m[..., None], np.clip(lum*np.array([1.0, .35, .3]) + np.array([90, 0, 0]), 0, 255), rgb).astype(np.uint8)
        for (x, y) in [(36, 4), (16, 14), (58, 18)]:
            for i in range(18): c.p(x, y+i, K7); c.p(x+1, y+i, K0); x += rnd.choice([-1, 0, 1, 1]) * (1 if x < 36 else -1)
    outline(c.a, K0)
    outline(c.a, K7 if fr != 3 else LR)  # aura de adesivo
    c.save({1: 'f3-caveira-1.png', 2: 'f3-caveira-2.png', 3: 'f3-caveira-dano.png'}[fr])
for f in (1, 2, 3): caveira(f)

def fogo():
    c = C(8, 12)
    shape = ["...aa...", "..aYa...", "..aYYa..", ".aYWYa..", ".aYWWYa.", "aYWWWYa.", "aYWWWWYa",
             "aYWWWWYa", ".aYWWYa.", ".aYYYa..", "..aaa...", "...r...."]
    cm = {'a': VM, 'Y': LR, 'W': AM, 'r': (120, 20, 20)}
    for y, row in enumerate(shape):
        for x, ch in enumerate(row):
            if ch in cm: c.p(x, y, cm[ch])
    c.p(3, 6, K7); c.p(4, 7, K7)
    c.save('f3-fogo.png')
fogo()

# ---------------- poderes 14x14 ----------------
def ficha(cor_borda, desenho, nome, mal=False):
    c = C(14, 14)
    for y in range(14):
        for x in range(14):
            d = math.hypot(x-6.5, y-6.5)
            if d <= 6.8:
                col = K1
                if d > 5.6: col = cor_borda
                elif y < 6 and d < 5: col = K2
                c.p(x, y, col)
    desenho(c)
    if mal: c.p(10, 2, K7)
    else: c.p(3, 3, K7)
    c.save(nome)

def d_drop(c):  # duas camisetas
    for ox, col in ((3, K6), (6, AM)):
        c.r(ox, 4, ox+4, 4, col); c.r(ox-1, 5, ox+5, 5, col); c.r(ox, 6, ox+4, 9, col); c.p(ox+2, 4, K1)
def d_andaime(c):
    for x in range(2, 12): c.p(x, 4, LR); c.p(x, 9, LR)
    for y in range(3, 11): c.p(3, y, K5); c.p(10, y, K5)
    for i in range(5): c.p(4+i*1.2, 5+i*.8, K4)
    c.p(2, 6, K7); c.p(11, 6, K7)
def d_touca(c):
    for y in range(4, 10):
        for x in range(3, 11):
            if ((x-6.5)/4)**2 + ((y-9)/5)**2 <= 1: c.p(x, y, K0 if (x % 2) else K2)
    c.r(3, 9, 10, 10, K4); c.r(5, 9, 8, 10, K7)  # etiqueta block
    c.p(6, 3, K3); c.p(7, 3, K3)
def d_encolhe(c):
    c.r(4, 6, 9, 7, K5)
    for i in range(3): c.p(1+i, 5+i if i < 2 else 7, K7); c.p(12-i, 5+i if i < 2 else 7, K7)
    c.p(2, 8, K7); c.p(11, 8, K7); c.p(1, 6, K7); c.p(12, 6, K7)
def d_luz(c):
    c.r(5, 3, 8, 7, K3); c.r(6, 8, 7, 9, K4); c.p(6, 4, K5)
    for i in range(10): c.p(2+i, 2+i, VM)
    c.p(9, 3, K4)
ficha(VC, d_drop, 'pw-drop.png'); ficha(AM, d_andaime, 'pw-andaime.png'); ficha(RC, d_touca, 'pw-touca.png')
ficha(VM, d_encolhe, 'pw-encolhe.png', True); ficha(VM, d_luz, 'pw-luz.png', True)

def vida():
    c = C(10, 10)
    rows = ["...xxxx...", "..xKKKKx..", ".xKKKKKKx.", ".xKKKKKKx.", "xKKKKKKKKx", "xWWWWWWWWx", "xWRRWWWWWx", "xxxxxxxxxx"]
    cm = {'x': K0, 'K': K2, 'W': K6, 'R': VM}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in cm: c.p(x, y+1, cm[ch])
    c.p(4, 2, K4); c.p(3, 3, K4)
    c.save('vida.png')
vida()

def puff(i):
    c = C(20, 20); rnd = random.Random(i)
    r0 = [4, 7, 9][i-1]; n = [4, 6, 7][i-1]
    for k in range(n):
        a = k/n*2*math.pi + i; rr = r0*(.5 if i == 1 else .75)
        bx, by = 10+math.cos(a)*rr, 10+math.sin(a)*rr; br = [3, 3.5, 2.5][i-1]
        for y in range(20):
            for x in range(20):
                d = math.hypot(x-bx, y-by)
                if d <= br:
                    col = K7 if (x-bx+y-by) < -1 else (K6 if d < br-1 else K5)
                    if i == 3 and BAYER[y % 4, x % 4] < .5: continue
                    c.p(x, y, col)
    c.save(f'puff{i}.png')
for i in (1, 2, 3): puff(i)

# ---------------- logos ----------------
def logo_hard():
    im = Image.open(os.path.join(ARC, 'marca', 'hard-jeans-santo.jpg')).convert('L')
    a = np.asarray(im) > 128; ys, xs = np.where(a)
    a = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    w = 196; h = round(a.shape[0]*w/a.shape[1])
    s = np.asarray(Image.fromarray((a*255).astype(np.uint8)).resize((w, h), Image.BOX)) > 100
    out = np.zeros((h+4, w+4, 4), np.uint8); out[2:-2, 2:-2][s] = [*K7, 255]
    # leve sombreado nas bases das letras
    m = out[..., 3] > 0; bot = m & ~np.roll(m, -1, 0); out[bot, :3] = K5
    outline(out, K0); outline(out, K0)
    Image.fromarray(out, 'RGBA').save(os.path.join(AQ, 'logo-hard.png'))
logo_hard()

def logo_block():
    im = Image.open(os.path.join(ARC, 'marca', 'block-logo.webp')).convert('RGBA')
    A = np.asarray(im).astype(int)
    w = 62; h = round(A.shape[0]*w/A.shape[1])
    sm = np.asarray(im.resize((w, h), Image.BOX)).astype(int)
    al = sm[..., 3] > 120; lum = sm[..., :3].mean(2)
    out = np.zeros((h+2, w+2, 4), np.uint8)
    blk = al & (lum < 128); wht = al & (lum >= 128)
    o = out[1:-1, 1:-1]
    o[blk] = [*K7, 255]; o[wht] = [*K1, 255]
    # sombreia face lateral
    yy, xx = np.mgrid[0:h, 0:w]
    o[blk & (xx > w*.5) & ((xx+yy) % 2 == 0)] = [*K6, 255]
    outline(out, K0)
    Image.fromarray(out, 'RGBA').save(os.path.join(AQ, 'logo-block.png'))
logo_block()

# ---------------- peças do drop ----------------
PAL = ["#0b0b0f","#1d1d24","#34343d","#55555f","#7b7b86","#a6a6ae","#d4d4d8","#f4f2ea",
       "#2f8f3a","#6fd16a","#6b3fa0","#a77be0","#c7261f","#f0662a","#ffc23d","#3c5a8a"]
pal = np.array([H(c) for c in PAL])
def sprite(path, Hh):
    a = np.asarray(Image.open(path).convert('RGB')).astype(int)
    fundo = (a.min(2) > 232)
    lab, n = nd.label(fundo); borda = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    m = ~np.isin(lab, list(borda)); m = nd.binary_opening(m, iterations=2)
    l2, n2 = nd.label(m); s = nd.sum(m, l2, range(1, n2+1)); m = l2 == (np.argmax(s)+1); m = nd.binary_fill_holes(m)
    ys, xs = np.where(m); a = a[ys.min():ys.max()+1, xs.min():xs.max()+1]; m = m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h = Hh-2; w = max(1, round(a.shape[1]*h/a.shape[0]))
    small = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(int)
    ms = np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize((w, h), Image.BOX)) > 110
    from PIL import ImageEnhance
    si = Image.fromarray(small.astype(np.uint8)); si = ImageEnhance.Contrast(si).enhance(1.35); si = ImageEnhance.Color(si).enhance(1.3)
    q = np.asarray(si.quantize(14, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')).astype(int)
    out = np.zeros((h+2, w+2, 4), np.uint8); out[1:-1, 1:-1, :3] = q; out[1:-1, 1:-1, 3] = ms*255
    mm = out[..., 3] > 0; cont = nd.binary_dilation(mm) & ~mm; out[cont] = [244, 242, 234, 255]
    bi = mm & ~nd.binary_erosion(mm); out[bi & (out[..., :3].sum(2) < 120)] = [85, 85, 95, 255]
    return Image.fromarray(out, 'RGBA')
LADO = {'01': '02', '02': '02', '03': '02', '04': '02', '05': '02', '07': '02'}
for i, d in enumerate(sorted(glob.glob(os.path.join(ARC, 'drop', '0*')))):
    k = os.path.basename(d)[:2]
    sprite(os.path.join(d, f"foto-{LADO.get(k, '01')}.webp"), 40).save(os.path.join(AQ, 'pecas', f'p{i+1}.png'))

# ---------------- fundos 270x480 ----------------
W, HH = 270, 480
def concreto(c, y0, y1, base, rnd, manchas=True):
    for y in range(y0, y1):
        for x in range(W):
            n = rnd.random()
            col = base
            if n < .10: col = mix(base, K0, .35)
            elif n < .16: col = mix(base, K4, .25)
            c.p(x, y, col)
    if manchas:
        for _ in range(14):  # manchas de umidade escorrendo
            x = rnd.randrange(W); y = rnd.randrange(y0, max(y0+1, y1-60)); L = rnd.randrange(20, 70); wd = rnd.randrange(2, 7)
            for k in range(L):
                for dx in range(wd):
                    if rnd.random() < .7 - k/L*.6: c.p(x+dx+(k//15), y+k, mix(base, K0, .5), 160)
        for _ in range(9):  # reboco descascando (manchas claras com borda escura)
            x = rnd.randrange(W); y = rnd.randrange(y0, y1-10); rw, rh = rnd.randrange(6, 22), rnd.randrange(4, 12)
            for yy in range(rh):
                for xx in range(rw):
                    if ((xx-rw/2)/(rw/2))**2 + ((yy-rh/2)/(rh/2))**2 <= 1 - rnd.random()*.25:
                        c.p(x+xx, y+yy, mix(base, K5, .35))
            for xx in range(rw): c.p(x+xx, y+rh, K0, 150)
def escurece_centro(c, forca=.45, y0=80, y1=400):
    for y in range(HH):
        for x in range(W):
            t = 0
            if y0 < y < y1: t = forca*math.sin((y-y0)/(y1-y0)*math.pi)
            vx = abs(x-W/2)/(W/2); t = max(t, .5*vx**3)
            if t > 0: c.a[y, x, :3] = (c.a[y, x, :3]*(1-t)).astype(np.uint8)
def cone(c, x, y, comp, larg, cor, alpha=60):
    for yy in range(comp):
        hw = 1 + yy*larg/comp
        for xx in range(int(x-hw), int(x+hw)+1):
            t = (1-yy/comp)*(1-abs(xx-x)/(hw+1))
            a = alpha*t
            if a/alpha > BAYER[(y+yy) % 4, xx % 4]*.6: c.p(xx, y+yy, cor, int(a))

def bg1():
    rnd = random.Random(11); c = C(W, HH, K2)
    concreto(c, 0, 400, (62, 62, 68), rnd)
    # teto + trilho de spots
    c.r(0, 0, W-1, 18, K1); c.r(0, 19, W-1, 20, K0)
    c.r(0, 26, W-1, 27, K0); c.r(0, 28, W-1, 28, K3)
    for sx in range(24, W, 44):
        c.r(sx-3, 29, sx+3, 34, K0); c.r(sx-2, 30, sx+2, 33, K3); c.r(sx-2, 35, sx+2, 35, (255, 220, 150))
        cone(c, sx, 36, 120, 26, (255, 205, 130), 70)
    # escada metálica preta subindo da direita pra esquerda (vazada)
    x0, y0 = 230, 400; steps = 13
    for i in range(steps):
        x = x0 - i*14; y = y0 - i*22
        c.r(x-22, y, x+8, y+2, K0); c.r(x-22, y, x+8, y, K4)  # degrau
        c.p(x-22, y+3, K1)
    for t in range(0, 300):  # longarinas
        x = x0+8 - t*14/22; y = y0 - t
        c.p(x, y, K0); c.p(x+1, y, K0); c.p(x-1, y, K3)
        x2 = x0-22 - t*14/22
        c.p(x2, y, K0); c.p(x2-1, y, K1)
    for i in range(0, steps, 2):  # guarda-corpo
        x = x0 - i*14 + 6; y = y0 - i*22
        for yy in range(y-30, y): c.p(x, yy, K0)
    for t in range(0, 300):
        c.p(x0+6 - t*14/22, y0-30-t, K0); c.p(x0+6 - t*14/22, y0-31-t, K4)
    # corrente pendurada no centro
    for y in range(20, 210):
        x = 135 + int(2*math.sin(y/30))
        if (y//3) % 2: c.p(x-1, y, K5); c.p(x+1, y, K3)
        else: c.p(x, y, K6); c.p(x, y+1, K4)
    c.r(131, 208, 139, 212, K4); c.r(132, 213, 138, 214, K3)  # gancho
    # arara de andaime lateral com roupas
    for y in range(250, 400): c.p(14, y, K4); c.p(15, y, K2)
    for x in range(10, 80): c.p(x, 250, K5); c.p(x, 251, K3)
    for x in range(20, 76, 8):
        col = rnd.choice([K1, JE, K0, K3, VD]); c.r(x, 254, x+6, 290, col); c.r(x+1, 254, x+5, 255, K5)
    # piso de concreto polido com reflexos
    for y in range(400, HH):
        for x in range(W):
            t = (y-400)/80
            col = mix((48, 48, 54), (30, 30, 36), t)
            if rnd.random() < .06: col = mix(col, K4, .3)
            c.p(x, y, col)
    for sx in range(24, W, 44):
        for y in range(404, 470, 3): c.p(sx + rnd.randint(-2, 2), y, (120, 105, 80), 120)
    c.r(0, 400, W-1, 400, K4); c.r(0, 401, W-1, 401, K1)
    # grafite de caveira pequeno na parede
    for y in range(-6, 7):
        for x in range(-7, 8):
            if (x/7)**2+(y/6)**2 <= 1: c.p(230+x, 120+y, K6)
    c.r(226, 118, 228, 121, K0); c.r(232, 118, 234, 121, K0); c.r(227, 126, 233, 128, K6); c.p(230, 123, K0)
    escurece_centro(c, .5)
    c.save('bg1.png')

def suzuki_grande(c, ox, oy, rnd):
    # moto ~110x70 vista de lado, pendurada
    def roda(cx, cy, r):
        for y in range(-r, r+1):
            for x in range(-r, r+1):
                d = math.hypot(x, y)
                if d <= r:
                    if d > r-4: col = K0 if (int(math.atan2(y, x)*8)) % 2 else K1
                    elif d > r-5: col = K4
                    elif d < 3: col = K4
                    elif (abs(x) < 1 or abs(y) < 1 or abs(x-y) < 1 or abs(x+y) < 1): col = K5
                    else: continue
                    c.p(cx+x, cy+y, col)
    roda(ox+18, oy+52, 17); roda(ox+92, oy+52, 17)
    for i in range(36): c.p(ox+18+i, oy+50-i//3, K3); c.p(ox+18+i, oy+51-i//3, K2)
    for i in range(36): c.p(ox+92-i//3, oy+52-i, K6); c.p(ox+91-i//3, oy+52-i, K4)
    c.r(ox+45, oy+34, ox+72, oy+52, K2); c.r(ox+47, oy+36, ox+70, oy+50, K3)
    for y in range(oy+38, oy+50, 3): c.r(ox+48, y, ox+68, y, K5)
    for x in range(ox+50, ox+80): c.p(x, oy+54 - (x-ox-50)//6, K5); c.p(x, oy+55-(x-ox-50)//6, K3)
    # carenagem amarela
    for x in range(ox+30, ox+86):
        top = oy+22 - (4 if ox+55 < x < ox+78 else 0)
        for y in range(top, oy+36):
            t = (y-top)/(oy+36-top)
            col = (255, 232, 150) if t < .12 else (AM if t < .7 else (200, 140, 28))
            c.p(x, y, col)
    c.r(ox+40, oy+27, ox+66, oy+30, K7); c.r(ox+42, oy+27, ox+50, oy+30, (30, 50, 140))  # grafismo
    for x in range(ox+80, ox+110): c.p(x, oy+26+(x-ox-94)**2//25, AM); c.p(x, oy+27+(x-ox-94)**2//25, (200, 140, 28))
    for x in range(ox, ox+34): c.p(x, oy+20+abs(x-ox-10)//4, AM); c.p(x, oy+21+abs(x-ox-10)//4, (200, 140, 28))
    c.r(ox+14, oy+18, ox+56, oy+21, K0); c.r(ox+14, oy+18, ox+56, oy+18, K3)  # banco
    c.r(ox+76, oy+10, ox+92, oy+12, K1); c.p(ox+75, oy+10, K5)
    c.r(ox+88, oy+16, ox+98, oy+24, K7); c.r(ox+91, oy+18, ox+95, oy+22, K0)  # placa numero
    # cintas vermelhas até o teto
    for sx in (ox+30, ox+82):
        for y in range(0, oy+24):
            c.p(sx, y, VM); c.p(sx+1, y, VM); c.p(sx+2, y, (130, 18, 18))
        c.r(sx-1, oy+22, sx+3, oy+24, K4)

def bg2():
    rnd = random.Random(22); c = C(W, HH, K2)
    concreto(c, 0, 400, (58, 58, 64), rnd)
    # mezanino em cima
    c.r(0, 0, W-1, 70, (30, 30, 36))
    for x in range(0, W, 30): c.r(x, 0, x+2, 70, (22, 22, 26))
    c.r(0, 70, W-1, 78, K1); c.r(0, 70, W-1, 70, K4); c.r(0, 79, W-1, 80, K0)
    for x in range(0, W): c.p(x, 36, K0); c.p(x, 37, K4)  # corrimão
    for x in range(0, W, 9):
        for y in range(38, 70): c.p(x, y, K0)
    for x in range(0, W, 45):
        c.r(x, 36, x+2, 70, K0)
    # luz quente vindo do mezanino
    for sx in (60, 210): cone(c, sx, 81, 110, 30, (255, 200, 120), 55)
    # duas Suzukis na parede (embaixo do mezanino)
    def suzuki_wrap(ox, oy):
        # cintas presas na viga do mezanino
        base = C(W, HH); suzuki_grande(base, ox, oy-oy+0 if False else ox*0+ox, rnd) if False else None
    tmp = C(W, HH)
    suzuki_grande(tmp, 8, 170, rnd)
    suzuki_grande(tmp, 150, 250, rnd)
    m = tmp.a[..., 3] > 0
    m[:81] = False  # cintas começam abaixo do mezanino
    o = nd.binary_dilation(m) & ~m
    c.a[o, :3] = K0
    c.a[m, :3] = tmp.a[m, :3]
    # sombra das motos na parede
    sh = nd.shift(m.astype(float), (4, 4), order=0) > 0
    c.a[sh & ~m & ~o, :3] = (c.a[sh & ~m & ~o, :3]*.6).astype(np.uint8)
    # piso
    for y in range(400, HH):
        for x in range(W):
            col = mix((46, 46, 52), (28, 28, 34), (y-400)/80)
            if rnd.random() < .05: col = mix(col, K4, .3)
            c.p(x, y, col)
    c.r(0, 400, W-1, 400, K4)
    escurece_centro(c, .35, 90, 400)
    c.save('bg2.png')

def bg3():
    rnd = random.Random(33); c = C(W, HH)
    for y in range(HH):  # céu noturno: preto -> roxo escuro -> vermelho
        for x in range(W):
            t = y/HH
            col = mix((8, 6, 14), (34, 14, 40), min(1, t*1.4)) if t < .7 else mix((34, 14, 40), (90, 20, 14), (t-.7)/.3)
            col = dith(col, mix(col, K0, .4), .15, x, y)
            c.p(x, y, col)
    for _ in range(60): c.p(rnd.randrange(W), rnd.randrange(260), K6 if rnd.random() < .3 else K4)
    # céu de cúpulas prismáticas acesas (vários tamanhos = profundidade)
    def cup(cx, cy, s, bright):
        for y in range(-int(cy)-1, 0): c.p(cx, cy+y, K1)
        for y in range(int(s*0.9)):
            t = y/(s*.9); half = s*math.sin(min(1, t*1.2+.15)*math.pi/2)
            for x in range(int(cx-half), int(cx+half)+1):
                band = (y % 3 == 0)
                col = mix(AM, (255, 245, 210), 1-t) if not band else (255, 250, 235)
                if abs(x-cx) > half-1: col = LR
                col = mix((20, 10, 20), col, bright)
                c.p(x, cy+y, col)
        r = s*3.2  # halo
        for y in range(int(-r), int(r)):
            for x in range(int(-r), int(r)):
                d = math.hypot(x, y*1.2)
                if s < d < r:
                    a = (1-d/r)*bright
                    if a*0.9 > BAYER[(cy+y) % 4, (cx+x) % 4]: c.p(cx+x, cy+y+int(s*.6), mix(LR, AM, .4), int(60*a))
    spots = []
    for row in range(6):
        for k in range(7 - row//2):
            cx = rnd.randrange(8, W-8); cy = 18 + row*42 + rnd.randrange(-10, 10)
            s = [4, 5, 7, 8, 10, 12][row] + rnd.randrange(0, 2)
            spots.append((cy, cx, s, .45 + row*.12))
    for cy, cx, s, b in sorted(spots): cup(cx, cy, s, min(1, b))
    # fumaça
    for _ in range(40):
        x, y = rnd.randrange(W), rnd.randrange(250, 420); r = rnd.randrange(6, 16)
        for yy in range(-r, r):
            for xx in range(-r, r):
                if xx*xx+yy*yy < r*r and BAYER[(y+yy) % 4, (x+xx) % 4] < .3: c.p(x+xx, y+yy, (60, 40, 48), 90)
    # chamas pixel embaixo
    heights = [rnd.randrange(30, 75) for _ in range(W)]
    heights = nd.uniform_filter1d(np.array(heights, float), 7)
    for x in range(W):
        hgt = heights[x] + 12*math.sin(x/9) + 8*math.sin(x/4.3)
        for y in range(HH-1, int(HH-hgt)-1, -1):
            t = (HH-y)/hgt
            if t > .85 and BAYER[y % 4, x % 4] < (t-.85)*6: continue
            col = AM if t < .3 else (LR if t < .6 else VM)
            if t < .12: col = (255, 240, 190)
            c.p(x, y, col)
    # calmaria: escurece a faixa onde fica a plataforma, mantém chamas por baixo
    for y in range(400, HH):
        for x in range(W):
            c.a[y, x, :3] = (c.a[y, x, :3]*.75).astype(np.uint8)
    escurece_centro(c, .3, 120, 400)
    c.save('bg3.png')
bg1(); bg2(); bg3()
# ---------------- REVISÃO 2: marcas BLOCK x HARD JEANS SANTO ----------------
_HM = None
def hard_mask(w):
    global _HM
    if _HM is None:
        a = np.asarray(Image.open(os.path.join(ARC, 'marca', 'hard-jeans-santo.jpg')).convert('L')) > 128
        ys, xs = np.where(a); _HM = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h = max(1, round(_HM.shape[0]*w/_HM.shape[1]))
    return np.asarray(Image.fromarray((_HM*255).astype(np.uint8)).resize((w, h), Image.BOX)) > 100
_BM = None
def block_mask(w):  # devolve (preto=corpo do bloco, branco=furos/faces)
    global _BM
    if _BM is None: _BM = Image.open(os.path.join(ARC, 'marca', 'block-logo.webp')).convert('RGBA')
    h = max(1, round(_BM.height*w/_BM.width))
    sm = np.asarray(_BM.resize((w, h), Image.BOX)).astype(int)
    al = sm[..., 3] > 120; lum = sm[..., :3].mean(2)
    return al & (lum < 128), al & (lum >= 128)
FONT = {  # 5x7
 'H':"10001 10001 10001 11111 10001 10001 10001",'A':"01110 10001 10001 11111 10001 10001 10001",
 'R':"11110 10001 10001 11110 10100 10010 10001",'D':"11110 10001 10001 10001 10001 10001 11110",
 'B':"11110 10001 10001 11110 10001 10001 11110",'L':"10000 10000 10000 10000 10000 10000 11111",
 'O':"01110 10001 10001 10001 10001 10001 01110",'C':"01110 10001 10000 10000 10000 10001 01110",
 'K':"10001 10010 10100 11000 10100 10010 10001",'x':"00000 10001 01010 00100 01010 10001 00000",
 '3':"11110 00001 00001 01110 00001 00001 11110",'4':"00010 00110 01010 10010 11111 00010 00010",
 '9':"01110 10001 10001 01111 00001 00010 01100",'P':"11110 10001 10001 11110 10000 10000 10000",
 ' ':"00000 00000 00000 00000 00000 00000 00000",'N':"10001 11001 10101 10011 10001 10001 10001",
 'E':"11111 10000 10000 11110 10000 10000 11111",'S':"01111 10000 10000 01110 00001 00001 11110",
 'T':"11111 00100 00100 00100 00100 00100 00100",'.':"00000 00000 00000 00000 00000 00000 00100"}
def texto(c, x, y, t, col, esc=1, a=255):
    for ch in t:
        g = FONT[ch].split()
        for yy in range(7):
            for xx in range(5):
                if g[yy][xx] == '1': c.r(x+xx*esc, y+yy*esc, x+xx*esc+esc-1, y+yy*esc+esc-1, col, a)
        x += 6*esc
    return x
def tw(t, esc=1): return len(t)*6*esc - esc
def pinta(c, m, x, y, col, a=255):
    ys, xs = np.where(m)
    for yy, xx in zip(ys, xs): c.p(x+xx, y+yy, col, a)
def brilho(c, m, x, y, col, raio=3, a=70):
    d = nd.distance_transform_edt(~np.pad(m, raio))
    ys, xs = np.where((d > 0) & (d <= raio))
    for yy, xx in zip(ys, xs):
        t = 1-d[yy, xx]/(raio+1)
        if t > BAYER[yy % 4, xx % 4]*.8: c.p(x+xx-raio, y+yy-raio, col, int(a*t))
def neon_block(c, x, y, w, col=(150, 230, 255)):
    blk, wht = block_mask(w)
    borda = blk & ~nd.binary_erosion(blk)
    brilho(c, borda, x, y, col, 4, 90); pinta(c, blk, x, y, K0, 200); pinta(c, borda, x, y, col)
    pinta(c, borda & (np.add.outer(np.arange(blk.shape[0]), np.arange(blk.shape[1])) % 5 == 0), x, y, (255, 255, 255))
def lambe(c, x, y, w, h, papel=(226, 220, 204), rnd=random.Random(5)):
    for yy in range(h):
        for xx in range(w):
            col = papel if rnd.random() > .08 else mix(papel, K4, .4)
            c.p(x+xx, y+yy, col)
    for k in range(w//3): c.p(x+rnd.randrange(w), y+h-1, K2)  # rasgos
    c.r(x+w, y+1, x+w, y+h, K0, 140); c.r(x+1, y+h, x+w, y+h, K0, 140)
def cartaz(c, x, y, peca, w=34, h=50, rnd=random.Random(7)):
    lambe(c, x, y, w, h, (232, 226, 210), rnd)
    c.r(x, y, x+w-1, y+8, K0)
    m = hard_mask(w-4); pinta(c, m[:7], x+2, y+1, K7)
    im = Image.open(os.path.join(AQ, 'pecas', peca)); sc = (h-20)/im.height
    im = im.resize((max(1, int(im.width*sc)), h-20), Image.NEAREST); A = np.asarray(im)
    ox = x + (w-im.width)//2
    for yy in range(im.height):
        for xx in range(im.width):
            if A[yy, xx, 3] > 0: c.p(ox+xx, y+10+yy, tuple(A[yy, xx, :3]))
    texto(c, x+(w-tw('349'))//2, y+h-8, '349', VM)
    c.r(x-1, y-1, x+3, y+1, (220, 210, 170), 200); c.r(x+w-4, y-1, x+w, y+1, (220, 210, 170), 200)
def carrega(n): return C.__new__(C) if False else _de(Image.open(os.path.join(AQ, n)).convert('RGBA'))
def _de(im):
    c = C(im.width, im.height); c.a = np.array(im); return c

# --- fundos ---
c = carrega('bg1.png')  # O SALÃO DA BLOCK
neon_block(c, 12, 44, 46)
texto(c, 12, 84, 'BLOCK', (150, 230, 255)); brilho(c, np.ones((7, 29), bool), 12, 84, (150, 230, 255), 2, 40)
x = W-58; c.r(x-2, 40, x+50, 58, K0); c.r(x-2, 40, x+50, 40, K4)
texto(c, x+3, 43, '349', (255, 90, 70), 2); brilho(c, np.ones((14, 34), bool), x+3, 43, VM, 3, 50)
cartaz(c, 4, 150, 'p1.png'); cartaz(c, W-38, 140, 'p3.png'); cartaz(c, W-40, 200, 'p5.png', 34, 46)
m = hard_mask(76); pinta(c, m, 2, 330, K7, 150)   # lambe da HARD na parede, embaixo da arara
m = hard_mask(70); pinta(c, m, W-72, 300, K6, 120)
c.save('bg1.png')

c = carrega('bg2.png')  # HARD NA PAREDE
c.r(30, 42, W-31, 64, K0); c.r(31, 43, W-32, 63, (236, 232, 220))   # faixa no mezanino
for xx in range(30, W-30, 4): c.p(xx, 64+(xx//4) % 2, K0)
hm = hard_mask(110); pinta(c, hm, 38, 53-hm.shape[0]//2, K0)
texto(c, 156, 47, 'x', VM, 2)
blk, wht = block_mask(20); pinta(c, blk, 176, 44, K0)
texto(c, 199, 50, 'BLOCK', K0)
hm = hard_mask(160); g = hm  # pichação grande da HARD (spray com escorridos)
pinta(c, g, 55, 212, K6, 45)
ys, xs = np.where(g[-1:])
for xx in xs[::7]:
    for k in range(random.Random(int(xx)).randrange(4, 18)): c.p(55+xx, 212+g.shape[0]+k, K6, 35)
cartaz(c, 4, 300, 'p2.png', 30, 44); cartaz(c, W-34, 330, 'p6.png', 30, 44)
neon_block(c, W-44, 120, 36, (255, 120, 90)) if False else neon_block(c, W-42, 94+60, 34)
c.save('bg2.png')

c = carrega('bg3.png')  # INFERNO SANTO
hm = hard_mask(230)
brilho(c, hm, 20, 8, LR, 4, 110); pinta(c, hm, 20, 8, (255, 220, 150))
pinta(c, hm & np.roll(hm, -2, 0) == False, 20, 8, VM) if False else None
yy = np.arange(hm.shape[0])[:, None]
pinta(c, hm & (yy > hm.shape[0]*.6), 20, 8, LR)
neon_block(c, 6, 300, 30, (255, 150, 90)); neon_block(c, W-36, 280, 30, (255, 150, 90))
cartaz(c, 4, 200, 'p7.png', 28, 42); cartaz(c, W-32, 190, 'p8.png', 28, 42)
x = (W-tw('HARD x BLOCK'))//2; texto(c, x, 64, 'HARD x BLOCK', (255, 200, 120), 1, 220)
c.save('bg3.png')

# --- alvos ---
def tijolo(w, h, base):
    c = C(w, h, base); c.r(0, 0, w-1, 0, mix(base, K7, .25)); c.r(0, h-1, w-1, h-1, mix(base, K0, .5))
    c.r(0, 0, 0, h-1, mix(base, K7, .15)); c.r(w-1, 0, w-1, h-1, mix(base, K0, .5)); return c
c = tijolo(24, 12, K1)
m = hard_mask(80); col = m.any(0); xs = np.where(col)[0]
fim = xs[0]
while fim < len(col) and col[fim]: fim += 1
L = m[:, xs[0]:fim]; ys = np.where(L.any(1))[0]; L = L[ys[0]:ys[-1]+1]
sc = 9/L.shape[0]; L = np.asarray(Image.fromarray((L*255).astype(np.uint8)).resize((max(1, int(L.shape[1]*sc)), 9), Image.BOX)) > 90
pinta(c, L, (24-L.shape[1])//2, 1, K7); c.r(0,0,23,0,K5); c.r(0,11,23,11,K5); c.r(0,0,0,11,K5); c.r(23,0,23,11,K5); c.save('t-hard.png')
c = tijolo(24, 12, K6)
blk, wht = block_mask(13); pinta(c, blk, (24-blk.shape[1])//2, (12-blk.shape[0])//2, K0); pinta(c, wht, (24-blk.shape[1])//2, (12-blk.shape[0])//2, K7)
c.save('t-block.png')
c = tijolo(24, 12, (176, 128, 74))
c.r(10, 0, 12, 11, (212, 176, 120)); c.r(1, 3, 22, 3, (140, 98, 52), 120)
texto(c, 1, 3, 'H', K0) if False else None
for i, ch in enumerate('HxB'): pass
def mini(c, x, y, ch, col):
    F = {'H': "101 101 111 101 101", 'B': "110 101 110 101 110", 'x': "000 101 010 101 000"}[ch].split()
    for yy in range(5):
        for xx in range(3):
            if F[yy][xx] == '1': c.p(x+xx, y+yy, col)
mini(c, 2, 4, 'H', K0); mini(c, 6, 4, 'x', VM); mini(c, 16, 4, 'B', K0); mini(c, 19, 4, 'x', K1) if False else None
c.save('t-caixa.png')
c = C(24, 16); cartaz(c, 1, 1, 'p4.png', 21, 14, random.Random(3)) if False else None
c = C(24, 16, (232, 226, 210)); c.r(0, 0, 23, 3, K0)
c.r(0, 15, 23, 15, K3); c.r(23, 0, 23, 15, K3)
pinta(c, hard_mask(22)[:3], 1, 0, K7)
im = Image.open(os.path.join(AQ, 'pecas', 'p4.png')); im = im.resize((max(1, im.width*11//im.height), 11), Image.NEAREST); A = np.asarray(im)
for yy in range(A.shape[0]):
    for xx in range(A.shape[1]):
        if A[yy, xx, 3]: c.p((24-A.shape[1])//2+xx, 4+yy, tuple(A[yy, xx, :3]))
c.p(0, 4, VM); c.p(23, 4, VM); c.save('t-cartaz.png')

# --- banner e logo collab ---
def collab(w, h, hw, bw, bg):
    c = C(w, h, bg) if bg else C(w, h)
    hm = hard_mask(hw); blk, wht = block_mask(bw)
    xw = 14 if h < 50 else 22
    tot = hw + 10 + xw + 10 + bw; x0 = (w-tot)//2
    pinta(c, hm, x0, (h-hm.shape[0])//2, K7)
    xx = x0+hw+10; e = 2 if h < 50 else 3
    texto(c, xx + (xw-5*e)//2, (h-7*e)//2, 'x', VM, e)
    bx = xx+xw+10; by = (h-blk.shape[0])//2
    pinta(c, blk, bx, by, K7); pinta(c, wht, bx, by, K1)
    return c
c = collab(270, 36, 150, 34, K0)
c.r(0, 0, 269, 0, VM); c.r(0, 35, 269, 35, VM)
for xx in range(0, 270, 6): c.p(xx, 2, K3); c.p(xx+3, 33, K3)
c.save('banner.png')
c = collab(240, 90, 136, 50, None)
a = c.a; outline(a, K0); outline(a, K0)
c.save('logo-collab.png')


# ---------------- velas góticas ----------------
CERA, CERA2, CH1, CH2 = (240, 236, 222), (196, 190, 176), (255, 236, 160), LR
def vela(c, x, y, h, fr=0, halo=True):  # x = centro, y = base
    if halo:
        for yy in range(-14, 15):
            for xx in range(-14, 15):
                d = math.hypot(xx, yy*1.1)/14
                if d < 1 and (1-d)*.9 > BAYER[(y+yy) % 4, (x+xx) % 4]: c.p(x+xx, y-h-4+yy, (255, 150, 60), int(70*(1-d)))
    c.r(x-2, y-h, x+1, y, CERA); c.r(x+1, y-h, x+1, y, CERA2)
    c.r(x-3, y-h, x+2, y-h, CERA)
    for k, dx in enumerate((-3, 2, -1)):
        L = 2 + (h*(k+1)) % 5
        c.r(x+dx, y-h, x+dx, y-h+L, CERA if dx < 1 else CERA2)
    c.p(x, y-h-1, K0)
    fl = [(0, -2), (0, -3), (0, -4), (-1, -2), (1, -2), (0, -5) if fr == 0 else (1, -5), (0, -6) if fr == 0 else (-1, -4)]
    for dx, dy in fl: c.p(x+dx, y-h+dy-1, CH2)
    c.p(x, y-h-3, CH1); c.p(x, y-h-4, CH1)
def castical(c, x, y, h=10):
    c.r(x-4, y+1, x+3, y+2, K0); c.r(x-1, y-1, x, y, K0); c.r(x-3, y-2, x+2, y-2, K0)
    vela(c, x, y-3, h)
def candelabro(c, cx, y, larg=30, hv=9):
    c.r(cx-1, y, cx, y+40, K0); c.r(cx-6, y+40, cx+5, y+42, K0); c.r(cx-3, y+20, cx+2, y+22, K0)
    for t in range(-larg, larg+1):
        yy = y + int(10*(t/larg)**2) * -1 + 10
        c.p(cx+t, yy, K0); c.p(cx+t, yy+1, K0)
    for t in (-larg, -larg//2, 0, larg//2, larg):
        yy = y + 10 - int(10*(t/larg)**2)
        c.r(cx+t-2, yy-2, cx+t+2, yy-1, K0); vela(c, cx+t, yy-3, hv+(0 if t else 4))
def pendente(c, cx, y, r=22):  # lustre de ferro pendurado
    for yy in range(0, y): c.p(cx, yy, K0)
    for t in range(-r, r+1): c.p(cx+t, y+abs(t)//4, K0); c.p(cx+t, y+1+abs(t)//4, K0)
    for t in range(-r, r+1, r//2): vela(c, cx+t, y-1+abs(t)//4, 7)
for i in (1, 2):
    c = C(10, 20); c.r(2, 18, 7, 19, K0); c.r(4, 16, 5, 17, K0); c.r(3, 15, 6, 15, K0)
    vela(c, 5, 14, 7, i-1, halo=False); c.save(f'vela-{i}.png')
c = carrega('bg1.png'); castical(c, 50, 398, 12); castical(c, 60, 398, 7); castical(c, 222, 398, 10)
candelabro(c, 236, 220, 14, 7); c.save('bg1.png')
c = carrega('bg2.png')
for x in range(16, W, 50): castical(c, x, 69, 6 + x % 3*2)  # velas no parapeito do mezanino
castical(c, 20, 398, 12); castical(c, 250, 398, 9); castical(c, 240, 398, 5); c.save('bg2.png')
c = carrega('bg3.png')
pendente(c, 135, 92, 30)
candelabro(c, 26, 330, 18, 8); candelabro(c, W-26, 320, 18, 8)
for x in (6, 64, 200, 262): c.r(x-8, 270 + (x % 7), x+8, 272 + (x % 7), K0); castical(c, x, 268 + (x % 7), 6 + x % 4)  # prateleiras
for x in range(10, W, 23): castical(c, x, 404, 5 + (x*7) % 9)
c.save('bg3.png')

# ---------------- folha de contato ----------------
def folha():
    Z = 4
    nomes = sorted(f for f in os.listdir(AQ) if f.endswith('.png') and not f.startswith('_') and not f.startswith('bg'))
    nomes += ['pecas/' + f for f in sorted(os.listdir(os.path.join(AQ, 'pecas')))]
    ims = [(n, Image.open(os.path.join(AQ, n))) for n in nomes]
    Wf = 1200; x = y = 10; rowh = 0; pos = []
    for n, im in ims:
        w, h = im.width*Z, im.height*Z
        if x + w > Wf-10: x = 10; y += rowh + 24; rowh = 0
        pos.append((n, im, x, y)); x += w + 16; rowh = max(rowh, h)
    y += rowh + 30
    sh = Image.new('RGB', (Wf, y + 490), (24, 24, 30)); d = ImageDraw.Draw(sh)
    for n, im, x, yy in pos:
        big = im.resize((im.width*Z, im.height*Z), Image.NEAREST); sh.paste(big, (x, yy), big)
        d.text((x, yy + big.height + 2), n.replace('.png', ''), fill=(170, 170, 180))
    for i, b in enumerate(['bg1.png', 'bg2.png', 'bg3.png']):
        im = Image.open(os.path.join(AQ, b)); sh.paste(im, (10 + i*290, y), im)
        p = Image.open(os.path.join(AQ, 'paddle.png')); sh.paste(p, (10+i*290+111, y+440), p)
    sh.save(os.path.join(AQ, '_folha.png')); print(sh.size)
folha()

# ---------------- REVISÃO 2b: plataforma = tijolo do logo da BLOCK (16 px de altura) ----------------
def paddle_block(w, h, nome):  # hexágono achatado preto, contorno branco grosso, vão em "C" como no logo da Block
    c = C(w, h); ch = 5
    def dentro(x, y, m=0):
        return m <= y < h-m and m <= x < w-m and (x-m) + (y-m) >= ch-m*0 and (x-m) + (h-1-m-y) >= ch and (w-1-m-x) + (y-m) >= ch and (w-1-m-x) + (h-1-m-y) >= ch
    for y in range(h):
        for x in range(w):
            if dentro(x, y): c.p(x, y, K7)
            if dentro(x, y, 2): c.p(x, y, K0 if (x+y) % 7 else K1)
    x0 = int(w*.52)  # vão em C: caixa com contorno branco aberta para a direita
    c.r(x0, 4, w-3, h-5, K7); c.r(x0+2, 6, w-1, h-7, K0)
    c.r(w-3, 6, w-1, h-7, K0)
    c.r(x0-int(w*.12), 4, x0-int(w*.12)+1, h-5, K3)  # aresta da face
    c.save(nome)
paddle_block(52, 16, 'paddle.png'); paddle_block(76, 16, 'paddle-largo.png'); paddle_block(36, 16, 'paddle-curto.png')
folha()
