import os,hashlib,json,urllib.request,sys
T=open(sys.argv[1]).read().strip();root=sys.argv[2];TEAM='team_Htks1gLzoWIJFzYSGG9Vrjto'
def req(url,data=None,headers={},method=None):
    r=urllib.request.Request(url,data=data,headers={'Authorization':'Bearer '+T,**headers},method=method)
    try:
        with urllib.request.urlopen(r,timeout=300) as x: return x.status,x.read()
    except urllib.error.HTTPError as e: return e.code,e.read()
files=[]
for d,_,fs in os.walk(root):
    for f in fs:
        p=os.path.join(d,f);rel=os.path.relpath(p,root);b=open(p,'rb').read();sha=hashlib.sha1(b).hexdigest()
        st,body=req(f'https://api.vercel.com/v2/files?teamId={TEAM}',b,{'Content-Type':'application/octet-stream','x-vercel-digest':sha,'Content-Length':str(len(b))},'POST')
        if st not in (200,201): print('upload',rel,st,body[:200]);sys.exit(1)
        files.append({'file':rel,'sha':sha,'size':len(b)})
print('enviados',len(files))
payload={'name':'dra-victoria-oss-emer','project':'prj_0f0Uwnl0X3caWAIVWR1hwJxYViOH','target':'production','files':files,'projectSettings':{'framework':None}}
st,body=req(f'https://api.vercel.com/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1',json.dumps(payload).encode(),{'Content-Type':'application/json'},'POST')
d=json.loads(body);print(st,d.get('id'),d.get('url'),d.get('readyState'),d.get('error'))
