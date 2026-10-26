import json,sys,os,urllib.request
UA={'User-Agent':'DotDesign/1.0'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA)).read()
name=sys.argv[1]; res=sys.argv[2] if len(sys.argv)>2 else '2k'
d=json.loads(get(f'https://api.polyhaven.com/files/{name}'))
g=d['gltf'][res]['gltf']; base=f'models/{name}'; os.makedirs(base+'/textures',exist_ok=True)
open(f'{base}/{name}.gltf','wb').write(get(g['url']))
for p,i in g['include'].items():
    os.makedirs(os.path.dirname(f'{base}/{p}'),exist_ok=True); open(f'{base}/{p}','wb').write(get(i['url']))
print('ok',name)
