const {chromium}=require('playwright');(async()=>{const [dir,pat,scale,outdir]=process.argv.slice(2);const fs=require('fs');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:+scale});
for(const f of fs.readdirSync(dir).filter(f=>f.startsWith(pat)&&f.endsWith('.html')).sort()){await p.goto('file://'+dir+'/'+f);await p.waitForTimeout(250);await p.screenshot({path:outdir+'/'+f.replace('.html','.png')});}
await b.close();})();
