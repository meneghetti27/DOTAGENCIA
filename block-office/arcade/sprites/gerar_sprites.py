import glob, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as nd
# paleta do jogo: blackwork + concreto + veneno + chamas + jeans
PAL=["#0b0b0f","#1d1d24","#34343d","#55555f","#7b7b86","#a6a6ae","#d4d4d8","#f4f2ea",
     "#2f8f3a","#6fd16a","#6b3fa0","#a77be0","#c7261f","#f0662a","#ffc23d","#3c5a8a"]
pal=np.array([[int(c[i:i+2],16) for i in (1,3,5)] for c in PAL])
def sprite(path,H):
    im=Image.open(path).convert('RGB'); a=np.asarray(im).astype(int)
    fundo=(a.min(2)>232)
    lab,n=nd.label(fundo); borda=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
    m=~np.isin(lab,list(borda)); m=nd.binary_opening(m,iterations=2)
    l2,n2=nd.label(m); s=nd.sum(m,l2,range(1,n2+1)); m=l2==(np.argmax(s)+1); m=nd.binary_fill_holes(m)
    ys,xs=np.where(m); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
    w=max(1,round(a.shape[1]*H/a.shape[0]))
    small=np.asarray(Image.fromarray(a.astype(np.uint8)).resize((w,H),Image.BOX)).astype(int)
    ms=np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize((w,H),Image.BOX))>110
    d=((small[:,:,None,:]-pal[None,None])**2).sum(3); q=pal[d.argmin(2)]
    out=np.zeros((H+2,w+2,4),np.uint8); out[1:-1,1:-1,:3]=q; out[1:-1,1:-1,3]=ms*255
    mm=out[...,3]>0; cont=nd.binary_dilation(mm)&~mm; out[cont]=[244,242,234,255]
    borda_in=mm&~nd.binary_erosion(mm); out[borda_in&(out[...,:3].sum(2)<120)]=[85,85,95,255]
    return Image.fromarray(out,'RGBA')
LADO={'03':'02','04':'02','07':'02','01':'02','02':'02','05':'02'}
fs=[f.replace('foto-01',f"foto-{LADO.get(f.split('/')[1][:2],'01')}") for f in sorted(glob.glob('drop/0*/foto-01.webp'))]
for H in (48,64):
    for f in fs:
        sp=sprite(f,H); sp.save(f'sprites/{f.split("/")[1]}-{H}.png')
# folha de prévia em fundo de concreto escuro
Z=5; tiles=[]
for f in fs:
    n=f.split('/')[1]; tiles.append((n,Image.open(f'sprites/{n}-48.png'),Image.open(f'sprites/{n}-64.png')))
W=sum(max(t[1].width,t[2].width)*Z+40 for t in tiles)+40
sh=Image.new('RGB',(W,64*Z+48*Z+150),(34,34,40)); d=ImageDraw.Draw(sh); x=40
for n,a,b in tiles:
    sh.paste(a.resize((a.width*Z,a.height*Z),Image.NEAREST),(x,30),a.resize((a.width*Z,a.height*Z),Image.NEAREST))
    sh.paste(b.resize((b.width*Z,b.height*Z),Image.NEAREST),(x,48*Z+70),b.resize((b.width*Z,b.height*Z),Image.NEAREST))
    d.text((x,8),n[:22],fill=(200,200,200)); x+=max(a.width,b.width)*Z+40
d.text((10,48*Z+45),"48 px (em cima) · 64 px (embaixo) · ampliado 5x",fill=(255,200,80))
sh.save('sprites/previa.png'); print(sh.size)
