// renderiza os jobs de perfil-jobs.txt em 1080x1920 (1x)
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
for(const l of fs.readFileSync('perfil-jobs.txt','utf8').trim().split('\n')){const [h,o]=l.split(' ');await p.goto('file://'+process.cwd()+'/perfil-html/'+h);await p.waitForLoadState('networkidle');await p.waitForTimeout(150);await p.screenshot({path:'../perfil/'+o});}
await b.close();})();
