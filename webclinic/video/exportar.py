# exporta os vetores (V) e o logo redondo do gerador Python para o vídeo
import json, os
os.chdir('../gerador')
_s=open('posts40.py').read(); exec(_s[:_s.index('P=[]')])
os.chdir('../video')
json.dump({'V':V,'logo':roundlogo(240),'cur':CUR},open('src/vetores.json','w'),ensure_ascii=False)
print(len(V))
