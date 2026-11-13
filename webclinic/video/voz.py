# Narração ElevenLabs eleven_v4 (voz Moutella), um take só, com tempo por palavra.
# Usa as funções de sva/tools/video/falas.py; a chave vem do .env do repositório sva (nunca imprimir).
import sys, json, subprocess
sys.path.insert(0,'/home/user/sva/tools'); sys.path.insert(0,'/home/user/sva/tools/video')
from lib import load_env
import falas
VOZ='X3j2R63Qu4Gdv6dsU2hB'  # Moutella - Brazilian Mentor
TEXTO=open('roteiro.txt').read().strip()
audio,palavras=falas.sintetizar_elevenlabs(TEXTO,VOZ,load_env()['ELEVENLABS_API_KEY'],modelo='eleven_v4')
open('public/voz-bruta.mp3','wb').write(audio)
json.dump(palavras,open('src/audio.json','w'),ensure_ascii=False,indent=0)
print(len(palavras), palavras[-1])
