# Monta dist/ para a Vercel: página completa (doctype) + assets + audio/card + shim do ranking + API.
import os, shutil
A=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(A,'..','game'); D=os.path.join(A,'dist')
shutil.rmtree(D,ignore_errors=True); os.makedirs(D)
html=open(os.path.join(G,'index.html'),encoding='utf-8').read()
cab='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta property="og:title" content="HARD × BLOCK"><meta property="og:description" content="Jogue o arcade da collab Hard Jeans Santo × Block Office."><script src="ranking-shim.js"></script></head><body style="margin:0;background:#0b0b0f">'
open(os.path.join(D,'index.html'),'w',encoding='utf-8').write(cab+html+'</body></html>')
for f in ('audio.js','card.js'): shutil.copy(os.path.join(G,f),D)
shutil.copytree(os.path.join(G,'assets'),os.path.join(D,'assets'),ignore=shutil.ignore_patterns('_*'))
for f in ('ranking-shim.js','package.json','vercel.json'): shutil.copy(os.path.join(A,f),D)
shutil.copytree(os.path.join(A,'api'),os.path.join(D,'api'))
print('dist ok')
