// renderiza stories-html/*.html (lista em stories-jobs.txt) em 1080x1920 -> pasta de saída
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const out=process.argv[2]||'out-st';fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
for(const h of fs.readFileSync('stories-jobs.txt','utf8').trim().split('\n')){await p.goto('file://'+process.cwd()+'/stories-html/'+h);await p.evaluate(()=>document.fonts.ready);await p.waitForLoadState('networkidle');await p.waitForTimeout(200);await p.screenshot({path:out+'/'+h.replace('.html','.png')});}
await b.close();})();
