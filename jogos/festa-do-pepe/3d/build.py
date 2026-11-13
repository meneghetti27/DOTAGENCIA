import base64,os,json
d=os.path.dirname(os.path.abspath(__file__))
tex={}
for f in sorted(os.listdir(os.path.join(d,'tex'))):
    if f.endswith('.jpg'):
        tex[f[:-4]]='data:image/jpeg;base64,'+base64.b64encode(open(os.path.join(d,'tex',f),'rb').read()).decode()
out=open(os.path.join(d,'shell.html')).read()
out+='<script>const TEXDATA='+json.dumps(tex)+';</script>\n<script>\n'+open(os.path.join(d,'game.js')).read()+'\n</script>\n'
open(os.path.join(d,'index.html'),'w').write(out)
print(len(out)//1024,'KB')
